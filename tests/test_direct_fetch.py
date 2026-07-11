"""Direct-fetch route resolution & fetching."""

from textwrap import dedent
from typing import TYPE_CHECKING

import pytest

from docs_for_ai.direct_fetch import (
    STRIPPED_SUFFIXES,
    extract_md_title,
    extract_rst_title,
    fetch_text,
    filename_from_canonical_url,
    github_blob_to_raw_url,
    github_filename_from_blob_url,
    is_github_url,
    load_direct_fetch_rules,
    resolve_route,
)
from docs_for_ai.errors import CurationError

if TYPE_CHECKING:
    from pathlib import Path


class TestIsGithubUrl:
    """is_github_url: a host-only gate; URL shape is validated downstream."""

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
        assert is_github_url(url) is expected


class TestLoadDirectFetchRules:
    """Registry loader: TOML `(transform → prefixes)`; unknown transforms fail loud."""

    def test_loads_and_normalises_prefixes(self, tmp_path: Path) -> None:
        """Parses transform → prefix lists; appends a missing trailing slash to each."""
        rules_file = tmp_path / "direct-fetch-rules.toml"
        rules_file.write_text(
            'append-md = ["https://vercel.com/docs/", "https://code.claude.com/docs"]\n'
            'readthedocs = ["https://rich.readthedocs.io/en/stable"]\n'
        )
        assert load_direct_fetch_rules(rules_file) == {
            "append-md": [
                "https://vercel.com/docs/",
                "https://code.claude.com/docs/",
            ],
            "readthedocs": ["https://rich.readthedocs.io/en/stable/"],
        }

    def test_unknown_transform_key_fails_loud(self, tmp_path: Path) -> None:
        rules_file = tmp_path / "direct-fetch-rules.toml"
        rules_file.write_text('mystery-transform = ["https://x.io/"]\n')
        with pytest.raises(CurationError, match="Unknown transform") as exc:
            load_direct_fetch_rules(rules_file)
        assert "mystery-transform" in str(exc.value)


# Registry prefixes for the offline routing tests below. A FetchRoute is a
# NamedTuple, so it compares equal to a plain (doc_format, fetch_url,
# canonical_url, filename) tuple — expectations are written as those tuples.
MD = "https://vercel.com/docs"
RTD = "https://rich.readthedocs.io/en/stable"
RULES = {"append-md": [f"{MD}/"], "readthedocs": [f"{RTD}/"]}


class TestResolveRoute:
    """The routing decision: doc_format, fetch URL, canonical, filename."""

    @pytest.mark.parametrize(
        ("url", "expected"),
        [
            (
                f"{MD}/storage.md",
                ("markdown", f"{MD}/storage.md", f"{MD}/storage", "storage.md"),
            ),
            (
                f"{MD}/storage.md?v=2",
                ("markdown", f"{MD}/storage.md", f"{MD}/storage", "storage.md"),
            ),
            (
                f"{MD}/guides/auth.md",
                (
                    "markdown",
                    f"{MD}/guides/auth.md",
                    f"{MD}/guides/auth",
                    "guides-auth.md",
                ),
            ),
            (
                f"{MD}/storage",
                ("markdown", f"{MD}/storage.md", f"{MD}/storage", "storage.md"),
            ),
            (
                f"{MD}/worktrees#x",
                ("markdown", f"{MD}/worktrees.md", f"{MD}/worktrees", "worktrees.md"),
            ),
            (
                f"{MD}/worktrees/?v=2",
                ("markdown", f"{MD}/worktrees.md", f"{MD}/worktrees", "worktrees.md"),
            ),
            (
                f"{MD}/v2.0/api",
                ("markdown", f"{MD}/v2.0/api.md", f"{MD}/v2.0/api", "v2-0-api.md"),
            ),
            (f"{MD}/page.html", (None, f"{MD}/page.html", f"{MD}/page.html", "page.md")),
            (f"{MD}/page.mdx", (None, f"{MD}/page.mdx", f"{MD}/page.mdx", "page.md")),
            (
                f"{RTD}/panel.html",
                (
                    "rst",
                    f"{RTD}/_sources/panel.rst.txt",
                    f"{RTD}/panel.html",
                    "panel.rst",
                ),
            ),
            (
                f"{RTD}/reference/console.html",
                (
                    "rst",
                    f"{RTD}/_sources/reference/console.rst.txt",
                    f"{RTD}/reference/console.html",
                    "reference-console.rst",
                ),
            ),
            (
                f"{RTD}/_sources/panel.rst.txt",
                (
                    "rst",
                    f"{RTD}/_sources/panel.rst.txt",
                    f"{RTD}/panel.html",
                    "panel.rst",
                ),
            ),
            (
                f"{RTD}/_sources/reference/console.rst.txt",
                (
                    "rst",
                    f"{RTD}/_sources/reference/console.rst.txt",
                    f"{RTD}/reference/console.html",
                    "reference-console.rst",
                ),
            ),
            (
                f"{RTD}/genindex",
                (None, f"{RTD}/genindex", f"{RTD}/genindex", "en-stable-genindex.md"),
            ),
            (
                "https://example.com/docs/notes.md",
                (
                    "markdown",
                    "https://example.com/docs/notes.md",
                    "https://example.com/docs/notes",
                    "notes.md",
                ),
            ),
            (
                "https://example.com/hello.rst.txt",
                (
                    "rst",
                    "https://example.com/hello.rst.txt",
                    "https://example.com/hello.rst.txt",
                    "hello.rst",
                ),
            ),
            (
                "https://example.com/docs/page",
                (
                    None,
                    "https://example.com/docs/page",
                    "https://example.com/docs/page",
                    "page.md",
                ),
            ),
            (
                "https://example.com",
                (None, "https://example.com", "https://example.com", "index.md"),
            ),
        ],
        ids=[
            "registry-md-fetched-as-is",
            "registry-md-query-stripped",
            "registry-md-nested-reverse-maps",
            "registry-no-suffix-appends-md",
            "registry-no-suffix-fragment-stripped",
            "registry-trailing-slash-before-query-stripped",
            "registry-dot-in-nonfinal-segment",
            "registry-html-suffix-declines-firecrawls",
            "registry-mdx-suffix-declines-firecrawls",
            "readthedocs-html-fetches-rst-twin",
            "readthedocs-nested-html-clean-filename",
            "readthedocs-raw-source-reverse-maps",
            "readthedocs-raw-nested-source-reverse-maps",
            "readthedocs-non-html-declines-firecrawls",
            "off-registry-md-fetched-as-is",
            "off-registry-rst-txt-fetched-as-is",
            "unmatched-path-firecrawls",
            "bare-domain-firecrawls",
        ],
    )
    def test_routes_url(
        self, url: str, expected: tuple[str | None, str, str, str]
    ) -> None:
        """Registry transform → raw `.md`/`.rst.txt` as-is → FireCrawl, in precedence."""
        assert resolve_route(url, RULES) == expected

    def test_github_blob_resolves_to_raw_route(self) -> None:
        """A GitHub blob URL resolves to its raw twin, ahead of the registry."""
        url = "https://github.com/o/r/blob/main/docs/guide.md"
        assert resolve_route(url, RULES) == (
            "markdown",
            "https://raw.githubusercontent.com/o/r/main/docs/guide.md",
            url,
            "guide.md",
        )


class TestFilenameFromCanonicalUrl:
    """Non-GitHub URL-path → filename derivation (slugified, doc/view suffix stripped)."""

    @pytest.mark.parametrize(
        ("url", "ext", "expected"),
        [
            (
                "https://clerk.com/docs/guides/users/inviting",
                "md",
                "guides-users-inviting.md",
            ),
            ("https://vercel.com/docs/monorepos", "md", "monorepos.md"),
            (
                "https://biomejs.dev/guides/configure-biome/",
                "md",
                "guides-configure-biome.md",
            ),
            ("https://docs.convex.dev/auth/convex-auth", "md", "auth-convex-auth.md"),
            ("https://site.com/Getting_Started", "md", "getting-started.md"),
            ("https://site.com/docs/v2.0/api", "md", "v2-0-api.md"),
            ("https://site.com/docs/guide?v=2#frag", "md", "guide.md"),
            ("https://example.com", "md", "index.md"),
            (
                "https://rich.readthedocs.io/en/stable/tree.html",
                "rst",
                "en-stable-tree.rst",
            ),
            (
                "https://rich.readthedocs.io/en/stable/_sources/panel.rst.txt",
                "rst",
                "en-stable-sources-panel.rst",
            ),
            ("https://site.com/guide.html", "md", "guide.md"),
            ("https://site.com/notes.md", "md", "notes.md"),
            ("https://site.com/page.HTML", "md", "page.md"),
            ("https://site.com/notes.MD", "md", "notes.md"),
            ("https://example.com/docs/", "md", "index.md"),
            ("panel", "rst", "panel.rst"),
            ("panel", "md", "panel.md"),
        ],
        ids=[
            "docs-segment-and-prefix-dropped",
            "docs-segment-dropped",
            "trailing-slash-stripped",
            "docs-subdomain-is-not-a-path-segment",
            "uppercase-and-underscore-slugged",
            "dot-in-nonfinal-segment-slugged",
            "query-and-fragment-stripped",
            "empty-path-falls-back-to-index",
            "html-suffix-stripped-ext-rst",
            "sources-rst-txt-stripped-ext-rst",
            "html-suffix-stripped-ext-md",
            "md-suffix-stripped-name-kept",
            "html-suffix-case-insensitive",
            "md-suffix-case-insensitive",
            "bare-docs-root-falls-back-to-index",
            "ext-overrides-to-rst",
            "ext-md-is-the-default",
        ],
    )
    def test_derives_filename(self, url: str, ext: str, expected: str) -> None:
        assert filename_from_canonical_url(url, ext=ext) == expected


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
            (
                "https://github.com/biomejs/website/blob/main/"
                "src/content/docs/guides/getting-started.mdx",
                "https://raw.githubusercontent.com/biomejs/website/main/"
                "src/content/docs/guides/getting-started.mdx",
            ),
            (
                "https://github.com/posit-dev/py-shiny-site/blob/main/"
                "get-started/deploy-cloud.qmd",
                "https://raw.githubusercontent.com/posit-dev/py-shiny-site/main/"
                "get-started/deploy-cloud.qmd",
            ),
        ],
    )
    def test_blob_url_becomes_raw(self, blob_url: str, raw_url: str) -> None:
        assert github_blob_to_raw_url(blob_url) == raw_url

    @pytest.mark.parametrize(
        "url",
        [
            "https://raw.githubusercontent.com/astral-sh/uv/main/docs/x.md",
            "https://github.com/astral-sh/uv",
            "https://github.com/astral-sh/uv/tree/main/docs",
            "https://github.com/astral-sh/uv/blob/dev/docs/x.md",
            "https://github.com/astral-sh/uv/blob/main/pyproject.toml",
            "https://github.com/astral-sh/uv/blob/main/docs/x.rst",
        ],
    )
    def test_non_blob_url_fails(self, url: str) -> None:
        """Raw, repo root, tree/, other branch, unsupported ext are all refused."""
        with pytest.raises(CurationError, match="Not a GitHub blob URL"):
            github_blob_to_raw_url(url)


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
            (
                "https://github.com/biomejs/website/blob/main/"
                "src/content/docs/guides/getting-started.mdx",
                "src-content-docs-guides-getting-started.mdx",
            ),
            (
                "https://github.com/posit-dev/py-shiny-site/blob/main/"
                "get-started/deploy-cloud.qmd",
                "get-started-deploy-cloud.qmd",
            ),
        ],
    )
    def test_derives_expected_name(self, blob_url: str, expected: str) -> None:
        assert github_filename_from_blob_url(blob_url) == expected

    def test_pattern_violating_name_fails(self) -> None:
        """A derived name breaking the filename pattern fails as a bad filename.

        Distinct from the no-match branch; the label is the only signal of which fired.
        """
        with pytest.raises(CurationError, match="Bad derived filename") as exc:
            github_filename_from_blob_url("https://github.com/o/r/blob/main/docs/a_b.md")
        assert "a_b.md" in str(exc.value)


class TestExtractMarkdownTitle:
    """Markdown title: frontmatter → first H1 → URL-basename fallback."""

    @pytest.mark.parametrize(
        ("content", "url", "expected"),
        [
            (
                "---\ntitle: Working on projects\n---\n# Heading\n",
                "x",
                "Working on projects",
            ),
            ('---\ntitle: "Managing dependencies"\n---\n', "x", "Managing dependencies"),
            ("---\ntitle: 'Managing dependencies'\n---\n", "x", "Managing dependencies"),
            ("---\ndescription: x\n---\n# Python versions\n", "x", "Python versions"),
            ("---\ntitle: ''\n---\n# Real Heading\n", "x", "Real Heading"),
            ("# First steps\n\nbody\n", "x", "First steps"),
            ("# [CLI Reference](#cli-reference)\n", "x", "CLI Reference"),
            ("```python\n# not a heading\n```\n# Real Title\n", "x", "Real Title"),
            (
                "no headings here\n",
                "https://raw.githubusercontent.com/o/r/main/docs/getting-started.md",
                "Getting Started",
            ),
        ],
        ids=[
            "frontmatter-wins-over-h1",
            "strips-double-quotes",
            "strips-single-quotes",
            "missing-title-key-falls-to-h1",
            "empty-title-falls-to-h1",
            "first-h1-without-frontmatter",
            "unwraps-h1-anchor-link",
            "ignores-hash-in-code-fence",
            "url-basename-title-cased-fallback",
        ],
    )
    def test_resolves_title(self, content: str, url: str, expected: str) -> None:
        assert extract_md_title(content, url) == expected


class TestExtractRstTitle:
    """RST title: first underlined heading → URL filename stem."""

    @pytest.mark.parametrize(
        ("content", "url", "expected"),
        [
            (
                # Tilde underline is as valid as '='; the first title still wins.
                dedent("""\
                    .. _target:

                    First Title
                    ~~~~~~~~~~~

                    Second Title
                    ============
                    """),
                "https://x.io/ignored.html",
                "First Title",
            ),
            (
                "A Longer Heading\n===\n\nbody with a stray short rule.\n",
                "https://x.io/fallback.html",
                "Fallback",
            ),
            ("just prose, no heading at all\n", "https://x.io/panel.html", "Panel"),
        ],
        ids=[
            "first-underlined-title-wins",
            "underline-must-span-the-title",
            "no-heading-falls-back-to-url-stem",
        ],
    )
    def test_resolves_title(self, content: str, url: str, expected: str) -> None:
        assert extract_rst_title(content, url) == expected


@pytest.mark.parametrize("suffix", STRIPPED_SUFFIXES)
def test_filename_and_title_strip_the_same_suffixes(suffix: str) -> None:
    url = f"https://x.io/name{suffix}"
    assert filename_from_canonical_url(url) == "name.md"
    assert extract_md_title("no heading here\n", url) == "Name"


@pytest.mark.direct_fetch
class TestFetchText:
    """Source fetch over HTTP, with structured 404/network failure."""

    def test_fetches_real_source(self) -> None:
        url = (
            "https://raw.githubusercontent.com/astral-sh/uv/main/"
            "docs/getting-started/first-steps.md"
        )
        text = fetch_text(url)
        assert len(text) > 0

    def test_404_fails_with_not_found(self) -> None:
        url = (
            "https://raw.githubusercontent.com/astral-sh/uv/main/"
            "docs/zzz-does-not-exist-xyz.md"
        )
        with pytest.raises(CurationError, match="404 not found"):
            fetch_text(url)


@pytest.mark.direct_fetch
@pytest.mark.parametrize(
    ("page", "expected_title"),
    [
        ("panel.html", "Panel"),
        ("syntax.html", "Syntax"),
        ("markup.html", "Console Markup"),
    ],
)
def test_real_rich_page_resolves_fetches_and_titles(
    page: str, expected_title: str
) -> None:
    url = f"https://rich.readthedocs.io/en/stable/{page}"
    route = resolve_route(url, load_direct_fetch_rules())
    assert route.doc_format == "rst"
    assert route.filename == f"{page.removesuffix('.html')}.rst"
    content = fetch_text(route.fetch_url)
    assert extract_rst_title(content, route.canonical_url) == expected_title


@pytest.mark.direct_fetch
def test_real_rich_raw_rst_source_reverse_maps_to_page() -> None:
    url = "https://rich.readthedocs.io/en/stable/_sources/panel.rst.txt"
    route = resolve_route(url, load_direct_fetch_rules())
    assert route.doc_format == "rst"
    assert route.canonical_url == "https://rich.readthedocs.io/en/stable/panel.html"
    assert route.filename == "panel.rst"
    content = fetch_text(route.fetch_url)
    assert extract_rst_title(content, route.canonical_url) == "Panel"
