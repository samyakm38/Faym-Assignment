from decimal import Decimal

from pydantic import BaseModel, Field


class CreateSaleRequest(BaseModel):
    user_id: int
    brand_id: int
    earning: Decimal = Field(gt=0)

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.core.enums import SaleStatus


class SaleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    brand_id: int

    earning: Decimal
    advance_amount: Decimal

    status: SaleStatus
    advance_added: bool

    created_at: datetime
    updated_at: datetime