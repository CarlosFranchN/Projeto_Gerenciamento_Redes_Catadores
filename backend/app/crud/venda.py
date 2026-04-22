from sqlalchemy.orm import Session,joinedload

from datetime import date
from sqlalchemy import func,and_
from typing import List,Optional
from sqlalchemy.exc import IntegrityError
import time
import random
# from .material import calcular_estoque_material
from .. import schemas,models, crud

MAX_RETRIES = 3

def create_venda(db: Session, venda: schemas.VendaCreate):
    ids_materiais_para_buscar = {item.id_material for item in venda.itens}
    materiais_db = db.query(models.Material).filter(models.Material.id.in_(ids_materiais_para_buscar)).all()
    materiais_map = {m.id: m for m in materiais_db}

    for item_venda in venda.itens:
        if item_venda.id_material not in materiais_map:
             raise ValueError(f"Material com ID {item_venda.id_material} não encontrado.")
        estoque_disponivel = crud.calcular_estoque_material(db, material_id=item_venda.id_material)
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
                id_comprador=venda.id_comprador, 
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
            
            db.commit() 
            
            db.refresh(db_venda)
            # 1. Calcula o valor total da venda que acabou de ser criada
            total_recebido = sum(
                item.quantidade_vendida * item.valor_unitario for item in db_venda.itens
            )
            
            # 2. Prepara a transação de ENTRADA
            transacao_entrada = schemas.TransacaoCreate(
                tipo="ENTRADA",
                valor=total_recebido,
                descricao=f"Recebimento referente à Venda Cód: {db_venda.codigo}",
                id_venda_associada=db_venda.id # Linka a transação à venda
            )
            
            # 3. Salva a transação
            crud.create_transacao(db, transacao_entrada)
            return db_venda 

        except IntegrityError as e:
            db.rollback() 
            
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


    raise RuntimeError("Falha ao criar venda após múltiplas tentativas.")

def get_venda(db: Session, venda_id: int):
    """Busca uma única venda pelo seu ID, incluindo seus itens."""
    return (
        db.query(models.Venda)
        .options(
            joinedload(models.Venda.itens).joinedload(models.ItemVenda.material),
            joinedload(models.Venda.comprador) # 👈 Carrega dados do Comprador
        )
        .filter(models.Venda.id == venda_id)
        .first()
    )

def get_vendas(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    id_comprador: Optional[int] = None, 
    id_material: Optional[int] = None
) -> dict:
    query = db.query(models.Venda).filter(models.Venda.concluida == True)

    if id_material:
        query = query.join(models.ItemVenda).filter(models.ItemVenda.id_material == id_material).distinct()
    if id_comprador: 
        query = query.filter(models.Venda.id_comprador == id_comprador)
    if data_inicio:
        query = query.filter(models.Venda.data_venda >= data_inicio)
    if data_fim:
        query = query.filter(models.Venda.data_venda <= data_fim)

    total_count = query.count()

    items = (
            query
            .options(
                joinedload(models.Venda.itens).joinedload(models.ItemVenda.material),
                joinedload(models.Venda.comprador) # 👈 Carrega o objeto Comprador na resposta
            )
            .order_by(models.Venda.data_venda.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    return {"total_count": total_count, "items": items}

def cancel_venda(db: Session, venda_id: int):
    """Marca uma venda como não concluída/cancelada (concluida=False)."""
    db_venda = get_venda(db, venda_id=venda_id) 
    if not db_venda: 
        return None 


    if not db_venda.concluida: 
        return db_venda 


    db_venda.concluida = False 
    total_estorno = sum(
        item.quantidade_vendida * item.valor_unitario for item in db_venda.itens
    )

    transacao_estorno = schemas.TransacaoCreate(
        tipo="SAIDA",
        valor=total_estorno,
        descricao=f"Estorno referente ao Cancelamento da Venda Cód: {db_venda.codigo}",
        id_venda_associada=db_venda.id 
    )
    

    crud.create_transacao(db, transacao_estorno)
    db.commit()
    db.refresh(db_venda)
    return db_venda
