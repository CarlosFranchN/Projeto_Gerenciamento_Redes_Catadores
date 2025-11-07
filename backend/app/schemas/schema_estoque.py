from pydantic import BaseModel
from typing import Optional, List

class EstoqueGeralResponseItem(BaseModel):
    id: int
    codigo: Optional[str] = None
    nome: str
    categoria: Optional[str] = None
    unidade_medida: str
    ativo: bool
    estoque_atual: float 

    class Config:
        from_attributes = True

class EstoquePaginadoResponse(BaseModel):
    total_count: int
    items: List[EstoqueGeralResponseItem]

    class Config:
        from_attributes = True