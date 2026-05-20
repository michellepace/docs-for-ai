"""Tests for sync_index.py script."""

import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from scripts.sync_index import (
    _get_changed_markdown_files,
    _restore_unchanged_descriptions,
    _sync_index_to_filesystem,
    get_markdown_files,
)


def create_index_xml(index_path: Path, sources: list[dict]) -> None:
    """Create INDEX.xml with given source entries."""
    root = ET.Element("docs_index")
    for source_data in sources:
        source = ET.SubElement(root, "source")
        ET.SubElement(source, "title").text = source_data["title"]
        ET.SubElement(source, "description").text = source_data["description"]
        ET.SubElement(source, "source_url").text = source_data["source_url"]
        ET.SubElement(source, "local_file").text = source_data["local_file"]
        ET.SubElement(source, "scraped_at").text = "2025-01-01"

    ET.indent(root, space="  ")
    tree = ET.ElementTree(root)
    tree.write(index_path, encoding="unicode", xml_declaration=False)


def get_descriptions_from_index(index_path: Path) -> dict[str, str]:
    """Parse INDEX.xml and return {local_file: description} mapping."""
    tree = ET.parse(index_path)
    root = tree.getroot()
    descriptions = {}

    for source in root.findall("source"):
        local_file_elem = source.find("local_file")
        desc_elem = source.find("description")
        if local_file_elem is not None and desc_elem is not None:
            descriptions[local_file_elem.text] = desc_elem.text

    return descriptions


class TestSyncIndexToFilesystem:
    """Tests for INDEX.xml sync logic."""

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
            valid_pairs, orphans, removed_count = _sync_index_to_filesystem(
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


class TestDescriptionRestorationUnit:
    """Unit tests for description restoration logic."""

    def test_unchanged_files_restore_descriptions(self) -> None:
        """All unchanged files get descriptions restored from backup."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            # Backup INDEX.xml (original descriptions)
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

            # Current INDEX.xml (all PLACEHOLDER after scraping)
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

            changed_files = set()

            restored = _restore_unchanged_descriptions(
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

            restored = _restore_unchanged_descriptions(
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

            # Two changed, two unchanged
            changed_files = {"doc-a.md", "doc-c.md"}

            restored = _restore_unchanged_descriptions(
                index_path, backup_path, changed_files
            )

            assert restored == 2
            descriptions = get_descriptions_from_index(index_path)
            assert descriptions["doc-a.md"] == "PLACEHOLDER"  # Changed
            assert descriptions["doc-b.md"] == "Original B"  # Unchanged
            assert descriptions["doc-c.md"] == "PLACEHOLDER"  # Changed
            assert descriptions["doc-d.md"] == "Original D"  # Unchanged

    def test_placeholder_backup_no_restoration(self) -> None:
        """Backup with PLACEHOLDER doesn't restore (new collection scenario)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            # Backup has PLACEHOLDER (first scrape)
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

            changed_files = set()

            restored = _restore_unchanged_descriptions(
                index_path, backup_path, changed_files
            )

            assert restored == 0
            descriptions = get_descriptions_from_index(index_path)
            assert descriptions["doc-a.md"] == "PLACEHOLDER"


class TestIntegration:
    """Integration tests using real git (scraping real or mocked)."""

    @pytest.mark.firecrawl
    def test_full_rescrape_workflow(self) -> None:
        """Full end-to-end workflow with real git and scraping."""
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

            # Create INDEX.xml with real scrape URL
            sources = [
                {
                    "title": "Updating State",
                    "description": "Original description for updating state",
                    "source_url": "https://zustand.docs.pmnd.rs/guides/updating-state",
                    "local_file": "updating-state.md",
                },
            ]
            index_path = collection_dir / "INDEX.xml"
            create_index_xml(index_path, sources)

            # Create dummy markdown file (will be overwritten by scrape)
            (collection_dir / "updating-state.md").write_text(
                "# Dummy content to be replaced"
            )
            (collection_dir / "README.md").write_text("# Test Collection")

            # Commit
            subprocess.run(
                ["git", "add", "."], cwd=tmp_path, check=True, capture_output=True
            )
            subprocess.run(
                ["git", "commit", "-m", "Initial commit"],
                cwd=tmp_path,
                check=True,
                capture_output=True,
            )

            # Run sync_index.py
            result = subprocess.run(
                ["uv", "run", "python", "scripts/sync_index.py", str(collection_dir)],
                capture_output=True,
                text=True,
                check=False,
            )

            assert result.returncode == 0

            # Check if git detected changes
            git_status = subprocess.run(
                ["git", "diff", "--name-only"],
                cwd=collection_dir,
                capture_output=True,
                text=True,
                check=True,
            )

            descriptions = get_descriptions_from_index(index_path)

            # Filename may differ from the seeded 'updating-state.md' if the real
            # scrape produced a different title-slug.
            assert len(descriptions) == 1, "Should have exactly one source"
            actual_filename = next(iter(descriptions.keys()))

            md_files_changed = [
                line
                for line in git_status.stdout.split("\n")
                if line.endswith(".md") and not line.endswith("README.md")
            ]

            # Verify correct behaviour based on whether content changed
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

    def test_whitespace_only_changes_restore_description(self) -> None:
        """Files with only whitespace changes should have descriptions restored."""
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

            # Create INDEX.xml with a source
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

            # Commit initial state
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

            # Mock the scraping by manually setting description to PLACEHOLDER
            # (simulating what curate_doc.py does)
            sources[0]["description"] = "PLACEHOLDER"
            create_index_xml(index_path, sources)

            # Create a backup (simulating what sync_index does)
            backup_path = index_path.parent / "INDEX.xml.backup"
            sources[0]["description"] = "Original description that should be restored"
            create_index_xml(backup_path, sources)

            # Run the restoration function directly
            changed_files = _get_changed_markdown_files(collection_dir)
            restored_count = _restore_unchanged_descriptions(
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


class TestErrorHandling:
    """Tests for error handling and validation."""

    def test_malformed_xml_exits_with_clear_error(self) -> None:
        """Malformed INDEX.xml exits with parse error."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            # Create invalid XML
            index_path = tmp_path / "INDEX.xml"
            index_path.write_text("This is not XML at all")

            # Run sync_index.py
            result = subprocess.run(
                ["uv", "run", "python", "scripts/sync_index.py", str(tmp_path)],
                capture_output=True,
                text=True,
                check=False,
            )

            assert result.returncode != 0
            assert "❌ Error: INVALID_XML|" in result.stdout + result.stderr
            assert "INDEX.xml" in result.stdout + result.stderr
