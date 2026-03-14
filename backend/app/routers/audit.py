from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models import AuditLog, Usuario
from app.schemas.schema_audit import AuditLogResponse, AuditLogCreate
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/audit", tags=["Auditoria"])

@router.get("/logs", response_model=List[AuditLogResponse])
def listar_logs(
    skip: int = 0,
    limit: int = 50,
    usuario_id: Optional[int] = None,
    tabela_afetada: Optional[str] = None,
    acao: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Listar logs de auditoria (apenas admin)
    """
    # Verifica se é admin
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem acessar logs de auditoria"
        )
    
    query = db.query(AuditLog)
    
    if usuario_id:
        query = query.filter(AuditLog.usuario_id == usuario_id)
    if tabela_afetada:
        query = query.filter(AuditLog.tabela_afetada == tabela_afetada)
    if acao:
        query = query.filter(AuditLog.acao == acao)
    
    logs = query.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()
    return logs


@router.get("/logs/{log_id}", response_model=AuditLogResponse)
def obter_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obter um log específico
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem acessar logs de auditoria"
        )
    
    log = db.query(AuditLog).filter(AuditLog.id == log_id).first()
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log não encontrado"
        )
    
    return log


@router.post("/logs", response_model=AuditLogResponse, status_code=status.HTTP_201_CREATED)
def criar_log(
    log_data: AuditLogCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Criar um novo log de auditoria (uso interno do sistema)
    """
    db_log = AuditLog(
        usuario_id=log_data.usuario_id or current_user.id,
        acao=log_data.acao,
        tabela_afetada=log_data.tabela_afetada,
        registro_id=log_data.registro_id,
        dados_antigos=log_data.dados_antigos,
        dados_novos=log_data.dados_novos,
        ip_address=log_data.ip_address
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log