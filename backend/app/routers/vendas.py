from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import crud, schemas
from ..database import get_db
from datetime import date
from ..dependecies import get_current_user

router = APIRouter(
    prefix="/vendas",
    tags=["Vendas"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=schemas.Venda, status_code=status.HTTP_201_CREATED)
def create_venda(venda: schemas.VendaCreate, db: Session = Depends(get_db)):
    if not crud.get_comprador(db, comprador_id=venda.id_comprador):
        raise HTTPException(status_code=404, detail="Comprador não encontrado")

    try:
        return crud.create_venda(db=db, venda=venda)
    except ValueError as e: 
        raise HTTPException(status_code=400, detail=str(e))
@router.get("/", response_model=schemas.VendasPaginadasResponse, summary="Lista todas as vendas registradas")
def read_vendas(
    skip: int = 0, limit: int = 100,
    data_inicio: Optional[date] = None, data_fim: Optional[date] = None,
    id_comprador: Optional[int] = None, 
    id_material: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_vendas(
        db=db, skip=skip, limit=limit,
        data_inicio=data_inicio, data_fim=data_fim,
        id_comprador=id_comprador, id_material=id_material
    )

@router.get("/{venda_id}", response_model=schemas.Venda)
def read_venda(venda_id: int, db: Session = Depends(get_db)):
    db_venda = crud.get_venda(db, venda_id=venda_id)
    if not db_venda: raise HTTPException(status_code=404, detail="Venda não encontrada")
    return db_venda

@router.get("/{venda_id}", response_model=schemas.Venda)
def read_venda(venda_id: int, db: Session = Depends(get_db)):
    db_venda = crud.get_venda(db, venda_id=venda_id)
    if db_venda is None:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return db_venda

@router.delete(
    "/{venda_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary="Marca uma venda como não concluída/cancelada (Soft Delete)"
)
def cancel_venda_endpoint(
    venda_id: int, 
    db: Session = Depends(get_db)
):
    cancelled_venda = crud.cancel_venda(db=db, venda_id=venda_id)
    
    if cancelled_venda is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venda não encontrada")
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)