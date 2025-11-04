from sqlalchemy.orm import Session, joinedload
from .. import models, schemas
from typing import List

def get_doador(db: Session, doador_id: int):
    # Busca o doador e já inclui os detalhes do tipo
    return (
        db.query(models.Doador)
        .options(joinedload(models.Doador.tipo_info))
        .filter(models.Doador.id == doador_id)
        .first()
    )

def get_doador_by_nome(db: Session, nome: str):
    return db.query(models.Doador).filter(models.Doador.nome == nome).first()

def get_all_doadores(db: Session, skip: int = 0, limit: int = 100) -> List[models.Doador]:
    # Retorna todos os doadores, com tipo
    return (
        db.query(models.Doador)
        .options(joinedload(models.Doador.tipo_info))
        .order_by(models.Doador.nome)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_doador(db: Session, doador: schemas.DoadorCreate):
    """Cria um Doador 'genérico' (ex: Pessoa Física, Órgão Público)"""
    db_doador = models.Doador(
        nome=doador.nome,
        id_tipo_doador=doador.id_tipo_doador
    )
    db.add(db_doador)
    db.commit()
    db.refresh(db_doador)
    return db_doador