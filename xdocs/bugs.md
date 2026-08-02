---
title: Known bugs / issues
updated: 2026-08-02
status: both re-validated against current code and re-reproduced (2026-08-02) — still valid, unfixed
---

## 1. Error pages curate as "✅ Success" (still valid)

**Where:** fetch path — `curate_doc.fetch_document()` → `direct_fetch.fetch_text` / `firecrawl_scrape.scrape`.

**What happens:** a dead URL that returns an error page with **HTTP 200** (Vercel does this for `.md` twins) is fetched, written, indexed, and reported `🏁 Success! curated doc`, with `<curated_at>` refreshed unconditionally (in `curate_doc._add_or_update_source_in_index`). No content validation exists on either path — the only guards are a non-200 HTTP status (direct, in `direct_fetch.fetch_text`) and empty-content (firecrawl, in `firecrawl_scrape._perform_scrape`).

**Junk title, per route:** the `.md`-twin case is the *direct* route, so the title comes from `direct_fetch.extract_title(body)` — frontmatter → first H1 → URL-slug fallback. It reads `Page Not Found` only if the error body actually carries that H1/frontmatter; otherwise it degrades to a URL-derived slug. On the *firecrawl* route the title is the page's `<title>` metadata, so `Page Not Found` is guaranteed there. Either way a junk title is stored.

**Also via sync-index:** same entry point (`curate_doc.curate`, called from `sync_index._curate_or_error`); a recreated entry re-fetches the same error page and prints `ok` (in `sync_index._run_sync`).

**Repro (verified 2026-07-08, re-verified 2026-08-02 — byte-identical output):** `uv run curate-doc collections/vercel https://vercel.com/docs/this-page-does-not-exist-404-test` → `163 chars, direct`, `<title>Page Not Found</title>`, exit 0, `🏁 Success! curated doc`.

**Fix:** content-validation heuristic — suspicious titles ("Page Not Found", "404"), a minimum-length threshold, or per-site rules in `direct-fetch-rules.toml`. Must cover *both* fetch paths. Open question: drop the entry from INDEX.xml, or keep it and just report? (INDEX.xml is the source of truth, so the file stays either way.)

## 2. `update-descriptions` silently ignores an unrecognised filename (still valid)

**Where:** `update_descriptions.py`. Reached via `/curate-doc` Step 3 and `/recurate-docs`.

**What happens:** you pipe filename + description pairs; each is matched to an INDEX `<source>` by **exact** `<local_file>` (in `update_descriptions()` — plain dict-key match, no case/path normalisation). Word-count validation (20–30 words, in `_in_band_descriptions`) and entry-matching are separate passes that never talk. A filename matching no entry (typo, wrong case, stray suffix) is skipped with no message and no failure.

Note there are **two distinct `✅` lines**: `✅ <file>: N words` (word-count only, from `_in_band_descriptions`) and `✅ Updated: <file>` (an actual write, from `update_descriptions`). The per-line word-count ✅ says nothing about whether the file exists in the index — it only ever meant "word count is fine".

**Observed:**

- Lone typo → `✅ typo.md: 27 words`, then `no updates needed`, exit 0.
- Real file + typo → `🏁 Updated 1 description(s)`, exit 0; the typo vanishes without a trace.

**Why it's suspect (not really "by design"):** the `--help` epilog documents it — "Unmatched filenames are skipped without error." — but rests entirely on the happy-path assumption that Claude copies the filename verbatim from `curate-doc`'s `doc:` output line rather than typing it. The tell is the asymmetry *within the same tool*: an out-of-band word count is loud (❌ → `CurationError` → exit 1, raised through `main`), yet writing to a filename that isn't in the index is silent (exit 0). The more damaging failure is the quiet one.

**Fix:** print `⚠️ No INDEX entry for <file>: skipped` per unmatched filename, and exit 1 if any matched nothing — mirroring how word-count errors already behave. (Not implemented; `test_unmatched_filename_applies_nothing_and_succeeds` currently locks in the silent exit-0.)
