---
description: Query curated documentation collection directory to answer the question.
argument-hint: <collection> <question>
allowed-tools:
  - Bash(sed *)
  - Glob
  - Grep
  - mcp__firecrawl__firecrawl_scrape
  - mcp__firecrawl__firecrawl_search
  - Read
  - WebFetch
  - WebSearch
---

# Query Documentation Collection

Split `$ARGUMENTS`: the first word is the **collection**, the rest is the **question**.

## Locations

- Index: `~/projects/python/docs-for-ai/<collection>/INDEX.xml`
- Directory: `~/projects/python/docs-for-ai/<collection>/`
- Fallbacks (run): `sed -n '/## 📦 Repo Collections/,/^---$/{/^|/p}' ~/projects/python/docs-for-ai/README.md`

## Task

1. Read the index and match the question to the relevant local file(s).

2. **If relevant files exist:** answer from them, citing file paths and quotes. If they fall short, say so and ask before going to the web.

3. **If nothing relevant:** check whether the collection even fits the question. Consult the fallbacks and propose a next step (another collection, or a web search).

4. **If the collection doesn't exist:** show available collections.

## Web fallback

Only after exhausting local docs. Prefer Firecrawl; fall back to WebSearch / WebFetch (lossy on code/config) only if it's unavailable.

- **Known URL:** `firecrawl_scrape` (`formats: ["markdown"]`, `onlyMainContent: true`).
- **Need to discover the page:** `firecrawl_search` for ranked URLs (no `scrapeOptions` — inline scraping overflows), then `firecrawl_scrape` the 1–2 best hits.

## Response Format

1. **Source:** local files (which) or web (which URLs).
2. **Answer:** a comprehensive answer to the question.
3. **References:** file paths with line numbers, or URLs.

## Rules

- Prefer local docs; be explicit about local vs web.
- Use the exact locations above — no variations.
