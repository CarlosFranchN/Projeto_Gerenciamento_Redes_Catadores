from fastapi import APIRouter, Depends,HTTPException, status,Body, Response
from sqlalchemy.orm import Session
from typing import List, Optional


from .. import crud, schemas,models
from app.database import get_db
from ..dependencies import get_current_user


router = APIRouter(
    prefix="/materiais",
    tags=["materiais"], 
    dependencies=[Depends(get_current_user)]
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
        
    if material.id_categoria:
        if not crud.get_categoria(db, categoria_id=material.id_categoria):
            raise HTTPException(status_code=404, detail=f"Categoria com ID {material.id_categoria} não encontrada.")
    return crud.create_material(db=db, material=material)

@router.get("/", response_model=schemas.EstoquePaginadoResponse, summary="Lista todos os materiais")
def read_all_materiais(
    skip: int = 0,
    limit: int = 100,
    nome: Optional[str] = None, 
    db: Session = Depends(get_db)):
    
    materiais = crud.get_estoque_todos_materiais(db, skip=skip, limit=limit, nome=nome)
    return materiais


@router.get("/id_material/{id_material}", response_model=schemas.Material, summary="Consulta um material pelo ID")
def read_material(
    id_material: int,
    db: Session = Depends(get_db)
):
    db_material = crud.get_material(
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
    db_material = db.query(models.Material).filter(models.Material.nome.ilike(f"%{nome_material}%")).first() 
    
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
    if material_update.id_categoria:
        if not crud.get_categoria(db, categoria_id=material_update.id_categoria):
            raise HTTPException(status_code=404, detail=f"Categoria com ID {material_update.id_categoria} não encontrada.")
            
    db_material = crud.update_material(db, material_id=material_id, material_update=material_update)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material não encontrado")
    return db_material

@router.delete("/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_material_endpoint(
    material_id: int,
    db: Session = Depends(get_db)
):
    db_material = crud.delete_material(db, material_id=material_id)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material não encontrado")

    return Response(status_code=status.HTTP_204_NO_CONTENT)