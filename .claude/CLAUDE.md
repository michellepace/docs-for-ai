# CLAUDE.md

## Overview

Documentation collections scraped via FireCrawl Python SDK. The collection/INDEX.xml is a routing signal that an LLM reader uses for targeted context retrieval.

Documentation is organised by tool/framework in collection directories:

```text
<collection>/
├── INDEX.xml       # Structured index for targeted doc retrieval
├── README.md       # Directory overview
└── *.md            # Curated doc files
```

Workflow is driven by slash commands in `.claude/commands/`:

- `/curate-doc <collection> <url>` — curate a source URL into a collection
- `/ask-docs <collection> <question>` — query a collection to answer a question
- `/improve-index-xml <collection>` — refine INDEX.xml descriptions for LLM reader routing
- `/rescrape-docs <collection>` — re-scrape all docs & regenerate descriptions

## Code Design Principles

TDD-driven — write the test first; let testability shape the design.

- **Pure functions preferred** — no side effects in business logic
- **Single responsibility** — one module, one purpose (one script, one job)
- **Layer separation** — CLI entry point → core logic → I/O
- **Fail loud at the I/O boundary** — print `❌ Error: TYPE|detail|url|` then `sys.exit(1)`; print `✅ ...` key progress. Slash commands key off these.

## TDD Development

Write a failing test (red) → code → pass (green).

- Write the test first; one test drives one behaviour
- Use pytest's `tmp_path` fixture instead of creating real files
- Use focused, descriptive test names

## Development Workflow (Python 3.14)

**Package Management:** `https://docs.astral.sh/uv/`

**Strict Rules:**

- Use British spelling - never American
- Use `uv run` - never activate venv
- Use `uv add` - never pip
- Use `pyproject.toml` - never requirements.txt

**Common Commands:**

```bash
# Setup & Dependencies
uv sync                           # Match packages to lockfile
uv tree                           # Show dependency tree
uv add --dev <pkg>                # Add dev dependency
uv lock --upgrade-package <pkg>   # Update specific package
uv lock --upgrade && uv sync      # Update all packages and apply

# Code Quality (see pyproject.toml)
uv run ruff check --fix           # Lint and auto-fix
uv run pyright                    # Type checking
uv run ruff format                # Format code
uv run pre-commit run --all-files # Run all hooks manually

# Run Non-Network Tests (markers in pyproject.toml)
uv run pytest -m "not firecrawl and not github"

# Markdown (.markdownlint-cli2.yaml)
npx markdownlint-cli2 --fix "filename.md"  # Lint and auto-fix
```
