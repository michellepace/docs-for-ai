"""sync_index.py: INDEX sync, description restore, and re-curate round-trips."""

import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from docs_for_ai.index_io import write_index
from docs_for_ai.sync_index import (
    format_descriptions_status,
    get_changed_markdown_files,
    get_markdown_files,
    restore_unchanged_descriptions,
    sync_index_to_filesystem,
)


class TestFormatDescriptionsStatus:
    """PLACEHOLDER files are listed as absolute `~/...` paths (CWD-independent)."""

    def test_placeholder_files_listed_as_home_relative_paths(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Each flagged file renders as `~/...`, regardless of the caller's CWD."""
        home = tmp_path.resolve()
        monkeypatch.setattr(Path, "home", lambda: home)
        collection_dir = home / "repo" / "collections" / "shiny"

        output = format_descriptions_status(collection_dir, 0, {"b.md", "a.md"})

        assert "  - ~/repo/collections/shiny/a.md" in output
        assert "  - ~/repo/collections/shiny/b.md" in output

    def test_no_file_lines_when_nothing_changed(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """With no PLACEHOLDER files, the report lists none and counts zero."""
        home = tmp_path.resolve()
        monkeypatch.setattr(Path, "home", lambda: home)
        collection_dir = home / "repo" / "collections" / "shiny"

        output = format_descriptions_status(collection_dir, 3, set())

        assert "(needs description)|0 files" in output
        assert "  - " not in output


def create_index_xml(index_path: Path, sources: list[dict[str, str]]) -> None:
    """Create INDEX.xml with given source entries."""
    root = ET.Element("docs_index")
    for source_data in sources:
        source = ET.SubElement(root, "source")
        ET.SubElement(source, "title").text = source_data["title"]
        ET.SubElement(source, "description").text = source_data["description"]
        ET.SubElement(source, "source_url").text = source_data["source_url"]
        ET.SubElement(source, "local_file").text = source_data["local_file"]
        ET.SubElement(source, "curated_at").text = "2025-01-01"

    write_index(root, index_path)


def get_descriptions_from_index(index_path: Path) -> dict[str, str]:
    """Parse INDEX.xml and return {local_file: description} mapping."""
    tree = ET.parse(index_path)
    root = tree.getroot()
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


class TestSyncIndexToFilesystem:
    """Stale sources are pruned from INDEX.xml; README.md is excluded."""

    def test_removes_stale_sources_and_keeps_valid(self) -> None:
        """Stale sources removed, valid sources kept."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            (tmp_path / "doc-a.md").write_text("# Doc A")
            (tmp_path / "doc-b.md").write_text("# Doc B")
            (tmp_path / "README.md").write_text("# Collection")

            # 4 sources: 2 valid, 2 missing from filesystem (stale).
            sources = [
                {
                    "title": "Doc A",
                    "description": "Description A",
                    "source_url": "https://example.com/a",
                    "local_file": "doc-a.md",
                },
                {
                    "title": "Doc B",
                    "description": "Description B",
                    "source_url": "https://example.com/b",
                    "local_file": "doc-b.md",
                },
                {
                    "title": "Stale 1",
                    "description": "Stale description",
                    "source_url": "https://example.com/stale1",
                    "local_file": "gone-1.md",
                },
                {
                    "title": "Stale 2",
                    "description": "Stale description",
                    "source_url": "https://example.com/stale2",
                    "local_file": "gone-2.md",
                },
            ]
            index_path = tmp_path / "INDEX.xml"
            create_index_xml(index_path, sources)

            md_files = get_markdown_files(tmp_path)
            valid_pairs, orphans, removed_count = sync_index_to_filesystem(
                index_path, md_files
            )

            assert removed_count == 2
            assert len(valid_pairs) == 2
            assert ("doc-a.md", "https://example.com/a") in valid_pairs
            assert ("doc-b.md", "https://example.com/b") in valid_pairs

            assert len(orphans) == 0

            descriptions = get_descriptions_from_index(index_path)
            assert len(descriptions) == 2
            assert "doc-a.md" in descriptions
            assert "doc-b.md" in descriptions
            assert "gone-1.md" not in descriptions
            assert "gone-2.md" not in descriptions

    def test_readme_excluded_from_markdown_files(self) -> None:
        """README.md excluded from markdown file set."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            (tmp_path / "doc-a.md").write_text("# Doc A")
            (tmp_path / "doc-b.md").write_text("# Doc B")
            (tmp_path / "README.md").write_text("# Collection")

            md_files = get_markdown_files(tmp_path)

            assert len(md_files) == 2
            assert "doc-a.md" in md_files
            assert "doc-b.md" in md_files
            assert "README.md" not in md_files


class TestDescriptionRestoration:
    """Backup descriptions are restored for unchanged files only."""

    def test_unchanged_files_restore_descriptions(self) -> None:
        """All unchanged files get descriptions restored from backup."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            backup_sources = [
                {
                    "title": "Doc A",
                    "description": "Original description for doc A",
                    "source_url": "https://example.com/a",
                    "local_file": "doc-a.md",
                },
                {
                    "title": "Doc B",
                    "description": "Original description for doc B",
                    "source_url": "https://example.com/b",
                    "local_file": "doc-b.md",
                },
            ]
            backup_path = tmp_path / "INDEX.xml.backup"
            create_index_xml(backup_path, backup_sources)

            # Current = all PLACEHOLDER (after curation)
            current_sources = [
                {
                    "title": "Doc A",
                    "description": "PLACEHOLDER",
                    "source_url": "https://example.com/a",
                    "local_file": "doc-a.md",
                },
                {
                    "title": "Doc B",
                    "description": "PLACEHOLDER",
                    "source_url": "https://example.com/b",
                    "local_file": "doc-b.md",
                },
            ]
            index_path = tmp_path / "INDEX.xml"
            create_index_xml(index_path, current_sources)

            changed_files: set[str] = set()

            restored = restore_unchanged_descriptions(
                index_path, backup_path, changed_files
            )

            assert restored == 2
            descriptions = get_descriptions_from_index(index_path)
            assert descriptions["doc-a.md"] == "Original description for doc A"
            assert descriptions["doc-b.md"] == "Original description for doc B"

    def test_changed_files_keep_placeholder(self) -> None:
        """Changed files keep PLACEHOLDER, not restored."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            backup_sources = [
                {
                    "title": "Doc A",
                    "description": "Original description A",
                    "source_url": "https://example.com/a",
                    "local_file": "doc-a.md",
                },
            ]
            backup_path = tmp_path / "INDEX.xml.backup"
            create_index_xml(backup_path, backup_sources)

            current_sources = [
                {
                    "title": "Doc A",
                    "description": "PLACEHOLDER",
                    "source_url": "https://example.com/a",
                    "local_file": "doc-a.md",
                },
            ]
            index_path = tmp_path / "INDEX.xml"
            create_index_xml(index_path, current_sources)

            changed_files = {"doc-a.md"}

            restored = restore_unchanged_descriptions(
                index_path, backup_path, changed_files
            )

            assert restored == 0
            descriptions = get_descriptions_from_index(index_path)
            assert descriptions["doc-a.md"] == "PLACEHOLDER"

    def test_mixed_changed_and_unchanged(self) -> None:
        """Mix of changed and unchanged files: restore only unchanged."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            backup_sources = [
                {
                    "title": "Doc A",
                    "description": "Original A",
                    "source_url": "https://example.com/a",
                    "local_file": "doc-a.md",
                },
                {
                    "title": "Doc B",
                    "description": "Original B",
                    "source_url": "https://example.com/b",
                    "local_file": "doc-b.md",
                },
                {
                    "title": "Doc C",
                    "description": "Original C",
                    "source_url": "https://example.com/c",
                    "local_file": "doc-c.md",
                },
                {
                    "title": "Doc D",
                    "description": "Original D",
                    "source_url": "https://example.com/d",
                    "local_file": "doc-d.md",
                },
            ]
            backup_path = tmp_path / "INDEX.xml.backup"
            create_index_xml(backup_path, backup_sources)

            current_sources = [s | {"description": "PLACEHOLDER"} for s in backup_sources]
            index_path = tmp_path / "INDEX.xml"
            create_index_xml(index_path, current_sources)

            changed_files = {"doc-a.md", "doc-c.md"}

            restored = restore_unchanged_descriptions(
                index_path, backup_path, changed_files
            )

            assert restored == 2
            descriptions = get_descriptions_from_index(index_path)
            assert descriptions["doc-a.md"] == "PLACEHOLDER"
            assert descriptions["doc-b.md"] == "Original B"
            assert descriptions["doc-c.md"] == "PLACEHOLDER"
            assert descriptions["doc-d.md"] == "Original D"

    def test_placeholder_backup_no_restoration(self) -> None:
        """Backup with PLACEHOLDER doesn't restore (new collection scenario)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            # Backup has PLACEHOLDER (first curation)
            backup_sources = [
                {
                    "title": "Doc A",
                    "description": "PLACEHOLDER",
                    "source_url": "https://example.com/a",
                    "local_file": "doc-a.md",
                },
            ]
            backup_path = tmp_path / "INDEX.xml.backup"
            create_index_xml(backup_path, backup_sources)

            current_sources = backup_sources.copy()
            index_path = tmp_path / "INDEX.xml"
            create_index_xml(index_path, current_sources)

            changed_files: set[str] = set()

            restored = restore_unchanged_descriptions(
                index_path, backup_path, changed_files
            )

            assert restored == 0
            descriptions = get_descriptions_from_index(index_path)
            assert descriptions["doc-a.md"] == "PLACEHOLDER"

    def test_whitespace_only_changes_restore_description(self) -> None:
        """Whitespace-only changes restore the description, not PLACEHOLDER."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            collection_dir = tmp_path / "test_collection"
            collection_dir.mkdir()

            # Initialise git repo
            for cmd in [
                ["git", "init"],
                ["git", "config", "user.email", "test@example.com"],
                ["git", "config", "user.name", "Test User"],
            ]:
                subprocess.run(cmd, cwd=tmp_path, check=True, capture_output=True)

            sources = [
                {
                    "title": "Test Document",
                    "description": "Original description that should be restored",
                    "source_url": "https://example.com/test-doc",
                    "local_file": "test-doc.md",
                },
            ]
            index_path = collection_dir / "INDEX.xml"
            create_index_xml(index_path, sources)

            md_file = collection_dir / "test-doc.md"
            md_file.write_text("# Test Document\n\nSome content here.\n")

            subprocess.run(
                ["git", "add", "."], cwd=tmp_path, check=True, capture_output=True
            )
            subprocess.run(
                ["git", "commit", "-m", "Initial commit"],
                cwd=tmp_path,
                check=True,
                capture_output=True,
            )

            # Modify file with ONLY whitespace changes (add trailing spaces)
            md_file.write_text("# Test Document\n\nSome content here.   \n")

            # Verify git sees a change
            git_diff_all = subprocess.run(
                ["git", "diff", "--name-only"],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                check=True,
            )
            assert "test-doc.md" in git_diff_all.stdout

            # Verify git with -w sees NO content change
            git_diff_w = subprocess.run(
                ["git", "diff", "-w"],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                check=True,
            )
            assert git_diff_w.stdout.strip() == ""

            # Simulate curate_doc.py's curation: set description to PLACEHOLDER
            sources[0]["description"] = "PLACEHOLDER"
            create_index_xml(index_path, sources)

            # Back up the original, as sync_index does
            backup_path = index_path.parent / "INDEX.xml.backup"
            sources[0]["description"] = "Original description that should be restored"
            create_index_xml(backup_path, sources)

            changed_files = get_changed_markdown_files(collection_dir)
            restored_count = restore_unchanged_descriptions(
                index_path, backup_path, changed_files
            )

            # Description must be RESTORED (whitespace-only diff), not PLACEHOLDER.
            descriptions = get_descriptions_from_index(index_path)
            expected_desc = "Original description that should be restored"
            assert descriptions["test-doc.md"] == expected_desc, (
                f"Expected description to be restored, "
                f"but got: {descriptions['test-doc.md']}"
            )
            assert restored_count == 1, f"Expected 1 restoration, got {restored_count}"


@pytest.mark.firecrawl
class TestIntegration:
    """Full re-curate through the sync_index.py CLI with real git and live FireCrawl."""

    def test_full_recurate_workflow(self) -> None:
        """PLACEHOLDER kept when content changed, restored when unchanged."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            collection_dir = tmp_path / "test_collection"
            collection_dir.mkdir()

            # Initialise git repo
            for cmd in [
                ["git", "init"],
                ["git", "config", "user.email", "test@example.com"],
                ["git", "config", "user.name", "Test User"],
            ]:
                subprocess.run(cmd, cwd=tmp_path, check=True, capture_output=True)

            sources = [
                {
                    "title": "Updating State",
                    "description": "Original description for updating state",
                    "source_url": "https://zustand.docs.pmnd.rs/learn/guides/updating-state",
                    "local_file": "learn-guides-updating-state.md",
                },
            ]
            index_path = collection_dir / "INDEX.xml"
            create_index_xml(index_path, sources)

            # Name matches filename_from_url(source_url) so re-curate overwrites it.
            (collection_dir / "learn-guides-updating-state.md").write_text(
                "# Dummy content to be replaced"
            )
            (collection_dir / "README.md").write_text("# Test Collection")

            subprocess.run(
                ["git", "add", "."], cwd=tmp_path, check=True, capture_output=True
            )
            subprocess.run(
                ["git", "commit", "-m", "Initial commit"],
                cwd=tmp_path,
                check=True,
                capture_output=True,
            )

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

            descriptions = get_descriptions_from_index(index_path)

            # Curated filename may differ from the seeded 'updating-state.md'.
            assert len(descriptions) == 1, "Should have exactly one source"
            actual_filename = next(iter(descriptions.keys()))

            md_files_changed = [
                line
                for line in git_status.stdout.split("\n")
                if line.endswith(".md") and not line.endswith("README.md")
            ]

            if md_files_changed:
                # Content changed → description is PLACEHOLDER
                assert descriptions[actual_filename] == "PLACEHOLDER"
                assert "✅ Restored (.md whitespace-only changes)|0" in result.stdout
            else:
                # Content unchanged (cache returned same) → description restored
                assert (
                    descriptions[actual_filename]
                    == "Original description for updating state"
                )
                assert "✅ Restored (.md whitespace-only changes)|1" in result.stdout


class TestErrorHandling:
    """Invalid input fails loud with a clear error and non-zero exit."""

    def test_malformed_xml_exits_with_clear_error(self) -> None:
        """Malformed INDEX.xml exits with parse error."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            index_path = tmp_path / "INDEX.xml"
            index_path.write_text("This is not XML at all")

            result = subprocess.run(
                ["uv", "run", "sync-index", str(tmp_path)],
                capture_output=True,
                text=True,
                check=False,
            )

            assert result.returncode != 0
            assert "❌ Error: INVALID_XML|" in result.stdout + result.stderr
            assert "INDEX.xml" in result.stdout + result.stderr


@pytest.mark.github
class TestGitHubBlobRoundTrip:
    """Live-network round-trip of a GitHub-blob source through sync_index.py."""

    def test_github_blob_entry_refetched_and_stale_content_replaced(self) -> None:
        """A GitHub-blob INDEX entry round-trips through unmodified sync_index.py."""
        # Restore isn't asserted: outside the repo, sync_index.py's git-diff finds
        # no changed files and restores every description unconditionally.
        blob_url = "https://github.com/astral-sh/uv/blob/main/docs/getting-started/first-steps.md"
        local_file = "getting-started-first-steps.md"
        stale_sentinel = "STALE SENTINEL"

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            collection_dir = tmp_path / "uv-test"
            collection_dir.mkdir()

            # Write the stale .md file — sync_index.py must overwrite this.
            (collection_dir / local_file).write_text(
                f"# {stale_sentinel}\n\nthis must be overwritten\n"
            )

            index_path = collection_dir / "INDEX.xml"
            create_index_xml(
                index_path,
                [
                    {
                        "title": "First steps",
                        "description": "Original curated description",
                        "source_url": blob_url,
                        "local_file": local_file,
                    }
                ],
            )

            # sync_index.py delegates to curate_doc.py's GitHub blob path.
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
