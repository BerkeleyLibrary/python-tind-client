# python-tind-client

Python library for interacting with the [TIND ILS](https://tind.io) API.

## Requirements

- Python 3.13+

## Installation

```bash
pip install python-tind-client
```

Install with optional development dependencies:

```bash
pip install "python-tind-client[dev]"    # test + lint + debug
pip install "python-tind-client[test]"   # pytest + requests-mock
pip install "python-tind-client[lint]"   # mypy + pydoclint + pylint
pip install "python-tind-client[debug]"  # debugpy
```

## Configuration

Create a `TINDClient` with explicit configuration values:

- `api_key` (required): Your TIND API token
- `api_url` (required): Base URL of the TIND instance (e.g. `https://tind.example.edu`)
- `default_storage_dir` (optional): Default output directory for downloaded files

## Usage

```python
from tind_client import TINDClient

client = TINDClient(
	api_key="your-token",
	api_url="https://tind.example.edu",
	default_storage_dir="/tmp",
)

# Fetch MARC metadata for a record
record = client.fetch_metadata("12345")
print(record["245"]["a"])  # title

# Download a file
path = client.fetch_file("https://tind.example.edu/files/12345/download")

# Search and retrieve PyMARC records
records = client.search("title:python programming", result_format="pymarc")
```

## Functional fetch API

The functions in `tind_client.fetch` are available for direct use and now accept
explicit credentials instead of a client object.

```python
from tind_client.fetch import fetch_metadata

record = fetch_metadata(
	"12345",
	api_key="your-token",
	api_url="https://tind.example.edu",
)
```

For most use cases, prefer `TINDClient` methods as the primary interface.

## Running tests

```bash
pytest
```

## License

MIT — © 2026 The Regents of the University of California
