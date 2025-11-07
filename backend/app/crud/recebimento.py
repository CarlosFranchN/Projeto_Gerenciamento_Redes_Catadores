from sqlalchemy.orm import Session, joinedload
from .. import models, schemas
from typing import List, Optional
from datetime import date
from sqlalchemy import func

def create_recebimento(db: Session, recebimento: schemas.RecebimentoDoacaoCreate):
    """Registra um novo recebimento de doação (entrada sem custo)."""
    
    hoje = date.today()
    prefixo_codigo = f"R-{hoje.strftime('%Y%m%d')}-" 
    
    count_hoje = db.query(models.RecebimentoDoacao).filter(models.RecebimentoDoacao.codigo_lote.startswith(prefixo_codigo)).count()
    sequencial = count_hoje + 1
    codigo_gerado = f"{prefixo_codigo}{sequencial:03d}"
    
    db_recebimento = models.RecebimentoDoacao(
        id_parceiro=recebimento.id_parceiro, 
        id_material=recebimento.id_material,
        quantidade=recebimento.quantidade,
        codigo_lote=codigo_gerado,
        status="Confirmada"
    )

    db.add(db_recebimento)
    db.commit()
    db.refresh(db_recebimento)
    return db_recebimento

def get_recebimentos(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    id_parceiro: Optional[int] = None, 
    id_material: Optional[int] = None
) -> dict: 
    """
    Lista recebimentos com filtros e paginação.
    """
    query = (
        db.query(models.RecebimentoDoacao)
        .filter(models.RecebimentoDoacao.status == "Confirmada")
    )

    if data_inicio:
        query = query.filter(models.RecebimentoDoacao.data_entrada >= data_inicio)
    if data_fim:
        query = query.filter(models.RecebimentoDoacao.data_entrada <= data_fim)
    if id_parceiro:
        query = query.filter(models.RecebimentoDoacao.id_parceiro == id_parceiro)
    if id_material:
        query = query.filter(models.RecebimentoDoacao.id_material == id_material)

    total_count = query.count()

    items = (
        query
        .options(
            joinedload(models.RecebimentoDoacao.material), 
            joinedload(models.RecebimentoDoacao.parceiro) # 👈 Carrega o Parceiro
        )
        .order_by(models.RecebimentoDoacao.data_entrada.desc()) 
        .offset(skip)
        .limit(limit)
        .all() 
    )
    
    return {"total_count": total_count, "items": items}

def cancel_recebimento(db: Session, recebimento_id: int):
    """Cancela um recebimento (Soft Delete)."""
    db_recebimento = db.query(models.RecebimentoDoacao).filter(models.RecebimentoDoacao.id == recebimento_id).first()
    if not db_recebimento or db_recebimento.status == "Cancelada":
        return db_recebimento

    db_recebimento.status = "Cancelada"
    db.commit()
    db.refresh(db_recebimento)
    return db_recebimento