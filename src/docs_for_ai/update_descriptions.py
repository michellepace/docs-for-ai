"""Update INDEX.xml descriptions from a descriptions file."""

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from docs_for_ai.index_io import write_index


def parse_descriptions_file(descriptions_path: Path) -> dict[str, str]:
    """Parse descriptions file into filename -> description mapping.

    Expected format:
    getting-started-installation.md
    Description text for this file
    configuration-typescript.md
    Description text for this file

    Args:
        descriptions_path: Path to descriptions file

    Returns:
        Dictionary mapping local_file to description text
    """
    descriptions: dict[str, str] = {}
    lines = descriptions_path.read_text().strip().split("\n")

    i = 0
    while i < len(lines):
        # Skip empty lines
        if not lines[i].strip():
            i += 1
            continue

        # Line should be a URL
        url = lines[i].strip()
        i += 1

        # Skip any empty lines before description
        while i < len(lines) and not lines[i].strip():
            i += 1

        # Next non-empty line should be the description
        if i < len(lines):
            description = lines[i].strip()
            descriptions[url] = description
            i += 1
        else:
            print(
                f"Warning: filename '{url}' has no description, skipping",
                file=sys.stderr,
            )

    return descriptions


def _validate_collection_inputs(
    directory: str, descriptions_file: str
) -> tuple[Path, Path]:
    """Validate collection (INDEX.xml exists) and descriptions file exist.

    Args:
        directory: Collection directory path from arguments
        descriptions_file: Descriptions file path from arguments

    Returns:
        Tuple of (index_path, descriptions_path) for downstream use

    Exits with error message if any validation fails.
    """
    collection_dir = Path(directory)
    index_path = collection_dir / "INDEX.xml"
    descriptions_path = Path(descriptions_file)

    # Validate this is a collection (has INDEX.xml)
    if not index_path.exists():
        print(f"Error: Not a valid collection - {index_path} not found", file=sys.stderr)
        sys.exit(1)

    # Validate descriptions file exists
    if not descriptions_path.exists():
        print(
            f"Error: Descriptions file '{descriptions_path}' does not exist",
            file=sys.stderr,
        )
        sys.exit(1)

    return index_path, descriptions_path


def _cleanup_temp_file(file_path: Path) -> None:
    """Delete temporary file with error handling."""
    try:
        file_path.unlink()
        print(f"🗑️  Cleaned up temporary file: {file_path}")
    except OSError as e:
        print(f"Warning: Could not delete {file_path}: {e}", file=sys.stderr)


def update_descriptions(index_path: Path, descriptions: dict[str, str]) -> int:
    """Update descriptions in INDEX.xml, write file, return count.

    Args:
        index_path: Path to INDEX.xml file
        descriptions: Dictionary mapping local_file to new description

    Returns:
        Number of descriptions updated
    """
    root = ET.parse(index_path).getroot()

    updated_count = 0

    for source in root.findall("source"):
        file_elem = source.find("local_file")
        desc_elem = source.find("description")

        if (
            file_elem is not None
            and file_elem.text in descriptions
            and desc_elem is not None
        ):
            old_desc = desc_elem.text
            new_desc = descriptions[file_elem.text]

            if old_desc != new_desc:
                desc_elem.text = new_desc
                updated_count += 1
                print(f"✅ Updated: {file_elem.text}")
            else:
                print(f"ℹ️  Unchanged: {file_elem.text}")  # noqa: RUF001

    # Write back to INDEX.xml
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
        "descriptions_file", help="Path to descriptions file (e.g. descriptions.txt)"
    )
    args = parser.parse_args()

    # Validate collection and inputs
    index_path, descriptions_path = _validate_collection_inputs(
        args.directory, args.descriptions_file
    )

    # Parse descriptions file
    descriptions = parse_descriptions_file(descriptions_path)

    if not descriptions:
        print("Error: No descriptions found in file", file=sys.stderr)
        sys.exit(1)

    print(f"📋 Parsed {len(descriptions)} description(s) from {descriptions_path}")
    print()

    # Update INDEX.xml
    update_descriptions(index_path, descriptions)

    # Cleanup temporary file
    _cleanup_temp_file(descriptions_path)


if __name__ == "__main__":
    main()
