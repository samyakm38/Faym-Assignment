from sqlalchemy.orm import Session

from app.models.brand import Brand
from .base import BaseRepository


class BrandRepository(BaseRepository):

    def get_by_id(self, brand_id: int) -> Brand | None:
        return (
            self.db.query(Brand)
            .filter(Brand.id == brand_id)
            .first()
        )

    def save(self, brand: Brand):
        self.db.add(brand)
        self.db.flush()