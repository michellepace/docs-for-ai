---
title: potential future refactors (unvalidated / rough)
updated: 2026-07-03
---

## Test Markers

Current in pyproject.toml

```toml
# TESTING (PYTEST)
# =================================
[tool.pytest.ini_options]
markers = [
  "firecrawl: hits FireCrawl API (paid, network)",
  "github: hits raw.githubusercontent.com (free, network)",
  "readthedocs: hits rich.readthedocs.io (free, network)",
]
```

Wanted: Firecrawl, direct_fetch (validate for github)

## re_sync - extension agnostic

One thing stays true and is independent of this decision: sync_index.get_markdown_files globbing *.md only means /recurate-docs shiny and /recurate-docs biome would already drop their .qmd/.mdx entries as "stale (missing .md)". That's a pre-existing bug on the existing mixed-extension collections, not something the rich question introduces. Worth verifying and fixing on its own merits — but it's a separate errand from the .md-vs-.rst label, which I'd now leave alone.

## Class Markers

The user's principle is clear: don't keep classes to carry markers or to satisfy a "one class per function" convention — keep a class only where grouping genuinely clarifies intent, otherwise flatten. I'll apply that principle and finalise the plan.

## __init__

Do I need it?

- BASE_DIR `~/.claude/docs-for-ai/` glueing
- COLLECTION `~/.claude/docs-for-ai/`

## test_direct_source.py

Re-ogranise and rename. and remove duplication.

## Rename toml twins

markdown-twins
sphinx-rst-twins.. does it need to be sphinx?

## test_curate_doc.py

Doesn't seem right - test_allowlisted_suffixed_url_routes_to_firecrawl

bad organisation

## Tests in general

Behaviour "for me"

## GitHub → Toml registry→ raw-format fallback → FireCrawl

```
<scenarios>
## Curation Scenarios

Test each of these scenarios:
- firecrawl / direct fetch
- `<title>` value
- `<local_file>` value

(GitHub scenarios excluded)

### In .toml

How does this work currently
1. /curate-doc claudecode https://code.claude.com/docs/en/best-practices
2. /curate-doc claudecode https://code.claude.com/docs/en/best-practices.md

Current (proven - see `rich` collection)
3. /curate-doc rich https://rich.readthedocs.io/en/stable/tree.html
4. /curate-doc rich https://rich.readthedocs.io/en/stable/_sources/panel.rst.txt

### Not in .toml

1. /curate mintlify https://www.mintlify.com/docs/quickstart
2. /curate mintlify https://www.mintlify.com/docs/quickstart.md
3. /curate-doc collection https://example.com/hello.rst.txt

### I expect

If a prefix is in the .toml, it's honoured, so:
- (2) should work like (1)
- (4) should work like (3)

If URL is NOT in the `toml` AND ends in ".rst.txt" (7):
- direct fetch
- Unsure about `<title>` and `<local_file>`: ideally the same as (3)... depending on implementation complexity (reuse)
</scenarios>
```
