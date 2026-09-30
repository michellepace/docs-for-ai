---
title: Known bugs / issues
updated: 2026-09-30
status: both re-reproduced 2026-09-30 — unfixed
---

## 1. Soft-404 error pages curate as success

**Where:** `curate_doc.fetch_document()` → `direct_fetch.fetch_text` / `firecrawl_scrape._perform_scrape`.

**What happens:** a site that serves its error page with **HTTP 200** gets fetched, written, indexed and reported `🏁 Success! curated doc`, exit 0. Nothing checks the content: the direct route only rejects a non-200 status, and FireCrawl only rejects empty markdown. `sync-index` goes through the same `curate_doc.curate` and prints `ok`.

**Repro (direct route, free):** `uv run curate-doc <scratch-dir> https://nextjs.org/docs/this-page-does-not-exist-404-test` gives `628 chars, direct`, `title: Page Not Found`, exit 0. Of the `direct-fetch-rules.toml` prefixes, only `nextjs.org/docs/` and `nextjs.org/blog/` still soft-404 (Vercel now returns a real 404).

**Fix:** add content validation that covers both routes, e.g. suspicious titles ("Page Not Found", "404") or a minimum length, and raise `CurationError` before anything is written. Still to decide: in `sync-index`, should an existing entry that now soft-404s be dropped from INDEX.xml, or kept and reported as `FAIL`?

## 2. `update-descriptions` silently skips an unmatched filename

**Where:** `update_descriptions.update_descriptions()`. Called in Step 3 of the `/curate-doc` and `/recurate-docs` skills.

**What happens:** each piped filename is matched to a `<source>` by exact `<local_file>`. A filename that matches nothing (typo, wrong case, a path) is skipped without any message. The word-count pass (`_in_band_descriptions`) still prints `✅ <file>: N words`, and that looks like success.

- Lone typo → `✅ typo.md: 10 words`, `no updates needed`, exit 0.
- Real file + typo → `🏁 Updated 1 description(s)`, exit 0; the typo is never mentioned.

An out-of-band word count is loud (`❌`, exit 1), but a description that went nowhere is silent. The `--help` epilog and `test_unmatched_filename_applies_nothing_and_succeeds` both lock in the silent exit 0.

**Fix:** print `⚠️ No INDEX entry for <file>: skipped` for each unmatched filename and exit 1 if there were any, the same way word-count errors behave. Update the epilog and flip that test.
