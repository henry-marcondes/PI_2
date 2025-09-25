from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
Base = declarative_base()

class Pessoa(Base):
    __tablename__ = "Pessoa"

    id_pessoa = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(45), nullable=False)
    sobrenome = Column(String(150), nullable=False)
    cpf = Column(String(20), unique=True, nullable=True)
    data_nasc = Column(Date, nullable=True)
    data_cadastro = Column(server_default=func.now(), nullable=True)
    id_usuario = Column(Integer, nullable=True)

    # Relacionamento opcional se você tiver a tabela Usuario
    #usuario = relationship("Usuario", back_populates="pessoas")

    def __repr__(self):
        return f"<Pessoa(id={self.id_pessoa}, nome={self.nome}, sobrenome={self.sobrenome})>"        
        #return f"<Pessoa(id={self.id_pessoa}, nome={self.nome} {self.sobrenome})>"
    
class User(Base):
    __tablename__ = "User"

    id_usuario = Column(Integer, primary_key=False, autoincrement=True)
    username = Column(String(16), nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    password = Column(String(32), nullable=True)
    pessoa_id = Column(Integer, nullable=True, ForeignKey("Pessoa.id_pessoa"))

    # Relacionamento com a tabela Pessoa
    pessoas = relationship("Pessoa", back_populates="usuario")

    def __repr__(self):
        return f"<User(id={self.id_usuario}, email={self.email})>"
    
class Fone(Base):
    __tablename__ = "Fone"

    id_fone = Column(Integer, primary_key=True, autoincrement=True)
    fone = Column(String(45), nullable=True)
    id_fornecedor = Column(Integer,nullable=True
    pessoa_id = Column(Integer, ForeignKey("Pessoa.id_pessoa"), nullable=True)

    def __repr__(self):
        return f"<Fone(id={self.id_fone}, fone={self.fone})>"
    
class Endereco(Base):
    __tablename__ = "Endereco"

    id_endereco = Column(Integer, primary_key=True, autoincrement=True)
    rua = Column(String(100), nullable=True)
    bairro = Column(String(100), nullable=True)
    cidade = Column(String(100), nullable=True)
    estado = Column(String(100), nullable=True)
    cep = Column(String(20), nullable=True)
    pessoa_id = Column(Integer, ForeignKey("Pessoa.id_pessoa"), nullable=True)

    def __repr__(self):
        return f"<Endereco(id={self.id_endereco}, rua={self.rua})>"
    
class Cardapio(Base):
    __tablename__ = "Cardapio"

    id_cardapio = Column(Integer, primary_key=True, autoincrement=True)
    Nome = Column(String(100), nullable=True)
    gramatura = Column(String(100), nullable=True)
    tempo_forno = Column(String(100), nullable=True)
    validade = Column(String(100), nullable=True)
    def __repr__(self):
        return f"<Cardapio(id={self.id_cardapio}, nome={self.nome})>"

   
