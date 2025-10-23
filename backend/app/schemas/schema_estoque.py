from pydantic import BaseModel
from typing import List,Optional


class EstoqueGeralResponseItem(BaseModel):
    
    id: int
    codigo: Optional[str] = None
    nome: str
    categoria: Optional[str] = None
    unidade_medida: str
    
    estoque_atual: float

    
    class Config:
         orm_mode = True