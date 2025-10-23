from pydantic import BaseModel
from datetime import datetime
from typing import List,Optional
from .schema_material import Material


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
    comprador: str
    concluida : bool = True

class VendaCreate(VendaBase):
    itens: List[ItemVendaCreate] # Para criar uma venda, passamos uma lista de itens

class Venda(VendaBase):
    id: int
    codigo: Optional[str] = None
    data_venda: datetime
    # comprador: Comprador
    itens: List[ItemVenda] = [] # A resposta da venda incluirá a lista de itens vendidos

    class Config:
        orm_mode = True
        
class VendasPaginadasResponse(BaseModel):
    total_count: int
    items:  List[Venda]
    
    class Config:
        from_attributes = True