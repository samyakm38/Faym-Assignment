from decimal import Decimal

from pydantic import BaseModel, Field


class CreateWithdrawalRequest(BaseModel):
    user_id: int
    amount: Decimal = Field(gt=0)

from pydantic import BaseModel


class MarkFailureRequest(BaseModel):
    reason: str


from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.core.enums import WithdrawalStatus


class WithdrawalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int

    amount: Decimal

    status: WithdrawalStatus

    failure_reason: str | None

    created_at: datetime
    updated_at: datetime