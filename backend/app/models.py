import datetime
from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, String, DateTime, 
    Float, UniqueConstraint, func, Enum, Numeric, Text, 
    CheckConstraint
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .database import Base 
import enum


# =============== NOVAS TABELAS (Fase 1) ===============

class ProducaoMensal(Base):
    __tablename__ = "producao_mensal"
    
    id = Column(Integer, primary_key=True, index=True)
    associacao_id = Column(Integer, ForeignKey("associacoes.id"), nullable=True, index=True)
    mes = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False, index=True)
    kg = Column(Numeric(10, 2), nullable=False)
    valor_venda = Column(Numeric(10, 2), nullable=True)
    observado = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relacionamento
    associacao = relationship("Associacao", back_populates="producoes")
    
    __table_args__ = (
        UniqueConstraint('associacao_id', 'mes', 'ano', name='uq_producao_mes_ano'),
        CheckConstraint('mes >= 1 AND mes <= 12', name='check_mes_valido'),
    )
    
    def __repr__(self):
        return f"<ProducaoMensal(mes={self.mes}, ano={self.ano}, kg={self.kg})>"


class EnderecosCache(Base):
    __tablename__ = "enderecos_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    cnpj = Column(String(18), unique=True, nullable=False, index=True)
    logradouro = Column(Text, nullable=True)
    numero = Column(String(20), nullable=True)
    complemento = Column(String(50), nullable=True)
    bairro = Column(String(100), nullable=True)
    cidade = Column(String(100), nullable=True)
    uf = Column(String(2), nullable=True)
    consulted_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<EnderecosCache(cnpj={self.cnpj}, cidade={self.cidade})>"


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    token = Column(String(255), unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relacionamento
    usuario = relationship("Usuario", back_populates="refresh_tokens")
    
    def __repr__(self):
        return f"<RefreshToken(usuario_id={self.usuario_id}, revoked={self.revoked})>"


class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True, index=True)
    acao = Column(String(50), nullable=False, index=True)
    tabela_afetada = Column(String(50), nullable=True)
    registro_id = Column(Integer, nullable=True)
    dados_antigos = Column(JSONB, nullable=True)
    dados_novos = Column(JSONB, nullable=True)
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    
    # Relacionamento
    usuario = relationship("Usuario", back_populates="audit_logs")
    
    def __repr__(self):
        return f"<AuditLog(acao={self.acao}, tabela={self.tabela_afetada})>"


# =============== TABELAS EXISTENTES (Corrigidas) ===============

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False) 
    nome = Column(String(255), nullable=True)
    role = Column(String(20), default="admin")  # admin, operador, visualizador
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relacionamentos (NOVOS - para as tabelas novas)
    refresh_tokens = relationship("RefreshToken", back_populates="usuario", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="usuario", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Usuario(username='{self.username}')>"


class CategoriaResiduo(Base):
    __tablename__ = "categoria_residuo"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False, index=True)
    
    materiais = relationship("Material", back_populates="categoria_info")
    
    def __repr__(self):
        return f"<CategoriaResiduo(nome='{self.nome}')>"


class Material(Base):
    __tablename__ = "materiais"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True, nullable=True) 
    nome = Column(String, unique=True, index=True, nullable=False)
    id_categoria = Column(Integer, ForeignKey("categoria_residuo.id"), nullable=True)
    unidade_medida = Column(String, default='Kg')
    ativo = Column(Boolean, server_default='true', nullable=False)
    
    categoria_info = relationship("CategoriaResiduo", back_populates="materiais")
    itens_venda = relationship("ItemVenda", back_populates="material")
    recebimentos_doacao = relationship("RecebimentoDoacao", back_populates="material")
    compras = relationship("Compra", back_populates="material")
    
    def __repr__(self):
        return f"<Material(nome='{self.nome}')>"


class TipoParceiro(Base):
    __tablename__ = "tipo_parceiro"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)
    
    parceiros = relationship("Parceiro", back_populates="tipo_info")
    
    def __repr__(self):
        return f"<TipoParceiro(nome='{self.nome}')>"


class Parceiro(Base):
    __tablename__ = "parceiros"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False, unique=True)
    
    id_tipo_parceiro = Column(Integer, ForeignKey("tipo_parceiro.id"), nullable=False)
    tipo_info = relationship("TipoParceiro", back_populates="parceiros")
    
    recebimentos_doacao = relationship("RecebimentoDoacao", back_populates="parceiro")
    compras = relationship("Compra", back_populates="parceiro")
    associacao_detalhes = relationship("Associacao", back_populates="parceiro_info", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Parceiro(nome='{self.nome}')>"


class Associacao(Base):
    __tablename__ = "associacoes"
    
    id = Column(Integer, primary_key=True, index=True) 
    
    parceiro_id = Column(Integer, ForeignKey("parceiros.id"), nullable=False, unique=True)
    parceiro_info = relationship("Parceiro", back_populates="associacao_detalhes")
    
    # Detalhes específicos
    lider = Column(String, nullable=True)
    telefone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    cnpj = Column(String, index=True, nullable=True)
    
    # Endereço (CAMPOS NOVOS - antes estava só no Parceiro)
    logradouro = Column(Text, nullable=True)
    numero = Column(String(20), nullable=True)
    complemento = Column(String(50), nullable=True)
    bairro = Column(String(100), nullable=True)
    cidade = Column(String(100), nullable=True)
    uf = Column(String(2), nullable=True)
    
    # Status e datas
    status = Column(String(20), default="ativo")  # ativo, inativo, pendente
    data_cadastro = Column(DateTime(timezone=True), server_default=func.now())
    ativo = Column(Boolean, server_default='true', nullable=False)
    
    # Relacionamento NOVO com ProducaoMensal
    producoes = relationship("ProducaoMensal", back_populates="associacao", cascade="all, delete-orphan")
    grupos = relationship("Grupo", back_populates="associacao", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Associacao(nome='{self.parceiro_info.nome if self.parceiro_info else 'N/A'}')>"


class Comprador(Base):
    __tablename__ = "compradores"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True, nullable=False)
    cnpj = Column(String, index=True, nullable=True, unique=True)
    telefone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    ativo = Column(Boolean, server_default='true', nullable=False)
    
    vendas = relationship("Venda", back_populates="comprador")
    
    def __repr__(self):
        return f"<Comprador(nome='{self.nome}')>"


# =============== TABELAS TRANSACIONAIS ===============

class RecebimentoDoacao(Base):
    __tablename__ = "recebimentos_doacao"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo_lote = Column(String, unique=True, index=True, nullable=True) 
    quantidade = Column(Float, nullable=False)
    data_entrada = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="Confirmada", server_default="Confirmada", nullable=False) 
    
    id_parceiro = Column(Integer, ForeignKey("parceiros.id"), nullable=False)
    id_material = Column(Integer, ForeignKey("materiais.id"), nullable=False)
    
    parceiro = relationship("Parceiro", back_populates="recebimentos_doacao")
    material = relationship("Material", back_populates="recebimentos_doacao")
    
    def __repr__(self):
        return f"<RecebimentoDoacao(codigo_lote='{self.codigo_lote}')>"


class Compra(Base):
    __tablename__ = "compras"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo_compra = Column(String, unique=True, index=True, nullable=True)
    quantidade = Column(Float, nullable=False)
    valor_pago_unitario = Column(Float, nullable=False)
    valor_pago_total = Column(Float, nullable=False)
    data_compra = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="Concluída", server_default="Concluída", nullable=False)
    
    id_parceiro = Column(Integer, ForeignKey("parceiros.id"), nullable=False)
    id_material = Column(Integer, ForeignKey("materiais.id"), nullable=False)
    
    parceiro = relationship("Parceiro", back_populates="compras")
    material = relationship("Material", back_populates="compras")
    transacao_financeira = relationship("TransacaoFinanceira", back_populates="compra", uselist=False)
    
    def __repr__(self):
        return f"<Compra(codigo='{self.codigo_compra}')>"


class Venda(Base):
    __tablename__ = "vendas"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True, nullable=True)
    data_venda = Column(DateTime(timezone=True), server_default=func.now())
    concluida = Column(Boolean, server_default='true', nullable=False)
    
    id_comprador = Column(Integer, ForeignKey("compradores.id"), nullable=False)
    comprador = relationship("Comprador", back_populates="vendas")
    
    itens = relationship("ItemVenda", back_populates="venda", cascade="all, delete-orphan")
    transacao_financeira = relationship("TransacaoFinanceira", back_populates="venda", uselist=False)
    
    def __repr__(self):
        return f"<Venda(codigo='{self.codigo}')>"


class ItemVenda(Base):
    __tablename__ = "itens_venda"
    
    id = Column(Integer, primary_key=True, index=True)
    quantidade_vendida = Column(Float, nullable=False)
    valor_unitario = Column(Float, nullable=False)
    
    id_venda = Column(Integer, ForeignKey("vendas.id"), nullable=False)
    id_material = Column(Integer, ForeignKey("materiais.id"), nullable=False)
    
    venda = relationship("Venda", back_populates="itens")
    material = relationship("Material", back_populates="itens_venda")
    
    def __repr__(self):
        return f"<ItemVenda(quantidade={self.quantidade_vendida})>"


class TipoTransacaoEnum(enum.Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"
    
    
class TransacaoFinanceira(Base):
    __tablename__ = "transacoes_financeiras"
    
    id = Column(Integer, primary_key=True, index=True)
    data = Column(DateTime(timezone=True), server_default=func.now())
    
    tipo = Column(Enum(TipoTransacaoEnum), nullable=False, index=True)
    valor = Column(Float, nullable=False)
    descricao = Column(String, nullable=True)
    
    id_compra_associada = Column(Integer, ForeignKey("compras.id"), nullable=True)
    id_venda_associada = Column(Integer, ForeignKey("vendas.id"), nullable=True)
    
    compra = relationship("Compra", back_populates="transacao_financeira")
    venda = relationship("Venda", back_populates="transacao_financeira")
    
    def __repr__(self):
        return f"<TransacaoFinanceira(tipo={self.tipo}, valor={self.valor})>"
    

# =============== GRUPOS E MUNICÍPIOS ===============

class Grupo(Base):
    __tablename__ = "grupos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False, index=True)
    integrantes = Column(Integer, default=0)
    associacao_id = Column(Integer, ForeignKey("associacoes.id"), nullable=True, index=True)
    cidade = Column(String(100), nullable=True)
    uf = Column(String(2), nullable=True)
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relacionamentos
    associacao = relationship("Associacao", back_populates="grupos")
    
    def __repr__(self):
        return f"<Grupo(nome='{self.nome}', integrantes={self.integrantes})>"


class Municipio(Base):
    __tablename__ = "municipios"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, unique=True, index=True)
    uf = Column(String(2), nullable=False)
    qtd_grupos = Column(Integer, default=0)
    qtd_associacoes = Column(Integer, default=0)
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f"<Municipio(nome='{self.nome}', uf='{self.uf}')>"