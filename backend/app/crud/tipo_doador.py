from sqlalchemy.orm import Session
from .. import models, schemas
from typing import List

def get_tipo_doador(db: Session, tipo_doador_id: int):
    return db.query(models.TipoDoador).filter(models.TipoDoador.id == tipo_doador_id).first()

def get_tipo_doador_by_nome(db: Session, nome: str):
    return db.query(models.TipoDoador).filter(models.TipoDoador.nome == nome).first()

def get_all_tipos_doador(db: Session, skip: int = 0, limit: int = 100) -> List[models.TipoDoador]:
    return db.query(models.TipoDoador).order_by(models.TipoDoador.nome).offset(skip).limit(limit).all()

def create_tipo_doador(db: Session, tipo_doador: schemas.TipoDoadorCreate):
    db_tipo_doador = models.TipoDoador(nome=tipo_doador.nome)
    db.add(db_tipo_doador)
    db.commit()
    db.refresh(db_tipo_doador)
    return db_tipo_doador