# app/routers/vendas.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/vendas",
    tags=["Vendas"]
)

@router.post("/", response_model=schemas.Venda)
def create_venda(venda: schemas.VendaCreate, db: Session = Depends(get_db)):
    # A lógica complexa de transação está escondida no crud.create_venda
    # O router apenas orquestra a chamada.
    return crud.create_venda(db=db, venda=venda)

@router.get("/", response_model=List[schemas.Venda])
def read_vendas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vendas = crud.get_vendas(db, skip=skip, limit=limit)
    return vendas

@router.get("/{venda_id}", response_model=schemas.Venda)
def read_venda(venda_id: int, db: Session = Depends(get_db)):
    db_venda = crud.get_venda(db, venda_id=venda_id)
    if db_venda is None:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return db_venda