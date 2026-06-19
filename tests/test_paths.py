"""Tests for paths.py."""

from pathlib import Path
from typing import TYPE_CHECKING

from docs_for_ai.paths import format_path_for_display

if TYPE_CHECKING:
    import pytest


class TestFormatPathForDisplay:
    """Display paths are absolute (CWD-independent) with $HOME collapsed to `~`."""

    def test_collapses_home_to_tilde(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A path under $HOME renders as `~/...`, regardless of the caller's CWD."""
        home = tmp_path.resolve()
        monkeypatch.setattr(Path, "home", lambda: home)

        target = home / "projects" / "repo" / "collections" / "x" / "y.md"

        assert format_path_for_display(target) == "~/projects/repo/collections/x/y.md"

    def test_outside_home_returns_absolute(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A path outside $HOME renders as the absolute resolved path, no `~`."""
        home = (tmp_path / "home").resolve()
        home.mkdir()
        monkeypatch.setattr(Path, "home", lambda: home)

        target = tmp_path / "elsewhere" / "file.md"

        result = format_path_for_display(target)
        assert result == str(target.resolve())
        assert "~" not in result
