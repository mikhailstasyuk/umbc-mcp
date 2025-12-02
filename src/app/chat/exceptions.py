class ChatServiceError(Exception):
    """Base exception for all chat service errors."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationFailedError(ChatServiceError):
    """Raised when OpenAI API authentication fails (invalid API key)."""

    def __init__(self, message: str = "OpenAI authentication failed"):
        super().__init__(message=message, status_code=401)


class RateLimitExceededError(ChatServiceError):
    """Raised when OpenAI API rate limit is exceeded."""

    def __init__(self, message: str = "OpenAI rate limit exceeded"):
        super().__init__(message=message, status_code=429)


class OpenAIConnectionError(ChatServiceError):
    """Raised when connection to OpenAI API fails."""

    def __init__(self, message: str = "Failed to connect to OpenAI API"):
        super().__init__(message=message, status_code=502)


class EmptyResponseError(ChatServiceError):
    """Raised when OpenAI returns an empty choices array."""

    def __init__(self, message: str = "OpenAI returned an empty response"):
        super().__init__(message=message, status_code=500)


class ModelNotFoundError(ChatServiceError):
    """Raised when the requested model does not exist."""

    def __init__(self, message: str = "Model not found"):
        super().__init__(message=message, status_code=404)
