from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Carro, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
carro_tag = Tag(name="Carro", description="Adição, visualização e remoção de carros à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um carro cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/carro', tags=[carro_tag],
          responses={"200": CarroViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_carro(form: CarroSchema):
    """Adiciona um novo Carro à base de dados

    Retorna uma representação dos carros e comentários associados.
    """
    carro = Carro(
        modelo=form.modelo,
        placa=form.placa,
        valor=form.valor,
        cor=form.cor,
        ano=form.ano)
    logger.debug(f"Adicionando carro de placa: '{carro.placa}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando carro
        session.add(carro)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado carro de placa: '{carro.placa}'")
        return apresenta_carro(carro), 200

    except IntegrityError as e:
        # como a duplicidade da placa é a provável razão do IntegrityError
        error_msg = "Carro de mesma placa já salvo na base :/"
        logger.warning(f"Erro ao adicionar carro '{carro.placa}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo carro :/"
        logger.warning(f"Erro ao adicionar carro de placa'{carro.placa}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/carros', tags=[carro_tag],
         responses={"200": ListagemCarrosSchema, "404": ErrorSchema})
def get_carros():
    """Faz a busca por todos os Carros cadastrados

    Retorna uma representação da listagem de carros.
    """
    logger.debug(f"Coletando carros ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    carros = session.query(Carro).all()

    if not carros:
        # se não há carros cadastrados
        return {"carros": []}, 200
    else:
        logger.debug(f"%d carros econtrados" % len(carros))
        # retorna a representação de carro
        print(carros)
        return apresenta_carros(carros), 200


@app.get('/carro', tags=[carro_tag],
         responses={"200": CarroViewSchema, "404": ErrorSchema})
def get_carro(query: CarroBuscaSchema):
    """Faz a busca por um Carro a partir do modelo do carro

    Retorna uma representação dos carros e comentários associados.
    """
    carro_modelo = query.modelo
    logger.debug(f"Coletando dados sobre carro #{carro_modelo}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    carro = session.query(Carro).filter(Carro.modelo == carro_modelo).first()

    if not carro:
        # se o carro não foi encontrado
        error_msg = "Carro não encontrado na base :/"
        logger.warning(f"Erro ao buscar carro '{carro_modelo}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Carro econtrado: '{carro.modelo}'")
        # retorna a representação do carro
        return apresenta_carro(carro), 200


@app.delete('/carro', tags=[carro_tag],
            responses={"200": CarroDelSchema, "404": ErrorSchema})
def del_carro(query: CarroBuscaDelSchema):
    """Deleta um Carro a partir da placa do carro informado
       Retorna uma mensagem de confirmação da remoção.
    """
    carro_placa = unquote(unquote(query.placa))
    print(carro_placa)
    logger.debug(f"Deletando dados sobre carro #{carro_placa}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Carro).filter(Carro.placa == carro_placa).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado carro de placa #{carro_placa}")
        return {"mesage": "Carro removido", "id": carro_placa}
    else:
        # se o carro não foi encontrado
        error_msg = "Carro não encontrado na base :/"
        logger.warning(f"Erro ao deletar carro #'{carro_placa}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/cometario', tags=[comentario_tag],
          responses={"200": CarroViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """Adiciona de um novo comentário à um carro cadastrado na base identificado pelo id

    Retorna uma representação dos carros e comentários associados.
    """
    carro_id  = form.carro_id
    logger.debug(f"Adicionando comentários ao carro #{carro_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo carro
    carro = session.query(Carro).filter(Carro.id == carro_id).first()

    if not carro:
        # se o carro não for encontrado
        error_msg = "Carro não encontrado na base :/"
        logger.warning(f"Erro ao adicionar comentário ao carro '{carro_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o comentário
    texto = form.texto
    comentario = Comentario(texto)

    # adicionando o comentário ao carro
    carro.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário ao carro #{carro_id}")

    # retorna a representação de carro
    return apresenta_carro(carro), 200
