from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db
from ..dependecies import get_current_user

router = APIRouter(
    prefix="/parceiros",
    tags=["Parceiros (Geral)"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/", response_model=schemas.ParceirosPaginadosResponse) # 👈 MUDANÇA AQUI
def read_all_parceiros(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_parceiros(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.Parceiro, status_code=status.HTTP_201_CREATED)
def create_parceiro_generico_endpoint(parceiro: schemas.ParceiroCreate, db: Session = Depends(get_db)):
    """Cria um parceiro genérico (NÃO use para Associações)."""
    # ... (validações de existência de tipo e nome duplicado) ...
    # (Implemente as validações chamando crud.get_tipo_parceiro e crud.get_parceiro_by_nome)
    return crud.create_parceiro_generico(db=db, parceiro=parceiro)

@router.put("/{parceiro_id}", response_model=schemas.Parceiro)
def update_parceiro_endpoint(parceiro_id: int, parceiro_update: schemas.ParceiroCreate, db: Session = Depends(get_db)):
    """Atualiza o nome de um parceiro."""
    updated = crud.update_parceiro(db, parceiro_id, parceiro_update.nome)
    if not updated:
        raise HTTPException(status_code=404, detail="Parceiro não encontrado")
    return updated

@router.delete("/{parceiro_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_parceiro_endpoint(parceiro_id: int, db: Session = Depends(get_db)):
    """Exclui um parceiro SEM histórico."""
    success = crud.delete_parceiro(db, parceiro_id)
    if not success:
         raise HTTPException(status_code=409, detail="Não é possível excluir este parceiro (pode ter histórico ou ser uma associação).")
    return Response(status_code=status.HTTP_204_NO_CONTENT)