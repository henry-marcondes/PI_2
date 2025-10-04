from datetime import datetime
import os, re
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "static"),
        static_url_path="/static",
        instance_relative_config=True,
    )

    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///app.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    with app.app_context():
        from .models import Cardapio, Pessoa, User, Fone
        db.create_all()
        if Cardapio.query.count() == 0:
            demo = Cardapio(
                Nome="Lasanha de Frango",
                gramatura=500,
                tempo_forno="25 min",
                validade="90 dias",
                imagem="lasanha.jpg",
            )
            db.session.add(demo)
            db.session.commit()

    @app.route("/")
    def index():
        return redirect(url_for("login"))

    @app.route("/vitrine")
    def vitrine():
        from .models import Cardapio
        produtos = Cardapio.query.all()
        return render_template("vitrine.html", produtos=produtos)

    @app.route("/cadastro", methods=["GET", "POST"])
    def cadastro():
        from .models import Pessoa, User, Fone
        if request.method == "POST":
            nome = request.form.get("nome")
            sobrenome = request.form.get("sobrenome")
            email = request.form.get("email")
            whatsApp = request.form.get("whatsapp")
            username = request.form.get("user")
            senha = request.form.get("login")
            confirm = request.form.get("confirm-login")

            if not nome or not whatsApp:
                flash("Preencha Nome e WhatsApp", "error")
            elif senha != confirm:
                flash("Senhas diferentes", "error")
            else:
                existing_user = User.query.filter_by(username=username).first()
                if existing_user:
                    flash("Nome de usuário já existe", "error")
                else:
                    pessoa = Pessoa(nome=nome, sobrenome=sobrenome)
                    db.session.add(pessoa)
                    db.session.flush()
                    user = User(username=username, email=email, password=senha,
                                pessoa_id=pessoa.id_pessoa)
                    db.session.add(user)
                    db.session.flush()
                    pessoa.id_usuario = user.idUser
                    db.session.add(pessoa)
                    fone = Fone(fone=whatsApp, pessoa_id=pessoa.id_pessoa)
                    db.session.add(fone)
                    db.session.commit()
                    flash(f"Usuário {nome} cadastrado com sucesso!", "success")
                    return redirect(url_for("vitrine"))
        return render_template("cadastro.html")

    @app.route("/cardapio")
    def cardapio():
        from .models import Cardapio
        itens = Cardapio.query.all()
        return "<br>".join([f"{c.id_cardapio} - {c.Nome} - {c.gramatura}g" for c in itens])

    @app.route("/login", methods=["GET", "POST"])
    def login():
        from .models import User
        if request.method == "POST":
            username = request.form.get("user")
            senha = request.form.get("login")
            if not username or not senha:
                flash("Preencha Nome de Usuário e Senha", "error")
            else:
                usuario = User.query.filter_by(username=username).first()
                if usuario and (usuario.password == senha):
                    session["user_id"] = usuario.idUser
                    session["pessoa_id"] = usuario.pessoa_id
                    flash(f"Usuário {usuario.username} logado com sucesso!", "success")
                    return redirect(url_for("vitrine"))
                else:
                    flash("Usuário ou Senha inválidos", "error")
        return render_template("login.html")

    @app.route("/usuario", methods=["GET", "POST"])
    def usuario():
        from .models import User, Pessoa, Fone
        user_id = session.get("user_id")
        if not user_id:
            flash("Usuário não autenticado.")
            return redirect(url_for("login"))
        usuario = User.query.get(user_id)
        if not usuario:
            flash("Usuário não encontrado.")
            return redirect(url_for("login"))
        pessoa = Pessoa.query.get(usuario.pessoa_id)
        if not pessoa:
            flash("Pessoa vinculada ao usuário não encontrada.")
            return redirect(url_for("login"))
        fones = Fone.query.filter_by(pessoa_id=pessoa.id_pessoa).order_by(Fone.id_fone).all()
        if request.method == "POST":
            pessoa.nome = request.form.get("nome")
            pessoa.sobrenome = request.form.get("sobrenome")
            novo_email = request.form.get("email")
            if novo_email and novo_email != usuario.email:
                if User.query.filter_by(email=novo_email).first():
                    flash("Este e-mail já está em uso.")
                    return redirect(url_for("usuario"))
                usuario.email = novo_email
            cpf_raw = request.form.get("cpf")
            if cpf_raw:
                pessoa.cpf = re.sub(r"\D", "", cpf_raw)
            data_nasc_raw = request.form.get("data_nasc")
            if data_nasc_raw:
                try:
                    pessoa.data_nasc = datetime.strptime(data_nasc_raw, "%Y-%m-%d").date()
                except ValueError:
                    flash("Data inválida. Use o formato YYYY-MM-DD.")
                    return redirect(url_for("usuario"))
            fones_form = [f.strip() for f in request.form.getlist("fones") if f.strip()]
            for i, fobj in enumerate(fones):
                if i < len(fones_form):
                    fobj.fone = fones_form[i]
                else:
                    db.session.delete(fobj)
            if len(fones_form) > len(fones):
                for j in range(len(fones), len(fones_form)):
                    db.session.add(Fone(fone=fones_form[j], pessoa_id=pessoa.id_pessoa))
            db.session.commit()
            flash("Dados atualizados com sucesso!")
            fones = Fone.query.filter_by(pessoa_id=pessoa.id_pessoa).order_by(Fone.id_fone).all()
        return render_template("usuario.html", user=usuario, fones=fones)

    return app
