# app/routers/entrada_material.py
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from .. import crud, schemas # Importa os módulos __init__
from ..database import get_db

router = APIRouter(
    prefix="/entradas", # Prefixo corrigido (sem _material)
    tags=["Entradas de Material"]
)

@router.post("/", response_model=schemas.EntradaMaterial)
def create_entrada_material(entrada: schemas.EntradaMaterialCreate, db: Session = Depends(get_db)):
    
    # Validação: O Doador existe?
    doador = crud.get_doador(db, doador_id=entrada.id_doador)
    if not doador:
        raise HTTPException(status_code=404, detail=f"Doador com id {entrada.id_doador} não encontrado.")
        
    # Validação: O Material existe?
    material = crud.get_material(db, id_material=entrada.id_material)
    if not material:
        raise HTTPException(status_code=404, detail=f"Material com id {entrada.id_material} não encontrado.")
    
    return crud.create_entrada_material(db=db, entrada=entrada)

@router.get("/", response_model=schemas.EntradasPaginadasResponse) # 👈 CORRIGIDO para paginação
def read_entradas(
    skip: int = 0, 
    limit: int = 100, 
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    id_doador: Optional[int] = None, # 👈 CORRIGIDO
    id_material: Optional[int] = None,
    db: Session = Depends(get_db)
):
    entradas_paginadas = crud.get_entradas_material(
        db=db, skip=skip, limit=limit, 
        data_inicio=data_inicio, data_fim=data_fim, 
        id_doador=id_doador, # 👈 CORRIGIDO
        id_material=id_material
    )
    return entradas_paginadas

@router.delete(
    "/{entrada_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary="Cancela uma entrada de material (Soft Delete)"
)
def cancel_entrada_material_endpoint(
    entrada_id: int, 
    db: Session = Depends(get_db)
):
    cancelled_entrada = crud.cancel_entrada_material(db=db, entrada_id=entrada_id)
    
    if cancelled_entrada is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entrada de material não encontrada")
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)