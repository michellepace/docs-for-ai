"""Shared INDEX.xml I/O and schema constants for the curation scripts."""

import xml.etree.ElementTree as ET
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

# Default <description> for a new/uncurated source
PLACEHOLDER_DESCRIPTION = "PLACEHOLDER"

DESCRIP_MIN_WORDS = 10
DESCRIP_MAX_WORDS = 30


def fits_word_band(description: str) -> bool:
    """Check the description word count is within range."""
    return DESCRIP_MIN_WORDS <= len(description.split()) <= DESCRIP_MAX_WORDS


def write_index(root: ET.Element, index_path: Path) -> None:
    """Write INDEX.xml with indentation and trailing newline (POSIX convention)."""
    ET.indent(root, space="  ")
    xml = ET.tostring(root, encoding="unicode")
    index_path.write_text(f"{xml}\n", encoding="utf-8")
