from pydantic import BaseModel
from typing import Optional, List
from model.carro import Carro

from schemas import ComentarioSchema


class CarroSchema(BaseModel):
    """ Define como um novo carro a ser inserido deve ser representado
    """
    modelo: str = "Gol"
    placa: str = "lje3888"
    valor: float = 15000.00
    cor: str = "Azul"
    ano: int = 1988


class CarroBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita com base no modelo do carro.
    """
    modelo: str = "Insira o modelo do carro."

class CarroBuscaDelSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca
       que sera feita com base na placa do carro para a deleção no banco de dados.
    """
    placa: str = "Insira a placa do carro"


class ListagemCarrosSchema(BaseModel):
    """ Define como uma listagem de carros será retornada.
    """
    carros:List[CarroSchema]


def apresenta_carros(carros: List[Carro]):
    """ Retorna uma representação do carro seguindo o schema definido em
        CarroViewSchema.
    """
    result = []
    for carro in carros:
        result.append({
            "modelo": carro.modelo,
            "placa": carro.placa,
            "valor": carro.valor,
            "cor": carro.cor,
            "ano": carro.ano,
        })

    return {"carro": result}


class CarroViewSchema(BaseModel):
    """ Define como um carro será retornado: carro + comentários.
    """
    id: int = 1
    modelo: str = "Gol"
    placa: str = "lje3888"
    valor: float = 15.000
    cor: str = "Azul"
    ano: int = 1988
    total_cometarios: int = 1
    comentarios:List[ComentarioSchema]


class CarroDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    placa: str

def apresenta_carro(carro: Carro):
    """ Retorna uma representação do carro seguindo o schema definido em
        CarroViewSchema.
    """
    return {
        "id": carro.id,
        "modelo": carro.modelo,
        "placa": carro.placa,
        "valor": carro.valor,
        "cor": carro.cor,
        "ano": carro.ano,
        "total_cometarios": len(carro.comentarios),
        "comentarios": [{"texto": c.texto} for c in carro.comentarios]
    }
