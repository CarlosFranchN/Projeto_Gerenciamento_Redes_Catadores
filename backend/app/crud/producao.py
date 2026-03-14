from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models import ProducaoMensal
from app.schemas.schema_producao import ProducaoCreate, ProducaoUpdate
from typing import List, Optional

def get_producao_by_ano(
    db: Session, 
    ano: int, 
    associacao_id: Optional[int] = None
) -> List[ProducaoMensal]:
    """Buscar produção por ano, opcionalmente filtrando por associação"""
    query = db.query(ProducaoMensal).filter(ProducaoMensal.ano == ano)
    if associacao_id:
        query = query.filter(ProducaoMensal.associacao_id == associacao_id)
    return query.order_by(ProducaoMensal.mes).all()

def get_producao_by_mes(
    db: Session, 
    mes: int, 
    ano: int
) -> Optional[ProducaoMensal]:
    """Buscar produção de um mês específico"""
    return db.query(ProducaoMensal).filter(
        and_(
            ProducaoMensal.mes == mes,
            ProducaoMensal.ano == ano
        )
    ).first()

def create_producao(
    db: Session, 
    producao: ProducaoCreate
) -> ProducaoMensal:
    """Criar novo registro de produção"""
    db_producao = ProducaoMensal(**producao.model_dump())
    db.add(db_producao)
    db.commit()
    db.refresh(db_producao)
    return db_producao

def update_producao(
    db: Session, 
    producao_id: int, 
    producao: ProducaoUpdate
) -> Optional[ProducaoMensal]:
    """Atualizar produção existente"""
    db_producao = db.query(ProducaoMensal).filter(
        ProducaoMensal.id == producao_id
    ).first()
    if not db_producao:
        return None
    
    update_data = producao.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_producao, key, value)
    
    db.commit()
    db.refresh(db_producao)
    return db_producao

def delete_producao(
    db: Session, 
    producao_id: int
) -> bool:
    """Deletar registro de produção"""
    db_producao = db.query(ProducaoMensal).filter(
        ProducaoMensal.id == producao_id
    ).first()
    if not db_producao:
        return False
    
    db.delete(db_producao)
    db.commit()
    return True

def get_total_producao_by_ano(
    db: Session, 
    ano: int
) -> float:
    """Somar toda a produção de um ano"""
    from sqlalchemy import func
    result = db.query(func.sum(ProducaoMensal.kg)).filter(
        ProducaoMensal.ano == ano
    ).scalar()
    return float(result) if result else 0.0