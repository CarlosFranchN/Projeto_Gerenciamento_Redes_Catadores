from pydantic import BaseModel
from typing import List

class ReportSummaryResponse(BaseModel):
    total_recebido: float
    total_vendido: float
    receita_periodo: float

class ReportPorMaterialItem(BaseModel):
    nome: str
    unidade_medida: str
    recebido: float = 0.0
    vendido: float = 0.0
    saldo: float = 0.0
    receita: float = 0.0

class ReportPorDoadorItem(BaseModel): 
    nome: str 
    quantidade: float = 0.0

class Config: 
    from_attributes = True