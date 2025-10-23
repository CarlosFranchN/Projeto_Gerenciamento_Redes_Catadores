from pydantic import BaseModel
from datetime import datetime
from typing import List,Optional


class AssociacaoBase(BaseModel):
    nome: str
    lider: Optional[str] = None
    telefone: Optional[str] = None
    cnpj: Optional[str] = None
    ativo: bool = True

class AssociacaoCreate(AssociacaoBase):
    pass

class AssociacaoUpdate(AssociacaoBase):
    pass
class Associacao(AssociacaoBase):
    id: int
    data_cadastro: datetime

    class Config:
        orm_mode = True