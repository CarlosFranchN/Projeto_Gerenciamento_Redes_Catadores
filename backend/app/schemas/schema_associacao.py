from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

# =============== PARCEIRO ===============
class ParceiroInfo(BaseModel):
    """Schema simples para informações do parceiro"""
    id: int
    nome: str
    
    model_config = ConfigDict(from_attributes=True)

# =============== ASSOCIACAO ===============
class AssociacaoBase(BaseModel):
    lider: Optional[str] = Field(None, max_length=255)
    telefone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=255)
    cnpj: Optional[str] = Field(None, max_length=18)
    
    # Campos de endereço
    logradouro: Optional[str] = None
    numero: Optional[str] = Field(None, max_length=20)
    complemento: Optional[str] = Field(None, max_length=50)
    bairro: Optional[str] = Field(None, max_length=100)
    cidade: Optional[str] = Field(None, max_length=100)
    uf: Optional[str] = Field(None, min_length=2, max_length=2)
    
    status: str = Field(default="ativo", pattern="^(ativo|inativo|pendente)$")

class AssociacaoCreate(AssociacaoBase):
    parceiro_id: int
    nome: str  # Nome do parceiro

class AssociacaoUpdate(BaseModel):
    lider: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    status: Optional[str] = None
    # Endereço
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None

class AssociacaoResponse(AssociacaoBase):
    id: int
    parceiro_id: int
    nome: str  # ✅ Nome do parceiro (não o objeto inteiro)
    data_cadastro: datetime
    ativo: bool
    
    model_config = ConfigDict(from_attributes=True)

class AssociacaoWithParceiro(AssociacaoResponse):
    parceiro_info: Optional[ParceiroInfo] = None

class AssociacoesPaginadasResponse(BaseModel):
    total_count: int
    items: list[AssociacaoResponse]