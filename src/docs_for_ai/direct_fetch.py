"""Resolve a doc URL to a fetch route (precedence order), fetch and extract its title."""

import re
import tomllib
import urllib.error
import urllib.request
from itertools import pairwise
from pathlib import Path
from typing import Literal, NamedTuple, NoReturn
from urllib.parse import urlparse, urlunparse

from docs_for_ai.errors import CurationError

# A directly-fetched doc's format; None on a route means "scrape via FireCrawl".
DocFormat = Literal["markdown", "rst"]

HTTP_NOT_FOUND = 404
FETCH_TIMEOUT_SECONDS = 30
USER_AGENT = "docs-for-ai-curate/1.0"
DIRECT_FETCH_RULES_PATH = Path(__file__).parent / "direct-fetch-rules.toml"
FILENAME_RE = re.compile(r"^[a-z0-9-]+\.(?:md|mdx|qmd)$")
FRONTMATTER_TITLE_RE = re.compile(r"^title:\s*(?P<val>.+?)\s*$", re.MULTILINE)
ANCHOR_LINK_RE = re.compile(r"^\[(?P<text>.+?)\]\(#.*\)$")
# Accepted shapes: a blob file on main/master ending in .md/.mdx/.qmd.
# Groups: owner, repo, ref, path-without-extension, extension.
GITHUB_BLOB_RE = re.compile(
    r"^https://github\.com/([^/]+)/([^/]+)/blob/(main|master)/(.+)\.(md|mdx|qmd)$",
    re.IGNORECASE,
)
STRIPPED_SUFFIXES = (".rst.txt", ".html", ".mdx", ".qmd", ".md", ".rst")
_STRIPPED_SUFFIX_RE = re.compile(
    r"(?:" + "|".join(re.escape(suffix) for suffix in STRIPPED_SUFFIXES) + r")$",
    re.IGNORECASE,
)
# Raw URLs fetched as-is, mapped to their (format, output extension).
RAW_SUFFIXES: dict[str, tuple[DocFormat, str]] = {
    ".md": ("markdown", "md"),
    ".rst.txt": ("rst", "rst"),
}


def _fail(label: str, detail: str = "", locus: str = "") -> NoReturn:
    """Fail with a `label[: detail][ — locus]` message."""
    message = label
    if detail:
        message += f": {detail}"
        if locus:
            message += f" — {locus}"
    elif locus:
        message += f": {locus}"
    raise CurationError(message)


def is_github_url(url: str) -> bool:
    """True if the URL is on a GitHub host; its shape is validated downstream."""
    return urlparse(url).netloc.lower() in {"github.com", "raw.githubusercontent.com"}


def _raw_format(url: str) -> tuple[DocFormat, str] | None:
    """The (format, extension) of a directly fetchable raw URL, else None.

    `.md` → markdown; `.rst.txt` → reStructuredText.
    """
    path = urlparse(url).path
    for suffix, format_ext in RAW_SUFFIXES.items():
        if path.endswith(suffix):
            return format_ext
    return None


class FetchRoute(NamedTuple):
    """How to source a URL: its format, the URL to fetch, and the outputs.

    `doc_format` is None for FireCrawl, else `"markdown"` or `"rst"` — it selects
    the title extractor and the output extension.
    `fetch_url` is fetched directly for a `doc_format`; for FireCrawl it is the
    URL scraped.
    `canonical_url` (recorded as `<source_url>`) is query/fragment-free.
    `filename` is the resolved output filename; its extension reflects the format.
    """

    doc_format: DocFormat | None
    fetch_url: str
    canonical_url: str
    filename: str


def _strip_query_fragment(url: str) -> str:
    """Drop any `?query` and `#fragment`, keeping scheme, host, and path."""
    return urlunparse(urlparse(url)._replace(query="", fragment=""))


def _has_no_file_suffix(url: str) -> bool:
    """True when the URL's final path segment carries no `.` file suffix."""
    return "." not in urlparse(url).path.rstrip("/").rsplit("/", 1)[-1]


def _slugify(text: str) -> str:
    """Lowercase `text` to a hyphen-joined `[a-z0-9]` slug (empty if no usable chars)."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _strip_doc_suffix(text: str) -> str:
    """Drop one trailing doc/view suffix (`.html`, `.rst.txt`, `.md`, …), if any."""
    return _STRIPPED_SUFFIX_RE.sub("", text)


def filename_from_canonical_url(url: str, ext: str = "md") -> str:
    """Slugify a URL path into a `{slug}.{ext}` filename.

    A trailing doc/view suffix is stripped first, then a `docs` segment and any
    prefix before it are dropped to avoid a redundant `docs-` slug.
    """
    path = _strip_doc_suffix(urlparse(url).path.strip("/"))
    segments = [s for s in path.split("/") if s]
    if "docs" in segments:
        segments = segments[segments.index("docs") + 1 :]
    slug = _slugify("-".join(segments))
    return f"{slug or 'index'}.{ext}"


def _matching_prefix(url: str, prefixes: list[str]) -> str | None:
    """The longest registry prefix `url` falls under, or None (boundary-safe)."""
    matches = [p for p in prefixes if f"{url}/".startswith(p)]
    return max(matches, key=len) if matches else None


def _raw_format_route(url: str) -> FetchRoute | None:
    """A raw `.md`/`.rst.txt` URL fetched as-is, else None.

    Markdown drops its `.md` for the canonical URL (so the two spellings collapse);
    reStructuredText keeps its raw URL.
    """
    fmt = _raw_format(url)
    if fmt is None:
        return None
    format_name, ext = fmt
    canonical = url.removesuffix(".md") if format_name == "markdown" else url
    filename = filename_from_canonical_url(canonical, ext=ext)
    return FetchRoute(format_name, url, canonical, filename)


def _github_route(url: str) -> FetchRoute:
    """A GitHub blob fetched from its raw twin; the blob URL stays canonical."""
    raw_url = github_blob_to_raw_url(url)
    return FetchRoute("markdown", raw_url, url, github_filename_from_blob_url(url))


def _append_md_route(url: str, _prefix: str) -> FetchRoute | None:
    """Map a suffix-less page and its `.md` twin, both saved as one `.md` file.

    Any other suffix (`.mdx`, `.html`, …) is declined.
    Accepts `_prefix` only to share the transform dispatch signature.
    """
    if url.endswith(".md"):  # reverse — check first
        canonical = url.removesuffix(".md")
    elif _has_no_file_suffix(url):  # forward page
        canonical = url
    else:
        return None
    return FetchRoute(
        "markdown", f"{canonical}.md", canonical, filename_from_canonical_url(canonical)
    )


def _rst_filename(rel: str) -> str:
    """Slugify a page-relative path (e.g. `reference/console`) into `{slug}.rst`."""
    return f"{_slugify(rel) or 'index'}.rst"


def _readthedocs_route(url: str, prefix: str) -> FetchRoute | None:
    """Map a readthedocs `.html` page and its `_sources/*.rst.txt` twin, saved `.rst`.

    Bidirectional: forward, a `.html` page fetches its twin and stays canonical; reverse,
    a `_sources/{rel}.rst.txt` URL is fetched as-is but maps back to the page — so both
    spellings converge on one file and one index entry. Declines anything else.
    """
    rel = url.removeprefix(prefix)
    if rel.startswith("_sources/") and rel.endswith(".rst.txt"):  # reverse — check first
        rel = rel.removeprefix("_sources/").removesuffix(".rst.txt")
        fetch_url, canonical = url, f"{prefix}{rel}.html"
    elif url.endswith(".html"):  # forward page
        rel = rel.removesuffix(".html")
        fetch_url, canonical = f"{prefix}_sources/{rel}.rst.txt", url
    else:
        return None
    return FetchRoute("rst", fetch_url, canonical, _rst_filename(rel))


def _firecrawl_route(url: str) -> FetchRoute:
    """No direct twin: scrape the URL via FireCrawl (doc_format None)."""
    return FetchRoute(None, url, url, filename_from_canonical_url(url))


TRANSFORMS = {"append-md": _append_md_route, "readthedocs": _readthedocs_route}


def resolve_route(url: str, rules: dict[str, list[str]]) -> FetchRoute:
    """Resolve a URL to its fetch source and outputs, in precedence order."""
    url = _strip_query_fragment(url).rstrip("/")
    if is_github_url(url):
        return _github_route(url)
    for name, prefixes in rules.items():
        prefix = _matching_prefix(url, prefixes)
        if prefix and (route := TRANSFORMS[name](url, prefix)):
            return route
    return _raw_format_route(url) or _firecrawl_route(url)


def _normalise_prefixes(rules: dict[str, list[str]]) -> dict[str, list[str]]:
    """Ensure every registry prefix ends in `/` so prefix matching is boundary-safe."""
    return {
        name: [p if p.endswith("/") else f"{p}/" for p in prefixes]
        for name, prefixes in rules.items()
    }


def load_direct_fetch_rules(
    path: Path = DIRECT_FETCH_RULES_PATH,
) -> dict[str, list[str]]:
    """Load the `(transform → URL-prefixes)` registry; unknown transforms fail loud."""
    rules = tomllib.loads(path.read_text())
    unknown = [name for name in rules if name not in TRANSFORMS]
    if unknown:
        joined = ", ".join(unknown)
        _fail("Unknown transform", joined, str(path))
    return _normalise_prefixes(rules)


def github_blob_to_raw_url(url: str) -> str:
    """Convert a GitHub blob `.md`/`.mdx`/`.qmd` URL (main/master) to its raw URL."""
    match = GITHUB_BLOB_RE.match(url)
    if match is None:
        _fail(
            "Not a GitHub blob URL",
            "expected https://github.com/<user>/<repo>/blob/(main|master)/"
            "<path>.(md|mdx|qmd)",
            url,
        )
    owner, repo, ref, path, ext = match.groups()
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{path}.{ext}"


def github_filename_from_blob_url(url: str) -> str:
    """Derive a filename from a GitHub blob URL's path, keeping its extension.

    Strips a leading `docs/`, lowercases, hyphen-joins.
    """
    match = GITHUB_BLOB_RE.match(url)
    if match is None:
        _fail("Not a GitHub blob URL", locus=url)
    segments = match.group(4).split("/")
    # Avoid a redundant "docs-" filename prefix.
    if segments and segments[0] == "docs":
        segments = segments[1:]
    filename = "-".join(segments).lower() + "." + match.group(5).lower()
    if not FILENAME_RE.match(filename):
        _fail(
            "Bad derived filename",
            f"'{filename}' fails ^[a-z0-9-]+\\.(?:md|mdx|qmd)$",
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


def _title_from_url(url: str) -> str:
    """A human-readable fallback title derived from the URL's filename."""
    basename = _strip_doc_suffix(urlparse(url).path.rsplit("/", 1)[-1])
    return " ".join(w.capitalize() for w in basename.split("-")) or "Untitled"


def _is_rst_adornment(line: str) -> bool:
    """True when a line is a run of a single RST adornment (punctuation) character."""
    stripped = line.strip()
    return bool(stripped) and len(set(stripped)) == 1 and not stripped[0].isalnum()


def _title_from_rst(content: str) -> str | None:
    """The first RST section title: a text line above an adornment that spans it."""
    for text, underline in pairwise(content.splitlines()):
        title = text.strip()
        if (
            title
            and not _is_rst_adornment(text)  # skip an overline
            and _is_rst_adornment(underline)
            and len(underline.strip()) >= len(title)
        ):
            return title
    return None


def extract_md_title(content: str, markdown_url: str) -> str:
    """Resolve a title: frontmatter, else first H1, else the URL filename."""
    return (
        _title_from_frontmatter(content)
        or _title_from_h1(content)
        or _title_from_url(markdown_url)
    )


def extract_rst_title(content: str, rst_url: str) -> str:
    """Resolve an RST title: first underlined heading, else the URL filename."""
    return _title_from_rst(content) or _title_from_url(rst_url)


TITLE_EXTRACTORS = {"markdown": extract_md_title, "rst": extract_rst_title}


def extract_title(content: str, doc_format: DocFormat, url: str) -> str:
    """Resolve a title for `content` via the route format's title extractor."""
    return TITLE_EXTRACTORS[doc_format](content, url)


def fetch_text(fetch_url: str) -> str:
    """Fetch text from `fetch_url`."""
    # S310: doc URL is operator-supplied via the CLI
    request = urllib.request.Request(  # noqa: S310
        fetch_url, headers={"User-Agent": USER_AGENT}
    )
    try:
        with urllib.request.urlopen(  # noqa: S310
            request, timeout=FETCH_TIMEOUT_SECONDS
        ) as response:
            text = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        if exc.code == HTTP_NOT_FOUND:
            _fail("Fetch failed", "404 not found", fetch_url)
        _fail("Fetch failed", f"HTTP {exc.code}", fetch_url)
    except (urllib.error.URLError, OSError, UnicodeDecodeError) as exc:
        _fail("Fetch failed", str(exc), fetch_url)
    return text
