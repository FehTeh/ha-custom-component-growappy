class GrowappyException(Exception):
    """Base exception for Growappy."""
    pass

class GrowappyUnauthorizedException(GrowappyException):
    """Raised when the API returns 401."""
    def __init__(self, message="Token inválido ou expirado"):
        self.message = message
        super().__init__(self.message)

class GrowappyApiException(GrowappyException):
    """Raised for other API errors (500, 404, etc)."""
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Error {status_code}: {message}")