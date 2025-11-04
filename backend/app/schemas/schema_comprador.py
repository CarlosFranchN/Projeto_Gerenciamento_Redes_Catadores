from pydantic import BaseModel, EmailStr
from typing import Optional,List

class CompradorBase(BaseModel):
    nome: str
    cnpj: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None # Pydantic valida o email!
    ativo: bool = True

class CompradorCreate(CompradorBase):
    pass # Por enquanto, criar e atualizar usam os mesmos campos

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