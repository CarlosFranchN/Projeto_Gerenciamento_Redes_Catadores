from sqlalchemy.orm import Session,joinedload
from app import models
from datetime import date
from sqlalchemy import func,and_
from typing import List,Optional
from sqlalchemy.exc import IntegrityError
import time
import random

from .. import schemas


def get_report_summary(db: Session, start_date: Optional[date] = None, end_date: Optional[date] = None):
    # Base queries
    query_entradas = db.query(func.sum(models.EntradaMaterial.quantidade)).filter(models.EntradaMaterial.status == "Confirmada")
    query_vendas = db.query(
        func.sum(models.ItemVenda.quantidade_vendida).label("total_vendido"),
        func.sum(models.ItemVenda.quantidade_vendida * models.ItemVenda.valor_unitario).label("receita")
    ).join(models.Venda).filter(models.Venda.concluida == True)
    
    # Apply date filters if provided
    if start_date:
        query_entradas = query_entradas.filter(models.EntradaMaterial.data_entrada >= start_date)
        query_vendas = query_vendas.filter(models.Venda.data_venda >= start_date)
    if end_date:
        # Include the end date by adding 1 day or adjusting the comparison
        # Simplest: filter up to the end of the end_date if using DateTime
        # If using Date, >= start_date and <= end_date works
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
    """Calcula recebido, vendido, saldo e receita agrupado por material para um período."""

    # Subquery para calcular o total recebido por material
    sq_recebido = (
        db.query(
            models.EntradaMaterial.id_material,
            func.sum(models.EntradaMaterial.quantidade).label("total_recebido")
        )
        .filter(models.EntradaMaterial.status == "Confirmada")
    )
    # Aplica filtros de data se fornecidos
    if start_date:
        sq_recebido = sq_recebido.filter(models.EntradaMaterial.data_entrada >= start_date)
    if end_date:
        sq_recebido = sq_recebido.filter(models.EntradaMaterial.data_entrada <= end_date)
    sq_recebido = sq_recebido.group_by(models.EntradaMaterial.id_material).subquery()

    # Subquery para calcular o total vendido e receita por material
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

    # Query principal: Junta Material com as subqueries
    resultado = (
        db.query(
            models.Material.nome,
            models.Material.unidade_medida,
            # Usa coalesce para tratar casos onde não houve recebimento ou venda (retorna 0)
            func.coalesce(sq_recebido.c.total_recebido, 0).label("recebido"),
            func.coalesce(sq_vendido.c.total_vendido, 0).label("vendido"),
            func.coalesce(sq_vendido.c.receita_total, 0).label("receita")
        )
        # Left join para incluir materiais que podem não ter tido entradas ou vendas no período
        .outerjoin(sq_recebido, models.Material.id == sq_recebido.c.id_material)
        .outerjoin(sq_vendido, models.Material.id == sq_vendido.c.id_material)
        .order_by(models.Material.nome)
        .all()
    )

    # Formata a resposta no schema esperado, calculando o saldo
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

def get_report_por_associacao(db: Session, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[schemas.ReportPorAssociacaoItem]:
    """Calcula o total recebido agrupado por associação para um período."""

    query = (
        db.query(
            models.Associacao.nome,
            func.sum(models.EntradaMaterial.quantidade).label("total_quantidade")
        )
        .join(models.EntradaMaterial, models.Associacao.id == models.EntradaMaterial.id_associacao)
        .filter(models.EntradaMaterial.status == "Confirmada") # Apenas entradas confirmadas
        .filter(models.Associacao.ativo == True) # Apenas associações ativas (opcional)
    )

    # Aplica filtros de data
    if start_date:
        query = query.filter(models.EntradaMaterial.data_entrada >= start_date)
    if end_date:
        query = query.filter(models.EntradaMaterial.data_entrada <= end_date)

    resultado = query.group_by(models.Associacao.nome).order_by(func.sum(models.EntradaMaterial.quantidade).desc()).all()

    # Formata a resposta no schema esperado
    report_final = [
        schemas.ReportPorAssociacaoItem(nome=r.nome, quantidade=r.total_quantidade)
        for r in resultado
    ]
    return report_final