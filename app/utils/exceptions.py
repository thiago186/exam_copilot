class AuthenticationError(Exception):
    """Exception raised when authentication fails."""
    pass

class UserNotFoundError(Exception):
    """Exception raised when a user is not found."""
    pass

class OpenAIException(Exception):
    """Exception raised when a request to OpenAI fails."""
    pass