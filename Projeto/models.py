from . import db

# O autoload_with=db.engine faz o SQLAlchemy consultar 
# o schema real no MySQL e importar todas as colunas 
# com os tipos corretos.

class Cardapio(db.Model):
    __tablename__ = 'Cardapio'
    __table_args__ = {'autoload_with': db.engine}  # importa colunas do banco

class Ficha_Tecnica(db.Model):
    __tablename__ = 'Ficha_Tecnica'
    __table_args__ = {'autoload_with': db.engine}

class Ingredientes(db.Model):
    __tablename__ = 'Ingredientes'
    __table_args__ = {'autoload_with': db.engine}

class Insumos(db.Model):
    __tablename__ = 'Insumos'
    __table_args__ = {'autoload_with': db.engine}
