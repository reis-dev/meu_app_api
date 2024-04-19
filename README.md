# Minha API

Este pequeno projeto é a atividade proposta para o MVP da disciplina Desenvolvimento Full Stack Básico

O projeto apresenta uma API voltada para uma concessionária de carros onde são inseridas informações sobre os veículos, e abaixa tais informações serao apresentadas em forma de lista.

O objetivo aqui é ilutsrar o conteúdo apresentado ao longo das três aulas da disciplina.

---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.


> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
