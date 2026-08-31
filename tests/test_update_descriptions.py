"""update_descriptions.py: INDEX.xml description updates piped via stdin."""

import io
import subprocess
from typing import TYPE_CHECKING

import pytest

from docs_for_ai.update_descriptions import main, parse_descriptions

if TYPE_CHECKING:
    from pathlib import Path


def words(count: int) -> str:
    return " ".join(["word"] * count)


IN_BAND = words(25)


class _InteractiveStdin(io.StringIO):
    def isatty(self) -> bool:
        return True


def make_collection(tmp_path: Path, descriptions_by_file: dict[str, str]) -> Path:
    """Write an INDEX.xml with one <source> per entry; return its path."""
    sources = "".join(
        "  <source>\n"
        f"    <title>{local_file}</title>\n"
        f"    <description>{description}</description>\n"
        f"    <source_url>https://example.com/{local_file}</source_url>\n"
        f"    <local_file>{local_file}</local_file>\n"
        "    <curated_at>2025-01-01</curated_at>\n"
        "  </source>\n"
        for local_file, description in descriptions_by_file.items()
    )
    index_path = tmp_path / "INDEX.xml"
    index_path.write_text(f"<docs_index>\n{sources}</docs_index>\n", encoding="utf-8")
    return index_path


def run_cli(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    collection_dir: Path,
    stdin_text: str = "",
    *,
    interactive: bool = False,
) -> tuple[int, str]:
    """Run main() with argv/stdin wired; return (exit_code, stdout)."""
    stdin = _InteractiveStdin(stdin_text) if interactive else io.StringIO(stdin_text)
    monkeypatch.setattr("sys.argv", ["update-descriptions", str(collection_dir)])
    monkeypatch.setattr("sys.stdin", stdin)
    exit_code = 0
    try:
        main()
    except SystemExit as exc:
        if exc.code is not None:  # bare sys.exit() means success, per CPython
            exit_code = exc.code if isinstance(exc.code, int) else 1
    return exit_code, capsys.readouterr().out


@pytest.mark.parametrize("word_count", [15, 30], ids=["at-min", "at-max"])
def test_in_band_description_is_applied_with_success_verdict(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    word_count: int,
) -> None:
    index_path = make_collection(tmp_path, {"doc-a.md": "old description"})
    description = words(word_count)

    exit_code, out = run_cli(
        monkeypatch, capsys, tmp_path, f"doc-a.md\n{description}\n"
    )

    assert exit_code == 0
    assert f"✅ doc-a.md: {word_count} words" in out
    content = index_path.read_text(encoding="utf-8")
    assert f"<description>{description}</description>" in content
    assert "old description" not in content


@pytest.mark.parametrize(
    "word_count", [14, 31], ids=["just-below-band", "just-above-band"]
)
def test_out_of_band_description_is_flagged_and_withheld(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    word_count: int,
) -> None:
    index_path = make_collection(tmp_path, {"doc-a.md": "old description"})
    description = words(word_count)

    exit_code, out = run_cli(
        monkeypatch, capsys, tmp_path, f"doc-a.md\n{description}\n"
    )

    assert exit_code == 1
    assert f"❌ doc-a.md: {word_count} words (need 15-30)" in out
    assert "old description" in index_path.read_text(encoding="utf-8")


def test_out_of_band_entry_does_not_block_in_band_sibling(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    index_path = make_collection(tmp_path, {"doc-a.md": "old A", "doc-b.md": "old B"})

    exit_code, out = run_cli(
        monkeypatch, capsys, tmp_path, f"doc-a.md\n{IN_BAND}\ndoc-b.md\ntoo short\n"
    )

    # The per-file verdicts, exit 1, and closing steer drive the repair loop
    assert exit_code == 1
    assert "✅ doc-a.md: 25 words" in out
    assert "❌ doc-b.md: 2 words (need 15-30)" in out
    assert "rerun with only those" in out

    # In-band doc-a is applied immediately; flagged doc-b keeps its old description
    content = index_path.read_text(encoding="utf-8")
    assert f"<description>{IN_BAND}</description>" in content
    assert "old B" in content


def test_repiping_an_identical_description_reports_unchanged_and_succeeds(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    make_collection(tmp_path, {"doc-a.md": IN_BAND})

    exit_code, out = run_cli(monkeypatch, capsys, tmp_path, f"doc-a.md\n{IN_BAND}\n")

    assert exit_code == 0
    assert "unchanged: doc-a.md" in out
    assert "no updates needed" in out


def test_unmatched_filename_applies_nothing_and_succeeds(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    index_path = make_collection(tmp_path, {"doc-a.md": "old description"})

    exit_code, out = run_cli(
        monkeypatch, capsys, tmp_path, f"doc-missing.md\n{IN_BAND}\n"
    )

    assert exit_code == 0
    assert "no updates needed" in out
    assert "old description" in index_path.read_text(encoding="utf-8")


def test_missing_index_reports_not_a_collection(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code, out = run_cli(monkeypatch, capsys, tmp_path, f"doc-a.md\n{IN_BAND}\n")

    assert exit_code == 1
    assert "Not a collection" in out
    assert str(tmp_path / "INDEX.xml") in out


def test_empty_stdin_reports_no_descriptions(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    make_collection(tmp_path, {"doc-a.md": "old description"})

    exit_code, out = run_cli(monkeypatch, capsys, tmp_path, "\n\n")

    assert exit_code == 1
    assert "No descriptions found" in out


def test_interactive_run_without_piped_stdin_is_rejected(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    make_collection(tmp_path, {"doc-a.md": "old description"})

    exit_code, out = run_cli(monkeypatch, capsys, tmp_path, interactive=True)

    assert exit_code == 1
    assert "No descriptions piped to stdin" in out


def test_parse_pairs_filename_and_description_lines_skipping_blanks() -> None:
    text = "\ndoc-a.md\nDescription for A\n\ndoc-b.md\nDescription for B\n"

    result = parse_descriptions(text)

    assert result == {"doc-a.md": "Description for A", "doc-b.md": "Description for B"}


def test_parse_warns_and_drops_trailing_filename_without_description(
    capsys: pytest.CaptureFixture[str],
) -> None:
    text = "doc-a.md\nDescription for A\ndoc-c.md\n"

    result = parse_descriptions(text)

    assert result == {"doc-a.md": "Description for A"}
    assert "no description for doc-c.md: skipping" in capsys.readouterr().out


def test_cli_entry_point_propagates_exit_1_while_applying_in_band_sibling(
    tmp_path: Path,
) -> None:
    index_path = make_collection(tmp_path, {"doc-a.md": "old A", "doc-b.md": "old B"})

    result = subprocess.run(
        ["uv", "run", "update-descriptions", str(tmp_path)],
        input=f"doc-a.md\n{IN_BAND}\ndoc-b.md\ntoo short\n",
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "✅ doc-a.md: 25 words" in result.stdout
    assert "❌ doc-b.md: 2 words (need 15-30)" in result.stdout
    content = index_path.read_text(encoding="utf-8")
    assert f"<description>{IN_BAND}</description>" in content
    assert "old B" in content
