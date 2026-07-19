from decimal import Decimal
from datetime import datetime

from sqlalchemy import DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func
from app.db.database import Base
from sqlalchemy import Index


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]

    withdrawable_balance: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        default=Decimal("0.00"),
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )
    __table_args__ = (
        Index("idx_withdrawal_user_created", "id", "created_at"),
    )

    sales = relationship("Sale", back_populates="user")
    withdrawals = relationship("Withdrawal", back_populates="user")