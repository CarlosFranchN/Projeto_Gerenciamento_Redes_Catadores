from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import crud, schemas
from ..database import get_db
from datetime import date

router = APIRouter(
    prefix="/vendas",
    tags=["Vendas"]
)

@router.post("/", response_model=schemas.Venda, status_code=status.HTTP_201_CREATED)
def create_venda_endpoint(venda: schemas.VendaCreate, db: Session = Depends(get_db)):
    try:
        nova_venda = crud.create_venda(db=db, venda=venda)
        return nova_venda
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Erro inesperado ao criar venda: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocorreu um erro interno.")

@router.get("/", response_model=schemas.VendasPaginadasResponse, summary="Lista todas as vendas registradas")
def read_vendas(
    skip: int = 0, 
    limit: int = 100, 
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    comprador: Optional[str] = None,
    id_material: Optional[int] = None,
    db: Session = Depends(get_db)
):
    vendas_paginadas = crud.get_vendas(
        db=db, skip=skip, limit=limit, 
        data_inicio=data_inicio, data_fim=data_fim, 
        comprador=comprador, id_material=id_material
    )
    return vendas_paginadas

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