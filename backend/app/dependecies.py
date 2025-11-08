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
    """
    Esta função é o 'Guarda-Costas'. Ela:
    1. Tenta pegar o token do cabeçalho 'Authorization'.
    2. Tenta decodificar o token usando nossa SECRET_KEY.
    3. Se conseguir, extrai o username (sub).
    4. Busca o usuário no banco de dados.
    5. Se tudo der certo, retorna o objeto usuário.
    Se algo der errado em qualquer passo, ela chuta a pessoa (Erro 401).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Tenta decodificar o token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
        
    # Busca o usuário no banco
    user = crud.get_usuario_por_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
        
    return user