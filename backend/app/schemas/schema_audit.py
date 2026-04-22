from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, Dict, Any

class AuditLogBase(BaseModel):
    acao: str = Field(..., max_length=50, description="Ação (CREATE, UPDATE, DELETE, LOGIN)")
    tabela_afetada: Optional[str] = Field(None, max_length=50)
    registro_id: Optional[int] = None
    dados_antigos: Optional[Dict[str, Any]] = None
    dados_novos: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = Field(None, max_length=45)

class AuditLogCreate(AuditLogBase):
    usuario_id: Optional[int] = None

class AuditLogResponse(AuditLogBase):
    id: int
    usuario_id: Optional[int]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class AuditLogListResponse(BaseModel):
    items: list[AuditLogResponse]
    total: int