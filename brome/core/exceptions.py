
class InitDriverException(Exception):
    """Raise when the driver failed initializing
    Args:
        msg (str): Human readable string describing the exception.
    """

    def __init__(self, msg):
        self.msg = msg


class InvalidBrowserName(Exception):
    """Raise when the given browserName config is invalid
    Args:
        msg (str): Human readable string describing the exception.
    """

    def __init__(self, msg):
        self.msg = msg


class BromeBrowserConfigException(Exception):
    """Raise when the given browser config is invalid
    Args:
        msg (str): Human readable string describing the exception.
    """

    def __init__(self, msg):
        self.msg = msg


class ServerBaseException(Exception):
    def get_name(self):
        return self.__repr__().split('(')[0]


class MissingModelValueException(ServerBaseException):
    pass


class WrongEmailOrPasswordException(ServerBaseException):
    pass


class EmailAlreadyExistsException(ServerBaseException):
    pass


class InvalidNameException(ServerBaseException):
    pass


class InvalidPasswordException(ServerBaseException):
    pass


class InvalidEmailException(ServerBaseException):
    pass


class NotAuthorizedException(ServerBaseException):
    pass


class CSRFMismatch(ServerBaseException):
    pass


class InvalidRequestException(ServerBaseException):
    pass


class EmailAlreadyConfirmedException(ServerBaseException):
    pass


class EmailMismatchException(ServerBaseException):
    pass


class TokenExpiredException(ServerBaseException):
    pass


class TokenViolationException(ServerBaseException):
    pass


class TokenAlreadyUsedException(ServerBaseException):
    pass


class TokenInvalidException(ServerBaseException):
    pass


class EmailNotFound(ServerBaseException):
    pass


class ModelImportException(ServerBaseException):
    pass


class InvalidRegistrationTokenException(ServerBaseException):
    pass
