"""Direct raw fetch for documentation sources; GitHub blob/raw normalised first.

GitHub blobs may be `.md`, `.mdx`, or `.qmd`; other hosts use `.md`. Failures use
the `❌ Error: TYPE|detail|url|` print-and-exit convention.
"""

import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import NamedTuple, NoReturn
from urllib.parse import urlparse, urlunparse

HTTP_NOT_FOUND = 404
FETCH_TIMEOUT_SECONDS = 30
USER_AGENT = "docs-for-ai-curate/1.0"
MD_ALLOWLIST_PATH = Path(__file__).parent / "md_allowlist.txt"
FILENAME_RE = re.compile(r"^[a-z0-9-]+\.(?:md|mdx|qmd)$")
FRONTMATTER_TITLE_RE = re.compile(r"^title:\s*(?P<val>.+?)\s*$", re.MULTILINE)
ANCHOR_LINK_RE = re.compile(r"^\[(?P<text>.+?)\]\(#.*\)$")
# Accepted shapes: a blob file on main/master ending in .md/.mdx/.qmd.
# Groups: owner, repo, ref, path-without-extension, extension.
GITHUB_BLOB_RE = re.compile(
    r"^https://github\.com/([^/]+)/([^/]+)/blob/(main|master)/(.+)\.(md|mdx|qmd)$",
    re.IGNORECASE,
)


def _fail(code: str, detail: str, url: str) -> NoReturn:
    """Emit a structured error line and exit."""
    print(f"❌ Error: {code}|{detail}|{url}|")
    sys.exit(1)


def is_github_url(url: str) -> bool:
    """True if the URL is on a GitHub host; its shape is validated downstream."""
    return urlparse(url).netloc.lower() in {"github.com", "raw.githubusercontent.com"}


def is_md_url(url: str) -> bool:
    """True when the URL's path ends in `.md`; query and fragment are ignored."""
    return urlparse(url).path.endswith(".md")


def load_md_allowlist(path: Path = MD_ALLOWLIST_PATH) -> list[str]:
    """Load non-GitHub host prefixes that serve a `.md` twin of each page.

    One prefix per line; blank lines and `#` comments are ignored.
    """
    return [
        stripped
        for line in path.read_text().splitlines()
        if (stripped := line.strip()) and not stripped.startswith("#")
    ]


class MdRoute(NamedTuple):
    """How to source a non-GitHub URL, and the canonical URL to record.

    `fetch_url` is the direct `.md` to fetch, or None when `use_firecrawl`.
    `canonical_url` is always query/fragment-free with no trailing `.md`.
    """

    use_firecrawl: bool
    fetch_url: str | None
    canonical_url: str


def _strip_query_fragment(url: str) -> str:
    """Drop any `?query` and `#fragment`, keeping scheme, host, and path."""
    return urlunparse(urlparse(url)._replace(query="", fragment=""))


def _has_no_file_suffix(url: str) -> bool:
    """True when the URL's final path segment carries no `.` file suffix."""
    return "." not in urlparse(url).path.rstrip("/").rsplit("/", 1)[-1]


def resolve_md_route(url: str, prefixes: list[str]) -> MdRoute:
    """Resolve a slash-trimmed non-GitHub URL to its fetch source and canonical URL.

    `.md` URLs fetch as-is, allowlisted suffixless URLs via a `.md` twin, else FireCrawl.
    """
    url = _strip_query_fragment(url)
    if is_md_url(url):
        return MdRoute(
            use_firecrawl=False, fetch_url=url, canonical_url=url.removesuffix(".md")
        )
    if _has_no_file_suffix(url) and any(f"{url}/".startswith(p) for p in prefixes):
        return MdRoute(use_firecrawl=False, fetch_url=f"{url}.md", canonical_url=url)
    return MdRoute(use_firecrawl=True, fetch_url=None, canonical_url=url)


def github_blob_to_raw_url(url: str) -> str:
    """Convert a GitHub blob `.md`/`.mdx`/`.qmd` URL (main/master) to its raw URL.

    Any non-conforming GitHub URL exits with a structured GITHUB_BLOB error.
    """
    match = GITHUB_BLOB_RE.match(url)
    if match is None:
        _fail(
            "GITHUB_BLOB",
            "expected https://github.com/<user>/<repo>/blob/(main|master)/"
            "<path>.(md|mdx|qmd)",
            url,
        )
    owner, repo, ref, path, ext = match.groups()
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{path}.{ext}"


def github_filename_from_blob_url(url: str) -> str:
    """Derive a filename from a GitHub blob URL's path, keeping its extension.

    Strips a leading `docs/`, lowercases, hyphen-joins; bad names exit GITHUB_FILENAME.
    """
    match = GITHUB_BLOB_RE.match(url)
    if match is None:
        _fail("GITHUB_BLOB", "not a github blob .md/.mdx/.qmd URL", url)
    segments = match.group(4).split("/")
    # Avoid a redundant "docs-" filename prefix.
    if segments and segments[0] == "docs":
        segments = segments[1:]
    filename = "-".join(segments).lower() + "." + match.group(5).lower()
    if not FILENAME_RE.match(filename):
        _fail(
            "GITHUB_FILENAME",
            f"derived '{filename}' fails ^[a-z0-9-]+\\.(?:md|mdx|qmd)$",
            url,
        )
    return filename


def _title_from_frontmatter(content: str) -> str | None:
    """The title declared in the document's YAML frontmatter, if any."""
    if not content.startswith("---\n"):
        return None
    end = content.find("\n---", len("---\n"))
    if end == -1:
        return None
    match = FRONTMATTER_TITLE_RE.search(content[len("---\n") : end])
    if match is None:
        return None
    return match.group("val").strip().strip("\"'") or None


def _title_from_h1(content: str) -> str | None:
    """The document's first H1 heading as plain text, if any."""
    # A '#' line inside a code fence isn't a heading
    in_fence = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
        elif not in_fence and stripped.startswith("# "):
            heading = stripped[2:].strip()
            # An H1 as '# [Title](#title)', yields 'Title'.
            anchor = ANCHOR_LINK_RE.match(heading)
            return anchor.group("text").strip() if anchor else heading
    return None


def _title_from_url(markdown_url: str) -> str:
    """A human-readable fallback title derived from the URL's filename."""
    basename = urlparse(markdown_url).path.rsplit("/", 1)[-1]
    basename = re.sub(r"\.(?:md|mdx|qmd)$", "", basename, flags=re.IGNORECASE)
    return " ".join(w.capitalize() for w in basename.split("-")) or "Untitled"


def extract_title(content: str, markdown_url: str) -> str:
    """Resolve a title: frontmatter, else first H1, else the URL filename."""
    return (
        _title_from_frontmatter(content)
        or _title_from_h1(content)
        or _title_from_url(markdown_url)
    )


def fetch_markdown(markdown_url: str) -> str:
    """Fetch markdown text from `markdown_url`; exits on 404 or network failure."""
    # S310: doc URL is operator-supplied via the CLI
    request = urllib.request.Request(  # noqa: S310
        markdown_url, headers={"User-Agent": USER_AGENT}
    )
    try:
        with urllib.request.urlopen(  # noqa: S310
            request, timeout=FETCH_TIMEOUT_SECONDS
        ) as response:
            text = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        if exc.code == HTTP_NOT_FOUND:
            _fail("FETCH_NOT_FOUND", "404 not found", markdown_url)
        _fail("FETCH_FAILED", f"HTTP {exc.code}", markdown_url)
    except (urllib.error.URLError, OSError, UnicodeDecodeError) as exc:
        _fail("FETCH_FAILED", str(exc), markdown_url)
    print(f"✅ Fetched markdown|({len(text):,} characters)|")
    return text
