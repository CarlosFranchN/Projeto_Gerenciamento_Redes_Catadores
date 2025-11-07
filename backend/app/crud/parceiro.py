from sqlalchemy.orm import Session, joinedload
from .. import models, schemas
from typing import List


def get_parceiro(db: Session, parceiro_id: int):
    query = db.query(models.Parceiro).options(joinedload(models.Parceiro.tipo_info)).filter(models.Parceiro.id == parceiro_id).first()
    
    return query

def get_parceiro_by_nome(db: Session, nome: str):
    query = db.query(models.Parceiro).filter(models.Parceiro.nome == nome).first()
    return query

def get_all_parceiros(db: Session, skip: int = 0, limit: int = 100) -> dict:
    query = db.query(models.Parceiro)
        
    total_count = query.count()
    
    items = (
        query
        .options(joinedload(models.Parceiro.tipo_info))
        .order_by(models.Parceiro.nome)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return {"total_count": total_count, "items": items}

def create_parceiro_generico(db: Session, parceiro:schemas.ParceiroCreate):
    db_parceiro = models.Parceiro(
        nome=parceiro.nome,
        id_tipo_parceiro=parceiro.id_tipo_parceiro
    )
    db.add(db_parceiro)
    db.commit()
    db.refresh(db_parceiro)
    return db_parceiro

def update_parceiro(db: Session, parceiro_id: int, nome_novo: str):
    
    db_parceiro = get_parceiro(db, parceiro_id=parceiro_id)
    if not db_parceiro:
        return None
    
    db_parceiro.nome = nome_novo
    db.commit()
    db.refresh(db_parceiro)
    return db_parceiro

def delete_parceiro(db: Session, parceiro_id: int):
    db_parceiro = get_parceiro(db, parceiro_id=parceiro_id)
    if not db_parceiro:
        return None
        
    try:
        db.delete(db_parceiro)
        db.commit()
        return True 
    except Exception as e:
        db.rollback()
        print(f"Erro ao excluir parceiro {parceiro_id}: {e}")
        return False 