from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class AssociacaoBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=150)
    cnpj: Optional[str] = Field(None, max_length=20)
    lider: Optional[str] = Field(None, max_length=100)
    telefone: Optional[str] = Field(None, max_length=20)
    endereco: Optional[str] = Field(None, max_length=255)
    bairro: Optional[str] = Field(None, max_length=100)
    cidade: Optional[str] = Field(None, max_length=100)
    uf: Optional[str] = Field(None, min_length=2, max_length=2)
    status: str = Field(default="ativo")
    municipio_id: Optional[int] = None
    grupo_id: Optional[int] = None

class AssociacaoCreate(AssociacaoBase):
    pass

class AssociacaoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=3, max_length=150)
    cnpj: Optional[str] = None
    lider: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    status: Optional[str] = None
    municipio_id: Optional[int] = None
    grupo_id: Optional[int] = None
    ativo: Optional[bool] = None

class AssociacaoResponse(AssociacaoBase):
    id: int
    ativo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# =============== SCHEMA PAGINADO (ESTE FALTAVA!) ===============
class AssociacoesPaginadasResponse(BaseModel):
    """Resposta para listagem paginada de associações"""
    items: List[AssociacaoResponse]
    total: int
    page: int
    page_size: int
    pages: int
    
    model_config = ConfigDict(from_attributes=True)

# =============== ALIAS PARA COMPATIBILIDADE ===============
# Se quiser usar AssociacoesListResponse como alias:
AssociacoesListResponse = AssociacoesPaginadasResponse