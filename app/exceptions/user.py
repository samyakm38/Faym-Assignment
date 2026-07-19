class UserNotFoundError(Exception):
    """Raised when the requested user does not exist."""

    def __init__(self, user_id: int):
        super().__init__(f"User with id {user_id} not found.")