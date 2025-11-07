from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .schema_parceiro import Parceiro 

class AssociacaoBase(BaseModel):
    lider: Optional[str] = None
    telefone: Optional[str] = None
    cnpj: Optional[str] = None
    ativo: bool = True
class AssociacaoBase(BaseModel):
    lider: Optional[str] = None
    telefone: Optional[str] = None
    cnpj: Optional[str] = None
    ativo: bool = True

class AssociacaoCreate(AssociacaoBase):
    nome: str 
    

class AssociacaoUpdate(AssociacaoBase):
    
    nome: Optional[str] = None

class Associacao(AssociacaoBase):
    id: int
    parceiro_id: int 
    data_cadastro: datetime
    
    parceiro_info: Parceiro 
    
    class Config:
        from_attributes = True
        
class AssociacoesPaginadasResponse(BaseModel):
    total_count : int
    items : List[Associacao]
    
    class Config:
        from_attributes = True