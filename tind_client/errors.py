"""
Exceptions raised by tind_client.
"""

import json


class TINDError(Exception):
    """Raised when the TIND API returns an unexpected error response."""

    @classmethod
    def from_json(cls, status: int, body: str) -> "TINDError":
        """Create a :class:`TINDError` from an HTTP status code and a JSON response body.

        :param int status: The HTTP status code returned by TIND.
        :param str body: The raw response body (expected to be JSON).
        :returns TINDError: A new :class:`TINDError` describing the failure.
        """
        try:
            data = json.loads(body)
            message: str = data.get("message", body) if isinstance(data, dict) else body
        except (json.JSONDecodeError, AttributeError):
            message = body
        return cls(f"TIND API error {status}: {message}")


class AuthorizationError(TINDError):
    """Raised when authorization with the TIND API fails."""


class RecordNotFoundError(TINDError):
    """Raised when a requested record or file is not found in TIND."""
