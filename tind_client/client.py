"""
TINDClient — the main entry point for interacting with the TIND DA API.
"""

import json
import os
import re
from io import StringIO
from typing import Any, Iterator
import xml.etree.ElementTree as E

from pymarc import Record
from pymarc.marcxml import parse_xml_to_array

from .api import tind_get, tind_download
from .errors import RecordNotFoundError, TINDError


NS = "http://www.loc.gov/MARC21/slim"
E.register_namespace("", NS)

# remove namespace that ElementTree adds to records when passed
_NS_DECL: str = f' xmlns="{NS}"'

class TINDClient:
    """Client for interacting with a TIND DA instance.

    :param str api_key: Your TIND API token.
    :param str api_url: Base URL of the TIND instance, e.g. ``https://tind.example.edu``.
    :param str default_storage_dir: Default directory used by :meth:`fetch_file`
                                    when no ``output_dir`` is supplied.
    """

    def __init__(
        self,
        api_key: str = "",
        api_url: str = "",
        default_storage_dir: str = "./tmp",
    ) -> None:
        self.api_key = api_key or os.environ.get("TIND_API_KEY", "")
        self.api_url = api_url or os.environ.get("TIND_API_URL", "")
        self.default_storage_dir = default_storage_dir

    def fetch_metadata(self, record: str) -> Record:
        """Fetch the MARC XML metadata for a given record.

        :param str record: The record ID for which to fetch metadata.
        :raises AuthorizationError: When the TIND API key is invalid.
        :raises RecordNotFoundError: When the record ID is invalid or not found.
        :returns Record: A PyMARC MARC record of the requested record.
        """
        status, response = tind_get(
            f"record/{record}/",
            api_key=self.api_key,
            api_url=self.api_url,
            params={"of": "xm"},
        )
        if status == 404 or len(response.strip()) == 0:
            raise RecordNotFoundError(f"Record {record} not found in TIND.")

        records: list[Record] = parse_xml_to_array(StringIO(response))
        # When the record does not match any records, we may receive a zero-length array of
        # records. Additionally, if the XML is malformed, the parser function may return
        # multiple records. We need to ensure that exactly one record is parsed.
        if len(records) != 1:
            raise RecordNotFoundError(
                f"Record {record} did not match exactly one record in TIND."
            )

        return records[0]

    def fetch_file(self, file_url: str, output_dir: str = "") -> str:
        """Download a file from TIND and save it locally.

        :param str file_url: The TIND file download URL.
        :param str output_dir: Directory in which to save the file.
                               Falls back to ``default_storage_dir`` when empty.
        :raises AuthorizationError: When the TIND API key is invalid or the file is restricted.
        :raises ValueError: When ``file_url`` is not a valid TIND file download URL.
        :raises RecordNotFoundError: When the file is invalid or not found.
        :returns str: The full path to the locally saved file.
        """
        if not re.match(r"^http.*/download(/)?(\?version=\d+)?$", file_url):
            raise ValueError("URL is not a valid TIND file download URL.")

        output_target = output_dir or self.default_storage_dir
        (status, saved_to) = tind_download(
            file_url, output_dir=output_target, api_key=self.api_key
        )

        if status != 200:
            raise RecordNotFoundError("Referenced file could not be downloaded.")

        return saved_to

    def fetch_file_metadata(self, record: str) -> list[dict[str, Any]]:
        """Fetch file metadata for a given TIND record.

        :param str record: The record ID in TIND to fetch file metadata for.
        :raises AuthorizationError: When the TIND API key is invalid.
        :raises TINDError: For any response other than 200.
        :returns list: A list of file metadata dicts for the given record.
        """
        status, files = tind_get(
            f"record/{record}/files", api_key=self.api_key, api_url=self.api_url
        )

        if status != 200:
            raise TINDError.from_json(status, files)

        return json.loads(files)  # type: ignore[no-any-return]

    def fetch_ids_search(self, query: str) -> list[str]:
        """Return a list of TIND record IDs matching a search query.

        :param str query: The query string to search for in TIND.
        :returns list[str]: A list of TIND record IDs.
        """
        status, rec_ids = tind_get(
            "search", api_key=self.api_key, api_url=self.api_url, params={"p": query}
        )

        if status != 200:
            raise TINDError.from_json(status, rec_ids)

        j = json.loads(rec_ids)
        hits = j.get("hits", []) if isinstance(j, dict) else []
        if not isinstance(hits, list):
            return []
        return [str(item) for item in hits]

    def fetch_marc_by_ids(self, ids: list[str]) -> list[Record]:
        """Fetch MARC records for a list of TIND record IDs.

        :param list[str] ids: The TIND record IDs to fetch.
        :returns list[Record]: A list of PyMARC records.
        """
        return [self.fetch_metadata(item) for item in ids]

    def fetch_search_metadata(self, query: str) -> list[Record]:
        """Return PyMARC records matching a search query.

        :param str query: The TIND search query.
        :returns list[Record]: A list of PyMARC records that match the given query.
        """
        ids = self.fetch_ids_search(query)
        return self.fetch_marc_by_ids(ids)

    def write_search_results_to_file(self, query: str, output_file_name: str = "tind.xml") -> int:
        """Search TIND and stream results to an XML file.
        
        :param str query: A TIND search query string.
        :param str output_file_name: filename for the output XML file.
        :returns int: The number of records written to the file.
        """
        total_hits = len(self.fetch_ids_search(query))
        recs_written = 0
        with open(self.default_storage_dir + "/" + output_file_name, "w", encoding="utf-8") as f:
            f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<collection xmlns="{NS}">\n')
            for record in self._iter_xml_records(query):
                record_xml = E.tostring(record, encoding="unicode")
                f.write(record_xml.replace(_NS_DECL, ""))
                f.write("\n")
                recs_written += 1

            f.write("</collection>\n")

        if recs_written != total_hits:
            raise TINDError(f"Expected {total_hits} records, but wrote {recs_written} to file.")
        return recs_written

    def _iter_xml_records(self, query: str) -> Iterator[E.Element]:
        """Yield every ``<record>`` element from all pages of a search.
        
        Issues the initial search request, then yields records one at a time,
        and continues to issue paginated search requests until all records have been yielded.
        :param str query: A TIND search query string.
        :yields: An iterator of XML elements representing the search results.
        """
        search_id: str | None = None

        while True:
            response = self._search_request(query, search_id=search_id)
            xml, search_id = self._retrieve_xml_search_id(response)
            collection = xml.find(f"{{{NS}}}collection")
            if collection is None or len(collection) == 0:
                break

            yield from collection

            if search_id is None:
                break

    def _search_request(self, query: str, *, search_id: str | None = None) -> str:
        """Retrieve a page of MARC data records.

        :param str query: The TIND search query.
        :param str|None search_id: The search_id for pagination.
        :returns str: A page of MARC records in XML format.
        """
        params: dict[str, str] = {"format": "xml", "p": query}
        if search_id:
            params["search_id"] = search_id

        status, response = tind_get(
            "search", api_key=self.api_key, api_url=self.api_url, params=params
        )

        if status != 200:
            raise TINDError(f"Status {status} while retrieving TIND record")

        return response

    def _retrieve_xml_search_id(self, response: str) -> tuple[E.Element, str]:
        """Parse a TIND search response and extract the pagination search_id.

        :param str response: The string returned from the TIND search call.
        :returns: A parsable XML element and the search ID for the next page.
        :rtype: tuple[xml.etree.ElementTree.Element, str]
        """
        E.register_namespace("", "http://www.loc.gov/MARC21/slim")
        xml = E.fromstring(response)
        search_id = xml.findtext("search_id", default="")

        return xml, search_id
