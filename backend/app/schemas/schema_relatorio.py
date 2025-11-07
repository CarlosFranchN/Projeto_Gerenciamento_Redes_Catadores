from pydantic import BaseModel
from typing import List

class ReportSummaryResponse(BaseModel):
    total_recebido: float
    total_comprado_qtd: float 
    total_gasto_compras: float 
    total_vendido: float
    receita_periodo: float
    lucro_bruto: float 

class ReportPorMaterialItem(BaseModel):
    nome: str
    unidade_medida: str
    recebido: float = 0.0
    comprado: float = 0.0 
    vendido: float = 0.0
    saldo: float = 0.0 
    receita: float = 0.0
    
class ReportPorParceiroItem(BaseModel): 
    nome: str
    tipo_parceiro: str
    quantidade_recebida: float = 0.0
    quantidade_comprada: float = 0.0