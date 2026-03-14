from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import crud_producao
from app.schemas.schema_producao import ProducaoCreate, ProducaoResponse

router = APIRouter(prefix="/api/producao", tags=["Produção"])

@router.get("/", response_model=list[ProducaoResponse])
def listar_producao(ano: int = 2024, associacao_id: int = None, db: Session = Depends(get_db)):
    return crud_producao.get_producao_by_ano(db, ano, associacao_id)

@router.post("/", response_model=ProducaoResponse)
def criar_producao(producao: ProducaoCreate, db: Session = Depends(get_db)):
    return crud_producao.create_producao(db, producao)