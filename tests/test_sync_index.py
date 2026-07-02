"""Tests for sync_index: pruning, description restore, and re-curate round-trips."""

import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from docs_for_ai.errors import CurationError
from docs_for_ai.index_io import PLACEHOLDER_DESCRIPTION, write_index
from docs_for_ai.sync_index import (
    delete_orphan_files,
    format_descriptions_status,
    get_changed_curated_files,
    main,
    prune_stale_index_sources,
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
    descriptions: dict[str, str] = {}

    for source in root.findall("source"):
        local_file_elem = source.find("local_file")
        desc_elem = source.find("description")
        if local_file_elem is None or desc_elem is None:
            continue
        local_file = local_file_elem.text
        description = desc_elem.text
        if local_file is not None and description is not None:
            descriptions[local_file] = description

    return descriptions


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


def test_prune_removes_stale_sources_and_keeps_existing(tmp_path: Path) -> None:
    (tmp_path / "doc-a.md").write_text("# Doc A")
    (tmp_path / "doc-b.md").write_text("# Doc B")

    sources = [
        make_source("doc-a.md", "https://example.com/a", "Description A"),
        make_source("doc-b.md", "https://example.com/b", "Description B"),
        make_source("gone-1.md", "https://example.com/stale1", "Stale"),
        make_source("gone-2.md", "https://example.com/stale2", "Stale"),
    ]
    index_path = tmp_path / "INDEX.xml"
    create_index_xml(index_path, sources)

    live_sources, removed_count = prune_stale_index_sources(index_path, tmp_path)

    assert removed_count == 2
    assert ("doc-a.md", "https://example.com/a") in live_sources
    assert ("doc-b.md", "https://example.com/b") in live_sources

    descriptions = read_descriptions_by_file(index_path)
    assert set(descriptions) == {"doc-a.md", "doc-b.md"}


def test_prune_keeps_arbitrary_extension_when_file_exists(tmp_path: Path) -> None:
    (tmp_path / "doc.abc").write_text("# x")
    index_path = tmp_path / "INDEX.xml"
    create_index_xml(index_path, [make_source("doc.abc", "https://e/doc.abc", "D")])

    live_sources, removed_count = prune_stale_index_sources(index_path, tmp_path)

    assert removed_count == 0
    assert {source.local_file for source in live_sources} == {"doc.abc"}


def test_delete_orphan_files_removes_unindexed_but_keeps_readme(tmp_path: Path) -> None:
    (tmp_path / "doc-a.md").write_text("# Doc A")
    (tmp_path / "orphan.md").write_text("# Orphan")
    (tmp_path / "README.md").write_text("# Readme")

    deleted = delete_orphan_files(tmp_path, {"doc-a.md"})

    assert deleted == ["orphan.md"]
    assert (tmp_path / "doc-a.md").exists()
    assert (tmp_path / "README.md").exists()
    assert not (tmp_path / "orphan.md").exists()


def test_changed_files_ignores_whitespace_only_edit(tmp_path: Path) -> None:
    collection_dir = tmp_path / "collection"
    collection_dir.mkdir()
    init_git_repo(tmp_path)

    md_file = collection_dir / "test-doc.md"
    md_file.write_text("# Test Document\n\nSome content here.\n")
    git_commit_all(tmp_path, "Initial commit")

    # Whitespace-only edit: git diff -w must report no change.
    md_file.write_text("# Test Document\n\nSome content here.   \n")

    assert get_changed_curated_files(collection_dir, {"test-doc.md"}) == set()


def test_changed_files_reports_only_indexed_files(tmp_path: Path) -> None:
    collection_dir = tmp_path / "collection"
    collection_dir.mkdir()
    init_git_repo(tmp_path)

    indexed_doc = collection_dir / "indexed-doc.md"
    stray_doc = collection_dir / "stray-doc.md"
    indexed_doc.write_text("# Indexed\n\nOriginal content.\n")
    stray_doc.write_text("# Stray\n\nOriginal content.\n")
    git_commit_all(tmp_path, "Initial commit")

    # Real content change to both files; only the indexed one is in scope.
    indexed_doc.write_text("# Indexed\n\nRewritten content.\n")
    stray_doc.write_text("# Stray\n\nRewritten content.\n")

    assert get_changed_curated_files(collection_dir, {"indexed-doc.md"}) == {
        "indexed-doc.md"
    }


def test_restore_replaces_placeholder_for_unchanged_file(tmp_path: Path) -> None:
    backup_path = tmp_path / "INDEX.xml.backup"
    create_index_xml(
        backup_path,
        [
            make_source("doc-a.md", "https://example.com/a", "Original A"),
            make_source("doc-b.md", "https://example.com/b", "Original B"),
        ],
    )

    index_path = tmp_path / "INDEX.xml"
    create_index_xml(
        index_path,
        [
            make_source("doc-a.md", "https://example.com/a", PLACEHOLDER_DESCRIPTION),
            make_source("doc-b.md", "https://example.com/b", PLACEHOLDER_DESCRIPTION),
        ],
    )

    restored = restore_unchanged_descriptions(index_path, backup_path, set())

    assert restored == 2
    descriptions = read_descriptions_by_file(index_path)
    assert descriptions["doc-a.md"] == "Original A"
    assert descriptions["doc-b.md"] == "Original B"


def test_restore_keeps_placeholder_for_changed_file(tmp_path: Path) -> None:
    backup_path = tmp_path / "INDEX.xml.backup"
    create_index_xml(
        backup_path, [make_source("doc-a.md", "https://example.com/a", "Original A")]
    )

    index_path = tmp_path / "INDEX.xml"
    create_index_xml(
        index_path,
        [make_source("doc-a.md", "https://example.com/a", PLACEHOLDER_DESCRIPTION)],
    )

    restored = restore_unchanged_descriptions(index_path, backup_path, {"doc-a.md"})

    assert restored == 0
    assert read_descriptions_by_file(index_path)["doc-a.md"] == PLACEHOLDER_DESCRIPTION


def test_restore_skips_when_backup_is_placeholder(tmp_path: Path) -> None:
    # A placeholder in the backup is not a real description, so nothing to restore.
    source = make_source("doc-a.md", "https://example.com/a", PLACEHOLDER_DESCRIPTION)

    backup_path = tmp_path / "INDEX.xml.backup"
    create_index_xml(backup_path, [source])

    index_path = tmp_path / "INDEX.xml"
    create_index_xml(index_path, [source])

    restored = restore_unchanged_descriptions(index_path, backup_path, set())

    assert restored == 0
    assert read_descriptions_by_file(index_path)["doc-a.md"] == PLACEHOLDER_DESCRIPTION


def test_status_lists_placeholder_files_as_home_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    home = tmp_path.resolve()
    monkeypatch.setattr(Path, "home", lambda: home)
    collection_dir = home / "repo" / "collections" / "shiny"

    output = format_descriptions_status(collection_dir, 0, {"b.md", "a.md"})

    assert "  - ~/repo/collections/shiny/a.md" in output
    assert "  - ~/repo/collections/shiny/b.md" in output


def test_status_omits_file_lines_when_nothing_changed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    home = tmp_path.resolve()
    monkeypatch.setattr(Path, "home", lambda: home)
    collection_dir = home / "repo" / "collections" / "shiny"

    output = format_descriptions_status(collection_dir, 3, set())

    assert "(needs description)|0 files" in output
    assert "  - " not in output


def test_cli_exits_with_clear_error_on_malformed_xml(tmp_path: Path) -> None:
    index_path = tmp_path / "INDEX.xml"
    index_path.write_text("This is not XML at all")

    result = subprocess.run(
        ["uv", "run", "sync-index", str(tmp_path)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "Invalid XML" in result.stdout + result.stderr
    assert "INDEX.xml" in result.stdout + result.stderr


def test_main_exits_when_collection_directory_missing(
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


def test_main_exits_when_index_missing(
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
    """One doc's failure is reported and counted; the sync still completes."""
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
    monkeypatch.setattr("sys.argv", ["sync-index", str(collection_dir)])

    main()

    out = capsys.readouterr().out
    assert curated_urls == ["https://example.com/a", "https://example.com/b"]
    assert "- Successful|1" in out
    assert "- Failed|1" in out
    assert "### Failed URLs\n- https://example.com/b" in out
    assert expected_error_line in out


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

    # Signal 3: source_url and local_file entries survive in INDEX.xml.
    final_index_text = index_path.read_text()
    assert f"<source_url>{blob_url}</source_url>" in final_index_text, (
        f"source_url missing from INDEX.xml after sync.\n"
        f"INDEX.xml contents:\n{final_index_text}"
    )
    assert f"<local_file>{local_file}</local_file>" in final_index_text, (
        f"local_file entry missing from INDEX.xml after sync.\n"
        f"INDEX.xml contents:\n{final_index_text}"
    )
