class ForbiddenError(Exception):
    """Exception raised when an action on a resource is not allowed."""

    def __init__(self, message: str):
        super().__init__(message)


class NotFoundError(Exception):
    """Exception raised when a resource is not found."""

    def __init__(self, message: str):
        super().__init__(message)
