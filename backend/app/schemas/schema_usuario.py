from pydantic import BaseModel

class UsuarioBase(BaseModel):
    username: str

class UsuarioCreate(UsuarioBase):
    password: str # Usado apenas na criação, nunca retornado

class Usuario(UsuarioBase):
    id: int
    
    class Config:
        from_attributes = True

# Schema para o Token JWT
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None