

class PGSSException(Exception):
    """Base exception class"""


class PGSSInvalidOperation(PGSSException):
    """Invalid operation"""


class PGSSLookupError(PGSSException):
    """Invalid GoGraph lookup (ex. missing node or edge)"""
