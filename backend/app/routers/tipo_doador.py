from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/tipo_doador",
    tags=["Tipos de Doador"]
)

@router.post("/", response_model=schemas.TipoDoador, status_code=status.HTTP_201_CREATED)
def create_tipo_doador(
    tipo_doador: schemas.TipoDoadorCreate, 
    db: Session = Depends(get_db)
):
    """
    Cria um novo tipo de doador (ex: ASSOCIACAO, ORGAO_PUBLICO).
    """
    db_tipo_existente = crud.get_tipo_doador_by_nome(db, nome=tipo_doador.nome)
    if db_tipo_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Tipo de doador com o nome '{tipo_doador.nome}' já existe."
        )
    return crud.create_tipo_doador(db=db, tipo_doador=tipo_doador)

@router.get("/", response_model=List[schemas.TipoDoador])
def read_all_tipos_doador(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Lista todos os tipos de doador cadastrados.
    """
    tipos = crud.get_all_tipos_doador(db, skip=skip, limit=limit)
    return tipos

@router.get("/{tipo_doador_id}", response_model=schemas.TipoDoador)
def read_tipo_doador(tipo_doador_id: int, db: Session = Depends(get_db)):
    """
    Busca um tipo de doador específico pelo seu ID.
    """
    db_tipo = crud.get_tipo_doador(db, tipo_doador_id=tipo_doador_id)
    if db_tipo is None:
        raise HTTPException(status_code=404, detail="Tipo de doador não encontrado")
    return db_tipo