from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class ProducaoBase(BaseModel):
    mes: int = Field(..., ge=1, le=12, description="Mês (1-12)")
    ano: int = Field(..., ge=2020, le=2100, description="Ano")
    kg: float = Field(..., gt=0, description="Quantidade em KG")
    valor_venda: Optional[float] = Field(None, ge=0, description="Valor de venda")
    observado: Optional[str] = Field(None, max_length=500, description="Observações")

class ProducaoCreate(ProducaoBase):
    associacao_id: Optional[int] = None

class ProducaoUpdate(BaseModel):
    kg: Optional[float] = Field(None, gt=0)
    valor_venda: Optional[float] = Field(None, ge=0)
    observado: Optional[str] = Field(None, max_length=500)

class ProducaoResponse(ProducaoBase):
    id: int
    associacao_id: Optional[int]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ProducaoListResponse(BaseModel):
    items: list[ProducaoResponse]
    total: int