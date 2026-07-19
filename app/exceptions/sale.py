class SaleNotFoundError(Exception):
    """Raised when the requested sale does not exist."""

    def __init__(self, sale_id: int):
        super().__init__(f"Sale with id {sale_id} not found.")