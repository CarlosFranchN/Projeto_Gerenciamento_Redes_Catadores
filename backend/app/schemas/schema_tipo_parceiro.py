from pydantic import BaseModel

class TipoParceiroBase(BaseModel):
    nome: str

class TipoParceiroCreate(TipoParceiroBase):
    pass

class TipoParceiro(TipoParceiroBase):
    id: int
    
    class Config:
        from_attributes = True