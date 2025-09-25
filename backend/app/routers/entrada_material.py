# app/routers/entradas_material.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db


router = APIRouter(
    prefix="/entradas_material",
    tags=["Entradas de Material"]
)

@router.post("/", response_model=schemas.EntradaMaterial)
def create_entrada_material(entrada: schemas.EntradaMaterialCreate, db: Session = Depends(get_db)):
    # Validação extra: verificar se o material e a associação existem antes de criar a entrada
    material = crud.get_material(db, material_id=entrada.id_material)
    if not material:
        raise HTTPException(status_code=404, detail=f"Material com id {entrada.id_material} não encontrado.")
    
    associacao = crud.get_associacao(db, associacao_id=entrada.id_associacao)
    if not associacao:
        raise HTTPException(status_code=404, detail=f"Associação com id {entrada.id_associacao} não encontrada.")

    return crud.create_entrada_material(db=db, entrada=entrada)

@router.get("/", response_model=List[schemas.EntradaMaterial])
def read_entradas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    entradas = crud.get_entradas_material(db, skip=skip, limit=limit)
    return entradas