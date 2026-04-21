from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from .schema_categoria import CategoriaMaterial 
class ProducaoImpactoBase(BaseModel):
    mes: int = Field(..., ge=1, le=12, description="Mês (1-12)")
    ano: int = Field(..., ge=2020, le=2100, description="Ano")
    categoria: CategoriaMaterial = Field(..., description="Tipo do material")
    peso_kg: float = Field(..., gt=0, description="Quantidade em KG")
    valor_gerado: Optional[float] = Field(None, ge=0, description="Valor gerado financeiro")
    observado: Optional[str] = Field(None, max_length=500, description="Observações")

class ProducaoImpactoCreate(ProducaoImpactoBase):
    associacao_id: int = Field(..., description="ID da Associação é obrigatório")

class ProducaoImpactoUpdate(BaseModel):
    peso_kg: Optional[float] = Field(None, gt=0)
    valor_gerado: Optional[float] = Field(None, ge=0)
    observado: Optional[str] = Field(None, max_length=500)

class ProducaoImpactoResponse(ProducaoImpactoBase):
    id: int
    associacao_id: int
    
    # Sintaxe perfeita do Pydantic V2!
    model_config = ConfigDict(from_attributes=True)

class ProducaoImpactoListResponse(BaseModel):
    items: list[ProducaoImpactoResponse]
    total: int