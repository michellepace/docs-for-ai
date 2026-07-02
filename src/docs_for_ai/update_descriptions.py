"""Update INDEX.xml descriptions. See `update-descriptions --help` for behaviour."""

import argparse
import sys
import xml.etree.ElementTree as ET
from itertools import batched
from pathlib import Path

from docs_for_ai.errors import CurationError
from docs_for_ai.index_io import write_index
from docs_for_ai.paths import normalise_collection_dir

DESCRIP_MIN_WORDS = 20
DESCRIP_MAX_WORDS = 30
LINES_PER_ENTRY = 2  # filename line + description line

type DescriptionsByFile = dict[str, str]


def _validate_word_counts(descriptions: DescriptionsByFile) -> bool:
    """True when every description is within band."""
    all_in_band = True
    for local_file, description in descriptions.items():
        count = len(description.split())
        if DESCRIP_MIN_WORDS <= count <= DESCRIP_MAX_WORDS:
            print(f"✅ {local_file}: {count} words")
        else:
            print(
                f"❌ {local_file}: {count} words "
                f"(need {DESCRIP_MIN_WORDS}-{DESCRIP_MAX_WORDS})"
            )
            all_in_band = False
    return all_in_band


def parse_descriptions_file(descriptions_path: Path) -> DescriptionsByFile:
    """Parse a descriptions file into a {local_file: description} mapping."""
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
            print(f"⚠️ No description for {entry[0]}: skipping")

    return descriptions


def _validate_collection_inputs(
    collection_dir: Path, temp_descriptions_file: str
) -> tuple[Path, Path]:
    """Resolve and validate the INDEX.xml and descriptions paths, or raise."""
    index_path = collection_dir / "INDEX.xml"
    descriptions_path = Path(temp_descriptions_file)

    if not index_path.exists():
        msg = f"Not a collection: {index_path} not found"
        raise CurationError(msg)

    if not descriptions_path.exists():
        msg = f"Descriptions file not found: {descriptions_path}"
        raise CurationError(msg)

    return index_path, descriptions_path


def _cleanup_temp_file(descriptions_path: Path) -> None:
    """Delete the temporary descriptions file, warning if it can't be removed."""
    try:
        descriptions_path.unlink()
        print(f"🗑️ Cleaned up: {descriptions_path}")
    except OSError as exc:
        print(f"⚠️ Could not delete {descriptions_path}: {exc}")


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
            print(f"ℹ️ Unchanged: {file_elem.text}")  # noqa: RUF001
            continue

        desc_elem.text = new_desc
        updated_count += 1
        print(f"✅ Updated: {file_elem.text}")

    if updated_count > 0:
        write_index(root, index_path)
        print(f"\n🏁 Updated {updated_count} description(s) in {index_path}")
    else:
        print(f"\nℹ️ No updates needed: {index_path}")  # noqa: RUF001

    return updated_count


def _run_update(collection_dir: Path, temp_descriptions_file: str) -> None:
    """Apply a descriptions file to INDEX.xml."""
    index_path, descriptions_path = _validate_collection_inputs(
        collection_dir, temp_descriptions_file
    )

    descriptions = parse_descriptions_file(descriptions_path)

    if not descriptions:
        msg = f"No descriptions found: {descriptions_path}"
        raise CurationError(msg)

    # Reject before touching INDEX.xml if out of the word-count band
    if not _validate_word_counts(descriptions):
        msg = "Word count(s) out of band: rewrite the flagged description(s) and rerun"
        raise CurationError(msg)

    print(f"✅ Parsed: {len(descriptions)} description(s)")
    print()

    updated_count = update_descriptions(index_path, descriptions)

    if updated_count > 0:
        _cleanup_temp_file(descriptions_path)


def main() -> None:
    """Parse arguments and update descriptions in INDEX.xml."""
    parser = argparse.ArgumentParser(
        description=(
            "Apply descriptions from a file to a collection's INDEX.xml, "
            "matched by filename."
        ),
        epilog=(
            "descriptions file format — one pair of lines per INDEX source:\n"
            "  <filename>\n"
            f"  <description>   ({DESCRIP_MIN_WORDS}-{DESCRIP_MAX_WORDS} words)\n\n"
            "A description outside that word band fails the run; "
            "INDEX.xml is left untouched."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "collection_dir", help="Target collection directory (must contain INDEX.xml)"
    )
    parser.add_argument(
        "temp_descriptions_file",
        help="Descriptions file (deleted after a successful update)",
    )
    args = parser.parse_args()

    try:
        _run_update(
            normalise_collection_dir(args.collection_dir), args.temp_descriptions_file
        )
    except CurationError as exc:
        print(f"❌ {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
