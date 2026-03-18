"""
Tests for TINDClient methods (fetch operations).
"""

import json

import pytest
import requests_mock as req_mock  # noqa: F401 — activates the requests_mock fixture

from tind_client import TINDClient
from tind_client.errors import RecordNotFoundError, TINDError

BASE_URL = "https://tind.example.edu"
pytestmark = pytest.mark.usefixtures("tind_env")


# ---------------------------------------------------------------------------
# fetch_metadata
# ---------------------------------------------------------------------------


def test_fetch_metadata_success(
    sample_marc_xml: str,
    requests_mock: req_mock.Mocker,
    client: TINDClient,
) -> None:
    """fetch_metadata returns a PyMARC Record for a valid record ID."""
    requests_mock.get(
        f"{BASE_URL}/record/12345/", text=sample_marc_xml, status_code=200
    )
    record = client.fetch_metadata("12345")
    assert record["245"]["a"] == "Sample Title"


def test_fetch_metadata_404(requests_mock: req_mock.Mocker, client: TINDClient) -> None:
    """fetch_metadata raises RecordNotFoundError on HTTP 404."""
    requests_mock.get(f"{BASE_URL}/record/99999/", text="", status_code=404)
    with pytest.raises(RecordNotFoundError):
        client.fetch_metadata("99999")


def test_fetch_metadata_empty_body(
    requests_mock: req_mock.Mocker, client: TINDClient
) -> None:
    """fetch_metadata raises RecordNotFoundError when the response body is empty."""
    requests_mock.get(f"{BASE_URL}/record/11111/", text="   ", status_code=200)
    with pytest.raises(RecordNotFoundError):
        client.fetch_metadata("11111")


# ---------------------------------------------------------------------------
# fetch_file
# ---------------------------------------------------------------------------


def test_fetch_file_invalid_url(client: TINDClient) -> None:
    """fetch_file raises ValueError for non-TIND download URLs."""
    with pytest.raises(ValueError):
        client.fetch_file("https://not-a-tind-url.com/file.pdf")


def test_fetch_file_success(
    requests_mock: req_mock.Mocker,
    tmp_path: pytest.TempPathFactory,
    client: TINDClient,
) -> None:
    """fetch_file downloads and saves a file, returning its local path."""
    url = f"{BASE_URL}/files/abc/download"
    requests_mock.get(
        url,
        content=b"file data",
        status_code=200,
        headers={"Content-Disposition": 'attachment; filename="document.pdf"'},
    )
    path = client.fetch_file(url, output_dir=str(tmp_path))
    assert path.endswith("document.pdf")


def test_fetch_file_not_found(
    requests_mock: req_mock.Mocker,
    tmp_path: pytest.TempPathFactory,
    client: TINDClient,
) -> None:
    """fetch_file raises RecordNotFoundError when the download returns non-200."""
    url = f"{BASE_URL}/files/missing/download"
    requests_mock.get(url, status_code=404)
    with pytest.raises(RecordNotFoundError):
        client.fetch_file(url, output_dir=str(tmp_path))


# ---------------------------------------------------------------------------
# fetch_file_metadata
# ---------------------------------------------------------------------------


def test_fetch_file_metadata_success(
    requests_mock: req_mock.Mocker, client: TINDClient
) -> None:
    """fetch_file_metadata returns a list of file metadata dicts."""
    payload = [{"name": "file.pdf", "size": 1024}]
    requests_mock.get(
        f"{BASE_URL}/record/12345/files",
        text=json.dumps(payload),
        status_code=200,
    )
    result = client.fetch_file_metadata("12345")
    assert result[0]["name"] == "file.pdf"


def test_fetch_file_metadata_error(
    requests_mock: req_mock.Mocker, client: TINDClient
) -> None:
    """fetch_file_metadata raises TINDError on non-200 responses."""
    requests_mock.get(
        f"{BASE_URL}/record/12345/files",
        text=json.dumps({"message": "Not found"}),
        status_code=404,
    )
    with pytest.raises(TINDError):
        client.fetch_file_metadata("12345")


# ---------------------------------------------------------------------------
# fetch_ids_search
# ---------------------------------------------------------------------------


def test_fetch_ids_search_success(
    requests_mock: req_mock.Mocker, client: TINDClient
) -> None:
    """fetch_ids_search returns the list of record IDs from the search response."""
    requests_mock.get(
        f"{BASE_URL}/search",
        text=json.dumps({"hits": ["1", "2", "3"]}),
        status_code=200,
    )
    ids = client.fetch_ids_search("title:python")
    assert ids == ["1", "2", "3"]


def test_fetch_ids_search_error(
    requests_mock: req_mock.Mocker, client: TINDClient
) -> None:
    """fetch_ids_search raises TINDError on non-200 responses."""
    requests_mock.get(
        f"{BASE_URL}/search",
        text=json.dumps({"message": "Bad request"}),
        status_code=400,
    )
    with pytest.raises(TINDError):
        client.fetch_ids_search("title:python")


# ---------------------------------------------------------------------------
# search
# ---------------------------------------------------------------------------


def test_search_invalid_format(client: TINDClient) -> None:
    """search raises ValueError for unsupported result_format values."""
    with pytest.raises(ValueError, match="Unexpected result format"):
        client.search("title:test", result_format="csv")


def test_search_returns_xml(
    sample_marc_xml: str,
    requests_mock: req_mock.Mocker,
    client: TINDClient,
) -> None:
    """search returns a list of XML strings when result_format='xml'."""
    # Wrap sample XML in a search_id element so pagination terminates correctly.
    wrapped = sample_marc_xml.replace(
        "<collection",
        "<root><search_id></search_id><collection",
    ).replace("</collection>", "</collection></root>")

    requests_mock.get(f"{BASE_URL}/search", text=wrapped, status_code=200)

    results = client.search("title:sample", result_format="xml")
    assert isinstance(results, list)
    assert len(results) >= 1
    assert requests_mock.call_count == 1
