"""Sync INDEX.xml and re-curate all docs. See `sync-index --help` for behaviour."""

import argparse
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from typing import TYPE_CHECKING, NamedTuple

from docs_for_ai import curate_doc
from docs_for_ai.errors import CurationError
from docs_for_ai.index_io import PLACEHOLDER_DESCRIPTION
from docs_for_ai.paths import format_path_for_display, normalise_collection_dir

if TYPE_CHECKING:
    from pathlib import Path


class IndexSource(NamedTuple):
    """One INDEX.xml <source> — written programmatically, so all fields are set."""

    local_file: str
    source_url: str


# Collection files that must survive a sync.
_PROTECTED_FILES = {"INDEX.xml", "README.md"}


def read_index_sources(index_path: Path) -> list[IndexSource]:
    """Read every <source> in INDEX.xml, rejecting invalid XML.

    Never removes a source: the index is the truth.
    """
    try:
        index_root = ET.parse(index_path).getroot()
    except ET.ParseError as e:
        msg = f"Invalid XML: {e} — {index_path}"
        raise CurationError(msg) from e
    return [
        IndexSource(
            source.findtext("local_file", ""),
            source.findtext("source_url", ""),
        )
        for source in index_root.findall("source")
    ]


def delete_orphan_files(collection_dir: Path, indexed_files: set[str]) -> list[str]:
    """Delete on-disk docs with no matching INDEX.xml <local_file>."""
    keep = indexed_files | _PROTECTED_FILES
    deleted: list[str] = []
    for path in sorted(collection_dir.iterdir()):
        if not path.is_file() or path.name in keep or path.name.startswith("."):
            continue
        path.unlink()
        deleted.append(path.name)
    return deleted


def _curate_doc(
    collection_dir: Path, source_url: str
) -> curate_doc.CurationResult | None:
    """Curate one source in-process; print its failure line and return None."""
    try:
        return curate_doc.curate(collection_dir, source_url)
    except CurationError as exc:
        print(f"❌ {exc}")
        return None
    except Exception as exc:  # noqa: BLE001 — one doc's crash must not abort the sync
        print(f"❌ Unexpected error: {type(exc).__name__}: {exc} — {source_url}")
        return None


def _print_curation_summary(
    curated_sources: list[IndexSource],
    failed_urls: list[str],
) -> None:
    print("\n### Curation Summary")
    print(f"- Successful|{len(curated_sources) - len(failed_urls)}")
    print(f"- Failed|{len(failed_urls)}")

    if failed_urls:
        print("\n### Failed URLs")
        for url in failed_urls:
            print(f"- {url}")


def files_needing_description(index_path: Path) -> set[str]:
    """Local files whose INDEX.xml description is still the placeholder."""
    index_root = ET.parse(index_path).getroot()
    return {
        source.findtext("local_file", "")
        for source in index_root.findall("source")
        if source.findtext("description") == PLACEHOLDER_DESCRIPTION
    }


def format_descriptions_status(
    collection_dir: Path,
    outcome_counts: Counter[curate_doc.DocOutcome],
    failed_count: int,
    placeholder_files: set[str],
) -> str:
    """Build the `## Index Descriptions Status` report, listing files as `~/...` paths."""
    outcome = curate_doc.DocOutcome
    lines = [
        "\n## Index Descriptions Status",
        f"- ✅ Kept (content unchanged)|{outcome_counts[outcome.UNCHANGED]}",
        f"- ✅ Kept (whitespace-only change)|{outcome_counts[outcome.WHITESPACE_ONLY]}",
        f"- ⚠️ Kept unverified (file recreated)|{outcome_counts[outcome.RECREATED]}",
        f"- 🚩 Reset to PLACEHOLDER (content changed)|{outcome_counts[outcome.CHANGED]}",
        f"- 🚩 New source (PLACEHOLDER)|{outcome_counts[outcome.NEW]}",
        f"- ❌ Failed (description untouched)|{failed_count}",
        f"- 🚩 {PLACEHOLDER_DESCRIPTION} in INDEX.xml (needs description)"
        f"|{len(placeholder_files)} files",
    ]
    lines.extend(
        f"  - {format_path_for_display(collection_dir / filename)}"
        for filename in sorted(placeholder_files)
    )
    return "\n".join(lines)


def _run_sync(collection_dir: Path) -> None:
    """Sync one collection to its INDEX.xml."""
    index_path = collection_dir / "INDEX.xml"

    if not collection_dir.exists() or not collection_dir.is_dir():
        msg = f"Collection directory not found: {collection_dir}"
        raise CurationError(msg)

    if not index_path.exists():
        msg = f"Not a collection: {index_path} not found"
        raise CurationError(msg)

    # Read (and so validate) the index before the destructive orphan sweep.
    index_sources = read_index_sources(index_path)
    indexed_files = {source.local_file for source in index_sources}
    deleted_orphans = delete_orphan_files(collection_dir, indexed_files)

    print("\n## SYNC INDEX.xml (source of truth)")
    print(f"- Index sources ready to curate|{len(index_sources)}")
    print(f"- Orphan files deleted (not in INDEX)|{len(deleted_orphans)}")
    sys.stdout.flush()

    print(f"\n## CURATING INDEX SOURCES ({len(index_sources)} total)")
    sys.stdout.flush()
    failed_urls: list[str] = []
    results: list[curate_doc.CurationResult] = []

    for position, source in enumerate(index_sources, 1):
        print(f"### 🔄 Doc {position} of {len(index_sources)}: {source.local_file}")
        sys.stdout.flush()
        result = _curate_doc(collection_dir, source.source_url)

        if result is None:
            failed_urls.append(source.source_url)
        else:
            results.append(result)
        sys.stdout.flush()

    _print_curation_summary(index_sources, failed_urls)

    outcome_counts = Counter(result.outcome for result in results)
    placeholder_files = files_needing_description(index_path)
    print(
        format_descriptions_status(
            collection_dir, outcome_counts, len(failed_urls), placeholder_files
        )
    )


def main() -> None:
    """Sync INDEX.xml, curate all docs, output structured results."""
    parser = argparse.ArgumentParser(
        description=(
            "Re-sync a docs collection to its INDEX.xml, "
            "refreshing every doc from source."
        ),
        epilog="""\
INDEX.xml is the source of truth. This reconciles the files on disk to it,
then re-fetches each listed doc from its source_url so content is current.

what it changes (destructive — commit or stash first):
  - Deletes orphan files not listed in INDEX.xml (README.md and dotfiles
    are kept).
  - Re-curates every listed source: overwrites its doc file with fresh content
    (recreating missing files), and refreshes that source's <title> and
    <curated_at> date in INDEX.xml.
  - Keeps existing descriptions for docs whose content is unchanged (ignoring
    whitespace); resets a changed doc's description to PLACEHOLDER, and flags
    every source whose description is still PLACEHOLDER.

what it never does: remove an INDEX source.

output: a structured report (sync counts, per-source description outcomes, and
        docs still needing descriptions).
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "collection_dir", help="Target collection directory (must contain INDEX.xml)"
    )
    args = parser.parse_args()

    try:
        _run_sync(normalise_collection_dir(args.collection_dir))
    except CurationError as exc:
        print(f"❌ {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
