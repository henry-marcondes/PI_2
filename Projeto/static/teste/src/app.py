from flask import Flask, render_template, request, redirect, url_for, flash, session
from ext import db
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import re


app = Flask(__name__)
app.secret_key = "55631376"  # troque por algo seguro

# Configuração MySQL
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://henry:55631376@127.0.0.1/lili"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

from models_src import Pessoa, User, Fone   # importa os modelos depois do db estar pronto


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Você precisa estar logado para acessar esta página")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# Cadastro

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        sobrenome = request.form.get("sobrenome")
        cpf = request.form.get("cpf")
        username = request.form.get("username")
        email = request.form.get("email")
        senha = request.form.get("password")

        if not all([nome, sobrenome, username, email, senha]):
            flash("Preencha todos os campos")
            return redirect(url_for("cadastro"))

        # Criar Pessoa
        nova_pessoa = Pessoa(nome=nome, sobrenome=sobrenome, cpf=cpf)
        db.session.add(nova_pessoa)
        db.session.flush()

        # Criar User
        novo_user = User(
            username=username,
            email=email,
            password=generate_password_hash(senha),
            pessoa_id=nova_pessoa.id_pessoa,
        )
        db.session.add(novo_user)
        db.session.commit()

        flash("Cadastro realizado com sucesso!")
        return redirect(url_for("login"))

    return render_template("cadastro.html")

# Login

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        senha = request.form.get("password")

        usuario = User.query.filter_by(username=user).first()
        if usuario and User.query.filter_by(password = senha):
            session["user_id"] = usuario.idUser
            session["pessoa_id"] = usuario.pessoa_id
            flash("Login realizado com sucesso!")
            return redirect(url_for("perfil"))
        else:
            flash("Usuário ou senha inválidos")

    return render_template("login.html")


# Perfil
@app.route("/perfil", methods=["GET", "POST"])
@login_required
def perfil():
    usuario = User.query.get(session["user_id"])
    pessoa = usuario.pessoa

    if request.method == "POST":
    # Atualiza dados da pessoa
        pessoa.nome = request.form.get("nome")
        pessoa.sobrenome = request.form.get("sobrenome")
        usuario.email = request.form.get("email")

        # CPF limpo
        cpf_raw = request.form.get("cpf")
        if cpf_raw:
            pessoa.cpf = re.sub(r'\D', '', cpf_raw)

        # Data de nascimento
        data_nasc_raw = request.form.get("data_nasc")
        if data_nasc_raw:
            pessoa.data_nasc = data_nasc_raw

        # Telefones múltiplos
        fones_form = request.form.getlist("fones")  # retorna lista
        # Atualiza existentes
        for i, fone_obj in enumerate(pessoa.fones):
            if i < len(fones_form):
                fone_obj.fone = fones_form[i]
        # Adiciona novos telefones
        for i in range(len(pessoa.fones), len(fones_form)):
            novo_fone = Fone(fone=fones_form[i], pessoa_id=pessoa.id_pessoa)
            db.session.add(novo_fone)

        db.session.commit()
        flash("Dados atualizados com sucesso!")


    return render_template("perfil.html", user=usuario)


# Logout
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Você saiu da conta.")
    return redirect(url_for("login"))


# ---------------------------------
# Main
# ---------------------------------
if __name__ == "__main__":
    app.run(debug=True)
