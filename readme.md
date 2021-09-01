## 🔥 API Firetest

As API's do APP são responsáveis pelo controle de questões e usuários. Também é responsável por cruzar estas informações para retirar a métrica dos acertos e erros. Desenvolvida com **python 3.8** e **FastApi**. Nosso ambiente cloud é composto por um Heroku Dyno integrado com o github via Docker. Usamos um banco Postgres da Heroku para gestão de usuários e um Mongo DB no Atlas para a gestão das questões.

### DTO Questões

As questões são extraidas com o código do nosso notebook python, salvo localmente em DataFrames Pandas e exportados em CSV, o JSON da questão é salvo no banco documental mongo.

```json
{
    "_id": "",
    "subject": "",
    "module": "",
    "details": "",
    "enunciation": "",
    "options": {
        "a": {
            "answer": "",
            "answer_correct": false
        },
        "b": {
            "answer": "",
            "answer_correct": false
        },
        "c": {
            "answer": "",
            "answer_correct": false
        },
        "d": {
            "answer": "",
            "answer_correct": true
        },
        "e": {
            "answer": "",
            "answer_correct": false
        }
    },
    "resources": [
        {
            "resource_type": "", // image or HTML
            "resource_content": "" // HTML or Image URL
        }
    ] 
}
```