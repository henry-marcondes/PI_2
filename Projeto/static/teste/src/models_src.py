from ext import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Date, TIMESTAMP, func

class Pessoa(db.Model):
    __tablename__ = "Pessoa"

    id_pessoa: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(45), nullable=False)
    sobrenome: Mapped[str] = mapped_column(String(150), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique=True)
    data_nasc: Mapped[Date] = mapped_column(Date)
    data_cadastro: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="pessoa", uselist=False)
    fones = relationship("Fone", back_populates="pessoa", cascade="all, delete-orphan")


class User(db.Model):
    __tablename__ = "User"

    idUser: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(16))
    email: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))  # guardaremos hash
    pessoa_id: Mapped[int] = mapped_column(ForeignKey("Pessoa.id_pessoa"))

    pessoa = relationship("Pessoa", back_populates="user")

class Fone(db.Model):
    __tablename__ = "Fone"
    id_fone: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fone: Mapped[str] = mapped_column(String(45), nullable=True)
    id_fornecedor: Mapped[int] = mapped_column(Integer, nullable=True)
    pessoa_id: Mapped[int] = mapped_column(ForeignKey("Pessoa.id_pessoa"))

    pessoa = relationship("Pessoa", back_populates="fones")


