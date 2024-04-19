from pydantic import BaseModel


class ComentarioSchema(BaseModel):
    """ Define como um novo comentário a ser inserido deve ser representado
    """
    carro_id: int = 1
    texto: str = "Pesquisar se o preço segue o valor de mercado!"
