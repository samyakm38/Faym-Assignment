from datetime import timedelta
from datetime import datetime
from sqlalchemy.orm import Session
from app.repositories.withdrawal import WithdrawalRepository
from app.repositories.user import UserRepository 
from decimal import Decimal
from app.services.balance_service import BalanceService
from app.exceptions.user import UserNotFoundError
from app.exceptions.withdrawal import WithdrawalCooldownError
from app.exceptions.withdrawal import WithdrawalNotFoundError
from app.models.withdrawal import Withdrawal
from app.core.config import settings
from app.core.enums import WithdrawalStatus

class WithdrawalService:

    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.withdrawal_repo = WithdrawalRepository(db)

    def create_withdrawal(
        self,
        user_id: int,
        amount: Decimal,
    ) -> Withdrawal:

        user = self.user_repo.get_by_id(user_id)

        if not user:
            raise UserNotFoundError(user_id)

        latest = self.withdrawal_repo.get_latest_for_user(user_id)

        if latest:
            cooldown = timedelta(
                hours=settings.WITHDRAWAL_COOLDOWN_HOURS
            )

            if datetime.utcnow() < latest.created_at + cooldown:
                raise WithdrawalCooldownError()

        BalanceService.debit(
            user,
            amount,
        )

        withdrawal = Withdrawal(
            user_id=user_id,
            amount=amount,
            status=WithdrawalStatus.INITIATED,
        )

        self.withdrawal_repo.save(withdrawal)

        return withdrawal

    def mark_success(
        self,
        withdrawal_id: int,
    ) -> Withdrawal:

        withdrawal = self.withdrawal_repo.get_by_id(
            withdrawal_id
        )

        if not withdrawal:
            raise WithdrawalNotFoundError(
                withdrawal_id
            )

        if withdrawal.status != WithdrawalStatus.INITIATED:
            return withdrawal

        withdrawal.status = WithdrawalStatus.SUCCESS

        return withdrawal

    def mark_failure(
        self,
        withdrawal_id: int,
        reason: str,
    ) -> Withdrawal:

        withdrawal = self.withdrawal_repo.get_by_id(
            withdrawal_id
        )

        if not withdrawal:
            raise WithdrawalNotFoundError(
                withdrawal_id
            )

        if withdrawal.status != WithdrawalStatus.INITIATED:
            return withdrawal

        BalanceService.credit(
            withdrawal.user,
            withdrawal.amount,
        )

        withdrawal.status = WithdrawalStatus.FAILED
        withdrawal.failure_reason = reason

        return withdrawal