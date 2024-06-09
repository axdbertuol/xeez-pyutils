from typing import Union


class CommonQueryParams:
    """
    Classe para representar parâmetros de consulta comuns.

    Esta classe encapsula os parâmetros de consulta que são comumente usados
    em endpoints, como parâmetros de pesquisa, salto e limite.

    Attributes:
        q (Union[str, None]): Parâmetro de consulta de pesquisa.
        skip (int): Número de registros a serem ignorados.
        limit (int): Número máximo de registros a serem retornados.
    """

    def __init__(self, q: Union[str, None] = None, skip: int = 0, limit: int = 10):
        """
        Inicializa os parâmetros de consulta comuns.

        Args:
            q (Union[str, None], optional): Parâmetro de consulta de pesquisa. Padrão é None.
            skip (int, optional): Número de registros a serem ignorados. Padrão é 0.
            limit (int, optional): Número máximo de registros a serem retornados. Padrão é 10.
        """
        self.q = q
        self.skip = skip
        self.limit = limit
