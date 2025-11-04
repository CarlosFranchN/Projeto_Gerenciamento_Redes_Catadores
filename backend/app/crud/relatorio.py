from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, select, case
from .. import models, schemas
from typing import List, Optional
from datetime import date

def get_report_summary(db: Session, start_date: Optional[date] = None, end_date: Optional[date] = None):
    query_entradas = db.query(func.sum(models.EntradaMaterial.quantidade)).filter(models.EntradaMaterial.status == "Confirmada")
    query_vendas = db.query(
        func.sum(models.ItemVenda.quantidade_vendida).label("total_vendido"),
        func.sum(models.ItemVenda.quantidade_vendida * models.ItemVenda.valor_unitario).label("receita")
    ).join(models.Venda).filter(models.Venda.concluida == True)
    
    if start_date:
        query_entradas = query_entradas.filter(models.EntradaMaterial.data_entrada >= start_date)
        query_vendas = query_vendas.filter(models.Venda.data_venda >= start_date)
    if end_date:
        query_entradas = query_entradas.filter(models.EntradaMaterial.data_entrada <= end_date)
        query_vendas = query_vendas.filter(models.Venda.data_venda <= end_date)
        
    total_recebido = query_entradas.scalar() or 0.0
    vendas_result = query_vendas.first()
    total_vendido = vendas_result.total_vendido if vendas_result else 0.0
    receita_periodo = vendas_result.receita if vendas_result else 0.0

    return schemas.ReportSummaryResponse(
        total_recebido=total_recebido,
        total_vendido=total_vendido,
        receita_periodo=receita_periodo
    )
    
def get_report_por_material(db: Session, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[schemas.ReportPorMaterialItem]:
    sq_recebido = (
        db.query(
            models.EntradaMaterial.id_material,
            func.sum(models.EntradaMaterial.quantidade).label("total_recebido")
        )
        .filter(models.EntradaMaterial.status == "Confirmada")
    )
    if start_date:
        sq_recebido = sq_recebido.filter(models.EntradaMaterial.data_entrada >= start_date)
    if end_date:
        sq_recebido = sq_recebido.filter(models.EntradaMaterial.data_entrada <= end_date)
    sq_recebido = sq_recebido.group_by(models.EntradaMaterial.id_material).subquery()

    sq_vendido = (
        db.query(
            models.ItemVenda.id_material,
            func.sum(models.ItemVenda.quantidade_vendida).label("total_vendido"),
            func.sum(models.ItemVenda.quantidade_vendida * models.ItemVenda.valor_unitario).label("receita_total")
        )
        .join(models.Venda)
        .filter(models.Venda.concluida == True)
    )
    if start_date:
        sq_vendido = sq_vendido.filter(models.Venda.data_venda >= start_date)
    if end_date:
        sq_vendido = sq_vendido.filter(models.Venda.data_venda <= end_date)
    sq_vendido = sq_vendido.group_by(models.ItemVenda.id_material).subquery()

    resultado = (
        db.query(
            models.Material.nome,
            models.Material.unidade_medida,
            func.coalesce(sq_recebido.c.total_recebido, 0).label("recebido"),
            func.coalesce(sq_vendido.c.total_vendido, 0).label("vendido"),
            func.coalesce(sq_vendido.c.receita_total, 0).label("receita")
        )
        .outerjoin(sq_recebido, models.Material.id == sq_recebido.c.id_material)
        .outerjoin(sq_vendido, models.Material.id == sq_vendido.c.id_material)
        .order_by(models.Material.nome)
        .all()
    )

    report_final = []
    for r in resultado:
        saldo = r.recebido - r.vendido
        report_final.append(schemas.ReportPorMaterialItem(
            nome=r.nome,
            unidade_medida=r.unidade_medida,
            recebido=r.recebido,
            vendido=r.vendido,
            saldo=saldo,
            receita=r.receita
        ))
        
    return report_final

def get_report_por_doador(db: Session, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[schemas.ReportPorDoadorItem]:
    """Calcula o total recebido agrupado por doador para um período."""
    
    query = (
        db.query(
            models.Doador.nome,
            func.sum(models.EntradaMaterial.quantidade).label("total_quantidade")
        )
        .join(models.EntradaMaterial, models.Doador.id == models.EntradaMaterial.id_doador)
        .filter(models.EntradaMaterial.status == "Confirmada") 
    )
    
    if start_date:
        query = query.filter(models.EntradaMaterial.data_entrada >= start_date)
    if end_date:
        query = query.filter(models.EntradaMaterial.data_entrada <= end_date)
        
    resultado = query.group_by(models.Doador.nome).order_by(func.sum(models.EntradaMaterial.quantidade).desc()).all()
    
    report_final = [
        schemas.ReportPorDoadorItem(nome=r.nome, quantidade=r.total_quantidade)
        for r in resultado
    ]
    return report_final