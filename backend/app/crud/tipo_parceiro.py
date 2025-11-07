from sqlalchemy.orm import Session
from .. import models, schemas
from typing import List

def get_tipo_parceiro_by_nome(db: Session, nome: str):
    """Busca um tipo pelo seu nome exato (ex: 'ASSOCIACAO')."""
    return db.query(models.TipoParceiro).filter(models.TipoParceiro.nome == nome).first()

def get_all_tipos_parceiro(db: Session, skip: int = 0, limit: int = 100) -> List[models.TipoParceiro]:
    """Lista todos os tipos cadastrados."""
    return db.query(models.TipoParceiro).order_by(models.TipoParceiro.nome).offset(skip).limit(limit).all()

