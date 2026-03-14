from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app import models, schemas, crud
from app.dependencies import get_current_user

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
    
    # Se não passar associacao_id, usa a "Rede de Catadores"
    if not associacao_id:
        rede = db.query(models.Associacao).filter(
            models.Associacao.cnpj == "09.000.185/0001-09"
        ).first()
        if rede:
            associacao_id = rede.id
    
    # ✅ Retorna os objetos do modelo direto (Pydantic serializa)
    return crud.get_producao_by_ano(db, ano=ano, associacao_id=associacao_id)


@router.get("/total/{ano}", response_model=dict)
def read_total_producao(
    ano: int,
    db: Session = Depends(get_db)
):
    """Obter total de produção por ano (público)"""
    from sqlalchemy import func
    
    total = db.query(
        func.sum(models.ProducaoMensal.kg)
    ).filter(
        models.ProducaoMensal.ano == ano
    ).scalar()
    
    return {"ano": ano, "total_kg": float(total) if total else 0.0}


@router.post("/", response_model=schemas.ProducaoResponse, status_code=status.HTTP_201_CREATED)
def create_producao(
    producao: schemas.ProducaoCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Criar novo registro de produção (requer autenticação)"""
    return crud.create_producao(db, producao=producao)