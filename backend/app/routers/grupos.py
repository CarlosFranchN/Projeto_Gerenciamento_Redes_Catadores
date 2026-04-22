from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app import crud, schemas
from app.dependencies import get_current_user
from app import models

router = APIRouter(
    prefix="/api/grupos",
    tags=["Grupos"]
)

@router.get("/", response_model=List[schemas.GrupoResponse])
def read_grupos(
    skip: int = 0,
    limit: int = 100,
    ativo: Optional[bool] = True,
    db: Session = Depends(get_db)
):
    """Listar todos os grupos (público)"""
    return crud.get_all_grupos(db, skip=skip, limit=limit, ativo=ativo)

@router.get("/{grupo_id}", response_model=schemas.GrupoResponse)
def read_grupo(
    grupo_id: int,
    db: Session = Depends(get_db)
):
    """Obter grupo por ID (público)"""
    db_grupo = crud.get_grupo_by_id(db, grupo_id)
    if not db_grupo:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    return db_grupo

@router.post("/", response_model=schemas.GrupoResponse, status_code=status.HTTP_201_CREATED)
def create_grupo(
    grupo: schemas.GrupoCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Criar novo grupo (requer autenticação)"""
    return crud.create_grupo(db, grupo=grupo)

@router.put("/{grupo_id}", response_model=schemas.GrupoResponse)
def update_grupo(
    grupo_id: int,
    grupo_update: schemas.GrupoUpdate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Atualizar grupo (requer autenticação)"""
    db_grupo = crud.update_grupo(db, grupo_id=grupo_id, grupo_update=grupo_update)
    if not db_grupo:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    return db_grupo

@router.delete("/{grupo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grupo(
    grupo_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Soft delete - marca como inativo (requer autenticação)"""
    success = crud.delete_grupo(db, grupo_id=grupo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    return None