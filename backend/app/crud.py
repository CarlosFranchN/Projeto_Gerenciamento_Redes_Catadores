from sqlalchemy.orm import Session
from app import models, schemas
from datetime import date



def get_associacao(db: Session, id_associacao: int):
    query = db.query(models.Associacao).filter(models.Associacao.id == id_associacao).first()
    return query

def get_all_associacoes(db: Session, skip: int = 0 , limit: int = 100):
    query = db.query(models.Associacao).offset(skip).limit(limit).all()
    return query

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

# =================================================
# Funções para Materiais

# =================================================

def get_material(db: Session, id_material: int):
    query = db.query(models.Material).filter(models.Material.id == id_material).first()
    return query

def get_all_material(db: Session, skip: int = 0 , limit: int = 100):
    query = db.query(models.Material).offset(skip).limit(limit).all()
    return query

def create_material(db: Session, material: schemas.MaterialCreate):
    db_material = models.Material(
        nome = material.nome,
        unidade_medida = material.unidade_medida
    )
    db.add(db_material)
    
    db.flush()
    db.refresh(db_material)
    
    codigo_gerado = f"MAT-{db_material.id:04d}"
    db_material.codigo_material = codigo_gerado
    
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
    

    vendas_de_hoje = db.query(models.Venda).filter(models.Venda.codigo.startswith(prefixo_codigo)).count()
    sequencial = vendas_de_hoje + 1
    codigo_gerado = f"{prefixo_codigo}{sequencial:03d}" # Ex: V-20250925-001
    
    
    db_entrada = models.EntradaMaterial(**entrada.dict(), codigo_lote = codigo_gerado)
    # db_entrada.
    db.add(db_entrada)
    db.commit()
    db.refresh(db_entrada)
    return db_entrada

def get_entradas_material(db: Session, skip: int = 0, limit: int = 100):
    """Lista todas as entradas de material."""
    return db.query(models.EntradaMaterial).offset(skip).limit(limit).all()

# =================================================================
# Funções CRUD para Venda e ItemVenda
# =================================================================

def create_venda(db: Session, venda: schemas.VendaCreate):
    """Cria uma nova venda, seus itens, e gera um código único para a venda."""
    
    # Lógica para gerar o código da venda
    hoje = date.today()
    prefixo_codigo = f"V-{hoje.strftime('%Y%m%d')}-"
    

    vendas_de_hoje = db.query(models.Venda).filter(models.Venda.codigo.startswith(prefixo_codigo)).count()
    sequencial = vendas_de_hoje + 1
    codigo_gerado = f"{prefixo_codigo}{sequencial:03d}" # Ex: V-20250925-001

    # Cria o objeto principal da Venda, agora já com o código
    db_venda = models.Venda(
        id_comprador=venda.id_comprador,
        codigo=codigo_gerado
    )
    db.add(db_venda)

    # O resto da lógica para salvar os itens continua a mesma
    for item_schema in venda.itens:
        db_item = models.ItemVenda(
            **item_schema.dict(),
            venda=db_venda
        )
        db.add(db_item)

    db.commit()
    db.refresh(db_venda)
    return db_venda

def get_venda(db: Session, venda_id: int):
    """Busca uma única venda pelo seu ID, incluindo seus itens."""
    return db.query(models.Venda).filter(models.Venda.id == venda_id).first()

def get_vendas(db: Session, skip: int = 0, limit: int = 100):
    """Lista todas as vendas."""
    return db.query(models.Venda).offset(skip).limit(limit).all()