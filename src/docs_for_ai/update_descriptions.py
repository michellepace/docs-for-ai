"""Update INDEX.xml descriptions from a descriptions file."""

import argparse
import sys
import xml.etree.ElementTree as ET
from itertools import batched
from pathlib import Path

from docs_for_ai.index_io import write_index

DESCRIP_MIN_WORDS = 20
DESCRIP_MAX_WORDS = 30
LINES_PER_ENTRY = 2  # filename line followed by its description line

type DescriptionsByFile = dict[str, str]


def _validate_word_counts(descriptions: DescriptionsByFile) -> None:
    """Ensure description is within [min, max] band."""
    failed = False
    for local_file, description in descriptions.items():
        count = len(description.split())
        if DESCRIP_MIN_WORDS <= count <= DESCRIP_MAX_WORDS:
            print(f"✅ '{local_file}' description is {count} words")
        else:
            print(
                f"❌ Error: '{local_file}' description is {count} words "
                f"(need {DESCRIP_MIN_WORDS}-{DESCRIP_MAX_WORDS})",
                file=sys.stderr,
            )
            failed = True
    if failed:
        sys.exit(1)


def parse_descriptions_file(descriptions_path: Path) -> DescriptionsByFile:
    """Parse a descriptions file of alternating local_file / description lines.

    file1.md
    Description text file 1
    file2.md
    Description text file 2
    """
    non_blank_lines = [
        line.strip()
        for line in descriptions_path.read_text().splitlines()
        if line.strip()
    ]

    descriptions: DescriptionsByFile = {}
    for entry in batched(non_blank_lines, LINES_PER_ENTRY, strict=False):
        if len(entry) == LINES_PER_ENTRY:
            local_file, description = entry
            descriptions[local_file] = description
        else:
            print(
                f"Warning: filename '{entry[0]}' has no description, skipping",
                file=sys.stderr,
            )

    return descriptions


def _validate_collection_inputs(
    directory: str, temp_descriptions_file: str
) -> tuple[Path, Path]:
    """Resolve and validate the INDEX.xml and descriptions paths, or exit."""
    collection_dir = Path(directory)
    index_path = collection_dir / "INDEX.xml"
    descriptions_path = Path(temp_descriptions_file)

    if not index_path.exists():
        print(
            f"❌ Error: Not a valid collection - {index_path} not found",
            file=sys.stderr,
        )
        sys.exit(1)

    if not descriptions_path.exists():
        print(
            f"❌ Error: Descriptions file '{descriptions_path}' does not exist",
            file=sys.stderr,
        )
        sys.exit(1)

    return index_path, descriptions_path


def _cleanup_temp_file(descriptions_path: Path) -> None:
    """Delete the temporary descriptions file, warning if it can't be removed."""
    try:
        descriptions_path.unlink()
        print(f"🗑️  Cleaned up temporary file: {descriptions_path}")
    except OSError as exc:
        print(f"Warning: Could not delete {descriptions_path}: {exc}", file=sys.stderr)


def update_descriptions(index_path: Path, descriptions: DescriptionsByFile) -> int:
    """Apply matching descriptions to INDEX.xml, write if changed, return update count."""
    root = ET.parse(index_path).getroot()

    updated_count = 0

    for source in root.findall("source"):
        file_elem = source.find("local_file")
        desc_elem = source.find("description")

        if file_elem is None or desc_elem is None:
            continue
        if file_elem.text not in descriptions:
            continue

        new_desc = descriptions[file_elem.text]
        if desc_elem.text == new_desc:
            print(f"ℹ️  Unchanged: {file_elem.text}")  # noqa: RUF001
            continue

        desc_elem.text = new_desc
        updated_count += 1
        print(f"✅ Updated: {file_elem.text}")

    if updated_count > 0:
        write_index(root, index_path)
        print(f"\n🎉 Updated {updated_count} description(s) in {index_path}")
    else:
        print(f"\nℹ️  No descriptions needed updating in {index_path}")  # noqa: RUF001

    return updated_count


def main() -> None:
    """Parse arguments and update descriptions in INDEX.xml."""
    parser = argparse.ArgumentParser(
        description="Update INDEX.xml descriptions from descriptions file"
    )
    parser.add_argument(
        "directory", help="Collection directory (e.g. collections/shiny/)"
    )
    parser.add_argument(
        "temp_descriptions_file",
        help="Temporary descriptions file (deleted after a successful update)",
    )
    args = parser.parse_args()

    index_path, descriptions_path = _validate_collection_inputs(
        args.directory, args.temp_descriptions_file
    )

    descriptions = parse_descriptions_file(descriptions_path)

    if not descriptions:
        print("❌ Error: No descriptions found in file", file=sys.stderr)
        sys.exit(1)

    # Reject before touching INDEX.xml if out of the word-count band
    _validate_word_counts(descriptions)

    print(f"📋 Parsed {len(descriptions)} description(s) from {descriptions_path}")
    print()

    update_descriptions(index_path, descriptions)

    _cleanup_temp_file(descriptions_path)


if __name__ == "__main__":
    main()
