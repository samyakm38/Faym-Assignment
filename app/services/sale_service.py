from app.models.sale import Sale
from sqlalchemy.orm import Session
from app.repositories.sale import SaleRepository 
from app.repositories.user import UserRepository 
from app.repositories.brand import BrandRepository 
from decimal import Decimal
from app.core.enums import SaleStatus
from app.services.balance_service import BalanceService
from app.exceptions.brand import BrandNotFoundError
from app.exceptions.user import UserNotFoundError
from app.exceptions.sale import SaleNotFoundError
from app.core.config import settings

class SaleService:

    def __init__(self, db: Session):
        self.db = db
        self.sale_repo = SaleRepository(db)
        self.user_repo = UserRepository(db)
        self.brand_repo = BrandRepository(db)

    def create_sale(
        self,
        user_id: int,
        brand_id: int,
        earning: Decimal,
    ) -> Sale:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()

        brand = self.brand_repo.get_by_id(brand_id)
        if not brand:
            raise BrandNotFoundError()

        advance = earning * Decimal(str(settings.ADVANCE_PERCENTAGE))

        sale = Sale(
            user_id=user_id,
            brand_id=brand_id,
            earning=earning,
            advance_amount=advance,
        )

        self.sale_repo.save(sale)

        return sale

    def process_pending_advances(self) -> int:
        sales = self.sale_repo.get_pending_without_advance()
        for sale in sales:

            BalanceService.credit(
                sale.user,
                sale.advance_amount,
            )

            sale.advance_added = True

        return len(sales)

    def approve_sale(self, sale_id: int) -> Sale:
        sale = self.sale_repo.get_by_id(sale_id)
        if not sale:
            raise SaleNotFoundError()

        if sale.status != SaleStatus.PENDING:
            return sale

        remaining = (
            sale.earning
            - sale.advance_amount
        )

        BalanceService.credit(
            sale.user,
            remaining,
        )

        sale.status = SaleStatus.APPROVED

        return sale

    def reject_sale(self, sale_id: int) -> Sale:
        sale = self.sale_repo.get_by_id(sale_id)
        if not sale:
            raise SaleNotFoundError()

        if sale.status != SaleStatus.PENDING:
            return sale

        if sale.advance_added:
            BalanceService.adjust_by(
                sale.user,
                -sale.advance_amount,
            )

        sale.status = SaleStatus.REJECTED

        return sale