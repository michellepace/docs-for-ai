---
title: potential future refactors
updated: 2026-09-30
status: rough notes
---

## Flatten the test classes

The `class Test…` groups in `test_direct_fetch.py`, `test_firecrawl_scrape.py` and `test_paths.py` are namespaces with no fixtures or shared state. Flatten them to module-level functions like the other test files (`grep -n "^class Test" tests/*.py`). Keep any class that has picked up real shared state since this was written.

- **Duplicate names shadow silently.** `test_resolves_title` exists in both `TestExtractMarkdownTitle` and `TestExtractRstTitle`. Check that `uv run pytest --collect-only -q | tail -1` gives the same count before and after.
- **Rename as you flatten.** Each name must carry its subject once the class is gone (e.g. `test_classifies_url`). Fold any class docstring that states a contract into the test names; drop boilerplate ones like `"""Tests for parse_retry_seconds."""`.
- **Move markers onto functions.** Put `TestFetchText`'s class-level `@pytest.mark.direct_fetch` on each test function, as the rest of that file already does.
