"""update_descriptions.py: INDEX.xml description updates."""

from typing import TYPE_CHECKING

import pytest

from docs_for_ai.update_descriptions import (
    main,
    parse_descriptions_file,
    update_descriptions,
)

if TYPE_CHECKING:
    from pathlib import Path

INDEX_XML = """<docs_index>
  <source>
    <title>Doc A</title>
    <description>old description</description>
    <source_url>https://example.com/a</source_url>
    <local_file>doc-a.md</local_file>
    <curated_at>2025-01-01</curated_at>
  </source>
</docs_index>
"""


@pytest.fixture
def index_and_descriptions(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[Path, Path]:
    """A one-source INDEX.xml and a temp descriptions path, wired into sys.argv."""
    index_path = tmp_path / "INDEX.xml"
    index_path.write_text(INDEX_XML, encoding="utf-8")
    descriptions_file = tmp_path / "description.txt"
    monkeypatch.setattr(
        "sys.argv", ["update_descriptions.py", str(tmp_path), str(descriptions_file)]
    )
    return index_path, descriptions_file


def test_word_band_gates_whether_a_description_is_applied(
    index_and_descriptions: tuple[Path, Path],
) -> None:
    index_path, descriptions_file = index_and_descriptions

    # Out of band: aborts, leaving INDEX.xml and the temp file untouched
    descriptions_file.write_text("doc-a.md\nfar too short\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        main()
    assert "old description" in index_path.read_text(encoding="utf-8")
    assert descriptions_file.exists()

    # In band: applied
    descriptions_file.write_text(
        f"doc-a.md\n{' '.join(['word'] * 25)}\n", encoding="utf-8"
    )
    main()
    assert "old description" not in index_path.read_text(encoding="utf-8")


def test_one_out_of_band_entry_blocks_the_whole_batch(
    index_and_descriptions: tuple[Path, Path],
) -> None:
    index_path, descriptions_file = index_and_descriptions

    # doc-a is in band and matches the index; doc-b is out of band
    in_band = " ".join(["word"] * 25)
    descriptions_file.write_text(
        f"doc-a.md\n{in_band}\ndoc-b.md\ntoo short\n", encoding="utf-8"
    )

    with pytest.raises(SystemExit):
        main()

    # doc-a's valid update is withheld because a sibling failed validation
    assert "old description" in index_path.read_text(encoding="utf-8")


def test_replaces_description_for_matching_file(tmp_path: Path) -> None:
    index_path = tmp_path / "INDEX.xml"
    index_path.write_text(INDEX_XML, encoding="utf-8")

    updated_count = update_descriptions(index_path, {"doc-a.md": "new description"})

    assert updated_count == 1
    content = index_path.read_text(encoding="utf-8")
    assert "<description>new description</description>" in content
    assert "old description" not in content


def test_parse_pairs_lines_skipping_blanks_and_drops_unpaired_filename(
    tmp_path: Path,
) -> None:
    descriptions_file = tmp_path / "descriptions.txt"
    descriptions_file.write_text(
        "\n"
        "doc-a.md\n"
        "Description for A\n"
        "\n"
        "doc-b.md\n"
        "Description for B\n"
        "doc-c.md\n",  # trailing filename with no description is dropped
        encoding="utf-8",
    )

    result = parse_descriptions_file(descriptions_file)

    assert result == {"doc-a.md": "Description for A", "doc-b.md": "Description for B"}
