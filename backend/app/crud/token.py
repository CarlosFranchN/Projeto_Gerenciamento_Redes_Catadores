from sqlalchemy.orm import Session
from app.models import RefreshToken
from datetime import datetime
from typing import Optional

def create_refresh_token(
    db: Session,
    usuario_id: int,
    token: str,
    expires_at: datetime
) -> RefreshToken:
    """Criar novo refresh token"""
    db_token = RefreshToken(
        usuario_id=usuario_id,
        token=token,
        expires_at=expires_at
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def get_refresh_token(
    db: Session,
    token: str
) -> Optional[RefreshToken]:
    """Buscar refresh token por valor"""
    return db.query(RefreshToken).filter(
        RefreshToken.token == token,
        RefreshToken.revoked == False,
        RefreshToken.expires_at > datetime.utcnow()
    ).first()

def revoke_refresh_token(
    db: Session,
    token: str
) -> bool:
    """Revogar refresh token"""
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == token
    ).first()
    if not db_token:
        return False
    
    db_token.revoked = True
    db.commit()
    return True

def revoke_all_user_tokens(
    db: Session,
    usuario_id: int
) -> int:
    """Revogar todos os tokens de um usuário"""
    affected = db.query(RefreshToken).filter(
        RefreshToken.usuario_id == usuario_id,
        RefreshToken.revoked == False
    ).update({"revoked": True})
    db.commit()
    return affected