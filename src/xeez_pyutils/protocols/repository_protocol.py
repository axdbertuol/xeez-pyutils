from typing import Any, Generic, List, Protocol, Type, TypeVar

from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class Transactional(Protocol, Generic[ModelType]):
    """
    Protocolo para operações transacionais (criação, atualização, exclusão).

    Este protocolo define a interface para a criação, atualização e exclusão
    de objetos no banco de dados.
    """

    def create(self, db_obj: ModelType, obj_in: dict[str, Any]) -> ModelType:
        """
        Cria um novo objeto no banco de dados.

        Parâmetros:
        - db_obj (ModelType): O objeto do banco de dados.
        - obj_in (dict): Um dicionário contendo os dados para criar o objeto.

        Retorna:
        - ModelType: O objeto criado.
        """
        ...

    def update(self, db_obj: ModelType, obj_in: dict[str, Any]) -> None:
        """
        Atualiza um objeto existente no banco de dados.

        Parâmetros:
        - db_obj (ModelType): O objeto existente a ser atualizado.
        - obj_in (dict): Um dicionário contendo os dados para atualizar o objeto.

        Retorna:
        - None
        """
        ...

    def delete(self, db_obj: ModelType) -> None:
        """
        Deleta um objeto do banco de dados.

        Parâmetros:
        - db_obj (ModelType): O objeto a ser deletado.

        Retorna:
        - None
        """
        ...


class GenericReadable(Protocol, Generic[ModelType]):
    """
    Protocolo para operações de leitura genéricas.

    Este protocolo define a interface para obter objetos do banco de dados,
    suportando a obtenção de um único objeto por ID e a obtenção de múltiplos objetos
    com paginação.
    """

    def get(self, model_type: Type[ModelType], id: Any) -> ModelType | None:
        """
        Obtém um único objeto pelo seu ID.

        Parâmetros:
        - id (Any): O ID do objeto a ser recuperado.

        Retorna:
        - ModelType: O objeto recuperado;
        - None
        """
        ...

    def get_multi(
        self, model_type: Type[ModelType], skip: int = 0, limit: int = 10
    ) -> List[ModelType]:
        """
        Obtém uma lista de objetos, com suporte para paginação.

        Parâmetros:
        - model_type (ModelType): O tipo do modelo.
        - skip (int): Número de registros a serem ignorados (padrão é 0).
        - limit (int): Número máximo de registros a serem retornados (padrão é 10).

        Retorna:
        - List[ModelType]: Uma lista de objetos.
        """
        ...


class Readable(Protocol, Generic[ModelType]):
    """
    Protocolo para operações de leitura.

    Este protocolo define a interface para obter objetos do banco de dados,
    suportando a obtenção de um único objeto por ID e a obtenção de múltiplos objetos
    com paginação.
    """

    def get(self, id: Any) -> ModelType | None:
        """
        Obtém um único objeto pelo seu ID.

        Parâmetros:
        - id (Any): O ID do objeto a ser recuperado.

        Retorna:
        - ModelType: O objeto recuperado;
        - None
        """
        ...

    def get_multi(self, skip: int = 0, limit: int = 10) -> List[ModelType]:
        """
        Obtém uma lista de objetos, com suporte para paginação.

        Parâmetros:
        - skip (int): Número de registros a serem ignorados (padrão é 0).
        - limit (int): Número máximo de registros a serem retornados (padrão é 10).

        Retorna:
        - List[ModelType]: Uma lista de objetos.
        """
        ...


class RepositoryProtocol(
    Transactional[ModelType], GenericReadable[ModelType], Protocol
):
    """
    Protocolo de Repositório para operações CRUD básicas.

    Um Repositório é a camada mais próxima do banco de dados, é aqui que devem ser feitas as queries/transactions.

    Este protocolo define a interface que deve ser implementada por qualquer repositório
    que realiza operações de CRUD (Create, Read, Update, Delete) em um tipo de modelo específico.

    Métodos:
    - get(id: Any) -> ModelType | None: Obtém um único objeto pelo seu ID.
    - get_multi(skip: int = 0, limit: int = 10) -> List[ModelType]: Obtém uma lista de objetos, com suporte para paginação.
    - create(db_obj: ModelType, obj_in: dict) -> ModelType: Cria um novo objeto no banco de dados.
    - update(db_obj: ModelType, obj_in: dict) -> None: Atualiza um objeto existente no banco de dados.
    - delete(db_obj: ModelType) -> None: Deleta um objeto do banco de dados.
    """
