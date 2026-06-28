---
description: Re-curate all docs in collection and regenerate descriptions
disable-model-invocation: true
argument-hint: <collection>
arguments: [collection]
allowed-tools:
  - Bash(find *)
  - Bash(printf *)
  - Bash(uv run --directory * sync-index *)
  - Bash(uv run --directory * update-descriptions *)
  - Bash(wc *)
  - Read
  - Write
---

Re-curate every document in `$collection` and batch-regenerate its descriptions.

## Context

Curated collections route an LLM reader to the right doc via INDEX.xml descriptions, instead of searching whole documentation sites. The sync script re-curates every source and flags new or changed docs with a PLACEHOLDER description. **Your task:** write a description for each flagged doc.

## Workflow

### 1. Validate argument

!`printf '<existing_collections>\n'; find ~/.claude/docs-for-ai/collections -mindepth 1 -maxdepth 1 -type d -printf '%f\n'; printf '</existing_collections>\n'`

Validate `$collection` against `<existing_collections>`; reject if absent, and suggest the closest match if it looks like a typo.

<example_validation_success>

```
## 🙂 Super! Re-curating the `$collection` collection...
```

</example_validation_success>

<example_validation_failure>

```
## 🤔 Missing argument!
- Usage: `/recurate-docs <collection>`
- Existing: `shiny`, `uv`, `tailwind`

[Friendly recommendation/suggestion in 1 short sentence]
```

</example_validation_failure>

### 2. Run sync and curate

```bash
uv run --directory ~/.claude/docs-for-ai sync-index "collections/$collection"
```

INDEX.xml is the source of truth: the script re-curates exactly the sources it lists, prunes entries whose file is missing, and leaves a PLACEHOLDER description on each new or content-changed doc. Read its output as it runs.

### 3. Generate descriptions for PLACEHOLDER entries only

Read `~/.claude/docs-for-ai/.claude/references/source-descriptions.md` for the quality rules and reference examples. Then, for each file the script flagged PLACEHOLDER (use the path **exactly as printed** — absolute `~/...`):

1. Analyse the markdown file and draft a description
2. Count words (`printf '%s' "<draft>" | wc -w`); rewrite until 20–30
3. Append it to `~/.claude/docs-for-ai/collections/$collection/descriptions.txt`:

   ```text
   getting-started-installation.md
   Description for this file here
   ```

### 4. Update INDEX.xml

```bash
uv run --directory ~/.claude/docs-for-ai update-descriptions "collections/$collection" "collections/$collection/descriptions.txt"
```

Confirm `PLACEHOLDER` no longer appears in `~/.claude/docs-for-ai/collections/$collection/INDEX.xml`; otherwise suggest a self-healing action and await user confirmation.

### 5. Report completion

Report from the script's output, in this format:

<example_summary_message>

```
## ✅ Re-curate Complete!

📊 Statistics
- Collection:            `$collection`
- Stale sources removed: [N]
- Total docs:            [M]
- Successfully curated:  [X]
- Failed to curate:      [Y]
- Descriptions updated:  [D]

💡 Collection Content Changes for `$collection`:
- [List files from the <GIT_CONTENT_CHANGES> block here]

*NB: excludes files with only whitespace changes*
```

</example_summary_message>
