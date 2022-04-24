class ValidationException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


class CryptoException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


class StorageFacadeException(Exception):
    def __init__(self, message, errors="Storage facade exception"):
        super().__init__(message)
        self.errors = errors


class FailedLoginException(Exception):
    def __init__(self, message, errors="Username or password incorrect"):
        super().__init__(message)
        self.errors = errors

