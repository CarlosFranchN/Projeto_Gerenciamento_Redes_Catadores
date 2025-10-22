from sqlalchemy.orm import Session,joinedload
from app import models, schemas
from datetime import date
from sqlalchemy import func,and_
from typing import List,Optional
from sqlalchemy.exc import IntegrityError
import time
import random


def calcular_estoque_material(db: Session, material_id: int) -> float:
    """Calcula o estoque atual de um material específico."""
    
    total_entradas = (
        db.query(func.sum(models.EntradaMaterial.quantidade))
        .filter(models.EntradaMaterial.id_material == material_id)
        .filter(models.EntradaMaterial.status == "Confirmada")
        .scalar() 
    ) or 0.0 

    total_vendido = (
        db.query(func.sum(models.ItemVenda.quantidade_vendida).label("total_vendido"))
        # 👇 ADICIONE A CONDIÇÃO DE JOIN EXPLÍCITA 👇
        .join(models.Venda, models.ItemVenda.id_venda == models.Venda.id) 
        .filter(models.ItemVenda.id_material == material_id)
        .filter(models.Venda.concluida == True) 
        .scalar()
    ) or 0.0

    estoque_calculado = total_entradas - total_vendido
    estoque_atual = max(0.0, estoque_calculado)
    return estoque_atual

def get_estoque_todos_materiais(db: Session) -> List[dict]:
    """Busca todos os materiais e calcula o estoque atual para cada um."""
    todos_materiais = db.query(models.Material).order_by(models.Material.nome).all()

    estoque_completo = []
    for material in todos_materiais:
        estoque_atual = calcular_estoque_material(db, material_id=material.id)
        estoque_completo.append({
            "id": material.id,
            "codigo": material.codigo_material,
            "nome": material.nome,
            "categoria": material.categoria,
            "unidade_medida": material.unidade_medida,
            "estoque_atual": estoque_atual 
        })
    return estoque_completo


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
        setattr(db_material, key, value) # Define o atributo dinamicamente


    db.commit()

    db.refresh(db_material)

    return db_material