"""update_descriptions.py: INDEX.xml description updates."""

from typing import TYPE_CHECKING

from docs_for_ai.update_descriptions import update_descriptions

if TYPE_CHECKING:
    from pathlib import Path

INDEX_XML = """<docs_index>
  <source>
    <title>Doc A</title>
    <description>old description</description>
    <source_url>https://example.com/a</source_url>
    <local_file>doc-a.md</local_file>
    <scraped_at>2025-01-01</scraped_at>
  </source>
</docs_index>
"""


def test_replaces_description_for_matching_file(tmp_path: Path) -> None:
    """A source's description is replaced when its local_file matches."""
    index_path = tmp_path / "INDEX.xml"
    index_path.write_text(INDEX_XML, encoding="utf-8")

    updated_count = update_descriptions(index_path, {"doc-a.md": "new description"})

    assert updated_count == 1
    content = index_path.read_text(encoding="utf-8")
    assert "<description>new description</description>" in content
    assert "old description" not in content
