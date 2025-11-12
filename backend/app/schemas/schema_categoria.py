from pydantic import BaseModel
from typing import List

class CategoriaBase(BaseModel):
    nome: str
    
class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int
    class Config:
        from_attributes = True
        
class CategoriasPaginadasResponse(BaseModel):
    total_count: int
    items: List[Categoria]

    class Config:
        from_attributes = True