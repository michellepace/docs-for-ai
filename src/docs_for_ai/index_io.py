"""Shared INDEX.xml writing for the curation scripts."""

import xml.etree.ElementTree as ET
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def write_index(root: ET.Element, index_path: Path) -> None:
    """Write INDEX.xml with indentation and trailing newline (POSIX convention)."""
    ET.indent(root, space="  ")
    xml = ET.tostring(root, encoding="unicode")
    index_path.write_text(f"{xml}\n", encoding="utf-8")
