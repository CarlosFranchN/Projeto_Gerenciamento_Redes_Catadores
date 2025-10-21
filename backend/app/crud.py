from sqlalchemy.orm import Session,joinedload
from app import models, schemas
from datetime import date
from sqlalchemy import func
from typing import List


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
        .scalar() 
    ) or 0.0 

    total_vendido = (
        db.query(func.sum(models.ItemVenda.quantidade_vendida))
        .filter(models.ItemVenda.id_material == material_id)
        .scalar()
    ) or 0.0

    estoque_atual = total_entradas - total_vendido
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
        .offset(skip)
        .limit(limit)
        .all()
    )

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
        nome_comprador=venda.nome_comprador,
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
    """Lista todas as vendas."""
    return db.query(models.Venda).offset(skip).limit(limit).all()