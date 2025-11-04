from fastapi import APIRouter, Depends, HTTPException,status,Response
from sqlalchemy.orm import Session
from typing import List

# from app import crud, models, schemas
from app import models
from .. import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/associacoes",
    tags=["associacoes"]
)


@router.post("/", response_model=schemas.Associacao)
def create_associacao(associacao: schemas.AssociacaoCreate, db: Session = Depends(get_db)):
    """
    Cria uma nova Associação (incluindo o registro Doador pai).
    """
    
    # --- Validação Corrigida ---
    # 1. Verifica se o NOME do Doador já existe (na tabela doadores)
    db_doador = crud.get_doador_by_nome(db, nome=associacao.nome)
    if db_doador:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, # 409 Conflito é mais apropriado
            detail=f"Um doador com o nome '{associacao.nome}' já existe."
        )
        
    # 2. Verifica se o Tipo de Doador existe
    db_tipo_doador = crud.get_tipo_doador(db, tipo_doador_id=associacao.id_tipo_doador)
    if not db_tipo_doador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de Doador com ID {associacao.id_tipo_doador} não encontrado."
        )
    # (Poderíamos adicionar uma verificação se o tipo é "ASSOCIACAO" aqui também)

    # 3. Se tudo estiver OK, chama o CRUD para criar
    try:
        return crud.create_associacao(db=db, associacao=associacao)
    except ValueError as e:
        # Captura outros erros de integridade (como CNPJ duplicado, se houver)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Erro inesperado ao criar associação: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno ao criar associação.")

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