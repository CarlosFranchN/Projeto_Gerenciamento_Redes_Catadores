from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .schema_material import Material
from .schema_parceiro import Parceiro

class CompraBase(BaseModel):
    quantidade: float
    valor_pago_unitario: float
    id_parceiro: int
    id_material: int

class CompraCreate(CompraBase):
    pass

class Compra(CompraBase):
    id: int
    codigo_compra: Optional[str] = None
    valor_pago_total: float
    data_compra: datetime
    status: str
    material: Material
    parceiro: Parceiro

    class Config:
        from_attributes = True

class ComprasPaginadasResponse(BaseModel):
    total_count: int
    items: List[Compra]

    class Config:
        from_attributes = True