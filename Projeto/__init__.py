##__init__.py
import os
from flask import Flask, render_template, request, flash, redirect, url_for 
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

app = Flask(__name__)
db = SQLAlchemy() 

def create_app(test_config=None):
    # cria e configura o app
    app = Flask(__name__,
                template_folder=os.path.join(os.path.dirname(__file__),"templates"),
                instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='mysql+pymysql://henry:55631376@127.0.0.1/lili',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    
    if test_config is None:
        # abre a instancia config, se este não existir, quando não exixtir
        app.config.from_pyfile('config.py', silent=True)
    else:
        # abre o test config se passado o argumento
        app.config.from_mapping(test_config)

    # garantir a instancia se a pasta existir
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # inicializa banco
    db.init_app(app)
    # import routes e modelos
    with app.app_context():
        from . import models

    from .models import Cardapio, Pessoa, User, Fone
        
    # inicializa o Swagger com a Configuração personalizada do Swagger
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "API do Sistema Lili",
            "description": "Documentação interativa das rotas do sistema de cardápio e cadastro.",
            "version": "1.0.0",
            "contact": {
                "responsible": "Henry Fernando Espindola Marcondes",
                "email": "raizmaker@gmail.com",
            },
            "license": {
                "name": "GNU GENERAL PUBLIC LICENSE",
                "url": "https://fsf.org/"
            }
        },
        "basePath": "/",  # Rota base da API
        "schemes": [
            "http"
        ],
    }

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec_1",
                "route": "/apispec_1.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
        "swagger_ui_bundle_js": "//unpkg.com/swagger-ui-dist/swagger-ui-bundle.js",
        "swagger_ui_standalone_preset_js": "//unpkg.com/swagger-ui-dist/swagger-ui-standalone-preset.js",
        "swagger_ui_css": "//unpkg.com/swagger-ui-dist/swagger-ui.css",
        "layout": "Material"
    }

    Swagger(app, template=swagger_template, config=swagger_config)
    
    # Importa modelos dentro do contexto
    #with app.app_context():
        #from Projeto import models
       

    # Página Vitrine
    @app.route("/vitrine")
    def vitrine():
        """
        Página Vitrine
        ---
        tags:
          - Produtos
        responses:
          200:
            description: Lista todos os produtos cadastrados
        """
        produtos = Cardapio.query.all()
        return render_template("vitrine.html", produtos=produtos)
        #return {"produtos": [(p.Nome, p.gramatura,p.imagem) for p in produtos]}


    # Cadastro de Usuário (não salva ainda, apenas flash)
    @app.route("/cadastro", methods=["GET", "POST"])
    def cadastro():
        if request.method == "POST":
            nome = request.form.get("nome")            # Tabela: Pessoa[1]: nome
            sobrenome = request.form.get("sobrenome")  # Tabela: Pessoa[2]: sobrenome
            email = request.form.get("email")          # Tabela: User[2]: email
            whatsApp = request.form.get("whatsapp")    # Tabela: Fone[1]: fone
            user = request.form.get("user")            # Tabela: User[1]: username
            login = request.form.get("login")          # Tabela: User[3]: password
            confirm_login = request.form.get("confirm-login")

            if not nome or not whatsApp:
                flash("Preencha Nome e whatsApp")
            elif login != confirm_login:
                flash("Senhas diferentes")
            else:
                # Verifique se o 'username' já existe no banco de dados
                existing_user = User.query.filter_by(username=user).first()
                if existing_user:
                    flash("Nome de usuário já existe", "error")
                else:
                    # Cria Pessoa
                    nova_pessoa = Pessoa(nome=nome,sobrenome=sobrenome)                  
                    db.session.add(nova_pessoa)
                    db.session.flush()  # para pegar o id da pessoa antes do commit

                    # Cria User
                    novo_user = User(username=user, email=email,password=login,
                                     pessoa_id=nova_pessoa.id_pessoa)
                    db.session.add(novo_user)
                    db.session.flush() # pegar o id do usuário

                   # Atualiza Pessoa.id_usuario com o id do User recém criado
                    nova_pessoa.id_usuario = novo_user.idUser
                    db.session.add(nova_pessoa)  # marca como "dirty" para update 

                    # Cria Fone
                    novo_fone = Fone(fone=whatsApp,pessoa_id=nova_pessoa.id_pessoa)
                    db.session.add(novo_fone)

                    # Commit no banco
                    db.session.commit()

                   

                flash(f"Usuário {nome} cadastrado com sucesso!", "success")
                return redirect(url_for("cadastro"))

        return render_template("cadastro.html")


    
    @app.route("/Cardapio")
    def cardapio():
        """
        Lista o cardápio
        ---
        tags:
          - Cardápio
        responses:
          200:
            description: Lista dos itens do cardápio em texto simples
        """
        from Projeto.models import Cardapio
        itens = Cardapio.query.all()
        return "<br>".join([f"{c.id_cardapio} - {c.Nome} - {c.gramatura}g" for c in itens])

    return app
