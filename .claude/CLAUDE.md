# CLAUDE.md

## Overview

Curated documentation collections — fetched directly when possible, else scraped via FireCrawl. Each collection's INDEX.xml routes an LLM reader to the right doc (via `/ask-docs`).

```text
collections/
└── <collection>/       # eg. nextjs/, clerk/, uv/
    ├── INDEX.xml       # Targeted doc retrieval
    ├── README.md       # Directory overview
    └── *.md            # Curated doc files
```

Consistent `INDEX.xml` schema (one `<source>` per curated `.md` file):

```xml
<docs_index>
  <source>
    <title>[curated source document title]</title>
    <description>[short description for LLM routing]</description>
    <source_url>[document source url]</source_url>
    <local_file>[curated .md filename]</local_file>
    <curated_at>YYYY-MM-DD</curated_at>
  </source>
  <!-- ...repeated per curated doc... -->
</docs_index>
```

User workflow (commands in `.claude/commands/`):
- `/curate-doc <collection> <url>`: curate doc into collection
- `/ask-docs <collection> <question>`: ask a question about a collection
- `/recurate-docs <collection>`: re-curate all docs & regenerate descriptions

## Code Design Principles

TDD-driven — write the test first; let testability shape the design.
- **Pure functions preferred** — no side effects in business logic
- **Single responsibility** — one module, one purpose (one script, one job)
- **Layer separation** — CLI entry point → core logic → I/O
- **Self-documenting code** — clear naming throughout, minimal docstrings
- **Fail loud at the I/O boundary** — print `❌ Error:` / `✅` progress; so Claude can key off them.

## TDD Development

Write a failing test (red) → code → pass (green).
- Test behaviour; not implementation or Python itself
- One test → one behaviour → minimal code → repeat. No bulk-writing tests.
- Use pytest's `tmp_path` fixture instead of creating real files
- Use self-documenting test names

## Common Commands

```shell
uv tree                           # Show dependency tree
uv add --dev <pkg>                # Add dev dependency
uv lock --upgrade && uv sync      # Update all packages and apply

# Quality (see pyproject.toml)
uv run ruff check --fix           # Lint and auto-fix
uv run pyright                    # Type checking
uv run ruff format                # Format code
uv run pre-commit run --all-files # Run pre-commit hooks manually

# Run Non-Network Tests (see pyproject.toml)
uv run pytest -m "not firecrawl and not github"
```
