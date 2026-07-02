"""Sync INDEX.xml and re-curate all docs. See `sync-index --help` for behaviour."""

import argparse
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import NamedTuple

from docs_for_ai import curate_doc
from docs_for_ai.errors import CurationError
from docs_for_ai.index_io import PLACEHOLDER_DESCRIPTION, write_index
from docs_for_ai.paths import format_path_for_display, normalise_collection_dir


class CuratedSource(NamedTuple):
    """A curated doc: its local filename paired with its source URL."""

    local_file: str
    source_url: str


# Collection files that must survive a sync.
_NON_DOC_FILES = {"INDEX.xml", "README.md"}


def prune_stale_index_sources(
    index_path: Path, collection_dir: Path
) -> tuple[list[CuratedSource], int]:
    """Remove malformed, blank, or missing-file sources, rewriting INDEX.xml."""
    index_root = ET.parse(index_path).getroot()

    live_sources: list[CuratedSource] = []
    removed_count = 0

    for source in list(index_root.findall("source")):
        local_file_elem = source.find("local_file")
        source_url_elem = source.find("source_url")

        if local_file_elem is None or source_url_elem is None:
            index_root.remove(source)
            removed_count += 1
            continue

        local_file = (local_file_elem.text or "").strip()
        source_url = (source_url_elem.text or "").strip()

        if not local_file or not source_url or not (collection_dir / local_file).exists():
            index_root.remove(source)
            removed_count += 1
        else:
            live_sources.append(CuratedSource(local_file, source_url))

    if removed_count > 0:
        write_index(index_root, index_path)

    return live_sources, removed_count


def delete_orphan_files(collection_dir: Path, indexed_files: set[str]) -> list[str]:
    """Delete on-disk docs with no matching INDEX.xml <local_file>."""
    keep = indexed_files | _NON_DOC_FILES
    deleted: list[str] = []
    for path in sorted(collection_dir.iterdir()):
        if not path.is_file() or path.name in keep or path.name.endswith(".backup"):
            continue
        path.unlink()
        deleted.append(path.name)
    return deleted


def _curate_doc(collection_dir: Path, source_url: str) -> bool:
    """Curate one source in-process; print its failure line and return False."""
    try:
        curate_doc.curate(collection_dir, source_url)
    except CurationError as exc:
        print(f"❌ {exc}")
        return False
    except Exception as exc:  # noqa: BLE001 — one doc's crash must not abort the sync
        print(f"❌ Unexpected error: {type(exc).__name__}: {exc} — {source_url}")
        return False
    return True


def _print_git_content_changes(collection_dir: Path) -> None:
    """Print git diff --stat for the collection, wrapped in report tags."""
    git_path = shutil.which("git")
    if not git_path:
        print("⚠️ Git not found: skipping change detection")
        return

    result = subprocess.run(
        [git_path, "diff", "--stat", "-w", "."],
        check=False,
        capture_output=True,
        text=True,
        cwd=collection_dir,
    )

    print("\n### Git Content Changes (git diff --stat -w)")
    print("<GIT_CONTENT_CHANGES>")
    if result.stdout.strip():
        print(result.stdout.rstrip())
    else:
        print("No content changes detected")
    print("</GIT_CONTENT_CHANGES>")


def _print_curation_summary(
    curated_sources: list[CuratedSource],
    failed_urls: list[str],
) -> None:
    print("\n### Curation Summary")
    print(f"- Successful|{len(curated_sources) - len(failed_urls)}")
    print(f"- Failed|{len(failed_urls)}")

    if failed_urls:
        print("\n### Failed URLs")
        for url in failed_urls:
            print(f"- {url}")


def _validate_and_backup_index(index_path: Path) -> Path:
    """Validate XML structure (exit on parse error), then create a backup file."""
    try:
        ET.parse(index_path)
    except ET.ParseError as e:
        print(f"❌ Invalid XML: {e} — {index_path}")
        sys.exit(1)

    backup_path = index_path.with_suffix(".xml.backup")
    shutil.copy2(index_path, backup_path)
    return backup_path


def get_changed_curated_files(collection_dir: Path, indexed_files: set[str]) -> set[str]:
    """Return INDEX filenames with non-whitespace content changes (git diff -w)."""
    git_path = shutil.which("git")
    if not git_path:
        return set()

    result = subprocess.run(
        [git_path, "diff", "--numstat", "-w", "--", "."],
        capture_output=True,
        text=True,
        check=False,
        cwd=collection_dir,
    )

    # numstat is tab-separated: "additions  deletions  filepath"
    numstat_field_count = 3

    changed_files: set[str] = set()
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue

        numstat_fields = line.split("\t")
        if len(numstat_fields) < numstat_field_count:
            continue

        filename = Path(numstat_fields[2]).name
        if filename in indexed_files:
            changed_files.add(filename)

    return changed_files


def restore_unchanged_descriptions(
    index_path: Path, backup_path: Path, changed_files: set[str]
) -> int:
    """Restore descriptions for unchanged files from backup."""
    backup_tree = ET.parse(backup_path)
    backup_root = backup_tree.getroot()
    backup_descriptions: dict[str | None, str | None] = {}

    for source in backup_root.findall("source"):
        local_file_elem = source.find("local_file")
        desc_elem = source.find("description")

        if local_file_elem is not None and desc_elem is not None:
            backup_descriptions[local_file_elem.text] = desc_elem.text

    current_root = ET.parse(index_path).getroot()
    restored_count = 0

    for source in current_root.findall("source"):
        local_file_elem = source.find("local_file")
        desc_elem = source.find("description")

        if local_file_elem is None or desc_elem is None:
            continue

        local_file = local_file_elem.text

        if (
            local_file not in changed_files
            and local_file in backup_descriptions
            and backup_descriptions[local_file] != PLACEHOLDER_DESCRIPTION
        ):
            desc_elem.text = backup_descriptions[local_file]
            restored_count += 1

    if restored_count > 0:
        write_index(current_root, index_path)

    return restored_count


def format_descriptions_status(
    collection_dir: Path, restored_count: int, changed_files: set[str]
) -> str:
    """Build the `## Index Descriptions Status` report, listing files as `~/...` paths."""
    lines = [
        "\n## Index Descriptions Status",
        f"- ✅ Restored (whitespace-only changes)|{restored_count} files",
        f"- ⚠️ {PLACEHOLDER_DESCRIPTION} in INDEX.xml (needs description)"
        f"|{len(changed_files)} files",
    ]
    lines.extend(
        f"  - {format_path_for_display(collection_dir / filename)}"
        for filename in sorted(changed_files)
    )
    return "\n".join(lines)


def _cleanup_backup(backup_path: Path) -> None:
    """Delete backup file with error handling (non-fatal)."""
    try:
        backup_path.unlink(missing_ok=True)
    except OSError as e:
        print(f"⚠️ Could not delete backup: {e}")


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
  - Drops INDEX sources that are malformed or whose local_file is missing.
  - Deletes orphan doc files not listed in INDEX.xml (README.md is kept).
  - Re-curates every listed source: overwrites its doc file with fresh content,
    and refreshes that source's <title> and <curated_at> date in INDEX.xml.
  - Keeps existing descriptions for docs whose content is unchanged; flags docs
    whose content changed as needing a new description.

output: a structured report (sync counts, per-doc curation results, content
        changes, docs still needing descriptions).
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "collection_dir", help="Target collection directory (must contain INDEX.xml)"
    )
    args = parser.parse_args()

    collection_dir = normalise_collection_dir(args.collection_dir)
    index_path = collection_dir / "INDEX.xml"

    if not collection_dir.exists() or not collection_dir.is_dir():
        print(f"❌ Collection directory not found: {collection_dir}")
        sys.exit(1)

    if not index_path.exists():
        print(f"❌ Not a collection: {index_path} not found")
        sys.exit(1)

    backup_path = _validate_and_backup_index(index_path)

    sources_to_curate, removed_count = prune_stale_index_sources(
        index_path, collection_dir
    )
    indexed_files = {source.local_file for source in sources_to_curate}
    deleted_orphans = delete_orphan_files(collection_dir, indexed_files)

    print("\n## SYNC INDEX.xml (source of truth)")
    print(f"- Index sources ready to curate|{len(sources_to_curate)}")
    print(f"- Stale sources removed (missing file)|{removed_count}")
    print(f"- Orphan files deleted (not in INDEX)|{len(deleted_orphans)}")
    sys.stdout.flush()

    print(f"\n## CURATING INDEX SOURCES ({len(sources_to_curate)} total)")
    sys.stdout.flush()
    failed_urls: list[str] = []

    for position, source in enumerate(sources_to_curate, 1):
        print(f"### 🔄 Doc {position} of {len(sources_to_curate)}: {source.local_file}")
        sys.stdout.flush()
        success = _curate_doc(collection_dir, source.source_url)

        if not success:
            failed_urls.append(source.source_url)
        sys.stdout.flush()

    _print_curation_summary(sources_to_curate, failed_urls)
    _print_git_content_changes(collection_dir)

    changed_files = get_changed_curated_files(collection_dir, indexed_files)
    restored_count = restore_unchanged_descriptions(
        index_path, backup_path, changed_files
    )

    print(format_descriptions_status(collection_dir, restored_count, changed_files))

    _cleanup_backup(backup_path)


if __name__ == "__main__":
    main()
