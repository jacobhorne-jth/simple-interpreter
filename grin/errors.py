class GrinParseError(Exception):
    """Raised when a parsing error occurs."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class GrinRuntimeError(Exception):
    """Raised when a runtime error occurs."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message