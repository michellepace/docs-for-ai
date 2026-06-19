"""Tests for curate_doc.py; network tests gated by `firecrawl`/`github` markers."""

import subprocess
from datetime import date
from typing import TYPE_CHECKING

import pytest

from docs_for_ai import curate_doc
from docs_for_ai.curate_doc import filename_from_canonical_url
from docs_for_ai.paths import format_path_for_display

if TYPE_CHECKING:
    from pathlib import Path

URL_FIRECRAWL = "https://zustand.docs.pmnd.rs/learn/guides/updating-state"

URL_GH_BLOB = (
    "https://github.com/astral-sh/uv/blob/main/docs/getting-started/first-steps.md"
)
URL_GH_RAW = (
    "https://raw.githubusercontent.com/astral-sh/uv/main/"
    "docs/getting-started/first-steps.md"
)
URL_GH_BLOB_404 = (
    "https://github.com/astral-sh/uv/blob/main/docs/zzz-does-not-exist-xyz.md"
)

URL_GH_BLOB_MDX = (
    "https://github.com/biomejs/website/blob/main/"
    "src/content/docs/guides/getting-started.mdx"
)
URL_GH_RAW_MDX = (
    "https://raw.githubusercontent.com/biomejs/website/main/"
    "src/content/docs/guides/getting-started.mdx"
)
URL_GH_BLOB_QMD = (
    "https://github.com/posit-dev/py-shiny-site/blob/main/get-started/deploy-cloud.qmd"
)
URL_GH_RAW_QMD = (
    "https://raw.githubusercontent.com/posit-dev/py-shiny-site/main/"
    "get-started/deploy-cloud.qmd"
)


class TestFilenameFromUrl:
    """Offline unit tests for non-GitHub URL-path filename derivation."""

    @pytest.mark.parametrize(
        ("url", "expected"),
        [
            ("https://clerk.com/docs/guides/users/inviting", "guides-users-inviting.md"),
            ("https://vercel.com/docs/monorepos", "monorepos.md"),
            ("https://biomejs.dev/guides/configure-biome/", "guides-configure-biome.md"),
            ("https://docs.convex.dev/auth/convex-auth", "auth-convex-auth.md"),
        ],
    )
    def test_derives_expected_name(self, url: str, expected: str) -> None:
        """Path drives the name; a `docs` segment (and its prefix) is dropped."""
        assert filename_from_canonical_url(url) == expected

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
        """Uppercase, underscores, dots, query/fragment slugify; empty path → index.md."""
        assert filename_from_canonical_url(url) == expected

    def test_bare_docs_root_falls_back_to_index(self) -> None:
        """Trailing `docs/` is a dropped segment, so it yields index.md, not docs.md."""
        assert filename_from_canonical_url("https://example.com/docs/") == "index.md"


def run_script(*args: str, cwd: Path | None = None) -> tuple[int, str]:
    """Run curate_doc.py script via uv and return (exit_code, output)."""
    cmd = ["uv", "run", "curate-doc"]
    cmd.extend(args)

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=cwd,
        check=False,
    )

    return result.returncode, result.stdout + result.stderr


def _index_source_fields(output: str, verb: str) -> dict[str, str]:
    """Parse key=value fields from the '✅ {verb} index source|...' line."""
    line = next(
        ln for ln in output.splitlines() if ln.startswith(f"✅ {verb} index source|")
    )
    return dict(part.split("=", 1) for part in line.split("|") if "=" in part)


class TestInputValidation:
    """Fast tests for argument, URL, and directory-state validation (no API calls)."""

    def test_requires_both_directory_and_url_arguments(self) -> None:
        """Argparse exits with usage code (2) when required args are missing."""
        exit_code, output = run_script()
        assert exit_code == 2
        assert "required" in output

    def test_fails_when_url_is_invalid(self, tmp_path: Path) -> None:
        """Script rejects malformed URLs with INVALID_URL error."""
        exit_code, output = run_script(str(tmp_path), "horse-donkey-cow")

        assert exit_code != 0
        assert "❌ Error: INVALID_URL|horse-donkey-cow" in output

    def test_fails_when_source_url_is_uv_docs_site(self, tmp_path: Path) -> None:
        """A uv hosted-docs URL is rejected, pointing to the GitHub blob source."""
        exit_code, output = run_script(
            str(tmp_path), "https://docs.astral.sh/uv/guides/install-python/"
        )

        assert exit_code != 0
        assert "❌ Error: USE_GITHUB_BLOB|" in output
        assert "collections/uv/INDEX.xml" in output

    def test_nonempty_noncollection_directory_fails(self, tmp_path: Path) -> None:
        """Non-empty directory without INDEX.xml fails with INVALID_COLLECTION error."""
        invalid_dir = tmp_path / "not_a_collection"

        invalid_dir.mkdir()
        (invalid_dir / "some_file.txt").write_text("random content")

        exit_code, output = run_script(str(invalid_dir), URL_FIRECRAWL)

        assert exit_code != 0
        assert (
            "❌ Error: INVALID_COLLECTION|"
            "Directory non-empty and missing INDEX.xml. "
            "Rejected to prevent inadvertent file overwrites|"
        ) in output

    def test_github_url_rejected_before_any_fetch(self, tmp_path: Path) -> None:
        """A non-blob GitHub URL exits GITHUB_BLOB before any fetch, writing no files."""
        new_dir = tmp_path / "uv"
        exit_code, output = run_script(str(new_dir), URL_GH_RAW)

        assert exit_code != 0
        assert "❌ Error: GITHUB_BLOB|" in output
        assert "✅ Fetched markdown|" not in output
        assert not (new_dir / "INDEX.xml").exists()
        assert not (new_dir / "README.md").exists()


class TestMarkdownDirectPath:
    """Offline end-to-end test of the non-GitHub `.md` direct-fetch path."""

    def test_md_url_curates_offline_end_to_end(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """A `.md` URL is curated offline end-to-end; FireCrawl is never called."""
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
        # Canonical source_url drops the trailing `.md` (the two spellings collapse).
        assert "<source_url>https://example.com/docs/hello/there/hi</source_url>" in index
        assert f"<source_url>{url}</source_url>" not in index
        assert "<local_file>hello-there-hi.md</local_file>" in index
        assert "<title>Hello</title>" in index

        assert "🎉 Curation Success!|" in capsys.readouterr().out


class TestCanonicalCollapse:
    """The `…/x` and `…/x.md` spellings of one page collapse to a single entry."""

    def test_no_suffix_then_md_suffix_yields_one_source(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Allowlisted `…/storage` then `…/storage.md` updates, not duplicates."""
        monkeypatch.setattr(
            curate_doc.markdown_source,
            "load_md_allowlist",
            lambda: ["https://allowed.test/docs/"],
        )

        def _fake_fetch(_url: str) -> str:
            return "# Storage\n\nbody\n"

        monkeypatch.setattr(curate_doc.markdown_source, "fetch_markdown", _fake_fetch)

        def _no_scrape(_url: str, _max_attempts: int = 2) -> tuple[str, str]:
            msg = "FireCrawl must not be called for an allowlisted/.md URL"
            raise AssertionError(msg)

        monkeypatch.setattr(curate_doc.firecrawl_source, "scrape", _no_scrape)

        collection = tmp_path / "coll"
        for url in (
            "https://allowed.test/docs/storage",
            "https://allowed.test/docs/storage.md",
        ):
            monkeypatch.setattr("sys.argv", ["curate_doc.py", str(collection), url])
            curate_doc.main()

        index = (collection / "INDEX.xml").read_text()
        assert index.count("<source>") == 1
        assert "<source_url>https://allowed.test/docs/storage</source_url>" in index
        assert (
            "<source_url>https://allowed.test/docs/storage.md</source_url>" not in index
        )


class TestFetchDocumentRouting:
    """Offline branch-selection tests for `fetch_document`."""

    def test_github_blob_routes_to_raw_fetch(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """A GitHub blob `.md` URL fetches from raw and never reaches FireCrawl."""
        fetched_urls: list[str] = []

        def _fake_fetch(url: str) -> str:
            fetched_urls.append(url)
            return "# stub\n\nbody\n"

        def _no_scrape(_url: str, _max_attempts: int = 2) -> tuple[str, str]:
            msg = "FireCrawl must not be called for a GitHub blob URL"
            raise AssertionError(msg)

        monkeypatch.setattr(curate_doc.markdown_source, "fetch_markdown", _fake_fetch)
        monkeypatch.setattr(curate_doc.firecrawl_source, "scrape", _no_scrape)

        doc = curate_doc.fetch_document(URL_GH_BLOB)

        # GitHub is matched before `.md`, fetched from raw, named from the blob path.
        assert fetched_urls == [URL_GH_RAW]
        assert doc.filename == "getting-started-first-steps.md"
        assert "✅ Detected GitHub source|" in capsys.readouterr().out

    @pytest.mark.parametrize(
        ("blob_url", "raw_url", "filename"),
        [
            (
                URL_GH_BLOB_MDX,
                URL_GH_RAW_MDX,
                "src-content-docs-guides-getting-started.mdx",
            ),
            (URL_GH_BLOB_QMD, URL_GH_RAW_QMD, "get-started-deploy-cloud.qmd"),
        ],
        ids=["mdx", "qmd"],
    )
    def test_github_blob_preserves_mdx_qmd_extension(
        self,
        blob_url: str,
        raw_url: str,
        filename: str,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """A GitHub `.mdx`/`.qmd` blob fetches from raw and keeps its extension."""
        fetched_urls: list[str] = []

        def _fake_fetch(url: str) -> str:
            fetched_urls.append(url)
            return "# stub\n\nbody\n"

        monkeypatch.setattr(curate_doc.markdown_source, "fetch_markdown", _fake_fetch)

        doc = curate_doc.fetch_document(blob_url)

        assert fetched_urls == [raw_url]
        assert doc.filename == filename
        assert doc.source_url == blob_url

    def test_non_md_url_routes_to_firecrawl(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A non-`.md` URL is scraped via FireCrawl; direct fetch is never called."""
        scraped_urls: list[str] = []

        def _no_fetch(_url: str) -> str:
            msg = "markdown fetch must not be called for a non-.md URL"
            raise AssertionError(msg)

        def _fake_scrape(url: str, _max_attempts: int = 2) -> tuple[str, str]:
            scraped_urls.append(url)
            return "stub body", "stub title"

        monkeypatch.setattr(curate_doc.markdown_source, "fetch_markdown", _no_fetch)
        monkeypatch.setattr(curate_doc.firecrawl_source, "scrape", _fake_scrape)

        url = "https://example.com/docs/some/page"
        doc = curate_doc.fetch_document(url)

        # The else-branch reached FireCrawl with the source URL; direct fetch raised.
        assert scraped_urls == [url]
        # A non-allowlisted URL is stored verbatim as its own canonical.
        assert doc.source_url == url

    def test_allowlisted_no_suffix_fetches_md_twin(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """An allowlisted suffixless URL fetches `url + '.md'` and never FireCrawls."""
        monkeypatch.setattr(
            curate_doc.markdown_source,
            "load_md_allowlist",
            lambda: ["https://allowed.test/docs/"],
        )
        fetched_urls: list[str] = []

        def _fake_fetch(url: str) -> str:
            fetched_urls.append(url)
            return "# stub\n\nbody\n"

        def _no_scrape(_url: str, _max_attempts: int = 2) -> tuple[str, str]:
            msg = "FireCrawl must not be called for an allowlisted URL"
            raise AssertionError(msg)

        monkeypatch.setattr(curate_doc.markdown_source, "fetch_markdown", _fake_fetch)
        monkeypatch.setattr(curate_doc.firecrawl_source, "scrape", _no_scrape)

        url = "https://allowed.test/docs/storage"
        doc = curate_doc.fetch_document(url)

        # The free `.md` twin is fetched; canonical drops the appended suffix.
        assert fetched_urls == [f"{url}.md"]
        assert doc.source_url == url

    def test_allowlisted_suffixed_url_routes_to_firecrawl(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """An allowlisted but suffixed (.html) URL still FireCrawls; stored as given."""
        monkeypatch.setattr(
            curate_doc.markdown_source,
            "load_md_allowlist",
            lambda: ["https://allowed.test/docs/"],
        )
        scraped_urls: list[str] = []

        def _no_fetch(_url: str) -> str:
            msg = "markdown fetch must not be called for a suffixed URL"
            raise AssertionError(msg)

        def _fake_scrape(url: str, _max_attempts: int = 2) -> tuple[str, str]:
            scraped_urls.append(url)
            return "stub body", "stub title"

        monkeypatch.setattr(curate_doc.markdown_source, "fetch_markdown", _no_fetch)
        monkeypatch.setattr(curate_doc.firecrawl_source, "scrape", _fake_scrape)

        url = "https://allowed.test/docs/page.html"
        doc = curate_doc.fetch_document(url)

        assert scraped_urls == [url]
        assert doc.source_url == url


@pytest.mark.firecrawl
class TestDirectoryScenarios:
    """Integration tests for different directory states (requires API)."""

    def test_nonexistent_directory_creates_new_collection(self, tmp_path: Path) -> None:
        """Nonexistent target path is created (not just initialised in place)."""
        new_dir = tmp_path / "new_collection"

        exit_code, output = run_script(str(new_dir), URL_FIRECRAWL)

        assert exit_code == 0

        readme_path = new_dir / "README.md"
        index_path = new_dir / "INDEX.xml"

        assert (
            f"✅ Created curation readme|{format_path_for_display(readme_path)}|"
            in output
        )
        assert (
            f"✅ Created curation index|{format_path_for_display(index_path)}|" in output
        )
        assert readme_path.exists()
        assert index_path.exists()

        # Filename is deterministic from the URL path.
        doc = new_dir / "learn-guides-updating-state.md"
        assert doc.exists()
        assert doc.name in output

        assert "✅ Added index source|" in output
        assert "🎉 Curation Success!|" in output

    def test_existing_collection_adds_document_without_creating_readme(
        self, tmp_path: Path
    ) -> None:
        """README is written once at collection creation, not per added document."""
        existing_dir = tmp_path / "existing_collection"

        existing_dir.mkdir()
        index_path = existing_dir / "INDEX.xml"
        index_path.write_text("<docs_index>\n</docs_index>\n")
        (existing_dir / "existing_file.md").write_text("# Existing content")

        exit_code, output = run_script(str(existing_dir), URL_FIRECRAWL)

        assert exit_code == 0

        # Filename is deterministic from the URL path.
        assert (existing_dir / "learn-guides-updating-state.md").exists()

        assert "✅ Added index source|" in output
        assert "🎉 Curation Success!|" in output

        readme_path = existing_dir / "README.md"
        assert not readme_path.exists()
        readme_created_count = output.count("README.md")
        assert readme_created_count == 0

    def test_curating_same_url_twice_updates_existing_source(
        self, tmp_path: Path
    ) -> None:
        """Re-curating a URL (or its trailing-slash variant) updates, not duplicates."""
        collection_dir = tmp_path / "test_collection"

        exit_code1, output1 = run_script(str(collection_dir), URL_FIRECRAWL)
        assert exit_code1 == 0
        assert "✅ Added index source|" in output1
        fields1 = _index_source_fields(output1, "Added")
        assert fields1["local_file"] == "learn-guides-updating-state.md"
        assert fields1["description"] == "PLACEHOLDER"
        assert fields1["title"]
        assert "💡 Source description pending|" in output1
        assert "🎉 Curation Success!|created and indexed new document|" in output1

        # Re-curating the SAME URL must UPDATE, not error.
        exit_code2, output2 = run_script(str(collection_dir), URL_FIRECRAWL)
        assert exit_code2 == 0
        assert "✅ Updated index source|" in output2
        fields2 = _index_source_fields(output2, "Updated")
        assert fields2["local_file"] == "learn-guides-updating-state.md"
        assert fields2["description"] == "PLACEHOLDER"
        assert fields2["title"]
        assert "💡 Source description pending|" in output2
        assert "🎉 Curation Success!|overwrote and re-indexed document|" in output2

        index_path = collection_dir / "INDEX.xml"
        index_content = index_path.read_text()
        source_count = index_content.count("<source>")
        assert source_count == 1, f"Expected 1 source, found {source_count}"

        # Trailing-slash variant must hit the same UPDATE path.
        url_variant = URL_FIRECRAWL + "/"
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
    def test_blob_url_curates_and_stores_blob(self, tmp_path: Path) -> None:
        """Blob URL is fetched (from raw) and stored verbatim as blob in INDEX + .md."""
        new_dir = tmp_path / "uv"
        exit_code, output = run_script(str(new_dir), URL_GH_BLOB)

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
        assert f"<source_url>{URL_GH_BLOB}</source_url>" in index
        assert "<local_file>getting-started-first-steps.md</local_file>" in index
        assert "<title>First steps with uv</title>" in index
        assert "<description>PLACEHOLDER</description>" in index

    @pytest.mark.github
    def test_404_fails_without_mutation(self, tmp_path: Path) -> None:
        """404 blob URL exits non-zero with FETCH_NOT_FOUND and leaves no files."""
        new_dir = tmp_path / "uv"
        exit_code, output = run_script(str(new_dir), URL_GH_BLOB_404)

        assert exit_code != 0
        assert "❌ Error: FETCH_NOT_FOUND|" in output
        md_files = list(new_dir.glob("*.md")) if new_dir.exists() else []
        assert md_files == []
        assert not (new_dir / "INDEX.xml").exists()
        assert not (new_dir / "README.md").exists()


@pytest.mark.firecrawl
class TestOutputContent:
    """Integration tests validating generated file content (requires API)."""

    def test_index_xml_structure_and_content(self, tmp_path: Path) -> None:
        """A new <source> stores PLACEHOLDER; a later LLM step fills the description."""
        new_dir = tmp_path / "test_collection"

        exit_code, _ = run_script(str(new_dir), URL_FIRECRAWL)

        assert exit_code == 0

        index_path = new_dir / "INDEX.xml"
        index_content = index_path.read_text()

        today = date.today().isoformat()

        assert index_content.startswith("<docs_index>")
        assert "<source>\n" in index_content
        assert "<title>Updating state - Zustand</title>\n" in index_content
        assert "<description>PLACEHOLDER</description>\n" in index_content
        assert f"<source_url>{URL_FIRECRAWL}</source_url>\n" in index_content
        assert (
            "<local_file>learn-guides-updating-state.md</local_file>\n" in index_content
        )
        assert f"<scraped_at>{today}</scraped_at>\n" in index_content
        assert "</source>\n" in index_content
        assert index_content.endswith("</docs_index>\n")

    def test_readme_md_contains_required_content(self, tmp_path: Path) -> None:
        """Generated README links to INDEX.xml and back to the upstream source site."""
        new_dir = tmp_path / "test_collection"

        exit_code, _ = run_script(str(new_dir), URL_FIRECRAWL)

        assert exit_code == 0

        readme_path = new_dir / "README.md"
        readme_content = readme_path.read_text()

        assert "# test_collection Documentation" in readme_content
        assert "Curated docs for targeted AI context.\n" in readme_content
        assert "- Curation Index: [INDEX.xml](INDEX.xml)\n" in readme_content
        assert "- Curation Source: <https://zustand.docs.pmnd.rs>\n" in readme_content
