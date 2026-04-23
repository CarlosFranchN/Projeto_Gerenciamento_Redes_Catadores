# from sqlalchemy.orm import Session
# from sqlalchemy import func
# from typing import List, Optional, Tuple
# import math

# from app import models, schemas

# # =============== CREATE ===============
# def create_afiliado(db: Session, afiliado: schemas.AfiliadoCreate) -> models.Afiliado:
#     """Criar novo afiliado"""
#     # Verifica se CPF já existe (se foi informado)
#     if afiliado.cpf:
#         existing = db.query(models.Afiliado).filter(
#             models.Afiliado.cpf == afiliado.cpf,
#             models.Afiliado.ativo == True
#         ).first()
#         if existing:
#             raise ValueError("CPF já cadastrado")
    
#     # Cria o afiliado (agora ligado direto à Associação, sem precisar de Parceiro!)
#     db_afiliado = models.Afiliado(
#         nome=afiliado.nome,
#         cpf=afiliado.cpf,
#         funcao=afiliado.funcao,
#         data_filiacao=afiliado.data_filiacao,
#         associacao_id=afiliado.associacao_id,
#         ativo=True
#     )
    
#     db.add(db_afiliado)
#     db.commit()
#     db.refresh(db_afiliado)
    
#     return db_afiliado

# # =============== READ (SINGLE) ===============
# def get_afiliado(db: Session, afiliado_id: int) -> Optional[models.Afiliado]:
#     """Obter afiliado por ID"""
#     return db.query(models.Afiliado).filter(models.Afiliado.id == afiliado_id).first()

# def get_afiliado_by_cpf(db: Session, cpf: str) -> Optional[models.Afiliado]:
#     """Obter afiliado por CPF"""
#     return db.query(models.Afiliado).filter(models.Afiliado.cpf == cpf).first()

# # =============== READ (LIST) ===============
# def get_afiliados(
#     db: Session,
#     skip: int = 0,
#     limit: int = 100,
#     associacao_id: Optional[int] = None,
#     ativo: Optional[bool] = None,
#     search: Optional[str] = None
# ) -> dict:
#     """
#     Listar afiliados com filtros e a paginação completa exigida pelo Schema do FastAPI
#     """
#     query = db.query(models.Afiliado)
    
#     if associacao_id is not None:
#         query = query.filter(models.Afiliado.associacao_id == associacao_id)
    
#     if ativo is not None:
#         query = query.filter(models.Afiliado.ativo == ativo)
    
#     if search:
#         query = query.filter(models.Afiliado.nome.ilike(f"%{search}%"))
    
#     total_count = query.count()
#     items = query.offset(skip).limit(limit).all()
    
#     # 🧮 Matemática da Paginação
#     page = (skip // limit) + 1 if limit > 0 else 1
#     pages = math.ceil(total_count / limit) if limit > 0 else 1

#     return {
#         "total": total_count,
#         "page": page,
#         "page_size": limit,
#         "pages": pages,
#         "items": items
#     }

# def get_afiliados_by_associacao(
#     db: Session,
#     associacao_id: int,
#     skip: int = 0,
#     limit: int = 100
# ) -> dict:
#     """Listar afiliados de uma associação específica"""
#     return get_afiliados(db, skip=skip, limit=limit, associacao_id=associacao_id)

# # =============== UPDATE ===============
# def update_afiliado(
#     db: Session,
#     afiliado_id: int,
#     afiliado: schemas.AfiliadoUpdate
# ) -> Optional[models.Afiliado]:
#     """Atualizar dados de um afiliado"""
#     db_afiliado = get_afiliado(db, afiliado_id)
    
#     if not db_afiliado:
#         return None
    
#     if afiliado.cpf and afiliado.cpf != db_afiliado.cpf:
#         existing = db.query(models.Afiliado).filter(
#             models.Afiliado.cpf == afiliado.cpf,
#             models.Afiliado.id != afiliado_id,
#             models.Afiliado.ativo == True
#         ).first()
#         if existing:
#             raise ValueError("CPF já cadastrado")
    
#     # ✅ Atualizado para o padrão do Pydantic v2
#     update_data = afiliado.model_dump(exclude_unset=True)
#     for field, value in update_data.items():
#         setattr(db_afiliado, field, value)
    
#     db.commit()
#     db.refresh(db_afiliado)
    
#     return db_afiliado

# # =============== DELETE (SOFT) ===============
# def delete_afiliado(db: Session, afiliado_id: int) -> bool:
#     """Desativar afiliado (soft delete)"""
#     db_afiliado = get_afiliado(db, afiliado_id)
    
#     if not db_afiliado:
#         return False
    
#     db_afiliado.ativo = False
#     db.commit()
    
#     return True

# def hard_delete_afiliado(db: Session, afiliado_id: int) -> bool:
#     """Excluir afiliado permanentemente (use com cautela!)"""
#     db_afiliado = get_afiliado(db, afiliado_id)
    
#     if not db_afiliado:
#         return False
    
#     db.delete(db_afiliado)
#     db.commit()
    
#     return True

# # =============== ESTATÍSTICAS ===============
# def get_afiliados_stats(db: Session, associacao_id: Optional[int] = None) -> dict:
#     """Obter estatísticas de afiliados"""
#     query = db.query(models.Afiliado)
    
#     if associacao_id:
#         query = query.filter(models.Afiliado.associacao_id == associacao_id)
    
#     total = query.count()
#     ativos = query.filter(models.Afiliado.ativo == True).count()
#     inativos = query.filter(models.Afiliado.ativo == False).count()
    
#     por_funcao = db.query(
#         models.Afiliado.funcao,
#         func.count(models.Afiliado.id).label('count')
#     ).filter(
#         models.Afiliado.ativo == True
#     )
    
#     if associacao_id:
#         por_funcao = por_funcao.filter(models.Afiliado.associacao_id == associacao_id)
    
#     por_funcao = por_funcao.group_by(models.Afiliado.funcao).all()
    
#     return {
#         "total": total,
#         "ativos": ativos,
#         "inativos": inativos,
#         "por_funcao": [{"funcao": f.funcao or "Não informada", "count": f.count} for f in por_funcao]
#     }