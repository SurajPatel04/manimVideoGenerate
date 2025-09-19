class UserNotFoundException(Exception):
    """Raised when a user is not found in the database."""
    pass

class UserAlreadyVerifiedException(Exception):
    """Raised when a user is already verified."""
    pass
