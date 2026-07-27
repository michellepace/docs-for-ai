"""Update INDEX.xml descriptions. See `update-descriptions --help` for behaviour."""

import argparse
import sys
import xml.etree.ElementTree as ET
from itertools import batched
from typing import TYPE_CHECKING

from docs_for_ai.errors import CurationError
from docs_for_ai.index_io import write_index
from docs_for_ai.paths import normalise_collection_dir

if TYPE_CHECKING:
    from pathlib import Path

DESCRIP_MIN_WORDS = 20
DESCRIP_MAX_WORDS = 30
LINES_PER_ENTRY = 2  # filename line + description line

type DescriptionsByFile = dict[str, str]


def parse_descriptions(text: str) -> DescriptionsByFile:
    """Parse filename/description line pairs into a {local_file: description} map."""
    non_blank_lines = [line.strip() for line in text.splitlines() if line.strip()]

    descriptions: DescriptionsByFile = {}
    for entry in batched(non_blank_lines, LINES_PER_ENTRY, strict=False):
        if len(entry) == LINES_PER_ENTRY:
            local_file, description = entry
            descriptions[local_file] = description
        else:
            print(f"no description for {entry[0]}: skipping")

    return descriptions


def _in_band_descriptions(descriptions: DescriptionsByFile) -> DescriptionsByFile:
    """Print a per-file word-count verdict; return only descriptions within band."""
    in_band: DescriptionsByFile = {}
    for local_file, description in descriptions.items():
        count = len(description.split())
        if DESCRIP_MIN_WORDS <= count <= DESCRIP_MAX_WORDS:
            print(f"✅ {local_file}: {count} words")
            in_band[local_file] = description
        else:
            print(
                f"❌ {local_file}: {count} words "
                f"(need {DESCRIP_MIN_WORDS}-{DESCRIP_MAX_WORDS})"
            )
    return in_band


def update_descriptions(index_path: Path, descriptions: DescriptionsByFile) -> int:
    """Apply matching descriptions to INDEX.xml, write if changed, return count."""
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
            print(f"unchanged: {file_elem.text}")
            continue

        desc_elem.text = new_desc
        updated_count += 1
        print(f"✅ Updated: {file_elem.text}")

    if updated_count > 0:
        write_index(root, index_path)
        print(f"\n🏁 Updated {updated_count} description(s) in {index_path}")
    else:
        print(f"no updates needed: {index_path}")

    return updated_count


def _run_update(collection_dir: Path, descriptions_text: str) -> None:
    """Apply piped descriptions to the collection's INDEX.xml."""
    index_path = collection_dir / "INDEX.xml"
    if not index_path.exists():
        msg = f"Not a collection: {index_path} not found"
        raise CurationError(msg)

    descriptions = parse_descriptions(descriptions_text)
    if not descriptions:
        msg = "No descriptions found on stdin (see --help for the format)"
        raise CurationError(msg)

    in_band = _in_band_descriptions(descriptions)
    print()

    if in_band:
        update_descriptions(index_path, in_band)

    if len(in_band) < len(descriptions):
        msg = (
            "Word count(s) out of band: rewrite the flagged description(s) "
            "and rerun with only those"
        )
        raise CurationError(msg)


def _read_piped_stdin() -> str:
    """Return stdin content, rejecting an interactive terminal with nothing piped."""
    if sys.stdin.isatty():
        msg = "No descriptions piped to stdin: pipe a heredoc (see --help)"
        raise CurationError(msg)
    return sys.stdin.read()


def main() -> None:
    """Parse arguments and apply stdin descriptions to a collection's INDEX.xml."""
    parser = argparse.ArgumentParser(
        description=(
            "Apply descriptions from stdin to a collection's INDEX.xml, "
            "matched by <local_file> filename."
        ),
        epilog=(
            "stdin format — one line pair per INDEX source, "
            "piped via a quoted heredoc:\n"
            "  update-descriptions collections/<name> <<'EOF'\n"
            "  <local_file>    (bare filename, not a path)\n"
            f"  <description>   ({DESCRIP_MIN_WORDS}-{DESCRIP_MAX_WORDS} words)\n"
            "  ...             (repeat the line pair per source)\n"
            "  EOF\n\n"
            "Out-of-band descriptions are flagged (exit 1); in-band siblings "
            "still apply. Unmatched filenames are skipped without error."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "collection_dir", help="Target collection directory (must contain INDEX.xml)"
    )
    args = parser.parse_args()

    try:
        _run_update(normalise_collection_dir(args.collection_dir), _read_piped_stdin())
    except CurationError as exc:
        print(f"❌ {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
