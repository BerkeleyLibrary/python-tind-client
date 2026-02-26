"""
TINDClient — the main entry point for interacting with the TIND ILS API.
"""

from typing import Any
from pymarc import Record

from .api import tind_get, tind_download
from .fetch import (
    fetch_metadata,
    fetch_file,
    fetch_file_metadata,
    fetch_ids_search,
    fetch_marc_by_ids,
    fetch_search_metadata,
    search,
)


class TINDClient:
    """Client for interacting with a TIND ILS instance.

    :param str api_key: Your TIND API token.
    :param str api_url: Base URL of the TIND instance, e.g. ``https://tind.example.edu``.
    :param str default_storage_dir: Default directory used by :meth:`fetch_file`
                                    when no ``output_dir`` is supplied.
    """

    def __init__(
        self, api_key: str, api_url: str, default_storage_dir: str = ""
    ) -> None:
        self.api_key = api_key
        self.api_url = api_url
        self.default_storage_dir = default_storage_dir

    def _tind_get(
        self, endpoint: str, params: dict[str, str] | None = None
    ) -> tuple[int, str]:
        """See :func:`tind_client.api.tind_get`."""
        return tind_get(
            endpoint, api_key=self.api_key, api_url=self.api_url, params=params
        )

    def _tind_download(self, url: str, output_dir: str) -> tuple[int, str]:
        """See :func:`tind_client.api.tind_download`."""
        return tind_download(url, output_dir, api_key=self.api_key)

    def fetch_metadata(self, record: str) -> Record:
        """See :func:`tind_client.fetch.fetch_metadata`."""
        return fetch_metadata(record, api_key=self.api_key, api_url=self.api_url)

    def fetch_file(self, file_url: str, output_dir: str = "") -> str:
        """See :func:`tind_client.fetch.fetch_file`."""
        return fetch_file(
            file_url,
            api_key=self.api_key,
            output_dir=output_dir,
            default_storage_dir=self.default_storage_dir,
        )

    def fetch_file_metadata(self, record: str) -> list[dict[str, Any]]:
        """See :func:`tind_client.fetch.fetch_file_metadata`."""
        return fetch_file_metadata(record, api_key=self.api_key, api_url=self.api_url)

    def fetch_ids_search(self, query: str) -> list[str]:
        """See :func:`tind_client.fetch.fetch_ids_search`."""
        return fetch_ids_search(query, api_key=self.api_key, api_url=self.api_url)

    def fetch_marc_by_ids(self, ids: list[str]) -> list[Record]:
        """See :func:`tind_client.fetch.fetch_marc_by_ids`."""
        return fetch_marc_by_ids(ids, api_key=self.api_key, api_url=self.api_url)

    def fetch_search_metadata(self, query: str) -> list[Record]:
        """See :func:`tind_client.fetch.fetch_search_metadata`."""
        return fetch_search_metadata(query, api_key=self.api_key, api_url=self.api_url)

    def search(self, query: str, result_format: str = "xml") -> list[Any]:
        """See :func:`tind_client.fetch.search`."""
        return search(
            query,
            result_format=result_format,
            api_key=self.api_key,
            api_url=self.api_url,
        )
