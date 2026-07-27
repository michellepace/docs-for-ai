"""Shared test helpers: INDEX.xml description access and fetch-route tripwires."""

import xml.etree.ElementTree as ET
from typing import TYPE_CHECKING

import pytest

from docs_for_ai import curate_doc
from docs_for_ai.index_io import write_index

if TYPE_CHECKING:
    from pathlib import Path


def forbid_scrape(_url: str, _max_attempts: int = 2) -> tuple[str, str]:
    """Stand in for `firecrawl_scrape.scrape` to prove FireCrawl is never touched."""
    # pytest.fail raises a BaseException, so `sync_index`'s catch-all lets it through.
    pytest.fail("FireCrawl must not be called in this test")


def forbid_fetch(_url: str) -> str:
    """Stand in for `direct_fetch.fetch_text` to prove direct fetch is never touched."""
    pytest.fail("direct fetch must not be called in this test")


def forbid_both_fetchers(monkeypatch: pytest.MonkeyPatch) -> None:
    """Forbid direct fetch and FireCrawl scrape alike for negative-path tests."""
    monkeypatch.setattr(curate_doc.direct_fetch, "fetch_text", forbid_fetch)
    monkeypatch.setattr(curate_doc.firecrawl_scrape, "scrape", forbid_scrape)


def _find_source(root: ET.Element, index_path: Path, local_file: str) -> ET.Element:
    """The <source> recording `local_file`; a miss fails loud, never no-ops."""
    for source in root.findall("source"):
        if source.findtext("local_file") == local_file:
            return source
    msg = f"no <source> with local_file {local_file!r} in {index_path}"
    raise AssertionError(msg)


def set_index_description(index_path: Path, local_file: str, description: str) -> None:
    root = ET.parse(index_path).getroot()
    desc_elem = _find_source(root, index_path, local_file).find("description")
    if desc_elem is None:
        msg = f"{local_file!r} has no <description> in {index_path}"
        raise AssertionError(msg)
    desc_elem.text = description
    write_index(root, index_path)


def read_index_description(index_path: Path, local_file: str) -> str:
    root = ET.parse(index_path).getroot()
    return _find_source(root, index_path, local_file).findtext("description", "")
