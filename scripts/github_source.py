"""GitHub raw-fetch curation path, dispatched from `curate_doc.py`.

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
_USER_AGENT = "docs-for-ai-curate/1.0"
_FILENAME_RE = re.compile(r"^[a-z0-9-]+\.md$")
_FRONTMATTER_TITLE_RE = re.compile(r"^title:\s*(?P<val>.+?)\s*$", re.MULTILINE)
_ANCHOR_LINK_RE = re.compile(r"^\[(?P<text>.+?)\]\(#.*\)$")


def _fail(code: str, detail: str, url: str) -> NoReturn:
    """Print the project ❌ error line and exit 1."""
    print(f"❌ Error: {code}|{detail}|{url}|")
    sys.exit(1)


def is_github_url(url: str) -> bool:
    """Return True for URLs the raw-fetch path handles; False routes to FireCrawl.

    The `.md` extension gate is not checked here — it's enforced later by
    :func:`derive_filename`.
    """
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    if host == "raw.githubusercontent.com":
        return True
    if host == "github.com":
        return "/blob/" in parsed.path
    return False


def to_raw_url(url: str) -> str:
    """Map a `github.com/…/blob/…` URL to its `raw.githubusercontent.com` form.

    Assumes :func:`is_github_url` is True for `url`. Exits with
    `UNSUPPORTED_GITHUB` if the path is not a `/blob/` file URL.
    """
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


def derive_filename(raw_url: str) -> str:
    r"""Derive a filename like `getting-started-features.md` from a raw GitHub URL.

    Exits with `UNSUPPORTED_GITHUB` (non-`.md` source) or `GITHUB_FILENAME`
    (derived stem violates `^[a-z0-9-]+\.md$`).
    """
    segments = urlparse(raw_url).path.strip("/").split("/")
    prefix_len = 3  # owner / repo / ref
    remainder = segments[prefix_len:]
    if not remainder or not remainder[-1].endswith(".md"):
        _fail("UNSUPPORTED_GITHUB", "only .md sources supported", raw_url)
    remainder = [*remainder[:-1], remainder[-1][:-3]]
    # Drop a single leading docs path segment (a docs.md root file fails the
    # pattern guard below loudly, which is the intended behaviour).
    if remainder and remainder[0] == "docs":
        remainder = remainder[1:]
    filename = "-".join(remainder).lower() + ".md"
    if not _FILENAME_RE.match(filename):
        _fail(
            "GITHUB_FILENAME",
            f"derived '{filename}' fails ^[a-z0-9-]+\\.md$",
            raw_url,
        )
    return filename


def extract_title(content: str, raw_url: str) -> str:
    """Resolve a title via frontmatter → first H1 → URL basename (never empty)."""
    body = content
    if content.startswith("---\n"):
        end = content.find("\n---", len("---\n"))
        if end != -1:
            match = _FRONTMATTER_TITLE_RE.search(content[len("---\n") : end])
            if match:
                title = match.group("val").strip().strip("\"'")
                if title:
                    return title
            newline = content.find("\n", end + 1)
            body = content[newline + 1 :] if newline != -1 else ""
    in_fence = False
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
        elif not in_fence and stripped.startswith("# "):
            heading = stripped[2:].strip()
            anchor = _ANCHOR_LINK_RE.match(heading)
            return anchor.group("text").strip() if anchor else heading
    basename = urlparse(raw_url).path.rsplit("/", 1)[-1].removesuffix(".md")
    return " ".join(w.capitalize() for w in basename.split("-")) or "Untitled"


def fetch_raw(raw_url: str) -> str:
    """Fetch raw markdown; prints `✅ Fetched raw markdown|…|` on success.

    Exits with `GITHUB_NOT_FOUND` (HTTP 404) or `GITHUB_FETCH` (any other
    fetch failure). No retry, no FireCrawl fallback.
    """
    # URL is constrained to https raw.githubusercontent.com by to_raw_url; S310 safe.
    request = urllib.request.Request(  # noqa: S310
        raw_url, headers={"User-Agent": _USER_AGENT}
    )
    try:
        with urllib.request.urlopen(  # noqa: S310
            request, timeout=FETCH_TIMEOUT_SECONDS
        ) as response:
            text = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        if exc.code == HTTP_NOT_FOUND:
            _fail("GITHUB_NOT_FOUND", "404 not found", raw_url)
        _fail("GITHUB_FETCH", f"HTTP {exc.code}", raw_url)
    except (urllib.error.URLError, OSError, UnicodeDecodeError) as exc:
        _fail("GITHUB_FETCH", str(exc), raw_url)
    print(f"✅ Fetched raw markdown|({len(text):,} characters)|")
    return text
