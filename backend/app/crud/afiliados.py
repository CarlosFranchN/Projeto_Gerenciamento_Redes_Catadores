# backend/app/crud/afiliado.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Tuple

from app import models, schemas


# =============== CREATE ===============
def create_afiliado(db: Session, afiliado: schemas.AfiliadoCreate) -> models.Afiliado:
    """
    Criar novo afiliado
    """
    # Verifica se CPF já existe (se foi informado)
    if afiliado.cpf:
        existing = db.query(models.Afiliado).filter(
            models.Afiliado.cpf == afiliado.cpf,
            models.Afiliado.ativo == True
        ).first()
        if existing:
            raise ValueError("CPF já cadastrado")
    
    # Cria o afiliado
    db_afiliado = models.Afiliado(
        nome=afiliado.nome,
        cpf=afiliado.cpf,
        funcao=afiliado.funcao,
        data_filiacao=afiliado.data_filiacao,
        associacao_id=afiliado.associacao_id,
        ativo=True
    )
    
    db.add(db_afiliado)
    db.commit()
    db.refresh(db_afiliado)
    
    return db_afiliado


# =============== READ (SINGLE) ===============
def get_afiliado(db: Session, afiliado_id: int) -> Optional[models.Afiliado]:
    """
    Obter afiliado por ID
    """
    return db.query(models.Afiliado).filter(
        models.Afiliado.id == afiliado_id
    ).first()


def get_afiliado_by_cpf(db: Session, cpf: str) -> Optional[models.Afiliado]:
    """
    Obter afiliado por CPF
    """
    return db.query(models.Afiliado).filter(
        models.Afiliado.cpf == cpf
    ).first()


# =============== READ (LIST) ===============
def get_afiliados(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    associacao_id: Optional[int] = None,
    ativo: Optional[bool] = None,
    search: Optional[str] = None
) -> Tuple[List[models.Afiliado], int]:
    """
    Listar afiliados com filtros e paginação
    
    Retorna: (lista de afiliados, total de registros)
    """
    query = db.query(models.Afiliado)
    
    # Filtro por associação
    if associacao_id is not None:
        query = query.filter(models.Afiliado.associacao_id == associacao_id)
    
    # Filtro por status (ativo/inativo)
    if ativo is not None:
        query = query.filter(models.Afiliado.ativo == ativo)
    
    # Busca por nome
    if search:
        query = query.filter(models.Afiliado.nome.ilike(f"%{search}%"))
    
    # Total de registros (para paginação)
    total = query.count()
    
    # Aplica paginação
    afiliados = query.offset(skip).limit(limit).all()
    
    return afiliados, total


def get_afiliados_by_associacao(
    db: Session,
    associacao_id: int,
    skip: int = 0,
    limit: int = 100
) -> Tuple[List[models.Afiliado], int]:
    """
    Listar afiliados de uma associação específica
    """
    return get_afiliados(
        db,
        skip=skip,
        limit=limit,
        associacao_id=associacao_id
    )


# =============== UPDATE ===============
def update_afiliado(
    db: Session,
    afiliado_id: int,
    afiliado: schemas.AfiliadoUpdate
) -> Optional[models.Afiliado]:
    """
    Atualizar dados de um afiliado
    """
    db_afiliado = get_afiliado(db, afiliado_id)
    
    if not db_afiliado:
        return None
    
    # Verifica CPF duplicado (se estiver sendo alterado)
    if afiliado.cpf and afiliado.cpf != db_afiliado.cpf:
        existing = db.query(models.Afiliado).filter(
            models.Afiliado.cpf == afiliado.cpf,
            models.Afiliado.id != afiliado_id,
            models.Afiliado.ativo == True
        ).first()
        if existing:
            raise ValueError("CPF já cadastrado")
    
    # Atualiza campos
    update_data = afiliado.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_afiliado, field, value)
    
    db.commit()
    db.refresh(db_afiliado)
    
    return db_afiliado


# =============== DELETE (SOFT) ===============
def delete_afiliado(db: Session, afiliado_id: int) -> bool:
    """
    Desativar afiliado (soft delete)
    
    Retorna: True se sucesso, False se não encontrado
    """
    db_afiliado = get_afiliado(db, afiliado_id)
    
    if not db_afiliado:
        return False
    
    db_afiliado.ativo = False
    db.commit()
    
    return True


def hard_delete_afiliado(db: Session, afiliado_id: int) -> bool:
    """
    Excluir afiliado permanentemente (use com cautela!)
    
    Retorna: True se sucesso, False se não encontrado
    """
    db_afiliado = get_afiliado(db, afiliado_id)
    
    if not db_afiliado:
        return False
    
    db.delete(db_afiliado)
    db.commit()
    
    return True


# =============== ESTATÍSTICAS ===============
def get_afiliados_stats(db: Session, associacao_id: Optional[int] = None) -> dict:
    """
    Obter estatísticas de afiliados
    
    Retorna: {
        "total": int,
        "ativos": int,
        "inativos": int,
        "por_funcao": [{"funcao": str, "count": int}, ...]
    }
    """
    query = db.query(models.Afiliado)
    
    if associacao_id:
        query = query.filter(models.Afiliado.associacao_id == associacao_id)
    
    total = query.count()
    ativos = query.filter(models.Afiliado.ativo == True).count()
    inativos = query.filter(models.Afiliado.ativo == False).count()
    
    # Agrupa por função
    por_funcao = db.query(
        models.Afiliado.funcao,
        func.count(models.Afiliado.id).label('count')
    ).filter(
        models.Afiliado.ativo == True
    )
    
    if associacao_id:
        por_funcao = por_funcao.filter(models.Afiliado.associacao_id == associacao_id)
    
    por_funcao = por_funcao.group_by(models.Afiliado.funcao).all()
    
    return {
        "total": total,
        "ativos": ativos,
        "inativos": inativos,
        "por_funcao": [{"funcao": f.funcao or "Não informada", "count": f.count} for f in por_funcao]
    }