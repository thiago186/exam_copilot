class AuthenticationError(Exception):
    """Exception raised when authentication fails."""
    pass

class UserNotFoundError(Exception):
    """Exception raised when a user is not found."""
    pass