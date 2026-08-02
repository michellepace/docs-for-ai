---
title: potential future refactors
updated: 2026-08-02
status: rough notes
---

## Flatten the test classes

The test classes are one-per-function-under-test — namespaces, not groupings. Flatten to module-level functions: drops a layer that scopes nothing, makes the marker convention uniform, and forces each name to carry its own subject. Every other test file is already flat.

Find them: `grep -n "^class Test" tests/*.py`. As of 2026-08-02: 13, in `test_direct_fetch.py`, `test_firecrawl_scrape.py`, `test_paths.py`.

- **Premise to re-check:** these are empty shells (no fixtures, setup, attributes, inheritance). Keep any class that has since grown real shared state.
- **Duplicate method names collide silently** — sibling classes can share a method name (`test_resolves_title` did), and de-indenting makes the second shadow the first with no error. Gate on `uv run pytest --collect-only -q | tail -1` matching before and after.
- **Rename as you flatten.** `test_classifies_url` is only legible under its class; at module level it must name its subject. Fold contract-bearing class docstrings into the names.
- Class-level `@pytest.mark.direct_fetch` becomes per-function — matching what the same file already does below it.
- **Takes a boilerplate docstring with it:** `TestParseRetrySeconds`'s `"""Tests for parse_retry_seconds."""` (test_firecrawl_scrape.py) names the code, not a behaviour — it dies with the class, no separate cleanup needed.

## Toml registry: readthedocs

readthedocs is a configured entry in `direct-fetch-rules.toml`; github is special-cased in `resolve_route` ahead of the toml loop. Idea: treat readthedocs like github (always direct-fetch, no config entry) to simplify the code.

**Caveat — not a clean equivalence.** github is recognised host-only (`is_github_url` netloc check, no config) and its transform reconstructs the `raw.githubusercontent.com` URL from owner/repo/ref/path. But `_readthedocs_route` needs the version-pinned `prefix` (`.../en/stable/`) to build its `_sources/*.rst.txt` twin, and that twin is a Sphinx-only artifact (source-links-disabled or MkDocs-on-RTD projects have none). Promoting readthedocs to an unconfigured host rule would **not** be behaviour-preserving.

**Settled — don't do it (2026-08-02).** `black.readthedocs.io` and `pip.readthedocs.io` serve `.html` pages whose `_sources` twin 404s. Unprefixed today, they reach FireCrawl and scrape fine; under a host-only rule `_readthedocs_route` claims them and curate-doc dies on `Fetch failed: 404 not found`.

- **The breaking class is Sphinx built with `html_copy_source = False`, not MkDocs** — MkDocs pretty-URLs carry no `.html`, so `_readthedocs_route` declines them anyway.
- **Little is saved:** one TOML prefix, versus deriving `/en/<ver>/` from URL shape — which single-version RTD projects don't expose.
