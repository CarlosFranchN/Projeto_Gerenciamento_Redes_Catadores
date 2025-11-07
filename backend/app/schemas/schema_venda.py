# app/schemas/schema_venda.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .schema_material import Material
from .schema_comprador import Comprador 
class ItemVendaBase(BaseModel):
    quantidade_vendida: float
    valor_unitario: float
    id_material: int

class ItemVendaCreate(ItemVendaBase):
    pass

class ItemVenda(ItemVendaBase):
    id: int
    material: Material
    class Config:
        from_attributes = True


class VendaBase(BaseModel):
    id_comprador: int 
    concluida: bool = True

class VendaCreate(VendaBase):
    itens: List[ItemVendaCreate]

class Venda(VendaBase):
    id: int
    codigo: Optional[str] = None
    data_venda: datetime
    itens: List[ItemVenda] = []
    comprador: Comprador 
    class Config:
        from_attributes = True

class VendasPaginadasResponse(BaseModel):
    total_count: int
    items: List[Venda]
    class Config:
        from_attributes = True