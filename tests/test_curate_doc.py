"""Tests for curate_doc.py.

Offline tests cover the filename helper, validation, and `.md` routing; the
FireCrawl- and github-marked tests hit real networks.
"""

import subprocess
import tempfile
from datetime import date
from pathlib import Path

import pytest

from scripts import curate_doc
from scripts.curate_doc import filename_from_url

# Real Zustand page; used by integration tests that exercise the FireCrawl path.
TEST_URL = "https://zustand.docs.pmnd.rs/learn/guides/updating-state"

# Real GitHub URLs for the validation and end-to-end network tests below.
GH_BLOB = "https://github.com/astral-sh/uv/blob/main/docs/getting-started/first-steps.md"
GH_RAW = (
    "https://raw.githubusercontent.com/astral-sh/uv/main/"
    "docs/getting-started/first-steps.md"
)
GH_404 = "https://github.com/astral-sh/uv/blob/main/docs/zzz-does-not-exist-xyz.md"
GH_NON_MD = "https://github.com/astral-sh/uv/blob/main/pyproject.toml"


class TestFilenameFromUrl:
    """Offline unit tests for non-GitHub URL-path filename derivation."""

    @pytest.mark.parametrize(
        ("url", "expected"),
        [
            ("https://clerk.com/docs/guides/users/inviting", "guides-users-inviting.md"),
            ("https://vercel.com/docs/monorepos", "monorepos.md"),
            ("https://vercel.com/docs/monorepos.md", "monorepos.md"),
            ("https://biomejs.dev/guides/configure-biome/", "guides-configure-biome.md"),
            ("https://docs.convex.dev/auth/convex-auth", "auth-convex-auth.md"),
        ],
    )
    def test_derives_expected_name(self, url: str, expected: str) -> None:
        """Path drives the name; a `docs` segment (and its prefix) is dropped."""
        assert filename_from_url(url) == expected

    @pytest.mark.parametrize(
        ("url", "expected"),
        [
            ("https://site.com/Getting_Started", "getting-started.md"),
            ("https://site.com/guide.html", "guide-html.md"),
            ("https://site.com/docs/v2.0/api", "v2-0-api.md"),
            ("https://site.com/docs/guide?v=2#frag", "guide.md"),
            ("https://example.com", "index.md"),
        ],
    )
    def test_sanitises_messy_url_paths(self, url: str, expected: str) -> None:
        """Uppercase, underscores, dots, and query/fragment reduce to a valid slug.

        Only a `.md` extension is stripped; an empty path falls back to index.md.
        """
        assert filename_from_url(url) == expected

    def test_bare_docs_root_falls_back_to_index(self) -> None:
        """A docs root with nothing after `docs` falls back to index.md."""
        assert filename_from_url("https://example.com/docs/") == "index.md"


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
        """A uv hosted-docs URL is rejected, pointing to the GitHub blob source."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            exit_code, output = run_script(
                tmp_dir, "https://docs.astral.sh/uv/guides/install-python/"
            )

            assert exit_code != 0
            assert "❌ Error: USE_GITHUB_BLOB|" in output
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

    @pytest.mark.parametrize(
        "url",
        [GH_RAW, GH_NON_MD],
        ids=["raw-url", "non-md-blob"],
    )
    def test_github_url_rejected_before_any_fetch(self, url: str) -> None:
        """A raw URL or non-`.md` blob exits GITHUB_BLOB before any fetch.

        Rejection happens before the network, so no files are written.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            new_dir = Path(tmp_dir) / "uv"
            exit_code, output = run_script(str(new_dir), url)

            assert exit_code != 0
            assert "❌ Error: GITHUB_BLOB|" in output
            assert "✅ Fetched markdown|" not in output
            assert not (new_dir / "INDEX.xml").exists()
            assert not (new_dir / "README.md").exists()


class TestMarkdownDirectPath:
    """Offline test: a non-GitHub `.md` URL routes to direct fetch, not FireCrawl."""

    def test_md_url_fetched_directly(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """A `.md` URL writes its URL-derived filename; FireCrawl is never called."""
        # The one in-process test: rather than fetching over the network we hand
        # main() a fixed markdown string, then assert FireCrawl is never reached.
        # This isolates the `.md` routing branch — there is no stable non-GitHub
        # `.md` URL to point a live test at.

        def _fake_fetch(_url: str) -> str:
            return "# Hello\n\nbody\n"

        monkeypatch.setattr(curate_doc.markdown_source, "fetch_markdown", _fake_fetch)

        def _no_scrape(_url: str, _max_attempts: int = 2) -> tuple[str, str]:
            msg = "FireCrawl must not be called for a .md URL"
            raise AssertionError(msg)

        monkeypatch.setattr(curate_doc.firecrawl_source, "scrape", _no_scrape)

        collection = tmp_path / "coll"
        url = "https://example.com/docs/hello/there/hi.md"
        monkeypatch.setattr("sys.argv", ["curate_doc.py", str(collection), url])

        curate_doc.main()

        doc = collection / "hello-there-hi.md"
        assert doc.read_text() == "# Hello\n\nbody\n"

        index = (collection / "INDEX.xml").read_text()
        assert f"<source_url>{url}</source_url>" in index
        assert "<local_file>hello-there-hi.md</local_file>" in index
        assert "<title>Hello</title>" in index

        assert "🎉 Curation Success!|" in capsys.readouterr().out


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

            # Filename is deterministic from the URL path.
            doc = new_dir / "learn-guides-updating-state.md"
            assert doc.exists()
            assert doc.name in output

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

            # Filename is deterministic from the URL path.
            assert (existing_dir / "learn-guides-updating-state.md").exists()

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
            assert "🎉 Curation Success!|created and indexed new document|" in output1

            # Re-curating the SAME URL must UPDATE, not error.
            exit_code2, output2 = run_script(str(collection_dir), TEST_URL)
            assert exit_code2 == 0
            assert "✅ Updated index source|" in output2
            assert "🎉 Curation Success!|overwrote and re-indexed document|" in output2

            index_path = collection_dir / "INDEX.xml"
            index_content = index_path.read_text()
            source_count = index_content.count("<source>")
            assert source_count == 1, f"Expected 1 source, found {source_count}"

            # Trailing-slash variant must hit the same UPDATE path.
            url_variant = TEST_URL + "/"
            exit_code3, output3 = run_script(str(collection_dir), url_variant)
            assert exit_code3 == 0
            assert "✅ Updated index source|" in output3

            # Still one source: the slash variant normalised to the same URL.
            index_content = index_path.read_text()
            source_count = index_content.count("<source>")
            assert source_count == 1, (
                f"Expected 1 source after slash variant, found {source_count}"
            )


class TestGithubSourcePath:
    """Real-network end-to-end tests for the GitHub blob path (curate + 404)."""

    @pytest.mark.github
    def test_blob_url_curates_and_stores_blob(self) -> None:
        """Blob URL is fetched (from raw) and stored verbatim as blob in INDEX + .md."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            new_dir = Path(tmp_dir) / "uv"
            exit_code, output = run_script(str(new_dir), GH_BLOB)

            assert exit_code == 0
            assert "✅ Detected GitHub source|" in output
            assert "✅ Fetched markdown|" in output
            assert "🎉 Curation Success!|" in output

            doc = new_dir / "getting-started-first-steps.md"
            assert doc.exists()
            content = doc.read_text()
            assert content.strip() != ""
            assert "<!DOCTYPE html>" not in content  # raw md fetched, not the blob HTML

            index = (new_dir / "INDEX.xml").read_text()
            assert f"<source_url>{GH_BLOB}</source_url>" in index
            assert "<local_file>getting-started-first-steps.md</local_file>" in index
            assert "<title>First steps with uv</title>" in index
            assert "<description>PLACEHOLDER</description>" in index

    @pytest.mark.github
    def test_404_fails_without_mutation(self) -> None:
        """404 blob URL exits non-zero with FETCH_NOT_FOUND and leaves no files."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            new_dir = Path(tmp_dir) / "uv"
            exit_code, output = run_script(str(new_dir), GH_404)

            assert exit_code != 0
            assert "❌ Error: FETCH_NOT_FOUND|" in output
            md_files = list(new_dir.glob("*.md")) if new_dir.exists() else []
            assert md_files == []
            assert not (new_dir / "INDEX.xml").exists()
            assert not (new_dir / "README.md").exists()


@pytest.mark.firecrawl
class TestOutputContent:
    """Integration tests validating generated file content (requires API)."""

    def test_index_xml_structure_and_content(self) -> None:
        """A new <source> stores PLACEHOLDER; a later LLM step fills the description."""
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
            assert (
                "<local_file>learn-guides-updating-state.md</local_file>\n"
                in index_content
            )
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
