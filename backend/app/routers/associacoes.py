from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from typing import List

from app import crud, models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/associacoes",
    tags=["associacoes"]
)


@router.post("/", response_model=schemas.Associacao, summary="Registra uma nova associação")
def create_associacao(
    associacao: schemas.AssociacaoCreate,
    db: Session = Depends(get_db)):
    # db_associacao = crud.create_associacao(db=db, associacao=associacao)
    db_associacao = db.query(models.Associacao).filter(models.Associacao.nome == associacao.nome).first()
    if db_associacao:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Associação já cadastrada")
    return crud.create_associacao(db=db, associacao=associacao)

@router.get("/",response_model=List[schemas.Associacao], summary="Lista todas as associações")
def read_all_associacoes(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)):
    associacoes = crud.get_all_associacoes(db, skip=skip, limit=limit)
    return associacoes

@router.get("/{id_associacao}", response_model=schemas.Associacao, summary="Consulta uma associação pelo ID")
def read_associacao(
    id_associacao: int,
    db: Session = Depends(get_db)
):
    db_associacao = crud.get_associacao(
        db,
        id_associacao=id_associacao)
    if db_associacao is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associação não encontrada")
    return db_associacao