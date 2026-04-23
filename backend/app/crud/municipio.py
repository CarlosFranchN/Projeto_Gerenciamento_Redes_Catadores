from sqlalchemy.orm import Session
from app.models import Municipio
from app.schemas.schema_municipio import MunicipioCreate, MunicipioUpdate
from app.models import Municipio
from typing import List, Optional
import math

def get_all_municipios(db: Session, skip: int = 0, limit: int = 100 , ativo: bool = True) -> dict:
    """Busca todos os municípios com paginação para o Pydantic"""
    query = db.query(Municipio)
    
    if ativo: 
        query = query.filter(Municipio.ativo == True)
    
    total_count = query.count()
    items = query.order_by(Municipio.nome).offset(skip).limit(limit).all()

    # 🧮 Matemática da Paginação
    page = (skip // limit) + 1 if limit > 0 else 1
    pages = math.ceil(total_count / limit) if limit > 0 else 1

    return {
        "total": total_count,
        "page": page,
        "page_size": limit,
        "pages": pages,
        "items": items
    }

def get_municipio_by_id(db: Session, municipio_id: int) -> Optional[Municipio]:
    return db.query(Municipio).filter(Municipio.id == municipio_id).first()

def get_municipio_by_nome_uf(db: Session, nome: str, uf: str) -> Optional[Municipio]:
    return db.query(Municipio).filter(
        Municipio.nome == nome,
        Municipio.uf == uf
    ).first()

def create_municipio(db: Session, municipio: MunicipioCreate) -> Municipio:
    # Verifica se já existe
    existing = get_municipio_by_nome_uf(db, municipio.nome, municipio.uf)
    if existing:
        raise ValueError(f"Município {municipio.nome}/{municipio.uf} já existe")
    
    db_municipio = Municipio(**municipio.model_dump())
    db.add(db_municipio)
    db.commit()
    db.refresh(db_municipio)
    return db_municipio

def update_municipio(db: Session, municipio_id: int, municipio_update: MunicipioUpdate) -> Optional[Municipio]:
    db_municipio = get_municipio_by_id(db, municipio_id)
    if not db_municipio:
        return None
    
    update_data = municipio_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_municipio, key, value)
    
    db.commit()
    db.refresh(db_municipio)
    return db_municipio

def delete_municipio(db: Session, municipio_id: int) -> bool:
    db_municipio = get_municipio_by_id(db, municipio_id)
    if not db_municipio:
        return False
    
    db_municipio.ativo = False  # Soft delete
    db.commit()
    return True