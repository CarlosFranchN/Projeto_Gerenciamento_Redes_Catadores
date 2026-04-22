from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app import models
from .. import crud, schemas
from app.database import get_db
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/api/usuarios",
    tags=["Usuários"]
)

@router.post("/", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED)
def create_usuario(
    usuario: schemas.UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Criar novo usuário (requer autenticação)"""
    db_user = crud.get_usuario_por_username(db, username=usuario.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    return crud.create_user(db=db, user=usuario)

@router.get("/", response_model=List[schemas.UsuarioResponse])
def read_all_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Listar todos usuários (requer autenticação)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Apenas administradores")
    return crud.get_all_usuarios(db, skip=skip, limit=limit)

@router.get("/me", response_model=schemas.UsuarioResponse)
def read_current_user(
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Obter dados do usuário atual"""
    return current_user

@router.get("/{usuario_id}", response_model=schemas.UsuarioResponse)
def read_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Consultar usuário por ID (requer autenticação)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Apenas administradores")
    db_user = crud.get_usuario_by_id(db, usuario_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user

@router.put("/{usuario_id}", response_model=schemas.UsuarioResponse)
def update_usuario(
    usuario_id: int,
    usuario_update: schemas.UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Atualizar usuário (requer autenticação)"""
    if current_user.role != "admin" and current_user.id != usuario_id:
        raise HTTPException(status_code=403, detail="Não autorizado")
    db_user = crud.update_user(db, usuario_id=usuario_id, user_update=usuario_update)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Soft delete - marca como inativo (requer autenticação)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Apenas administradores")
    success = crud.delete_user(db, usuario_id)
    if not success:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return None