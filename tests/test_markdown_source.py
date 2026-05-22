"""Tests for markdown_source.py.

Pure-helper tests are offline; TestFetchMarkdown hits the real network.
"""

import pytest

from scripts.markdown_source import (
    extract_title,
    fetch_markdown,
    filename_from_raw_github_url,
    is_github_url,
    is_md_url,
    to_raw_github_url,
)


class TestIsGithubUrl:
    """Tests for is_github_url."""

    @pytest.mark.parametrize(
        ("url", "expected"),
        [
            ("https://raw.githubusercontent.com/astral-sh/uv/main/docs/x.md", True),
            ("https://github.com/astral-sh/uv/blob/main/docs/x.md", True),
            ("https://github.com/astral-sh/uv/blob/main/README.md", True),
            ("https://github.com/astral-sh/uv", False),
            ("https://github.com/astral-sh/uv/tree/main/docs", False),
            ("https://docs.astral.sh/uv/reference/cli/index.md", False),
            ("https://shiny.posit.co/py/docs/overview.html", False),
        ],
    )
    def test_classifies_url(self, url: str, expected: bool) -> None:  # noqa: FBT001 — bool is the correct param type for a URL classifier test
        """True for raw.githubusercontent.com URLs and any github.com blob path."""
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


class TestToRawGithubUrl:
    """Blob→raw GitHub URL normalisation."""

    def test_blob_url_becomes_raw(self) -> None:
        """github.com/.../blob/<ref>/<path> rewrites to raw.githubusercontent.com/..."""
        url = "https://github.com/astral-sh/uv/blob/main/docs/getting-started/first-steps.md"
        assert to_raw_github_url(url) == (
            "https://raw.githubusercontent.com/astral-sh/uv/main/"
            "docs/getting-started/first-steps.md"
        )

    def test_raw_url_passes_through_stripped(self) -> None:
        """A raw URL passes through, trailing slash stripped."""
        url = "https://raw.githubusercontent.com/astral-sh/uv/main/docs/x.md/"
        assert to_raw_github_url(url) == (
            "https://raw.githubusercontent.com/astral-sh/uv/main/docs/x.md"
        )

    def test_malformed_blob_url_fails(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Malformed blob URL exits with UNSUPPORTED_GITHUB (not a generic ValueError)."""
        with pytest.raises(SystemExit) as exc:
            to_raw_github_url("https://github.com/astral-sh/blob/x")
        assert exc.value.code == 1
        assert "UNSUPPORTED_GITHUB" in capsys.readouterr().out


class TestFilenameFromRawGithubUrl:
    """Filename derivation from a raw GitHub URL."""

    @pytest.mark.parametrize(
        ("raw_url", "expected"),
        [
            (
                "https://raw.githubusercontent.com/astral-sh/uv/main/"
                "docs/getting-started/features.md",
                "getting-started-features.md",
            ),
            (
                "https://raw.githubusercontent.com/astral-sh/uv/main/"
                "docs/concepts/projects/dependencies.md",
                "concepts-projects-dependencies.md",
            ),
            (
                "https://raw.githubusercontent.com/o/r/main/readme.md",
                "readme.md",
            ),
            (
                "https://raw.githubusercontent.com/o/r/main/docs/index.md",
                "index.md",
            ),
        ],
    )
    def test_derives_expected_name(self, raw_url: str, expected: str) -> None:
        """Path becomes hyphen-joined basename; one leading 'docs/' segment is dropped."""
        assert filename_from_raw_github_url(raw_url) == expected

    def test_non_md_source_fails(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Non-.md sources (e.g. pyproject.toml) exit with UNSUPPORTED_GITHUB."""
        with pytest.raises(SystemExit) as exc:
            filename_from_raw_github_url(
                "https://raw.githubusercontent.com/o/r/main/pyproject.toml"
            )
        assert exc.value.code == 1
        assert "UNSUPPORTED_GITHUB" in capsys.readouterr().out

    def test_pattern_violating_name_fails(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """A name breaking the filename pattern exits with GITHUB_FILENAME."""
        with pytest.raises(SystemExit) as exc:
            filename_from_raw_github_url(
                "https://raw.githubusercontent.com/o/r/main/docs/a_b.md"
            )
        assert exc.value.code == 1
        assert "GITHUB_FILENAME" in capsys.readouterr().out


class TestExtractTitle:
    """Tests for extract_title."""

    def test_frontmatter_title_unquoted(self) -> None:
        """Unquoted YAML frontmatter 'title:' takes precedence over the H1."""
        content = "---\ntitle: Working on projects\n---\n# Heading\n"
        assert extract_title(content, "x") == "Working on projects"

    def test_frontmatter_title_quoted(self) -> None:
        """Double-quoted frontmatter title is unquoted before being returned."""
        content = '---\ntitle: "Managing dependencies"\n---\n# H\n'
        assert extract_title(content, "x") == "Managing dependencies"

    def test_frontmatter_without_title_falls_to_h1(self) -> None:
        """Frontmatter without a 'title:' key falls through to the H1 heading."""
        content = "---\ndescription: x\n---\n# Python versions\n"
        assert extract_title(content, "x") == "Python versions"

    def test_h1_when_no_frontmatter(self) -> None:
        """First H1 is used when there is no frontmatter block at all."""
        content = "# First steps\n\nbody\n"
        assert extract_title(content, "x") == "First steps"

    def test_h1_anchor_link_is_unwrapped(self) -> None:
        """H1 of form '# [text](#anchor)' returns just 'text' (link syntax stripped)."""
        content = "# [CLI Reference](#cli-reference)\n"
        assert extract_title(content, "x") == "CLI Reference"

    def test_fenced_hash_is_ignored(self) -> None:
        """'#' lines inside ``` fences are skipped — only real headings count."""
        content = "```python\n# not a heading\n```\n# Real Title\n"
        assert extract_title(content, "x") == "Real Title"

    def test_basename_fallback_title_cased(self) -> None:
        """No frontmatter or H1: the title comes from the URL filename, Title-Cased."""
        content = "no headings here\n"
        url = "https://raw.githubusercontent.com/o/r/main/docs/getting-started.md"
        assert extract_title(content, url) == "Getting Started"

    def test_frontmatter_title_single_quoted(self) -> None:
        """Single-quoted frontmatter title is unquoted (mirrors double-quote handling)."""
        content = "---\ntitle: 'Managing dependencies'\n---\n# H\n"
        assert extract_title(content, "x") == "Managing dependencies"

    def test_empty_frontmatter_title_falls_through_to_h1(self) -> None:
        """An empty frontmatter title must not win; fall through to the H1."""
        content = "---\ntitle: ''\n---\n# Real Heading\n"
        assert extract_title(content, "x") == "Real Heading"


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
