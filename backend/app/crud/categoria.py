from sqlalchemy.orm import Session
from .. import models, schemas
from typing import List

def get_categoria(db: Session, categoria_id: int):
    return db.query(models.CategoriaResiduo).filter(models.CategoriaResiduo.id == categoria_id).first()

def get_categoria_by_nome(db: Session, nome: str):
    return db.query(models.CategoriaResiduo).filter(models.CategoriaResiduo.nome == nome).first()

def get_all_categorias(db: Session, skip: int = 0, limit: int = 100) -> List[models.CategoriaResiduo]:
    """Lista todas as categorias cadastradas."""
    return (
        db.query(models.CategoriaResiduo)
        .order_by(models.CategoriaResiduo.nome)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_categoria(db: Session, categoria: schemas.CategoriaCreate):
    db_categoria = models.CategoriaResiduo(nome=categoria.nome)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria