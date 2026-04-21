# backend/app/schemas/schema_afiliado.py

from pydantic import BaseModel, Field, validator , ConfigDict, field_validator
from typing import Optional
from datetime import date, datetime
import re


# =============== SCHEMA BASE ===============
class AfiliadoBase(BaseModel):
    """Campos comuns para criação e atualização"""
    nome: str = Field(..., min_length=3, max_length=150, description="Nome completo do afiliado")
    cpf: Optional[str] = Field(None, description="CPF no formato 000.000.000-00")
    funcao: Optional[str] = Field(None, max_length=50, description="Ex: Triador, Prensista, Coordenador")
    data_filiacao: Optional[date] = Field(None, description="Data de filiação à associação")
    
    @field_validator('cpf')
    def validar_cpf(cls, v):
        if v is None:
            return v
        
        # Remove formatação (pontos e traço)
        cpf_limpo = re.sub(r'\D', '', v)
        
        # Valida tamanho
        if len(cpf_limpo) != 11:
            raise ValueError('CPF deve ter 11 dígitos')
        
        # Valida dígitos repetidos (CPFs inválidos comuns)
        if cpf_limpo in ['00000000000', '11111111111', '22222222222', 
                         '33333333333', '44444444444', '55555555555',
                         '66666666666', '77777777777', '88888888888', '99999999999']:
            raise ValueError('CPF inválido')
        
        # Retorna formatado
        return f'{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}'
    
    class Config:
        json_schema_extra = {
            "example": {
                "nome": "João da Silva",
                "cpf": "123.456.789-00",
                "funcao": "Triador",
                "data_filiacao": "2024-01-15"
            }
        }


# =============== SCHEMA DE CRIAÇÃO ===============
class AfiliadoCreate(AfiliadoBase):
    """Dados necessários para criar um afiliado"""
    associacao_id: int = Field(..., description="ID da associação à qual o afiliado pertence")


# =============== SCHEMA DE ATUALIZAÇÃO ===============
class AfiliadoUpdate(BaseModel):
    """Campos que podem ser atualizados (todos opcionais)"""
    nome: Optional[str] = Field(None, min_length=3, max_length=150)
    cpf: Optional[str] = None
    funcao: Optional[str] = Field(None, max_length=50)
    data_filiacao: Optional[date] = None
    ativo: Optional[bool] = None
    
    @field_validator('cpf')
    def validar_cpf(cls, v):
        if v is None:
            return v
        cpf_limpo = re.sub(r'\D', '', v)
        if len(cpf_limpo) != 11:
            raise ValueError('CPF deve ter 11 dígitos')
        return f'{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}'


# =============== SCHEMA DE RESPOSTA ===============
class AfiliadoResponse(AfiliadoBase):
    """Dados retornados pela API (com campos adicionais)"""
    id: int
    associacao_id: int
    ativo: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# =============== SCHEMA COM DADOS DA ASSOCIAÇÃO ===============
class AfiliadoWithAssociacaoResponse(AfiliadoResponse):
    """Resposta incluindo dados da associação"""
    associacao_nome: Optional[str] = None
    
    class Config:
        from_attributes = True


# =============== SCHEMA PARA LISTAGEM PAGINADA ===============
class AfiliadosListResponse(BaseModel):
    """Resposta para listagem paginada de afiliados"""
    items: list[AfiliadoResponse]
    total: int
    page: int
    page_size: int
    pages: int
    
    model_config = ConfigDict(from_attributes=True)