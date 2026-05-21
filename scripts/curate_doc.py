"""Add or update documentation in collection directories.

Routes each source URL to either GitHub raw fetch (`github_source`) or
FireCrawl scrape, then resolves a non-colliding filename and updates
INDEX.xml. Filenames are stable across re-scrapes.
"""

import argparse
import re
import sys
import time
import xml.etree.ElementTree as ET
from datetime import date
from os import environ
from pathlib import Path
from typing import TYPE_CHECKING, Literal, TypedDict
from urllib.parse import urlparse

import github_source
from firecrawl import Firecrawl
from firecrawl.v2.utils.error_handler import FirecrawlError, RateLimitError

if TYPE_CHECKING:
    from firecrawl.types import Document


class ScrapedDoc(TypedDict):
    """Normalised result of a single scrape: markdown body plus metadata."""

    markdown: str
    metadata: dict[str, str]


def _normalise_directory_path(dir_path_str: str) -> Path:
    """Normalise directory path by removing trailing slash."""
    return Path(dir_path_str.rstrip("/"))


def _format_path_for_display(path: Path) -> str:
    """Format path as a project-relative string, e.g. `vite/INDEX.xml`.

    Falls back to `str(path)` for paths outside the project root.
    """
    try:
        absolute_path = path.resolve()
        project_root = Path.cwd()
        return str(absolute_path.relative_to(project_root))
    except ValueError:
        # Path is outside project (edge case) - return as-is
        return str(path)


def _validate_url(url: str) -> None:
    """Validate URL has scheme and netloc, exit if invalid."""
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        print(f"❌ Error: INVALID_URL|{url}|")
        sys.exit(1)


def _reject_uv_docs_url(url: str) -> None:
    """Reject hosted-docs uv URLs; the uv collection is sourced from GitHub raw."""
    if url.startswith("https://docs.astral.sh/uv/"):
        print(
            "❌ Error: USE_RAW_GITHUB|"
            "Use the GitHub RAW URL for this source; "
            "see uv/INDEX.xml for the canonical mapping|"
            f"{url}|"
        )
        sys.exit(1)


def _validate_directory_for_collection(dir_path: Path, index_path: Path) -> None:
    """Exit if directory exists, is non-empty, and lacks INDEX.xml.

    Prevents overwriting unrelated files in a non-collection directory.
    """
    if dir_path.exists() and not index_path.exists() and any(dir_path.iterdir()):
        print(
            f"❌ Error: INVALID_COLLECTION|"
            f"Directory non-empty and missing INDEX.xml. "
            f"Rejected to prevent inadvertent file overwrites|{dir_path}|"
        )
        sys.exit(1)


def filename_from_url(url: str) -> str:
    """Derive a `.md` filename from a (non-GitHub) doc URL path.

    Drops everything up to and including a `docs` path segment, strips a
    trailing `.md`, then lowercases and sanitises the remainder into a
    hyphen-joined slug. A bare docs root falls back to `index.md`.
    """
    segments = [s for s in urlparse(url).path.strip("/").split("/") if s]
    if segments and segments[-1].endswith(".md"):
        segments[-1] = segments[-1][:-3]
    if "docs" in segments:
        segments = segments[segments.index("docs") + 1 :]
    slug = re.sub(r"[^a-z0-9]+", "-", "-".join(segments).lower()).strip("-")
    return f"{slug or 'index'}.md"


def _create_readme(dir_path: Path, source_site_url: str) -> None:
    """Create README.md for new collection with overview and source link."""
    readme_content = f"""# {dir_path.name} Documentation

Curated docs for targeted AI context.

- Curation Index: [INDEX.xml](INDEX.xml)
- Curation Source: <{source_site_url}>
"""
    readme_path = dir_path / "README.md"
    readme_path.write_text(readme_content)
    print(f"✅ Created curation readme|{_format_path_for_display(readme_path)}|")


def _create_index_xml(dir_path: Path) -> None:
    """Create empty INDEX.xml structure."""
    root = ET.Element("docs_index")
    ET.indent(root, space="  ")

    tree = ET.ElementTree(root)
    index_path = dir_path / "INDEX.xml"
    tree.write(index_path, encoding="unicode", xml_declaration=False)
    print(f"✅ Created curation index|{_format_path_for_display(index_path)}|")


def _add_or_update_source_in_index(
    dir_path: Path, title: str, source_url: str, local_file: str
) -> bool:
    """Add or replace the source for `source_url` in INDEX.xml.

    Returns `is_update` — True if an existing entry was replaced.
    """
    index_path = dir_path / "INDEX.xml"

    tree = ET.parse(index_path)
    root = tree.getroot()

    is_update = False

    for existing_source in root.findall("source"):
        existing_url_elem = existing_source.find("source_url")
        if (
            existing_url_elem is not None
            and existing_url_elem.text is not None
            and existing_url_elem.text.rstrip("/") == source_url
        ):
            root.remove(existing_source)
            is_update = True
            break

    source = ET.SubElement(root, "source")
    ET.SubElement(source, "title").text = title
    ET.SubElement(source, "description").text = "PLACEHOLDER"
    ET.SubElement(source, "source_url").text = source_url
    ET.SubElement(source, "local_file").text = local_file
    ET.SubElement(source, "scraped_at").text = date.today().isoformat()

    ET.indent(root, space="  ")

    tree.write(index_path, encoding="unicode", xml_declaration=False)

    if is_update:
        print(f"✅ Updated index source|{_format_path_for_display(index_path)}|")
    else:
        print(f"✅ Added index source|{_format_path_for_display(index_path)}|")

    print("💡 INDEX.xml <description> pending: PLACEHOLDER requires summary|")

    return is_update


def resolve_filename(
    index_path: Path,
    source_url: str,
    candidate: str,
    *,
    on_collision: Literal["error", "suffix"],
) -> str:
    """Pick a non-colliding filename in INDEX.xml.

    Re-scrape (`source_url` already in INDEX) reuses the assigned filename.
    New source with a free candidate uses the candidate as-is. New source
    colliding with a different source either exits (`error`) or appends
    `-2`, `-3`, ... until free (`suffix`).

    `candidate` must include an extension (e.g. `foo.md`); the suffix
    branch splits on the final `.`.
    """
    if not index_path.exists():
        return candidate

    root = ET.parse(index_path).getroot()
    normalised = source_url.rstrip("/")
    taken: dict[str, str] = {}  # local_file -> source_url (for other sources)

    for source in root.findall("source"):
        url_elem = source.find("source_url")
        file_elem = source.find("local_file")
        if (
            url_elem is None
            or url_elem.text is None
            or file_elem is None
            or file_elem.text is None
        ):
            continue
        stored_url = url_elem.text.rstrip("/")
        if stored_url == normalised:
            return file_elem.text
        taken[file_elem.text] = stored_url

    if candidate not in taken:
        return candidate

    if on_collision == "error":
        print(
            f"❌ Error: FILENAME_COLLISION|"
            f"{candidate} already mapped to {taken[candidate]}|{source_url}|"
        )
        sys.exit(1)

    stem, ext = candidate.rsplit(".", 1)
    n = 2
    while f"{stem}-{n}.{ext}" in taken:
        n += 1
    return f"{stem}-{n}.{ext}"


def _get_firecrawl_client() -> Firecrawl:
    """Get Firecrawl client with API key from environment."""
    api_key = environ.get("API_KEY_MCP_FIRECRAWL")
    if not api_key:
        print("❌ Error: MISSING_API_KEY|API_KEY_MCP_FIRECRAWL not set|")
        sys.exit(1)
    return Firecrawl(api_key=api_key)


def _parse_retry_seconds(error: RateLimitError) -> int:
    """Parse retry-after seconds from rate limit error message."""
    error_msg = str(error)
    retry_match = re.search(r"retry after (\d+)s", error_msg, re.IGNORECASE)
    if retry_match:
        return int(retry_match.group(1))
    # Default to 60s if pattern not found (rate limit window is per minute)
    return 60


def _extract_metadata(result: Document) -> dict[str, str]:
    """Extract title from Firecrawl document metadata."""
    metadata = {}
    if hasattr(result, "metadata") and result.metadata:
        metadata = {
            "title": getattr(result.metadata, "title", "Untitled"),
        }
    return metadata


def _perform_scrape(firecrawl: Firecrawl, url: str) -> ScrapedDoc:
    """Make one Firecrawl scrape call and return `{markdown, metadata}`.

    Exits with `NO_CONTENT` if the response has no markdown. Rate-limit,
    API, network, and unexpected errors propagate to `_scrape_with_firecrawl`.
    """
    result = firecrawl.scrape(
        url,
        formats=["markdown"],
        only_main_content=True,  # Excl. nav menu, footer, sidebars, etc.
        remove_base64_images=True,  # Removes base64 strings (keeps alt text)
        wait_for=3000,  # Wait to capture dynamic content (3 seconds)
        max_age=86400000,  # Use cached content for speed (24 hours)
    )

    if not result or not hasattr(result, "markdown") or not result.markdown:
        print(f"❌ Error: NO_CONTENT|No scrape content returned|{url}|")
        sys.exit(1)

    return {
        "markdown": result.markdown,
        "metadata": _extract_metadata(result),
    }


def _scrape_with_firecrawl(url: str, max_attempts: int = 2) -> ScrapedDoc:
    """Scrape URL using Firecrawl Python SDK with automatic retry on rate limits.

    Retries on `RateLimitError` for the retry-after duration plus a 2-second
    safety buffer. `max_attempts` is initial + retries (default `2` = 1
    initial + 1 retry). Exits via `sys.exit(1)` on rate-limit exhaustion or
    any other API, network, or unexpected error.
    """
    firecrawl = _get_firecrawl_client()

    for attempt in range(max_attempts):
        try:
            return _perform_scrape(firecrawl, url)

        except RateLimitError as e:
            if attempt < max_attempts - 1:
                retry_seconds = _parse_retry_seconds(e)
                wait_time = retry_seconds + 2  # Add 2s safety buffer
                print(f"⏳ Rate limited|Waiting {wait_time}s before retry...|")
                time.sleep(wait_time)
                continue

            # Final attempt exhausted
            print(
                f"❌ Error: FIRECRAWL_RATELIMIT|"
                f"Firecrawl rate limited all {max_attempts} attempts, "
                f"no content scraped|{url}|"
            )
            sys.exit(1)

        except FirecrawlError as e:
            # All other Firecrawl API errors
            print(f"❌ Error: FIRECRAWL|{e}|{url}|")
            sys.exit(1)

        except OSError as e:
            # Network/connection failures (timeouts, DNS errors, etc.)
            print(f"❌ Error: NETWORK|{e}|{url}|")
            sys.exit(1)

        except Exception as e:  # noqa: BLE001
            # Unexpected errors (ValueError, RuntimeError, SDK bugs, etc.)
            print(f"❌ Error: UNEXPECTED|{type(e).__name__}: {e}|{url}|")
            sys.exit(1)

    # Defensive fallback (unreachable in normal execution)
    print(f"❌ Error: NETWORK|Failed after {max_attempts} attempts|{url}|")
    sys.exit(1)


def main() -> None:
    """Add or update documentation in a collection directory.

    Workflow:
        1. Validate URL and directory
        2. Detect source: GitHub raw fetch or FireCrawl scrape
        3. Create collection structure if new (README.md, INDEX.xml)
        4. Resolve filename (re-scrape preserves assigned name; new sources
           use candidate, with GitHub erroring on collision and FireCrawl
           suffixing)
        5. Write markdown file and update INDEX.xml

    Filenames are stable across re-scrapes even when the upstream title
    changes — the URL, not the title, is the identity key in INDEX.
    """
    parser = argparse.ArgumentParser(
        description="Add or update documentation in a collection directory"
    )

    parser.add_argument(
        "directory",
        help="Documentation directory (e.g. `tailwind/`)",
    )
    parser.add_argument(
        "source_url",
        help="Web URL to curate (Firecrawl scrape or GitHub raw fetch)",
    )

    args = parser.parse_args()

    source_url = args.source_url.rstrip("/")  # canonical form: no trailing slash
    dir_path = _normalise_directory_path(args.directory)
    index_path = dir_path / "INDEX.xml"

    _validate_url(source_url)
    _reject_uv_docs_url(source_url)
    _validate_directory_for_collection(dir_path, index_path)

    print(f"✅ Starting to curate from|{source_url}|")

    dir_path.mkdir(parents=True, exist_ok=True)

    # Route GitHub vs FireCrawl before creating files (fail fast).
    is_github = github_source.is_github_url(source_url)

    if is_github:
        source_url = github_source.to_raw_url(source_url)
        print(f"✅ Detected GitHub source|{source_url}|")
        candidate = github_source.derive_filename(source_url)  # exits if invalid
        content = github_source.fetch_raw(source_url)  # exits on 404/network
        title = github_source.extract_title(content, source_url)
    else:
        scraped_doc = _scrape_with_firecrawl(source_url, max_attempts=2)
        content = scraped_doc["markdown"]
        print(f"✅ Scraped content|({len(content):,} characters)|")
        title = scraped_doc["metadata"].get("title", "Untitled")
        candidate = filename_from_url(source_url)

    # scheme + netloc for the README's curation-source link
    parsed_url = urlparse(source_url)
    source_site_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    if not index_path.exists():
        _create_readme(dir_path, source_site_url)
        _create_index_xml(dir_path)

    filename = resolve_filename(
        index_path,
        source_url,
        candidate,
        on_collision="error" if is_github else "suffix",
    )

    file_path = dir_path / filename

    file_existed = file_path.exists()
    file_path.write_text(content)
    if file_existed:
        print(f"✅ Overwrote existing document|{_format_path_for_display(file_path)}|")
    else:
        print(f"✅ Created new document|{_format_path_for_display(file_path)}|")

    is_update = _add_or_update_source_in_index(dir_path, title, source_url, filename)

    # source_url is canonical (raw form for GitHub, rstripped user URL for FireCrawl)
    verb = "overwrote and re-indexed" if is_update else "created and indexed new"
    print(f"🎉 Curation Success!|{verb} document|{source_url}|\n")


if __name__ == "__main__":
    main()
