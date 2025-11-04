from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .schema_material import Material
from .schema_comprador import Comprador # 👈 IMPORTAÇÃO NOVA

# --- Schemas para ItemVenda (depende de Material) ---
class ItemVendaBase(BaseModel):
    quantidade_vendida: float
    valor_unitario: float
    id_material: int

class ItemVendaCreate(ItemVendaBase):
    pass

class ItemVenda(ItemVendaBase):
    id: int
    material: Material # Mostra o objeto Material aninhado

    class Config:
        from_attributes = True

# --- Schemas para Venda (depende de Comprador e ItemVenda) ---
class VendaBase(BaseModel):
    id_comprador: int # 👈 MUDANÇA AQUI (de nome_comprador para id_comprador)
    concluida: bool = True

class VendaCreate(VendaBase):
    itens: List[ItemVendaCreate] # A lista de itens para criar

class Venda(VendaBase):
    id: int
    codigo: Optional[str] = None
    data_venda: datetime

    itens: List[ItemVenda] = []
    comprador: Comprador # 👈 MUDANÇA AQUI (mostra o objeto Comprador)

    class Config:
        from_attributes = True

# Schema de resposta paginada
class VendasPaginadasResponse(BaseModel):
    total_count: int
    items: List[Venda]

    class Config:
        from_attributes = True