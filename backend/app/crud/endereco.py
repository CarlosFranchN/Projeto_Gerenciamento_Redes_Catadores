from sqlalchemy.orm import Session
from app.models import EnderecosCache
from datetime import datetime, timedelta
from typing import Optional

def get_endereco_by_cnpj(
    db: Session, 
    cnpj: str
) -> Optional[EnderecosCache]:
    """Buscar endereço cacheado por CNPJ"""
    cnpj_limpo = cnpj.replace('/\D/g', '')
    return db.query(EnderecosCache).filter(
        EnderecosCache.cnpj == cnpj_limpo
    ).first()

def is_cache_valido(
    endereco: EnderecosCache
) -> bool:
    """Verificar se cache ainda é válido (não expirou)"""
    if not endereco or not endereco.expires_at:
        return False
    return datetime.utcnow() < endereco.expires_at

def create_or_update_endereco(
    db: Session,
    cnpj: str,
    logradouro: str = None,
    numero: str = None,
    complemento: str = None,
    bairro: str = None,
    cidade: str = None,
    uf: str = None,
    validade_dias: int = 30
) -> EnderecosCache:
    """Criar ou atualizar endereço em cache"""
    cnpj_limpo = cnpj.replace('/\D/g', '')
    
    db_endereco = db.query(EnderecosCache).filter(
        EnderecosCache.cnpj == cnpj_limpo
    ).first()
    
    if db_endereco:
        # Atualiza existente
        db_endereco.logradouro = logradouro
        db_endereco.numero = numero
        db_endereco.complemento = complemento
        db_endereco.bairro = bairro
        db_endereco.cidade = cidade
        db_endereco.uf = uf
        db_endereco.consulted_at = datetime.utcnow()
        db_endereco.expires_at = datetime.utcnow() + timedelta(days=validade_dias)
    else:
        # Cria novo
        db_endereco = EnderecosCache(
            cnpj=cnpj_limpo,
            logradouro=logradouro,
            numero=numero,
            complemento=complemento,
            bairro=bairro,
            cidade=cidade,
            uf=uf,
            expires_at=datetime.utcnow() + timedelta(days=validade_dias)
        )
        db.add(db_endereco)
    
    db.commit()
    db.refresh(db_endereco)
    return db_endereco