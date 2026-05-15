from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from app import models
from .. import crud, schemas
from app.database import get_db
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/api/associacoes",
    tags=["Associações"]
)

@router.post("/", response_model=schemas.AssociacaoResponse, status_code=status.HTTP_201_CREATED)
def create_associacao(
    associacao: schemas.AssociacaoCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user) # Descomente se quiser exigir login
):
    """Criar nova associação - versão limpa e alinhada com o models.py atual"""
    
    try:
        # Apenas passamos os dados direto para o CRUD
        nova_associacao = crud.create_associacao(db=db, associacao=associacao)
        return nova_associacao
        
    except ValueError as e:
        # 1. Captura o aviso limpo que veio do nosso CRUD (sobre Nome ou CNPJ)
        # e transforma no Erro 400 para o React ler.
        raise HTTPException(status_code=400, detail=str(e))
        
    except Exception as e:
        # 2. Se for qualquer outro erro bizarro, dá erro 500
        db.rollback()
        print(f"❌ ERRO: {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")
    
@router.get("/", response_model=schemas.AssociacoesPaginadasResponse)
def read_all_associacoes(
    skip: int = 0,
    limit: int = 100,
    ativo: Optional[bool] = True,
    db: Session = Depends(get_db)
):
    """Listar todas associações (público)"""
    return crud.get_all_associacoes(db, skip=skip, limit=limit, ativo=ativo)

@router.get("/ativas", response_model=List[schemas.AssociacaoResponse])
def read_associacoes_ativas(db: Session = Depends(get_db)):
    """Listar apenas associações ativas (para o frontend público)"""
    return crud.get_associacoes_ativas(db)

@router.get("/{associacao_id}", response_model=schemas.AssociacaoResponse)
def read_associacao(
    associacao_id: int,
    db: Session = Depends(get_db)
):
    """Consultar uma associação pelo ID"""
    db_assoc = crud.get_associacao(db, associacao_id=associacao_id)
    if not db_assoc:
        raise HTTPException(status_code=404, detail="Associação não encontrada")
    return db_assoc

@router.put("/{associacao_id}", response_model=schemas.AssociacaoResponse)
def update_associacao(
    associacao_id: int,
    associacao_update: schemas.AssociacaoUpdate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Atualizar associação (requer autenticação)"""
    db_assoc = crud.update_associacao(
        db,
        associacao_id=associacao_id,
        associacao_update=associacao_update
    )
    if not db_assoc:
        raise HTTPException(status_code=404, detail="Associação não encontrada")
    return db_assoc

@router.delete("/{associacao_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_associacao(
    associacao_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Soft delete - marca como inativa (requer autenticação)"""
    db_assoc = crud.delete_associacao(db, associacao_id=associacao_id)
    if not db_assoc:
        raise HTTPException(status_code=404, detail="Associação não encontrada")
    return Response(status_code=status.HTTP_204_NO_CONTENT)