"""Path helpers shared across the curation scripts."""

from pathlib import Path


def format_path_for_display(path: Path) -> str:
    """Format a resolved absolute path for display, collapsing $HOME to `~`."""
    resolved = path.resolve()
    home = Path.home()
    if resolved.is_relative_to(home):
        return f"~/{resolved.relative_to(home)}"
    return str(resolved)


def collection_label(collection_dir: Path) -> str:
    """`parent/name` report-header label, resolving so a bare arg still renders."""
    resolved = collection_dir.resolve()
    return f"{resolved.parent.name}/{resolved.name}"


def normalise_collection_dir(raw: str) -> Path:
    """Collection dir from a CLI arg; `Path` already tolerates a trailing slash."""
    return Path(raw)
