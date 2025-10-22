from sqlalchemy.orm import Session,joinedload
from app import models, schemas
from datetime import date
from sqlalchemy import func,and_
from typing import List,Optional
from sqlalchemy.exc import IntegrityError
import time
import random
from .material import calcular_estoque_material

MAX_RETRIES = 3

def create_venda(db: Session, venda: schemas.VendaCreate):
    """Cria uma nova venda, seus itens, e gera um código único para a venda,
       VALIDANDO o estoque e usando LÓGICA DE RETENTATIVA para o código."""

    # --- Bloco de Validação de Estoque (permanece igual) ---
    ids_materiais_para_buscar = {item.id_material for item in venda.itens}
    materiais_db = db.query(models.Material).filter(models.Material.id.in_(ids_materiais_para_buscar)).all()
    materiais_map = {m.id: m for m in materiais_db}

    for item_venda in venda.itens:
        if item_venda.id_material not in materiais_map:
             raise ValueError(f"Material com ID {item_venda.id_material} não encontrado.")
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

    # --- Lógica de Criação com Retentativa ---
    retry_count = 0
    db_venda = None 

    while retry_count < MAX_RETRIES:
        hoje = date.today()
        prefixo_codigo = f"V-{hoje.strftime('%Y%m%d')}-"
        vendas_de_hoje = db.query(models.Venda).filter(models.Venda.codigo.startswith(prefixo_codigo)).count()
        sequencial = vendas_de_hoje + 1
        codigo_gerado = f"{prefixo_codigo}{sequencial:03d}"
        
        try:
            db_venda = models.Venda(
                # CORREÇÃO 1: Usar o nome correto do campo do modelo/schema
                comprador=venda.comprador, 
                # CORREÇÃO 2: Definir explicitamente como True ao criar
                concluida = True, 
                codigo=codigo_gerado
            )
            db.add(db_venda)

            itens_obj_list = [] 
            for item_schema in venda.itens:
                db_item = models.ItemVenda(
                    id_material=item_schema.id_material,
                    quantidade_vendida=item_schema.quantidade_vendida,
                    valor_unitario=item_schema.valor_unitario,
                    venda=db_venda 
                )
                db.add(db_item)
                itens_obj_list.append(db_item)
            
            db.commit() # Tenta salvar
            
            db.refresh(db_venda) # Sucesso! Atualiza o objeto principal
            # (Refresh nos itens é opcional aqui, Pydantic/SQLAlchemy devem carregar via relationship)
            return db_venda # Retorna sucesso

        except IntegrityError as e:
            db.rollback() # Desfaz a tentativa
            
            original_error_msg = str(getattr(e, 'orig', e)).lower() 
            is_unique_violation = "unique constraint" in original_error_msg or "duplicar valor da chave" in original_error_msg
            is_codigo_index = "ix_vendas_codigo" in original_error_msg 

            if is_unique_violation and is_codigo_index:
                retry_count += 1
                print(f"Código de venda {codigo_gerado} duplicado. Retentativa {retry_count}/{MAX_RETRIES}...")
                if retry_count >= MAX_RETRIES:
                    print(f"Máximo de retentativas ({MAX_RETRIES}) atingido para gerar código de venda.")
                    raise ValueError("Não foi possível gerar um código de venda único. Tente novamente.") from e
                time.sleep(random.uniform(0.05, 0.15)) 
                # Continua para a próxima iteração do loop
            else:
                print(f"Erro de integridade inesperado ao salvar venda: {e}")
                raise ValueError(f"Erro de integridade ao salvar venda: {e}") from e
                
        except Exception as e:
            db.rollback()
            print(f"Erro inesperado durante create_venda: {e}")
            raise ValueError(f"Erro inesperado ao salvar venda: {e}") from e

    # Se saiu do loop sem sucesso
    raise RuntimeError("Falha ao criar venda após múltiplas tentativas.")

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
