from pydantic import BaseModel
from datetime import datetime
from typing import List,Optional
from .schema_material import Material


class ReportSummaryResponse(BaseModel):
    total_recebido: float
    total_vendido: float
    receita_periodo: float
    
class ReportPorMaterialItem(BaseModel):
    # id_material: int # Opcional, se o frontend precisar
    nome: str
    unidade_medida: str
    recebido: float = 0.0
    vendido: float = 0.0
    saldo: float = 0.0 # Calculado: recebido - vendido
    receita: float = 0.0
    
class ReportPorAssociacaoItem(BaseModel):
    nome:str
    quantidade:float = 0.0