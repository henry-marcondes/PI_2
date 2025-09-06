from . import db

# O autoload_with=db.engine faz o SQLAlchemy consultar 
# o schema real no MySQL e importar todas as colunas 
# com os tipos corretos.

class Cardapio(db.Model):
    __tablename__ = 'Cardapio'
    __table_args__ = {'autoload_with': db.engine}  # importa colunas do banco

class Compras(db.Model):
    __tablename__ = 'Compras'
    __table_args__ = {'autoload_with': db.engine}

class Endereco(db.Model):
    __tablename__ = 'Endereco'
    __table_args__ = {'autoload_with': db.engine}

class Ficha_Tecnica(db.Model):
    __tablename__ = 'Ficha_Tecnica'
    __table_args__ = {'autoload_with': db.engine}

class Fone(db.Model):
    __tablename__ = 'Fone'
    __table_args__ = {'autoload_with': db.engine}

class Ingredientes(db.Model):
    __tablename__ = 'Ingredientes'
    __table_args__ = {'autoload_with': db.engine}

class Insumos(db.Model):
    __tablename__ = 'Insumos'
    __table_args__ = {'autoload_with': db.engine}

class Movimentacoes(db.Model):
    __tablename__ = 'Movimentacoes'
    __table_args__ = {'autoload_with': db.engine}

class Pessoa(db.Model):
    __tablename__ = 'Pessoa'
    __table_args__ = {'autoload_with': db.engine}

class Fornecedor(db.Model):
    __tablename__ = 'Fornecedor'
    __table_args__ = {'autoload_with': db.engine}
    


