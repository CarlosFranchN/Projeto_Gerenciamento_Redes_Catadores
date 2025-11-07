from pydantic import BaseModel
from datetime import datetime
from typing import List,Optional

class MaterialBase(BaseModel):
    nome: str
    unidade_medida: str = 'Kg'
    categoria: Optional[str] = None
    ativo: bool = True 
class MaterialCreate(MaterialBase):
    pass

class MaterialUpdate(MaterialBase):
    pass

class Material(MaterialBase):
    id: int
    codigo: Optional[str] = None
    
    class Config:
        from_attributes = True 