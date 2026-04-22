from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class EnderecoCacheBase(BaseModel):
    cnpj: str = Field(..., min_length=14, max_length=18, description="CNPJ")
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = Field(None, min_length=2, max_length=2)

class EnderecoCacheCreate(EnderecoCacheBase):
    expires_at: Optional[datetime] = None

class EnderecoCacheResponse(EnderecoCacheBase):
    id: int
    consulted_at: datetime
    expires_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)