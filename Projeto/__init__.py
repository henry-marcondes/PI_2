import os
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

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

    # cria uma simples página
    @app.route("/Cardapio")
    def Cardapio():
        return " Faça seu Pedido: CARDAPIO"
    return app
