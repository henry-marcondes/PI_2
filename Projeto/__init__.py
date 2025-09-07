import os
from flask import Flask, render_template, request, redirect, url_for, flash 
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

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
    # inicializa o Swagger
    Swagger(app)
    
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
            description: Página de Cadastro de Cientes

        """
        if request.method == "POST":
            nome = request.form.get("nome")
            email = request.form.get("email")
            whatsApp = request.form.get("whatsApp")
            user = request.form.get("usuário")
            login = request.form.get("Senha")

            if not nome or not whatsApp:
                flash("Preencha Nome e whatsApp")
            else:
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

    return app
