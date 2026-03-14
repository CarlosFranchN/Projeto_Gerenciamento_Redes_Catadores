from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ProducaoBase(BaseModel):
    mes: int = Field(..., ge=1, le=12)
    ano: int
    kg: float
    valor_venda: Optional[float] = None
    observado: Optional[str] = None

class ProducaoCreate(ProducaoBase):
    associacao_id: Optional[int] = None

class ProducaoResponse(ProducaoBase):
    id: int
    associacao_id: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True