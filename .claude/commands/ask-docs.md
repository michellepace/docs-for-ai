---
description: Query a local doc collection for a grounded answer.
disable-model-invocation: true
argument-hint: [collection] [question]
allowed-tools:
  - Bash(find *)
  - Bash(printf *)
  - Glob
  - Grep
  - mcp__firecrawl__firecrawl_scrape
  - mcp__firecrawl__firecrawl_search
  - Read
  - WebFetch
  - WebSearch
---

# Answer from a Doc Collection

Parse `$ARGUMENTS`:
- **collection** = the first word
- **question** = everything after the first word

Available collections: !`printf '<available_collections>\n'; find ~/.claude/docs-for-ai/collections -mindepth 1 -maxdepth 1 -type d -printf '%f\n'; printf '</available_collections>\n'`

Read the collection's `INDEX.xml` to route to the relevant local files, then give a grounded, cohesive answer to the question.

The collection follows this pattern:

<collection_pattern>

```text
~/.claude/docs-for-ai/collections/{collection}/
├── INDEX.xml       # Index of all docs
├── README.md
├── curated-doc.md  # Indexed doc
└── ...
```

`INDEX.xml` schema:

```xml
<docs_index>
  <source>
    <title>{use as routing signal}</title>
    <description>{use as routing signal}</description>
    <source_url>{URL}</source_url>
    <local_file>{file}</local_file>
  </source>
  <!-- Multiple <source> entries, one per curated doc file -->
</docs_index>
```

Local file: `~/.claude/docs-for-ai/collections/{collection}/{file}`

</collection_pattern>

## Procedure

1. **Read `INDEX.xml` first** — it's the authoritative manifest. Use each source's `<title>` and `<description>` to route.
2. **Analyse** the local files of the relevant sources `~/.claude/docs-for-ai/collections/{collection}/{file}`
3. **Answer** from those files, citing quotes. If they fall short, re-check the index for other relevant files, then **ask before any web fallback**.

If the question doesn't fit this collection, suggest a better-matching one from `<available_collections>` (or a web search) before answering.

## Web fallback (only after local docs are exhausted)

Prefer Firecrawl; use WebSearch / WebFetch (lossy on code/config) only if it's unavailable.

- **Known URL:** `firecrawl_scrape` (`formats: ["markdown"]`, `onlyMainContent: true`).
- **Discover the page:** `firecrawl_search` for ranked URLs (no `scrapeOptions` — inline scraping overflows), then `firecrawl_scrape` the 1–2 best hits.

## Response format

Use this as a guide:

<format>
# Question tersely framed

Grounded answer — well-structured and scannable, use emojis to aid readability

## References used

- Index: `~/.claude/docs-for-ai/collections/{collection}/INDEX.xml`
- `~/.claude/docs-for-ai/collections/{collection}/{file-1}`
- `~/.claude/docs-for-ai/collections/{collection}/{file-N}`
- `https://..` (Web fallback only)

</format>
