from fastapi import APIRouter, Depends, HTTPException,status, Response
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db
from typing import Optional
from datetime import date

router = APIRouter(
    prefix="/relatorio",
    tags=["Relatorio"]
)


@router.get("/relatorio", response_model=schemas.ReportSummaryResponse)
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

# 👇 ENDPOINT NOVO POR ASSOCIAÇÃO 👇
@router.get(
    "/por-associacao", 
    response_model=List[schemas.ReportPorAssociacaoItem],
    summary="Relatório agregado por associação"
)
def get_por_associacao_endpoint(
    start_date: Optional[date] = None, 
    end_date: Optional[date] = None, 
    db: Session = Depends(get_db)
):
    """ Retorna o total recebido por associação para um período. """
    return crud.get_report_por_associacao(db, start_date=start_date, end_date=end_date)