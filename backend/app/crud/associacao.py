from sqlalchemy.orm import Session,joinedload
from app import models, schemas
from datetime import date
from sqlalchemy import func,and_
from typing import List,Optional
from sqlalchemy.exc import IntegrityError
import time
import random

MAX_RETRIES = 3

def get_associacao(db: Session, id_associacao: int):
    query = db.query(models.Associacao).filter(models.Associacao.id == id_associacao).first()
    return query

def get_all_associacoes(db: Session, skip: int = 0, limit: int = 100):
    """Lista todas as associações ATIVAS com paginação."""
    return (
        db.query(models.Associacao)
        .filter(models.Associacao.ativo == True) # 👈 GARANTA QUE ESTE FILTRO EXISTE
        .offset(skip)
        .limit(limit)
        .all()
    )

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

def update_associacao(db: Session, associacao_id: int, associacao_update: schemas.AssociacaoUpdate):
    """Atualiza os dados de uma associação existente."""

    db_associacao = get_associacao(db, id_associacao=associacao_id)

    if not db_associacao:
        return None

    # Atualiza os campos usando os dados do schema
    update_data = associacao_update.dict(exclude_unset=True) 
    for key, value in update_data.items():
        setattr(db_associacao, key, value) 

    db.commit()
    db.refresh(db_associacao)
    return db_associacao

def delete_associacao(db: Session, associacao_id: int):
    """Marca uma associação como inativa."""
    db_associacao = get_associacao(db, id_associacao=associacao_id)
    if not db_associacao: return None
    if not db_associacao.ativo: return db_associacao # Já inativo

    db_associacao.ativo = False # <--- USE 'ativo' e 'False'
    
    db.commit()
    db.refresh(db_associacao)
    return db_associacao