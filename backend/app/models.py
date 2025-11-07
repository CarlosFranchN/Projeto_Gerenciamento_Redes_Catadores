from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, func
from sqlalchemy.orm import relationship
from .database import Base 

class Material(Base):
    __tablename__ = "materiais"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True, nullable=True) 
    nome = Column(String, unique=True, index=True, nullable=False)
    categoria = Column(String, index=True, nullable=True) 
    unidade_medida = Column(String, default='Kg')
    ativo = Column(Boolean, server_default='true', nullable=False)
    
    # Relacionamento reverso para todas as transações
    itens_venda = relationship("ItemVenda", back_populates="material")
    recebimentos_doacao = relationship("RecebimentoDoacao", back_populates="material") # Renomeado
    compras = relationship("Compra", back_populates="material") # Novo

class TipoParceiro(Base): # Renomeado de TipoDoador
    """
    TABELA DIMENSÃO: Armazena os tipos de parceiros.
    Ex: 'ASSOCIACAO', 'FORNECEDOR_COMERCIAL', 'ORGAO_PUBLICO'
    """
    __tablename__ = "tipo_parceiro" # Renomeado
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)

    parceiros = relationship("Parceiro", back_populates="tipo_info") # Renomeado

class Parceiro(Base): # Renomeado de Doador
    """
    TABELA DIMENSÃO (SUPERTIPO): Armazena TODOS os parceiros (Doadores E Fornecedores).
    Ex: 'ASSORECICLA', 'Prefeitura', 'FerroVelho Central'
    """
    __tablename__ = "parceiros" # Renomeado
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False, unique=True)
    
    id_tipo_parceiro = Column(Integer, ForeignKey("tipo_parceiro.id"), nullable=False) # Renomeado
    tipo_info = relationship("TipoParceiro", back_populates="parceiros") # Renomeado
    
    # Relacionamento reverso para Entradas
    recebimentos_doacao = relationship("RecebimentoDoacao", back_populates="parceiro") # Renomeado
    compras = relationship("Compra", back_populates="parceiro") # Novo
    
    # Relacionamento reverso para os detalhes da Associação (se for uma)
    associacao_detalhes = relationship("Associacao", back_populates="parceiro_info", uselist=False, cascade="all, delete-orphan") # Renomeado

class Associacao(Base):
    """
    TABELA DE DETALHES (SUBTIPO): Detalhes específicos de um Parceiro do tipo 'ASSOCIACAO'.
    """
    __tablename__ = "associacoes"
    
    id = Column(Integer, primary_key=True, index=True) 
    
    parceiro_id = Column(Integer, ForeignKey("parceiros.id"), nullable=False, unique=True) # Renomeado
    parceiro_info = relationship("Parceiro", back_populates="associacao_detalhes") # Renomeado
    
    # Detalhes específicos
    lider = Column(String, nullable=True)
    telefone = Column(String,nullable=True)
    data_cadastro = Column(DateTime(timezone=True), server_default=func.now())
    cnpj = Column(String,index=True,nullable=True)
    ativo = Column(Boolean, server_default='true' , nullable=False)

class Comprador(Base):
    """
    TABELA DIMENSÃO: Armazena os clientes que COMPRAM da rede.
    """
    __tablename__ = "compradores"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True, nullable=False)
    cnpj = Column(String, index=True, nullable=True, unique=True)
    telefone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    ativo = Column(Boolean, server_default='true', nullable=False)
    
    vendas = relationship("Venda", back_populates="comprador")


# --- TABELAS TRANSACIONAIS (FATOS) ---

class RecebimentoDoacao(Base): # Renomeado de EntradaMaterial
    """
    TABELA FATO: Registra o evento de uma entrada SEM CUSTO (Doação).
    """
    __tablename__ = "recebimentos_doacao" # Renomeado
    
    id = Column(Integer, primary_key=True, index=True)
    codigo_lote = Column(String, unique=True, index=True, nullable=True) 
    quantidade = Column(Float, nullable=False)
    data_entrada = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="Confirmada", server_default="Confirmada", nullable=False) 
    
    # Links para as dimensões
    id_parceiro = Column(Integer, ForeignKey("parceiros.id"), nullable=False) # Renomeado
    id_material = Column(Integer, ForeignKey("materiais.id"), nullable=False)

    # Relacionamentos
    parceiro = relationship("Parceiro", back_populates="recebimentos_doacao") # Renomeado
    material = relationship("Material", back_populates="recebimentos_doacao") # Renomeado

class Compra(Base):
    """
    TABELA FATO (NOVA): Registra o evento de uma entrada COM CUSTO (Compra).
    """
    __tablename__ = "compras"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo_compra = Column(String, unique=True, index=True, nullable=True) # Ex: C-20251106-001
    quantidade = Column(Float, nullable=False)
    valor_pago_unitario = Column(Float, nullable=False)
    valor_pago_total = Column(Float, nullable=False) # Calculado (qtd * valor_unitario)
    data_compra = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="Concluída", server_default="Concluída", nullable=False) # Ex: Concluída, Cancelada
    
    # Links para as dimensões
    id_parceiro = Column(Integer, ForeignKey("parceiros.id"), nullable=False) # Quem vendeu para nós
    id_material = Column(Integer, ForeignKey("materiais.id"), nullable=False)
    
    # Relacionamentos
    parceiro = relationship("Parceiro", back_populates="compras")
    material = relationship("Material", back_populates="compras")

class Venda(Base):
    """
    TABELA FATO: Registra o cabeçalho de uma SAÍDA (Venda).
    """
    __tablename__ = "vendas"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True, nullable=True)
    data_venda = Column(DateTime(timezone=True) , server_default=func.now())
    concluida = Column(Boolean, server_default='true' ,nullable=False)
    
    id_comprador = Column(Integer, ForeignKey("compradores.id"), nullable=False)
    comprador = relationship("Comprador", back_populates="vendas")
    
    itens = relationship("ItemVenda", back_populates="venda", cascade="all, delete-orphan")

class ItemVenda(Base):
    """
    TABELA FATO (Nível do Item): Detalhes de cada item em uma SAÍDA (Venda).
    """
    __tablename__ = "itens_venda"
    
    id = Column(Integer, primary_key=True, index=True)
    quantidade_vendida = Column(Float, nullable=False)
    valor_unitario = Column(Float, nullable=False)
    
    id_venda = Column(Integer, ForeignKey("vendas.id"), nullable=False)
    id_material = Column(Integer, ForeignKey("materiais.id"), nullable=False)
    
    venda = relationship("Venda", back_populates="itens")
    material = relationship("Material", back_populates="itens_venda")