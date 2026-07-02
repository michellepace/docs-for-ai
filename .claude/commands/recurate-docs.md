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

Re-curate every document in `$collection` and regenerate its INDEX.xml descriptions.

## Context

INDEX.xml descriptions route an LLM reader to the right doc, instead of searching whole doc sites. The `sync-index` script re-curates the docs; **your task** is to write a description for each doc it flags with a PLACEHOLDER.

## Workflow

### 1. Validate argument

Existing collections: !`printf '<existing_collections>\n'; find ~/.claude/docs-for-ai/collections -mindepth 1 -maxdepth 1 -type d -printf '%f\n'; printf '</existing_collections>\n'`

Validate `$collection` against `<existing_collections>`: reject if it's missing or unknown, suggesting the closest match when it looks like a typo. Keep messages emoji-led, brief, and kind — fail with a suggested fix, or show success and proceed.

<validation_failure>

Shape: `## 🤔 <one-line diagnosis>`, a `-` bullet or two (what you saw + the corrected `/recurate-docs …`), then one warm line. Anchor example (missing arg):

```
## 🤔 Missing argument!
- Usage: `/recurate-docs <collection>`
- Existing: `shiny`, `uv`, `tailwind`

[Friendly recommendation/suggestion in 1 short sentence]
```

</validation_failure>

<validation_success>

```
## 🙂 Super! Re-curating the `$collection` collection...
```

</validation_success>

### 2. Run sync and curate

```shell
uv run --directory ~/.claude/docs-for-ai sync-index "collections/$collection"
```

INDEX.xml is the source of truth: the script re-curates exactly the sources it lists, prunes entries whose file is missing, and leaves a PLACEHOLDER description on each new or content-changed doc. Read its output as it runs.

### 3. Generate descriptions for PLACEHOLDER entries only

Read `~/.claude/docs-for-ai/.claude/references/source-descriptions.md` and follow its rules and examples. Then, for each file the script flagged PLACEHOLDER (use the path **exactly as printed** — absolute `~/...`):

1. Analyse the doc and draft a [20, 30]-word description (strict)
2. Append it to `~/.claude/docs-for-ai/collections/$collection/descriptions.txt`:

   ```text
   getting-started-installation.md
   Description for this file here
   ```

### 4. Update INDEX.xml

```shell
uv run --directory ~/.claude/docs-for-ai update-descriptions "collections/$collection" "collections/$collection/descriptions.txt"
```

Word count is enforced; rewrite the flagged description(s) and rerun until it passes.

**Verify before proceeding:** no `PLACEHOLDER` remains in `~/.claude/docs-for-ai/collections/$collection/INDEX.xml`; otherwise suggest a self-healing action and await user confirmation.

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
