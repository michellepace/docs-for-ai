"""Tests for markdown_source.py; network tests gated by `firecrawl`/`github` markers."""

from typing import TYPE_CHECKING

import pytest

from scripts.markdown_source import (
    extract_title,
    fetch_markdown,
    github_blob_to_raw_url,
    github_filename_from_blob_url,
    is_github_url,
    is_md_url,
    load_md_allowlist,
    resolve_md_route,
)

if TYPE_CHECKING:
    from pathlib import Path


class TestIsGithubUrl:
    """Tests for is_github_url: a host-only gate (URL shape is validated elsewhere)."""

    @pytest.mark.parametrize(
        ("url", "expected"),
        [
            ("https://raw.githubusercontent.com/astral-sh/uv/main/docs/x.md", True),
            ("https://github.com/astral-sh/uv/blob/main/docs/x.md", True),
            ("https://github.com/astral-sh/uv/blob/main/README.md", True),
            ("https://github.com/astral-sh/uv", True),
            ("https://github.com/astral-sh/uv/tree/main/docs", True),
            ("https://docs.astral.sh/uv/reference/cli/index.md", False),
            ("https://shiny.posit.co/py/docs/overview.html", False),
        ],
    )
    def test_classifies_url(self, url: str, expected: bool) -> None:  # noqa: FBT001 — bool is the correct param type for a URL classifier test
        """True for any github.com / raw.githubusercontent.com host; else False."""
        assert is_github_url(url) is expected


class TestIsMdUrl:
    """Tests for is_md_url (the generic .md routing gate)."""

    @pytest.mark.parametrize(
        ("url", "expected"),
        [
            ("https://example.com/docs/a.md", True),
            ("https://raw.githubusercontent.com/o/r/m/x.md", True),
            ("https://example.com/docs/a.md?v=2", True),
            ("https://example.com/docs/guide", False),
            ("https://example.com", False),
        ],
    )
    def test_classifies_url(self, url: str, expected: bool) -> None:  # noqa: FBT001 — bool is the correct param type for a URL classifier test
        """True only when the URL path ends in `.md`; query string is ignored."""
        assert is_md_url(url) is expected


class TestLoadMdAllowlist:
    """Allowlist loader: one prefix per line, ignoring blanks and `#` comments."""

    def test_parses_prefixes_ignoring_comments_and_blanks(self, tmp_path: Path) -> None:
        """Comment lines, blank lines, and surrounding whitespace are dropped."""
        allowlist = tmp_path / "md_allowlist.txt"
        allowlist.write_text(
            "# a comment\n"
            "\n"
            "https://vercel.com/docs/\n"
            "  https://vitest.dev/guide/  \n"
            "\n"
            "# trailing comment\n"
        )
        assert load_md_allowlist(allowlist) == [
            "https://vercel.com/docs/",
            "https://vitest.dev/guide/",
        ]


BASE = "https://vercel.com/docs"
PREFIXES = [f"{BASE}/"]


class TestResolveMdRoute:
    """The non-GitHub routing decision plus the canonical URL it records."""

    @pytest.mark.parametrize(
        ("url", "expected"),
        [
            (f"{BASE}/storage.md", (False, f"{BASE}/storage.md", f"{BASE}/storage")),
            (f"{BASE}/storage.md?v=2", (False, f"{BASE}/storage.md", f"{BASE}/storage")),
            (f"{BASE}/storage", (False, f"{BASE}/storage.md", f"{BASE}/storage")),
            (BASE, (False, f"{BASE}.md", BASE)),
            (f"{BASE}-other", (True, None, f"{BASE}-other")),
            (f"{BASE}/worktrees#x", (False, f"{BASE}/worktrees.md", f"{BASE}/worktrees")),
            (f"{BASE}/page.html", (True, None, f"{BASE}/page.html")),
            (f"{BASE}/v2.0/api", (False, f"{BASE}/v2.0/api.md", f"{BASE}/v2.0/api")),
            ("https://x.io/docs/page", (True, None, "https://x.io/docs/page")),
            ("https://example.com", (True, None, "https://example.com")),
        ],
        ids=[
            "md-suffix-fetched-as-is",
            "md-suffix-query-stripped",
            "allowlisted-no-suffix-appends-md",
            "allowlisted-section-root-appends-md",
            "boundary-sibling-path-firecrawls",
            "allowlisted-fragment-stripped",
            "allowlisted-html-suffix-firecrawls",
            "dot-in-nonfinal-segment-still-appends",
            "non-allowlisted-no-suffix-firecrawls",
            "bare-domain-firecrawls",
        ],
    )
    def test_routes_url(self, url: str, expected: tuple[bool, str | None, str]) -> None:
        """`.md` wins first; else allowlisted no-suffix appends; else FireCrawl.

        A `MdRoute` compares equal to a plain `(use_firecrawl, fetch_url,
        canonical_url)` tuple, so expectations read as tuples.
        """
        assert resolve_md_route(url, PREFIXES) == expected

    def test_md_suffix_takes_precedence_over_allowlist(self) -> None:
        """An allowlisted `.md` URL is fetched as-is, not appended."""
        url = f"{BASE}/storage.md"
        assert resolve_md_route(url, PREFIXES).fetch_url == url


class TestGithubBlobToRawUrl:
    """Blob → raw GitHub URL validation and normalisation."""

    @pytest.mark.parametrize(
        ("blob_url", "raw_url"),
        [
            (
                "https://github.com/astral-sh/uv/blob/main/"
                "docs/getting-started/first-steps.md",
                "https://raw.githubusercontent.com/astral-sh/uv/main/"
                "docs/getting-started/first-steps.md",
            ),
            (
                "https://github.com/o/r/blob/master/docs/x.md",
                "https://raw.githubusercontent.com/o/r/master/docs/x.md",
            ),
        ],
    )
    def test_blob_url_becomes_raw(self, blob_url: str, raw_url: str) -> None:
        """github.com/.../blob/(main|master)/<path>.md rewrites to its raw URL."""
        assert github_blob_to_raw_url(blob_url) == raw_url

    @pytest.mark.parametrize(
        "url",
        [
            "https://raw.githubusercontent.com/astral-sh/uv/main/docs/x.md",
            "https://github.com/astral-sh/uv",
            "https://github.com/astral-sh/uv/tree/main/docs",
            "https://github.com/astral-sh/uv/blob/dev/docs/x.md",
            "https://github.com/astral-sh/uv/blob/main/pyproject.toml",
        ],
    )
    def test_non_blob_url_fails(
        self, url: str, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Raw, repo root, tree/, other branch, and non-.md all exit with GITHUB_BLOB."""
        with pytest.raises(SystemExit) as exc:
            github_blob_to_raw_url(url)
        assert exc.value.code == 1
        assert "GITHUB_BLOB" in capsys.readouterr().out


class TestGithubFilenameFromBlobUrl:
    """Filename derivation from a GitHub blob URL."""

    @pytest.mark.parametrize(
        ("blob_url", "expected"),
        [
            (
                "https://github.com/astral-sh/uv/blob/main/"
                "docs/getting-started/features.md",
                "getting-started-features.md",
            ),
            (
                "https://github.com/astral-sh/uv/blob/main/"
                "docs/concepts/projects/dependencies.md",
                "concepts-projects-dependencies.md",
            ),
            (
                "https://github.com/o/r/blob/main/readme.md",
                "readme.md",
            ),
            (
                "https://github.com/o/r/blob/main/docs/index.md",
                "index.md",
            ),
        ],
    )
    def test_derives_expected_name(self, blob_url: str, expected: str) -> None:
        """Path segments are hyphen-joined; one leading 'docs/' segment is dropped."""
        assert github_filename_from_blob_url(blob_url) == expected

    def test_pattern_violating_name_fails(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """A name breaking the filename pattern exits with GITHUB_FILENAME."""
        with pytest.raises(SystemExit) as exc:
            github_filename_from_blob_url("https://github.com/o/r/blob/main/docs/a_b.md")
        assert exc.value.code == 1
        assert "GITHUB_FILENAME" in capsys.readouterr().out


class TestExtractTitle:
    """Tests for extract_title (frontmatter → H1 → URL-basename fallback)."""

    @pytest.mark.parametrize(
        ("content", "expected"),
        [
            ("---\ntitle: Working on projects\n---\n# Heading\n", "Working on projects"),
            ('---\ntitle: "Managing dependencies"\n---\n# H\n', "Managing dependencies"),
            ("---\ntitle: 'Managing dependencies'\n---\n# H\n", "Managing dependencies"),
            ("---\ndescription: x\n---\n# Python versions\n", "Python versions"),
            ("---\ntitle: ''\n---\n# Real Heading\n", "Real Heading"),
            ("# First steps\n\nbody\n", "First steps"),
            ("# [CLI Reference](#cli-reference)\n", "CLI Reference"),
            ("```python\n# not a heading\n```\n# Real Title\n", "Real Title"),
        ],
        ids=[
            "frontmatter-unquoted",
            "frontmatter-double-quoted",
            "frontmatter-single-quoted",
            "no-title-key-falls-to-h1",
            "empty-title-falls-to-h1",
            "h1-no-frontmatter",
            "h1-anchor-unwrapped",
            "fenced-hash-ignored",
        ],
    )
    def test_resolves_title(self, content: str, expected: str) -> None:
        """Frontmatter title wins (quotes stripped); else first real H1."""
        assert extract_title(content, "x") == expected

    def test_basename_fallback_title_cased(self) -> None:
        """No frontmatter or H1: the title comes from the URL filename, Title-Cased."""
        content = "no headings here\n"
        url = "https://raw.githubusercontent.com/o/r/main/docs/getting-started.md"
        assert extract_title(content, url) == "Getting Started"


RAW_OK = (
    "https://raw.githubusercontent.com/astral-sh/uv/main/"
    "docs/getting-started/first-steps.md"
)
RAW_404 = (
    "https://raw.githubusercontent.com/astral-sh/uv/main/docs/zzz-does-not-exist-xyz.md"
)


@pytest.mark.github
class TestFetchMarkdown:
    """Markdown fetch over HTTP, with structured 404/network failure."""

    def test_fetches_real_markdown(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Real-network fetch returns non-empty markdown and prints the success line."""
        text = fetch_markdown(RAW_OK)
        assert len(text) > 0
        assert "✅ Fetched markdown|" in capsys.readouterr().out

    def test_404_fails_with_not_found(self, capsys: pytest.CaptureFixture[str]) -> None:
        """404 on raw URL exits non-zero with structured FETCH_NOT_FOUND error line."""
        with pytest.raises(SystemExit) as exc:
            fetch_markdown(RAW_404)
        assert exc.value.code == 1
        assert "❌ Error: FETCH_NOT_FOUND|" in capsys.readouterr().out
