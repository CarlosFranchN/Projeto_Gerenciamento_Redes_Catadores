from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db
from ..dependecies import get_current_user

router = APIRouter(
    prefix="/tipos_parceiro", 
    tags=["Tipos de Parceiro"],
    dependencies=[Depends(get_current_user)]
)
@router.get("/", response_model=List[schemas.TipoParceiro])
def read_all_tipos_parceiro(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_tipos_parceiro(db, skip=skip, limit=limit)