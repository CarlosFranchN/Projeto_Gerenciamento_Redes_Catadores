from sqlalchemy.orm import Session,joinedload
from app import models, schemas
from datetime import date
from sqlalchemy import func,and_
from typing import List,Optional


def get_associacao(db: Session, id_associacao: int):
    query = db.query(models.Associacao).filter(models.Associacao.id == id_associacao).first()
    return query

def get_all_associacoes(db: Session, skip: int = 0, limit: int = 100):
    """Lista todas as associações ATIVAS com paginação."""
    return (
        db.query(models.Associacao)
        .filter(models.Associacao.ativo == True) # 👈 GARANTA QUE ESTE FILTRO EXISTE
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_associacao(db: Session, associacao: schemas.AssociacaoCreate):
    db_associacao = models.Associacao(
        nome = associacao.nome,
        lider = associacao.lider,
        telefone = associacao.telefone,
        cnpj = associacao.cnpj
    )
    db.add(db_associacao)
    db.commit()
    db.refresh(db_associacao)
    return db_associacao

def update_associacao(db: Session, associacao_id: int, associacao_update: schemas.AssociacaoUpdate):
    """Atualiza os dados de uma associação existente."""

    db_associacao = get_associacao(db, id_associacao=associacao_id)

    if not db_associacao:
        return None

    # Atualiza os campos usando os dados do schema
    update_data = associacao_update.dict(exclude_unset=True) 
    for key, value in update_data.items():
        setattr(db_associacao, key, value) 

    db.commit()
    db.refresh(db_associacao)
    return db_associacao

def delete_associacao(db: Session, associacao_id: int):
    """Marca uma associação como inativa."""
    db_associacao = get_associacao(db, id_associacao=associacao_id)
    if not db_associacao: return None
    if not db_associacao.ativo: return db_associacao # Já inativo

    db_associacao.ativo = False # <--- USE 'ativo' e 'False'
    
    db.commit()
    db.refresh(db_associacao)
    return db_associacao
# =================================================
# Funções para Materiais

# =================================================

def calcular_estoque_material(db: Session, material_id: int) -> float:
    """Calcula o estoque atual de um material específico."""
    
    total_entradas = (
        db.query(func.sum(models.EntradaMaterial.quantidade))
        .filter(models.EntradaMaterial.id_material == material_id)
        .filter(models.EntradaMaterial.status == "Confirmada")
        .scalar() 
    ) or 0.0 

    total_vendido = (
        db.query(func.sum(models.ItemVenda.quantidade_vendida))
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


# =================================================================
# Funções CRUD para Comprador
# =================================================================

def get_comprador(db: Session, comprador_id: int):
    """Busca um único comprador pelo seu ID."""
    return db.query(models.Comprador).filter(models.Comprador.id == comprador_id).first()

def get_compradores(db: Session, skip: int = 0, limit: int = 100):
    """Lista todos os compradores com paginação."""
    return db.query(models.Comprador).offset(skip).limit(limit).all()

def create_comprador(db: Session, comprador: schemas.CompradorCreate):
    """Cria um novo comprador no banco de dados."""
    db_comprador = models.Comprador(**comprador.dict())
    db.add(db_comprador)
    db.commit()
    db.refresh(db_comprador)
    return db_comprador

# =================================================================
# Funções CRUD para EntradaMaterial
# =================================================================

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

def get_entradas_material(db: Session, skip: int = 0, limit: int = 100):
    """Lista todas as entradas de material."""
    # return db.query(models.EntradaMaterial).offset(skip).limit(limit).all()
    return (
        db.query(models.EntradaMaterial)
        .options(
            joinedload(models.EntradaMaterial.material), 
            joinedload(models.EntradaMaterial.associacao)
        )
        .filter(models.EntradaMaterial.status == "Confirmada")
        .offset(skip)
        .limit(limit)
        .all()
    )

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
# =================================================================
# Funções CRUD para Venda e ItemVenda
# =================================================================

def create_venda(db: Session, venda: schemas.VendaCreate):
    """Cria uma nova venda, seus itens, e gera um código único para a venda,
       VALIDANDO o estoque."""

    # --- Bloco de Validação de Estoque ---
    ids_materiais_para_buscar = {item.id_material for item in venda.itens} # Pega IDs únicos
    materiais_db = db.query(models.Material).filter(models.Material.id.in_(ids_materiais_para_buscar)).all()
    materiais_map = {m.id: m for m in materiais_db} # Mapeia ID para objeto Material

    for item_venda in venda.itens:
        if item_venda.id_material not in materiais_map:
             raise ValueError(f"Material com ID {item_venda.id_material} não encontrado.") # Segurança extra

        estoque_disponivel = calcular_estoque_material(db, material_id=item_venda.id_material)

        if item_venda.quantidade_vendida <= 0:
             raise ValueError(f"Quantidade vendida para '{materiais_map[item_venda.id_material].nome}' deve ser positiva.")

        if item_venda.quantidade_vendida > estoque_disponivel:
            nome_material = materiais_map[item_venda.id_material].nome
            unidade = materiais_map[item_venda.id_material].unidade_medida
            raise ValueError(
                f"Estoque insuficiente para '{nome_material}'. "
                f"Disponível: {estoque_disponivel} {unidade}, "
                f"Tentando vender: {item_venda.quantidade_vendida} {unidade}."
            )
    # --- Fim da Validação ---

    # Se passou pela validação, continua com a criação...
    hoje = date.today()
    prefixo_codigo = f"V-{hoje.strftime('%Y%m%d')}-"
    vendas_de_hoje = db.query(models.Venda).filter(models.Venda.codigo.startswith(prefixo_codigo)).count()
    sequencial = vendas_de_hoje + 1
    codigo_gerado = f"{prefixo_codigo}{sequencial:03d}"

    db_venda = models.Venda(
        comprador=venda.comprador,
        concluida = venda.concluida,
        codigo=codigo_gerado
    )
    db.add(db_venda)

    # Adiciona os itens (já validados)
    for item_schema in venda.itens:
        db_item = models.ItemVenda(
            id_material=item_schema.id_material,
            quantidade_vendida=item_schema.quantidade_vendida,
            valor_unitario=item_schema.valor_unitario,
            venda=db_venda # Linka com a venda principal
        )
        db.add(db_item)

    try:
        db.commit() # Salva a venda e todos os itens atomicamente
        db.refresh(db_venda)
        # Recarregar os itens para que a resposta contenha os dados completos (opcional, mas bom)
        db.refresh(db_item) # Refresh no último item pode não ser suficiente para carregar todos
        # Para carregar todos os itens na resposta:
        # db.expire_all() # Força recarregar tudo da venda
        # db_venda = db.query(models.Venda).options(joinedload(models.Venda.itens)).filter(models.Venda.id == db_venda.id).one()

        return db_venda
    except Exception as e:
        db.rollback() # Desfaz TUDO se der erro no commit
        print(f"Erro no commit da venda: {e}")
        # Re-levanta a exceção original ou uma mais genérica
        raise ValueError(f"Erro ao salvar a venda no banco de dados: {e}")

def get_venda(db: Session, venda_id: int):
    """Busca uma única venda pelo seu ID, incluindo seus itens."""
    return db.query(models.Venda).filter(models.Venda.id == venda_id).first()

def get_vendas(db: Session, skip: int = 0, limit: int = 100):
    """Lista todas as vendas CONCLUÍDAS (concluida=True)."""
    return (
        db.query(models.Venda)
        # 👇 ALTERE AQUI 👇
        .filter(models.Venda.concluida == True) 
        .offset(skip)
        .limit(limit)
        .all()
    )

def cancel_venda(db: Session, venda_id: int):
    """Marca uma venda como não concluída/cancelada (concluida=False)."""
    db_venda = get_venda(db, venda_id=venda_id) # Busca a venda
    if not db_venda: 
        return None # Venda não encontrada

    # Verifica se já está cancelada (concluida == False)
    if not db_venda.concluida: 
        return db_venda # Já está cancelada

    # 👇 ALTERE AQUI 👇
    db_venda.concluida = False # Marca como não concluída/cancelada

    db.commit()
    db.refresh(db_venda)
    return db_venda


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