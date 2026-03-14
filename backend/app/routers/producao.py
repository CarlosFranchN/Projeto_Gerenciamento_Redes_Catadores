from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app import models
from .. import crud, schemas
from app.database import get_db
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/api/producao",
    tags=["Produção"]
)

@router.get("/", response_model=List[schemas.ProducaoResponse])
def read_producao(
    ano: int = 2024,
    associacao_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Listar produção por ano (público)"""
    return crud.get_producao_by_ano(db, ano=ano, associacao_id=associacao_id)

@router.get("/total/{ano}", response_model=dict)
def read_total_producao(
    ano: int,
    db: Session = Depends(get_db)
):
    """Obter total de produção por ano (público)"""
    total = crud.get_total_producao_by_ano(db, ano=ano)
    return {"ano": ano, "total_kg": total}

@router.post("/", response_model=schemas.ProducaoResponse, status_code=status.HTTP_201_CREATED)
def create_producao(
    producao: schemas.ProducaoCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Criar novo registro de produção (requer autenticação)"""
    # Verifica se já existe produção para este mês/ano/associação
    existing = crud.get_producao_by_mes(db, mes=producao.mes, ano=producao.ano)
    if existing and existing.associacao_id == producao.associacao_id:
        raise HTTPException(
            status_code=409,
            detail="Produção já cadastrada para este mês/ano"
        )
    
    db_producao = crud.create_producao(db, producao=producao)
    
    # Registra no audit log
    crud.create_log(
        db=db,
        acao="CREATE",
        tabela_afetada="producao_mensal",
        registro_id=db_producao.id,
        dados_novos=producao.model_dump(),
        usuario_id=current_user.id
    )
    
    return db_producao

@router.put("/{producao_id}", response_model=schemas.ProducaoResponse)
def update_producao(
    producao_id: int,
    producao_update: schemas.ProducaoUpdate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Atualizar produção (requer autenticação)"""
    db_producao = crud.update_producao(db, producao_id=producao_id, producao=producao_update)
    if not db_producao:
        raise HTTPException(status_code=404, detail="Produção não encontrada")
    return db_producao

@router.delete("/{producao_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_producao(
    producao_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Deletar produção (requer autenticação)"""
    success = crud.delete_producao(db, producao_id=producao_id)
    if not success:
        raise HTTPException(status_code=404, detail="Produção não encontrada")
    return None