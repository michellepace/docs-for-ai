"""curate-doc tests: fetch the cheapest route; URL twins collapse to one source.

Descriptions survive unless content really changed.
"""

import subprocess
import xml.etree.ElementTree as ET
from datetime import date
from typing import TYPE_CHECKING

import pytest

from docs_for_ai import curate_doc
from docs_for_ai.index_io import PLACEHOLDER_DESCRIPTION, write_index

if TYPE_CHECKING:
    from pathlib import Path

URL_FIRECRAWL = "https://zustand.docs.pmnd.rs/learn/guides/updating-state"

URL_GH_BLOB = (
    "https://github.com/astral-sh/uv/blob/main/docs/getting-started/first-steps.md"
)
URL_GH_RAW_TWIN = (
    "https://raw.githubusercontent.com/astral-sh/uv/main/"
    "docs/getting-started/first-steps.md"
)
URL_GH_BLOB_404 = (
    "https://github.com/astral-sh/uv/blob/main/docs/zzz-does-not-exist-xyz.md"
)

DOC_URL = "https://example.com/docs/hello.md"  # canonical …/hello → hello.md
DOC_CONTENT = "# Hello\n\nFirst paragraph.\n\nSecond paragraph.\n"


def run_script(*args: str) -> tuple[int, str]:
    """Run the curate-doc CLI via uv (real network) and return (exit_code, output)."""
    result = subprocess.run(
        ["uv", "run", "curate-doc", *args],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode, result.stdout + result.stderr


def run_curate(
    collection_dir: Path,
    url: str,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> str:
    """Run `curate-doc <collection_dir> <url>` in-process and return its stdout."""
    monkeypatch.setattr("sys.argv", ["curate-doc", str(collection_dir), url])
    curate_doc.main()
    return capsys.readouterr().out


def _forbid_scrape(_url: str, _max_attempts: int = 2) -> tuple[str, str]:
    """Stand in for `firecrawl_scrape.scrape` to prove FireCrawl is never touched."""
    msg = "FireCrawl must not be called on a direct-fetch route"
    raise AssertionError(msg)


def _forbid_fetch(_url: str) -> str:
    """Stand in for `direct_fetch.fetch_text` to prove direct fetch is never touched."""
    msg = "direct fetch must not be called on a FireCrawl route"
    raise AssertionError(msg)


def stub_direct_fetch(monkeypatch: pytest.MonkeyPatch, content: str) -> list[str]:
    """Serve `content` for any direct fetch, offline; returns the fetched URLs."""
    fetched_urls: list[str] = []

    def fetch(url: str) -> str:
        fetched_urls.append(url)
        return content

    monkeypatch.setattr(curate_doc.direct_fetch, "fetch_text", fetch)
    monkeypatch.setattr(curate_doc.firecrawl_scrape, "scrape", _forbid_scrape)
    return fetched_urls


def stub_scrape(monkeypatch: pytest.MonkeyPatch, body: str, title: str) -> list[str]:
    """Serve a canned FireCrawl scrape, offline; returns the scraped URLs."""
    scraped_urls: list[str] = []

    def scrape(url: str, _max_attempts: int = 2) -> tuple[str, str]:
        scraped_urls.append(url)
        return body, title

    monkeypatch.setattr(curate_doc.firecrawl_scrape, "scrape", scrape)
    monkeypatch.setattr(curate_doc.direct_fetch, "fetch_text", _forbid_fetch)
    return scraped_urls


def set_index_description(index_path: Path, local_file: str, description: str) -> None:
    root = ET.parse(index_path).getroot()
    for source in root.findall("source"):
        desc_elem = source.find("description")
        if source.findtext("local_file") == local_file and desc_elem is not None:
            desc_elem.text = description
    write_index(root, index_path)


def read_index_description(index_path: Path, local_file: str) -> str:
    root = ET.parse(index_path).getroot()
    for source in root.findall("source"):
        if source.findtext("local_file") == local_file:
            return source.findtext("description", "")
    return ""


def curate_offline(
    collection_dir: Path, content: str, monkeypatch: pytest.MonkeyPatch
) -> curate_doc.CurationResult:
    """Curate DOC_URL offline, serving `content` as the fetched document."""
    stub_direct_fetch(monkeypatch, content)
    return curate_doc.curate(collection_dir, DOC_URL)


def test_curate_exits_with_usage_error_when_arguments_missing(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr("sys.argv", ["curate-doc"])

    with pytest.raises(SystemExit) as exc:
        curate_doc.main()

    assert exc.value.code == 2
    assert "required" in capsys.readouterr().err


def test_curate_rejects_a_malformed_url(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr("sys.argv", ["curate-doc", str(tmp_path), "horse-donkey-cow"])

    with pytest.raises(SystemExit) as exc:
        curate_doc.main()

    assert exc.value.code == 1
    out = capsys.readouterr().out
    assert "Invalid URL" in out
    assert "horse-donkey-cow" in out


def test_curate_rejects_a_uv_hosted_docs_url(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    url = "https://docs.astral.sh/uv/guides/install-python/"
    monkeypatch.setattr("sys.argv", ["curate-doc", str(tmp_path), url])

    with pytest.raises(SystemExit) as exc:
        curate_doc.main()

    assert exc.value.code == 1
    out = capsys.readouterr().out
    assert "Unsupported uv URL" in out
    assert "collections/uv/INDEX.xml" in out


def test_curate_refuses_a_nonempty_directory_without_index(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    invalid_dir = tmp_path / "not_a_collection"
    invalid_dir.mkdir()
    (invalid_dir / "some_file.txt").write_text("random content")
    monkeypatch.setattr("sys.argv", ["curate-doc", str(invalid_dir), URL_FIRECRAWL])

    with pytest.raises(SystemExit) as exc:
        curate_doc.main()

    assert exc.value.code == 1
    out = capsys.readouterr().out
    assert "Unsafe collection dir" in out
    assert str(invalid_dir) in out


def test_curate_rejects_a_non_blob_github_url_before_fetching(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(curate_doc.direct_fetch, "fetch_text", _forbid_fetch)
    monkeypatch.setattr(curate_doc.firecrawl_scrape, "scrape", _forbid_scrape)
    new_dir = tmp_path / "uv"
    monkeypatch.setattr("sys.argv", ["curate-doc", str(new_dir), URL_GH_RAW_TWIN])

    with pytest.raises(SystemExit) as exc:
        curate_doc.main()

    assert exc.value.code == 1
    assert "Not a GitHub blob URL" in capsys.readouterr().out
    assert not (new_dir / "INDEX.xml").exists()
    assert not (new_dir / "README.md").exists()


def test_curate_md_url_fetches_directly_and_writes_exact_index(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    stub_direct_fetch(monkeypatch, "# Hello\n\nbody\n")
    collection = tmp_path / "coll"

    out = run_curate(
        collection, "https://example.com/docs/hello/there/hi.md", monkeypatch, capsys
    )

    assert (collection / "hello-there-hi.md").read_text() == "# Hello\n\nbody\n"
    # Canonical source_url drops the trailing `.md` (the two spellings collapse).
    expected_index = (
        "<docs_index>\n"
        "  <source>\n"
        "    <title>Hello</title>\n"
        f"    <description>{PLACEHOLDER_DESCRIPTION}</description>\n"
        "    <source_url>https://example.com/docs/hello/there/hi</source_url>\n"
        "    <local_file>hello-there-hi.md</local_file>\n"
        f"    <curated_at>{date.today().isoformat()}</curated_at>\n"
        "  </source>\n"
        "</docs_index>\n"
    )
    assert (collection / "INDEX.xml").read_text() == expected_index
    assert "🏁 Success! curated doc" in out


@pytest.mark.parametrize(
    ("blob_url", "raw_url", "filename"),
    [
        pytest.param(
            URL_GH_BLOB,
            URL_GH_RAW_TWIN,
            "getting-started-first-steps.md",
            id="md",
        ),
        pytest.param(
            "https://github.com/biomejs/website/blob/main/"
            "src/content/docs/guides/getting-started.mdx",
            "https://raw.githubusercontent.com/biomejs/website/main/"
            "src/content/docs/guides/getting-started.mdx",
            "src-content-docs-guides-getting-started.mdx",
            id="mdx",
        ),
        pytest.param(
            "https://github.com/posit-dev/py-shiny-site/blob/main/"
            "get-started/deploy-cloud.qmd",
            "https://raw.githubusercontent.com/posit-dev/py-shiny-site/main/"
            "get-started/deploy-cloud.qmd",
            "get-started-deploy-cloud.qmd",
            id="qmd",
        ),
    ],
)
def test_curate_github_blob_fetches_raw_twin_preserving_extension(  # noqa: PLR0913
    blob_url: str,
    raw_url: str,
    filename: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    fetched_urls = stub_direct_fetch(monkeypatch, "# stub\n\nbody\n")
    collection = tmp_path / "coll"

    run_curate(collection, blob_url, monkeypatch, capsys)

    assert fetched_urls == [raw_url]
    assert (collection / filename).read_text() == "# stub\n\nbody\n"
    # The blob URL (not the raw twin) is stored as the source of record.
    assert (
        f"<source_url>{blob_url}</source_url>" in (collection / "INDEX.xml").read_text()
    )


def test_curate_initialises_a_new_collection_only_once(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    stub_direct_fetch(monkeypatch, "# Doc\n\nbody\n")
    collection = tmp_path / "zustand"

    run_curate(collection, "https://z.test/a.md", monkeypatch, capsys)

    readme = collection / "README.md"
    assert readme.read_text() == (
        "# zustand Documentation\n"
        "\n"
        "Curated docs for targeted AI context.\n"
        "\n"
        "- Curation Index: [INDEX.xml](INDEX.xml)\n"
        "- Curation Source: <https://z.test>\n"
    )
    assert (collection / "a.md").exists()

    # A user edit to the README survives re-curation, proving the collection is
    # not re-scaffolded when a second doc is added.
    readme.write_text("EDITED")
    run_curate(collection, "https://z.test/b.md", monkeypatch, capsys)

    assert readme.read_text() == "EDITED"
    assert (collection / "b.md").exists()


def test_curate_same_url_again_updates_the_existing_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Re-curating a URL (or its slash twin) updates the source, never duplicating."""
    monkeypatch.setattr(curate_doc.direct_fetch, "load_direct_fetch_rules", dict)
    scraped_urls = stub_scrape(monkeypatch, "# Body\n\ntext\n", "Updating State")
    collection = tmp_path / "zustand"
    url = "https://example.com/docs/updating-state"

    for source_url in (url, url, f"{url}/"):
        run_curate(collection, source_url, monkeypatch, capsys)

    # Every spelling reaches FireCrawl as the slash-trimmed canonical URL.
    assert scraped_urls == [url, url, url]
    index = (collection / "INDEX.xml").read_text()
    assert index.count("<source>") == 1
    assert f"<source_url>{url}</source_url>" in index
    assert "<title>Updating State</title>" in index


def test_curate_same_url_again_keeps_the_sources_position(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A re-curated entry is rewritten in place, not relocated to the bottom."""
    collection = tmp_path / "coll"
    stub_direct_fetch(monkeypatch, "# Doc\n\nbody\n")
    for name in ("alpha", "beta", "gamma"):
        curate_doc.curate(collection, f"https://example.com/docs/{name}.md")

    # The MIDDLE entry — relocating the last one would leave order unchanged.
    stub_direct_fetch(monkeypatch, "# Beta v2\n\nbody\n")
    curate_doc.curate(collection, "https://example.com/docs/beta.md")

    sources = ET.parse(collection / "INDEX.xml").getroot().findall("source")
    assert [s.findtext("local_file") for s in sources] == [
        "alpha.md",
        "beta.md",
        "gamma.md",
    ]
    assert sources[1].findtext("title") == "Beta v2"  # rewritten in place


def test_curate_page_and_md_twin_collapse_to_one_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        curate_doc.direct_fetch,
        "load_direct_fetch_rules",
        lambda: {"append-md": ["https://allowed.test/docs/"]},
    )
    fetched_urls = stub_direct_fetch(monkeypatch, "# Storage\n\nbody\n")
    collection = tmp_path / "coll"
    page = "https://allowed.test/docs/storage"

    for url in (page, f"{page}.md"):
        run_curate(collection, url, monkeypatch, capsys)

    # Both spellings fetch the free `.md` twin; the page URL stays canonical.
    assert fetched_urls == [f"{page}.md", f"{page}.md"]
    index = (collection / "INDEX.xml").read_text()
    assert index.count("<source>") == 1
    assert f"<source_url>{page}</source_url>" in index
    assert f"<source_url>{page}.md</source_url>" not in index


def test_curate_readthedocs_page_and_rst_twin_collapse_to_one_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        curate_doc.direct_fetch,
        "load_direct_fetch_rules",
        lambda: {"readthedocs": ["https://allowed.test/"]},
    )
    fetched_urls = stub_direct_fetch(
        monkeypatch, "Panel Widgets\n=============\n\nbody\n"
    )
    collection = tmp_path / "coll"
    page = "https://allowed.test/panel.html"
    rst_twin = "https://allowed.test/_sources/panel.rst.txt"

    for url in (page, rst_twin):
        run_curate(collection, url, monkeypatch, capsys)

    # Both spellings fetch the free RST source twin; the page URL stays canonical.
    assert fetched_urls == [rst_twin, rst_twin]
    index = (collection / "INDEX.xml").read_text()
    assert index.count("<source>") == 1
    assert "<local_file>panel.rst</local_file>" in index
    assert f"<source_url>{page}</source_url>" in index
    # The title comes from the RST heading, not the URL stem.
    assert "<title>Panel Widgets</title>" in index
    assert [p.name for p in collection.glob("*.rst")] == ["panel.rst"]


def test_curate_keeps_description_when_content_unchanged(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    collection = tmp_path / "coll"
    curate_offline(collection, DOC_CONTENT, monkeypatch)
    index_path = collection / "INDEX.xml"
    set_index_description(index_path, "hello.md", "Generated description")

    result = curate_offline(collection, DOC_CONTENT, monkeypatch)

    assert read_index_description(index_path, "hello.md") == "Generated description"
    assert result.outcome == curate_doc.DocOutcome.UNCHANGED


def test_curate_keeps_description_when_change_is_whitespace_only(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    collection = tmp_path / "coll"
    curate_offline(collection, DOC_CONTENT, monkeypatch)
    index_path = collection / "INDEX.xml"
    set_index_description(index_path, "hello.md", "Generated description")
    respaced = DOC_CONTENT.replace("\n\nSecond", "\n\n\n\nSecond")

    result = curate_offline(collection, respaced, monkeypatch)

    assert read_index_description(index_path, "hello.md") == "Generated description"
    assert result.outcome == curate_doc.DocOutcome.WHITESPACE_ONLY


def test_curate_resets_description_when_content_changed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    collection = tmp_path / "coll"
    curate_offline(collection, DOC_CONTENT, monkeypatch)
    index_path = collection / "INDEX.xml"
    set_index_description(index_path, "hello.md", "Generated description")
    changed = DOC_CONTENT.replace("Second paragraph.", "Rewritten paragraph.")

    result = curate_offline(collection, changed, monkeypatch)

    assert read_index_description(index_path, "hello.md") == PLACEHOLDER_DESCRIPTION
    assert result.outcome == curate_doc.DocOutcome.CHANGED


def test_curate_keeps_description_when_doc_file_recreated(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    collection = tmp_path / "coll"
    curate_offline(collection, DOC_CONTENT, monkeypatch)
    index_path = collection / "INDEX.xml"
    set_index_description(index_path, "hello.md", "Generated description")
    (collection / "hello.md").unlink()

    result = curate_offline(collection, DOC_CONTENT, monkeypatch)

    assert read_index_description(index_path, "hello.md") == "Generated description"
    assert result.outcome == curate_doc.DocOutcome.RECREATED
    assert "file recreated, unverified" in capsys.readouterr().out


def test_curate_reports_pending_when_placeholder_carried_over(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    collection = tmp_path / "coll"
    curate_offline(collection, DOC_CONTENT, monkeypatch)
    capsys.readouterr()  # discard the first curation's output

    curate_offline(collection, DOC_CONTENT, monkeypatch)

    index_path = collection / "INDEX.xml"
    assert read_index_description(index_path, "hello.md") == PLACEHOLDER_DESCRIPTION
    assert "🚩 description pending" in capsys.readouterr().out


def test_curate_compares_against_the_entrys_recorded_local_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A renamed doc file with identical content still keeps its description."""
    collection = tmp_path / "coll"
    curate_offline(collection, DOC_CONTENT, monkeypatch)
    index_path = collection / "INDEX.xml"
    set_index_description(index_path, "hello.md", "Generated description")
    root = ET.parse(index_path).getroot()
    for source in root.findall("source"):
        local_file_elem = source.find("local_file")
        assert local_file_elem is not None
        local_file_elem.text = "renamed.md"
    write_index(root, index_path)
    (collection / "hello.md").rename(collection / "renamed.md")

    result = curate_offline(collection, DOC_CONTENT, monkeypatch)

    assert read_index_description(index_path, "hello.md") == "Generated description"
    assert result.outcome == curate_doc.DocOutcome.UNCHANGED


def test_curate_rejects_filename_collision_without_clobbering(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Two DIFFERENT canonical URLs that slugify to one filename fail loud."""
    monkeypatch.setattr(curate_doc.direct_fetch, "load_direct_fetch_rules", dict)
    # The collision is rejected before the (paid) fetch — neither fetcher may run.
    monkeypatch.setattr(curate_doc.direct_fetch, "fetch_text", _forbid_fetch)
    monkeypatch.setattr(curate_doc.firecrawl_scrape, "scrape", _forbid_scrape)

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
        "sys.argv", ["curate-doc", str(collection), "https://x.test/foo-bar"]
    )

    with pytest.raises(SystemExit) as exc:
        curate_doc.main()

    assert exc.value.code == 1
    out = capsys.readouterr().out
    assert "Filename collision" in out
    assert "foo-bar.md" in out
    # No partial state: the file keeps the first doc, index still one <source>.
    assert (collection / "foo-bar.md").read_text() == "# First\n"
    assert (collection / "INDEX.xml").read_text().count("<source>") == 1


@pytest.mark.github
def test_cli_curates_github_blob_and_stores_blob_url(tmp_path: Path) -> None:
    """A blob URL is fetched (from raw) and stored verbatim as blob in INDEX + .md."""
    new_dir = tmp_path / "uv"
    exit_code, output = run_script(str(new_dir), URL_GH_BLOB)

    assert exit_code == 0
    assert "🏁 Success! curated doc" in output

    content = (new_dir / "getting-started-first-steps.md").read_text()
    assert content.strip() != ""
    assert "<!DOCTYPE html>" not in content  # raw md fetched, not the blob HTML

    index = (new_dir / "INDEX.xml").read_text()
    assert f"<source_url>{URL_GH_BLOB}</source_url>" in index
    assert "<local_file>getting-started-first-steps.md</local_file>" in index
    assert "<title>First steps with uv</title>" in index
    assert "<description>PLACEHOLDER</description>" in index


@pytest.mark.github
def test_cli_github_404_fails_without_writing_files(tmp_path: Path) -> None:
    new_dir = tmp_path / "uv"
    exit_code, output = run_script(str(new_dir), URL_GH_BLOB_404)

    assert exit_code != 0
    assert "404 not found" in output
    md_files = list(new_dir.glob("*.md")) if new_dir.exists() else []
    assert md_files == []
    assert not (new_dir / "INDEX.xml").exists()
    assert not (new_dir / "README.md").exists()


@pytest.mark.firecrawl
def test_cli_curates_via_firecrawl_scrape(tmp_path: Path) -> None:
    """Only what a live scrape proves: the real page title and slugged filename."""
    new_dir = tmp_path / "zustand"
    exit_code, output = run_script(str(new_dir), URL_FIRECRAWL)

    assert exit_code == 0
    assert "🏁 Success! curated doc" in output

    index = (new_dir / "INDEX.xml").read_text()
    assert "<title>Updating state - Zustand</title>" in index
    assert f"<source_url>{URL_FIRECRAWL}</source_url>" in index
    assert "<local_file>learn-guides-updating-state.md</local_file>" in index
    assert f"<description>{PLACEHOLDER_DESCRIPTION}</description>" in index
