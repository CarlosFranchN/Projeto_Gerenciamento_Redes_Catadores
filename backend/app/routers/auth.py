from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app import models, schemas
from app.database import get_db
# from app.core.security import authenticate_user, create_access_token, create_refresh_token
from app.core.security import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_password_hash
)

from app.core.config import settings

router = APIRouter(
    prefix="/api",
    tags=["Autenticação"]
)

@router.post("/token", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login de usuário"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    
    # Cria refresh token
    refresh_token = create_refresh_token(db, user_id=user.id)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/token/refresh", response_model=schemas.Token)
def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """Renovar access token usando refresh token"""
    # Implementar lógica de validação do refresh token
    pass

@router.post("/usuarios/", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED)
def create_usuario(
    usuario: schemas.UsuarioCreate,
    db: Session = Depends(get_db)
):
    """Criar novo usuário (registro público ou admin)"""
    # Verifica se usuário já existe
    existing = db.query(models.Usuario).filter(
        models.Usuario.username == usuario.username
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário já existe"
        )
    
    # Cria usuário
    db_user = models.Usuario(
        username=usuario.username,
        hashed_password=get_password_hash(usuario.password),
        nome=usuario.nome,
        role=usuario.role
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user