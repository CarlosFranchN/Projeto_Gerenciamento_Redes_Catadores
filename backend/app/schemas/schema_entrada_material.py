from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .schema_material import Material
from .schema_doador import Doador # 👈 MUDANÇA AQUI

class EntradaMaterialBase(BaseModel):
    quantidade: float
    id_material: int
    id_doador: int # 👈 MUDANÇA AQUI (de id_associacao para id_doador)

class EntradaMaterialCreate(EntradaMaterialBase):
    pass

class EntradaMaterial(EntradaMaterialBase):
    id: int
    data_entrada: datetime
    codigo_lote: Optional[str] = None
    status: str

    material: Material
    doador: Doador # 👈 MUDANÇA AQUI

    class Config:
        from_attributes = True

# Schema de resposta paginada
class EntradasPaginadasResponse(BaseModel):
    total_count: int
    items: List[EntradaMaterial]

    class Config:
        from_attributes = True