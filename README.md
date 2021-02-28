# API TEST backend

Criando uma API REST em Python + Flask




### Prerequisites

-Python 3.6.2;
-Criar ambiente virtual (venv);
-Instalar módulos: flask, flask_sqlalchemy, flask_jwt_extended, flask_restful;



### Installing

Utilizando Ubuntu 16 e seguindo instruções do Django Girls Tutorial: https://tutorial.djangogirls.org/pt/django/

```
1- Clonar o repositório;
2- Acesse o diretório do seu projeto e execute:
  python3 -m venv myvenv
3- Ative o ambiente através da linha de comando:
  source venv/bin/activate
4-  Para iniciar o servidor : FLASK_APP=run.py FLASK_DEBUG=1 flask run
5- Em um software como por exemplo Postman, é possível testar os endpoints criados;
6- No caso do endpoint exigir o token: vá na aba Header e crie: key=Authorization, value=Bearer "token"
substituindo "token" pelo access_token recebido no cadastro ou login de usuário.
```


