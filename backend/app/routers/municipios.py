from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app import crud, schemas, models
from app.dependencies import get_current_user

# 🔥 IMPORTA A SUA FUNÇÃO DE LOG CENTRALIZADA
from app.crud.audit import create_log

router = APIRouter(
    prefix="/api/municipios",
    tags=["Municípios"]
)

@router.get("/", response_model=schemas.MunicipioPaginated)
def read_municipios(
    skip: int = 0,
    limit: int = 100,
    ativo: Optional[bool] = True,
    db: Session = Depends(get_db)
):
    """Listar todos os municípios (público)"""
    return crud.get_all_municipios(db, skip=skip, limit=limit, ativo=ativo)


@router.get("/{municipio_id}", response_model=schemas.MunicipioResponse)
def read_municipio(
    grupo_id: int, # Mantendo consistente com a assinatura interna se necessário, ou corrigindo para municipio_id
    municipio_id: int,
    db: Session = Depends(get_db)
):
    """Obter município por ID (público)"""
    db_municipio = crud.get_municipio_by_id(db, municipio_id)
    if not db_municipio:
        raise HTTPException(status_code=404, detail="Município não encontrado")
    return db_municipio


@router.post("/", response_model=schemas.MunicipioResponse, status_code=status.HTTP_201_CREATED)
def create_municipio(
    municipio: schemas.MunicipioCreate,
    request: Request, # 🔥 Injetado para pegar o IP real
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Criar novo município (requer autenticação)"""
    try:
        db_municipio = crud.create_municipio(db, municipio=municipio)
        
        # 🔥 AUDITORIA: Registro novo criado com sucesso
        client_ip = request.client.host if request.client else None
        create_log(
            db=db,
            acao="INSERT",
            tabela_afetada="municipios",
            registro_id=db_municipio.id,
            dados_antigos=None,
            dados_novos=schemas.MunicipioResponse.from_orm(db_municipio).dict(),
            usuario_id=current_user.id,
            ip_address=client_ip
        )
        
        return db_municipio
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{municipio_id}", response_model=schemas.MunicipioResponse)
def update_municipio(
    municipio_id: int,
    municipio_update: schemas.MunicipioUpdate,
    request: Request, # 🔥 Injetado para pegar o IP real
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Atualizar município (requer autenticação)"""
    # 1. Busca o estado atual do município ANTES da edição
    muni_antes = crud.get_municipio_by_id(db, municipio_id)
    if not muni_antes:
        raise HTTPException(status_code=404, detail="Município não encontrado")
        
    dados_antigos = schemas.MunicipioResponse.from_orm(muni_antes).dict()

    # 2. Executa a atualização real no banco
    db_municipio = crud.update_municipio(db, municipio_id=municipio_id, municipio_update=municipio_update)
    
    # 3. Mapeia o estado final e captura o IP
    dados_novos = schemas.MunicipioResponse.from_orm(db_municipio).dict()
    client_ip = request.client.host if request.client else None

    # 4. 🔥 AUDITORIA: Grava o log de alteração
    create_log(
        db=db,
        acao="UPDATE",
        tabela_afetada="municipios",
        registro_id=municipio_id,
        dados_antigos=dados_antigos,
        dados_novos=dados_novos,
        usuario_id=current_user.id,
        ip_address=client_ip
    )

    return db_municipio


@router.delete("/{municipio_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_municipio(
    municipio_id: int,
    request: Request, # 🔥 Injetado para pegar o IP real
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Soft delete - marca como inativo (requer autenticação)"""
    # 1. Busca o estado do município antes do soft delete
    muni_antes = crud.get_municipio_by_id(db, municipio_id)
    if not muni_antes:
        raise HTTPException(status_code=404, detail="Município não encontrado")
        
    dados_antigos = schemas.MunicipioResponse.from_orm(muni_antes).dict()

    # 2. Executa o Soft Delete
    success = crud.delete_municipio(db, municipio_id=municipio_id)
    if not success:
        raise HTTPException(status_code=404, detail="Município não encontrado")
        
    # 3. Busca o estado final pós-soft-delete para auditoria
    muni_depois = crud.get_municipio_by_id(db, municipio_id)
    dados_novos = schemas.MunicipioResponse.from_orm(muni_depois).dict() if muni_depois else None
    
    client_ip = request.client.host if request.client else None

    # 4. 🔥 AUDITORIA: Grava o log de Soft Delete
    create_log(
        db=db,
        acao="DELETE",
        tabela_afetada="municipios",
        registro_id=municipio_id,
        dados_antigos=dados_antigos,
        dados_novos=dados_novos,
        usuario_id=current_user.id,
        ip_address=client_ip
    )
    
    return None