from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .schema_doador import Doador # Importa o schema do Doador

# Este schema é para os DETALHES específicos da associação
class AssociacaoBase(BaseModel):
    lider: Optional[str] = None
    telefone: Optional[str] = None
    cnpj: Optional[str] = None
    ativo: bool = True

class AssociacaoCreate(AssociacaoBase):
    # Para CRIAR uma associação, precisamos também dos dados do Doador-pai
    nome: str
    id_tipo_doador: int # Vamos simplificar e assumir que o tipo é sempre 'ASSOCIACAO'
    # Mas para flexibilidade, vamos pedir o nome e o tipo do doador

class AssociacaoUpdate(AssociacaoBase):
    # Para ATUALIZAR, podemos querer atualizar o nome também
    nome: Optional[str] = None

class Associacao(AssociacaoBase):
    id: int
    doador_id: int
    

    # Inclui o objeto Doador-pai (para pegar o NOME)
    doador_info: Doador 

    class Config:
        from_attributes = True