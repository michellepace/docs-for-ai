"""FireCrawl scrape path, dispatched from curate-doc orchestrator."""

import re
import time
import warnings
from os import environ

from docs_for_ai.errors import CurationError

# Mute upstream firecrawl pydantic field-shadow warning.
with warnings.catch_warnings():
    warnings.filterwarnings(
        "ignore",
        message='Field name "json" .* shadows an attribute in parent',
        category=UserWarning,
    )
    from firecrawl import Firecrawl
    from firecrawl.v2.utils.error_handler import (
        FirecrawlError,
        RateLimitError,
    )


def _get_firecrawl_client() -> Firecrawl:
    """Get Firecrawl client with API key from environment."""
    api_key = environ.get("API_KEY_MCP_FIRECRAWL")
    if not api_key:
        msg = "Missing API key: set API_KEY_MCP_FIRECRAWL"
        raise CurationError(msg)
    return Firecrawl(api_key=api_key)


def parse_retry_seconds(error: RateLimitError) -> int:
    """Parse retry-after seconds from rate limit error message."""
    retry_match = re.search(r"retry after (\d+)s", str(error), re.IGNORECASE)
    if retry_match:
        return int(retry_match.group(1))
    # Default to 60s if pattern not found (rate limit window is per minute)
    return 60


def _perform_scrape(firecrawl: Firecrawl, url: str) -> tuple[str, str]:
    """Make one Firecrawl scrape call and return `(markdown, title)`."""
    result = firecrawl.scrape(
        url,
        formats=["markdown"],
        only_main_content=True,  # Excl. nav menu, footer, sidebars, etc.
        remove_base64_images=True,  # Removes base64 strings (keeps alt text)
        wait_for=3000,  # Wait to capture dynamic content (3 seconds)
        max_age=86400000,  # Use cached content for speed (24 hours)
    )

    if not result or not result.markdown:
        msg = f"No content scraped: {url}"
        raise CurationError(msg)

    title = "Untitled"
    if result.metadata:
        title = getattr(result.metadata, "title", "Untitled")
    print(f"✅ Scraped: {len(result.markdown):,} chars")
    return result.markdown, title


def scrape(url: str, max_attempts: int = 2) -> tuple[str, str]:
    """Scrape URL via the Firecrawl SDK, returning `(markdown, title)`.

    Retries on `RateLimitError` for the retry-after duration + buffer
    """
    firecrawl = _get_firecrawl_client()

    for attempt in range(max_attempts):
        try:
            return _perform_scrape(firecrawl, url)

        except CurationError:
            # Already a structured failure (e.g. empty content) — don't re-wrap
            raise

        except RateLimitError as e:
            if attempt < max_attempts - 1:
                wait_time = parse_retry_seconds(e) + 2  # Add 2s safety buffer
                print(f"⏳ Rate limited: retrying in {wait_time}s")
                time.sleep(wait_time)
                continue

            # Final attempt exhausted
            msg = f"Rate limited: no content after {max_attempts} attempts — {url}"
            raise CurationError(msg) from e

        except FirecrawlError as e:
            # All other Firecrawl API errors
            msg = f"Firecrawl error: {e} — {url}"
            raise CurationError(msg) from e

        except OSError as e:
            # Network/connection failures (timeouts, DNS errors, etc.)
            msg = f"Network error: {e} — {url}"
            raise CurationError(msg) from e

        except Exception as e:
            # Unexpected errors (ValueError, RuntimeError, SDK bugs, etc.)
            msg = f"Unexpected error: {type(e).__name__}: {e} — {url}"
            raise CurationError(msg) from e

    # Defensive fallback (unreachable in normal execution)
    msg = f"Network error: failed after {max_attempts} attempts — {url}"
    raise CurationError(msg)
