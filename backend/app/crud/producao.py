from sqlalchemy.orm import Session
from app.models import ProducaoMensal
from app.schemas.schema_producao import ProducaoCreate

def get_producao_by_ano(db: Session, ano: int, associacao_id: int = None):
    query = db.query(ProducaoMensal).filter(ProducaoMensal.ano == ano)
    if associacao_id:
        query = query.filter(ProducaoMensal.associacao_id == associacao_id)
    return query.order_by(ProducaoMensal.mes).all()

def create_producao(db: Session, producao: ProducaoCreate):
    db_producao = ProducaoMensal(**producao.dict())
    db.add(db_producao)
    db.commit()
    db.refresh(db_producao)
    return db_producao