"""Tests for curate_doc.py; network tests gated by `firecrawl`/`github` markers."""

import subprocess
from datetime import date
from typing import TYPE_CHECKING

import pytest

from docs_for_ai import curate_doc

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


class TestInputValidation:
    """Fast tests for argument, URL, and directory-state validation (no API calls)."""

    def test_requires_both_collection_dir_and_url_arguments(self) -> None:
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
        assert "✅ Fetched:" not in output
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

        monkeypatch.setattr(curate_doc.direct_fetch, "fetch_text", _fake_fetch)

        def _no_scrape(_url: str, _max_attempts: int = 2) -> tuple[str, str]:
            msg = "FireCrawl must not be called for a .md URL"
            raise AssertionError(msg)

        monkeypatch.setattr(curate_doc.firecrawl_scrape, "scrape", _no_scrape)

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

        assert "🏁 Success! curated doc" in capsys.readouterr().out


class TestCanonicalCollapse:
    """The `…/x` and `…/x.md` spellings of one page collapse to a single entry."""

    def test_no_suffix_then_md_suffix_yields_one_source(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Registry-matched `…/storage` then `…/storage.md` updates, not duplicates."""
        monkeypatch.setattr(
            curate_doc.direct_fetch,
            "load_direct_fetch_rules",
            lambda: {"append-md": ["https://allowed.test/docs/"]},
        )

        def _fake_fetch(_url: str) -> str:
            return "# Storage\n\nbody\n"

        monkeypatch.setattr(curate_doc.direct_fetch, "fetch_text", _fake_fetch)

        def _no_scrape(_url: str, _max_attempts: int = 2) -> tuple[str, str]:
            msg = "FireCrawl must not be called for a registry-matched/.md URL"
            raise AssertionError(msg)

        monkeypatch.setattr(curate_doc.firecrawl_scrape, "scrape", _no_scrape)

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

    def test_readthedocs_html_then_source_twin_yields_one_source(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """`.html` page then its `_sources` twin yield one file and one source."""
        monkeypatch.setattr(
            curate_doc.direct_fetch,
            "load_direct_fetch_rules",
            lambda: {"readthedocs": ["https://allowed.test/"]},
        )

        def _fake_fetch(_url: str) -> str:
            return "Panel\n=====\n\nbody\n"

        monkeypatch.setattr(curate_doc.direct_fetch, "fetch_text", _fake_fetch)

        def _no_scrape(_url: str, _max_attempts: int = 2) -> tuple[str, str]:
            msg = "FireCrawl must not be called for a readthedocs URL"
            raise AssertionError(msg)

        monkeypatch.setattr(curate_doc.firecrawl_scrape, "scrape", _no_scrape)

        collection = tmp_path / "coll"
        for url in (
            "https://allowed.test/panel.html",
            "https://allowed.test/_sources/panel.rst.txt",
        ):
            monkeypatch.setattr("sys.argv", ["curate_doc.py", str(collection), url])
            curate_doc.main()

        index = (collection / "INDEX.xml").read_text()
        assert index.count("<source>") == 1
        assert "<local_file>panel.rst</local_file>" in index
        assert "<source_url>https://allowed.test/panel.html</source_url>" in index
        assert [p.name for p in collection.glob("*.rst")] == ["panel.rst"]


def _forbid_scrape(_url: str, _max_attempts: int = 2) -> tuple[str, str]:
    """Stand in for `firecrawl_scrape.scrape` to prove the network is never touched."""
    msg = "FireCrawl must not be called for a .md URL"
    raise AssertionError(msg)


def test_new_directory_is_initialised_as_a_collection_once(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A new collection is scaffolded once; re-curating never re-scaffolds it."""

    def _fake_fetch(_url: str) -> str:
        return "# Doc\n\nbody\n"

    monkeypatch.setattr(curate_doc.direct_fetch, "fetch_text", _fake_fetch)
    monkeypatch.setattr(curate_doc.firecrawl_scrape, "scrape", _forbid_scrape)

    collection = tmp_path / "zustand"
    first_url = "https://z.test/a.md"
    second_url = "https://z.test/b.md"

    monkeypatch.setattr("sys.argv", ["curate_doc.py", str(collection), first_url])
    curate_doc.main()

    readme = collection / "README.md"
    assert readme.exists()
    assert (collection / "INDEX.xml").exists()
    assert (collection / "a.md").exists()

    # A user edit to the README survives re-curation, proving the collection is
    # not re-scaffolded when a second doc is added.
    readme.write_text("EDITED")

    monkeypatch.setattr("sys.argv", ["curate_doc.py", str(collection), second_url])
    curate_doc.main()

    assert readme.read_text() == "EDITED"
    assert (collection / "b.md").exists()


def test_recurating_a_url_updates_the_existing_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Re-curating a URL (or its slash twin) updates the source, never duplicating."""
    monkeypatch.setattr(curate_doc.direct_fetch, "load_direct_fetch_rules", dict)
    monkeypatch.setattr(
        curate_doc.firecrawl_scrape,
        "scrape",
        lambda _url, _max_attempts=2: ("# Body\n\ntext\n", "Updating State"),
    )

    collection = tmp_path / "zustand"
    url = "https://example.com/docs/updating-state"

    for source_url in (url, url, f"{url}/"):
        monkeypatch.setattr("sys.argv", ["curate_doc.py", str(collection), source_url])
        curate_doc.main()

    index = (collection / "INDEX.xml").read_text()
    assert index.count("<source>") == 1
    assert f"<source_url>{url}</source_url>" in index
    assert "<title>Updating State</title>" in index


class TestFilenameCollisionGuard:
    """Two DIFFERENT canonical URLs that slugify to one filename fail loud."""

    def test_colliding_filename_different_url_fails_without_clobber(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """A 2nd URL colliding on `local_file` exits FILENAME_COLLISION, no clobber."""
        monkeypatch.setattr(curate_doc.direct_fetch, "load_direct_fetch_rules", dict)
        monkeypatch.setattr(
            curate_doc.firecrawl_scrape,
            "scrape",
            lambda _url, _max_attempts=2: ("# Second\n", "Second"),
        )

        # Pre-seed: foo-bar.md already curated from a DIFFERENT canonical URL.
        collection = tmp_path / "coll"
        collection.mkdir()
        (collection / "foo-bar.md").write_text("# First\n")
        (collection / "INDEX.xml").write_text(
            "<docs_index><source>"
            "<local_file>foo-bar.md</local_file>"
            "<source_url>https://x.test/foo/bar</source_url>"
            "</source></docs_index>"
        )

        monkeypatch.setattr(
            "sys.argv", ["curate_doc.py", str(collection), "https://x.test/foo-bar"]
        )
        with pytest.raises(SystemExit) as excinfo:
            curate_doc.main()

        assert excinfo.value.code == 1
        assert "❌ Error: FILENAME_COLLISION|" in capsys.readouterr().out
        # No partial state: the file keeps the first doc, index still one <source>.
        assert (collection / "foo-bar.md").read_text() == "# First\n"
        assert (collection / "INDEX.xml").read_text().count("<source>") == 1


class TestFetchDocumentRouting:
    """Offline branch-selection tests for `fetch_document`."""

    def test_github_blob_routes_to_raw_fetch(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """A GitHub blob `.md` URL fetches from raw and never reaches FireCrawl."""
        fetched_urls: list[str] = []

        def _fake_fetch(url: str) -> str:
            fetched_urls.append(url)
            return "# stub\n\nbody\n"

        def _no_scrape(_url: str, _max_attempts: int = 2) -> tuple[str, str]:
            msg = "FireCrawl must not be called for a GitHub blob URL"
            raise AssertionError(msg)

        monkeypatch.setattr(curate_doc.direct_fetch, "fetch_text", _fake_fetch)
        monkeypatch.setattr(curate_doc.firecrawl_scrape, "scrape", _no_scrape)

        route = curate_doc.direct_fetch.resolve_route(URL_GH_BLOB, {})
        doc = curate_doc.fetch_document(route)

        # GitHub is matched first, fetched from raw, named from the blob path.
        assert fetched_urls == [URL_GH_RAW]
        assert doc.filename == "getting-started-first-steps.md"

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

        monkeypatch.setattr(curate_doc.direct_fetch, "fetch_text", _fake_fetch)

        route = curate_doc.direct_fetch.resolve_route(blob_url, {})
        doc = curate_doc.fetch_document(route)

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

        monkeypatch.setattr(curate_doc.direct_fetch, "fetch_text", _no_fetch)
        monkeypatch.setattr(curate_doc.firecrawl_scrape, "scrape", _fake_scrape)

        url = "https://example.com/docs/some/page"
        route = curate_doc.direct_fetch.resolve_route(url, {})
        doc = curate_doc.fetch_document(route)

        # The else-branch reached FireCrawl with the source URL; direct fetch raised.
        assert scraped_urls == [url]
        # A URL with no matching registry rule is stored verbatim as its own canonical.
        assert doc.source_url == url

    def test_registry_no_suffix_fetches_md_twin(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A registry-matched suffixless URL fetches `url + '.md'`, never FireCrawls."""
        rules = {"append-md": ["https://allowed.test/docs/"]}
        fetched_urls: list[str] = []

        def _fake_fetch(url: str) -> str:
            fetched_urls.append(url)
            return "# stub\n\nbody\n"

        def _no_scrape(_url: str, _max_attempts: int = 2) -> tuple[str, str]:
            msg = "FireCrawl must not be called for a registry-matched URL"
            raise AssertionError(msg)

        monkeypatch.setattr(curate_doc.direct_fetch, "fetch_text", _fake_fetch)
        monkeypatch.setattr(curate_doc.firecrawl_scrape, "scrape", _no_scrape)

        url = "https://allowed.test/docs/storage"
        route = curate_doc.direct_fetch.resolve_route(url, rules)
        doc = curate_doc.fetch_document(route)

        # The free `.md` twin is fetched; canonical drops the appended suffix.
        assert fetched_urls == [f"{url}.md"]
        assert doc.source_url == url

    def test_append_md_twin_reverse_maps_to_page(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        rules = {"append-md": ["https://allowed.test/docs/"]}
        fetched_urls: list[str] = []

        def _fake_fetch(url: str) -> str:
            fetched_urls.append(url)
            return "# stub\n\nbody\n"

        def _no_scrape(_url: str, _max_attempts: int = 2) -> tuple[str, str]:
            msg = "FireCrawl must not be called for a registry-matched URL"
            raise AssertionError(msg)

        monkeypatch.setattr(curate_doc.direct_fetch, "fetch_text", _fake_fetch)
        monkeypatch.setattr(curate_doc.firecrawl_scrape, "scrape", _no_scrape)

        url = "https://allowed.test/docs/storage.md"
        route = curate_doc.direct_fetch.resolve_route(url, rules)
        doc = curate_doc.fetch_document(route)

        # Fetched as-is, but canonical drops `.md`, so it converges with the page.
        assert fetched_urls == [url]
        assert doc.source_url == "https://allowed.test/docs/storage"
        assert doc.filename == "storage.md"

    def test_registry_suffixed_url_routes_to_firecrawl(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A registry-matched but suffixed (.html) URL FireCrawls; stored as given."""
        rules = {"append-md": ["https://allowed.test/docs/"]}
        scraped_urls: list[str] = []

        def _no_fetch(_url: str) -> str:
            msg = "markdown fetch must not be called for a suffixed URL"
            raise AssertionError(msg)

        def _fake_scrape(url: str, _max_attempts: int = 2) -> tuple[str, str]:
            scraped_urls.append(url)
            return "stub body", "stub title"

        monkeypatch.setattr(curate_doc.direct_fetch, "fetch_text", _no_fetch)
        monkeypatch.setattr(curate_doc.firecrawl_scrape, "scrape", _fake_scrape)

        url = "https://allowed.test/docs/page.html"
        route = curate_doc.direct_fetch.resolve_route(url, rules)
        doc = curate_doc.fetch_document(route)

        assert scraped_urls == [url]
        assert doc.source_url == url

    def test_readthedocs_routes_to_rst_twin(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A registered readthedocs `.html` URL fetches its `_sources/*.rst.txt` twin."""
        rules = {"readthedocs": ["https://allowed.test/"]}
        fetched_urls: list[str] = []

        def _fake_fetch(url: str) -> str:
            fetched_urls.append(url)
            return "Panel\n=====\n\nbody\n"

        def _no_scrape(_url: str, _max_attempts: int = 2) -> tuple[str, str]:
            msg = "FireCrawl must not be called for a readthedocs URL"
            raise AssertionError(msg)

        monkeypatch.setattr(curate_doc.direct_fetch, "fetch_text", _fake_fetch)
        monkeypatch.setattr(curate_doc.firecrawl_scrape, "scrape", _no_scrape)

        url = "https://allowed.test/panel.html"
        route = curate_doc.direct_fetch.resolve_route(url, rules)
        doc = curate_doc.fetch_document(route)

        # The RST source twin is fetched; the page `.html` URL stays canonical.
        assert fetched_urls == ["https://allowed.test/_sources/panel.rst.txt"]
        assert doc.filename == "panel.rst"
        assert doc.source_url == url
        # The title comes from the RST heading, not the URL stem.
        assert doc.title == "Panel"

    def test_readthedocs_source_twin_reverse_maps_to_page(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A registered `_sources/*.rst.txt` URL maps back to its `.html` page."""
        rules = {"readthedocs": ["https://allowed.test/"]}
        fetched_urls: list[str] = []

        def _fake_fetch(url: str) -> str:
            fetched_urls.append(url)
            return "Panel\n=====\n\nbody\n"

        def _no_scrape(_url: str, _max_attempts: int = 2) -> tuple[str, str]:
            msg = "FireCrawl must not be called for a readthedocs URL"
            raise AssertionError(msg)

        monkeypatch.setattr(curate_doc.direct_fetch, "fetch_text", _fake_fetch)
        monkeypatch.setattr(curate_doc.firecrawl_scrape, "scrape", _no_scrape)

        url = "https://allowed.test/_sources/panel.rst.txt"
        route = curate_doc.direct_fetch.resolve_route(url, rules)
        doc = curate_doc.fetch_document(route)

        # Fetched as-is, but canonical + filename map to the `.html` page, so this
        # converges with the `.html` spelling onto one file and one index entry.
        assert fetched_urls == [url]
        assert doc.filename == "panel.rst"
        assert doc.source_url == "https://allowed.test/panel.html"
        assert doc.title == "Panel"

    def test_raw_rst_txt_routes_to_direct_fetch(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """An off-registry `.rst.txt` URL is fetched directly (not scraped)."""
        rules: dict[str, list[str]] = {}
        fetched_urls: list[str] = []

        def _fake_fetch(url: str) -> str:
            fetched_urls.append(url)
            return "Panel\n=====\n\nbody\n"

        def _no_scrape(_url: str, _max_attempts: int = 2) -> tuple[str, str]:
            msg = "FireCrawl must not be called for a .rst.txt URL"
            raise AssertionError(msg)

        monkeypatch.setattr(curate_doc.direct_fetch, "fetch_text", _fake_fetch)
        monkeypatch.setattr(curate_doc.firecrawl_scrape, "scrape", _no_scrape)

        url = "https://example.com/guide.rst.txt"
        route = curate_doc.direct_fetch.resolve_route(url, rules)
        doc = curate_doc.fetch_document(route)

        # Fetched as-is; named `.rst`; titled from the RST heading; stored verbatim.
        assert fetched_urls == [url]
        assert doc.filename == "guide.rst"
        assert doc.source_url == url
        assert doc.title == "Panel"


class TestGithubSourcePath:
    """Real-network end-to-end tests for the GitHub blob path (curate + 404)."""

    @pytest.mark.github
    def test_blob_url_curates_and_stores_blob(self, tmp_path: Path) -> None:
        """Blob URL is fetched (from raw) and stored verbatim as blob in INDEX + .md."""
        new_dir = tmp_path / "uv"
        exit_code, output = run_script(str(new_dir), URL_GH_BLOB)

        assert exit_code == 0
        assert "🏁 Success! curated doc" in output

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
        assert f"<curated_at>{today}</curated_at>\n" in index_content
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
