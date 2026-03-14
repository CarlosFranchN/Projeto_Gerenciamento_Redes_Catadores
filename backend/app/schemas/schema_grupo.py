from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class GrupoBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=255)
    integrantes: int = Field(default=0, ge=0)
    cidade: Optional[str] = Field(None, max_length=100)
    uf: Optional[str] = Field(None, min_length=2, max_length=2)
    ativo: bool = True

class GrupoCreate(GrupoBase):
    associacao_id: Optional[int] = None

class GrupoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=3, max_length=255)
    integrantes: Optional[int] = Field(None, ge=0)
    cidade: Optional[str] = None
    uf: Optional[str] = None
    ativo: Optional[bool] = None

class GrupoResponse(GrupoBase):
    id: int
    associacao_id: Optional[int]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class GrupoListResponse(BaseModel):
    items: list[GrupoResponse]
    total: int