from sqlalchemy.orm import Session
from app.models import ProducaoImpacto
from app.schemas.schema_producao import ProducaoImpactoCreate, ProducaoImpactoUpdate
from typing import List, Optional
import math

def get_producoes(db: Session, skip: int = 0, limit: int = 100) -> dict:
    """Busca todas as produções (Ideal para o painel geral) com paginação"""
    query = db.query(ProducaoImpacto)
    
    total_count = query.count()
    items = query.order_by(ProducaoImpacto.ano.desc(), ProducaoImpacto.mes.desc()).offset(skip).limit(limit).all()
    
    # 🧮 Matemática da Paginação
    page = (skip // limit) + 1 if limit > 0 else 1
    pages = math.ceil(total_count / limit) if limit > 0 else 1

    return {
        "total": total_count,
        "page": page,
        "page_size": limit,
        "pages": pages,
        "items": items
    }

def get_producoes_by_associacao(db: Session, associacao_id: int, skip: int = 0, limit: int = 100) -> dict:
    """Busca a produção de uma associação específica com paginação"""
    query = db.query(ProducaoImpacto).filter(ProducaoImpacto.associacao_id == associacao_id)
    
    total_count = query.count()
    items = query.order_by(ProducaoImpacto.ano.desc(), ProducaoImpacto.mes.desc()).offset(skip).limit(limit).all()
    
    # 🧮 Matemática da Paginação
    page = (skip // limit) + 1 if limit > 0 else 1
    pages = math.ceil(total_count / limit) if limit > 0 else 1

    return {
        "total": total_count,
        "page": page,
        "page_size": limit,
        "pages": pages,
        "items": items
    }

def create_producao(db: Session, producao: ProducaoImpactoCreate) -> ProducaoImpacto:
    """Registra um novo impacto mensal"""
    db_producao = ProducaoImpacto(**producao.model_dump())
    db.add(db_producao)
    db.commit()
    db.refresh(db_producao)
    return db_producao

def update_producao(db: Session, producao_id: int, producao_update: ProducaoImpactoUpdate) -> Optional[ProducaoImpacto]:
    """Atualiza um registro (ex: digitou o peso errado)"""
    db_producao = db.query(ProducaoImpacto).filter(ProducaoImpacto.id == producao_id).first()
    if not db_producao:
        return None
    
    # exclude_unset=True garante que só vamos atualizar os campos que foram enviados
    update_data = producao_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_producao, key, value)
    
    db.commit()
    db.refresh(db_producao)
    return db_producao

def delete_producao(db: Session, producao_id: int) -> bool:
    """Apaga um registro de produção"""
    db_producao = db.query(ProducaoImpacto).filter(ProducaoImpacto.id == producao_id).first()
    if not db_producao:
        return False
    
    db.delete(db_producao)
    db.commit()
    return True