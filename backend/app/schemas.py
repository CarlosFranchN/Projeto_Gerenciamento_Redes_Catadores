from pydantic import BaseModel
from datetime import datetime
from typing import List,Optional


class MaterialBase(BaseModel):
    nome:str
    categoria: Optional[str] = None
    unidade_medida: str = 'Kg'
    
class MaterialCreate(MaterialBase):
    pass

class Material(MaterialBase):
    id : int
    codigo_material : Optional[str]
    
    class Config:
        orm_mode = True
# --- Schemas para Comprador ---
class CompradorBase(BaseModel):
    nome: str
    contato: Optional[str] = None

class CompradorCreate(CompradorBase):
    pass

class Comprador(CompradorBase):
    id: int

    class Config:
        orm_mode = True

# --- Schemas para Associação ---
class AssociacaoBase(BaseModel):
    nome: str
    lider: Optional[str] = None
    telefone: Optional[str] = None
    cnpj: Optional[str] = None
    status: bool = True

class AssociacaoCreate(AssociacaoBase):
    pass

class Associacao(AssociacaoBase):
    id: int
    data_cadastro: datetime

    class Config:
        orm_mode = True

# --- Schemas para Entrada de Material (com relacionamentos) ---
class EntradaMaterialBase(BaseModel):
    quantidade: float
    id_material: int
    id_associacao: int
    material: Material
    associacao:Associacao
    class Config:
        orm_mode = True

class EntradaMaterialCreate(EntradaMaterialBase):
    pass

class EntradaMaterial(EntradaMaterialBase):
    id: int
    data_entrada: datetime
    # Aqui mostramos os dados completos das entidades relacionadas
    material: Material
    associacao: Associacao

    class Config:
        orm_mode = True

# --- Schemas para Venda (com relacionamentos aninhados) ---
class ItemVendaBase(BaseModel):
    quantidade_vendida: float
    valor_unitario: float
    id_material: int

class ItemVendaCreate(ItemVendaBase):
    pass

class ItemVenda(ItemVendaBase):
    id: int
    material: Material # Mostra os dados completos do material

    class Config:
        orm_mode = True

class VendaBase(BaseModel):
    id_comprador: int

class VendaCreate(VendaBase):
    itens: List[ItemVendaCreate] # Para criar uma venda, passamos uma lista de itens

class Venda(VendaBase):
    id: int
    data_venda: datetime
    comprador: Comprador
    itens: List[ItemVenda] = [] # A resposta da venda incluirá a lista de itens vendidos

    class Config:
        orm_mode = True