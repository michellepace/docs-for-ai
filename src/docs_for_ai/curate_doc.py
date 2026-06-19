"""Curate one source URL into a collection directory.

Saves the curated doc as a file and registers it in INDEX.xml. URLs ending in
`.md` and GitHub blobs (`.md`/`.mdx`/`.qmd`, extension preserved) are fetched
directly. All other URLs are scraped via FireCrawl.
"""

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path
from typing import NamedTuple
from urllib.parse import urlparse

from docs_for_ai import firecrawl_source, markdown_source
from docs_for_ai.index_io import write_index
from docs_for_ai.paths import format_path_for_display

# Written for every new source; a later LLM step fills it.
PLACEHOLDER_DESCRIPTION = "PLACEHOLDER"


def _normalise_directory_path(dir_path_str: str) -> Path:
    """Normalise directory path by removing trailing slash."""
    return Path(dir_path_str.rstrip("/"))


def _validate_url(url: str) -> None:
    """Validate URL has scheme and netloc, exit if invalid."""
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        print(f"❌ Error: INVALID_URL|{url}|")
        sys.exit(1)


def _reject_uv_docs_url(url: str) -> None:
    """Reject hosted-docs uv URLs; the uv collection is sourced from GitHub."""
    if url.startswith("https://docs.astral.sh/uv/"):
        print(
            "❌ Error: USE_GITHUB_BLOB|"
            "Use the GitHub blob URL for this source; "
            "see collections/uv/INDEX.xml for the canonical mapping|"
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


def filename_from_canonical_url(url: str) -> str:
    """Derive a `.md` filename from a non-GitHub doc URL path.

    Expects the canonical URL from `resolve_md_route` (no query/fragment or
    trailing `.md`); a `docs` segment and any prefix are dropped to avoid a
    redundant `docs-` slug.
    """
    segments = [s for s in urlparse(url).path.strip("/").split("/") if s]
    if "docs" in segments:
        segments = segments[segments.index("docs") + 1 :]
    slug = re.sub(r"[^a-z0-9]+", "-", "-".join(segments).lower()).strip("-")
    return f"{slug or 'index'}.md"


def _create_readme(dir_path: Path, source_url: str) -> None:
    """Create README.md for a new collection with overview and source link."""
    parsed_url = urlparse(source_url)
    source_site_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    readme_content = f"""# {dir_path.name} Documentation

Curated docs for targeted AI context.

- Curation Index: [INDEX.xml](INDEX.xml)
- Curation Source: <{source_site_url}>
"""
    readme_path = dir_path / "README.md"
    readme_path.write_text(readme_content)
    print(f"✅ Created curation readme|{format_path_for_display(readme_path)}|")


def _create_empty_index(dir_path: Path) -> None:
    """Create empty INDEX.xml structure."""
    root = ET.Element("docs_index")

    index_path = dir_path / "INDEX.xml"
    write_index(root, index_path)
    print(f"✅ Created curation index|{format_path_for_display(index_path)}|")


def _add_or_update_source_in_index(
    dir_path: Path, title: str, source_url: str, local_file: str
) -> bool:
    """Add or replace the source for `source_url` in INDEX.xml.

    Returns `is_update` — True if an existing entry was replaced.
    """
    index_path = dir_path / "INDEX.xml"

    root = ET.parse(index_path).getroot()

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
    ET.SubElement(source, "description").text = PLACEHOLDER_DESCRIPTION
    ET.SubElement(source, "source_url").text = source_url
    ET.SubElement(source, "local_file").text = local_file
    ET.SubElement(source, "scraped_at").text = date.today().isoformat()

    write_index(root, index_path)

    verb = "Updated" if is_update else "Added"
    fields = (
        f"title={title}|local_file={local_file}|description={PLACEHOLDER_DESCRIPTION}|"
    )
    print(f"✅ {verb} index source|{format_path_for_display(index_path)}|{fields}")
    print("💡 Source description pending|")

    return is_update


class FetchedDoc(NamedTuple):
    """A fetched source document: body, title, filename, and canonical URL."""

    content: str
    title: str
    filename: str
    source_url: str


def fetch_document(source_url: str) -> FetchedDoc:
    """Fetch a source document, returning a `FetchedDoc`.

    GitHub is checked before the generic `.md` branch because a blob URL also
    ends in `.md`, yet must be fetched from `raw` and keep its blob URL.
    """
    if markdown_source.is_github_url(source_url):
        raw_url = markdown_source.github_blob_to_raw_url(source_url)
        print(f"✅ Detected GitHub source|{source_url}|")
        filename = markdown_source.github_filename_from_blob_url(source_url)
        content = markdown_source.fetch_markdown(raw_url)
        title = markdown_source.extract_title(content, raw_url)
        return FetchedDoc(content, title, filename, source_url)

    prefixes = markdown_source.load_md_allowlist()
    route = markdown_source.resolve_md_route(source_url, prefixes)
    filename = filename_from_canonical_url(route.canonical_url)
    # fetch_url is set unless we route to FireCrawl; the None check also narrows it.
    if route.use_firecrawl or route.fetch_url is None:
        content, title = firecrawl_source.scrape(route.canonical_url)
    else:
        content = markdown_source.fetch_markdown(route.fetch_url)
        title = markdown_source.extract_title(content, route.fetch_url)
    return FetchedDoc(content, title, filename, route.canonical_url)


def _write_document(dir_path: Path, doc: FetchedDoc) -> None:
    """Write the fetched markdown to its file."""
    file_path = dir_path / doc.filename
    file_existed = file_path.exists()
    file_path.write_text(doc.content)
    if file_existed:
        print(f"✅ Overwrote existing document|{format_path_for_display(file_path)}|")
    else:
        print(f"✅ Created new document|{format_path_for_display(file_path)}|")


def _parse_args() -> argparse.Namespace:
    """Parse CLI arguments: target directory and source URL."""
    parser = argparse.ArgumentParser(
        description="Add or update documentation in a collection directory"
    )
    parser.add_argument(
        "directory",
        help="Documentation directory (e.g. `collections/tailwind/`)",
    )
    parser.add_argument(
        "source_url",
        help=(
            "Web URL to curate (direct `.md` fetch, GitHub `.md`/`.mdx`/`.qmd` "
            "blob, or FireCrawl scrape)"
        ),
    )
    return parser.parse_args()


def main() -> None:
    """Curate a single source URL into a collection directory."""
    args = _parse_args()

    source_url: str = args.source_url.rstrip("/")
    dir_path = _normalise_directory_path(args.directory)
    index_path = dir_path / "INDEX.xml"

    _validate_url(source_url)
    _reject_uv_docs_url(source_url)
    _validate_directory_for_collection(dir_path, index_path)

    print(f"✅ Starting to curate from|{source_url}|")

    dir_path.mkdir(parents=True, exist_ok=True)

    # Fetch first: failures leave no partial collection.
    doc = fetch_document(source_url)

    if not index_path.exists():
        _create_readme(dir_path, source_url)
        _create_empty_index(dir_path)

    _write_document(dir_path, doc)

    # doc.source_url is canonical: query/fragment-free, no trailing `.md`
    # (blob form for GitHub). The raw input is kept only for the steps above.
    is_update = _add_or_update_source_in_index(
        dir_path, doc.title, doc.source_url, doc.filename
    )

    verb = "overwrote and re-indexed" if is_update else "created and indexed new"
    print(f"🎉 Curation Success!|{verb} document|{doc.source_url}|\n")


if __name__ == "__main__":
    main()
