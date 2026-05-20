from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app import models, schemas
from app.database import get_db
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

@router.post("/token")
def login(
    response: Response, 
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login de usuário compatível com LocalStorage e Cookies de produção"""
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
    
    refresh_token = create_refresh_token(db, user_id=user.id)
    
    # Configuração correta de cookies para produção (Vercel -> Render)
    # Mantemos o cookie configurado certo caso você precise dele no futuro
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,  
        secure=True,     # 🔥 Corrigido: Obrigatoriamente True em ambiente HTTPS (Nuvem)
        samesite="none", # 🔥 Corrigido: Permite o tráfego cross-origin (Vercel para Render)
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60 
    )
    
    # 🔥 AQUI ESTÁ A CORREÇÃO: Enviamos o access_token explicitamente no JSON
    # para que o seu novo interceptador do Axios consiga capturar e salvar no LocalStorage!
    return {
        "message": "Login realizado com sucesso",
        "access_token": access_token,  # 🚀 Adicionado para alimentar o Frontend
        "user": {
            "username": user.username,
            "role": user.role,
            "nome": user.nome
        }
    }


@router.post("/logout")
def logout(response: Response):
    """Destrói a sessão do usuário"""
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="none", # 🔥 Alinhado com a rota de login
        secure=True      # 🔥 Alinhado com a rota de login
    )
    return {"message": "Logout realizado com sucesso"}

@router.post("/token/refresh")
def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """Renovar access token usando refresh token"""
    pass

@router.post("/usuarios/", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED)
def create_usuario(
    usuario: schemas.UsuarioCreate,
    db: Session = Depends(get_db)
):
    """Criar novo usuário (txt público ou admin)"""
    existing = db.query(models.Usuario).filter(
        models.Usuario.username == usuario.username
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário já existe"
        )
    
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