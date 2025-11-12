# app/crud/crud_material.py
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from .. import models, schemas
from typing import List, Optional
from sqlalchemy.orm import joinedload 

def get_material(db: Session, id_material: int) -> Optional[models.Material]:
    return (
        db.query(models.Material)
        .options(joinedload(models.Material.categoria_info)) 
        .filter(models.Material.id == id_material)
        .first()
    )

def get_material_by_nome(db: Session, nome: str) -> Optional[models.Material]:
    return db.query(models.Material).filter(models.Material.nome == nome).first()

def get_all_material(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    nome: Optional[str] = None 
) -> dict:
        
    query = (
        db.query(models.Material)
        .filter(models.Material.ativo == True)
        .options(joinedload(models.Material.categoria_info))
    )
    
    if nome:
        query = query.filter(models.Material.nome.ilike(f"%{nome}%"))

    total_count = query.count()
    
    items = (
        query
        .order_by(models.Material.nome)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return {"total_count": total_count, "items": items}


def create_material(db: Session, material: schemas.MaterialCreate) -> models.Material:
    db_material = models.Material(**material.dict()) 
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    
    
    db_material.codigo = f"MAT-{db_material.id:04d}"
    db.commit()
    db.refresh(db_material)
    return db_material

def update_material(db: Session, material_id: int, material_update: schemas.MaterialUpdate) -> Optional[models.Material]:
    """Atualiza um material (agora usa o schema MaterialUpdate)."""
    db_material = get_material(db, id_material=material_id)
    if not db_material: return None
    
    
    update_data = material_update.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_material, key, value)
        
    db.commit()
    db.refresh(db_material)
    return db_material

def delete_material(db: Session, material_id: int) -> Optional[models.Material]:
    """Marca um material como inativo (Soft Delete)."""
    db_material = get_material(db, id_material=material_id)
    if not db_material or not db_material.ativo: return db_material

    db_material.ativo = False
    db.commit()
    db.refresh(db_material)
    return db_material


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

def get_estoque_todos_materiais(db: Session, skip: int = 0, limit: int = 100,nome: Optional[str] = None) -> dict:
    """Retorna lista paginada de materiais ATIVOS com o estoque calculado."""
    

    query = (
        db.query(models.Material)
        .filter(models.Material.ativo == True)
        .options(joinedload(models.Material.categoria_info))
    )
    if nome:
        query = query.filter(models.Material.nome.ilike(f"%{nome}%"))
    

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