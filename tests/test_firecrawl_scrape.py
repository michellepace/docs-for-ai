"""FireCrawl scrape path: offline helpers (retry parsing, missing-key guard)."""

import pytest
from firecrawl.v2.utils.error_handler import RateLimitError

from docs_for_ai.errors import CurationError
from docs_for_ai.firecrawl_scrape import _get_firecrawl_client, parse_retry_seconds


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


class TestGetFirecrawlClient:
    """The client guards on the API key before any network use."""

    def test_missing_api_key_raises_naming_the_variable(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """No API key raises, naming the variable to set (no client built)."""
        monkeypatch.delenv("API_KEY_MCP_FIRECRAWL", raising=False)

        with pytest.raises(
            CurationError, match="Missing API key: set API_KEY_MCP_FIRECRAWL"
        ):
            _get_firecrawl_client()
