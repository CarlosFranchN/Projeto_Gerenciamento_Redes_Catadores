from fastapi import APIRouter, Depends,HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, models,schemas
from app.database import get_db



router = APIRouter(
    prefix="/estoque",
    tags=["Estoque"]
)

# Endpoint antigo para estoque de UM material (pode manter)
@router.get(
    "/{id_material}",
    response_model=schemas.EstoqueGeralResponseItem, # Reutiliza o schema
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

    # Monta a resposta usando o schema definido
    return schemas.EstoqueGeralResponseItem(
        id=material.id, # Corrigido para id em vez de material_id
        codigo=material.codigo_material,
        nome=material.nome,
        categoria=material.categoria,
        estoque_atual=estoque,
        unidade_medida=material.unidade_medida
    )
@router.get(
    "/",
    response_model=List[schemas.EstoqueGeralResponseItem],
    summary="Lista todos os materiais com o estoque atual calculado"
)
def get_estoque_geral(db: Session = Depends(get_db)):
    estoque_geral_calculado = crud.get_estoque_todos_materiais(db)

    # Retorna a lista. FastAPI/Pydantic cuidam da validação e serialização.
    return estoque_geral_calculado
