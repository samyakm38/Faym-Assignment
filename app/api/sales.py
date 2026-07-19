from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.repositories.sale import SaleRepository
from app.exceptions.sale import SaleNotFoundError

from app.db.session import get_db
from app.schemas.sale import (
    CreateSaleRequest,
    SaleResponse,
)
from app.services.sale_service import SaleService

router = APIRouter(
    prefix="/sales",
    tags=["Sales"],
)


@router.post(
    "",
    response_model=SaleResponse,
    status_code=201,
)
def create_sale(
    request: CreateSaleRequest,
    db: Session = Depends(get_db),
):
    service = SaleService(db)

    sale = service.create_sale(
        user_id=request.user_id,
        brand_id=request.brand_id,
        earning=request.earning,
    )

    return sale


@router.get(
    "/{sale_id}",
    response_model=SaleResponse,
)
def get_sale(
    sale_id: int,
    db: Session = Depends(get_db),
):
    sale = SaleRepository(db).get_by_id(sale_id)

    if not sale:
        raise SaleNotFoundError(sale_id)

    return sale


@router.post(
    "/{sale_id}/approve",
    response_model=SaleResponse,
)
def approve_sale(
    sale_id: int,
    db: Session = Depends(get_db),
):
    service = SaleService(db)

    sale = service.approve_sale(sale_id)
    return sale


@router.post(
    "/{sale_id}/reject",
    response_model=SaleResponse,
)
def reject_sale(
    sale_id: int,
    db: Session = Depends(get_db),
):
    service = SaleService(db)
    sale = service.reject_sale(sale_id)
    return sale
