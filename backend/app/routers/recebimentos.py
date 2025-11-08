# app/routers/entrada_material.py
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from .. import crud, schemas 
from ..database import get_db
from ..dependecies import get_current_user

router = APIRouter(
    prefix="/entradas", 
    tags=["Recebimentos"],
    dependencies=[Depends(get_current_user)]
)
@router.post("/", response_model=schemas.RecebimentoDoacao, status_code=status.HTTP_201_CREATED)
def create_recebimento(recebimento: schemas.RecebimentoDoacaoCreate, db: Session = Depends(get_db)):
    if not crud.get_parceiro(db, parceiro_id=recebimento.id_parceiro):
        raise HTTPException(status_code=404, detail="Parceiro não encontrado")
    if not crud.get_material(db, id_material=recebimento.id_material):
        raise HTTPException(status_code=404, detail="Material não encontrado")
        
    return crud.create_recebimento(db=db, recebimento=recebimento)

@router.get("/", response_model=schemas.RecebimentosPaginadosResponse)
def read_recebimentos(
    skip: int = 0, limit: int = 100,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    id_parceiro: Optional[int] = None,
    id_material: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_recebimentos(db,
                                 skip=skip,
                                 limit=limit,
                                 data_inicio=data_inicio,
                                 data_fim=data_fim,
                                 id_parceiro=id_parceiro,
                                 id_material=id_material)

@router.delete("/{recebimento_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_recebimento(recebimento_id: int, db: Session = Depends(get_db)):
    if not crud.cancel_recebimento(db, recebimento_id=recebimento_id):
         raise HTTPException(status_code=404, detail="Recebimento não encontrado")
    return Response(status_code=status.HTTP_204_NO_CONTENT)