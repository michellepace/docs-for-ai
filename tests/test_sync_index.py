"""sync_index tests: INDEX.xml is the truth — reconcile, re-fetch, keep-if-unchanged."""

import subprocess
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

import pytest

from docs_for_ai import curate_doc
from docs_for_ai.errors import CurationError
from docs_for_ai.index_io import PLACEHOLDER_DESCRIPTION, write_index
from docs_for_ai.sync_index import format_descriptions_status, main


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


def set_index_description(index_path: Path, local_file: str, description: str) -> None:
    root = ET.parse(index_path).getroot()
    for source in root.findall("source"):
        desc_elem = source.find("description")
        if source.findtext("local_file") == local_file and desc_elem is not None:
            desc_elem.text = description
    write_index(root, index_path)


def run_sync(
    collection_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> str:
    """Run `sync-index <collection_dir>` in-process and return its stdout."""
    monkeypatch.setattr("sys.argv", ["sync-index", str(collection_dir)])
    main()
    return capsys.readouterr().out


def _forbid_scrape(_url: str, _max_attempts: int = 2) -> tuple[str, str]:
    """Stand in for `firecrawl_scrape.scrape` to prove the network is never touched."""
    msg = "FireCrawl must not be called during a sync test"
    raise AssertionError(msg)


def stub_fetches(
    monkeypatch: pytest.MonkeyPatch, docs: dict[str, str | Exception]
) -> None:
    """Serve canned content for https://example.com/* fetch URLs, offline.

    Keys are FETCH urls — the `append-md` rule fetches `<canonical>.md`.
    An Exception value is raised instead of returned.
    """

    def fetch(url: str) -> str:
        content = docs[url]
        if isinstance(content, Exception):
            raise content
        return content

    monkeypatch.setattr(
        curate_doc.direct_fetch,
        "load_direct_fetch_rules",
        lambda: {"append-md": ["https://example.com/"]},
    )
    monkeypatch.setattr(curate_doc.direct_fetch, "fetch_text", fetch)
    monkeypatch.setattr(curate_doc.firecrawl_scrape, "scrape", _forbid_scrape)


def create_collection(tmp_path: Path, doc_content: str, description: str) -> Path:
    """A collection holding one indexed doc ('doc.md') sourced from …/doc."""
    collection_dir = tmp_path / "collection"
    collection_dir.mkdir()
    (collection_dir / "doc.md").write_text(doc_content)
    create_index_xml(
        collection_dir / "INDEX.xml",
        [make_source("doc.md", "https://example.com/doc", description)],
    )
    return collection_dir


def test_status_lists_placeholder_files_as_home_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    home = tmp_path.resolve()
    monkeypatch.setattr(Path, "home", lambda: home)
    collection_dir = home / "repo" / "collections" / "shiny"

    output = format_descriptions_status(collection_dir, Counter(), 0, {"b.md", "a.md"})

    assert "  - ~/repo/collections/shiny/a.md" in output
    assert "  - ~/repo/collections/shiny/b.md" in output


def test_status_omits_file_lines_when_no_placeholders() -> None:
    output = format_descriptions_status(Path("collections/shiny"), Counter(), 0, set())

    assert "(needs description)|0 files" in output
    assert "  - " not in output


def test_status_prints_every_outcome_line_even_at_zero() -> None:
    output = format_descriptions_status(Path("collections/shiny"), Counter(), 0, set())

    assert "- ✅ Kept (content unchanged)|0" in output
    assert "- ✅ Kept (whitespace-only change)|0" in output
    assert "- ⚠️ Kept unverified (file recreated)|0" in output
    assert "- 🚩 Reset to PLACEHOLDER (content changed)|0" in output
    assert "- 🚩 New source (PLACEHOLDER)|0" in output
    assert "- ❌ Failed (description untouched)|0" in output


def test_sync_exits_when_collection_directory_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
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
    monkeypatch.setattr("sys.argv", ["sync-index", str(tmp_path)])

    with pytest.raises(SystemExit) as exc:
        main()

    assert exc.value.code == 1
    out = capsys.readouterr().out
    assert "Not a collection" in out
    assert str(tmp_path / "INDEX.xml") in out


def test_sync_exits_when_index_xml_malformed(
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


def test_sync_keeps_description_when_refetched_content_is_unchanged(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    collection_dir = create_collection(
        tmp_path, "# Doc\n\nStable content.\n", "Curated description"
    )
    stub_fetches(
        monkeypatch, {"https://example.com/doc.md": "# Doc\n\nStable content.\n"}
    )

    out = run_sync(collection_dir, monkeypatch, capsys)

    descriptions = read_descriptions_by_file(collection_dir / "INDEX.xml")
    assert descriptions["doc.md"] == "Curated description"
    assert "- ✅ Kept (content unchanged)|1" in out
    assert "(needs description)|0 files" in out


def test_sync_keeps_description_when_refetch_adds_only_blank_lines(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    collection_dir = create_collection(
        tmp_path, "# Doc\n\nStable content.\n", "Curated description"
    )
    # Inserted blank lines defeated `git diff -w`; whitespace-normalised compare must not.
    stub_fetches(
        monkeypatch, {"https://example.com/doc.md": "# Doc\n\n\n\nStable content.\n"}
    )

    out = run_sync(collection_dir, monkeypatch, capsys)

    descriptions = read_descriptions_by_file(collection_dir / "INDEX.xml")
    assert descriptions["doc.md"] == "Curated description"
    assert "- ✅ Kept (whitespace-only change)|1" in out
    assert "(needs description)|0 files" in out


def test_sync_resets_description_when_refetched_content_changed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """No git repo anywhere: change detection must not depend on git state."""
    collection_dir = create_collection(
        tmp_path, "# Doc\n\nOriginal content.\n", "Curated description"
    )
    stub_fetches(monkeypatch, {"https://example.com/doc.md": "# Doc\n\nRewritten.\n"})

    out = run_sync(collection_dir, monkeypatch, capsys)

    descriptions = read_descriptions_by_file(collection_dir / "INDEX.xml")
    assert descriptions["doc.md"] == PLACEHOLDER_DESCRIPTION
    assert "- 🚩 Reset to PLACEHOLDER (content changed)|1" in out
    status_section = out.split("## Index Descriptions Status")[1]
    assert "(needs description)|1 files" in status_section
    assert "doc.md" in status_section


def test_sync_flags_kept_placeholder_description(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    collection_dir = tmp_path / "collection"
    collection_dir.mkdir()
    create_index_xml(
        collection_dir / "INDEX.xml",
        [
            make_source(
                "fresh-doc.md", "https://example.com/fresh-doc", PLACEHOLDER_DESCRIPTION
            )
        ],
    )
    stub_fetches(monkeypatch, {"https://example.com/fresh-doc.md": "# Fetched fresh"})

    out = run_sync(collection_dir, monkeypatch, capsys)

    status_section = out.split("## Index Descriptions Status")[1]
    assert "(needs description)|1 files" in status_section
    assert "fresh-doc.md" in status_section


def test_sync_keeps_description_regenerated_after_reset(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    collection_dir = create_collection(
        tmp_path, "# Doc\n\nOld content.\n", "Old description"
    )
    stub_fetches(monkeypatch, {"https://example.com/doc.md": "# Doc\n\nNew content.\n"})
    run_sync(collection_dir, monkeypatch, capsys)  # content changed → PLACEHOLDER
    index_path = collection_dir / "INDEX.xml"
    set_index_description(index_path, "doc.md", "Generated after sync")

    out = run_sync(collection_dir, monkeypatch, capsys)

    assert read_descriptions_by_file(index_path)["doc.md"] == "Generated after sync"
    assert "- ✅ Kept (content unchanged)|1" in out


def test_sync_fetches_missing_file_instead_of_pruning_entry(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    collection_dir = tmp_path / "collection"
    collection_dir.mkdir()
    index_path = collection_dir / "INDEX.xml"
    create_index_xml(
        index_path,
        [make_source("missing-doc.md", "https://example.com/missing-doc", "Description")],
    )
    stub_fetches(monkeypatch, {"https://example.com/missing-doc.md": "# Fetched fresh"})

    out = run_sync(collection_dir, monkeypatch, capsys)

    assert (collection_dir / "missing-doc.md").read_text() == "# Fetched fresh"
    assert read_sources_by_file(index_path) == {
        "missing-doc.md": "https://example.com/missing-doc"
    }
    assert "- Successful|1" in out
    assert "- ⚠️ Kept unverified (file recreated)|1" in out
    assert read_descriptions_by_file(index_path)["missing-doc.md"] == "Description"


def test_sync_deletes_files_not_in_index_and_keeps_protected_files(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The survivors cover every keep rule: indexed doc, protected file, dotfile."""
    collection_dir = tmp_path / "collection"
    collection_dir.mkdir()
    survivors = {"doc-a.md", "README.md", "INDEX.xml", ".gitkeep"}
    orphans = {"orphan.md", "notes.txt"}
    for name in (survivors | orphans) - {"INDEX.xml"}:
        (collection_dir / name).write_text("content")
    create_index_xml(
        collection_dir / "INDEX.xml",
        [make_source("doc-a.md", "https://example.com/doc-a", "Description A")],
    )
    stub_fetches(monkeypatch, {"https://example.com/doc-a.md": "content"})

    out = run_sync(collection_dir, monkeypatch, capsys)

    assert {p.name for p in collection_dir.iterdir()} == survivors
    assert "- Orphan files deleted (not in INDEX)|2" in out


@pytest.mark.parametrize(
    ("failure", "expected_error_line"),
    [
        (
            CurationError("Fetch failed: 404 not found — https://example.com/doc-a"),
            "❌ Fetch failed: 404 not found — https://example.com/doc-a",
        ),
        (RuntimeError("boom"), "❌ Unexpected error: RuntimeError: boom"),
    ],
    ids=["curation-error", "unexpected-crash"],
)
def test_sync_keeps_index_entry_and_reports_url_when_fetch_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    failure: Exception,
    expected_error_line: str,
) -> None:
    """The first doc's failure doesn't abort the sync: the second doc still curates."""
    collection_dir = tmp_path / "collection"
    collection_dir.mkdir()
    (collection_dir / "doc-a.md").write_text("# A")
    (collection_dir / "doc-b.md").write_text("# B")
    create_index_xml(
        collection_dir / "INDEX.xml",
        [
            make_source("doc-a.md", "https://example.com/doc-a", "Description A"),
            make_source("doc-b.md", "https://example.com/doc-b", "Description B"),
        ],
    )
    stub_fetches(
        monkeypatch,
        {"https://example.com/doc-a.md": failure, "https://example.com/doc-b.md": "# B"},
    )

    out = run_sync(collection_dir, monkeypatch, capsys)

    assert "- Successful|1" in out
    assert "- Failed|1" in out
    assert "### Failed URLs\n- https://example.com/doc-a" in out
    assert expected_error_line in out
    assert "- ❌ Failed (description untouched)|1" in out

    # The failed source survives untouched in INDEX.xml, ready for retry.
    index_path = collection_dir / "INDEX.xml"
    assert read_sources_by_file(index_path) == {
        "doc-a.md": "https://example.com/doc-a",
        "doc-b.md": "https://example.com/doc-b",
    }
    assert read_descriptions_by_file(index_path)["doc-a.md"] == "Description A"


@pytest.mark.direct_fetch
def test_cli_refetches_github_blob_and_replaces_stale_content(tmp_path: Path) -> None:
    blob_url = (
        "https://github.com/astral-sh/uv/blob/main/docs/getting-started/first-steps.md"
    )
    local_file = "getting-started-first-steps.md"
    stale_sentinel = "STALE SENTINEL"

    collection_dir = tmp_path / "uv-test"
    collection_dir.mkdir()

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

    assert result.returncode == 0, (
        f"sync_index.py exited {result.returncode}:\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )

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

    final_sources = read_sources_by_file(index_path)
    assert final_sources == {local_file: blob_url}, (
        f"INDEX.xml entry lost or rewritten after sync.\nSources now: {final_sources}"
    )
    assert read_descriptions_by_file(index_path)[local_file] == PLACEHOLDER_DESCRIPTION, (
        "The sentinel guarantees a real content change, so the stale description "
        "must reset to PLACEHOLDER"
    )
