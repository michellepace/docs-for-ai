# /// script
# requires-python = ">=3.14"
# dependencies = ["rich>=15.0.0"]
# ///
"""Report the state of every collection INDEX.xml in the repo."""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from rich.console import Console
from rich.table import Table

PLACEHOLDER = "PLACEHOLDER"
COLLECTIONS_DIR = "collections"


@dataclass(frozen=True)
class CollectionStats:
    """Tally of one collection's INDEX.xml."""

    name: str
    total: int
    populated: int
    date_counts: Counter[str]
    error: str | None = None

    @property
    def placeholder(self) -> int:
        """Sources still carrying a PLACEHOLDER (or empty) description."""
        return self.total - self.populated


def analyse_index(index_path: Path) -> CollectionStats:
    """Parse one INDEX.xml into a CollectionStats (pure, no side effects)."""
    name = index_path.parent.name
    try:
        root = ET.parse(index_path).getroot()  # noqa: S314  (trusted local files)
    except ET.ParseError as exc:
        return CollectionStats(name, 0, 0, Counter(), error=f"parse error: {exc}")

    sources = root.findall("source")
    populated = 0
    date_counts: Counter[str] = Counter()
    for source in sources:
        description = (source.findtext("description") or "").strip()
        if description and description != PLACEHOLDER:
            populated += 1
        curated = (source.findtext("curated_at") or "").strip() or "(missing)"
        date_counts[curated] += 1

    return CollectionStats(name, len(sources), populated, date_counts)


def format_dates(date_counts: Counter[str]) -> str:
    """Render curation dates: a single date, or each distinct date with its count."""
    if not date_counts:
        return "—"
    if len(date_counts) == 1:
        return next(iter(date_counts))
    # ISO dates sort chronologically as plain strings.
    return "\n".join(f"{date} x{count}" for date, count in sorted(date_counts.items()))


def find_indexes(root: Path) -> list[Path]:
    """Return every collections/<collection>/INDEX.xml under root, sorted by name."""
    return sorted(root.glob(f"{COLLECTIONS_DIR}/*/INDEX.xml"))


def build_table(stats: list[CollectionStats]) -> Table:
    """Build the rich table (plus a totals footer row)."""
    table = Table(title="📦 Collection INDEX.xml status", show_footer=True)
    table.add_column("Collection", style="bold cyan", footer="TOTAL")
    table.add_column("Sources", justify="right")
    table.add_column("Populated", justify="right", style="green")
    table.add_column("Placeholder", justify="right")
    table.add_column("Curated date(s)")

    total_sources = sum(s.total for s in stats)
    total_populated = sum(s.populated for s in stats)
    total_placeholder = sum(s.placeholder for s in stats)
    all_dates: Counter[str] = Counter()
    for s in stats:
        all_dates.update(s.date_counts)

    for s in stats:
        if s.error:
            table.add_row(s.name, "[red]ERROR[/red]", "—", "—", f"[red]{s.error}[/red]")
            continue
        placeholder_cell = f"[yellow]{s.placeholder}[/yellow]" if s.placeholder else "0"
        mixed = len(s.date_counts) > 1
        dates_cell = format_dates(s.date_counts)
        if mixed:
            dates_cell = f"[yellow]{dates_cell}[/yellow]"
        table.add_row(
            s.name,
            str(s.total),
            str(s.populated),
            placeholder_cell,
            dates_cell,
        )

    table.columns[1].footer = str(total_sources)
    table.columns[2].footer = str(total_populated)
    table.columns[3].footer = (
        f"[yellow]{total_placeholder}[/yellow]" if total_placeholder else "0"
    )
    table.columns[4].footer = f"{len(all_dates)} distinct date(s)"
    return table


def main() -> int:
    """CLI entry point: scan the repo and print the status table."""
    parser = argparse.ArgumentParser(
        description=(
            "Report each <collection>/INDEX.xml: source count, populated vs "
            "PLACEHOLDER descriptions, and a tally of <curated_at> dates."
        ),
    )
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help=(
            f"repo root to scan for {COLLECTIONS_DIR}/*/INDEX.xml "
            "(default: repo containing this script)"
        ),
    )
    root: Path = parser.parse_args().root
    console = Console()

    indexes = find_indexes(root)
    if not indexes:
        console.print(f"[red]No {COLLECTIONS_DIR}/*/INDEX.xml found under {root}[/red]")
        return 1

    stats = [analyse_index(path) for path in indexes]
    console.print(build_table(stats))
    console.print(
        f"\n[dim]{len(stats)} collections scanned under {root}[/dim]",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
