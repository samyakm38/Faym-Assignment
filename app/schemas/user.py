from pydantic import BaseModel
from decimal import Decimal

class BalanceResponse(BaseModel):
    withdrawable_balance: Decimal