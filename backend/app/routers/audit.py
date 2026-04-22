from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app import models
from .. import crud, schemas
from app.database import get_db
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/api/audit",
    tags=["Auditoria"]
)

@router.get("/logs", response_model=List[schemas.AuditLogResponse])
def read_logs(
    skip: int = 0,
    limit: int = 50,
    usuario_id: Optional[int] = None,
    tabela_afetada: Optional[str] = None,
    acao: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Listar logs de auditoria (apenas admin)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Apenas administradores")
    
    # Implementação simplificada - você pode expandir com filtros
    logs = db.query(models.AuditLog)
    if usuario_id:
        logs = logs.filter(models.AuditLog.usuario_id == usuario_id)
    if tabela_afetada:
        logs = logs.filter(models.AuditLog.tabela_afetada == tabela_afetada)
    if acao:
        logs = logs.filter(models.AuditLog.acao == acao)
    
    return logs.order_by(models.AuditLog.created_at.desc()).offset(skip).limit(limit).all()

@router.get("/logs/{log_id}", response_model=schemas.AuditLogResponse)
def read_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Obter log específico (apenas admin)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Apenas administradores")
    
    log = db.query(models.AuditLog).filter(models.AuditLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log não encontrado")
    return log