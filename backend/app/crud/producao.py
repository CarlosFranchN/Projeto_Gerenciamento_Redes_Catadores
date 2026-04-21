from sqlalchemy.orm import Session
from app.models import ProducaoImpacto
from app.schemas.schema_producao import ProducaoImpactoCreate, ProducaoImpactoUpdate
from typing import List, Optional

def get_producoes(db: Session, skip: int = 0, limit: int = 100) -> List[ProducaoImpacto]:
    """Busca todas as produções (Ideal para o painel geral)"""
    return db.query(ProducaoImpacto).order_by(ProducaoImpacto.ano.desc(), ProducaoImpacto.mes.desc()).offset(skip).limit(limit).all()

def get_producoes_by_associacao(db: Session, associacao_id: int, skip: int = 0, limit: int = 100) -> List[ProducaoImpacto]:
    """Busca a produção de uma associação específica"""
    return db.query(ProducaoImpacto).filter(ProducaoImpacto.associacao_id == associacao_id).order_by(ProducaoImpacto.ano.desc(), ProducaoImpacto.mes.desc()).offset(skip).limit(limit).all()

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