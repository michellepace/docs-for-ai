"""Tests for firecrawl_source.py.

Only the offline retry-parsing helper is unit-tested here; the network scrape
path is covered end-to-end by the FireCrawl-marked tests in test_curate_doc.py.
"""

from firecrawl.v2.utils.error_handler import RateLimitError

from scripts.firecrawl_source import parse_retry_seconds


class TestParseRetrySeconds:
    """Tests for parse_retry_seconds."""

    def test_parses_seconds_from_message(self) -> None:
        """A 'retry after Ns' message yields N."""
        error = RateLimitError("Rate limit exceeded. Retry after 30s.")
        assert parse_retry_seconds(error) == 30

    def test_defaults_to_60_when_absent(self) -> None:
        """No retry-after pattern falls back to the per-minute default of 60."""
        error = RateLimitError("Rate limit exceeded.")
        assert parse_retry_seconds(error) == 60
