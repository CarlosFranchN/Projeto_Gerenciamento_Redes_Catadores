from sqlalchemy import (Column,Integer,String,Float,DateTime,ForeignKey,Boolean)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Associacao(Base):
    __tablename__ = "associacoes"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    lider = Column(String, nullable=True)
    telefone = Column(String,nullable=True)
    status = Column(Boolean, server_default='true', nullable=False)
    data_cadastro = Column(DateTime(timezone=True), server_default=func.now())
    cnpj = Column(String,index=True,nullable=True)
    
    entradas = relationship("EntradaMaterial", back_populates="associacao")
    
    def __repr__(self):
        return f"<Associacao(nome='{self.nome}')>"
    
class Material(Base):
    __tablename__ = "materiais"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo_material  =Column(String, unique=True,index=True,nullable=True)
    nome = Column(String,unique=True, index=True,nullable=False)
    categoria = Column(String, index=True, nullable=True)
    unidade_medida = Column(String, default='Kg')
    
    def __repr__(self):
        return f"<Material(nome='{self.nome}')>"
    
class Comprador(Base):
    __tablename__ = "compradores"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True, nullable=False)
    contato = Column(String, nullable=True)
    
    def __repr__(self):
        return f"<Comprador(nome='{self.nome}')>"
    
# --- Tabelas de Operações! (evento q acontecem).... tende a mudar ainda ---
class EntradaMaterial(Base):
    __tablename__ = "entradas_material"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo_lote = Column(String, unique=True, index=True, nullable=False)
    quantidade = Column(Float, nullable=False)
    data_entrada = Column(DateTime(timezone=True), server_default=func.now())
    
    id_material = Column(Integer, ForeignKey("materiais.id") , nullable=False)
    id_associacao = Column(Integer, ForeignKey("associacoes.id"), nullable=False)
    
    
    
    associacao = relationship("Associacao" , back_populates="entradas")
    material = relationship("Material")

    def __repr__(self):
        return f"<EntradaMaterial(material_id={self.id_material}, qtd={self.quantidade})>"
    
class Venda(Base):
    __tablename__ = "vendas"
    
    id = Column(Integer, primary_key=True,index=True)
    codigo = Column(String, unique=True, index=True, nullable=False)
    data_venda = Column(DateTime(timezone=True) , server_default=func.now())
    
    id_comprador = Column(Integer, ForeignKey("compradores.id"), nullable=False)
    
    comprador = relationship("Comprador")
    itens = relationship("ItemVenda" , back_populates="venda")
    
    def __repr__(self):
        return f"<Venda(id={self.id}, data='{self.data_venda.strftime('%Y-%m-%d')}')>"
    
class ItemVenda(Base):
    __tablename__ = "itens_venda"
    
    id = Column(Integer, primary_key=True, index=True)
    quantidade_vendida = Column(Float, nullable=False)
    valor_unitario = Column(Float, nullable=False)
    
    id_venda = Column(Integer, ForeignKey("vendas.id"), nullable=False)
    id_material = Column(Integer, ForeignKey("materiais.id"), nullable=False)
    
    venda = relationship("Venda", back_populates="itens")
    material = relationship("Material")


    def __repr__(self):
            return f"<ItemVenda(material_id={self.id_material}, qtd={self.quantidade_vendida})>"
