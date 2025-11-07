from pydantic import BaseModel
from typing import Optional, List
from .schema_tipo_parceiro import TipoParceiro

class ParceiroBase(BaseModel):
    nome: str
    id_tipo_parceiro: int

class ParceiroCreate(ParceiroBase):
    pass

class Parceiro(ParceiroBase):
    id: int
    tipo_info: TipoParceiro # Mostra o objeto 'TipoParceiro' aninhado
    
    class Config:
        from_attributes = True
        
class ParceirosPaginadosResponse(BaseModel):
    total_count: int
    items : List[Parceiro]
    
    class Config:
        from_attributes = True