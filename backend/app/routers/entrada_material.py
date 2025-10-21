# app/routers/entradas_material.py
from fastapi import APIRouter, Depends,status, HTTPException,Response
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
    material = crud.get_material(db, id_material=entrada.id_material)
    if not material:
        raise HTTPException(status_code=404, detail=f"Material com id {entrada.id_material} não encontrado.")
    
    associacao = crud.get_associacao(db, id_associacao=entrada.id_associacao)
    if not associacao:
        raise HTTPException(status_code=404, detail=f"Associação com id {entrada.id_associacao} não encontrada.")

    return crud.create_entrada_material(db=db, entrada=entrada)

@router.get("/", response_model=List[schemas.EntradaMaterial])
def read_entradas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    entradas = crud.get_entradas_material(db, skip=skip, limit=limit)
    return entradas

@router.delete(
    "/{entrada_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary="Cancela uma entrada de material (Soft Delete)"
)
def cancel_entrada_material_endpoint(
    entrada_id: int, 
    db: Session = Depends(get_db)
):
    """
    Marca uma entrada de material específica como 'Cancelada'.
    O registro não é excluído e o estoque será recalculado.
    """
    cancelled_entrada = crud.cancel_entrada_material(db=db, entrada_id=entrada_id)

    if cancelled_entrada is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entrada de material não encontrada")

    return Response(status_code=status.HTTP_204_NO_CONTENT)