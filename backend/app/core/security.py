from datetime import datetime, timedelta, timezone
from typing import Any, Union, Optional
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app import models
from .config import settings
import secrets

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# =============== SENHA ===============

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar se senha plain bate com hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gerar hash da senha"""
    return pwd_context.hash(password)

# =============== TOKENS ===============

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Criar access token JWT"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(db: Session, user_id: int, expires_delta: Optional[timedelta] = None) -> str:
    """Criar refresh token e salvar no banco"""
    token = secrets.token_urlsafe(32)
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    # Salva no banco
    db_token = models.RefreshToken(
        usuario_id=user_id,
        token=token,
        expires_at=expire
    )
    db.add(db_token)
    db.commit()
    
    return token

def revoke_refresh_token(db: Session, token: str) -> bool:
    """Revogar refresh token"""
    db_token = db.query(models.RefreshToken).filter(
        models.RefreshToken.token == token
    ).first()
    
    if db_token:
        db_token.revoked = True
        db.commit()
        return True
    return False

# =============== AUTENTICAÇÃO ===============

def authenticate_user(db: Session, username: str, password: str):
    """Autenticar usuário (login)"""
    user = db.query(models.Usuario).filter(
        models.Usuario.username == username
    ).first()
    
    if not user or not user.ativo:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user

def get_current_user_from_token(token: str, db: Session):
    """Validar token e retornar usuário"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            return None
        
        user = db.query(models.Usuario).filter(
            models.Usuario.username == username
        ).first()
        
        return user
    except jwt.JWTError:
        return None