from sqlalchemy.orm import Session
from app.models import AuditLog
from app.schemas.schema_audit import AuditLogCreate
from typing import List, Optional

def create_log(
    db: Session,
    acao: str,
    tabela_afetada: str = None,
    registro_id: int = None,
    dados_antigos: dict = None,
    dados_novos: dict = None,
    usuario_id: int = None,
    ip_address: str = None
):
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
    return (
        db.query(AuditLog)
        .filter(AuditLog.tabela_afetada == tabela_afetada)
        .order_by(AuditLog.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )