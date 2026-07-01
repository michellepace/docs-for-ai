"""Path helpers shared across the curation scripts."""

from pathlib import Path


def format_path_for_display(path: Path) -> str:
    """Format a resolved absolute path for display, collapsing $HOME to `~`."""
    resolved = path.resolve()
    home = Path.home()
    if resolved.is_relative_to(home):
        return f"~/{resolved.relative_to(home)}"
    return str(resolved)


def normalise_collection_dir(raw: str) -> Path:
    """Collection dir from a CLI arg, tolerating a trailing slash."""
    return Path(raw.rstrip("/"))
