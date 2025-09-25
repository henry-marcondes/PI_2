#backup.py

import os
from flask import Flask, render_template, request, flash 
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

app = Flask(__name__)
db = SQLAlchemy() 

def create_app(test_config=None):
    # cria e configura o app
    app = Flask(__name__, instance_relative_config=True)
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

    with app.app_context():
        conn = db.engine.connect()
    

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
    with app.app_context():
        db.Model.metadata.reflect(bind=db.engine)
        from Projeto import models
        # Link explícito da tabela refletida para a classe
        models.Cardapio.__table__ = db.Model.metadata.tables["Cardapio"]

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
        from Projeto.models import Cardapio
        produtos = Cardapio.query.all()
        return render_template("vitrine.html", produtos=produtos)
    
    # Cadastro de Usuário (não salva ainda, apenas flash)
    @app.route("/cadastro", methods=["GET", "POST"])
    def cadastro():
        """
        Página Cadastro
        ---
        tags:
            - Usuários
        parameters:
          - name: nome
            in: formData
            type: string
            required: true
          - name: email
            in: formData
            type: string
            required: true
          - name: whatsApp
            in: formData
            type: sring
            required: false
          - name: user
            in: formData
            type: sring
            required: false
          - name: login
            in: formData
            type: sring
            required: false
        responses:
          200:
            description: Página de Cadastro de Clientes

        """
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
                # Se não existir, insira os dados do formulário no banco de dados
                # Se existir, exiba uma mensagem de erro
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM User WHERE username = %s", (user,))
                result = cursor.fetchone()
                if result:
                    flash("Nome de Usuário já existe, escolha outro.")
                else:
            #     # Insira os dados do formulário no banco de dados
                    cursor.execute("INSERT INTO Pessoa (nome, sobrenome) VALUES (%s, %s)", (nome, sobrenome))
                    conn.commit()
                    id_pessoa = cursor.lastrowid
                    print(id_pessoa)
                    cursor.execute("INSERT INTO Fone (pessoa_id, fone) VALUES (%s, %s)", (id_pessoa, whatsApp))
                    conn.commit()
                    cursor.execute("INSERT INTO User (username, email, password, pessoa_id) VALUES (%s, %s, %s, %s)", (user, email,login, id_pessoa))
                    conn.commit()
                    conn.close()

                    flash(f"Ususário {nome} cadastrado com sucesso!")

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

    return app, conn

