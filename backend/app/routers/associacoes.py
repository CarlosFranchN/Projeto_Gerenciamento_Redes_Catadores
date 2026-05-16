from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from typing import List, Optional

from app import models
from .. import crud, schemas
from app.database import get_db
from ..dependencies import get_current_user

# 🔥 IMPORTA A SUA FUNÇÃO DE LOG CENTRALIZADA
from app.crud.audit import create_log

router = APIRouter(
    prefix="/api/associacoes",
    tags=["Associações"]
)

@router.post("/", response_model=schemas.AssociacaoResponse, status_code=status.HTTP_201_CREATED)
def create_associacao(
    associacao: schemas.AssociacaoCreate,
    request: Request, # 🔥 Injetado para pegar o IP real
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Criar nova associação - versão limpa, alinhada com o models.py e auditada"""
    try:
        # Apenas passamos os dados direto para o CRUD
        nova_associacao = crud.create_associacao(db=db, associacao=associacao)
        
        # 🔥 AUDITORIA: Registro novo criado com sucesso
        client_ip = request.client.host if request.client else None
        create_log(
            db=db,
            acao="INSERT",
            tabela_afetada="associacoes",
            registro_id=nova_associacao.id,
            dados_antigos=None,
            dados_novos=schemas.AssociacaoResponse.from_orm(nova_associacao).dict(),
            usuario_id=current_user.id,
            ip_address=client_ip
        )
        
        return nova_associacao
        
    except ValueError as e:
        # Captura o aviso limpo que veio do nosso CRUD (sobre Nome ou CNPJ)
        raise HTTPException(status_code=400, detail=str(e))
        
    except Exception as e:
        # Se for qualquer outro erro bizarro, dá erro 500
        db.rollback()
        print(f"❌ ERRO: {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")
    

@router.get("/", response_model=schemas.AssociacoesPaginadasResponse)
def read_all_associacoes(
    skip: int = 0,
    limit: int = 100,
    ativo: Optional[bool] = True,
    db: Session = Depends(get_db)
):
    """Listar todas associações (público)"""
    return crud.get_all_associacoes(db, skip=skip, limit=limit, ativo=ativo)


@router.get("/ativas", response_model=List[schemas.AssociacaoResponse])
def read_associacoes_ativas(db: Session = Depends(get_db)):
    """Listar apenas associações ativas (para o frontend público)"""
    return crud.get_associacoes_ativas(db)


@router.get("/{associacao_id}", response_model=schemas.AssociacaoResponse)
def read_associacao(
    associacao_id: int,
    db: Session = Depends(get_db)
):
    """Consultar uma associação pelo ID"""
    db_assoc = crud.get_associacao(db, associacao_id=associacao_id)
    if not db_assoc:
        raise HTTPException(status_code=404, detail="Associação não encontrada")
    return db_assoc


@router.put("/{associacao_id}", response_model=schemas.AssociacaoResponse)
def update_associacao(
    associacao_id: int,
    associacao_update: schemas.AssociacaoUpdate,
    request: Request, # 🔥 Injetado para pegar o IP real
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Atualizar associação (requer autenticação)"""
    # 1. Busca o estado atual da associação ANTES da edição
    assoc_antes = crud.get_associacao(db, associacao_id=associacao_id)
    if not assoc_antes:
        raise HTTPException(status_code=404, detail="Associação não encontrada")
        
    dados_antigos = schemas.AssociacaoResponse.from_orm(assoc_antes).dict()

    # 2. Executa a atualização real no banco
    db_assoc = crud.update_associacao(
        db,
        associacao_id=associacao_id,
        associacao_update=associacao_update
    )
    
    # 3. Mapeia o estado final e captura o IP
    dados_novos = schemas.AssociacaoResponse.from_orm(db_assoc).dict()
    client_ip = request.client.host if request.client else None

    # 4. 🔥 AUDITORIA: Grava o log de alteração
    create_log(
        db=db,
        acao="UPDATE",
        tabela_afetada="associacoes",
        registro_id=associacao_id,
        dados_antigos=dados_antigos,
        dados_novos=dados_novos,
        usuario_id=current_user.id,
        ip_address=client_ip
    )

    return db_assoc


@router.delete("/{associacao_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_associacao(
    associacao_id: int,
    request: Request, # 🔥 Injetado para pegar o IP real
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Soft delete - marca como inativa (requer autenticação)"""
    # 1. Busca o estado da associação antes de desativá-la
    assoc_antes = crud.get_associacao(db, associacao_id=associacao_id)
    if not assoc_antes:
        raise HTTPException(status_code=404, detail="Associação não encontrada")
        
    dados_antigos = schemas.AssociacaoResponse.from_orm(assoc_antes).dict()

    # 2. Executa o Soft Delete
    db_assoc = crud.delete_associacao(db, associacao_id=associacao_id)
    if not db_assoc:
        raise HTTPException(status_code=404, detail="Associação não encontrada")
    
    # 3. Busca o estado final pós-soft-delete para auditoria
    assoc_depois = crud.get_associacao(db, associacao_id=associacao_id)
    dados_novos = schemas.AssociacaoResponse.from_orm(assoc_depois).dict() if assoc_depois else None
    
    client_ip = request.client.host if request.client else None

    # 4. 🔥 AUDITORIA: Grava o log de Soft Delete
    create_log(
        db=db,
        acao="DELETE",
        tabela_afetada="associacoes",
        registro_id=associacao_id,
        dados_antigos=dados_antigos,
        dados_novos=dados_novos,
        usuario_id=current_user.id,
        ip_address=client_ip
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)