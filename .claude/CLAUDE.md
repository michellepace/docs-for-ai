# CLAUDE.md

**Ignore `xdocs/` unless I reference it** — personal notes, often stale.

## Overview

Curated documentation collections — fetched directly when possible, else scraped via FireCrawl. Each collection's INDEX.xml routes an LLM reader to the right doc (via `/ask-docs`).

```text
collections/
└── <collection>/           # eg. nextjs/, clerk/, uv/
    ├── INDEX.xml           # Targeted doc retrieval
    ├── README.md
    └── *.{md,rst,mdx,qmd}  # Curated doc files
```

`INDEX.xml` is written programmatically; only `<description>` is LLM-generated via user workflow. One `<source>` per curated doc file:

```xml
<docs_index>
  <source>
    <title>[curated source document title]</title>
    <description>[short description for LLM routing]</description>
    <source_url>[document source url]</source_url>
    <local_file>[curated doc filename]</local_file>
    <curated_at>YYYY-MM-DD</curated_at>
  </source>
  <!-- ...repeated per curated doc... -->
</docs_index>
```

User workflow (commands in `.claude/commands/`):

- `/curate-doc <collection> <url>`: curate doc into collection
- `/ask-docs <collection> <question>`: ask a question about a collection
- `/recurate-docs <collection>`: re-curate all docs & regenerate descriptions

## Test-Driven Development (TDD)

Failing test first (red → green), shaping the interface as you go. No bulk writing.

**Test the behaviour a caller depends on, not how the code produces it** — assert observable outputs and effects, so tests survive refactors and fail when real behaviour breaks.

- One behaviour per test (be pragmatic not perfect)
- Prefer pytest's `tmp_path` fixture over real files
- Self-documenting test names over docstrings

## Code Design Principles

Elegant and pragmatic choices; easy to maintain and comprehend for an AI coding agent.

- **Names reveal intent** — functions, tests, variables, classes alike; coherent across the codebase.
- **Focused functions and classes** — one responsibility each, kept small; compose, don't grow.
- **Types and structure over prose** — encode meaning in signatures and data shapes; docstrings only where names can't reach.

## Common Commands

```shell
# Entry points
uv run curate-doc --help          # Fetch a doc from a URL into a collection
uv run sync-index --help          # Re-sync a collection to its INDEX.xml
uv run update-descriptions --help # Pipe filename/description pair(s) into INDEX.xml

# Quality
uv run ruff check --fix           # Lint and auto-fix
uv run pyright                    # Type checking
uv run ruff format                # Format code
uv run pre-commit run --all-files # Run manually

# Run Tests
uv run pytest -m "not firecrawl"  # free suite: non-network + direct_fetch
uv run pytest -m direct_fetch     # just the free direct_fetch network tests
```
