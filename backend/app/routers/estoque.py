from fastapi import APIRouter, Depends,HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, models
from app.database import get_db
from .. import schemas
from ..dependecies import get_current_user



router = APIRouter(
    prefix="/estoque",
    tags=["Estoque"],
    dependencies=[Depends(get_current_user)]
)


@router.get(
    "/{id_material}",
    response_model=schemas.EstoqueGeralResponseItem, 
    summary="Consulta o estoque atual de um material específico"
)
def get_estoque_material(id_material: int, db: Session = Depends(get_db)):
    """
    Calcula e retorna a quantidade atual em estoque para um material
    específico identificado pelo seu ID.

    Exemplo de URL: `/estoque/1`
    """
    material = crud.get_material(db, id_material=id_material)
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Material com ID {id_material} não encontrado"
        )

    estoque = crud.calcular_estoque_material(db, material_id=id_material)


    return schemas.EstoqueGeralResponseItem(
        id=material.id, 
        codigo=material.codigo,
        nome=material.nome,
        categoria=material.categoria,
        estoque_atual=estoque,
        unidade_medida=material.unidade_medida
    )
@router.get(
    "/",
    response_model=schemas.EstoquePaginadoResponse,
    summary="Lista todos os materiais com o estoque atual calculado"
)
def get_estoque_geral(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.get_estoque_todos_materiais(db, skip=skip, limit=limit)