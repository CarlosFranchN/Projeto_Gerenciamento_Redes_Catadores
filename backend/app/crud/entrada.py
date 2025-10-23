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


def create_entrada_material(db: Session, entrada: schemas.EntradaMaterialCreate):
    """Registra uma nova entrada de material no banco de dados."""
    
    hoje = date.today()
    prefixo_codigo = f"E-{hoje.strftime('%Y%m%d')}-"
    

    # vendas_de_hoje = db.query(models.Venda).filter(models.Venda.codigo.startswith(prefixo_codigo)).count()
    entradas_de_hoje = db.query(models.EntradaMaterial).filter(models.EntradaMaterial.codigo_lote.startswith(prefixo_codigo)).count()
    sequencial = entradas_de_hoje + 1
    codigo_gerado = f"{prefixo_codigo}{sequencial:03d}" # Ex: V-20250925-001
    
    
    db_entrada = models.EntradaMaterial(
        **entrada.dict(), 
        codigo_lote=codigo_gerado
    )

    # db_entrada.
    db.add(db_entrada)
    db.commit()
    db.refresh(db_entrada)
    return db_entrada

def get_entradas_material(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    id_associacao: Optional[int] = None,
    id_material: Optional[int] = None
) -> dict: 

    query = (
        db.query(models.EntradaMaterial)
        .filter(models.EntradaMaterial.status == "Confirmada")
    )


    if data_inicio:
        query = query.filter(models.EntradaMaterial.data_entrada >= data_inicio)
    if data_fim:
        query = query.filter(models.EntradaMaterial.data_entrada <= data_fim)
    if id_associacao:
        query = query.filter(models.EntradaMaterial.id_associacao == id_associacao)
    if id_material:
        query = query.filter(models.EntradaMaterial.id_material == id_material)

    total_count = query.count()


    items = (
        query
        .options(
            joinedload(models.EntradaMaterial.material), 
            joinedload(models.EntradaMaterial.associacao)
        )
        .order_by(models.EntradaMaterial.data_entrada.desc()) 
        .offset(skip)
        .limit(limit)
        .all() 
    )


    return {"total_count": total_count, "items": items}

def cancel_entrada_material(db: Session, entrada_id: int):
    """Marca uma entrada de material como 'Cancelada'."""

    db_entrada = db.query(models.EntradaMaterial).filter(models.EntradaMaterial.id == entrada_id).first()

    if not db_entrada:
        return None # Entrada não encontrada

    if db_entrada.status == "Cancelada":
         return db_entrada # Já está cancelada

    db_entrada.status = "Cancelada"

    db.commit()
    db.refresh(db_entrada)

    return db_entrada