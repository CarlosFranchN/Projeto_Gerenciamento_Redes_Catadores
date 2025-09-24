from sqlalchemy.orm import Session
from app import models, schemas
# from app.database import SessionLocal


def get_associacao(db: Session, id_associacao: int):
    query = db.query(models.Associacao).filter(models.Associacao.id == id_associacao).first()
    return query

def get_all_associacoes(db: Session, skip: int = 0 , limit: int = 100):
    query = db.query(models.Associacao).offset(skip).limit(limit).all()
    return query

def create_associacao(db: Session, associacao: schemas.AssociacaoCreate):
    db_associacao = models.Associacao(
        nome = associacao.nome,
        lider = associacao.lider,
        telefone = associacao.telefone,
        cnpj = associacao.cnpj
    )
    db.add(db_associacao)
    db.commit()
    db.refresh(db_associacao)
    return db_associacao

