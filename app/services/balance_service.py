from decimal import Decimal

from app.models.user import User
from app.exceptions.balance import InsufficientBalanceError


class BalanceService:

    @staticmethod
    def credit(user: User, amount: Decimal) -> None:
        """Increase the user's withdrawable balance."""
        user.withdrawable_balance += amount

    @staticmethod
    def debit(user: User, amount: Decimal) -> None:
        """
        Decrease the user's withdrawable balance.

        Raises:
            InsufficientBalanceError if the balance is insufficient.
        """
        if user.withdrawable_balance < amount:
            raise InsufficientBalanceError(
                "Insufficient withdrawable balance."
            )

        user.withdrawable_balance -= amount

    @staticmethod
    def adjust_by(user: User, delta: Decimal) -> None:
        """
        Apply a reconciliation adjustment.

        Delta may be positive or negative and may result in
        a negative balance.
        """
        user.withdrawable_balance += delta