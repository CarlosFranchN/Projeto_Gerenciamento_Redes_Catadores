from fastapi import APIRouter, Depends, HTTPException,status,Response
from sqlalchemy.orm import Session
from typing import List

# from app import crud, models, schemas
from app import models
from .. import crud, schemas
from app.database import get_db
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/associacoes",
    tags=["Associações"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/", response_model=schemas.Associacao)
def create_associacao(associacao: schemas.AssociacaoCreate, db: Session = Depends(get_db)):
    if crud.get_parceiro_by_nome(db, nome=associacao.nome):
        raise HTTPException(status_code=409,detail=f"Parceiro '{associacao.nome}' já existe.")
    
    try:
        return crud.create_associacao(db=db, associacao=associacao)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/", response_model=schemas.AssociacoesPaginadasResponse) 
def read_all_associacoes(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.get_all_associacoes(db, skip=skip, limit=limit)

@router.get("/{id_associacao}", response_model=schemas.Associacao, summary="Consulta uma associação pelo ID")
def read_associacao(associacao_id: int, db: Session = Depends(get_db)):
    db_assoc = crud.get_associacao(db, associacao_id=associacao_id)
    if not db_assoc:
        raise HTTPException(status_code=404, detail="Associação não encontrada")
    return db_assoc

@router.put("/{associacao_id}", response_model=schemas.Associacao)
def update_associacao(associacao_id: int, associacao_update: schemas.AssociacaoUpdate, db: Session = Depends(get_db)):
    db_assoc = crud.update_associacao(db, associacao_id=associacao_id, associacao_update=associacao_update)
    if not db_assoc:
        raise HTTPException(status_code=404, detail="Associação não encontrada")
    return db_assoc

@router.delete("/{associacao_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_associacao(associacao_id: int, db: Session = Depends(get_db)):
    db_assoc = crud.delete_associacao(db, associacao_id=associacao_id)
    if not db_assoc:
        raise HTTPException(status_code=404, detail="Associação não encontrada")
    return Response(status_code=status.HTTP_204_NO_CONTENT)