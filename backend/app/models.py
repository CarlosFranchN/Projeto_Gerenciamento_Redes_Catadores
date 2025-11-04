from sqlalchemy import (Column,Integer,String,Float,DateTime,ForeignKey,Boolean)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


    
class Material(Base):
    __tablename__ = "materiais"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True, nullable=True) 
    nome = Column(String, unique=True, index=True, nullable=False)
    categoria = Column(String, index=True, nullable=True) 
    unidade_medida = Column(String, default='Kg')
    ativo = Column(Boolean, server_default='true', nullable=False)
    
    # Relacionamento: Um material pode estar em muitos itens de venda/entrada
    itens_venda = relationship("ItemVenda", back_populates="material")
    entradas = relationship("EntradaMaterial", back_populates="material")
    
    def __repr__(self):
        return f"<Material(nome='{self.nome}')>"
    
class TipoDoador(Base):
    __tablename__ = "tipo_doador"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String,unique=True, nullable=False)
    
    doadores = relationship("Doador", back_populates="tipo_info")
    
class Doador(Base):
    __tablename__ = "doadores"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False,unique=True)
    
    id_tipo_doador = Column(Integer, ForeignKey("tipo_doador.id"), nullable=False)
    tipo_info = relationship("TipoDoador", back_populates="doadores")
    
    entradas = relationship("EntradaMaterial" , back_populates="doador")
    associacao_detalhes = relationship("Associacao" , back_populates="doador_info" , uselist=False, cascade="all, delete-orphan")


class Associacao(Base):
    __tablename__ = "associacoes"
    
    id = Column(Integer, primary_key=True, index=True)
    
    doador_id = Column(Integer, ForeignKey("doadores.id"),nullable=False, unique=True)
    doador_info = relationship("Doador", back_populates="associacao_detalhes")

    lider = Column(String, nullable=True)
    telefone = Column(String, nullable=True)
    cnpj = Column(String, index=True, nullable=True)
    ativo = Column(Boolean, server_default='true', nullable=False)
    
    
class Comprador(Base):
    __tablename__ = "compradores"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True, nullable=False)
    cnpj = Column(String, index=True, nullable=True , unique=True)
    telefone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    ativo = Column(Boolean, server_default='true', nullable= False)
    
    vendas = relationship("Venda", back_populates="comprador")
    
    def __repr__(self):
        return f"<Comprador(nome='{self.nome}')>"
    
# --- Tabelas de Operações! (evento q acontecem).... tende a mudar ainda ---
class EntradaMaterial(Base):
    __tablename__ = "entradas_material"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo_lote = Column(String, unique=True, index=True, nullable=False)
    quantidade = Column(Float, nullable=False)
    
    data_entrada = Column(DateTime(timezone=True), server_default=func.now())
    
    status = Column(String, default="Confirmada", server_default="Confirmada", nullable=False)
    
    id_doador = Column(Integer, ForeignKey("doadores.id"), nullable=False)
    id_material = Column(Integer, ForeignKey("materiais.id") , nullable=False)
    
    
    
    doador = relationship("Doador" , back_populates="entradas")
    material = relationship("Material", back_populates="entradas")

    def __repr__(self):
        return f"<EntradaMaterial(material_id={self.id_material}, qtd={self.quantidade})>"
    
class Venda(Base):
    __tablename__ = "vendas"
    
    id = Column(Integer, primary_key=True,index=True)
    codigo = Column(String, unique=True, index=True, nullable=False)
    data_venda = Column(DateTime(timezone=True) , server_default=func.now())
    concluida = Column(Boolean, default='true' , server_default='true' ,nullable=False)
    
    id_comprador = Column(Integer, ForeignKey("compradores.id") , nullable=False)
    comprador = relationship("Comprador", back_populates="vendas")
    
    itens = relationship("ItemVenda" , back_populates="venda" , cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Venda(id={self.id}, comprador='{self.nome_comprador}')>"
    
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
            return f"<ItemVenda(material_id={self.id_material}, qtd={self.quantidade_vendida})>"
