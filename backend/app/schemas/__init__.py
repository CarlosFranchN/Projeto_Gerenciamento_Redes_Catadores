# backend/app/schemas/__init__.py

from .schema_usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from .schema_token import Token, TokenData
from .schema_associacao import AssociacaoCreate, AssociacaoResponse, AssociacaoUpdate, AssociacoesPaginadasResponse , AssociacoesListResponse
from .schema_producao import *
from .schema_grupo import GrupoCreate, GrupoResponse, GrupoUpdate
from .schema_municipio import MunicipioCreate, MunicipioResponse , MunicipioUpdate , MunicipioBase
from .schema_afiliados import (                    
    AfiliadoCreate, 
    AfiliadoUpdate, 
    AfiliadoResponse, 
    AfiliadosListResponse
)
from .schema_categoria import CategoriaMaterial, CategoriaResponse

__all__ = [
    "UsuarioCreate", "UsuarioResponse", "UsuarioUpdate", "Token", "TokenData",
    "AssociacaoCreate", "AssociacaoResponse", "AssociacoesListResponse", "AssociacaoUpdate", "AssociacoesPaginadasResponse" , "AssociacoesListResponse"
    "ProducaoImpactoCreate", "ProducaoImpactoResponse",
    "GrupoCreate", "GrupoResponse", "GrupoUpdate",
    "MunicipioCreate", "MunicipioResponse", "MunicipioUpdate", "MunicipioUpdate" , "MunicipioBase"
    "AfiliadoCreate", "AfiliadoUpdate", "AfiliadoResponse", "AfiliadosListResponse",  
    "CategoriaMaterial", "CategoriaResponse"
]