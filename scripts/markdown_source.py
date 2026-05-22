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


def _fail(code: str, detail: str, url: str) -> NoReturn:
    """Emit a structured error line and exit."""
    print(f"❌ Error: {code}|{detail}|{url}|")
    sys.exit(1)


def is_github_url(url: str) -> bool:
    """True for GitHub blob or raw URLs; False routes to FireCrawl."""
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    if host == "raw.githubusercontent.com":
        return True
    if host == "github.com":
        return "/blob/" in parsed.path
    return False


def is_md_url(url: str) -> bool:
    """True for direct `.md` URLs; False routes to FireCrawl."""
    return urlparse(url).path.endswith(".md")


def to_raw_github_url(url: str) -> str:
    """Map a `github.com/…/blob/…` URL to its `raw.githubusercontent.com` form."""
    url = url.rstrip("/")
    parsed = urlparse(url)
    if parsed.netloc.lower() == "raw.githubusercontent.com":
        return url
    parts = parsed.path.strip("/").split("/")
    min_segments = 5  # owner / repo / blob / ref / path…
    if len(parts) < min_segments or parts[2] != "blob":
        _fail("UNSUPPORTED_GITHUB", "not a github blob file URL", url)
    owner, repo, _blob, ref, *rest = parts
    return "https://raw.githubusercontent.com/" + "/".join([owner, repo, ref, *rest])


def filename_from_raw_github_url(raw_url: str) -> str:
    """Derive a filename from RAW GitHub URL."""
    segments = urlparse(raw_url).path.strip("/").split("/")
    prefix_len = 3  # owner / repo / ref
    remainder = segments[prefix_len:]
    if not remainder or not remainder[-1].endswith(".md"):
        _fail("UNSUPPORTED_GITHUB", "only .md sources supported", raw_url)
    remainder = [*remainder[:-1], remainder[-1][:-3]]
    # Avoid a redundant "docs-" filename prefix.
    if remainder and remainder[0] == "docs":
        remainder = remainder[1:]
    filename = "-".join(remainder).lower() + ".md"
    if not FILENAME_RE.match(filename):
        _fail(
            "GITHUB_FILENAME",
            f"derived '{filename}' fails ^[a-z0-9-]+\\.md$",
            raw_url,
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
