from fastapi import APIRouter, Depends,HTTPException, status,Body
from sqlalchemy.orm import Session
from typing import List

from app import crud, models,schemas
from app.database import get_db


router = APIRouter(
    prefix="/materiais",
    tags=["materiais"]  
)


@router.post("/",response_model=schemas.Material, summary="Registra um novo material")
def create_material(
    material: schemas.MaterialCreate,
    db : Session = Depends(get_db)):
    db_material = db.query(models.Material).filter(models.Material.nome == material.nome).first()
    
    if db_material:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Material já cadastrado")
    return crud.create_material(db=db, material=material)

@router.get("/", response_model=List[schemas.Material], summary="Lista todos os materiais")
def read_all_materiais(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)):
    materiais = crud.get_all_material(db, skip=skip, limit=limit)
    return materiais

@router.get("/id_material/{id_material}", response_model=schemas.Material, summary="Consulta um material pelo ID")
def read_material(
    id_material: int,
    db: Session = Depends(get_db)
):
    db_material = crud.get_mateiral(
        db,
        id_material=id_material)
    if db_material is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material não encontrado")
    return db_material

@router.get("/nome/{nome_material}", response_model=schemas.Material, summary="Consulta um material pelo nome")
def read_material_nome(
    nome_material:str,
    db: Session = Depends(get_db)):
    db_material = db.query(models.Material).filter(models.Material.nome.ilike(f"%{nome_material}%")).all()
    if db_material is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material não encontrado")
    return db_material

@router.put(
    "/{material_id}", 
    response_model=schemas.Material, 
    summary="Atualiza um material existente"
)
def update_material_endpoint(
    material_id: int, 
    material_update: schemas.MaterialUpdate, # Recebe os novos dados no corpo da requisição 
    db: Session = Depends(get_db)
):
    
    
    updated_material = crud.update_material(db=db, material_id=material_id, material_update=material_update)

    if updated_material is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material não encontrado")

    return updated_material

