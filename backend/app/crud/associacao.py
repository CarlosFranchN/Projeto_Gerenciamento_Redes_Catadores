from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_
from typing import List, Optional
from sqlalchemy.exc import IntegrityError
from app import models
from .. import schemas
import math

def get_associacao(db: Session, associacao_id: int):
    """Buscar associação por ID (Nova arquitetura sem Parceiro)"""
    return db.query(models.Associacao).filter(models.Associacao.id == associacao_id).first()

def get_all_associacoes(db: Session, skip: int = 0, limit: int = 100, ativo: bool = True) -> dict:
    """Lista associações com paginação completa exigida pelo Schema."""
    query = db.query(models.Associacao)
    
    if ativo:
        query = query.filter(models.Associacao.ativo == True)

    total_count = query.count()

    items = (
        query
        .order_by(models.Associacao.nome)
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    
    page = (skip // limit) + 1 if limit > 0 else 1
    pages = math.ceil(total_count / limit) if limit > 0 else 1

    return {
        "total": total_count,
        "page": page,
        "page_size": limit,
        "pages": pages,
        "items": items
    }

def get_associacoes_ativas(db: Session) -> List[models.Associacao]:
    """Buscar todas associações ativas (para o frontend público)"""
    return (
        db.query(models.Associacao)
        .filter(models.Associacao.ativo == True)
        .order_by(models.Associacao.nome)
        .all()
    )

def create_associacao(db: Session, associacao: schemas.AssociacaoCreate) -> models.Associacao:
    """Cria uma Associação diretamente (Nova Arquitetura)"""
    
    # Cria o registro direto na tabela Associacao
    db_associacao = models.Associacao(
        nome=associacao.nome,
        cnpj=associacao.cnpj,
        lider=associacao.lider,
        telefone=associacao.telefone,
        endereco=associacao.endereco, # Substituindo logradouro/numero
        bairro=associacao.bairro,
        cidade=associacao.cidade,
        uf=associacao.uf,
        status=associacao.status,
        ativo=associacao.ativo,
        municipio_id=associacao.municipio_id,
        grupo_id=associacao.grupo_id
    )
    
    db.add(db_associacao)

    try:
        db.commit() 
        db.refresh(db_associacao)
        return db_associacao
    except IntegrityError as e:
        db.rollback()
        if "unique constraint" in str(e).lower() and "nome" in str(e).lower():
            raise ValueError(f"Já existe uma associação com o nome '{associacao.nome}'")
        if "unique constraint" in str(e).lower() and "cnpj" in str(e).lower():
            raise ValueError(f"Já existe uma associação com o CNPJ '{associacao.cnpj}'")
        raise e
    except Exception as e:
        db.rollback()
        raise ValueError(f"Erro ao salvar associação: {e}") from e

def update_associacao(db: Session, associacao_id: int, associacao_update: schemas.AssociacaoUpdate) -> Optional[models.Associacao]:
    """Atualiza uma associação diretamente."""
    db_associacao = get_associacao(db, associacao_id=associacao_id)
    if not db_associacao:
        return None

    update_data = associacao_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if hasattr(db_associacao, key):
            setattr(db_associacao, key, value)
    
    try:
        db.commit()
        db.refresh(db_associacao)
        return db_associacao
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Erro de integridade (talvez Nome ou CNPJ já existam).")
    except Exception as e:
        db.rollback()
        raise ValueError(f"Erro inesperado ao atualizar associação: {e}") from e


def delete_associacao(db: Session, associacao_id: int) -> Optional[models.Associacao]:
    """Soft delete - marca como inativa"""
    db_associacao = get_associacao(db, associacao_id=associacao_id)
    
    if not db_associacao:
        return None
        
    if not db_associacao.ativo:
         return db_associacao

    db_associacao.ativo = False
    
    db.commit()
    db.refresh(db_associacao)
    
    return db_associacao

# =============== FUNÇÕES PARA PRODUÇÃO ===============

def get_associacao_with_producao(db: Session, associacao_id: int, ano: int = None):
    """Buscar associação com dados de produção (Nova Arquitetura)"""
    query = db.query(models.Associacao).options(
        joinedload(models.Associacao.producoes)
    ).filter(models.Associacao.id == associacao_id)
    
    if ano:
        # Note a mudança de ProducaoMensal para ProducaoImpacto
        query = query.join(models.ProducaoImpacto).filter(
            models.ProducaoImpacto.ano == ano
        )
    
    return query.first()

def get_total_producao_by_associacao(db: Session, associacao_id: int, ano: int) -> float:
    """Somar produção total de uma associação no ano"""
    # Note a mudança para ProducaoImpacto e peso_kg
    result = db.query(func.sum(models.ProducaoImpacto.peso_kg)).filter(
        and_(
            models.ProducaoImpacto.associacao_id == associacao_id,
            models.ProducaoImpacto.ano == ano
        )
    ).scalar()
    
    return float(result) if result else 0.0