from fastapi import APIRouter, Depends, HTTPException,status,Response
from sqlalchemy.orm import Session
from typing import List

from app import crud, models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/associacoes",
    tags=["associacoes"]
)


@router.post("/", response_model=schemas.Associacao, summary="Registra uma nova associação")
def create_associacao(
    associacao: schemas.AssociacaoCreate,
    db: Session = Depends(get_db)):
    # db_associacao = crud.create_associacao(db=db, associacao=associacao)
    db_associacao = db.query(models.Associacao).filter(models.Associacao.nome == associacao.nome).first()
    if db_associacao:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Associação já cadastrada")
    return crud.create_associacao(db=db, associacao=associacao)

@router.get("/",response_model=List[schemas.Associacao], summary="Lista todas as associações")
def read_all_associacoes(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)):
    associacoes = crud.get_all_associacoes(db, skip=skip, limit=limit)
    return associacoes

@router.get("/{id_associacao}", response_model=schemas.Associacao, summary="Consulta uma associação pelo ID")
def read_associacao(
    id_associacao: int,
    db: Session = Depends(get_db)
):
    db_associacao = crud.get_associacao(
        db,
        id_associacao=id_associacao)
    if db_associacao is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associação não encontrada")
    return db_associacao

@router.put(
    "/{associacao_id}",
    response_model=schemas.Associacao,
    summary="Atualiza uma associação existente"
)
def update_associacao_endpoint(
    associacao_id: int,
    associacao_update: schemas.AssociacaoUpdate, # Dados vêm no corpo
    db: Session = Depends(get_db)
):
    """
    Atualiza os dados de uma associação específica (identificada pelo ID).
    Envie o objeto completo com as novas informações no corpo da requisição.
    """
    updated_associacao = crud.update_associacao(
        db=db,
        associacao_id=associacao_id,
        associacao_update=associacao_update
    )

    if updated_associacao is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associação não encontrada"
        )

    return updated_associacao


@router.delete(
    "/{associacao_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary="Marca uma associação como inativa (Soft Delete)"
)
def delete_associacao_endpoint(
    associacao_id: int, 
    db: Session = Depends(get_db)
):
    """
    Marca uma associação específica como inativa. 
    O registro não é excluído permanentemente. 
    Associações inativas não aparecerão nas listagens padrão.
    """
    deleted_associacao = crud.delete_associacao(db=db, associacao_id=associacao_id)

    if deleted_associacao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associação não encontrada")

    # Retorna resposta sem conteúdo para indicar sucesso na deleção (inativação)
    return Response(status_code=status.HTTP_204_NO_CONTENT)