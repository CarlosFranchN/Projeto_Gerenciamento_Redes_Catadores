from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class UsuarioBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    nome: Optional[str] = Field(None, max_length=255)
    role: str = Field(default="admin", pattern="^(admin|operador|visualizador)$")

class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=6)

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=255)
    ativo: Optional[bool] = None
    role: Optional[str] = Field(None, pattern="^(admin|operador|visualizador)$")

class UsuarioResponse(UsuarioBase):
    id: int
    ativo: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UsuarioLogin(BaseModel):
    username: str
    password: str