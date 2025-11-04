# app/crud/crud_entrada.py
from sqlalchemy.orm import Session, joinedload
from .. import models, schemas
from typing import List, Optional
from datetime import date
from sqlalchemy import func # Importar func

def create_entrada_material(db: Session, entrada: schemas.EntradaMaterialCreate):
    """Registra uma nova entrada de material (com lógica de código e Doador)."""
    
    hoje = date.today()
    prefixo_codigo = f"E-{hoje.strftime('%Y%m%d')}-"
    
    # Lógica de contagem (pode ser melhorada com Retry, mas funcional por enquanto)
    entradas_de_hoje = db.query(models.EntradaMaterial).filter(models.EntradaMaterial.codigo_lote.startswith(prefixo_codigo)).count()
    sequencial = entradas_de_hoje + 1
    codigo_gerado = f"{prefixo_codigo}{sequencial:03d}"
    
    db_entrada = models.EntradaMaterial(
        # Usa **entrada.dict() para pegar id_doador, id_material, quantidade
        **entrada.dict(), 
        codigo_lote=codigo_gerado,
        status="Confirmada" # Garante o status na criação
    )

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
    id_doador: Optional[int] = None, # 👈 CORRIGIDO: de id_associacao para id_doador
    id_material: Optional[int] = None
) -> dict: 
    """
    Lista entradas de material (CONFIRMADAS), com filtros, paginação e
    alinhado com a tabela Doador.
    """
    
    query = (
        db.query(models.EntradaMaterial)
        .filter(models.EntradaMaterial.status == "Confirmada")
    )

    # Adiciona os filtros dinamicamente
    if data_inicio:
        query = query.filter(models.EntradaMaterial.data_entrada >= data_inicio)
    if data_fim:
        query = query.filter(models.EntradaMaterial.data_entrada <= data_fim)
    if id_doador: # 👈 CORRIGIDO
        query = query.filter(models.EntradaMaterial.id_doador == id_doador)
    if id_material:
        query = query.filter(models.EntradaMaterial.id_material == id_material)

    # EXECUTA A CONTAGEM
    total_count = query.count()

    # Aplica JOINs, ordenação e paginação
    items = (
        query
        .options(
            joinedload(models.EntradaMaterial.material), 
            joinedload(models.EntradaMaterial.doador) # 👈 CORRIGIDO
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
        return None 
        
    if db_entrada.status == "Cancelada":
         return db_entrada 

    db_entrada.status = "Cancelada"
    
    db.commit()
    db.refresh(db_entrada)
    
    return db_entrada