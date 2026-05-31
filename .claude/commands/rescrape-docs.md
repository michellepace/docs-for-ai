---
description: Re-scrape all docs in collection and regenerate descriptions
argument-hint: <collection>
arguments: [collection]
allowed-tools:
  - Bash(find *)
  - Bash(printf *)
  - Bash(uv run sync-index *)
  - Bash(uv run update-index-descriptions *)
  - Bash(wc *)
  - Read
  - Write
---

Re-scrape every document in `$collection` and batch-regenerate its descriptions.

## Context

Documentation curation enables targeted, efficient context retrieval for AI agents. Rather than searching entire documentation sites, curated collections provide INDEX.xml descriptions that route an LLM reader to the relevant markdown files.

The sync script re-scrapes every source, syncs INDEX.xml to the filesystem, and flags new or changed docs with a PLACEHOLDER description. **Your task:** write a description for each flagged doc.

## Workflow

### 1. Validate argument

!`printf '<existing_collections>\n'; find . -mindepth 2 -maxdepth 2 -name INDEX.xml -printf '%h\n'; printf '</existing_collections>\n'`

Validate `$collection` against `<existing_collections>`; reject if absent, and if it looks like a typo suggest the closest match.

<example_validation_success>

```
## 🙂 Super! Re-scraping the `$collection` collection...
```

</example_validation_success>

<example_validation_failure>

```
## 🤔 Missing argument!
- Usage: `/rescrape-docs <collection>`
- Existing: `shiny`, `uv`, `tailwind`

[Friendly recommendation/suggestion in 1 short sentence]
```

</example_validation_failure>

### 2. Run sync and scrape

```bash
uv run sync-index "$collection"
```

This script:

- Syncs INDEX.xml to filesystem (removes stale entries)
- Re-scrapes all docs via curate_doc.py
- Preserves existing index descriptions for unchanged/whitespace-only content
- Sets PLACEHOLDER index descriptions only for new or content-changed docs, and lists them in its `## Index Descriptions Status` output

### 3. Generate descriptions for PLACEHOLDER entries only

Take the files marked PLACEHOLDER from the script's `## Index Descriptions Status` output.

Read `.claude/references/source-descriptions.md` and follow its quality rules and reference examples. Then, for each PLACEHOLDER source:

1. Analyse the corresponding markdown file
2. Draft a description
3. Count words - rewrite until [20, 30]: `printf '%s' "<draft>" | wc -w`
4. Append it to `$collection/descriptions.txt`:

   ```text
   getting-started-installation.md
   Description for this file here
   ```

### 4. Update INDEX.xml

Run the update script to apply all descriptions:

```bash
uv run update-index-descriptions "$collection" "$collection/descriptions.txt"
```

Verify `PLACEHOLDER` no longer appears in `$collection/INDEX.xml`, otherwise suggest self-healing action and await user confirmation.

### 5. Report completion

Parse structured output from the script and report completion following the `<example_summary_message>` format:

<example_summary_message>

```
## ✅ Re-scrape Complete!

📊 Statistics
- Collection:            `$collection`
- Stale sources removed: [N]
- Total docs:            [M]
- Successfully scraped:  [X]
- Failed to scrape:      [Y]
- Descriptions updated:  [D]

💡 Collection Content Changes for `$collection`:
- [Analyse script output section "## Git Content Changes" and list files here]

*NB: excludes files with only whitespace changes*
```

</example_summary_message>
