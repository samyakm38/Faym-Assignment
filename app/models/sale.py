from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func
from sqlalchemy import Index
from app.core.enums import SaleStatus
from app.db.database import Base


class Sale(Base):
    __tablename__ = "sales"
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    brand_id: Mapped[int] = mapped_column(
        ForeignKey("brands.id"),
        nullable=False,
    )

    earning: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    advance_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    status: Mapped[SaleStatus] = mapped_column(
        Enum(SaleStatus),
        nullable=False,
        default=SaleStatus.PENDING,
    )

    advance_added: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )
    __table_args__ = (
        Index("idx_sale_pending_advances", "status", "advance_added"),
    )


    user = relationship("User", back_populates="sales")
    brand = relationship("Brand", back_populates="sales")