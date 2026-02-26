"""
Tests for tind_client.api.
"""

import pytest
import requests_mock as req_mock  # noqa: F401 — activates the requests_mock fixture

from tind_client.api import tind_download, tind_get
from tind_client.errors import AuthorizationError

BASE_URL = "https://tind.example.edu"
API_KEY = "test-api-key"
pytestmark = pytest.mark.usefixtures("tind_env")


def test_tind_get_success(requests_mock: req_mock.Mocker) -> None:
    """tind_get returns (200, body) on a successful request."""
    requests_mock.get(f"{BASE_URL}/record/1/", text="OK", status_code=200)
    status, text = tind_get("record/1/", api_key=API_KEY, api_url=BASE_URL)
    assert status == 200
    assert text == "OK"


def test_tind_get_with_params(requests_mock: req_mock.Mocker) -> None:
    """tind_get forwards query parameters to the HTTP request."""
    requests_mock.get(f"{BASE_URL}/record/1/", text="<xml/>", status_code=200)
    status, _ = tind_get(
        "record/1/", api_key=API_KEY, api_url=BASE_URL, params={"of": "xm"}
    )
    assert status == 200
    assert requests_mock.last_request is not None
    assert requests_mock.last_request.qs == {"of": ["xm"]}


def test_tind_get_raises_on_401(requests_mock: req_mock.Mocker) -> None:
    """tind_get raises AuthorizationError on HTTP 401."""
    requests_mock.get(f"{BASE_URL}/record/1/", status_code=401)
    with pytest.raises(AuthorizationError):
        tind_get("record/1/", api_key=API_KEY, api_url=BASE_URL)


def test_tind_get_raises_on_500(requests_mock: req_mock.Mocker) -> None:
    """tind_get propagates an HTTPError on HTTP 5xx."""
    requests_mock.get(f"{BASE_URL}/record/1/", status_code=500)
    with pytest.raises(Exception):
        tind_get("record/1/", api_key=API_KEY, api_url=BASE_URL)


def test_tind_get_missing_api_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """tind_get raises AuthorizationError when API key is empty."""
    monkeypatch.delenv("TIND_API_KEY", raising=False)
    with pytest.raises(AuthorizationError):
        tind_get("record/1/", api_key="", api_url=BASE_URL)


def test_tind_download_success(
    requests_mock: req_mock.Mocker, tmp_path: pytest.TempPathFactory
) -> None:
    """tind_download saves the file and returns its path."""
    url = f"{BASE_URL}/files/12345/download"
    requests_mock.get(
        url,
        content=b"file content",
        status_code=200,
        headers={"Content-Disposition": 'attachment; filename="report.pdf"'},
    )
    status, path = tind_download(url, str(tmp_path), api_key=API_KEY)
    assert status == 200
    assert path.endswith("report.pdf")


def test_tind_download_uses_url_filename_fallback(
    requests_mock: req_mock.Mocker, tmp_path: pytest.TempPathFactory
) -> None:
    """tind_download falls back to extracting the filename from the URL."""
    url = f"{BASE_URL}/files/myfile/download"
    requests_mock.get(url, content=b"data", status_code=200)
    status, path = tind_download(url, str(tmp_path), api_key=API_KEY)
    assert status == 200
    assert "myfile" in path


def test_tind_download_raises_on_401(requests_mock: req_mock.Mocker) -> None:
    """tind_download raises AuthorizationError on HTTP 401."""
    url = f"{BASE_URL}/files/12345/download"
    requests_mock.get(url, status_code=401)
    with pytest.raises(AuthorizationError):
        tind_download(url, "/tmp", api_key=API_KEY)


def test_tind_download_non_200_returns_empty(requests_mock: req_mock.Mocker) -> None:
    """tind_download returns (status, '') for non-200, non-error responses."""
    url = f"{BASE_URL}/files/12345/download"
    requests_mock.get(url, status_code=404)
    status, path = tind_download(url, "/tmp", api_key=API_KEY)
    assert status == 404
    assert path == ""
