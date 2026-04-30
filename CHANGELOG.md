# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased - proposed 1.0.0?]

### Added
- `output_dir` parameter to `write_search_results_to_file`, defaulting to `./tmp`
- `fetch_file` now defaults `output_dir` to `./tmp` when not supplied

### Removed
- **BREAKING**: `default_storage_dir` constructor parameter removed from `TINDClient`; pass `output_dir` directly to `fetch_file` and `write_search_results_to_file` instead

## [0.2.2]

### Changed
- build package and publish to pypi, using setuptools_scm for version management

## [0.2.1]

### Changed
 - reconciling version agreement between the releases, this file, and the pyproject.toml

## [0.2.0]

### Added
- client method to write search results to an XML file, with validation against expected number of records to be written
- client method to return an iterator of XML records from a search, to support streaming results for large result sets
- xml fixture files for testing
- tests for the new client methods, including edge cases for validation

### Changed
- README examples

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A


## [0.1.1]

### Added
- N/A

### Changed
- Expand supported Python versions to include 3.12

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A


## [0.1.0]

### Added
- Implemented TINDClient to wrap API interactions
- Created tests, linting, and ci configurations

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A
