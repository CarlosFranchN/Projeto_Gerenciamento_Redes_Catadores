
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ..models import TipoTransacaoEnum 

class TransacaoBase(BaseModel):
    descricao: Optional[str] = None 
    valor: float

class TransacaoCreate(TransacaoBase):
    tipo: TipoTransacaoEnum 
    
    
    id_compra_associada: Optional[int] = None
    id_venda_associada: Optional[int] = None

class Transacao(TransacaoBase):
    id: int
    data: datetime
    tipo: TipoTransacaoEnum 
    
    
    id_compra_associada: Optional[int] = None
    id_venda_associada: Optional[int] = None

    class Config:
        from_attributes = True
        
class TransacoesPaginadas(BaseModel):
    total_count: int
    items: List[Transacao]

class SaldoResponse(BaseModel):
    saldo_atual: float
    total_entradas: float
    total_saidas: float