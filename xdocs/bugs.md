---
title: Known bugs / issues
updated: 2026-09-30
status: all re-reproduced 2026-09-30 — unfixed
---

## 1. Soft-404 error pages curate as success

**Where:** `curate_doc.fetch_document()` → `direct_fetch.fetch_text` / `firecrawl_scrape._perform_scrape`.

**What happens:** a site that serves its error page with **HTTP 200** gets fetched, written, indexed and reported `🏁 Success! curated doc`, exit 0. Nothing checks the content: the direct route only rejects a non-200 status, and FireCrawl only rejects empty markdown. `sync-index` goes through the same `curate_doc.curate` and prints `ok`.

**Repro (direct route, free):** `uv run curate-doc <scratch-dir> https://nextjs.org/docs/this-page-does-not-exist-404-test` gives `title: Page Not Found`, exit 0. If Next.js starts returning a real 404, look for another soft-404 host by requesting a made-up page under each `direct-fetch-rules.toml` prefix and checking for HTTP 200.

**Fix:** validate content on both routes and raise `CurationError` before anything is written. Two options:

- **Heuristic:** reject suspicious titles ("Page Not Found", "404") or very short bodies. Free, but it depends on the language and phrasing of each site's error page.
- **Control fetch:** also fetch a sibling that can't exist (last path segment → `xxxCONTROLxxx`). If that returns 200 with the same title, the page is the host's soft-404. This doesn't depend on wording, but every curate costs a second fetch, and on the FireCrawl route that fetch is paid.

Open question: in `sync-index`, should an existing entry that now soft-404s be dropped from INDEX.xml, or kept and reported as `FAIL`?

## 2. `update-descriptions` silently skips an unmatched filename

**Where:** `update_descriptions.update_descriptions()`. Called by the `/curate-doc` and `/recurate-docs` skills when they write descriptions.

**What happens:** each piped filename is matched to a `<source>` by exact `<local_file>`. A filename that matches nothing (typo, wrong case, a path) is skipped without any message. The word-count pass (`_in_band_descriptions`) still prints `✅ <file>: N words`, and that looks like success.

- Lone typo → `✅ typo.md: 10 words`, `no updates needed`, exit 0.
- Real file + typo → `🏁 Updated 1 description(s)`, exit 0; the typo is never mentioned.

An out-of-band word count is loud (`❌`, exit 1), but a description that went nowhere is silent. The `--help` epilog and `test_unmatched_filename_applies_nothing_and_succeeds` both lock in the silent exit 0.

**Fix:** print `⚠️ No INDEX entry for <file>: skipped` for each unmatched filename and exit 1 if there were any, the same way word-count errors behave. Update the epilog and flip that test.

## 3. A host-root rule prefix appends `.md` to the hostname

**Where:** `direct_fetch._append_md_route()`.

**What happens:** when a rule prefix is a bare host, curating its root URL fetches `<host>.md`, which is a different domain under Moldova's `.md` TLD. `https://docs.convex.dev/` → `https://docs.convex.dev.md`. Those hosts resolve to an unrelated server; today TLS fails, so the curate errors, but it still contacts that server. Path prefixes are fine (`https://clerk.com/docs/` → `https://clerk.com/docs.md`, HTTP 200).

Affected prefixes: `docs.coderabbit.ai`, `docs.convex.dev`, `docs.firecrawl.dev`, `docs.marimo.io`, `modelcontextprotocol.io`.

**Repro (free, no network):** `uv run python -c "from docs_for_ai.direct_fetch import *; print(resolve_route('https://docs.convex.dev/', load_direct_fetch_rules()).fetch_url)"`

**Fix:** `_append_md_route` declines a URL with an empty path, so a host root falls through to FireCrawl (or `/index.md` once per-site suffixes land, see `ideas.md`).

## 4. A mis-cased URL misses its rule and pays for FireCrawl

**Where:** `direct_fetch._matches_prefix()`.

**What happens:** prefix matching is case-sensitive, so `https://NextJS.org/Docs/app/…` matches no rule and is scraped via FireCrawl (paid) instead of direct-fetched. Nothing says why.

**Fix:** lowercase the scheme and host before matching. Leave the path alone, because servers treat path case as significant (a mis-cased path should fail, not be silently corrected).
