# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- client method to write search results to an XML file, with validation against expected number of records to be written
- client method to return an iterator of XML records from a search, to support streaming results for large result sets

### Changed
- N/A

### Deprecated
- N/A

### Removed
- client method to return raw XML or pyMARC records from a search, in favor of separate methods for each result format and a streaming iterator method for XML results

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
