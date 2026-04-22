from pydantic import BaseModel, Field , ConfigDict
from typing import Optional, List
from datetime import date
from enum import Enum
class CategoriaMaterial(str, Enum):
    PET = "PET"
    PAPELAO = "Papelão"
    VIDRO = "Vidro"
    PLASTICO_DURO = "Plástico Duro"
    METAL = "Metal"
    MISTO = "Misto"

# 2. Se você quiser um endpoint para o frontend puxar a lista de categorias
class CategoriaResponse(BaseModel):
    nome: str
    valor: str

class CategoriasListResponse(BaseModel):
    total_count: int
    items: List[CategoriaResponse]
    
    model_config = ConfigDict(from_attributes=True)