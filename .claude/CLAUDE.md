# CLAUDE.md

Curated documentation collections — fetched directly when possible, else scraped via FireCrawl. Each collection's INDEX.xml routes an LLM reader to the right doc (via `/ask-docs`).

```text
collections/
└── <collection>/           # eg. nextjs/, clerk/, uv/
    ├── INDEX.xml
    ├── README.md
    └── *.{md,mdx,qmd,txt}  # Curated doc files
```

Every collection's `INDEX.xml` follows this exact schema, each leaf element on one line:

```xml
<docs_index>
  <source>
    <title>[curated source document title]</title>
    <description>[routing signal an LLM uses to pick this file]</description>
    <source_url>[document source url]</source_url>
    <local_file>[curated doc filename]</local_file>
    <curated_at>YYYY-MM-DD</curated_at>
  </source>
  <!-- One <source> entry per curated doc file -->
</docs_index>
```

## Workflows

Skills (`.claude/skills/`), invoked by the user:

- `/curate-doc <collection> <url>`: curate doc into a collection
- `/ask-docs <collection> <question>`: ask a question about a collection
- `/recurate-docs <collection>`: re-curate all docs & regenerate descriptions

CLIs, run directly or called by the skills above:

```shell
uv run curate-doc --help          # Fetch a doc from a URL into a collection
uv run sync-index --help          # Re-sync a collection to its INDEX.xml
uv run update-descriptions --help # Pipe filename/description pairs into INDEX.xml
```

## Development

### Code Design

Elegant and pragmatic choices; easy to maintain and comprehend for an AI coding agent.

- **Names reveal intent** — functions, tests, variables, classes alike; coherent across the codebase
- **Focused functions and classes** — one responsibility each, kept small; compose, don't grow
- **Types and structure over prose** — encode meaning in signatures and data shapes; docstrings only where names can't reach

### Testing (TDD)

Failing test first (red → green), shaping the interface as you go. No bulk writing.

**Test the behaviour a caller depends on, not how the code produces it** — assert observable outputs and effects, so tests survive refactors and fail when real behaviour breaks.

- One behaviour per test (be pragmatic not perfect)
- Prefer pytest's `tmp_path` fixture over real files
- Self-documenting test names over docstrings

### Commands

```shell
uv run pre-commit run --all-files # ruff, pyright, free tests, linters

uv run pytest -m "not firecrawl"  # default, runs on pre-commit
uv run pytest -m firecrawl        # paid
uv run pytest                     # runs on pre-push
```

## Rules

- Never run firecrawl tests unless asked — paid API
- Never hand-edit `INDEX.xml` — the CLIs above write it
- Ignore `xdocs/` unless I reference it — personal notes, often stale
