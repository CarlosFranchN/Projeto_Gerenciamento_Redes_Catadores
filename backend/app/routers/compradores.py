# app/routers/compradores.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix="/compradores",
    tags=["Compradores"]
)

@router.post("/", response_model=schemas.Comprador)
def create_comprador(comprador: schemas.CompradorCreate, db: Session = Depends(get_db)):
    return crud.create_comprador(db=db, comprador=comprador)

@router.get("/", response_model=schemas.CompradoresPaginadosResponse) 
def read_compradores(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    compradores_paginados = crud.get_compradores(db, skip=skip, limit=limit) 
    return compradores_paginados

@router.get("/{comprador_id}", response_model=schemas.Comprador)
def read_comprador(comprador_id: int, db: Session = Depends(get_db)):
    db_comprador = crud.get_comprador(db, comprador_id=comprador_id) 
    if db_comprador is None:
        raise HTTPException(status_code=404, detail="Comprador não encontrado")
    return db_comprador