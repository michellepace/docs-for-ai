"""update_descriptions.py: INDEX.xml description updates from stdin."""

import io
from typing import TYPE_CHECKING

import pytest

from docs_for_ai.update_descriptions import main, parse_descriptions

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

IN_BAND = " ".join(["word"] * 25)


@pytest.fixture
def index_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A one-source INDEX.xml collection, wired into sys.argv."""
    index_path = tmp_path / "INDEX.xml"
    index_path.write_text(INDEX_XML, encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["update-descriptions", str(tmp_path)])
    return index_path


def pipe_stdin(monkeypatch: pytest.MonkeyPatch, text: str) -> None:
    monkeypatch.setattr("sys.stdin", io.StringIO(text))


def test_word_band_gates_whether_a_description_is_applied(
    index_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Out of band: rejected, INDEX.xml untouched
    pipe_stdin(monkeypatch, "doc-a.md\nfar too short\n")
    with pytest.raises(SystemExit):
        main()
    assert "old description" in index_path.read_text(encoding="utf-8")

    # In band: applied
    pipe_stdin(monkeypatch, f"doc-a.md\n{IN_BAND}\n")
    main()
    content = index_path.read_text(encoding="utf-8")
    assert f"<description>{IN_BAND}</description>" in content
    assert "old description" not in content


def test_out_of_band_entry_is_flagged_without_blocking_in_band_siblings(
    index_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    # doc-a is in band and matches the index; doc-b is out of band
    pipe_stdin(monkeypatch, f"doc-a.md\n{IN_BAND}\ndoc-b.md\ntoo short\n")

    with pytest.raises(SystemExit) as exc:
        main()

    # The per-file report names each verdict — the repair loop keys off these lines
    assert exc.value.code == 1
    out = capsys.readouterr().out
    assert "✅ doc-a.md: 25 words" in out
    assert "❌ doc-b.md: 2 words (need 20-30)" in out

    # doc-a's in-band update is applied; only doc-b needs a rewrite and rerun
    assert "old description" not in index_path.read_text(encoding="utf-8")


def test_unmatched_filename_applies_nothing_and_succeeds(
    index_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    # In-band words, but the local_file matches nothing in INDEX.xml
    pipe_stdin(monkeypatch, f"doc-missing.md\n{IN_BAND}\n")

    main()

    assert "No updates needed" in capsys.readouterr().out
    assert "old description" in index_path.read_text(encoding="utf-8")


def test_missing_index_reports_not_a_collection(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr("sys.argv", ["update-descriptions", str(tmp_path)])
    pipe_stdin(monkeypatch, f"doc-a.md\n{IN_BAND}\n")

    with pytest.raises(SystemExit) as exc:
        main()

    assert exc.value.code == 1
    out = capsys.readouterr().out
    assert "Not a collection" in out
    assert str(tmp_path / "INDEX.xml") in out


@pytest.mark.usefixtures("index_path")
def test_empty_stdin_reports_no_descriptions(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    pipe_stdin(monkeypatch, "\n\n")

    with pytest.raises(SystemExit) as exc:
        main()

    assert exc.value.code == 1
    assert "No descriptions found" in capsys.readouterr().out


@pytest.mark.usefixtures("index_path")
def test_interactive_run_without_piped_stdin_is_rejected(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    class InteractiveStdin(io.StringIO):
        def isatty(self) -> bool:
            return True

    monkeypatch.setattr("sys.stdin", InteractiveStdin())

    with pytest.raises(SystemExit) as exc:
        main()

    assert exc.value.code == 1
    assert "stdin" in capsys.readouterr().out


def test_parse_pairs_lines_skipping_blanks_and_drops_unpaired_filename() -> None:
    text = (
        "\n"
        "doc-a.md\n"
        "Description for A\n"
        "\n"
        "doc-b.md\n"
        "Description for B\n"
        "doc-c.md\n"  # trailing filename with no description is dropped
    )

    result = parse_descriptions(text)

    assert result == {"doc-a.md": "Description for A", "doc-b.md": "Description for B"}
