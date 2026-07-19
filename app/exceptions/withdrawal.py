class WithdrawalCooldownError(Exception):
    """Raised when a user attempts to withdraw within the cooldown period."""

    def __init__(self):
        super().__init__(
            "Withdrawals are allowed only once every 24 hours."
        )

class WithdrawalNotFoundError(Exception):
    """Raised when the requested withdrawal does not exist."""

    def __init__(self, withdrawal_id: int):
        super().__init__(f"Withdrawal with id {withdrawal_id} not found.")