from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/doadores",
    tags=["Doadores"]
)

@router.post("/", response_model=schemas.Doador, status_code=status.HTTP_201_CREATED)
def create_doador(
    doador: schemas.DoadorCreate, 
    db: Session = Depends(get_db)
):
    """
    Cria um novo doador genérico (ex: Pessoa Física, Órgão Público).
    Para criar uma Associação, use o endpoint /associacoes/.
    """
    # Verifica se o tipo de doador existe
    db_tipo_doador = crud.get_tipo_doador(db, tipo_doador_id=doador.id_tipo_doador)
    if not db_tipo_doador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de Doador com ID {doador.id_tipo_doador} não encontrado."
        )
    
    # Verifica se o nome do doador já existe
    db_doador_existente = crud.get_doador_by_nome(db, nome=doador.nome)
    if db_doador_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Um doador com o nome '{doador.nome}' já existe."
        )

    return crud.create_doador(db=db, doador=doador)

@router.get("/", response_model=List[schemas.Doador])
def read_all_doadores(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Lista todos os doadores cadastrados (Associações, Externos, etc.).
    """
    doadores = crud.get_all_doadores(db, skip=skip, limit=limit)
    return doadores

@router.get("/{doador_id}", response_model=schemas.Doador)
def read_doador(doador_id: int, db: Session = Depends(get_db)):
    """
    Busca um doador específico pelo seu ID.
    """
    db_doador = crud.get_doador(db, doador_id=doador_id)
    if db_doador is None:
        raise HTTPException(status_code=404, detail="Doador não encontrado")
    return db_doador