# app/crud/crud_relatorio.py
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from .. import models, schemas
from typing import Optional, List
from datetime import date

def get_report_summary(db: Session, start_date: Optional[date] = None, end_date: Optional[date] = None) -> schemas.ReportSummaryResponse:
    """
    Retorna totais do período: Recebido (Doação), Comprado, Gasto em Compras, Vendido, Receita, Lucro Bruto.
    """
    # Queries base
    q_doacoes = db.query(func.sum(models.RecebimentoDoacao.quantidade)).filter(models.RecebimentoDoacao.status == "Confirmada")
    q_compras = db.query(
        func.sum(models.Compra.quantidade).label("qtd"),
        func.sum(models.Compra.valor_pago_total).label("valor")
    ).filter(models.Compra.status == "Concluída")
    q_vendas = db.query(
        func.sum(models.ItemVenda.quantidade_vendida).label("qtd"),
        func.sum(models.ItemVenda.quantidade_vendida * models.ItemVenda.valor_unitario).label("receita")
    ).join(models.Venda).filter(models.Venda.concluida == True)

    # Filtros de data
    if start_date:
        q_doacoes = q_doacoes.filter(models.RecebimentoDoacao.data_entrada >= start_date)
        q_compras = q_compras.filter(models.Compra.data_compra >= start_date)
        q_vendas = q_vendas.filter(models.Venda.data_venda >= start_date)
    if end_date:
        q_doacoes = q_doacoes.filter(models.RecebimentoDoacao.data_entrada <= end_date)
        q_compras = q_compras.filter(models.Compra.data_compra <= end_date)
        q_vendas = q_vendas.filter(models.Venda.data_venda <= end_date)

    # Executa as queries
    total_recebido = q_doacoes.scalar() or 0.0
    res_compras = q_compras.first()
    total_comprado = res_compras.qtd if res_compras and res_compras.qtd else 0.0
    total_gasto = res_compras.valor if res_compras and res_compras.valor else 0.0
    res_vendas = q_vendas.first()
    total_vendido = res_vendas.qtd if res_vendas and res_vendas.qtd else 0.0
    receita_periodo = res_vendas.receita if res_vendas and res_vendas.receita else 0.0

    return schemas.ReportSummaryResponse(
        total_recebido=total_recebido,
        total_comprado_qtd=total_comprado,
        total_gasto_compras=total_gasto,
        total_vendido=total_vendido,
        receita_periodo=receita_periodo,
        lucro_bruto=receita_periodo - total_gasto # Lucro simples (Receita - Custo de Aquisição)
    )

def get_report_por_material(db: Session, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[schemas.ReportPorMaterialItem]:
    """Relatório detalhado por material, incluindo doações e compras."""
    
    # Subquery Doações
    sq_doado = db.query(models.RecebimentoDoacao.id_material, func.sum(models.RecebimentoDoacao.quantidade).label("qtd")).filter(models.RecebimentoDoacao.status == "Confirmada")
    if start_date: sq_doado = sq_doado.filter(models.RecebimentoDoacao.data_entrada >= start_date)
    if end_date: sq_doado = sq_doado.filter(models.RecebimentoDoacao.data_entrada <= end_date)
    sq_doado = sq_doado.group_by(models.RecebimentoDoacao.id_material).subquery()

    # Subquery Compras
    sq_comprado = db.query(models.Compra.id_material, func.sum(models.Compra.quantidade).label("qtd")).filter(models.Compra.status == "Concluída")
    if start_date: sq_comprado = sq_comprado.filter(models.Compra.data_compra >= start_date)
    if end_date: sq_comprado = sq_comprado.filter(models.Compra.data_compra <= end_date)
    sq_comprado = sq_comprado.group_by(models.Compra.id_material).subquery()

    # Subquery Vendas
    sq_vendido = db.query(
        models.ItemVenda.id_material,
        func.sum(models.ItemVenda.quantidade_vendida).label("qtd"),
        func.sum(models.ItemVenda.quantidade_vendida * models.ItemVenda.valor_unitario).label("receita")
    ).join(models.Venda).filter(models.Venda.concluida == True)
    if start_date: sq_vendido = sq_vendido.filter(models.Venda.data_venda >= start_date)
    if end_date: sq_vendido = sq_vendido.filter(models.Venda.data_venda <= end_date)
    sq_vendido = sq_vendido.group_by(models.ItemVenda.id_material).subquery()

    # Query Principal
    res = db.query(
        models.Material.nome,
        models.Material.unidade_medida,
        func.coalesce(sq_doado.c.qtd, 0).label("doado"),
        func.coalesce(sq_comprado.c.qtd, 0).label("comprado"),
        func.coalesce(sq_vendido.c.qtd, 0).label("vendido"),
        func.coalesce(sq_vendido.c.receita, 0).label("receita")
    ).outerjoin(sq_doado, models.Material.id == sq_doado.c.id_material)\
     .outerjoin(sq_comprado, models.Material.id == sq_comprado.c.id_material)\
     .outerjoin(sq_vendido, models.Material.id == sq_vendido.c.id_material)\
     .order_by(models.Material.nome).all()

    return [
        schemas.ReportPorMaterialItem(
            nome=r.nome, unidade_medida=r.unidade_medida,
            recebido=r.doado, comprado=r.comprado, vendido=r.vendido,
            saldo=(r.doado + r.comprado) - r.vendido, receita=r.receita
        ) for r in res
    ]

def get_report_por_parceiro(db: Session, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[schemas.ReportPorParceiroItem]:
    """Relatório de entradas (doações + compras) agrupado por Parceiro."""
    
    # Precisamos unir (UNION ALL) as duas tabelas de entrada para agrupar por parceiro
    # Esta é uma query mais avançada, vamos simplificar fazendo duas e somando no Python por enquanto,
    # ou usar uma CTE se o volume for grande. Para MVP, vamos de Python puro após buscar os totais.
    
    # 1. Totais de Doações por Parceiro
    q_doacoes = db.query(models.RecebimentoDoacao.id_parceiro, func.sum(models.RecebimentoDoacao.quantidade)).filter(models.RecebimentoDoacao.status == "Confirmada")
    if start_date: q_doacoes = q_doacoes.filter(models.RecebimentoDoacao.data_entrada >= start_date)
    if end_date: q_doacoes = q_doacoes.filter(models.RecebimentoDoacao.data_entrada <= end_date)
    doacoes_map = dict(q_doacoes.group_by(models.RecebimentoDoacao.id_parceiro).all())

    # 2. Totais de Compras por Parceiro
    q_compras = db.query(models.Compra.id_parceiro, func.sum(models.Compra.quantidade)).filter(models.Compra.status == "Concluída")
    if start_date: q_compras = q_compras.filter(models.Compra.data_compra >= start_date)
    if end_date: q_compras = q_compras.filter(models.Compra.data_compra <= end_date)
    compras_map = dict(q_compras.group_by(models.Compra.id_parceiro).all())

    # 3. Busca os Parceiros que tiveram alguma movimentação
    ids_ativos = set(doacoes_map.keys()) | set(compras_map.keys())
    if not ids_ativos: return []
    
    parceiros = db.query(models.Parceiro).options(joinedload(models.Parceiro.tipo_info)).filter(models.Parceiro.id.in_(ids_ativos)).all()

    report = []
    for p in parceiros:
        report.append(schemas.ReportPorParceiroItem(
            nome=p.nome,
            tipo_parceiro=p.tipo_info.nome,
            quantidade_recebida=doacoes_map.get(p.id, 0.0),
            quantidade_comprada=compras_map.get(p.id, 0.0)
        ))
    
    # Ordena por total movimentado (decrescente)
    report.sort(key=lambda x: x.quantidade_recebida + x.quantidade_comprada, reverse=True)
    return report