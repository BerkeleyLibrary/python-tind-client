"""
Shared pytest fixtures for python-tind-client tests.
"""

import pytest
from tind_client import TINDClient


SAMPLE_MARC_XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<collection xmlns="http://www.loc.gov/MARC21/slim">
  <record>
    <leader>00000nam a2200000 i 4500</leader>
    <controlfield tag="001">12345</controlfield>
    <datafield tag="245" ind1="1" ind2="0">
      <subfield code="a">Sample Title</subfield>
    </datafield>
  </record>
</collection>"""


@pytest.fixture
def tind_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set required TIND environment variables for a test."""
    monkeypatch.setenv("TIND_API_KEY", "test-api-key")
    monkeypatch.setenv("TIND_API_URL", "https://tind.example.edu")


@pytest.fixture
def sample_marc_xml() -> str:
    """Return a minimal, valid MARC XML string containing one record."""
    return SAMPLE_MARC_XML


@pytest.fixture
def client() -> TINDClient:
    """Return a configured TINDClient instance for tests."""
    return TINDClient(
        api_key="test-api-key",
        api_url="https://tind.example.edu",
    )
