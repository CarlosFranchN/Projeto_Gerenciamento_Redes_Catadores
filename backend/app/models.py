import datetime
from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, String, DateTime, Date,
    Float, UniqueConstraint, func, Enum, Numeric, Text, 
    CheckConstraint
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .database import Base 
import enum



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


class Municipio(Base):
    __tablename__ = "municipios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), index=True, nullable=False)
    uf = Column(String(2), default="CE", nullable=False)
    regiao = Column(String(50), nullable=True)
    ativo = Column(Boolean, default=True, nullable=False)  # ✅ Soft delete
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # ✅ Timestamp

    associacoes = relationship("Associacao", back_populates="municipio")


class Grupo(Base):
    __tablename__ = "grupos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), index=True, nullable=False)
    descricao = Column(String(255), nullable=True)
    ativo = Column(Boolean, default=True, nullable=False)  # ✅ Soft delete
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # ✅ Timestamp

    associacoes = relationship("Associacao", back_populates="grupo")


class Associacao(Base):
    __tablename__ = "associacoes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), unique=True, index=True, nullable=False)
    cnpj = Column(String(20), unique=True, index=True, nullable=True)  # ✅ Nullable para casos sem CNPJ
    lider = Column(String(100), nullable=True)
    telefone = Column(String(20), nullable=True)
    endereco = Column(String(255), nullable=True)
    bairro = Column(String(100), nullable=True)  # ✅ Separado para filtros
    cidade = Column(String(100), nullable=True)  # ✅ Separado para filtros
    uf = Column(String(2), nullable=True)  # ✅ Separado para filtros
    status = Column(String(20), default="ativo")  # ✅ 'ativo', 'inativo', 'pendente'
    ativo = Column(Boolean, default=True, nullable=False)  # ✅ Soft delete
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    municipio_id = Column(Integer, ForeignKey("municipios.id", ondelete="SET NULL"), nullable=True)
    grupo_id = Column(Integer, ForeignKey("grupos.id", ondelete="SET NULL"), nullable=True)

    municipio = relationship("Municipio", back_populates="associacoes")
    grupo = relationship("Grupo", back_populates="associacoes")
    afiliados = relationship("Afiliado", back_populates="associacao", cascade="all, delete-orphan")
    producoes = relationship("ProducaoImpacto", back_populates="associacao", cascade="all, delete-orphan")


class Afiliado(Base):
    __tablename__ = "afiliados"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    cpf = Column(String(14), unique=True, index=True, nullable=True)  # ✅ Nullable + tamanho fixo
    cpf_hash = Column(String(64), index=True, nullable=True)  # ✅ Para buscas sem expor CPF
    funcao = Column(String(50), nullable=True)
    data_filiacao = Column(Date, nullable=True)
    ativo = Column(Boolean, default=True, nullable=False)  # ✅ Soft delete
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    associacao_id = Column(Integer, ForeignKey("associacoes.id", ondelete="CASCADE"), nullable=False)
    associacao = relationship("Associacao", back_populates="afiliados")


class ProducaoImpacto(Base):
    __tablename__ = "producao_impacto"

    id = Column(Integer, primary_key=True, index=True)
    mes = Column(Integer, nullable=False)  # ✅ 1-12
    ano = Column(Integer, nullable=False)  # ✅ Ex: 2024
    categoria = Column(String(50), nullable=False)  # ⚠️ Ideal: FK para tabela categorias
    peso_kg = Column(Numeric(10, 2), nullable=False)
    valor_gerado = Column(Numeric(10, 2), nullable=True)
    tipo_registro = Column(String(20), default="PRODUCAO")  # ✅ 'PRODUCAO', 'VENDA', 'DOACAO'
    observado = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    associacao_id = Column(Integer, ForeignKey("associacoes.id", ondelete="CASCADE"), nullable=False)
    associacao = relationship("Associacao", back_populates="producoes")

    # ✅ Trava para evitar duplicidade (associação + mês + ano + categoria)
    __table_args__ = (
        UniqueConstraint('associacao_id', 'mes', 'ano', 'categoria', name='trava_producao_unica'),
        CheckConstraint('mes >= 1 AND mes <= 12', name='chk_mes_valido'),
        CheckConstraint('peso_kg >= 0', name='chk_peso_positivo'),
    )