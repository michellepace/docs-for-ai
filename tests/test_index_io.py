"""index_io.py: shared INDEX.xml writing."""

import xml.etree.ElementTree as ET
from typing import TYPE_CHECKING

from docs_for_ai.index_io import write_index

if TYPE_CHECKING:
    from pathlib import Path


def test_write_index_ends_with_single_newline(tmp_path: Path) -> None:
    root = ET.Element("docs_index")
    ET.SubElement(root, "source")
    index_path = tmp_path / "INDEX.xml"

    write_index(root, index_path)

    content = index_path.read_text(encoding="utf-8")
    assert content.endswith("</docs_index>\n")
    assert not content.endswith("\n\n")


def test_write_index_indents_with_two_spaces(tmp_path: Path) -> None:
    root = ET.Element("docs_index")
    ET.SubElement(root, "source")
    index_path = tmp_path / "INDEX.xml"

    write_index(root, index_path)

    assert "\n  <source" in index_path.read_text(encoding="utf-8")
