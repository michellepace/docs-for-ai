"""Tests for curate_doc.py script."""

import subprocess
import tempfile
from datetime import date
from pathlib import Path

import pytest

# Real Zustand page; used by integration tests that exercise the FireCrawl path.
TEST_URL = "https://zustand.docs.pmnd.rs/learn/guides/updating-state"


def run_script(*args: str, cwd: Path | None = None) -> tuple[int, str]:
    """Run curate_doc.py script via uv and return (exit_code, output)."""
    cmd = ["uv", "run", "python", "scripts/curate_doc.py"]
    cmd.extend(args)

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=cwd,
        check=False,
    )

    return result.returncode, result.stdout + result.stderr


class TestInputValidation:
    """Fast tests for argument, URL, and directory-state validation (no API calls)."""

    def test_requires_both_directory_and_url_arguments(self) -> None:
        """Argparse exits with usage code (2) when required args are missing."""
        exit_code, output = run_script()
        assert exit_code == 2
        assert "required" in output

    def test_fails_when_url_is_invalid(self) -> None:
        """Script rejects malformed URLs with INVALID_URL error."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            exit_code, output = run_script(tmp_dir, "horse-donkey-cow")

            assert exit_code != 0
            assert "❌ Error: INVALID_URL|horse-donkey-cow" in output

    def test_nonempty_noncollection_directory_fails(self) -> None:
        """Non-empty directory without INDEX.xml fails with INVALID_COLLECTION error."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            invalid_dir = tmp_path / "not_a_collection"

            invalid_dir.mkdir()
            (invalid_dir / "some_file.txt").write_text("random content")

            exit_code, output = run_script(str(invalid_dir), TEST_URL)

            assert exit_code != 0
            assert (
                "❌ Error: INVALID_COLLECTION|"
                "Directory non-empty and missing INDEX.xml. "
                "Rejected to prevent inadvertent file overwrites|"
            ) in output


@pytest.mark.firecrawl
class TestDirectoryScenarios:
    """Integration tests for different directory states (requires API)."""

    def test_nonexistent_directory_creates_new_collection(self) -> None:
        """Nonexistent target path is created (not just initialised in place)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            new_dir = tmp_path / "new_collection"

            exit_code, output = run_script(str(new_dir), TEST_URL)

            assert exit_code == 0

            readme_path = new_dir / "README.md"
            index_path = new_dir / "INDEX.xml"

            assert f"✅ Created curation readme|{readme_path}|" in output
            assert f"✅ Created curation index|{index_path}|" in output
            assert readme_path.exists()
            assert index_path.exists()

            # Filename is dynamic (derived from real scrape title); cannot hard-code.
            md_files = [
                f
                for f in new_dir.iterdir()
                if f.suffix == ".md" and f.name != "README.md"
            ]
            assert len(md_files) == 1
            assert md_files[0].name in output

            assert "✅ Added index source|" in output
            assert "🎉 Curation Success!|" in output

    def test_empty_directory_creates_new_collection(self) -> None:
        """Empty existing directory is initialised as a fresh collection."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            empty_dir = tmp_path / "empty_collection"

            empty_dir.mkdir()

            exit_code, output = run_script(str(empty_dir), TEST_URL)

            assert exit_code == 0

            readme_path = empty_dir / "README.md"
            index_path = empty_dir / "INDEX.xml"

            # Script outputs absolute paths for files outside project root
            assert f"✅ Created curation readme|{readme_path}|" in output
            assert f"✅ Created curation index|{index_path}|" in output
            assert readme_path.exists()
            assert index_path.exists()

            # Filename is dynamic (derived from real scrape title); cannot hard-code.
            md_files = [
                f
                for f in empty_dir.iterdir()
                if f.suffix == ".md" and f.name != "README.md"
            ]
            assert len(md_files) == 1

            assert "✅ Added index source|" in output
            assert "🎉 Curation Success!|" in output

    def test_existing_collection_adds_document_without_creating_readme(self) -> None:
        """Existing collection adds new document without creating README."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            existing_dir = tmp_path / "existing_collection"

            existing_dir.mkdir()
            index_path = existing_dir / "INDEX.xml"
            index_path.write_text("<docs_index>\n</docs_index>\n")
            (existing_dir / "existing_file.md").write_text("# Existing content")

            exit_code, output = run_script(str(existing_dir), TEST_URL)

            assert exit_code == 0

            # Filename is dynamic (derived from real scrape title); cannot hard-code.
            md_files = [
                f
                for f in existing_dir.iterdir()
                if f.suffix == ".md" and f.name not in ["README.md", "existing_file.md"]
            ]
            assert len(md_files) == 1

            assert "✅ Added index source|" in output
            assert "🎉 Curation Success!|" in output

            readme_path = existing_dir / "README.md"
            assert not readme_path.exists()
            readme_created_count = output.count("README.md")
            assert readme_created_count == 0

    def test_curating_same_url_twice_updates_existing_source(self) -> None:
        """Curating the same URL twice should update existing source, not fail.

        Also tests that URLs with/without trailing slashes are treated as the same URL.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            collection_dir = tmp_path / "test_collection"

            exit_code1, output1 = run_script(str(collection_dir), TEST_URL)
            assert exit_code1 == 0
            assert "✅ Added index source|" in output1
            # Add-path success message
            assert (
                "🎉 Curation Success!|scraped, created and indexed new document|"
                in output1
            )

            # Re-curating the SAME URL must UPDATE, not error.
            exit_code2, output2 = run_script(str(collection_dir), TEST_URL)
            assert exit_code2 == 0
            assert "✅ Updated index source|" in output2
            # Update-path success message
            assert (
                "🎉 Curation Success!|scraped, overwrote and re-indexed document|"
                in output2
            )

            index_path = collection_dir / "INDEX.xml"
            index_content = index_path.read_text()
            source_count = index_content.count("<source>")
            assert source_count == 1, f"Expected 1 source, found {source_count}"

            # Trailing-slash variant must hit the same UPDATE path.
            url_variant = (
                TEST_URL + "/" if not TEST_URL.endswith("/") else TEST_URL.rstrip("/")
            )
            exit_code3, output3 = run_script(str(collection_dir), url_variant)
            assert exit_code3 == 0
            assert "✅ Updated index source|" in output3

            # Verify STILL only ONE source entry (trailing slash normalized)
            index_content = index_path.read_text()
            source_count = index_content.count("<source>")
            assert source_count == 1, (
                f"Expected 1 source after slash variant, found {source_count}"
            )


@pytest.mark.firecrawl
class TestOutputContent:
    """Integration tests validating generated file content (requires API)."""

    def test_index_xml_structure_and_content(self) -> None:
        """New <source> entry uses PLACEHOLDER descrip (filled by sync_index later)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            new_dir = tmp_path / "test_collection"

            exit_code, _ = run_script(str(new_dir), TEST_URL)

            assert exit_code == 0

            index_path = new_dir / "INDEX.xml"
            index_content = index_path.read_text()

            today = date.today().isoformat()

            assert index_content.startswith("<docs_index>")
            assert "<source>\n" in index_content
            assert "<title>Updating state - Zustand</title>\n" in index_content
            assert "<description>PLACEHOLDER</description>\n" in index_content
            assert f"<source_url>{TEST_URL}</source_url>\n" in index_content
            assert "<local_file>updating-state-zustand.md</local_file>\n" in index_content
            assert f"<scraped_at>{today}</scraped_at>\n" in index_content
            assert "</source>\n" in index_content
            assert index_content.endswith("</docs_index>")

    def test_readme_md_contains_required_content(self) -> None:
        """Generated README links to INDEX.xml and back to the upstream source site."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            new_dir = tmp_path / "test_collection"

            exit_code, _ = run_script(str(new_dir), TEST_URL)

            assert exit_code == 0

            readme_path = new_dir / "README.md"
            readme_content = readme_path.read_text()

            assert "# test_collection Documentation" in readme_content
            assert "Curated docs for targeted AI context.\n" in readme_content
            assert "- Curation Index: [INDEX.xml](INDEX.xml)\n" in readme_content
            assert "- Curation Source: <https://zustand.docs.pmnd.rs>\n" in readme_content
