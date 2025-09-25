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

@router.get("/", response_model=List[schemas.Comprador])
def read_compradores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    compradores = crud.get_compradores(db, skip=skip, limit=limit)
    return compradores