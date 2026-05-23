"""Direct raw-markdown fetch for `.md` sources; GitHub blob/raw normalised first.

Failures use the `❌ Error: TYPE|detail|url|` print-and-exit convention.
"""

import re
import sys
import urllib.error
import urllib.request
from typing import NoReturn
from urllib.parse import urlparse

HTTP_NOT_FOUND = 404
FETCH_TIMEOUT_SECONDS = 30
USER_AGENT = "docs-for-ai-curate/1.0"
FILENAME_RE = re.compile(r"^[a-z0-9-]+\.md$")
FRONTMATTER_TITLE_RE = re.compile(r"^title:\s*(?P<val>.+?)\s*$", re.MULTILINE)
ANCHOR_LINK_RE = re.compile(r"^\[(?P<text>.+?)\]\(#.*\)$")
# The one shape we accept: a blob file on main/master with a .md extension.
GITHUB_BLOB_RE = re.compile(
    r"^https://github\.com/([^/]+)/([^/]+)/blob/(main|master)/(.+\.md)$",
    re.IGNORECASE,
)


def _fail(code: str, detail: str, url: str) -> NoReturn:
    """Emit a structured error line and exit."""
    print(f"❌ Error: {code}|{detail}|{url}|")
    sys.exit(1)


def is_github_url(url: str) -> bool:
    """True for any GitHub-host URL; routed to blob validation (else FireCrawl)."""
    return urlparse(url).netloc.lower() in {"github.com", "raw.githubusercontent.com"}


def is_md_url(url: str) -> bool:
    """True for direct `.md` URLs; False routes to FireCrawl."""
    return urlparse(url).path.endswith(".md")


def github_blob_to_raw_url(url: str) -> str:
    """Validate a GitHub blob URL (main/master, `.md`) and return its raw URL.

    Any other GitHub URL — raw, repo root, `tree/`, another branch, non-`.md` —
    fails with one structured error and exits.
    """
    match = GITHUB_BLOB_RE.match(url)
    if match is None:
        _fail(
            "GITHUB_BLOB",
            "expected https://github.com/<user>/<repo>/blob/(main|master)/<path>.md",
            url,
        )
    owner, repo, ref, path = match.groups()
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{path}"


def github_filename_from_blob_url(url: str) -> str:
    """Derive a `.md` filename from a GitHub blob URL's path.

    Drops a leading `docs/` segment, lowercases, hyphen-joins. A name that breaks
    the filename pattern exits with GITHUB_FILENAME.
    """
    match = GITHUB_BLOB_RE.match(url)
    if match is None:
        _fail("GITHUB_BLOB", "not a github blob .md URL", url)
    segments = match.group(4).removesuffix(".md").split("/")
    # Avoid a redundant "docs-" filename prefix.
    if segments and segments[0] == "docs":
        segments = segments[1:]
    filename = "-".join(segments).lower() + ".md"
    if not FILENAME_RE.match(filename):
        _fail("GITHUB_FILENAME", f"derived '{filename}' fails ^[a-z0-9-]+\\.md$", url)
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
    basename = urlparse(markdown_url).path.rsplit("/", 1)[-1].removesuffix(".md")
    return " ".join(w.capitalize() for w in basename.split("-")) or "Untitled"


def extract_title(content: str, markdown_url: str) -> str:
    """Resolve a non-empty title for the document at `markdown_url`."""
    return (
        _title_from_frontmatter(content)
        or _title_from_h1(content)
        or _title_from_url(markdown_url)
    )


def fetch_markdown(markdown_url: str) -> str:
    """Fetch markdown text from `markdown_url`; exits on 404 or network failure.

    Prints `✅ Fetched markdown|…|` on success. No retry, no FireCrawl fallback.
    """
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
