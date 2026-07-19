from sqlalchemy import select

from app.models.withdrawal import Withdrawal
from .base import BaseRepository


class WithdrawalRepository(BaseRepository):

    def get_by_id(self, withdrawal_id: int) -> Withdrawal | None:
        return self.db.scalar(
            select(Withdrawal).where(
                Withdrawal.id == withdrawal_id
            )
        )

    def get_latest_for_user(self, user_id: int) -> Withdrawal | None:
        return self.db.scalar(
            select(Withdrawal)
            .where(Withdrawal.user_id == user_id)
            .order_by(Withdrawal.created_at.desc())
        )

    def save(self, withdrawal: Withdrawal) -> None:
        self.db.add(withdrawal)
        self.db.flush()
    