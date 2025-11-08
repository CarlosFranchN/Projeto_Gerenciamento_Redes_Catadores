from sqlalchemy.orm import Session
from .. import models, schemas
from ..core.security import get_password_hash

def get_usuario_por_username(db: Session, username: str):
    query = db.query(models.Usuario).filter(models.Usuario.username == username).first()
    return query

def create_user(db: Session, user: schemas.UsuarioCreate):
    hashed_password = get_password_hash(user.password) 
    
    db_user = models.Usuario(
        username=user.username,
        hashed_password=hashed_password,
        ativo=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user