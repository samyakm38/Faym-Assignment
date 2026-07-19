from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.sales import router as sales_router
from app.api.withdrawals import router as withdrawals_router
from app.api.users import router as users_router
from app.api.jobs import router as jobs_router
from app.db.database import Base, engine

from app.exceptions.user import UserNotFoundError
from app.exceptions.brand import BrandNotFoundError
from app.exceptions.sale import SaleNotFoundError
from app.exceptions.withdrawal import (
    WithdrawalNotFoundError,
    WithdrawalCooldownError,
)
from app.exceptions.balance import InsufficientBalanceError
from app.models.user import User
from app.models.brand import Brand
from app.models.sale import Sale
from app.models.withdrawal import Withdrawal

app = FastAPI(title="User Payout Management System")
Base.metadata.create_all(bind=engine)
@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(
    request: Request,
    exc: UserNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.exception_handler(BrandNotFoundError)
async def brand_not_found_handler(
    request: Request,
    exc: BrandNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.exception_handler(SaleNotFoundError)
async def sale_not_found_handler(
    request: Request,
    exc: SaleNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.exception_handler(WithdrawalNotFoundError)
async def withdrawal_not_found_handler(
    request: Request,
    exc: WithdrawalNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.exception_handler(InsufficientBalanceError)
async def insufficient_balance_handler(
    request: Request,
    exc: InsufficientBalanceError,
):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


@app.exception_handler(WithdrawalCooldownError)
async def withdrawal_cooldown_handler(
    request: Request,
    exc: WithdrawalCooldownError,
):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )

app.include_router(sales_router)
app.include_router(withdrawals_router)
app.include_router(users_router)
app.include_router(jobs_router)

@app.get("/")
def health_check():
    return {"status": "ok"}