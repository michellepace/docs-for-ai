"""Shared test helpers: INDEX.xml description access and fetch-route tripwires."""

import xml.etree.ElementTree as ET
from typing import TYPE_CHECKING

from docs_for_ai.index_io import write_index

if TYPE_CHECKING:
    from pathlib import Path


def forbid_scrape(_url: str, _max_attempts: int = 2) -> tuple[str, str]:
    """Stand in for `firecrawl_scrape.scrape` to prove FireCrawl is never touched."""
    msg = "FireCrawl must not be called in this test"
    raise AssertionError(msg)


def forbid_fetch(_url: str) -> str:
    """Stand in for `direct_fetch.fetch_text` to prove direct fetch is never touched."""
    msg = "direct fetch must not be called in this test"
    raise AssertionError(msg)


def set_index_description(index_path: Path, local_file: str, description: str) -> None:
    root = ET.parse(index_path).getroot()
    for source in root.findall("source"):
        desc_elem = source.find("description")
        if source.findtext("local_file") == local_file and desc_elem is not None:
            desc_elem.text = description
    write_index(root, index_path)


def read_index_description(index_path: Path, local_file: str) -> str:
    root = ET.parse(index_path).getroot()
    for source in root.findall("source"):
        if source.findtext("local_file") == local_file:
            return source.findtext("description", "")
    return ""
