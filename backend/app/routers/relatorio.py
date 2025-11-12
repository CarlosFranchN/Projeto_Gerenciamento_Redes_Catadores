# app/routers/relatorio.py

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import date
from .. import crud, schemas 
from ..database import get_db
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/relatorio",
    tags=["Relatorio"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/summary", response_model=schemas.ReportSummaryResponse)
def get_summary_endpoint(
    start_date: Optional[date] = None, 
    end_date: Optional[date] = None, 
    db: Session = Depends(get_db)
):
    """ Retorna os totais de recebido, vendido e receita para um período. """
    return crud.get_report_summary(db, start_date=start_date, end_date=end_date)

@router.get(
    "/por-material", 
    response_model=List[schemas.ReportPorMaterialItem],
    summary="Relatório agregado por material"
)
def get_por_material_endpoint(
    start_date: Optional[date] = None, 
    end_date: Optional[date] = None, 
    db: Session = Depends(get_db)
):
    """ Retorna recebido, vendido, saldo e receita por material para um período. """
    return crud.get_report_por_material(db, start_date=start_date, end_date=end_date)


@router.get(
    "/por-doador",  
    response_model=List[schemas.ReportPorParceiroItem], 
    summary="Relatório agregado por doador" 
)
def get_por_doador_endpoint( 
    start_date: Optional[date] = None, 
    end_date: Optional[date] = None, 
    db: Session = Depends(get_db)
):
    """ Retorna o total recebido por doador para um período. """
    # 5. Chamada da função CRUD corrigida
    return crud.get_report_por_parceiro(db, start_date=start_date, end_date=end_date)