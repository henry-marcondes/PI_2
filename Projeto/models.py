from . import db  # importa a instância de SQLAlchemy criada no __init__.py


class Cardapio(db.Model):
    __tablename__ = 'Cardapio'
    __table_args__ = {'comment': 'Destina-se aos Itens de Produção e Vendas'}

    id_cardapio = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(100), nullable=False, comment='Nome do Produto')
    gramatura = db.Column(db.Integer, nullable=False, comment='Categorias: 250g, 500g, 1000g')
    tempo_forno = db.Column(db.String(45), nullable=False)
    validade = db.Column(db.String(100), nullable=False)
    imagem = db.Column(db.String(100))

    Ficha_Tecnica = db.relationship('FichaTecnica', back_populates='Cardapio_')


class Endereco(db.Model):
    __tablename__ = 'Endereco'

    id_endereco = db.Column(db.Integer, primary_key=True)
    rua_av = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.Enum('RESINDENCIAL', 'COMERCIAL'), nullable=False)
    numero = db.Column(db.String(10))
    complemento = db.Column(db.String(20))
    id_fornecedor = db.Column(db.Integer)
    id_pessoa = db.Column(db.Integer)

    Fornecedor = db.relationship('Fornecedor', back_populates='endereco')


class Insumos(db.Model):
    __tablename__ = 'Insumos'
    __table_args__ = {'comment': 'Entrada dos insumos'}

    idInsumos = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(45), nullable=False)
    categoria = db.Column(db.String(15), nullable=False)
    menor_parte = db.Column(db.Float)
    valor_medio = db.Column(db.Float)

    Ingredientes = db.relationship('Ingredientes', back_populates='Insumos_')
    Movimentacoes = db.relationship('Movimentacoes', back_populates='Insumos_')
    Compras = db.relationship('Compras', back_populates='Insumos_')


class Pessoa(db.Model):
    __tablename__ = 'Pessoa'
    __table_args__ = (
        db.Index('cpf_UNIQUE', 'cpf', unique=True),
    )

    id_pessoa = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(45), nullable=False)
    sobrenome = db.Column(db.String(150), nullable=False)
    cpf = db.Column(db.String(11))
    data_nasc = db.Column(db.Date)
    data_cadastro = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP'))
    id_usuario = db.Column(db.Integer)
    

    # coleção de fones (um-para-muitos)
    fones = db.relationship('Fone', back_populates='pessoa', cascade="all, delete-orphan")
    User = db.relationship('User', back_populates='pessoa')


class Fone(db.Model):
    __tablename__ = 'Fone'
    __table_args__ = (
        db.ForeignKeyConstraint(['pessoa_id'], ['Pessoa.id_pessoa'], name='fk_fone_pessoa'),
        db.Index('fk_fone_pessoa_idx', 'pessoa_id')
    )

    id_fone = db.Column(db.Integer, primary_key=True)
    fone = db.Column(db.String(45), nullable=False)
    id_fornecedor = db.Column(db.Integer)
    pessoa_id = db.Column(db.Integer)

    pessoa = db.relationship('Pessoa', back_populates='fones')
    Fornecedor = db.relationship('Fornecedor', back_populates='fone')


class Ingredientes(db.Model):
    __tablename__ = 'Ingredientes'
    __table_args__ = (
        db.ForeignKeyConstraint(['Insumos_idInsumos'], ['Insumos.idInsumos'], ondelete='CASCADE', onupdate='CASCADE', name='fk_Ingredientes_Insumos1'),
        db.Index('fk_Ingredientes_Insumos1_idx', 'Insumos_idInsumos'),
        {'comment': 'Ingredientes conforme ficha técnica do cardápio'}
    )

    id_ingredientes = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(db.Float, nullable=False)
    unidade = db.Column(db.String(5), nullable=False)
    categoria = db.Column(db.String(12), nullable=False)
    Insumos_idInsumos = db.Column(db.Integer, nullable=False)

    Insumos_ = db.relationship('Insumos', back_populates='Ingredientes')
    Ficha_Tecnica = db.relationship('FichaTecnica', back_populates='Ingredientes_')


class Movimentacoes(db.Model):
    __tablename__ = 'Movimentacoes'
    __table_args__ = (
        db.ForeignKeyConstraint(['idInsumos'], ['Insumos.idInsumos'], ondelete='CASCADE', onupdate='CASCADE', name='fk_Movimentacoes_1'),
        db.Index('fk_Movimentacoes_1_idx', 'idInsumos'),
        {'comment': 'Controla entradas e saídas de insumos'}
    )

    idMov = db.Column(db.Integer, primary_key=True)
    idInsumos = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.Enum('ENTRADA', 'SAIDA'), nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    data_mov = db.Column(db.DateTime, nullable=False)

    Insumos_ = db.relationship('Insumos', back_populates='Movimentacoes')
    Compras = db.relationship('Compras', back_populates='Movimentacoes_')


class User(db.Model):
    __tablename__ = 'User'
    __table_args__ = (
        db.ForeignKeyConstraint(['pessoa_id'], ['Pessoa.id_pessoa'], ondelete='CASCADE', onupdate='CASCADE', name='fk_para_pessoa_2'),
        db.Index('fk_para_pessoa_1_idx', 'pessoa_id')
    )

    idUser = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16))
    email = db.Column(db.String(255))
    password = db.Column(db.String(32))
    pessoa_id = db.Column(db.Integer)

    pessoa = db.relationship('Pessoa', back_populates='User')


class Compras(db.Model):
    __tablename__ = 'Compras'
    __table_args__ = (
        db.ForeignKeyConstraint(['idInsumos'], ['Insumos.idInsumos'], ondelete='CASCADE', onupdate='CASCADE', name='fk_Compras_1'),
        db.ForeignKeyConstraint(['idMov'], ['Movimentacoes.idMov'], ondelete='SET NULL', onupdate='CASCADE', name='fk_Compras_2'),
        db.Index('fk_Compras_1_idx', 'idInsumos'),
        db.Index('fk_Compras_2_idx', 'idMov')
    )

    idCompras = db.Column(db.Integer, primary_key=True)
    idInsumos = db.Column(db.Integer, nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    unidade = db.Column(db.String(5), nullable=False)
    valor = db.Column(db.DECIMAL(10, 2), nullable=False)
    validade = db.Column(db.Date, nullable=False)
    fornecedor = db.Column(db.String(100), nullable=False)
    menor_parte = db.Column(db.Float, nullable=False)
    valor_medio = db.Column(db.DECIMAL(10, 5), nullable=False)
    idMov = db.Column(db.Integer)

    Insumos_ = db.relationship('Insumos', back_populates='Compras')
    Movimentacoes_ = db.relationship('Movimentacoes', back_populates='Compras')


class FichaTecnica(db.Model):
    __tablename__ = 'Ficha_Tecnica'
    __table_args__ = (
        db.ForeignKeyConstraint(['cardapio'], ['Cardapio.id_cardapio'], ondelete='CASCADE', onupdate='CASCADE', name='fk_cardapio_1'),
        db.ForeignKeyConstraint(['ingredientes'], ['Ingredientes.id_ingredientes'], name='fk_ingredientes_1'),
        db.Index('fk_cardapio_1_idx', 'cardapio'),
        db.Index('fk_ingredientes_1_idx', 'ingredientes'),
        {'comment': 'Detalhamento da ficha técnica do cardápio'}
    )

    id_Ficha_Tecnica = db.Column(db.Integer, primary_key=True)
    cardapio = db.Column(db.Integer, nullable=False)
    ingredientes = db.Column(db.Integer, nullable=False)
    tempo_preparo = db.Column(db.String(45))

    Cardapio_ = db.relationship('Cardapio', back_populates='Ficha_Tecnica')
    Ingredientes_ = db.relationship('Ingredientes', back_populates='Ficha_Tecnica')


class Fornecedor(db.Model):
    __tablename__ = 'Fornecedor'
    __table_args__ = (
        db.ForeignKeyConstraint(['endereco_id'], ['Endereco.id_endereco'], ondelete='CASCADE', onupdate='CASCADE', name='fk_Fornecedor_2'),
        db.ForeignKeyConstraint(['fone_id'], ['Fone.id_fone'], ondelete='CASCADE', onupdate='CASCADE', name='fk_Fornecedor_1'),
        db.Index('fk_Fornecedor_1_idx', 'fone_id'),
        db.Index('fk_Fornecedor_2_idx', 'endereco_id')
    )

    idFornecedor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco_id = db.Column(db.Integer, nullable=False)
    CNPJ = db.Column(db.String(25))
    fone_id = db.Column(db.Integer)

    endereco = db.relationship('Endereco', back_populates='Fornecedor')
    fone = db.relationship('Fone', back_populates='Fornecedor')
