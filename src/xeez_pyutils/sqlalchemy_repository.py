from typing import Any, List, Type, TypeVar

from fastapi.logger import logger
from pydantic import BaseModel, ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from .exceptions import (
    DatabaseError,
    DatabaseIntegrityError,
    InternalServerError,
)
from .protocols.repository_protocol import RepositoryProtocol

ModelType = TypeVar("ModelType", bound=BaseModel)


class SQLAlchemyRepository(RepositoryProtocol[ModelType]):
    """
    Repositório para interação com o banco de dados utilizando SQLAlchemy.

    Este repositório fornece métodos genéricos para executar operações CRUD em um modelo específico.

    Args:
        session (Session): Sessão do SQLAlchemy para interagir com o banco de dados.
        model_type (Type[ModelType]): O tipo de modelo associado ao repositório.

    Attributes:
        session (Session): Sessão do SQLAlchemy para interagir com o banco de dados.
        model_type (Type[ModelType]): O tipo de modelo associado ao repositório.
    """

    def __init__(self, session: Session, model_type: Type[ModelType]):
        self.session = session
        self.model_type = model_type

    def get(self, model_type: Type[ModelType], id: Any) -> ModelType | None:
        """
        Obtém um objeto do banco de dados pelo ID.

        Args:
            id (Any): O ID do objeto a ser obtido.

        Returns:
            Any: O objeto obtido, se encontrado; caso contrário, None.
        """
        try:
            result = (
                self.session.query(self.model_type or model_type)
                .filter_by(id=id)
                .first()
            )
            return result
        except IntegrityError as e:
            self.session.rollback()
            logger.error("Erro de Integridade do Banco de Dados: %s", e)
            raise DatabaseIntegrityError(e.args)
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error("Erro do Banco de Dados: %s", e)
            raise DatabaseError(e.args)

    def get_multi(
        self, model_type: Type[ModelType], skip: int = 0, limit: int = 10
    ) -> List[ModelType]:
        """
        Obtém vários objetos do banco de dados com opções de paginação.

        Args:
            model_type (ModelType):
            skip (int): O número de objetos a serem pulados.
            limit (int): O número máximo de objetos a serem obtidos.

        Returns:
            List[Any]: Uma lista de objetos obtidos.
        """
        try:
            result = (
                self.session.query(self.model_type or model_type)
                .offset(skip)
                .limit(limit)
                .all()
            )
            return result
        except IntegrityError as e:
            self.session.rollback()
            logger.error("Erro de Integridade do Banco de Dados: %s", e)
            raise DatabaseIntegrityError(e.args)
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error("Erro do Banco de Dados: %s", e)
            raise DatabaseError(e.args)

    def create(self, db_obj: ModelType, obj_in: dict[str, Any]) -> ModelType:
        """
        Cria um novo objeto no banco de dados.

        Args:
            db_obj (ModelType): O objeto a ser criado.
            obj_in (dict[str, Any]): Os dados do objeto a serem utilizados na criação.

        Returns:
            Any: O objeto criado.
        """
        try:
            db_obj = self.model_type(**obj_in)
            self.session.add(db_obj)
            self.session.commit()
            self.session.refresh(db_obj)
            return db_obj
        except ValidationError as e:
            raise InternalServerError(
                "Erro inesperado ao fazer o parsing para o modelo", e.args
            )
        except IntegrityError as e:
            self.session.rollback()
            logger.error("Erro de Integridade do Banco de Dados: %s", e)
            raise DatabaseIntegrityError(e.args)
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error("Erro do Banco de Dados: %s", e)
            raise DatabaseError(e.args)

    def update(self, db_obj: ModelType, obj_in: dict[str, Any]) -> None:
        """
        Atualiza um objeto existente no banco de dados.

        Args:
            db_obj (ModelType): O objeto a ser atualizado.
            obj_in (dict[str, Any]): Os novos dados do objeto.

        Returns:
            None
        """
        try:
            for key, value in obj_in.items():
                setattr(db_obj, key, value)
            self.session.add(db_obj)
            self.session.commit()
            self.session.refresh(db_obj)
        except IntegrityError as e:
            self.session.rollback()
            logger.error("Erro de Integridade do Banco de Dados: %s", e)
            raise DatabaseIntegrityError(e.args)
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error("Erro do Banco de Dados: %s", e)
            raise DatabaseError(e.args)

    def delete(self, db_obj: ModelType) -> None:
        """
        Exclui um objeto do banco de dados.

        Args:
            db_obj (ModelType): O objeto a ser excluído.

        Returns:
            None
        """
        try:
            self.session.delete(db_obj)
            self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
            logger.error("Erro de Integridade do Banco de Dados: %s", e)
            raise DatabaseIntegrityError(e.args)
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error("Erro do Banco de Dados: %s", e)
            raise DatabaseError(e.args)
