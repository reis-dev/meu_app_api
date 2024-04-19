from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Comentario


class Carro(Base):
    __tablename__ = 'carro'

    id = Column("pk_carro", Integer, primary_key=True)
    modelo = Column(String(25))
    placa = Column(String(8), unique=True)
    valor = Column(Float)
    cor = Column(String(30))
    ano = Column(Integer)
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o carro e o comentário.
    # Essa relação é implicita, não está salva na tabela 'carro',
    # mas aqui e assim como foi ensinado em aula deixarei para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comentarios = relationship("Comentario")

    def __init__(self, modelo:str, placa:str, valor:float, cor:str, ano:int,  
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Carro

        Arguments:
            modelo: modelo do carro.
            placa: placa de registro do veículo
            valor: valor considerado para venda do carro
            cor: cor do veículo
            data_insercao: data de quando o carro foi inserido à base
        """
        self.modelo = modelo
        self.placa = placa
        self.valor = valor
        self.cor = cor
        self.ano = ano

        # será sempre o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário ao Carro
        """
        self.comentarios.append(comentario)

