# auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Response # 1. Importado o Response
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

# 2. Removido o response_model=schemas.Token, pois não retornaremos mais o token no corpo
@router.post("/token")
def login(
    response: Response, # <-- Injetamos o Response aqui
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login de usuário com Cookie Seguro (LGPD)"""
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
    
    # ===== A MÁGICA DA SEGURANÇA ACONTECE AQUI =====
    # Embutimos o token diretamente no cabeçalho da resposta
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,  # Impede ataques XSS (JavaScript não lê o cookie)
        secure=False,   # Mude para True em Produção (quando tiver HTTPS)
        samesite="lax", # Impede ataques CSRF
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60 # Tempo de vida em segundos
    )
    
    # O frontend não recebe mais o token, apenas os dados úteis para a interface
    return {
        "message": "Login realizado com sucesso",
        "user": {
            "username": user.username,
            "role": user.role,
            "nome": user.nome
        }
    }

# 3. NOVA ROTA: O backend precisa destruir o cookie no Logout
@router.post("/logout")
def logout(response: Response):
    """Destrói a sessão do usuário"""
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax",
        secure=False # Mude para True em Produção
    )
    return {"message": "Logout realizado com sucesso"}

@router.post("/token/refresh")
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