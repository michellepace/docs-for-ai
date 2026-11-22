---
description: Get a grounded answer against a doc collection
disable-model-invocation: false
argument-hint: "[collection] \"your question\""
allowed-tools:
  - Bash(grep *)
  - Bash(ls *)
  - Bash(uvx --from yq xq *)
  - Glob
  - Grep
  - Read
  - WebFetch
  - WebSearch
---

Your task is to provide a grounded answer to a user's question against the applicable curated documentation collection.

Available collections:

<available_collections>
!`ls -1 ~/.claude/docs-for-ai/collections`
</available_collections>

## Step 1. Parse Arguments

Parse `$ARGUMENTS`: **collection** = first word, **question** = everything after.

If the question clearly belongs to another collection from `<available_collections>` (or only the web can answer it), halt to confirm a sensible alternative — use "🤔 ..." for visibility.

## Step 2. Research a grounded answer

1. List the collection's docs from its `INDEX.xml` (the authoritative manifest):

   ```shell
   uvx --from yq xq -r --xml-force-list source '
     "local_file | title | description",
     (.docs_index.source[] | "\(.local_file) | \(.title) | \(.description)")
   ' ~/.claude/docs-for-ai/collections/{collection}/INDEX.xml
   ```

2. Answer from the relevant docs. If they fall short, re-check the index for other files. If still short, **ask before** searching the web, preferring the official source domain(s) in `INDEX.xml`'s `<source_url>`.

## Step 3. Craft the answer

Grounded answer — coherent, scannable, and well-structured for a TUI like Claude Code. Include key quotation(s) when directly relevant; use emojis strategically for scannability.

<response_format>

```markdown
# Question tersely framed

[grounded answer]

## References used
- Index and each local file read (full paths)
- Web URLs (fallback only)
```

</response_format>
