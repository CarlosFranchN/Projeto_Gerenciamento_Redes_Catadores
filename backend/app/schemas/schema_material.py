from pydantic import BaseModel
from datetime import datetime
from typing import List,Optional
from .schema_categoria import Categoria
class MaterialBase(BaseModel):
    nome: str
    unidade_medida: str = 'Kg'
    id_categoria: Optional[int] = None
    ativo: bool = True 
class MaterialCreate(MaterialBase):
    pass

class MaterialUpdate(BaseModel): 
    nome: Optional[str] = None
    unidade_medida: Optional[str] = None
    id_categoria: Optional[int] = None
    ativo: Optional[bool] = None

class Material(MaterialBase):
    id: int
    codigo: Optional[str] = None
    categoria_info : Optional[Categoria] = None
    
    class Config:
        from_attributes = True 