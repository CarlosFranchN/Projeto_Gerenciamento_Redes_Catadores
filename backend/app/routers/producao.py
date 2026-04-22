from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from app.database import get_db
from app import models, schemas, crud
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/api/producao",
    tags=["Produção"]
)

@router.get("/", response_model=List[schemas.ProducaoImpactoResponse])
def read_producao(
    ano: int = 2024,
    associacao_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Listar produção por ano (público)"""
    

    if not associacao_id:
        rede = db.query(models.Associacao).filter(
            models.Associacao.cnpj == "09.000.185/0001-09"
        ).first()
        if rede:
            associacao_id = rede.id
    

    query = db.query(models.ProducaoImpacto).filter(models.ProducaoImpacto.ano == ano)
    if associacao_id:
        query = query.filter(models.ProducaoImpacto.associacao_id == associacao_id)
        
    return query.order_by(models.ProducaoImpacto.mes.desc()).all()


@router.get("/total/{ano}", response_model=dict)
def read_total_producao(
    ano: int,
    db: Session = Depends(get_db)
):
    """Obter total de produção por ano (público)"""
    from sqlalchemy import func
    

    total = db.query(
        func.sum(models.ProducaoImpacto.peso_kg)
    ).filter(
        models.ProducaoImpacto.ano == ano
    ).scalar()
    
    return {"ano": ano, "total_kg": float(total) if total else 0.0}


@router.post("/", response_model=schemas.ProducaoImpactoResponse, status_code=status.HTTP_201_CREATED)
def create_producao(
    producao: schemas.ProducaoImpactoCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Criar novo registro de produção (requer autenticação)"""
    try:
        return crud.create_producao(db, producao=producao)
    
    except IntegrityError as e:
        db.rollback() 
        

        if "trava_producao_unica" in str(e):
            raise HTTPException(
                status_code=400,
                detail=f"Já existe um registro de {producao.categoria.value} para o mês {producao.mes}/{producao.ano} nesta associação. Tente atualizar o registro existente."
            )
            
        # Para outros erros de banco
        raise HTTPException(
            status_code=400,
            detail="Erro de integridade ao registrar produção. Verifique os dados."
        )