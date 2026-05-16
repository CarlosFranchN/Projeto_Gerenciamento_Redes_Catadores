from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app import crud, schemas, models
from app.dependencies import get_current_user

# 🔥 IMPORTA A SUA FUNÇÃO DE LOG CENTRALIZADA
from app.crud.audit import create_log

router = APIRouter(
    prefix="/api/grupos",
    tags=["Grupos"]
)

@router.get("/", response_model=schemas.GrupoPaginated)
def read_grupos(
    skip: int = 0,
    limit: int = 100,
    ativo: Optional[bool] = True,
    db: Session = Depends(get_db)
):
    """Listar todos os grupos (público)"""
    return crud.get_all_grupos(db, skip=skip, limit=limit, ativo=ativo)


@router.get("/{grupo_id}", response_model=schemas.GrupoResponse)
def read_grupo(
    grupo_id: int,
    db: Session = Depends(get_db)
):
    """Obter grupo por ID (público)"""
    db_grupo = crud.get_grupo_by_id(db, grupo_id)
    if not db_grupo:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    return db_grupo


@router.post("/", response_model=schemas.GrupoResponse, status_code=status.HTTP_201_CREATED)
def create_grupo(
    grupo: schemas.GrupoCreate,
    request: Request, # 🔥 Injetado para pegar o IP
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Criar novo grupo (requer autenticação)"""
    # 1. Executa a criação normal do grupo
    db_grupo = crud.create_grupo(db, grupo=grupo)
    
    # 2. Captura o IP e grava o Log de Criação
    client_ip = request.client.host if request.client else None
    
    create_log(
        db=db,
        acao="INSERT",
        tabela_afetada="grupos",
        registro_id=db_grupo.id,
        dados_antigos=None, # Registro novo não tem passado
        dados_novos=schemas.GrupoResponse.from_orm(db_grupo).dict(), # Converte o modelo salvo para dict
        usuario_id=current_user.id,
        ip_address=client_ip
    )
    
    return db_grupo


@router.put("/{grupo_id}", response_model=schemas.GrupoResponse)
def update_grupo(
    grupo_id: int,
    grupo_update: schemas.GrupoUpdate,
    request: Request, # 🔥 Injetado para pegar o IP
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Atualizar grupo (requer autenticação)"""
    # 1. Busca o estado atual do grupo ANTES da edição para salvar na auditoria
    grupo_antes = crud.get_grupo_by_id(db, grupo_id)
    if not grupo_antes:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
        
    dados_antigos = schemas.GrupoResponse.from_orm(grupo_antes).dict()

    # 2. Executa a atualização real no banco
    db_grupo = crud.update_grupo(db, grupo_id=grupo_id, grupo_update=grupo_update)
    
    # 3. Mapeia o estado final e o IP
    dados_novos = schemas.GrupoResponse.from_orm(db_grupo).dict()
    client_ip = request.client.host if request.client else None

    # 4. Grava o Log de Alteração
    create_log(
        db=db,
        acao="UPDATE",
        tabela_afetada="grupos",
        registro_id=grupo_id,
        dados_antigos=dados_antigos,
        dados_novos=dados_novos,
        usuario_id=current_user.id,
        ip_address=client_ip
    )

    return db_grupo


@router.delete("/{grupo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grupo(
    grupo_id: int,
    request: Request, # 🔥 Injetado para pegar o IP
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Soft delete - marca como inativo (requer autenticação)"""
    # 1. Busca o estado do grupo antes de desativá-lo
    grupo_antes = crud.get_grupo_by_id(db, grupo_id)
    if not grupo_antes:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
        
    dados_antigos = schemas.GrupoResponse.from_orm(grupo_antes).dict()

    # 2. Executa o Soft Delete no banco (muda ativo para False)
    success = crud.delete_grupo(db, grupo_id=grupo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    
    # 3. Busca o estado final pós-soft-delete para auditoria limpa
    grupo_depois = crud.get_grupo_by_id(db, grupo_id)
    dados_novos = schemas.GrupoResponse.from_orm(grupo_depois).dict() if grupo_depois else None
    
    client_ip = request.client.host if request.client else None

    # 4. Grava o Log de Desativação (Soft Delete)
    create_log(
        db=db,
        acao="DELETE", # Ou "SOFT_DELETE", mas mantendo o padrão da sua constraint de tamanho
        tabela_afetada="grupos",
        registro_id=grupo_id,
        dados_antigos=dados_antigos,
        dados_novos=dados_novos,
        usuario_id=current_user.id,
        ip_address=client_ip
    )
    
    return None