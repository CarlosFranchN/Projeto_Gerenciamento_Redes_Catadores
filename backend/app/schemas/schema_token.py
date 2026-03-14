from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

class RefreshTokenCreate(BaseModel):
    usuario_id: int
    token: str
    expires_at: datetime

class RefreshTokenResponse(BaseModel):
    id: int
    usuario_id: int
    expires_at: datetime
    revoked: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)