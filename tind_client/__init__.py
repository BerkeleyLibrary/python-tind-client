"""
python-tind-client — Python library for interacting with the TIND DA API.
"""

__copyright__ = "© 2026 The Regents of the University of California.  MIT license."

from .client import TINDClient
from .errors import AuthorizationError, RecordNotFoundError, TINDError

__all__ = [
    "TINDClient",
    "AuthorizationError",
    "RecordNotFoundError",
    "TINDError",
]
