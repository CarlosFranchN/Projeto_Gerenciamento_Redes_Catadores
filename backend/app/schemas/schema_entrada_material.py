from pydantic import BaseModel
from datetime import datetime
from typing import List,Optional
from .schema_material import Material
from .schema_associacao import Associacao


class EntradaMaterialBase(BaseModel):
    quantidade: float
    id_material: int
    id_associacao: int

    class Config:
        orm_mode = True

class EntradaMaterialCreate(EntradaMaterialBase):
    pass

class EntradaMaterial(EntradaMaterialBase):
    id: int
    data_entrada: datetime
    codigo_lote: Optional[str] = None
    # Aqui mostramos os dados completos das entidades relacionadas
    material: Material
    associacao: Associacao

    class Config:
        orm_mode = True
        
class  EntradaPaginasResponse(BaseModel):
    total_count : int
    items: List[EntradaMaterial]
    
    class Config:
        from_attributes = True