from sqlalchemy.orm import Session, joinedload
from app import models
from datetime import datetime
from sqlalchemy import func, and_
from typing import List, Optional
from sqlalchemy.exc import IntegrityError

from .. import schemas

def get_associacao(db: Session, associacao_id: int):
    """Buscar associação por ID com parceiro carregado"""
    query = db.query(models.Associacao).options(
        joinedload(models.Associacao.parceiro_info)
    ).filter(models.Associacao.id == associacao_id).first()
    return query

def get_all_associacoes(db: Session, skip: int = 0, limit: int = 100, ativo: bool = True) -> dict:
    """Lista associações ATIVAS com paginação e contagem total."""
    
    # 1. Query base
    query = db.query(models.Associacao).join(models.Parceiro)
    
    if ativo:
        query = query.filter(models.Associacao.ativo == True)

    # 2. Contagem total
    total_count = query.count()

    # 3. Busca da página atual
    items = (
        query
        .options(joinedload(models.Associacao.parceiro_info))
        .order_by(models.Parceiro.nome)
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    # ✅ Converte para dicionário com nome do parceiro
    items_data = []
    for assoc in items:
        items_data.append({
            "id": assoc.id,
            "parceiro_id": assoc.parceiro_id,
            "nome": assoc.parceiro_info.nome if assoc.parceiro_info else "N/A",
            "lider": assoc.lider,
            "telefone": assoc.telefone,
            "email": assoc.email,
            "cnpj": assoc.cnpj,
            "logradouro": assoc.logradouro,
            "numero": assoc.numero,
            "complemento": assoc.complemento,
            "bairro": assoc.bairro,
            "cidade": assoc.cidade,
            "uf": assoc.uf,
            "status": assoc.status,
            "ativo": assoc.ativo,
            "data_cadastro": assoc.data_cadastro
        })
    
    return {"total_count": total_count, "items": items_data}

def get_associacoes_ativas(db: Session) -> List[models.Associacao]:
    """Buscar todas associações ativas (para o frontend público)"""
    return (
        db.query(models.Associacao)
        .filter(models.Associacao.ativo == True)
        .options(joinedload(models.Associacao.parceiro_info))
        .order_by(models.Parceiro.nome)
        .all()
    )

def create_associacao(db: Session, associacao: schemas.AssociacaoCreate) -> models.Associacao:
    """
    Cria um Parceiro (tipo ASSOCIACAO) e seus detalhes de Associação.
    """
    # 1. Garante que o tipo 'ASSOCIACAO' existe
    tipo_assoc = db.query(models.TipoParceiro).filter(
        models.TipoParceiro.nome == "ASSOCIACAO"
    ).first()
    if not tipo_assoc:
        tipo_assoc = models.TipoParceiro(nome="ASSOCIACAO")
        db.add(tipo_assoc)
        db.flush()
    
    id_tipo = tipo_assoc.id

    # 2. Cria o registro PAI (Parceiro)
    db_parceiro = models.Parceiro(
        nome=associacao.nome,  # ✅ Usa o nome do schema
        id_tipo_parceiro=id_tipo
    )
    db.add(db_parceiro)
    
    try:
        db.flush() 
    except IntegrityError as e:
        db.rollback()
        if "unique constraint" in str(e).lower() and "parceiros_nome_key" in str(e).lower():
            raise ValueError(f"Já existe um parceiro com o nome '{associacao.nome}'")
        raise e

    # 3. Cria o registro FILHO (Associacao)
    db_associacao = models.Associacao(
        parceiro_id=db_parceiro.id,
        lider=associacao.lider,
        telefone=associacao.telefone,
        email=associacao.email,
        cnpj=associacao.cnpj,
        logradouro=associacao.logradouro,
        numero=associacao.numero,
        complemento=associacao.complemento,
        bairro=associacao.bairro,
        cidade=associacao.cidade,
        uf=associacao.uf,
        status=associacao.status,
        ativo=associacao.ativo
    )
    db.add(db_associacao)

    try:
        db.commit() 
        db.refresh(db_associacao)
        return db_associacao
    except Exception as e:
        db.rollback()
        raise ValueError(f"Erro ao salvar associação: {e}") from e

def update_associacao(db: Session, associacao_id: int, associacao_update: schemas.AssociacaoUpdate) -> Optional[models.Associacao]:
    """
    Atualiza uma associação.
    Pode precisar atualizar a tabela 'parceiros' (para o nome) e 'associacoes' (para os detalhes).
    """
    # 1. Busca a Associacao (detalhes) pelo seu ID
    db_associacao = get_associacao(db, associacao_id=associacao_id)
    if not db_associacao:
        return None

    # 2. Pega o objeto Parceiro pai (antigo Doador)
    db_parceiro = db_associacao.parceiro_info

    # 3. Converte o schema de update para um dicionário
    update_data = associacao_update.model_dump(exclude_unset=True)

    # 4. Itera e atualiza os campos nas tabelas corretas
    for key, value in update_data.items():
        if key == 'nome':
            # 'nome' pertence ao Parceiro
            setattr(db_parceiro, key, value)
        elif hasattr(db_associacao, key):
            # 'lider', 'cnpj', 'ativo', 'endereco', etc. pertencem à Associacao
            setattr(db_associacao, key, value)
    
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        if "unique constraint" in str(e).lower() and "parceiros_nome_key" in str(e).lower():
            raise ValueError(f"Já existe um parceiro com o nome '{update_data.get('nome')}'")
        else:
            raise e
    except Exception as e:
        db.rollback()
        raise ValueError(f"Erro inesperado ao atualizar associação: {e}") from e

    db.refresh(db_associacao)
    return db_associacao

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
    """Buscar associação com dados de produção"""
    from sqlalchemy.orm import joinedload
    
    query = db.query(models.Associacao).options(
        joinedload(models.Associacao.parceiro_info),
        joinedload(models.Associacao.producoes)
    ).filter(models.Associacao.id == associacao_id)
    
    if ano:
        # Filtra produções do ano específico
        query = query.join(models.ProducaoMensal).filter(
            models.ProducaoMensal.ano == ano
        )
    
    return query.first()

def get_total_producao_by_associacao(db: Session, associacao_id: int, ano: int) -> float:
    """Somar produção total de uma associação no ano"""
    from sqlalchemy import func
    
    result = db.query(func.sum(models.ProducaoMensal.kg)).filter(
        and_(
            models.ProducaoMensal.associacao_id == associacao_id,
            models.ProducaoMensal.ano == ano
        )
    ).scalar()
    
    return float(result) if result else 0.0