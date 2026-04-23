from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List

class MunicipioBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    uf: str = Field(..., min_length=2, max_length=2)
    qtd_grupos: int = Field(default=0, ge=0)
    qtd_associacoes: int = Field(default=0, ge=0)
    qtd_integrantes: Optional[int] = 0
    ativo: bool = True

class MunicipioCreate(MunicipioBase):
    pass

class MunicipioUpdate(BaseModel):
    nome: Optional[str] = None
    uf: Optional[str] = None
    qtd_grupos: Optional[int] = None
    qtd_associacoes: Optional[int] = None
    qtd_integrantes: Optional[int] = Field(None, ge=0) # Adicionado aqui!
    ativo: Optional[bool] = None

class MunicipioResponse(MunicipioBase):
    id: int
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class MunicipioListResponse(BaseModel):
    items: list[MunicipioResponse]
    total: int
    
class MunicipioPaginated(BaseModel):
    total: int
    page: int
    page_size: int
    pages: int
    items: List[MunicipioResponse]
    
    model_config = ConfigDict(from_attributes=True)
    