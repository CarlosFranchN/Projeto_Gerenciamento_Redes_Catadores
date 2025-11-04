from pydantic import BaseModel

class TipoDoadorBase(BaseModel):
    nome: str

class TipoDoadorCreate(TipoDoadorBase):
    pass

class TipoDoador(TipoDoadorBase):
    id: int

    class Config:
        from_attributes = True