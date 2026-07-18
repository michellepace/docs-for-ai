---
description: Get a grounded answer against a doc collection.
disable-model-invocation: true
argument-hint: "[collection] \"your question\""
allowed-tools:
  - Bash(find *)
  - Bash(printf *)
  - Glob
  - Grep
  - mcp__firecrawl__firecrawl_scrape
  - mcp__firecrawl__firecrawl_search
  - mcp__firecrawl__firecrawl_search_feedback
  - Read
  - WebFetch
  - WebSearch
---

# Answer from a Doc Collection

Your task is to provide a grounded answer to a user's question against the applicable curated documentation collection.

Available collections: !`printf '<available_collections>\n'; find ~/.claude/docs-for-ai/collections -mindepth 1 -maxdepth 1 -type d -printf '%f\n'; printf '</available_collections>\n'`

## Step 1. Parse Arguments

Parse `$ARGUMENTS`: **collection** = first word, **question** = everything after.

If the question clearly belongs to another collection from `<available_collections>` (or only the web can answer it), halt to confirm a sensible alternative — use "🤔 ..." for visibility.

## Step 2. Research a grounded answer

1. Read `~/.claude/docs-for-ai/collections/{collection}/INDEX.xml` — the authoritative manifest. Route by each source's `<title>` and `<description>`; its `<local_file>` names a doc in the same directory.

2. Answer from the relevant docs. If they fall short, re-check the index for other files, then **ask before any web fallback**.

<web_fallback>
Fallback to the web when the curated collection is insufficient to answer the question and the user has agreed.

Always prefer Firecrawl:
- Known URL: `firecrawl_scrape` (`formats: ["markdown"]`, `onlyMainContent: true`).
- Discovery: `firecrawl_search` (`includeDomains`: bare hostname(s) from `<source_url>`; drop the filter if that returns nothing useful). Omit `scrapeOptions` — it embeds every result's full text in one huge response. Then `firecrawl_scrape` the 1–3 best hits.

Fallback to `WebSearch`/`WebFetch` (lossy on code/config) only if Firecrawl is unavailable.
</web_fallback>

## Step 3. Craft the answer

Grounded answer — coherent, scannable, and well-structured for a TUI like Claude Code. Include key quotation(s) when directly relevant; use emojis strategically for scannability.

<response_format>
```
# Question tersely framed

[grounded answer]

## References used
- Index and each local file read (full paths)
- Web URLs (fallback only)
```
</response_format>
