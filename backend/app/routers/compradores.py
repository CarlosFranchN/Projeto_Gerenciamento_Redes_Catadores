# app/routers/compradores.py
from fastapi import APIRouter, Depends, HTTPException,status, Response
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import SessionLocal
from ..dependencies import get_current_user
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix="/compradores",
    tags=["Compradores"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=schemas.Comprador)
def create_comprador(comprador: schemas.CompradorCreate, db: Session = Depends(get_db)):
    if crud.get_comprador_by_nome(db, nome=comprador.nome):
        raise HTTPException(status_code=409, detail="Comprador já existe.")
    return crud.create_comprador(db=db, comprador=comprador)

@router.get("/", response_model=schemas.CompradoresPaginadosResponse) 
def read_compradores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_compradores(db, skip=skip, limit=limit)

@router.get("/{comprador_id}", response_model=schemas.Comprador)
def read_comprador(comprador_id: int, db: Session = Depends(get_db)):
    db_comprador = crud.get_comprador(db, comprador_id=comprador_id) 
    if db_comprador is None:
        raise HTTPException(status_code=404, detail="Comprador não encontrado")
    return db_comprador

@router.put("/{comprador_id}", response_model=schemas.Comprador)
def update_comprador(comprador_id : int , comprador_update : schemas.CompradorUpdate, db: Session = Depends(get_db)):
    db_comp = crud.update_associacao(db, comprador_id,comprador_update)
    if not db_comp: raise HTTPException(status_code=404, detail="Comprador não encontrado")
    
    return db_comp

@router.delete("/{comprador_id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_comprador(comprador_id: int, db: Session = Depends(get_db)):
    db_comp = crud.delete_comprador(db, comprador_id)
    if not db_comp: raise HTTPException(status_code=404, detail="Comprador não encontrado")
    return Response(status_code=status.HTTP_204_NO_CONTENT)