"""Sync INDEX.xml and re-curate all docs. See `sync-index --help` for behaviour."""

import argparse
import sys
import xml.etree.ElementTree as ET
from typing import TYPE_CHECKING, NamedTuple

from docs_for_ai import curate_doc
from docs_for_ai.errors import CurationError
from docs_for_ai.index_io import PLACEHOLDER_DESCRIPTION
from docs_for_ai.paths import (
    collection_label,
    format_path_for_display,
    normalise_collection_dir,
)

if TYPE_CHECKING:
    from pathlib import Path


class IndexSource(NamedTuple):
    """One INDEX.xml <source> — written programmatically, so all fields are set."""

    local_file: str
    source_url: str


class SyncFailure(NamedTuple):
    """One source that failed to curate."""

    source_url: str
    error: str


class SyncReport(NamedTuple):
    """Everything one sync run produced, ready for `format_sync_report`."""

    collection_dir: Path
    total_sources: int
    successes: list[curate_doc.CurationResult]
    failures: list[SyncFailure]
    orphans_deleted: int
    placeholder_files: set[str]


# Collection files that must survive a sync.
_PROTECTED_FILES = {"INDEX.xml", "README.md"}

# Reason tag per description-resetting outcome; any other placeholder in
# INDEX.xml was carried over from an earlier run.
_PLACEHOLDER_REASONS = {
    curate_doc.DocOutcome.NEW: "new source",
    curate_doc.DocOutcome.CHANGED: "content changed",
    curate_doc.DocOutcome.RECREATED: "file recreated",
}
_CARRIED_OVER_REASON = "kept placeholder"


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


def _curate_or_error(
    collection_dir: Path, source_url: str
) -> curate_doc.CurationResult | SyncFailure:
    """Curate one source in-process; a failure returns its `SyncFailure`."""
    try:
        return curate_doc.curate(collection_dir, source_url)
    except CurationError as exc:
        return SyncFailure(source_url, str(exc))
    except Exception as exc:  # noqa: BLE001 — one doc's crash must not abort the sync
        return SyncFailure(
            source_url, f"Unexpected error: {type(exc).__name__}: {exc} — {source_url}"
        )


def files_needing_description(index_path: Path) -> set[str]:
    """Local files whose INDEX.xml description is still the placeholder."""
    index_root = ET.parse(index_path).getroot()
    return {
        source.findtext("local_file", "")
        for source in index_root.findall("source")
        if source.findtext("description") == PLACEHOLDER_DESCRIPTION
    }


def _placeholder_reasons(results: list[curate_doc.CurationResult]) -> dict[str, str]:
    """Reason tag per curated file whose outcome reset its description."""
    return {
        result.local_file: _PLACEHOLDER_REASONS[result.outcome]
        for result in results
        if result.outcome in _PLACEHOLDER_REASONS
    }


def format_sync_report(report: SyncReport) -> str:
    """Build the end-of-run report: counts, then actionable sections only."""
    curated = len(report.successes)
    lines = [
        f"SYNC {collection_label(report.collection_dir)}",
        f"sources {report.total_sources} · curated {curated}"
        f" · failed {len(report.failures)} · orphans deleted {report.orphans_deleted}",
    ]

    if report.failures:
        lines += ["", f"FAILED ({len(report.failures)})"]
        for failure in report.failures:
            # Error messages often end "— <url>"; the line above already shows it.
            error = failure.error.removesuffix(f" — {failure.source_url}")
            lines += [f"  {failure.source_url}", f"    {error}"]

    if report.placeholder_files:
        reasons = _placeholder_reasons(report.successes)
        paths = {
            filename: format_path_for_display(report.collection_dir / filename)
            for filename in sorted(report.placeholder_files)
        }
        width = max(len(path) for path in paths.values())
        lines += ["", f"NEEDS DESCRIPTION ({len(paths)})"]
        lines += [
            f"  {path:<{width}}  ({reasons.get(filename, _CARRIED_OVER_REASON)})"
            for filename, path in paths.items()
        ]

    needed = len(report.placeholder_files)
    noun = "description" if needed == 1 else "descriptions"
    lines += [
        "",
        f"🏁 Sync complete: {curated}/{report.total_sources} curated,"
        f" {needed} {noun} needed",
    ]
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

    successes: list[curate_doc.CurationResult] = []
    failures: list[SyncFailure] = []
    total = len(index_sources)

    for position, source in enumerate(index_sources, 1):
        attempt = _curate_or_error(collection_dir, source.source_url)
        if isinstance(attempt, SyncFailure):
            failures.append(attempt)
            print(
                f"[{position}/{total}] {'FAIL':<6}{source.local_file} — {attempt.error}"
            )
        else:
            successes.append(attempt)
            print(f"[{position}/{total}] {'ok':<6}{attempt.local_file}")
        sys.stdout.flush()

    if index_sources:
        print()
    report = SyncReport(
        collection_dir=collection_dir,
        total_sources=total,
        successes=successes,
        failures=failures,
        orphans_deleted=len(deleted_orphans),
        placeholder_files=files_needing_description(index_path),
    )
    print(format_sync_report(report))


def main() -> None:
    """Sync INDEX.xml, curate all docs, print ticks then one report."""
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
    whitespace); resets a changed or recreated doc's description to PLACEHOLDER,
    and flags every source whose description is still PLACEHOLDER.

what it never does: remove an INDEX source.

output: one tick line per doc while curating, then a report — counts,
        failed sources, and docs still needing descriptions.
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
