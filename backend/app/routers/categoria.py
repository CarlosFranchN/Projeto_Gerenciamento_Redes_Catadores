# app/routers/categorias.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, models
from ..database import get_db
from ..dependencies import get_current_user 

router = APIRouter(
    prefix="/categorias",
    tags=["Categorias de Resíduo"],
    dependencies=[Depends(get_current_user)] 
)

@router.post("/", response_model=schemas.Categoria, status_code=status.HTTP_201_CREATED)
def create_categoria(
    categoria: schemas.CategoriaCreate, 
    db: Session = Depends(get_db)
):
    """Cria uma nova categoria de resíduo."""
    db_categoria = crud.get_categoria_by_nome(db, nome=categoria.nome)
    if db_categoria:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Categoria '{categoria.nome}' já existe."
        )
    return crud.create_categoria(db=db, categoria=categoria)

@router.get("/", response_model=List[schemas.Categoria])
def read_all_categorias(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Lista todas as categorias cadastradas."""
    return crud.get_all_categorias(db, skip=skip, limit=limit)