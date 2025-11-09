# app/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from .core.config import settings
from .core import security
from . import crud, models, schemas
from .database import get_db

# Define de onde o FastAPI deve tentar tirar o token (da rota "/token" que criamos)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> models.Usuario:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        print(f"DEBUG: Tentando validar token: {token[:20]}...")
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            print("DEBUG: Token sem username (sub)")
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError as e:
        print(f"DEBUG: Erro na decodificação JWT: {e}")
        raise credentials_exception
        
    user = crud.get_usuario_por_username(db, username=token_data.username)
    if user is None:
        print(f"DEBUG: Usuário '{token_data.username}' não encontrado no banco")
        raise credentials_exception
        
    return user