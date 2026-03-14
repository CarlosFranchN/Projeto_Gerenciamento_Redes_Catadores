from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List, Optional

from app import models
from .. import crud, schemas
from app.database import get_db
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/api/associacoes",  # ✅ Adicionado /api
    tags=["Associações"]
)

@router.post("/", response_model=schemas.AssociacaoResponse, status_code=status.HTTP_201_CREATED)
def create_associacao(
    associacao: schemas.AssociacaoCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Criar nova associação (requer autenticação)"""
    try:
        return crud.create_associacao(db=db, associacao=associacao)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=dict)
def read_all_associacoes(
    skip: int = 0,
    limit: int = 100,
    ativo: Optional[bool] = True,
    db: Session = Depends(get_db)
):
    """Listar todas associações (público)"""
    return crud.get_all_associacoes(db, skip=skip, limit=limit)

@router.get("/ativas", response_model=List[schemas.AssociacaoResponse])
def read_associacoes_ativas(db: Session = Depends(get_db)):
    """Listar apenas associações ativas (para o frontend público)"""
    return crud.get_associacoes_ativas(db)

@router.get("/{associacao_id}", response_model=schemas.AssociacaoResponse)
def read_associacao(
    associacao_id: int,
    db: Session = Depends(get_db)
):
    """Consultar uma associação pelo ID"""
    db_assoc = crud.get_associacao(db, associacao_id=associacao_id)
    if not db_assoc:
        raise HTTPException(status_code=404, detail="Associação não encontrada")
    return db_assoc

@router.put("/{associacao_id}", response_model=schemas.AssociacaoResponse)
def update_associacao(
    associacao_id: int,
    associacao_update: schemas.AssociacaoUpdate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Atualizar associação (requer autenticação)"""
    db_assoc = crud.update_associacao(
        db,
        associacao_id=associacao_id,
        associacao_update=associacao_update
    )
    if not db_assoc:
        raise HTTPException(status_code=404, detail="Associação não encontrada")
    return db_assoc

@router.delete("/{associacao_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_associacao(
    associacao_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Soft delete - marca como inativa (requer autenticação)"""
    db_assoc = crud.delete_associacao(db, associacao_id=associacao_id)
    if not db_assoc:
        raise HTTPException(status_code=404, detail="Associação não encontrada")
    return Response(status_code=status.HTTP_204_NO_CONTENT)