from pydantic import BaseModel
from datetime import datetime
from typing import List,Optional

class MaterialBase(BaseModel):
    nome:str
    categoria: Optional[str] = None
    unidade_medida: str = 'Kg'
    
class MaterialCreate(MaterialBase):
    pass

class MaterialUpdate(MaterialBase):
    pass

class Material(MaterialBase):
    id : int
    codigo_material : Optional[str] = None
    
    class Config:
        orm_mode = True