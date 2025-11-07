from sqlalchemy.orm import Session,joinedload
from .. import models, schemas
from typing import Optional
from datetime import date

def get_compras(
    db: Session, skip: int = 0, limit: int = 100,
    data_inicio: Optional[date] = None, data_fim: Optional[date] = None,
    id_parceiro: Optional[int] = None, id_material: Optional[int] = None
) -> dict:
    """Lista compras com filtros e paginação."""
    query = db.query(models.Compra).filter(models.Compra.status == "Concluída")
    # 2. Aplicação dinâmica dos filtros
    if data_inicio:
        # Na tabela Compra, o campo de data é 'data_compra'
        query = query.filter(models.Compra.data_compra >= data_inicio)
    if data_fim:
        query = query.filter(models.Compra.data_compra <= data_fim)
    if id_parceiro:
        query = query.filter(models.Compra.id_parceiro == id_parceiro)
    if id_material:
        query = query.filter(models.Compra.id_material == id_material)

    # 3. Contagem total (para paginação)
    total_count = query.count()

    # 4. Busca da página atual com ordenação e relacionamentos
    items = (
        query
        .options(
            joinedload(models.Compra.material), 
            joinedload(models.Compra.parceiro)
        )
        .order_by(models.Compra.data_compra.desc()) 
        .offset(skip)
        .limit(limit)
        .all() 
    )
    return {"total_count": total_count, "items": items}

def create_compra(db: Session, compra: schemas.CompraCreate):
    """Registra uma nova compra (entrada COM custo)."""
    hoje = date.today()
    prefixo = f"C-{hoje.strftime('%Y%m%d')}-"
    count = db.query(models.Compra).filter(models.Compra.codigo_compra.startswith(prefixo)).count()
    codigo = f"{prefixo}{count + 1:03d}"
    
    # Calcula o total pago
    total_pago = compra.quantidade * compra.valor_pago_unitario

    db_compra = models.Compra(
        **compra.dict(),
        codigo_compra=codigo,
        valor_pago_total=total_pago,
        status="Concluída"
    )
    db.add(db_compra)
    db.commit()
    db.refresh(db_compra)
    return db_compra

def cancel_compra(db: Session, compra_id: int):
    """Cancela uma compra."""
    db_compra = db.query(models.Compra).filter(models.Compra.id == compra_id).first()
    if not db_compra or db_compra.status == "Cancelada": return db_compra
    db_compra.status = "Cancelada"
    db.commit()
    db.refresh(db_compra)
    return db_compra