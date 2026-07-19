from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.repositories.withdrawal import WithdrawalRepository
from app.exceptions.withdrawal import WithdrawalNotFoundError

from app.db.session import get_db
from app.schemas.withdrawal import (
    CreateWithdrawalRequest,
    WithdrawalResponse,
    MarkFailureRequest
)
from app.services.withdrawal_service import WithdrawalService

router = APIRouter(
    prefix="/withdrawals",
    tags=["Withdrawals"],
)

@router.post(
    "",
    response_model=WithdrawalResponse,
    status_code=201,
)
def create_withdrawal(
    request: CreateWithdrawalRequest,
    db: Session = Depends(get_db),
):
    service = WithdrawalService(db)

    withdrawal = service.create_withdrawal(
        request.user_id,
        request.amount,
    )

    return withdrawal

@router.post(
    "/{withdrawal_id}/success",
    response_model=WithdrawalResponse,
)
def mark_success(
    withdrawal_id: int,
    db: Session = Depends(get_db),
):
    service = WithdrawalService(db)

    withdrawal = service.mark_success(
        withdrawal_id,
    )

    return withdrawal

@router.post(
    "/{withdrawal_id}/failure",
    response_model=WithdrawalResponse,
)
def mark_failure(
    withdrawal_id: int,
    request: MarkFailureRequest,
    db: Session = Depends(get_db),
):
    service = WithdrawalService(db)

    withdrawal = service.mark_failure(
        withdrawal_id,
        request.reason,
    )

    return withdrawal


@router.get(
    "/{withdrawal_id}",
    response_model=WithdrawalResponse,
)
def get_withdrawal(
    withdrawal_id: int,
    db: Session = Depends(get_db),
):
    withdrawal = WithdrawalRepository(db).get_by_id(
        withdrawal_id
    )

    if not withdrawal:
        raise WithdrawalNotFoundError(withdrawal_id)

    return withdrawal