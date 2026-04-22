from sqlalchemy.orm import Session
from app.models import AuditLog
from app.schemas.schema_audit import AuditLogCreate
from typing import List, Optional, Dict, Any

def create_log(
    db: Session,
    acao: str,
    tabela_afetada: str = None,
    registro_id: int = None,
    dados_antigos: Dict = None,
    dados_novos: Dict = None,
    usuario_id: int = None,
    ip_address: str = None
) -> AuditLog:
    """Criar novo log de auditoria"""
    db_log = AuditLog(
        usuario_id=usuario_id,
        acao=acao,
        tabela_afetada=tabela_afetada,
        registro_id=registro_id,
        dados_antigos=dados_antigos,
        dados_novos=dados_novos,
        ip_address=ip_address
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_logs_by_usuario(
    db: Session,
    usuario_id: int,
    skip: int = 0,
    limit: int = 50
) -> List[AuditLog]:
    """Buscar logs por usuário"""
    return (
        db.query(AuditLog)
        .filter(AuditLog.usuario_id == usuario_id)
        .order_by(AuditLog.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_logs_by_tabela(
    db: Session,
    tabela_afetada: str,
    skip: int = 0,
    limit: int = 50
) -> List[AuditLog]:
    """Buscar logs por tabela afetada"""
    return (
        db.query(AuditLog)
        .filter(AuditLog.tabela_afetada == tabela_afetada)
        .order_by(AuditLog.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_logs_by_periodo(
    db: Session,
    data_inicio: str,
    data_fim: str,
    skip: int = 0,
    limit: int = 50
) -> List[AuditLog]:
    """Buscar logs por período"""
    from datetime import datetime
    inicio = datetime.fromisoformat(data_inicio)
    fim = datetime.fromisoformat(data_fim)
    
    return (
        db.query(AuditLog)
        .filter(
            AuditLog.created_at >= inicio,
            AuditLog.created_at <= fim
        )
        .order_by(AuditLog.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )