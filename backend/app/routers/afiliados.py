# backend/app/routers/afiliados.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas, crud
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/afiliados", tags=["Afiliados"])

@router.post("/", response_model=schemas.AfiliadoResponse, status_code=status.HTTP_201_CREATED)
def create_afiliado(
    afiliado: schemas.AfiliadoCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Criar novo afiliado"""
    # Verifica se CPF já existe
    existing = db.query(models.Afiliado).filter(
        models.Afiliado.cpf == afiliado.cpf
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="CPF já cadastrado")
    
    return crud.create_afiliado(db=db, afiliado=afiliado)

@router.get("/", response_model=schemas.AfiliadosListResponse)
def read_afiliados(
    skip: int = 0,
    limit: int = 100,
    associacao_id: int = None,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Listar afiliados (com filtros opcionais)"""
    afiliados, total = crud.get_afiliados(
        db, skip=skip, limit=limit, associacao_id=associacao_id
    )
    
    return {
        "items": afiliados,
        "total": total,
        "page": (skip // limit) + 1,
        "page_size": limit,
        "pages": (total + limit - 1) // limit
    }

@router.get("/{afiliado_id}", response_model=schemas.AfiliadoResponse)
def read_afiliado(
    afiliado_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Obter detalhes de um afiliado"""
    afiliado = crud.get_afiliado(db, afiliado_id=afiliado_id)
    if not afiliado:
        raise HTTPException(status_code=404, detail="Afiliado não encontrado")
    return afiliado

@router.put("/{afiliado_id}", response_model=schemas.AfiliadoResponse)
def update_afiliado(
    afiliado_id: int,
    afiliado: schemas.AfiliadoUpdate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Atualizar dados de um afiliado"""
    return crud.update_afiliado(db, afiliado_id=afiliado_id, afiliado=afiliado)

@router.delete("/{afiliado_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_afiliado(
    afiliado_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Desativar afiliado (soft delete)"""
    crud.delete_afiliado(db, afiliado_id=afiliado_id)
    return None