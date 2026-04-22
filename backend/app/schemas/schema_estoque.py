from pydantic import BaseModel
from typing import Optional, List
from .schema_categoria import Categoria

class EstoqueGeralResponseItem(BaseModel):
    id: int
    codigo: Optional[str] = None
    nome: str
    
    unidade_medida: str
    ativo: bool
    estoque_atual: float 

    categoria_info: Optional[Categoria] = None
    class Config:
        from_attributes = True

class EstoquePaginadoResponse(BaseModel):
    total_count: int
    items: List[EstoqueGeralResponseItem]

    class Config:
        from_attributes = True