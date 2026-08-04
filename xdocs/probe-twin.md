# About `probe-md-twin.py`

> If I come back to this: can we simplify - if it returns and its got no 404 and is over 100 words. then its a twin. But I need to figure out, what exactly goes into the toml.

## The problem

`/curate-doc` direct-fetches a suffix-less page URL only when a prefix in
`direct-fetch-rules.toml` matches it. A site not yet in the TOML — every **new**
collection — is silently scraped via FireCrawl instead, even when it publishes a
perfectly good `.md` twin.

The fix is deterministic code **inside the curate-doc script**. Claude Code never sees
it, never decides anything about it, and the `/curate-doc` skill gains no instructions.
Its only visible effect is that the doc is direct-fetched rather than scraped, with a
validated prefix appended to the TOML on the way.

**This script is not that fix** — it establishes *which rules* such a check must apply.
Where the logic finally lives — `curate_doc.py`, `direct_fetch.py`, or a new module — is
undecided, to be settled against deep-module / one-module-one-thing criteria.

## What this script is

The 19 URLs aren't a feature — they're a corpus with known verdicts. Each is recorded
against the verdict it *should* produce, so a run either prints 19 ✓ or tells you a rule
changed or a host changed behaviour.

Every URL earns its place by being evidence of something. Don't "tidy" the sample — a
shortened corpus is a weakened one.

## The rules

Stop on first failure. The probe target for rules 2–5 is the URL with any trailing `/`
stripped, plus `.md`. **Title** means the body's first non-empty line with surrounding
`#` and spaces removed, matched case-insensitively.

Rule 4 additionally fetches a **control** — the same URL with its final path segment
replaced by `xxxCONTROLxxx` — to see what a miss looks like on that host. It runs only
after rules 1–3 pass, so the second request happens only for URLs that already look like
twins: 5 of the 19.

| rule | condition | verdict | printed reason |
| :--- | :--- | :--- | :--- |
| 1 | URL path has a file suffix — no request made | skipped | `url has path suffix` |
| 2 | request failed, or status != 200 | no twin | `fetch failed` / `status != 200` |
| 3 | media type is not `text/markdown` or `text/plain`, or body is empty, or body opens with `<` | no twin | `response is not markdown` |
| 4 | the control's twin is Markdown carrying the same title | no twin | `same title as control` / `control probe failed` |
| 5 | survived rules 2–4 | has twin | `markdown page served` |

**A false negative is cheaper than a false positive.** A missed twin costs one manual
curation. A false twin poisons `append-md` for an entire domain, and every later page
under that prefix is then trusted blindly. Hence default-reject.

## Why the rules are shaped this way

Each was forced by a real response. Re-verified 2026-08-02.

- **Rule 3 is an allowlist, not a "contains HTML" check.** `code.claude.com`,
  `docs.coderabbit.ai` and `docs.firecrawl.dev` answer with `application/json` holding a
  literal `null`. A blacklist waves through everything you failed to predict.
- **Rule 3 rejects an empty body, because the allowlist cannot catch a missing
  content-type.** `ui.shadcn.com` returns zero bytes and no content-type at all — and
  Python reports an absent header as `text/plain`, which the allowlist *accepts*.
  Emptiness is what stops it, not the media type.
- **Rule 3 also inspects the body, because a content-type header is not evidence.**
  `docs.marimo.io` serves 115KB of `<!doctype html>` under a `text/markdown` header.
- **Rule 3 accepts `text/plain`.** `react.dev/learn.md` returns `200 text/plain` carrying
  real frontmatter and real content, and `react.dev/learn` has no suffix, so rule 1 never
  skips it. Excluding `text/plain` rejected React's entire docs site.
- **Rule 4 measures the host instead of matching phrases.** A hardcoded `"404"` /
  `"not found"` list is a blacklist guarding the *expensive* direction: a host titling its
  stub "Oops" or "Seite nicht gefunden" sails through and poisons a whole domain. Asking
  the host what it serves for a known miss is language- and phrasing-independent.
- **Rule 4 compares titles, not bodies.** Byte comparison was tested and fails:
  `nextjs.org` echoes the requested path back in its stub, so a control and a mistyped
  URL are never byte-identical — they differ only by the length gap between the two path
  segments (604 vs 606 here) — while their titles match exactly.

## What the sample does not exercise

**Rule 3 decides nothing.** Every response that would fail it fails rule 2 first, so no
run prints `response is not markdown`. It is insurance, not a live filter — if
`docs.marimo.io` ever served that HTML under a 200, rule 3 is the only thing standing
between it and a false twin. Don't delete it because the output looks like it's unused.

The four `skipped` expectations are likewise tautological: rule 1 makes no request, so
they can only break if rule 1 itself changes.

Two limits of rule 4 are unproven either way, because no host in the sample behaves this
way:

- A stub that puts the requested path **in its title** would differ from the control's
  title and be accepted — a false positive, the expensive direction.
- A stub carrying frontmatter would have title `---`, colliding with every real page on
  that host and rejecting all of them — a false negative, the cheap direction.

## What the solution must do

**Trigger:** the point where `resolve_route` (`direct_fetch.py`) falls through to
`_firecrawl_route` — no TOML prefix matched, and the URL is neither a GitHub blob nor a
raw `.md`/`.rst.txt`. That covers a brand-new collection and an existing one curating from
a site not yet in the TOML.

**On a pass:** write the URL's first path segment as the prefix, else the host root —
`docs.mobbin.com/mcp/introduction` → `https://docs.mobbin.com/mcp/`.

Two facts make the gap concrete:

- `direct_fetch.fetch_text` accepts **any** 200 — no content-type check, no body check.
- `nextjs.org` and `vercel.com` are already in `append-md`, and both answer an absent
  twin with `200 text/markdown`.

So today, `/curate-doc nextjs <mistyped-url>` writes a "Page Not Found" stub into the
collection and indexes it as a real doc. Rule 4-by-control is what closes that.

Rule 1 duplicates the existing `direct_fetch._has_no_file_suffix` and should reuse it
wherever the logic lands; the two differ today on dotfile-style segments.

Whatever gets built stays proportionate — this bites roughly once a month. No new
dependencies and no new config surfaces.

## Open

- `docs.mobbin.com` is a verified twin and a positive control here, but still isn't in
  `direct-fetch-rules.toml`.

## probe-md-twin.py

This code was in `src/docs_for_ai/probe-md-twin.py`. But the entire idea just seemed to continually explode into more complexity. So I've just pasted it here rather, for later. Maybe for later, and maybe not.

<code>

```python
# ruff: noqa: N999  hyphenated name: a script to run, not a module to import
"""Probe sample urls for a Markdown twin and print each verdict.

Groundwork only. These rules belong in the curate-doc script as deterministic
code, never as `/curate-doc` skill instructions: a validated twin earns its
prefix a `direct-fetch-rules.toml` entry, and the url is direct-fetched
instead of scraped.
"""

import urllib.error
import urllib.request
from enum import StrEnum
from pathlib import Path
from typing import NamedTuple
from urllib.parse import urlparse, urlunparse

from docs_for_ai.direct_fetch import USER_AGENT

REQUEST_TIMEOUT_SECONDS = 20
HTTP_OK = 200

MARKDOWN_MEDIA_TYPES = frozenset({"text/markdown", "text/plain"})
# Names a sibling page that cannot exist, to see what a miss looks like on this host.
CONTROL_SEGMENT = "xxxCONTROLxxx"


class Verdict(StrEnum):
    """What the rule chain concluded about a url's Markdown twin."""

    TWIN = "has twin"
    NO_TWIN = "no twin"
    SKIPPED = "skipped"


# `xxxBREAKxxx` names a page that does not exist on an otherwise real docs site.
SAMPLE_URLS_BY_EXPECTED_VERDICT = {
    Verdict.TWIN: (
        "https://clerk.com/docs/reference/objects/user",
        "https://docs.mobbin.com/mcp/introduction",
        "https://react.dev/learn",
    ),
    Verdict.NO_TWIN: (
        "https://code.claude.com/docs/en/xxxBREAKxxx",
        "https://docs.coderabbit.ai/cli/xxxBREAKxxx",
        "https://docs.convex.dev/ai/xxxBREAKxxx",
        "https://docs.firecrawl.dev/sdks/xxxBREAKxxx",
        "https://docs.marimo.io/xxxBREAKxxx",
        "https://nextjs.org/docs/pages/getting-started/xxxBREAKxxx",
        "https://platform.claude.com/docs/en/build-with-claude/xxxBREAKxxx",
        "https://tailwindcss.com/docs/box-shadow",
        "https://tailwindcss.com/plus/ui-blocks/application-ui/navigation/navbars",
        "https://ui.shadcn.com/docs/xxxBREAKxxx",
        "https://vercel.com/docs/agent-resources/xxxBREAKxxx",
        "https://vitest.dev/guide/browser/xxxBREAKxxx",
    ),
    Verdict.SKIPPED: (
        "https://github.com/astral-sh/uv/blob/main/docs/guides/integration/dependabot.md",
        "https://github.com/biomejs/website/blob/main/src/content/docs/reference/vscode.mdx",
        "https://mdformat.readthedocs.io/en/stable/users/style.html",
        "https://ui.shadcn.com/llms.txt",
    ),
}


class Outcome(NamedTuple):
    """A verdict, the rule that decided it, and what that rule saw."""

    verdict: Verdict
    rule: int
    reason: str


class Response(NamedTuple):
    """The parts of a response the rules care about."""

    status: int
    media_type: str
    body: str


def _has_path_suffix(url: str) -> bool:
    return bool(Path(urlparse(url).path).suffix)


def _twin_url(url: str) -> str:
    return f"{url.rstrip('/')}.md"


def _control_url(url: str) -> str:
    """`url`'s sibling that cannot exist — whatever a miss looks like on this host."""
    parsed = urlparse(url.rstrip("/"))
    parent = parsed.path.rsplit("/", 1)[0]
    return urlunparse(parsed._replace(path=f"{parent}/{CONTROL_SEGMENT}"))


def _fetch(url: str) -> Response | None:
    """Fetch `url` (following redirects); None when the request itself fails."""
    # S310: probe URLs are the fixed sample above
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})  # noqa: S310
    try:
        with urllib.request.urlopen(  # noqa: S310
            request, timeout=REQUEST_TIMEOUT_SECONDS
        ) as response:
            return Response(
                status=response.status,
                media_type=response.headers.get_content_type(),
                body=response.read().decode("utf-8", errors="replace"),
            )
    except urllib.error.HTTPError as exc:
        return Response(status=exc.code, media_type="", body="")
    except OSError:
        return None


def _title_line(body: str) -> str:
    for line in body.splitlines():
        if title := line.strip(" #"):
            return title.casefold()
    return ""


def _is_markdown(response: Response) -> bool:
    body = response.body.lstrip()
    return response.media_type in MARKDOWN_MEDIA_TYPES and bool(body) and body[0] != "<"


def _markdown_failure(response: Response) -> Outcome | None:
    """Why `response` is not a served Markdown page (rules 2-3); None when it is."""
    if response.status != HTTP_OK:
        return Outcome(Verdict.NO_TWIN, 2, "status != 200")
    if not _is_markdown(response):
        return Outcome(Verdict.NO_TWIN, 3, "response is not markdown")
    return None


def _classify(url: str) -> Outcome:
    if _has_path_suffix(url):
        return Outcome(Verdict.SKIPPED, 1, "url has path suffix")

    twin = _fetch(_twin_url(url))
    if twin is None:
        return Outcome(Verdict.NO_TWIN, 2, "fetch failed")
    if failure := _markdown_failure(twin):
        return failure

    # A host that answers a miss with Markdown makes the response above no evidence.
    control = _fetch(_twin_url(_control_url(url)))
    if control is None:
        return Outcome(Verdict.NO_TWIN, 4, "control probe failed")
    control_serves_markdown = _markdown_failure(control) is None
    if control_serves_markdown and _title_line(control.body) == _title_line(twin.body):
        return Outcome(Verdict.NO_TWIN, 4, "same title as control")
    return Outcome(Verdict.TWIN, 5, "markdown page served")


def _result_line(url: str, expected: Verdict, outcome: Outcome) -> str:
    as_expected = outcome.verdict == expected
    marker = "✓" if as_expected else "✗"
    surprise = "" if as_expected else f"  (expected {expected})"
    return (
        f"{marker} {outcome.verdict:<10}rule {outcome.rule}  "
        f"{outcome.reason:<26}{url}{surprise}"
    )


def main() -> None:
    """Run the twin-detection rules over the sample and print each verdict."""
    for expected, urls in SAMPLE_URLS_BY_EXPECTED_VERDICT.items():
        for url in urls:
            print(_result_line(url, expected, _classify(url)))


if __name__ == "__main__":
    main()
```

</code>
