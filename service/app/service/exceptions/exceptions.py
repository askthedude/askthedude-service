class ValidationException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


class CryptoException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


class StorageFacadeException(Exception):
    def __init__(self, message, errors="Exception while communicating with Storage."):
        super().__init__(message)
        self.errors = errors


class FailedLoginException(Exception):
    def __init__(self, message, errors="Login credentials: Username or password is incorrect"):
        super().__init__(message)
        self.errors = errors


class FailedSignupException(Exception):
    def __init__(self, message, errors="Couldn't signup with input parameters. Please change email and username."):
        super().__init__(message)
        self.errors = errors


class NotAuthorizedException(Exception):
    def __init__(self, message, errors="Couldn't authorize user of the request"):
        super().__init__(message)
        self.errors = errors


class ResourceNotFoundException(Exception):
    def __init__(self, message, errors="Couldn't find requested resource"):
        super().__init__(message)
        self.errors = errors


class ResourceConflictException(Exception):
    def __init__(self, message, errors="Resource like new input already present"):
        super().__init__(message)
        self.errors = errors