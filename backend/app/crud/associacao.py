from sqlalchemy.orm import Session,joinedload
from app import models
from datetime import date
from sqlalchemy import func,and_
from typing import List,Optional
from sqlalchemy.exc import IntegrityError
import time
import random

from .. import schemas

MAX_RETRIES = 3

def get_associacao(db: Session, id_associacao: int):
    query = db.query(models.Associacao).options(joinedload(models.Associacao.doador_info)).filter(models.Associacao.id == id_associacao).first()
    return query

def get_all_associacoes(db: Session, skip: int = 0, limit: int = 100) -> dict:
    """Lista associações ATIVAS com paginação e contagem total."""
    
    # 1. Query base (apenas ativas)
    query = db.query(models.Associacao).filter(models.Associacao.ativo == True)

    # 2. Contagem total
    total_count = query.count()

    # 3. Busca da página atual
    items = (
        query
        .join(models.Parceiro, models.Associacao.parceiro_id == models.Parceiro.id)
        .options(joinedload(models.Associacao.parceiro_info))
        .order_by(models.Parceiro.nome)
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    return {"total_count": total_count, "items": items}

def create_associacao(db: Session, associacao: schemas.AssociacaoCreate) -> models.Associacao:
    """
    Cria um Parceiro (tipo ASSOCIACAO) e seus detalhes de Associação.
    """
    # 1. Garante que o tipo 'ASSOCIACAO' existe e pega seu ID
    tipo_assoc = db.query(models.TipoParceiro).filter(models.TipoParceiro.nome == "ASSOCIACAO").first()
    if not tipo_assoc:
        # Se não existir (o que não deve acontecer se a migração rodou), cria por segurança
        tipo_assoc = models.TipoParceiro(nome="ASSOCIACAO")
        db.add(tipo_assoc)
        db.flush()
    
    id_tipo = tipo_assoc.id

    # 2. Cria o registro PAI (Parceiro)
    db_parceiro = models.Parceiro(
        nome=associacao.nome,
        id_tipo_parceiro=id_tipo # 👈 CORRIGIDO AQUI (de 'associacao' para 'parceiro')
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
        parceiro_id=db_parceiro.id, # Linka ao pai
        lider=associacao.lider,
        telefone=associacao.telefone,
        cnpj=associacao.cnpj,
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
    Pode precisar atualizar a tabela 'doadores' (para o nome) e 'associacoes' (para os detalhes).
    """
    # 1. Busca a Associacao (detalhes) pelo seu ID
    db_associacao = get_associacao(db, associacao_id=associacao_id)
    if not db_associacao:
        return None

    # 2. Pega o objeto Doador pai
    db_doador = db_associacao.doador_info

    # 3. Converte o schema de update para um dicionário
    update_data = associacao_update.dict(exclude_unset=True)

    # 4. Itera e atualiza os campos nas tabelas corretas
    for key, value in update_data.items():
        if key == 'nome':
            # 'nome' pertence ao Doador
            setattr(db_doador, key, value)
        elif hasattr(db_associacao, key):
            # 'lider', 'cnpj', 'ativo', etc. pertencem à Associacao
            setattr(db_associacao, key, value)
    
    try:
        db.commit() # Salva as mudanças (potencialmente em ambas as tabelas)
    except IntegrityError as e:
        db.rollback()
        # Verifica erro de nome de doador duplicado
        if "unique constraint" in str(e).lower() and "doadores_nome_key" in str(e).lower():
            raise ValueError(f"Já existe um doador com o nome '{update_data['nome']}'")
        else:
            raise e
    except Exception as e:
        db.rollback()
        raise ValueError(f"Erro inesperado ao atualizar associação: {e}") from e

    db.refresh(db_associacao)
    return db_associacao

def delete_associacao(db: Session, associacao_id: int) -> Optional[models.Associacao]:

    db_associacao = get_associacao(db, id_associacao=associacao_id)
    
    if not db_associacao:
        return None # Associação não encontrada
        
    if not db_associacao.ativo:
         return db_associacao # Já está inativa

    db_associacao.ativo = False # Marca como inativa
    
    db.commit()
    db.refresh(db_associacao)
    
    return db_associacao