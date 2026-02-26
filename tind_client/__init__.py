"""
python-tind-client — Python library for interacting with the TIND ILS API.
"""

__copyright__ = "© 2026 The Regents of the University of California.  MIT license."

from .client import TINDClient
from .api import tind_download, tind_get
from .errors import AuthorizationError, RecordNotFoundError, TINDError
from .fetch import (
    fetch_file,
    fetch_file_metadata,
    fetch_ids_search,
    fetch_marc_by_ids,
    fetch_metadata,
    fetch_search_metadata,
    search,
)

__all__ = [
    "TINDClient",
    "tind_get",
    "tind_download",
    "AuthorizationError",
    "RecordNotFoundError",
    "TINDError",
    "fetch_metadata",
    "fetch_file",
    "fetch_file_metadata",
    "fetch_ids_search",
    "fetch_marc_by_ids",
    "fetch_search_metadata",
    "search",
]
