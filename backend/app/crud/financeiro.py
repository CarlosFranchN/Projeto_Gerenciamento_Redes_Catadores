from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas
from typing import Optional

def get_saldo(db: Session) -> schemas.SaldoResponse:
    """Calcula o saldo atual, total de entradas e total de saídas."""
    
    total_entradas = db.query(func.sum(models.TransacaoFinanceira.valor))\
                       .filter(models.TransacaoFinanceira.tipo == models.TipoTransacaoEnum.ENTRADA)\
                       .scalar() or 0.0
    
    total_saidas = db.query(func.sum(models.TransacaoFinanceira.valor))\
                     .filter(models.TransacaoFinanceira.tipo == models.TipoTransacaoEnum.SAIDA)\
                     .scalar() or 0.0
    
    saldo = total_entradas - total_saidas
    
    return schemas.SaldoResponse(
        saldo_atual=saldo,
        total_entradas=total_entradas,
        total_saidas=total_saidas
    )

def create_transacao(db: Session, transacao: schemas.TransacaoCreate) -> models.TransacaoFinanceira:
    """Cria uma nova transação financeira (Entrada ou Saída)."""
    db_transacao = models.TransacaoFinanceira(**transacao.dict())
    db.add(db_transacao)
    db.commit()
    db.refresh(db_transacao)
    return db_transacao

def get_transacoes(db: Session, skip: int = 0, limit: int = 20) -> dict:
    """Retorna uma lista paginada do histórico de transações."""
    query = db.query(models.TransacaoFinanceira)
    total_count = query.count()
    items = query.order_by(models.TransacaoFinanceira.data.desc())\
                 .offset(skip).limit(limit).all()
    
    return {"total_count": total_count, "items": items}