"""Sync INDEX.xml, re-scrape all docs, output results for batch processing."""

import argparse
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def get_markdown_files(collection_dir: Path) -> set[str]:
    """Return set of .md filenames (excluding README.md)."""
    return {file.name for file in collection_dir.glob("*.md") if file.name != "README.md"}


def sync_index_to_filesystem(
    index_path: Path, md_files: set[str]
) -> tuple[list[tuple[str, str]], list[str], int]:
    """Remove invalid sources from INDEX.xml, write cleaned file, return results.

    Args:
        index_path: Path to INDEX.xml file
        md_files: Set of existing .md filenames

    Returns:
        Tuple of (valid_pairs, orphans, removed_count) where:
        - valid_pairs: List of (local_file, source_url) tuples
        - orphans: List of .md filenames not in INDEX.xml
        - removed_count: Number of invalid sources removed
    """
    tree = ET.parse(index_path)
    root = tree.getroot()

    valid_pairs: list[tuple[str, str]] = []
    indexed_files: set[str] = set()
    removed_count = 0

    # Process each source entry
    for source in list(root.findall("source")):
        local_file_elem = source.find("local_file")
        source_url_elem = source.find("source_url")

        if local_file_elem is None or source_url_elem is None:
            root.remove(source)
            removed_count += 1
            continue

        local_file = (local_file_elem.text or "").strip()
        source_url = (source_url_elem.text or "").strip()

        # Remove if text is blank, or the markdown file doesn't exist
        if not local_file or not source_url or local_file not in md_files:
            root.remove(source)
            removed_count += 1
        else:
            # Valid entry
            valid_pairs.append((local_file, source_url))
            indexed_files.add(local_file)

    # Find orphan markdown files (exist but not in INDEX)
    orphans = sorted(md_files - indexed_files)

    # Write cleaned INDEX.xml back
    if removed_count > 0:
        ET.indent(root, space="  ")
        tree.write(index_path, encoding="unicode", xml_declaration=False)

    return valid_pairs, orphans, removed_count


def _scrape_doc(collection_dir: Path, source_url: str) -> bool:
    """Scrape single doc using curate_doc.py via subprocess.

    Args:
        collection_dir: Collection directory path
        source_url: URL to scrape

    Returns:
        True if successful, False if failed
    """
    # Find uv executable with absolute path to prevent PATH hijacking (S607)
    uv_path = shutil.which("uv")
    if not uv_path:
        print("Error: 'uv' executable not found in PATH", file=sys.stderr)
        return False

    # S603: Subprocess call is safe - calling our own trusted script with validated args
    # - collection_dir is validated by main() to be existing dir with INDEX.xml
    # - source_url is validated by curate_doc.py via urlparse
    # - Using list (not shell=True) prevents command injection
    result = subprocess.run(
        [uv_path, "run", "curate-doc", str(collection_dir), source_url],
        check=False,
        capture_output=False,  # Let output stream through
        text=True,
    )
    return result.returncode == 0


def _print_git_content_changes(collection_dir: Path) -> None:
    """Print git diff stats for the collection directory.

    Args:
        collection_dir: Path to collection directory
    """
    git_path = shutil.which("git")
    if not git_path:
        print("⚠️  Git not found - skipping change detection")
        return

    # S603: Subprocess call is safe - calling git with validated directory path
    # - collection_dir validated in main() to be existing directory
    # - Using list (not shell=True) prevents command injection
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


def _print_scrape_summary(
    valid_pairs: list[tuple[str, str]],
    failed_urls: list[str],
    orphans: list[str],
) -> None:
    """Print scrape summary."""
    print("\n### Scrape Summary")
    print(f"- Successful|{len(valid_pairs) - len(failed_urls)}")
    print(f"- Failed|{len(failed_urls)}")

    if orphans:
        print(f"- Orphaned files|{len(orphans)} (ignored - not in INDEX.xml)")

    # Show failed URLs for debugging
    if failed_urls:
        print("\n### Failed URLs")
        for url in failed_urls:
            print(f"- {url}")


def _backup_index_xml(index_path: Path) -> Path:
    """Validate XML structure and create backup file."""
    try:
        ET.parse(index_path)
    except ET.ParseError as e:
        print(f"❌ Error: INVALID_XML|{e}|{index_path}|", file=sys.stderr)
        sys.exit(1)

    backup_path = index_path.with_suffix(".xml.backup")
    shutil.copy2(index_path, backup_path)
    return backup_path


def get_changed_markdown_files(collection_dir: Path) -> set[str]:
    """Get set of changed .md filenames with non-whitespace changes.

    Uses git diff --numstat -w which only shows files with actual content changes,
    ignoring whitespace-only changes.
    """
    git_path = shutil.which("git")
    if not git_path:
        return set()

    # Use --numstat with -w: only returns files with non-whitespace changes
    # Output format: "additions deletions filename"
    result = subprocess.run(
        [git_path, "diff", "--numstat", "-w", "--", "."],
        capture_output=True,
        text=True,
        check=False,
        cwd=collection_dir,
    )

    # numstat format has 3 tab-separated fields: additions, deletions, filepath
    numstat_field_count = 3

    changed_files: set[str] = set()
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue

        parts = line.split("\t")
        if len(parts) < numstat_field_count:
            continue

        filepath = parts[2]
        if filepath.endswith(".md") and not filepath.endswith("README.md"):
            filename = Path(filepath).name
            changed_files.add(filename)

    return changed_files


def restore_unchanged_descriptions(
    index_path: Path, backup_path: Path, changed_files: set[str]
) -> int:
    """Restore descriptions for unchanged files from backup."""
    backup_tree = ET.parse(backup_path)
    backup_root = backup_tree.getroot()
    backup_descriptions = {}

    for source in backup_root.findall("source"):
        local_file_elem = source.find("local_file")
        desc_elem = source.find("description")

        if local_file_elem is not None and desc_elem is not None:
            backup_descriptions[local_file_elem.text] = desc_elem.text

    tree = ET.parse(index_path)
    root = tree.getroot()
    restored_count = 0

    for source in root.findall("source"):
        local_file_elem = source.find("local_file")
        desc_elem = source.find("description")

        if local_file_elem is None or desc_elem is None:
            continue

        local_file = local_file_elem.text

        if (
            local_file not in changed_files
            and local_file in backup_descriptions
            and backup_descriptions[local_file] != "PLACEHOLDER"
        ):
            desc_elem.text = backup_descriptions[local_file]
            restored_count += 1

    if restored_count > 0:
        ET.indent(root, space="  ")
        tree.write(index_path, encoding="unicode", xml_declaration=False)

    return restored_count


def _cleanup_backup(backup_path: Path) -> None:
    """Delete backup file with error handling (non-fatal)."""
    try:
        backup_path.unlink(missing_ok=True)
    except OSError as e:
        print(f"⚠️  Could not delete backup: {e}", file=sys.stderr)


def main() -> None:
    """Sync INDEX.xml, scrape all docs, output structured results."""
    parser = argparse.ArgumentParser(
        description="Sync INDEX.xml, re-scrape all docs, output batch processing data"
    )
    parser.add_argument(
        "directory", help="Collection directory (e.g. collections/shiny/)"
    )
    args = parser.parse_args()

    collection_dir = Path(args.directory)
    index_path = collection_dir / "INDEX.xml"

    # Validate directory and INDEX.xml exist
    if not collection_dir.exists() or not collection_dir.is_dir():
        print(f"Error: Directory '{collection_dir}' does not exist", file=sys.stderr)
        sys.exit(1)

    if not index_path.exists():
        print(f"Error: INDEX.xml not found in '{collection_dir}'", file=sys.stderr)
        sys.exit(1)

    # Backup INDEX.xml (validates XML structure)
    backup_path = _backup_index_xml(index_path)

    # Step 1: Sync INDEX.xml
    md_files = get_markdown_files(collection_dir)
    valid_pairs, orphans, removed_count = sync_index_to_filesystem(index_path, md_files)

    print("\n## SYNC INDEX.xml (source of truth)")
    print(f"- Index sources ready to scrape|{len(valid_pairs)}")
    print(f"- Stale sources removed (missing .md)|{removed_count}")
    print(f"- Orphaned .md files (not in INDEX)|{len(orphans)}")
    sys.stdout.flush()

    # Step 2: Scrape all docs
    print(f"\n## SCRAPING INDEX SOURCES ({len(valid_pairs)} total)")
    sys.stdout.flush()
    failed_urls: list[str] = []

    for idx, (local_file, source_url) in enumerate(valid_pairs, 1):
        print(f"### 🔄 Doc {idx} of {len(valid_pairs)}: {local_file}")
        sys.stdout.flush()
        success = _scrape_doc(collection_dir, source_url)

        if not success:
            failed_urls.append(source_url)
        sys.stdout.flush()

    # Step 3: Output scrape results
    _print_scrape_summary(valid_pairs, failed_urls, orphans)

    # Step 4: Show git changes summary
    _print_git_content_changes(collection_dir)

    # Restore unchanged descriptions
    changed_files = get_changed_markdown_files(collection_dir)
    restored_count = restore_unchanged_descriptions(
        index_path, backup_path, changed_files
    )

    # Show descriptions status
    print("\n## Index Descriptions Status")
    print(f"- ✅ Restored (.md whitespace-only changes)|{restored_count} files")
    print(f"- ⚠️ PLACEHOLDER in INDEX.xml (needs description)|{len(changed_files)} files")
    if changed_files:
        for filename in sorted(changed_files):
            print(f"  - {collection_dir}/{filename}")

    # Cleanup backup file
    _cleanup_backup(backup_path)


if __name__ == "__main__":
    main()
