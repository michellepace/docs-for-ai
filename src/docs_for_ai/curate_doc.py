"""Curate one source URL into a collection. See `curate-doc --help` for behaviour."""

import argparse
import sys
import xml.etree.ElementTree as ET
from datetime import date
from enum import StrEnum
from typing import TYPE_CHECKING, Literal, NamedTuple
from urllib.parse import urlparse

from docs_for_ai import direct_fetch, firecrawl_scrape
from docs_for_ai.errors import CurationError
from docs_for_ai.index_io import PLACEHOLDER_DESCRIPTION, write_index
from docs_for_ai.paths import (
    collection_label,
    format_path_for_display,
    normalise_collection_dir,
)

if TYPE_CHECKING:
    from pathlib import Path


class DocOutcome(StrEnum):
    """Fate of a source's description, decided at write time."""

    NEW = "new"  # no INDEX entry for this canonical URL
    UNCHANGED = "unchanged"  # fetched bytes identical to the entry's doc file
    WHITESPACE_ONLY = "whitespace-only"  # differs only in whitespace
    CHANGED = "changed"  # real content change — description resets
    RECREATED = "recreated"  # entry exists but its doc file is missing


class CurationResult(NamedTuple):
    """One curation's outcome and everything the CLI report prints."""

    outcome: DocOutcome
    local_file: str
    doc_action: Literal["created", "overwrote"]
    index_action: Literal["indexed", "reindexed"]
    canonical_url: str
    chars: int
    route: Literal["direct", "firecrawl"]
    title: str
    description: str
    initialised: bool


class _ExistingEntry(NamedTuple):
    """The INDEX.xml entry already recording a canonical URL, pre-curation."""

    local_file: str
    description: str


def _validate_url(url: str) -> None:
    """Validate URL has scheme and netloc."""
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        msg = f"Invalid URL: {url}"
        raise CurationError(msg)


def _reject_uv_docs_url(url: str) -> None:
    """Reject hosted-docs uv URLs; the uv collection is sourced from GitHub."""
    if url.startswith("https://docs.astral.sh/uv/"):
        msg = (
            "Unsupported uv URL: use the GitHub blob "
            f"(see collections/uv/INDEX.xml) — {url}"
        )
        raise CurationError(msg)


def _validate_collection_dir(collection_dir: Path, index_path: Path) -> None:
    if (
        collection_dir.exists()
        and not index_path.exists()
        and any(collection_dir.iterdir())
    ):
        msg = (
            f"Unsafe collection dir: non-empty and missing INDEX.xml — {collection_dir}"
        )
        raise CurationError(msg)


def _initialise_collection(collection_dir: Path, source_url: str) -> None:
    """Scaffold a new collection."""
    site = urlparse(source_url)
    readme = f"""# {collection_dir.name} Documentation

Curated docs for targeted AI context.

- Curation Index: [INDEX.xml](INDEX.xml)
- Curation Source: {site.scheme}://{site.netloc}

**What is {collection_dir.name}?** [40-70 words: what it is / does, said simply]
"""
    (collection_dir / "README.md").write_text(readme, encoding="utf-8")
    write_index(ET.Element("docs_index"), collection_dir / "INDEX.xml")


def _urls_match(entry_url: str | None, canonical_url: str) -> bool:
    """The one URL-matching rule: trailing-slash-insensitive equality."""
    return entry_url is not None and entry_url.rstrip("/") == canonical_url


def _find_existing_entry(index_path: Path, canonical_url: str) -> _ExistingEntry | None:
    """The INDEX entry recording `canonical_url`, or None if not yet curated."""
    root = ET.parse(index_path).getroot()
    for source in root.findall("source"):
        if _urls_match(source.findtext("source_url"), canonical_url):
            return _ExistingEntry(
                source.findtext("local_file", ""), source.findtext("description", "")
            )
    return None


def _classify_outcome(
    collection_dir: Path, existing: _ExistingEntry | None, fetched_content: str
) -> DocOutcome:
    """Compare fetched content against the entry's recorded doc file."""
    if existing is None:
        return DocOutcome.NEW
    comparison_file = collection_dir / existing.local_file
    if not comparison_file.is_file():
        return DocOutcome.RECREATED
    current = comparison_file.read_text(encoding="utf-8")
    if current == fetched_content:
        return DocOutcome.UNCHANGED
    if current.split() == fetched_content.split():
        return DocOutcome.WHITESPACE_ONLY
    return DocOutcome.CHANGED


def _decide_description(outcome: DocOutcome, existing: _ExistingEntry | None) -> str:
    """Keep the existing description only when the fetch matches the recorded file."""
    keep = {DocOutcome.UNCHANGED, DocOutcome.WHITESPACE_ONLY}
    if outcome in keep and existing is not None and existing.description:
        return existing.description
    return PLACEHOLDER_DESCRIPTION


def _description_note(outcome: DocOutcome, description: str) -> str:
    """The report's `description:` value — the fate Claude keys Step 3 off."""
    if description == PLACEHOLDER_DESCRIPTION:
        return "PLACEHOLDER (pending)"
    if outcome is DocOutcome.WHITESPACE_ONLY:
        return "kept — whitespace-only change"
    return "kept — content unchanged"


def _add_or_update_source_in_index(
    collection_dir: Path, title: str, source_url: str, local_file: str, description: str
) -> Literal["indexed", "reindexed"]:
    """Rewrite an existing entry in place, append a new one."""
    index_path = collection_dir / "INDEX.xml"

    root = ET.parse(index_path).getroot()
    curated_at = date.today().isoformat()

    fields = {
        "title": title,
        "description": description,
        "source_url": source_url,
        "local_file": local_file,
        "curated_at": curated_at,
    }

    source = next(
        (
            s
            for s in root.findall("source")
            if _urls_match(s.findtext("source_url"), source_url)
        ),
        None,
    )
    is_update = source is not None
    if source is None:
        source = ET.SubElement(root, "source")

    for tag, value in fields.items():
        child = source.find(tag)
        if child is None:
            child = ET.SubElement(source, tag)
        child.text = value

    write_index(root, index_path)

    return "reindexed" if is_update else "indexed"


def _reject_filename_collision(
    collection_dir: Path, filename: str, source_url: str
) -> None:
    """Reject `filename` already belonging to a DIFFERENT source_url in INDEX.xml."""
    root = ET.parse(collection_dir / "INDEX.xml").getroot()
    for source in root.findall("source"):
        existing_file = source.findtext("local_file")
        existing_url = (source.findtext("source_url") or "").rstrip("/")
        if existing_file == filename and existing_url != source_url:
            msg = (
                f"Filename collision: {filename} already curated from "
                f"{existing_url} — {source_url}"
            )
            raise CurationError(msg)


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
        title = direct_fetch.extract_title(
            content, route.doc_format, route.canonical_url
        )
    return FetchedDoc(content, title, route.filename, route.canonical_url)


def _write_fetched_document(
    collection_dir: Path, doc: FetchedDoc
) -> Literal["created", "overwrote"]:
    """Write the fetched document to its file; report created vs overwrote."""
    file_path = collection_dir / doc.filename
    action: Literal["created", "overwrote"] = (
        "overwrote" if file_path.exists() else "created"
    )
    file_path.write_text(doc.content, encoding="utf-8")
    return action


def _parse_args() -> argparse.Namespace:
    """Parse CLI arguments: target collection directory and source URL."""
    parser = argparse.ArgumentParser(
        description=(
            "Fetch a doc from a URL, save it into a collection, "
            "and register it in INDEX.xml."
        ),
        epilog="""\
notes:
  - Fetch precedence: GitHub raw → .md/.rst.txt twin → FireCrawl (last resort).
  - Re-curating a URL overwrites its doc and replaces its INDEX entry.
  - A new, content-changed, or recreated doc gets a PLACEHOLDER description to
    fill in later; if the re-fetched content is unchanged (ignoring whitespace),
    the existing description is kept.
  - The collection is initialised if the directory doesn't exist.
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
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


def curate(collection_dir: Path, source_url: str) -> CurationResult:
    """Curate one source URL into a collection.

    A description survives only when the fetched document matches the doc file its
    INDEX entry records (compared before the overwrite, ignoring whitespace); new,
    changed, or recreated docs reset it to PLACEHOLDER.
    """
    source_url = source_url.rstrip("/")
    index_path = collection_dir / "INDEX.xml"

    _validate_url(source_url)
    _reject_uv_docs_url(source_url)
    _validate_collection_dir(collection_dir, index_path)

    index_exists = index_path.exists()

    fetch_route = direct_fetch.resolve_route(
        source_url, direct_fetch.load_direct_fetch_rules()
    )

    # Reject a colliding filename before the (paid) fetch.
    if index_exists:
        _reject_filename_collision(
            collection_dir, fetch_route.filename, fetch_route.canonical_url
        )

    existing = (
        _find_existing_entry(index_path, fetch_route.canonical_url)
        if index_exists
        else None
    )

    doc = fetch_document(fetch_route)

    # Only now touch the filesystem: a failed fetch must leave no trace behind.
    collection_dir.mkdir(parents=True, exist_ok=True)
    if not index_exists:
        _initialise_collection(collection_dir, source_url)

    outcome = _classify_outcome(collection_dir, existing, doc.content)

    doc_action = _write_fetched_document(collection_dir, doc)

    description = _decide_description(outcome, existing)

    # doc.source_url is canonical: query/fragment-free, no trailing `.md`
    index_action = _add_or_update_source_in_index(
        collection_dir, doc.title, doc.source_url, doc.filename, description
    )

    return CurationResult(
        outcome=outcome,
        local_file=doc.filename,
        doc_action=doc_action,
        index_action=index_action,
        canonical_url=doc.source_url,
        chars=len(doc.content),
        route="firecrawl" if fetch_route.doc_format is None else "direct",
        title=doc.title,
        description=description,
        initialised=not index_exists,
    )


def _format_curate_report(collection_dir: Path, result: CurationResult) -> str:
    """Build the CURATE report; the 🏁 gate line is printed separately."""
    doc_path = format_path_for_display(collection_dir / result.local_file)
    index_path = format_path_for_display(collection_dir / "INDEX.xml")
    lines = [f"CURATE {collection_label(collection_dir)}"]
    if result.initialised:
        lines.append("  collection: initialised")
    lines.extend(
        [
            f"  doc:    {doc_path} ({result.doc_action})",
            f"  index:  {index_path} ({result.index_action})",
            f"  url:    {result.canonical_url}",
            f"  fetch:  {result.chars:,} chars, {result.route}",
            f"  title:  {result.title}",
            f"  description: {_description_note(result.outcome, result.description)}",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    """Curate a single source URL into a collection directory."""
    args = _parse_args()
    collection_dir = normalise_collection_dir(args.collection_dir)
    try:
        result = curate(collection_dir, args.source_url)
    except CurationError as exc:
        print(f"❌ {exc}")
        sys.exit(1)
    print(_format_curate_report(collection_dir, result))
    print()
    print("🏁 Success! curated doc")


if __name__ == "__main__":
    main()
