class ProviderUserProjectConfigurationError(Exception):
    """Exception raised when a provider user project configuration fails."""

    def __init__(self, message: str):
        super().__init__(message)
