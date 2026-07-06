"""sync_index tests: the INDEX is the source of truth — reconcile, re-fetch, restore."""

import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from docs_for_ai.errors import CurationError
from docs_for_ai.index_io import PLACEHOLDER_DESCRIPTION, write_index
from docs_for_ai.sync_index import (
    delete_orphan_files,
    files_needing_description,
    format_descriptions_status,
    get_changed_curated_files,
    main,
    restore_unchanged_descriptions,
)


def make_source(local_file: str, source_url: str, description: str) -> dict[str, str]:
    return {
        "title": local_file,
        "description": description,
        "source_url": source_url,
        "local_file": local_file,
    }


def create_index_xml(index_path: Path, sources: list[dict[str, str]]) -> None:
    root = ET.Element("docs_index")
    for source_data in sources:
        source = ET.SubElement(root, "source")
        ET.SubElement(source, "title").text = source_data["title"]
        ET.SubElement(source, "description").text = source_data["description"]
        ET.SubElement(source, "source_url").text = source_data["source_url"]
        ET.SubElement(source, "local_file").text = source_data["local_file"]
        ET.SubElement(source, "curated_at").text = "2025-01-01"

    write_index(root, index_path)


def read_descriptions_by_file(index_path: Path) -> dict[str, str]:
    root = ET.parse(index_path).getroot()
    return {
        source.findtext("local_file", ""): source.findtext("description", "")
        for source in root.findall("source")
    }


def read_sources_by_file(index_path: Path) -> dict[str, str]:
    root = ET.parse(index_path).getroot()
    return {
        source.findtext("local_file", ""): source.findtext("source_url", "")
        for source in root.findall("source")
    }


def init_git_repo(repo_dir: Path) -> None:
    for cmd in [
        ["git", "init"],
        ["git", "config", "user.email", "test@example.com"],
        ["git", "config", "user.name", "Test User"],
    ]:
        subprocess.run(cmd, cwd=repo_dir, check=True, capture_output=True)


def git_commit_all(repo_dir: Path, message: str) -> None:
    subprocess.run(["git", "add", "."], cwd=repo_dir, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", message], cwd=repo_dir, check=True, capture_output=True
    )


def run_sync(
    collection_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> str:
    """Run `sync-index <collection_dir>` in-process and return its stdout."""
    monkeypatch.setattr("sys.argv", ["sync-index", str(collection_dir)])
    main()
    return capsys.readouterr().out


def test_delete_orphan_files_removes_only_unindexed_unprotected_files(
    tmp_path: Path,
) -> None:
    survivors = {"doc-a.md", "README.md", "INDEX.xml", ".gitkeep"}
    orphans = {"orphan.md", "notes.txt"}
    for name in survivors | orphans:
        (tmp_path / name).write_text("content")

    deleted = delete_orphan_files(tmp_path, {"doc-a.md"})

    assert sorted(deleted) == sorted(orphans)
    assert {p.name for p in tmp_path.iterdir()} == survivors


def test_changed_files_reports_only_indexed_files_with_content_changes(
    tmp_path: Path,
) -> None:
    collection_dir = tmp_path / "collection"
    collection_dir.mkdir()
    init_git_repo(tmp_path)

    indexed_changed = collection_dir / "indexed-changed.md"
    indexed_whitespace = collection_dir / "indexed-whitespace.md"
    stray = collection_dir / "stray.md"
    for doc in (indexed_changed, indexed_whitespace, stray):
        doc.write_text("# Doc\n\nOriginal content.\n")
    git_commit_all(tmp_path, "Initial commit")

    indexed_changed.write_text("# Doc\n\nRewritten content.\n")
    # Whitespace-only edit: git diff -w must report no change.
    indexed_whitespace.write_text("# Doc\n\nOriginal content.   \n")
    stray.write_text("# Doc\n\nRewritten content.\n")  # not indexed: out of scope

    indexed = {"indexed-changed.md", "indexed-whitespace.md"}
    assert get_changed_curated_files(collection_dir, indexed) == {"indexed-changed.md"}


def test_restore_replaces_placeholders_only_from_real_originals_of_unchanged_files(
    tmp_path: Path,
) -> None:
    """Restore iff the file is unchanged and its original description is real."""
    original_descriptions = {
        "unchanged.md": "Original A",
        "changed.md": "Original B",
        "still-pending.md": PLACEHOLDER_DESCRIPTION,
    }

    index_path = tmp_path / "INDEX.xml"
    create_index_xml(
        index_path,
        [
            make_source("unchanged.md", "https://example.com/a", PLACEHOLDER_DESCRIPTION),
            make_source("changed.md", "https://example.com/b", PLACEHOLDER_DESCRIPTION),
            make_source(
                "still-pending.md", "https://example.com/c", PLACEHOLDER_DESCRIPTION
            ),
        ],
    )

    restored = restore_unchanged_descriptions(
        index_path, original_descriptions, {"changed.md"}
    )

    assert restored == 1
    descriptions = read_descriptions_by_file(index_path)
    assert descriptions["unchanged.md"] == "Original A"
    assert descriptions["changed.md"] == PLACEHOLDER_DESCRIPTION
    assert descriptions["still-pending.md"] == PLACEHOLDER_DESCRIPTION


def test_files_needing_description_returns_only_placeholder_sources(
    tmp_path: Path,
) -> None:
    index_path = tmp_path / "INDEX.xml"
    create_index_xml(
        index_path,
        [
            make_source("described.md", "https://example.com/a", "Real description"),
            make_source("pending.md", "https://example.com/b", PLACEHOLDER_DESCRIPTION),
        ],
    )

    assert files_needing_description(index_path) == {"pending.md"}


def test_status_lists_placeholder_files_as_home_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    home = tmp_path.resolve()
    monkeypatch.setattr(Path, "home", lambda: home)
    collection_dir = home / "repo" / "collections" / "shiny"

    output = format_descriptions_status(collection_dir, 0, {"b.md", "a.md"})

    assert "  - ~/repo/collections/shiny/a.md" in output
    assert "  - ~/repo/collections/shiny/b.md" in output


def test_status_omits_file_lines_when_no_placeholders() -> None:
    output = format_descriptions_status(Path("collections/shiny"), 3, set())

    assert "(needs description)|0 files" in output
    assert "  - " not in output


def test_sync_exits_with_clear_error_on_malformed_xml(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    index_path = tmp_path / "INDEX.xml"
    index_path.write_text("This is not XML at all")
    monkeypatch.setattr("sys.argv", ["sync-index", str(tmp_path)])

    with pytest.raises(SystemExit) as exc:
        main()

    assert exc.value.code == 1
    out = capsys.readouterr().out
    assert "Invalid XML" in out
    assert "INDEX.xml" in out


def test_sync_exits_when_collection_directory_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A non-existent collection dir aborts non-zero, naming the dir on stdout."""
    missing = tmp_path / "no-such-collection"
    monkeypatch.setattr("sys.argv", ["sync-index", str(missing)])

    with pytest.raises(SystemExit) as exc:
        main()

    assert exc.value.code == 1
    out = capsys.readouterr().out
    assert "Collection directory not found" in out
    assert str(missing) in out


def test_sync_exits_when_index_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A dir without INDEX.xml aborts non-zero, naming the missing index on stdout."""
    monkeypatch.setattr("sys.argv", ["sync-index", str(tmp_path)])

    with pytest.raises(SystemExit) as exc:
        main()

    assert exc.value.code == 1
    out = capsys.readouterr().out
    assert "Not a collection" in out
    assert str(tmp_path / "INDEX.xml") in out


def test_sync_deletes_orphan_file_and_keeps_indexed_docs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A real sync sweeps the orphan from disk while indexed and protected files stay."""
    collection_dir = tmp_path / "collection"
    collection_dir.mkdir()
    (collection_dir / "doc-a.md").write_text("# A")
    (collection_dir / "orphan.md").write_text("# Orphan")
    (collection_dir / "README.md").write_text("# Readme")
    create_index_xml(
        collection_dir / "INDEX.xml",
        [make_source("doc-a.md", "https://example.com/a", "Description A")],
    )
    monkeypatch.setattr("docs_for_ai.curate_doc.curate", lambda *_: None)

    out = run_sync(collection_dir, monkeypatch, capsys)

    assert not (collection_dir / "orphan.md").exists()
    assert (collection_dir / "doc-a.md").exists()
    assert (collection_dir / "README.md").exists()
    assert (collection_dir / "INDEX.xml").exists()
    assert "- Orphan files deleted (not in INDEX)|1" in out


@pytest.mark.parametrize(
    ("failure", "expected_error_line"),
    [
        (
            CurationError("Fetch failed: 404 not found — https://example.com/b"),
            "❌ Fetch failed: 404 not found — https://example.com/b",
        ),
        (RuntimeError("boom"), "❌ Unexpected error: RuntimeError: boom"),
    ],
    ids=["curation-error", "unexpected-crash"],
)
def test_sync_curates_each_source_in_process_and_isolates_failures(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    failure: Exception,
    expected_error_line: str,
) -> None:
    """A failed doc is reported, counted, and keeps its INDEX entry; sync completes."""
    collection_dir = tmp_path / "collection"
    collection_dir.mkdir()
    (collection_dir / "doc-a.md").write_text("# A")
    (collection_dir / "doc-b.md").write_text("# B")
    create_index_xml(
        collection_dir / "INDEX.xml",
        [
            make_source("doc-a.md", "https://example.com/a", "Description A"),
            make_source("doc-b.md", "https://example.com/b", "Description B"),
        ],
    )

    curated_urls: list[str] = []

    def fake_curate(_collection_dir: Path, source_url: str) -> None:
        curated_urls.append(source_url)
        if source_url == "https://example.com/b":
            raise failure

    monkeypatch.setattr("docs_for_ai.curate_doc.curate", fake_curate)

    out = run_sync(collection_dir, monkeypatch, capsys)

    assert curated_urls == ["https://example.com/a", "https://example.com/b"]
    assert "- Successful|1" in out
    assert "- Failed|1" in out
    assert "### Failed URLs\n- https://example.com/b" in out
    assert expected_error_line in out

    # The failed source survives untouched in INDEX.xml, ready for retry.
    index_path = collection_dir / "INDEX.xml"
    assert read_sources_by_file(index_path) == {
        "doc-a.md": "https://example.com/a",
        "doc-b.md": "https://example.com/b",
    }
    assert read_descriptions_by_file(index_path)["doc-b.md"] == "Description B"


def test_sync_fetches_missing_file_instead_of_pruning_entry(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    collection_dir = tmp_path / "collection"
    collection_dir.mkdir()
    create_index_xml(
        collection_dir / "INDEX.xml",
        [make_source("missing-doc.md", "https://example.com/missing", "Description")],
    )

    def fake_curate(target_dir: Path, _source_url: str) -> None:
        (target_dir / "missing-doc.md").write_text("# Fetched fresh")

    monkeypatch.setattr("docs_for_ai.curate_doc.curate", fake_curate)

    out = run_sync(collection_dir, monkeypatch, capsys)

    assert (collection_dir / "missing-doc.md").read_text() == "# Fetched fresh"
    assert read_sources_by_file(collection_dir / "INDEX.xml") == {
        "missing-doc.md": "https://example.com/missing"
    }
    assert "- Successful|1" in out


def test_sync_flags_fresh_fetched_placeholder_doc_in_status(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Fresh files are untracked, invisible to git diff — the 🚩 list must flag them."""
    collection_dir = tmp_path / "collection"
    collection_dir.mkdir()
    create_index_xml(
        collection_dir / "INDEX.xml",
        [
            make_source(
                "fresh-doc.md", "https://example.com/fresh", PLACEHOLDER_DESCRIPTION
            )
        ],
    )

    def fake_curate(target_dir: Path, _source_url: str) -> None:
        (target_dir / "fresh-doc.md").write_text("# Fetched fresh")

    monkeypatch.setattr("docs_for_ai.curate_doc.curate", fake_curate)

    out = run_sync(collection_dir, monkeypatch, capsys)

    status_section = out.split("## Index Descriptions Status")[1]
    assert "(needs description)|1 files" in status_section
    assert "fresh-doc.md" in status_section


@pytest.mark.firecrawl
def test_cli_recurate_keeps_or_restores_descriptions(tmp_path: Path) -> None:
    """Placeholder kept when content changed; description restored when unchanged."""
    collection_dir = tmp_path / "test_collection"
    collection_dir.mkdir()
    init_git_repo(tmp_path)

    index_path = collection_dir / "INDEX.xml"
    create_index_xml(
        index_path,
        [
            make_source(
                "learn-guides-updating-state.md",
                "https://zustand.docs.pmnd.rs/learn/guides/updating-state",
                "Original description for updating state",
            )
        ],
    )

    # Filename is derived from the source URL, so re-curate overwrites this file in place.
    (collection_dir / "learn-guides-updating-state.md").write_text(
        "# Dummy content to be replaced"
    )
    (collection_dir / "README.md").write_text("# Test Collection")
    git_commit_all(tmp_path, "Initial commit")

    result = subprocess.run(
        ["uv", "run", "sync-index", str(collection_dir)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0

    git_status = subprocess.run(
        ["git", "diff", "--name-only"],
        cwd=collection_dir,
        capture_output=True,
        text=True,
        check=True,
    )

    descriptions = read_descriptions_by_file(index_path)

    # Curated filename may differ from the seeded 'updating-state.md'.
    assert len(descriptions) == 1, "Should have exactly one source"
    actual_filename = next(iter(descriptions.keys()))

    md_files_changed = [
        line
        for line in git_status.stdout.split("\n")
        if line.endswith(".md") and not line.endswith("README.md")
    ]

    if md_files_changed:
        assert descriptions[actual_filename] == PLACEHOLDER_DESCRIPTION
        assert "✅ Restored (whitespace-only changes)|0" in result.stdout
    else:
        # Cache returned identical content, so the description was restored.
        assert descriptions[actual_filename] == "Original description for updating state"
        assert "✅ Restored (whitespace-only changes)|1" in result.stdout


@pytest.mark.github
def test_cli_refetches_github_blob_and_replaces_stale_content(tmp_path: Path) -> None:
    # Restore isn't asserted: outside the repo, sync_index.py's git-diff finds
    # no changed files and restores every description unconditionally.
    blob_url = (
        "https://github.com/astral-sh/uv/blob/main/docs/getting-started/first-steps.md"
    )
    local_file = "getting-started-first-steps.md"
    stale_sentinel = "STALE SENTINEL"

    collection_dir = tmp_path / "uv-test"
    collection_dir.mkdir()

    # Write the stale .md file — sync_index.py must overwrite this.
    (collection_dir / local_file).write_text(
        f"# {stale_sentinel}\n\nthis must be overwritten\n"
    )

    index_path = collection_dir / "INDEX.xml"
    create_index_xml(
        index_path,
        [make_source(local_file, blob_url, "Original curated description")],
    )

    result = subprocess.run(
        ["uv", "run", "sync-index", str(collection_dir)],
        capture_output=True,
        text=True,
        check=False,
    )

    # Signal 1: sync completed without error.
    assert result.returncode == 0, (
        f"sync_index.py exited {result.returncode}:\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )

    # Signal 2: stale sentinel is gone; real upstream content is present.
    md_text = (collection_dir / local_file).read_text()
    assert stale_sentinel not in md_text, (
        f"Stale sentinel still present in {local_file} — "
        "sync_index.py did not re-fetch from GitHub"
    )
    # The H1 is the doc's own title (not body prose), so it's stable
    # across upstream wording changes. Asserting it rejects HTML
    # rate-limit / error bodies that size heuristics would let through.
    assert "# First steps" in md_text, (
        "Re-fetched .md is missing the upstream H1 '# First steps' — "
        f"got a possible error page / wrong content:\n{md_text[:300]}"
    )

    # Signal 3: the source entry survives intact in INDEX.xml.
    final_sources = read_sources_by_file(index_path)
    assert final_sources == {local_file: blob_url}, (
        f"INDEX.xml entry lost or rewritten after sync.\nSources now: {final_sources}"
    )
