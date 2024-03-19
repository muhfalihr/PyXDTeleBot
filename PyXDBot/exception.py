from requests import RequestException


class PyXDTelebotException(Exception):
    """Base exception for this script.

    :note: This exception may not be applied for directly.
    """
    pass


class HTTPErrorException(Exception):
    pass


class RequestProcessingError(RequestException):
    pass


class CSRFTokenMissingError(Exception):
    pass


class URLValidationError(Exception):
    pass


class FunctionNotFoundError(Exception):
    pass


class CookieFileNotFoundError(Exception):
    pass


class CookieCreationError(Exception):
    pass
