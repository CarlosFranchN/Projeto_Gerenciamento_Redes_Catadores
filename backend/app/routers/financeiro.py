
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import crud, schemas, models
from ..database import get_db
from ..dependencies import get_current_user 

router = APIRouter(
    prefix="/financeiro",
    tags=["Financeiro (Livro Caixa)"],
    dependencies=[Depends(get_current_user)] 
)

@router.get("/saldo", response_model=schemas.SaldoResponse)
def read_saldo_atual(db: Session = Depends(get_db)):
    return crud.get_saldo(db)

@router.get("/transacoes", response_model=schemas.TransacoesPaginadas)
def read_historico_transacoes(
    skip: int = 0, 
    limit: int = 20, 
    db: Session = Depends(get_db)
):
    """
    Lista o histórico paginado de todas as transações financeiras (entradas e saídas).
    """
    return crud.get_transacoes(db, skip=skip, limit=limit)

@router.post("/transacoes", response_model=schemas.Transacao)
def create_transacao_manual(
    transacao: schemas.TransacaoCreate, 
    db: Session = Depends(get_db)
):
    """
    Registra uma transação manual (Aporte/Retirada).
    Usado para despesas (aluguel, gasolina) ou aportes (verba do projeto).
    """

    if transacao.valor <= 0:
         raise HTTPException(status_code=400, detail="O valor da transação deve ser positivo.")
    

    if transacao.id_compra_associada or transacao.id_venda_associada:
        raise HTTPException(status_code=400, detail="Transações manuais não podem ser associadas a compras ou vendas.")
        
    return crud.create_transacao(db, transacao)