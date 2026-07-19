from sqlalchemy.orm import Session

from app.models.sale import Sale
from .base import BaseRepository
from app.core.enums import SaleStatus 

class SaleRepository(BaseRepository):

    def get_by_id(self, sale_id: int) -> Sale | None:
        return (
            self.db.query(Sale)
            .filter(Sale.id == sale_id)
            .first()
        )

    def get_pending_without_advance(self) -> list[Sale]:
        return (
            self.db.query(Sale)
            .filter(
                Sale.status == SaleStatus.PENDING,
                Sale.advance_added.is_(False),
            )
            .all()
        )

    def save(self, sale: Sale):
        self.db.add(sale)
        self.db.flush()