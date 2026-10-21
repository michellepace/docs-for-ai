"""Reuse the summary a trusted publisher puts atop its doc as the INDEX description."""

import re

from docs_for_ai.direct_fetch import split_frontmatter

# Anthropic only: other publishers' summaries are too generic to route by.
TRUSTED_SUMMARY_SITES = (
    "https://claude.com/docs/",
    "https://code.claude.com/docs/",
    "https://platform.claude.com/docs/",
)
FRONTMATTER_DESCRIPTION_RE = re.compile(
    r"^description:[ \t]*(?P<val>.*)$", re.MULTILINE
)


def _frontmatter_description(frontmatter: str) -> str | None:
    match = FRONTMATTER_DESCRIPTION_RE.search(frontmatter)
    value = match.group("val").strip().strip("\"'") if match else ""
    return value or None


def _summary_line_under_h1(body: str) -> str | None:
    lines = iter(body.splitlines())
    for line in lines:
        if line.startswith("# "):
            next_line = next((rest for rest in lines if rest.strip()), "")
            return next_line[2:].strip() if next_line.startswith("> ") else None
    return None


def publisher_summary(content: str, source_url: str) -> str | None:
    """Summary line a trusted site publishes atop its doc, if any."""
    if not source_url.startswith(TRUSTED_SUMMARY_SITES):
        return None
    frontmatter, body = split_frontmatter(content)
    return _frontmatter_description(frontmatter) or _summary_line_under_h1(body)
