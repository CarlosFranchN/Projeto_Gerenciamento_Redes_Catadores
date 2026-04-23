from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List

class GrupoBase(BaseModel):
    # Padronizado com o banco: qtd_integrantes
    nome: str = Field(..., min_length=3, max_length=255)
    cidade: Optional[str] = Field(None, max_length=100)
    uf: Optional[str] = Field(None, min_length=2, max_length=2)
    qtd_integrantes: int = Field(default=0, ge=0) # Removi o 'integrantes' duplicado
    ativo: bool = True

class GrupoCreate(GrupoBase):
    associacao_id: Optional[int] = None

class GrupoUpdate(BaseModel):
    # Aqui colocamos tudo como Optional para permitir atualizações parciais
    nome: Optional[str] = Field(None, min_length=3, max_length=255)
    qtd_integrantes: Optional[int] = Field(None, ge=0) # Adicionado aqui!
    cidade: Optional[str] = None
    uf: Optional[str] = None
    ativo: Optional[bool] = None

class GrupoResponse(GrupoBase):
    id: int
    associacao_id: Optional[int] = None
    created_at: Optional[datetime] = None
    
    # Importante para o SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

class GrupoPaginated(BaseModel):
    total: int
    page: int
    page_size: int
    pages: int
    items: List[GrupoResponse]