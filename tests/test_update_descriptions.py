"""update_descriptions.py: INDEX.xml description updates piped via stdin."""

import io
import subprocess
from typing import TYPE_CHECKING

import pytest

from docs_for_ai.index_io import DESCRIP_MAX_WORDS, DESCRIP_MIN_WORDS
from docs_for_ai.update_descriptions import main

if TYPE_CHECKING:
    from pathlib import Path


def words(count: int) -> str:
    return " ".join(["word"] * count)


IN_BAND = words(DESCRIP_MAX_WORDS)
NEED_BAND = f"need {DESCRIP_MIN_WORDS}-{DESCRIP_MAX_WORDS}"


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


@pytest.mark.parametrize(
    "word_count", [DESCRIP_MIN_WORDS, DESCRIP_MAX_WORDS], ids=["at-min", "at-max"]
)
def test_in_band_description_is_applied_with_success_verdict(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    word_count: int,
) -> None:
    index_path = make_collection(tmp_path, {"doc-a.md": "old description"})
    description = words(word_count)

    exit_code, out = run_cli(monkeypatch, capsys, tmp_path, f"doc-a.md|{description}\n")

    assert exit_code == 0
    assert f"✅ doc-a.md: {word_count} words" in out
    content = index_path.read_text(encoding="utf-8")
    assert f"<description>{description}</description>" in content
    assert "old description" not in content


@pytest.mark.parametrize(
    "word_count",
    [DESCRIP_MIN_WORDS - 1, DESCRIP_MAX_WORDS + 1],
    ids=["just-below-band", "just-above-band"],
)
def test_out_of_band_description_is_flagged_and_withheld(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    word_count: int,
) -> None:
    index_path = make_collection(tmp_path, {"doc-a.md": "old description"})
    description = words(word_count)

    exit_code, out = run_cli(monkeypatch, capsys, tmp_path, f"doc-a.md|{description}\n")

    assert exit_code == 1
    assert f"❌ doc-a.md: {word_count} words ({NEED_BAND})" in out
    assert "old description" in index_path.read_text(encoding="utf-8")


def test_out_of_band_entry_does_not_block_in_band_sibling(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    index_path = make_collection(tmp_path, {"doc-a.md": "old A", "doc-b.md": "old B"})

    exit_code, out = run_cli(
        monkeypatch, capsys, tmp_path, f"doc-a.md|{IN_BAND}\ndoc-b.md|too short\n"
    )

    # The per-file verdicts, exit 1, and closing steer drive the repair loop
    assert exit_code == 1
    assert f"✅ doc-a.md: {DESCRIP_MAX_WORDS} words" in out
    assert f"❌ doc-b.md: 2 words ({NEED_BAND})" in out
    assert "rerun with only those" in out

    content = index_path.read_text(encoding="utf-8")
    assert f"<description>{IN_BAND}</description>" in content
    assert "old B" in content


def test_repiping_an_identical_description_reports_unchanged_and_succeeds(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    make_collection(tmp_path, {"doc-a.md": IN_BAND})

    exit_code, out = run_cli(monkeypatch, capsys, tmp_path, f"doc-a.md|{IN_BAND}\n")

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
        monkeypatch, capsys, tmp_path, f"doc-missing.md|{IN_BAND}\n"
    )

    assert exit_code == 0
    assert "no updates needed" in out
    assert "old description" in index_path.read_text(encoding="utf-8")


def test_missing_index_reports_not_a_collection(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code, out = run_cli(monkeypatch, capsys, tmp_path, f"doc-a.md|{IN_BAND}\n")

    assert exit_code == 1
    assert "Not a collection" in out
    assert str(tmp_path / "INDEX.xml") in out


def test_blank_only_stdin_reports_no_descriptions(
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


def test_each_line_splits_on_first_pipe_trimming_spaces_and_skipping_blanks(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    index_path = make_collection(tmp_path, {"doc-a.md": "old A", "doc-b.md": "old B"})
    with_pipe = f"Run `a | b` to {words(DESCRIP_MIN_WORDS)}"

    run_cli(
        monkeypatch,
        capsys,
        tmp_path,
        f"\n doc-a.md | {IN_BAND} \n\ndoc-b.md|{with_pipe}\n",
    )

    content = index_path.read_text(encoding="utf-8")
    assert f"<description>{IN_BAND}</description>" in content
    assert f"<description>{with_pipe}</description>" in content


def test_line_without_pipe_fails_citing_its_line_number_and_writes_nothing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    index_path = make_collection(tmp_path, {"doc-a.md": "old A", "doc-b.md": "old B"})

    exit_code, out = run_cli(
        monkeypatch, capsys, tmp_path, f"\ndoc-a.md|{IN_BAND}\ndoc-b.md {IN_BAND}\n"
    )

    assert exit_code == 1
    assert f"❌ No '|' on line 3: doc-b.md {IN_BAND}" in out
    content = index_path.read_text(encoding="utf-8")
    assert "old A" in content
    assert "old B" in content


def test_cli_entry_point_propagates_exit_1_while_applying_in_band_sibling(
    tmp_path: Path,
) -> None:
    index_path = make_collection(tmp_path, {"doc-a.md": "old A", "doc-b.md": "old B"})

    result = subprocess.run(
        ["uv", "run", "update-descriptions", str(tmp_path)],
        input=f"doc-a.md|{IN_BAND}\ndoc-b.md|too short\n",
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert f"✅ doc-a.md: {DESCRIP_MAX_WORDS} words" in result.stdout
    assert f"❌ doc-b.md: 2 words ({NEED_BAND})" in result.stdout
    content = index_path.read_text(encoding="utf-8")
    assert f"<description>{IN_BAND}</description>" in content
    assert "old B" in content
