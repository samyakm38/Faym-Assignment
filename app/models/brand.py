from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Brand(Base):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]

    sales = relationship("Sale", back_populates="brand")