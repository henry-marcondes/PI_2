##__init__.py
from datetime import datetime
import os
from flask import Flask, render_template, request, flash, redirect, url_for 
from flask_sqlalchemy import SQLAlchemy
from flask import session
import re

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

    from .models import Cardapio, Pessoa, User, Fone, Endereco
        
   

    # Página Vitrine
    @app.route("/vitrine")
    def vitrine():
       
        produtos = Cardapio.query.all()
        return render_template("vitrine.html", produtos=produtos)


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

                    # Redireciona para a vitrine
                flash(f"Usuário {nome} cadastrado com sucesso!", "success")
                return redirect(url_for("vitrine"))

        return render_template("cadastro.html")


    
    @app.route("/cardapio")
    def cardapio():
       
        from Projeto.models import Cardapio
        itens = Cardapio.query.all()
        return "<br>".join([f"{c.id_cardapio} - {c.Nome} - {c.gramatura}g" for c in itens])
    
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            user = request.form.get("user")
            #login_senha = request.form.get("password")
            login_senha = request.form.get("login")  # melhor renomear para não confundir

            if not user or not login_senha:
                flash("Preencha Nome de Usuário e Senha", "error")
            else:
                usuario = User.query.filter_by(username=user).first()
                if usuario and User.query.filter_by(password = login_senha ):
                    session["user_id"] = usuario.idUser
                    session["pessoa_id"] = usuario.pessoa_id
                    flash(f"Usuário {usuario.username} logado com sucesso!", "success")
                    return redirect(url_for("usuario", usiario=usuario.username))  # redireciona para a página do usuário
                else:
                    flash("Usuário ou Senha inválidos", "error")

        return render_template("login.html")
    
    @app.route("/usuario", methods=["GET", "POST"])
    def usuario():
        user_id = session.get("user_id")
        if not user_id:
            flash("Usuário não autenticado.")
            return redirect(url_for("login"))

        #  Busca usuário e pessoa
        usuario = User.query.get(user_id)
        if not usuario:
            flash("Usuário não encontrado.")
            return redirect(url_for("login"))

        pessoa = Pessoa.query.get(usuario.pessoa_id)  # ou usuario.pessoa se relação existir
        if not pessoa:
            flash("Pessoa vinculada ao usuário não encontrada.")
            return redirect(url_for("login"))

        #  Busca telefones existentes
        fones = Fone.query.filter_by(pessoa_id=pessoa.id_pessoa).order_by(Fone.id_fone).all()
        # busca por endereços existentes
        enderecos = Endereco.query.filter_by(id_endereco=pessoa.id_pessoa).order_by(Endereco.id_endereco).all()

        if request.method == "POST":
            # --- Campos básicos ---
            pessoa.nome = request.form.get("nome")
            pessoa.sobrenome = request.form.get("sobrenome")

            # --- Email ---
            novo_email = request.form.get("email")
            if novo_email and novo_email != usuario.email:
                if User.query.filter_by(email=novo_email).first():
                    flash("Este e-mail já está em uso.")
                    return redirect(url_for("usuario"))
                usuario.email = novo_email

            # --- CPF ---
            cpf_raw = request.form.get("cpf")
            if cpf_raw:
                pessoa.cpf = re.sub(r"\D", "", cpf_raw)

            # --- Data de nascimento ---
            data_nasc_raw = request.form.get("data_nasc")
            if data_nasc_raw:
                try:
                    pessoa.data_nasc = datetime.strptime(data_nasc_raw, "%Y-%m-%d").date()
                except ValueError:
                    flash("Data inválida. Use o formato YYYY-MM-DD.")
                    return redirect(url_for("usuario"))

            # --- Telefones múltiplos ---
            fones_form = [f.strip() for f in request.form.getlist("fones") if f.strip()]           

            # Atualiza os existentes ou remove se não estiver no formulário
            for i, fone_obj in enumerate(fones):
                if i < len(fones_form):
                    fone_obj.fone = fones_form[i]
                else:
                    db.session.delete(fone_obj)

            # Adiciona novos telefones se houver mais no formulário
            if len(fones_form) > len(fones):
                for j in range(len(fones), len(fones_form)):
                    novo = Fone(fone=fones_form[j], pessoa_id=pessoa.id_pessoa)
                    db.session.add(novo)
 
            # Busca no Banco endereços existentes
            ruas_form = [r.strip() for r in request.form.getlist("rua_av") if r.strip()]
            
            for j, end_obj in enumerate(enderecos):
                if j < len(ruas_form):
                    end_obj.rua_av = ruas_form[j]
                else:
                    db.session.delete(end_obj)

            if len(ruas_form) > len(enderecos):
                for i in range(len(enderecos), len(ruas_form)):
                    inclui_endereco = Endereco(rua_av=ruas_form[i], id_pessoa = pessoa.id_pessoa, tipo="RESIDENCIAL")
                    db.session.add(inclui_endereco) 

            # --- Commit final ---
            db.session.commit()
            flash("Dados atualizados com sucesso!")

             # Recarrega lista de telefones
            fones = Fone.query.filter_by(pessoa_id=pessoa.id_pessoa).order_by(Fone.id_fone).all()
            enderecos = Endereco.query.filter_by(id_endereco=pessoa.id_pessoa).order_by(Endereco.id_endereco).all()
            

        return render_template("usuario.html", user=usuario, fones=fones, enderecos=enderecos)


    return app
