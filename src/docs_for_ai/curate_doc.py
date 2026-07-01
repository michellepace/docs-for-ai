"""Curate one source URL into a collection directory.

Saves the curated doc as a file and registers it in INDEX.xml. GitHub blobs and
URLs under a direct-fetch registry prefix are fetched directly, as are raw
`.md`/`.rst.txt` URLs; all other URLs are scraped via FireCrawl.
"""

import argparse
import sys
import xml.etree.ElementTree as ET
from datetime import date
from typing import TYPE_CHECKING, NamedTuple
from urllib.parse import urlparse

from docs_for_ai import direct_fetch, firecrawl_scrape
from docs_for_ai.index_io import PLACEHOLDER_DESCRIPTION, write_index
from docs_for_ai.paths import format_path_for_display, normalise_collection_dir

if TYPE_CHECKING:
    from pathlib import Path


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


def _validate_collection_dir(collection_dir: Path, index_path: Path) -> None:
    if (
        collection_dir.exists()
        and not index_path.exists()
        and any(collection_dir.iterdir())
    ):
        print(
            f"❌ Error: INVALID_COLLECTION|"
            f"Directory non-empty and missing INDEX.xml. "
            f"Rejected to prevent inadvertent file overwrites|{collection_dir}|"
        )
        sys.exit(1)


def _create_readme(collection_dir: Path, source_url: str) -> None:
    """Create README.md for a new collection with overview and source link."""
    parsed_url = urlparse(source_url)
    source_site_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    readme_content = f"""# {collection_dir.name} Documentation

Curated docs for targeted AI context.

- Curation Index: [INDEX.xml](INDEX.xml)
- Curation Source: <{source_site_url}>
"""
    readme_path = collection_dir / "README.md"
    readme_path.write_text(readme_content)
    print(f"✅ Created curation readme|{format_path_for_display(readme_path)}|")


def _create_empty_index(collection_dir: Path) -> None:
    """Create empty INDEX.xml structure."""
    root = ET.Element("docs_index")

    index_path = collection_dir / "INDEX.xml"
    write_index(root, index_path)
    print(f"✅ Created curation index|{format_path_for_display(index_path)}|")


def _add_or_update_source_in_index(
    collection_dir: Path, title: str, source_url: str, local_file: str
) -> bool:
    """Add or replace the source for `source_url` in INDEX.xml.

    Returns `is_update` — True if an existing entry was replaced.
    """
    index_path = collection_dir / "INDEX.xml"

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
    ET.SubElement(source, "curated_at").text = date.today().isoformat()

    write_index(root, index_path)

    verb = "Updated" if is_update else "Added"
    fields = (
        f"title={title}|local_file={local_file}|description={PLACEHOLDER_DESCRIPTION}|"
    )
    print(f"✅ {verb} index source|{format_path_for_display(index_path)}|{fields}")
    print("💡 Source description pending|")

    return is_update


def _reject_filename_collision(
    collection_dir: Path, filename: str, source_url: str
) -> None:
    """Exit if `filename` already belongs to a DIFFERENT source_url in INDEX.xml."""
    root = ET.parse(collection_dir / "INDEX.xml").getroot()
    for source in root.findall("source"):
        existing_file = source.findtext("local_file")
        existing_url = (source.findtext("source_url") or "").rstrip("/")
        if existing_file == filename and existing_url != source_url:
            print(
                f"❌ Error: FILENAME_COLLISION|"
                f"{filename} already curated from {existing_url}|{source_url}|"
            )
            sys.exit(1)


class FetchedDoc(NamedTuple):
    """A fetched source document: body, title, filename, and canonical URL."""

    content: str
    title: str
    filename: str
    source_url: str


def fetch_document(route: direct_fetch.FetchRoute) -> FetchedDoc:
    """Fetch a resolved route's document; `doc_format` None ⇒ FireCrawl scrape."""
    if route.doc_format is None:
        content, title = firecrawl_scrape.scrape(route.canonical_url)
    else:
        content = direct_fetch.fetch_text(route.fetch_url)
        title = direct_fetch.extract_title(content, route.doc_format, route.canonical_url)
    return FetchedDoc(content, title, route.filename, route.canonical_url)


def _write_fetched_document(collection_dir: Path, doc: FetchedDoc) -> None:
    """Write the fetched document to its file."""
    file_path = collection_dir / doc.filename
    file_existed = file_path.exists()
    file_path.write_text(doc.content)
    if file_existed:
        print(f"✅ Overwrote doc|{format_path_for_display(file_path)}|")
    else:
        print(f"✅ Created doc|{format_path_for_display(file_path)}|")


def _parse_args() -> argparse.Namespace:
    """Parse CLI arguments: target collection directory and source URL."""
    parser = argparse.ArgumentParser(
        description="Add or update documentation in a collection directory"
    )
    parser.add_argument(
        "collection_dir",
        help="Collection directory (e.g. collections/tailwind/)",
    )
    parser.add_argument(
        "source_url",
        help=(
            "Web URL to curate (direct fetch for `.md`/GitHub blobs and "
            "registered sites, else FireCrawl scrape)"
        ),
    )
    return parser.parse_args()


def main() -> None:
    """Curate a single source URL into a collection directory."""
    args = _parse_args()

    source_url: str = args.source_url.rstrip("/")
    collection_dir = normalise_collection_dir(args.collection_dir)
    index_path = collection_dir / "INDEX.xml"

    _validate_url(source_url)
    _reject_uv_docs_url(source_url)
    _validate_collection_dir(collection_dir, index_path)

    print(f"✅ Curating from|{source_url}|")

    collection_dir.mkdir(parents=True, exist_ok=True)
    index_exists = index_path.exists()

    route = direct_fetch.resolve_route(source_url, direct_fetch.load_direct_fetch_rules())

    # Reject a colliding filename before the (paid) fetch.
    if index_exists:
        _reject_filename_collision(collection_dir, route.filename, route.canonical_url)

    doc = fetch_document(route)

    if not index_exists:
        _create_readme(collection_dir, source_url)
        _create_empty_index(collection_dir)

    _write_fetched_document(collection_dir, doc)

    # doc.source_url is canonical: query/fragment-free, no trailing `.md`
    # (blob form for GitHub). The raw input is kept only for the steps above.
    is_update = _add_or_update_source_in_index(
        collection_dir, doc.title, doc.source_url, doc.filename
    )

    verb = "overwrote and re-indexed" if is_update else "created and indexed new"
    print(f"🎉 Curation Success!|{verb} document|{doc.source_url}|\n")


if __name__ == "__main__":
    main()
