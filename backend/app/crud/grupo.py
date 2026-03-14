from sqlalchemy.orm import Session
from app.models import Grupo
from app.schemas.schema_grupo import GrupoCreate, GrupoUpdate
from typing import List, Optional

def get_all_grupos(db: Session, skip: int = 0, limit: int = 100, ativo: bool = True) -> List[Grupo]:
    query = db.query(Grupo)
    if ativo:
        query = query.filter(Grupo.ativo == True)
    return query.order_by(Grupo.nome).offset(skip).limit(limit).all()

def get_grupo_by_id(db: Session, grupo_id: int) -> Optional[Grupo]:
    return db.query(Grupo).filter(Grupo.id == grupo_id).first()

def create_grupo(db: Session, grupo: GrupoCreate) -> Grupo:
    db_grupo = Grupo(**grupo.model_dump())
    db.add(db_grupo)
    db.commit()
    db.refresh(db_grupo)
    return db_grupo

def update_grupo(db: Session, grupo_id: int, grupo_update: GrupoUpdate) -> Optional[Grupo]:
    db_grupo = get_grupo_by_id(db, grupo_id)
    if not db_grupo:
        return None
    
    update_data = grupo_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_grupo, key, value)
    
    db.commit()
    db.refresh(db_grupo)
    return db_grupo

def delete_grupo(db: Session, grupo_id: int) -> bool:
    db_grupo = get_grupo_by_id(db, grupo_id)
    if not db_grupo:
        return False
    
    db_grupo.ativo = False  # Soft delete
    db.commit()
    return True

def get_grupos_by_associacao(db: Session, associacao_id: int) -> List[Grupo]:
    return db.query(Grupo).filter(
        Grupo.associacao_id == associacao_id,
        Grupo.ativo == True
    ).all()