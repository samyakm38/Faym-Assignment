class BrandNotFoundError(Exception):
    """Raised when the requested brand does not exist."""

    def __init__(self, brand_id: int):
        super().__init__(f"Brand with id {brand_id} not found.")