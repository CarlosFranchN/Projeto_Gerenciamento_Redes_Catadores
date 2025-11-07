from pydantic import BaseModel, EmailStr
from typing import Optional, List

class CompradorBase(BaseModel):
    nome: str
    cnpj: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    ativo: bool = True

class CompradorCreate(CompradorBase):
    pass

class CompradorUpdate(CompradorBase):
    pass 
class Comprador(CompradorBase):
    id: int
    
    class Config:
        from_attributes = True


class CompradoresPaginadosResponse(BaseModel):
    total_count: int
    items: List[Comprador]

    class Config:
        from_attributes = True