# python-tind-client

Python library for interacting with the [TIND DA](https://tind.io) API.

## Requirements

- Python 3.12+

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

Create a `TINDClient` with optional configuration values:

- `api_key` (optional): Your TIND API token. Falls back to the `TIND_API_KEY` environment variable.
- `api_url` (optional): Base URL of the TIND instance (e.g. `https://tind.example.edu`). Falls back to the `TIND_API_URL` environment variable.

## Usage

### TIND Credentials / Optional ENV config
You will need to either pass your TIND API credentials as arguments when instantiating a `TINDClient` or set them as environment variables with the following names:
 - `TIND_API_KEY`
 - `TIND_API_URL`

### instantiate a client
```python
from tind_client import TINDClient

client = TINDClient(
	api_key="your-token",
	api_url="https://tind.example.edu",
)
```

### Fetch pyMARC metadata for a record
```python
record = client.fetch_metadata("116262")
print(record["245"]["a"])  # title
```

### Fetch file metadata for a record
```python
metadata = client.fetch_file_metadata("116262")
print(metadata[0])         # first file metadata dict
print(metadata[0]["url"])  # file download URL
```

### Download a file
```python
# use metadata from previous example
path_to_download = client.fetch_file(metadata[0]["url"])
```

### Search for records
```python
# return a list of record IDs matching a query
ids = client.fetch_ids_search("collection:'Disabled Students Program Photos'")

# return PyMARC records matching a query
records = client.fetch_search_metadata("collection:'Disabled Students Program Photos'")

# return raw XML or PyMARC records from a paginated search
# NOTE: for large result sets, use the write_search_results_to_file() method and then parse that file
xml_results = client.search("collection:'Disabled Students Program Photos'", result_format="xml")
pymarc_results = client.search("collection:'Disabled Students Program Photos'", result_format="pymarc")

# search Tind with a query and write results to an XML file
records_written = client.write_search_results_to_file("Old Emperor Norton", "full_norton_results.xml", output_dir="/data")
```

## Running tests

```bash
pytest
```

## License

MIT — © 2026 The Regents of the University of California
