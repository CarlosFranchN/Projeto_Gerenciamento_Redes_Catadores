# app/schemas/schema_recebimento.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .schema_material import Material
from .schema_parceiro import Parceiro # 👈 MUDANÇA AQUI

class RecebimentoDoacaoBase(BaseModel):
    quantidade: float
    id_material: int
    id_parceiro: int # 👈 MUDANÇA AQUI (de id_doador)

class RecebimentoDoacaoCreate(RecebimentoDoacaoBase):
    pass

class RecebimentoDoacao(RecebimentoDoacaoBase):
    id: int
    data_entrada: datetime
    codigo_lote: Optional[str] = None
    status: str
    material: Material
    parceiro: Parceiro # 👈 MUDANÇA AQUI

    class Config:
        from_attributes = True
        
class RecebimentosPaginadosResponse(BaseModel):
    total_count: int
    items: List[RecebimentoDoacao]

    class Config:
        from_attributes = True