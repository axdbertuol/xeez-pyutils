from typing import Generic, List, Protocol, TypeVar

from pydantic import BaseModel
from src.common import CommonQueryParams

SchemaType = TypeVar("SchemaType", bound=BaseModel)


class ServiceProtocol(Protocol, Generic[SchemaType]):
    """
    Protocolo de Serviço para operações CRUD com validação de esquema.

    Um Serviço é a camada que fica entre um Router e um Repositório, tendo variadas funções como lidar
    com a regra de négocio específica, lidar com erros ou enviar mensagens para uma Mensageria.

    Este protocolo define a interface que deve ser implementada por qualquer serviço
    que realiza operações de CRUD (Criar, Ler, Atualizar, Deletar) em um tipo de esquema específico,
    utilizando um repositório para as operações de banco de dados.

    Métodos:
    - create_item(body: SchemaType) -> SchemaType: Cria um novo item.
    - fetch_item(item_id: int) -> SchemaType: Busca um item pelo seu ID.
    - fetch_many_items(q: CommonQueryParams) -> List[SchemaType]: Busca múltiplos itens com suporte a paginação.
    - update_item(item_id: int, body: SchemaType) -> None: Atualiza um item existente.
    - delete_item(item_id: int) -> None: Deleta um item pelo seu ID.
    """

    def create_item(self, body: SchemaType) -> SchemaType:
        """
        Cria um novo item.

        Parâmetros:
        - body (SchemaType): O corpo do item a ser criado, conforme o esquema.

        Retorna:
        - SchemaType: O item criado.
        """
        ...

    def fetch_item(self, item_id: int) -> SchemaType:
        """
        Busca um item pelo seu ID.

        Parâmetros:
        - item_id (int): O ID do item a ser buscado.

        Retorna:
        - SchemaType: O item encontrado.
        """
        ...

    def fetch_many_items(self, q: CommonQueryParams) -> List[SchemaType]:
        """
        Busca múltiplos itens com suporte a paginação.

        Parâmetros:
        - q (CommonQueryParams): Parâmetros de consulta comuns para paginação e filtragem.

        Retorna:
        - List[SchemaType]: Uma lista de itens conforme o esquema.
        """
        ...

    def update_item(self, item_id: int, body: SchemaType) -> None:
        """
        Atualiza um item existente.

        Parâmetros:
        - item_id (int): O ID do item a ser atualizado.
        - body (SchemaType): O corpo do item com os dados atualizados, conforme o esquema.

        Retorna:
        - None
        """
        ...

    def delete_item(self, item_id: int) -> None:
        """
        Deleta um item pelo seu ID.

        Parâmetros:
        - item_id (int): O ID do item a ser deletado.

        Retorna:
        - None
        """
        ...
