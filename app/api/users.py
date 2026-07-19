from fastapi import APIRouter
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.exceptions.user import UserNotFoundError
from app.repositories.user import UserRepository
from app.schemas.user import BalanceResponse
from app.db.session import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get(
    "/{user_id}/balance",
    response_model=BalanceResponse,
)
def get_balance(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = UserRepository(db).get_by_id(user_id)

    if not user:
        raise UserNotFoundError(user_id)

    return BalanceResponse(
        withdrawable_balance=user.withdrawable_balance,
    )