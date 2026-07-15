---
title: potential future refactors
updated: 2026-07-11
status: rough notes
---

## sync-index bug: 404-fetched-as-success

A dead URL that returns an HTTP-200 error page ("Page Not Found") is fetched, titled from that page, indexed, and reported as `✅ Success`. Nothing checks the body for not-found markers:

- direct route only catches HTTP-*status* 404 (`direct_fetch.fetch_text`)
- FireCrawl route only rejects *empty* content (`firecrawl_scrape`), taking the title verbatim from metadata

So the entry's title becomes the junk body title ("Page Not Found") — not anything correct. For the repro below (and any unconfigured host) that junk title comes from FireCrawl metadata; on the direct route it'd instead come from `extract_title`. A fix has to cover both paths.

**Fix** needs a content-validation heuristic — its own piece of work. Open question on detection: drop the entry from INDEX.xml, or keep it and just report? (INDEX.xml is the source of truth, so the file stays either way.)

Repro: `uv run curate-doc temp https://vercel.com/docs/evehhhhh`

## Test class markers

13 test classes each wrap a single function-under-test — the "one class per function" convention, no real grouping. Flatten them to module-level functions.

- located in `test_direct_fetch.py`, `test_firecrawl_scrape.py`, `test_paths.py`; 5 are single-method wrappers
- `TestFetchText` puts `@pytest.mark.direct_fetch` on the *class*, while the two module-level tests just below it in the same file tag the marker per-function — inconsistent; flatten it too

Principle: keep a class only where grouping genuinely clarifies intent, otherwise flatten.

## Refactor out TDD scaffolding (`tests/*.py`)

Leftover scaffolding to clean (inspiration: `docs-x/test-beck.md`, Kent Beck / sociable tests):

- `_forbid_scrape`/`_forbid_fetch` interaction guards (test_curate_doc.py, test_sync_index.py) assert HOW not WHAT — partly redundant with the output assertions
- boilerplate docstring in test_firecrawl_scrape.py ("Tests for parse_retry_seconds.")
- `set_index_description` + description-reader helpers duplicated across test_curate_doc.py and test_sync_index.py
- index-formatting assertions overlap between test_index_io.py and test_curate_doc.py

## Toml registry: readthedocs

readthedocs is a configured entry in `direct-fetch-rules.toml`; github is special-cased in `resolve_route` ahead of the toml loop. Idea: treat readthedocs like github (always direct-fetch, no config entry) to simplify the code.

**Caveat — not a clean equivalence.** github is recognised host-only (`is_github_url` netloc check, no config) and its transform reconstructs the `raw.githubusercontent.com` URL from owner/repo/ref/path. But `_readthedocs_route` needs the version-pinned `prefix` (`.../en/stable/`) to build its `_sources/*.rst.txt` twin, and that twin is a Sphinx-only artifact (MkDocs-on-RTD or source-links-disabled projects have none). Promoting readthedocs to an unconfigured host rule would **not** be behaviour-preserving — reconsider before doing it.
