"""Shared curation failure; CLIs catch it, print a `❌ …` line, and exit 1."""


class CurationError(Exception):
    """A curation failure whose message the CLI prints as a `❌ …` line."""
