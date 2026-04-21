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
    current_user: models.Usuario = Depends(get_current_user)
):
    """Criar nova associação - versão robusta"""
    
    # =============== PASSO 1: Garantir parceiro_id ===============
    if associacao.nome and associacao.parceiro_id is None:
        nome_limpo = associacao.nome.strip().lower()
        
        # 🔍 Busca EXATA (case-insensitive via Python, não SQL)
        todos_parceiros = db.query(models.Parceiro).all()
        parceiro = next(
            (p for p in todos_parceiros if p.nome.strip().lower() == nome_limpo),
            None
        )
        
        if not parceiro:
            # ➕ Cria novo parceiro
            tipo_assoc = db.query(models.TipoParceiro).filter(
                models.TipoParceiro.nome == "ASSOCIACAO"
            ).first()
            
            if not tipo_assoc:
                tipo_assoc = models.TipoParceiro(nome="ASSOCIACAO")
                db.add(tipo_assoc)
                db.flush()
            
            parceiro = models.Parceiro(
                nome=associacao.nome.strip(),  # Mantém case original para exibição
                id_tipo_parceiro=tipo_assoc.id
            )
            db.add(parceiro)
            db.flush()
        
        associacao.parceiro_id = parceiro.id
    
    # =============== PASSO 2: Criar associação ===============
    try:
        nova_associacao = crud.create_associacao(db=db, associacao=associacao)
        db.refresh(nova_associacao)
        return nova_associacao
        
    except IntegrityError as e:
        db.rollback()
        
        # 🔄 Race condition: tenta re-fetch e retry uma vez
        if "ix_parceiros_nome" in str(e) and associacao.nome:
            nome_limpo = associacao.nome.strip().lower()
            parceiro = next(
                (p for p in db.query(models.Parceiro).all() 
                 if p.nome.strip().lower() == nome_limpo),
                None
            )
            if parceiro:
                associacao.parceiro_id = parceiro.id
                try:
                    nova_associacao = crud.create_associacao(db=db, associacao=associacao)
                    db.refresh(nova_associacao)
                    return nova_associacao
                except IntegrityError:
                    pass  # Cai para o erro de CNPJ abaixo
        
        if "cnpj" in str(e).lower() or "ix_associacoes_cnpj" in str(e):
            raise HTTPException(status_code=400, detail="CNPJ já cadastrado")
        
        raise HTTPException(status_code=400, detail=f"Erro: {str(e)}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ ERRO: {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

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