from pydantic import BaseModel
from typing import Optional
from .schema_tipo_doador import TipoDoador # Importa o schema do Tipo

class DoadorBase(BaseModel):
    nome: str
    id_tipo_doador: int

class DoadorCreate(DoadorBase):
    pass

class Doador(DoadorBase):
    id: int
    tipo_info: TipoDoador # Mostra o objeto 'TipoDoador' aninhado

    class Config:
        from_attributes = True