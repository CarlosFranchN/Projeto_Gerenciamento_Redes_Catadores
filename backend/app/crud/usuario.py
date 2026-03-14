from sqlalchemy.orm import Session
from .. import models, schemas
from ..core.security import get_password_hash
from typing import Optional

def get_usuario_por_username(db: Session, username: str):
    """Buscar usuário por username"""
    query = db.query(models.Usuario).filter(
        models.Usuario.username == username
    ).first()
    return query

def get_usuario_by_id(db: Session, usuario_id: int):
    """Buscar usuário por ID"""
    return db.query(models.Usuario).filter(
        models.Usuario.id == usuario_id
    ).first()

def get_all_usuarios(db: Session, skip: int = 0, limit: int = 100):
    """Listar todos usuários com paginação"""
    return (
        db.query(models.Usuario)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_user(db: Session, user: schemas.UsuarioCreate):
    """Criar novo usuário"""
    hashed_password = get_password_hash(user.password) 
    
    db_user = models.Usuario(
        username=user.username,
        hashed_password=hashed_password,
        nome=user.nome,  # ✅ NOVO
        role=user.role,  # ✅ NOVO (default: "admin" no schema)
        ativo=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, usuario_id: int, user_update: schemas.UsuarioUpdate) -> Optional[models.Usuario]:
    """Atualizar usuário existente"""
    db_user = get_usuario_by_id(db, usuario_id)
    if not db_user:
        return None
    
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Se tiver senha nova, faz hash
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, usuario_id: int) -> bool:
    """Soft delete - marca como inativo"""
    db_user = get_usuario_by_id(db, usuario_id)
    if not db_user:
        return False
    
    db_user.ativo = False
    db.commit()
    return True

def authenticate_user(db: Session, username: str, password: str):
    """Autenticar usuário (login)"""
    from ..core.security import verify_password
    
    user = get_usuario_por_username(db, username)
    if not user or not user.ativo:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user