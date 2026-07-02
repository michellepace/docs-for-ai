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
        print(f"❌ Invalid URL: {url}")
        sys.exit(1)


def _reject_uv_docs_url(url: str) -> None:
    """Reject hosted-docs uv URLs; the uv collection is sourced from GitHub."""
    if url.startswith("https://docs.astral.sh/uv/"):
        print(
            "❌ Unsupported uv URL: use the GitHub blob "
            f"(see collections/uv/INDEX.xml) — {url}"
        )
        sys.exit(1)


def _validate_collection_dir(collection_dir: Path, index_path: Path) -> None:
    if (
        collection_dir.exists()
        and not index_path.exists()
        and any(collection_dir.iterdir())
    ):
        print(
            f"❌ Unsafe collection dir: non-empty and missing INDEX.xml "
            f"— {collection_dir}"
        )
        sys.exit(1)


def _initialise_collection(collection_dir: Path, source_url: str) -> None:
    """Scaffold a new collection."""
    site = urlparse(source_url)
    readme = f"""# {collection_dir.name} Documentation

Curated docs for targeted AI context.

- Curation Index: [INDEX.xml](INDEX.xml)
- Curation Source: <{site.scheme}://{site.netloc}>
"""
    (collection_dir / "README.md").write_text(readme)
    write_index(ET.Element("docs_index"), collection_dir / "INDEX.xml")
    print(f"✅ Collection: {collection_dir.name} (initialised)")


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

    curated_at = date.today().isoformat()

    source = ET.SubElement(root, "source")
    ET.SubElement(source, "title").text = title
    ET.SubElement(source, "description").text = PLACEHOLDER_DESCRIPTION
    ET.SubElement(source, "source_url").text = source_url
    ET.SubElement(source, "local_file").text = local_file
    ET.SubElement(source, "curated_at").text = curated_at

    write_index(root, index_path)

    label = "Reindexed" if is_update else "Indexed"
    print(f"✅ {label}: {format_path_for_display(index_path)}")
    print("   <source>")
    print(f"     <title>{title}</title>")
    print(f"     <description>{PLACEHOLDER_DESCRIPTION}</description>")
    print(f"     <source_url>{source_url}</source_url>")
    print(f"     <local_file>{local_file}</local_file>")
    print(f"     <curated_at>{curated_at}</curated_at>")
    print("   </source>")

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
                f"❌ Filename collision: {filename} already curated from "
                f"{existing_url} — {source_url}"
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
        print(f"✅ Overwrote: {format_path_for_display(file_path)}")
    else:
        print(f"✅ Created: {format_path_for_display(file_path)}")


def _parse_args() -> argparse.Namespace:
    """Parse CLI arguments: target collection directory and source URL."""
    parser = argparse.ArgumentParser(
        description="Curate a source document into a collection directory"
    )
    parser.add_argument(
        "collection_dir",
        help="Target collection directory (created if it doesn't exist)",
    )
    parser.add_argument(
        "source_url",
        help="Web URL of the document to curate",
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

    print("Curating…")

    collection_dir.mkdir(parents=True, exist_ok=True)
    index_exists = index_path.exists()

    route = direct_fetch.resolve_route(source_url, direct_fetch.load_direct_fetch_rules())

    # Reject a colliding filename before the (paid) fetch.
    if index_exists:
        _reject_filename_collision(collection_dir, route.filename, route.canonical_url)

    doc = fetch_document(route)

    if not index_exists:
        _initialise_collection(collection_dir, source_url)

    _write_fetched_document(collection_dir, doc)

    # doc.source_url is canonical: query/fragment-free, no trailing `.md`
    _add_or_update_source_in_index(
        collection_dir, doc.title, doc.source_url, doc.filename
    )

    print("🏁 Success! curated doc (🚩 description pending)\n")


if __name__ == "__main__":
    main()
