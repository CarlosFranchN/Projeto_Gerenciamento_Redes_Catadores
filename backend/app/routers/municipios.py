from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app import crud, schemas
from app.dependencies import get_current_user
from app import models

router = APIRouter(
    prefix="/api/municipios",
    tags=["Municípios"]
)

@router.get("/", response_model=List[schemas.MunicipioResponse])
def read_municipios(
    skip: int = 0,
    limit: int = 100,
    ativo: Optional[bool] = True,
    db: Session = Depends(get_db)
):
    """Listar todos os municípios (público)"""
    return crud.get_all_municipios(db, skip=skip, limit=limit, ativo=ativo)

@router.get("/{municipio_id}", response_model=schemas.MunicipioResponse)
def read_municipio(
    municipio_id: int,
    db: Session = Depends(get_db)
):
    """Obter município por ID (público)"""
    db_municipio = crud.get_municipio_by_id(db, municipio_id)
    if not db_municipio:
        raise HTTPException(status_code=404, detail="Município não encontrado")
    return db_municipio

@router.post("/", response_model=schemas.MunicipioResponse, status_code=status.HTTP_201_CREATED)
def create_municipio(
    municipio: schemas.MunicipioCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Criar novo município (requer autenticação)"""
    try:
        return crud.create_municipio(db, municipio=municipio)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{municipio_id}", response_model=schemas.MunicipioResponse)
def update_municipio(
    municipio_id: int,
    municipio_update: schemas.MunicipioUpdate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Atualizar município (requer autenticação)"""
    db_municipio = crud.update_municipio(db, municipio_id=municipio_id, municipio_update=municipio_update)
    if not db_municipio:
        raise HTTPException(status_code=404, detail="Município não encontrado")
    return db_municipio

@router.delete("/{municipio_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_municipio(
    municipio_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Soft delete - marca como inativo (requer autenticação)"""
    success = crud.delete_municipio(db, municipio_id=municipio_id)
    if not success:
        raise HTTPException(status_code=404, detail="Município não encontrado")
    return None