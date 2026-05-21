"""Tests for curate_doc.py script."""

import subprocess
import tempfile
from datetime import date
from pathlib import Path

import pytest

from scripts.curate_doc import resolve_filename

# Real Zustand page; used by integration tests that exercise the FireCrawl path.
TEST_URL = "https://zustand.docs.pmnd.rs/learn/guides/updating-state"


def _write_index(index_path: Path, entries: list[tuple[str, str, str]]) -> None:
    """Write a minimal INDEX.xml for resolver tests.

    Each entry is (title, source_url, local_file).
    """
    sources = "\n".join(
        f"  <source>\n"
        f"    <title>{title}</title>\n"
        f"    <description>PLACEHOLDER</description>\n"
        f"    <source_url>{url}</source_url>\n"
        f"    <local_file>{local_file}</local_file>\n"
        f"    <scraped_at>2026-05-19</scraped_at>\n"
        f"  </source>"
        for title, url, local_file in entries
    )
    index_path.write_text(f"<docs_index>\n{sources}\n</docs_index>\n")


class TestResolveFilename:
    """Offline unit tests for the unified filename resolver."""

    def test_returns_candidate_when_index_missing(self) -> None:
        """No INDEX.xml → candidate is returned unchanged."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            index_path = Path(tmp_dir) / "INDEX.xml"
            result = resolve_filename(
                index_path,
                "https://example.com/foo",
                "foo.md",
                on_collision="suffix",
            )
            assert result == "foo.md"

    def test_returns_candidate_when_free(self) -> None:
        """New URL with a free candidate filename → candidate used as-is."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            index_path = Path(tmp_dir) / "INDEX.xml"
            _write_index(
                index_path,
                [("Other", "https://example.com/other", "other.md")],
            )
            result = resolve_filename(
                index_path,
                "https://example.com/foo",
                "foo.md",
                on_collision="suffix",
            )
            assert result == "foo.md"

    def test_rescrape_preserves_assigned_filename(self) -> None:
        """Re-scrape of URL1 with sibling same-title sources keeps URL1's filename.

        Bug scenario: three sources titled "Foo" mapped to foo.md, foo-2.md,
        foo-3.md. Re-scraping URL1 must return foo.md (not foo-3.md, which
        would silently overwrite URL3's file).
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            index_path = Path(tmp_dir) / "INDEX.xml"
            _write_index(
                index_path,
                [
                    ("Foo", "https://example.com/foo1", "foo.md"),
                    ("Foo", "https://example.com/foo2", "foo-2.md"),
                    ("Foo", "https://example.com/foo3", "foo-3.md"),
                ],
            )
            result = resolve_filename(
                index_path,
                "https://example.com/foo1",
                "foo.md",
                on_collision="suffix",
            )
            assert result == "foo.md"

    def test_rescrape_match_ignores_trailing_slash(self) -> None:
        """source_url with/without trailing slash matches the stored entry."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            index_path = Path(tmp_dir) / "INDEX.xml"
            _write_index(
                index_path,
                [("Foo", "https://example.com/foo", "foo.md")],
            )
            result = resolve_filename(
                index_path,
                "https://example.com/foo/",
                "foo.md",
                on_collision="suffix",
            )
            assert result == "foo.md"

    def test_different_titles_same_slug_get_suffixed(self) -> None:
        """Distinct titles that slugify identically must not collide.

        Existing title "Foo Bar" → foo-bar.md. New URL with title "Foo-Bar"
        slugifies the same; resolver must return foo-bar-2.md, not silently
        accept foo-bar.md (which title-based counting misses).
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            index_path = Path(tmp_dir) / "INDEX.xml"
            _write_index(
                index_path,
                [("Foo Bar", "https://example.com/a", "foo-bar.md")],
            )
            result = resolve_filename(
                index_path,
                "https://example.com/b",
                "foo-bar.md",
                on_collision="suffix",
            )
            assert result == "foo-bar-2.md"

    def test_suffix_walks_past_existing_collisions(self) -> None:
        """Suffix mode picks the next free -N, not blindly count + 1."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            index_path = Path(tmp_dir) / "INDEX.xml"
            _write_index(
                index_path,
                [
                    ("Foo", "https://example.com/a", "foo.md"),
                    ("Foo", "https://example.com/b", "foo-2.md"),
                ],
            )
            result = resolve_filename(
                index_path,
                "https://example.com/c",
                "foo.md",
                on_collision="suffix",
            )
            assert result == "foo-3.md"

    def test_error_on_collision_exits(self, capsys: pytest.CaptureFixture[str]) -> None:
        """on_collision='error' (GitHub policy) exits 1 with FILENAME_COLLISION."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            index_path = Path(tmp_dir) / "INDEX.xml"
            _write_index(
                index_path,
                [("Old", "https://example.com/old", "first-steps.md")],
            )
            with pytest.raises(SystemExit) as exc_info:
                resolve_filename(
                    index_path,
                    "https://example.com/new",
                    "first-steps.md",
                    on_collision="error",
                )
            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "FILENAME_COLLISION" in (captured.out + captured.err)

    def test_rescrape_with_error_mode_returns_existing_filename(self) -> None:
        """Re-scrape under on_collision='error' returns existing filename, not exit.

        Guards against a future reordering of checks that might cause GitHub
        re-curation to spuriously trip the collision branch.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            index_path = Path(tmp_dir) / "INDEX.xml"
            _write_index(
                index_path,
                [("Foo", "https://example.com/foo", "foo.md")],
            )
            result = resolve_filename(
                index_path,
                "https://example.com/foo",
                "something-else.md",  # differs from stored "foo.md"
                on_collision="error",
            )
            assert result == "foo.md"

    def test_malformed_index_entries_are_skipped(self) -> None:
        """Sources missing source_url or local_file are skipped, not crashed on."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            index_path = Path(tmp_dir) / "INDEX.xml"
            index_path.write_text(
                "<docs_index>\n"
                "  <source>\n"
                "    <title>NoUrl</title>\n"
                "    <local_file>no-url.md</local_file>\n"
                "  </source>\n"
                "  <source>\n"
                "    <title>NoFile</title>\n"
                "    <source_url>https://example.com/no-file</source_url>\n"
                "  </source>\n"
                "  <source>\n"
                "    <title>Good</title>\n"
                "    <source_url>https://example.com/good</source_url>\n"
                "    <local_file>good.md</local_file>\n"
                "  </source>\n"
                "</docs_index>\n"
            )
            result = resolve_filename(
                index_path,
                "https://example.com/new",
                "good.md",  # collides with the well-formed entry
                on_collision="suffix",
            )
            assert result == "good-2.md"


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

    def test_fails_when_source_url_is_uv_docs_site(self) -> None:
        """Uv hosted-docs URLs are rejected."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            exit_code, output = run_script(
                tmp_dir, "https://docs.astral.sh/uv/guides/install-python/"
            )

            assert exit_code != 0
            assert "❌ Error: USE_RAW_GITHUB|" in output
            assert "uv/INDEX.xml" in output

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
            assert "🎉 Curation Success!|created and indexed new document|" in output1

            # Re-curating the SAME URL must UPDATE, not error.
            exit_code2, output2 = run_script(str(collection_dir), TEST_URL)
            assert exit_code2 == 0
            assert "✅ Updated index source|" in output2
            # Update-path success message
            assert "🎉 Curation Success!|overwrote and re-indexed document|" in output2

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


GH_RAW = (
    "https://raw.githubusercontent.com/astral-sh/uv/main/"
    "docs/getting-started/first-steps.md"
)
GH_BLOB = "https://github.com/astral-sh/uv/blob/main/docs/getting-started/first-steps.md"
GH_404 = (
    "https://raw.githubusercontent.com/astral-sh/uv/main/docs/zzz-does-not-exist-xyz.md"
)
GH_NON_MD = "https://github.com/astral-sh/uv/blob/main/pyproject.toml"


class TestGithubSourcePath:
    """Integration tests for GitHub raw-source routing (real network)."""

    @pytest.mark.github
    def test_raw_url_curates_into_collection(self) -> None:
        """Raw GitHub URL is detected, fetched, and routed end-to-end into INDEX + .md."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            new_dir = Path(tmp_dir) / "uv"
            exit_code, output = run_script(str(new_dir), GH_RAW)

            assert exit_code == 0
            assert "✅ Detected GitHub source|" in output
            assert "✅ Fetched raw markdown|" in output
            assert "🎉 Curation Success!|" in output

            doc = new_dir / "getting-started-first-steps.md"
            assert doc.exists()
            assert doc.read_text().strip() != ""

            index = (new_dir / "INDEX.xml").read_text()
            assert f"<source_url>{GH_RAW}</source_url>" in index
            assert "<local_file>getting-started-first-steps.md</local_file>" in index
            assert "<description>PLACEHOLDER</description>" in index

    @pytest.mark.github
    def test_blob_url_stored_normalised_to_raw(self) -> None:
        """Blob URL is normalised to raw URL before being stored in INDEX."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            new_dir = Path(tmp_dir) / "uv"
            exit_code, _ = run_script(str(new_dir), GH_BLOB)

            assert exit_code == 0
            index = (new_dir / "INDEX.xml").read_text()
            assert f"<source_url>{GH_RAW}</source_url>" in index

    @pytest.mark.github
    def test_404_fails_without_mutation(self) -> None:
        """404 URL exits non-zero with GITHUB_NOT_FOUND and leaves no files."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            new_dir = Path(tmp_dir) / "uv"
            exit_code, output = run_script(str(new_dir), GH_404)

            assert exit_code != 0
            assert "❌ Error: GITHUB_NOT_FOUND|" in output
            md_files = list(new_dir.glob("*.md")) if new_dir.exists() else []
            assert md_files == []
            assert not (new_dir / "INDEX.xml").exists()
            assert not (new_dir / "README.md").exists()

    def test_non_md_blob_rejected_before_fetch(self) -> None:
        """Non-markdown blob exits non-zero with UNSUPPORTED_GITHUB before any fetch."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            new_dir = Path(tmp_dir) / "uv"
            exit_code, output = run_script(str(new_dir), GH_NON_MD)

            assert exit_code != 0
            assert "❌ Error: UNSUPPORTED_GITHUB|" in output
            assert "✅ Fetched raw markdown|" not in output
            assert not (new_dir / "INDEX.xml").exists()
            assert not (new_dir / "README.md").exists()

    @pytest.mark.github
    def test_filename_collision_is_rejected(self) -> None:
        """Same filename + different URL is rejected (not silently overwritten)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            coll = Path(tmp_dir) / "uv"
            coll.mkdir()
            (coll / "getting-started-first-steps.md").write_text("# Old\n")
            (coll / "INDEX.xml").write_text(
                "<docs_index>\n"
                "  <source>\n"
                "    <title>Old</title>\n"
                "    <description>PLACEHOLDER</description>\n"
                "    <source_url>https://example.com/other</source_url>\n"
                "    <local_file>getting-started-first-steps.md</local_file>\n"
                "    <scraped_at>2026-05-19</scraped_at>\n"
                "  </source>\n"
                "</docs_index>\n"
            )
            exit_code, output = run_script(str(coll), GH_RAW)

            assert exit_code != 0
            assert "❌ Error: FILENAME_COLLISION|" in output


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
