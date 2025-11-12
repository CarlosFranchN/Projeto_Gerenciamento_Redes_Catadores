from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from .. import crud, schemas
from ..database import get_db
from ..dependencies import get_current_user
router = APIRouter(
    prefix="/compras",
    tags=["Compras (Com Custo)"],
    dependencies=[Depends(get_current_user)]
    )

@router.post("/", response_model=schemas.Compra, status_code=status.HTTP_201_CREATED)
def create_compra(compra: schemas.CompraCreate, db: Session = Depends(get_db)):
    if not crud.get_parceiro(db, parceiro_id=compra.id_parceiro):
         raise HTTPException(status_code=404, detail="Fornecedor (Parceiro) não encontrado")
    if not crud.get_material(db, id_material=compra.id_material):
         raise HTTPException(status_code=404, detail="Material não encontrado")
     
    try:
        return crud.create_compra(db=db, compra=compra)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=schemas.ComprasPaginadasResponse)
def read_compras(
    skip: int = 0, limit: int = 100,
    data_inicio: Optional[date] = None, data_fim: Optional[date] = None,
    id_parceiro: Optional[int] = None, id_material: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_compras(db, skip=skip, limit=limit, data_inicio=data_inicio, data_fim=data_fim, id_parceiro=id_parceiro, id_material=id_material)

@router.delete("/{compra_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_compra(compra_id: int, db: Session = Depends(get_db)):
    if not crud.cancel_compra(db, compra_id=compra_id):
        raise HTTPException(status_code=404, detail="Compra não encontrada")
    return Response(status_code=status.HTTP_204_NO_CONTENT)