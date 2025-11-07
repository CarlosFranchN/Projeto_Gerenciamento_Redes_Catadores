from sqlalchemy.orm import Session
from .. import models, schemas
from typing import List, Optional

def get_comprador(db: Session, comprador_id: int):
    return db.query(models.Comprador).filter(models.Comprador.id == comprador_id).first()

def get_comprador_by_nome(db: Session, nome: str):
    return db.query(models.Comprador).filter(models.Comprador.nome == nome).first()

def get_compradores(db: Session, skip: int = 0, limit: int = 100) -> List[models.Comprador]:

    query = (
        db.query(models.Comprador)
        .filter(models.Comprador.ativo == True)
    )


    total_count = query.count()


    items = (
        query
        .order_by(models.Comprador.nome) 
        .offset(skip)
        .limit(limit)
        .all()
    )
    return {"total_count": total_count, "items": items}


def get_all_compradores(db: Session, skip: int = 0, limit: int = 100) -> dict:
    query = db.query(models.Comprador).filter(models.Comprador.ativo == True)
    
    total_count = query.count()
    
    items = (
        query
        .order_by(models.Comprador.nome)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return {"total_count": total_count, "items": items}
def create_comprador(db: Session, comprador: schemas.CompradorCreate):
    db_comprador = models.Comprador(**comprador.dict())
    db.add(db_comprador)
    db.commit()
    db.refresh(db_comprador)
    return db_comprador

def update_comprador(db: Session, comprador_id: int, comprador_update: schemas.CompradorUpdate):
    db_comprador = get_comprador(db, comprador_id=comprador_id)
    if not db_comprador:
        return None

    update_data = comprador_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_comprador, key, value)

    db.commit()
    db.refresh(db_comprador)
    return db_comprador

def delete_comprador(db: Session, comprador_id: int): 
    db_comprador = get_comprador(db, comprador_id=comprador_id)
    if not db_comprador:
        return None

    db_comprador.ativo = False 
    db.commit()
    db.refresh(db_comprador)
    return db_comprador