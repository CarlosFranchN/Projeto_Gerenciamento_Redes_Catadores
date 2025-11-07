from sqlalchemy.orm import Session,joinedload
from app import models
from datetime import date
from sqlalchemy import func,and_
from typing import List,Optional
from sqlalchemy.exc import IntegrityError
import time
import random


from .. import schemas


def calcular_estoque_material(db: Session, material_id: int) -> float:
    total_doado = (
        db.query(func.sum(models.RecebimentoDoacao.quantidade))
        .filter(models.RecebimentoDoacao.id_material == material_id)
        .filter(models.RecebimentoDoacao.status == "Confirmada")
        .scalar()
    ) or 0.0

    total_comprado = (
        db.query(func.sum(models.Compra.quantidade))
        .filter(models.Compra.id_material == material_id)
        .filter(models.Compra.status == "Concluída")
        .scalar()
    ) or 0.0

    total_vendido = (
        db.query(func.sum(models.ItemVenda.quantidade_vendida))
        .join(models.Venda)
        .filter(models.ItemVenda.id_material == material_id)
        .filter(models.Venda.concluida == True)
        .scalar()
    ) or 0.0

    estoque_atual = (total_doado + total_comprado) - total_vendido
    return max(0.0, estoque_atual)

def get_estoque_todos_materiais(db: Session) -> List[dict]:
    """Retorna lista de materiais com o estoque calculado."""
    todos_materiais = get_all_material(db, limit=1000) 
    estoque_completo = []
    for material in todos_materiais:
        estoque = calcular_estoque_material(db, material.id)
        
        estoque_completo.append({
            **material.__dict__, 
            "estoque_atual": estoque
        })
    return estoque_completo

def get_estoque_todos_materiais(db: Session, skip: int = 0, limit: int = 100) -> dict:

    query = db.query(models.Material).filter(models.Material.ativo == True)
    
    
    total_count = query.count()
    
    
    materiais_pagina = (
        query
        .order_by(models.Material.nome)
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    
    items = []
    for material in materiais_pagina:
        estoque = calcular_estoque_material(db, material.id)
        items.append({
            **material.__dict__,
            "estoque_atual": estoque
        })
        
    return {"total_count": total_count, "items": items}


def get_material(db: Session, id_material: int):
    query = db.query(models.Material).filter(models.Material.id == id_material).first()
    return query

def get_all_material(db: Session, skip: int = 0 , limit: int = 100):
    query = db.query(models.Material).offset(skip).limit(limit).all()
    return query

def create_material(db: Session, material: schemas.MaterialCreate):
    
    db_material = models.Material(
        nome = material.nome,
        categoria = material.categoria,
        unidade_medida = material.unidade_medida
    )
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    
    cod_gerado = f"{db_material.id:04d}"
    db_material.codigo_material = cod_gerado
    
    db.commit()
    db.refresh(db_material)
    return db_material

def update_material(db: Session, material_id: int, material_update: schemas.MaterialUpdate):

    db_material = get_material(db, id_material=material_id)

   
    if not db_material:
        return None

 
    update_data = material_update.dict(exclude_unset=True) 
    for key, value in update_data.items():
        setattr(db_material, key, value) 


    db.commit()

    db.refresh(db_material)

    return db_material

def delete_material(db: Session, material_id: int):
    """Marca um material como inativo (Soft Delete)."""
    db_material = get_material(db, id_material=material_id)
    if not db_material:
        return None
    
    
    if not db_material.ativo:
        return db_material

    db_material.ativo = False
    db.commit()
    db.refresh(db_material)
    return db_material