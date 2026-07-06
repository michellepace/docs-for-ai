---
description: Re-curate a collection's docs and descriptions
disable-model-invocation: true
argument-hint: <collection>
arguments: [collection]
allowed-tools:
  - Bash(find *)
  - Bash(printf *)
  - Bash(uv run --directory * sync-index *)
  - Bash(uv run --directory * update-descriptions *)
  - Read
---

Re-curate every document in `$collection` and regenerate its `INDEX.xml` descriptions.

## Context

`INDEX.xml` descriptions route an LLM reader to the right doc, instead of searching whole doc sites. The `sync-index` script re-curates the docs; **your task** is to write a description for each doc it flags with a `PLACEHOLDER`.

## Workflow

### Step 1. Validate argument

Existing collections: !`printf '<existing_collections>\n'; find ~/.claude/docs-for-ai/collections -mindepth 1 -maxdepth 1 -type d -printf '%f\n'; printf '</existing_collections>\n'`

Validate `$collection` against `<existing_collections>`: reject if it's missing or unknown; suggest the closest match for a typo.

Print your verdict before any tool call: on a problem, fail with a suggested fix and stop; on success, print the success message, then start Step 2.

<validation_failure>

Be friendly and brief, and include the corrected `/recurate-docs …` — in the spirit of this example:

```
## 🤔 Missing argument!
- Usage: `/recurate-docs <collection>`
- Existing: `shiny`, `uv`, `tailwind`

[Friendly suggestion in 1 short sentence]
```

</validation_failure>

<validation_success>

```
## 🙂 Super! Re-curating the `$collection` collection...
```

</validation_success>

### Step 2. Run sync and curate

```shell
uv run --directory ~/.claude/docs-for-ai sync-index "collections/$collection"
```

`INDEX.xml` is the source of truth: the script re-curates exactly the sources it lists — and leaves a `PLACEHOLDER` description on each new or content-changed doc. Read its output as it runs.

### Step 3. Write and apply descriptions for `PLACEHOLDER` entries only

Read the rules first: `~/.claude/docs-for-ai/.claude/references/description-rules.md` — its rules and examples govern every description below.

Then work through each file the script flagged `PLACEHOLDER`, one at a time. Each description feeds on two reads — those rules, plus the **full** doc (from the absolute `~/...` path exactly as printed, however large). Write a [20, 30]-word description (strict) per doc.

Apply them all in **one** command — a quoted heredoc, one filename/description line pair per `PLACEHOLDER` entry, keyed by the INDEX `<local_file>`, e.g. `en-hooks.md`:

```shell
uv run --directory ~/.claude/docs-for-ai update-descriptions "collections/$collection" <<'EOF'
getting-started.md
Description for this file here
en-hooks.md
Description for the hooks doc here
EOF
```

Word count is enforced; on ❌, rewrite the flagged description(s) and rerun with only those.

**Verify before proceeding:** no `PLACEHOLDER` remains in `~/.claude/docs-for-ai/collections/$collection/INDEX.xml`; otherwise suggest a self-healing action and await user confirmation.

### Step 4. Report completion

Report from the script's output, in this format:

<example_summary_message>

```
## ✅ Re-curate Complete!

📊 Statistics
- Collection:            `$collection`
- Total docs:            [M]
- Successfully curated:  [X]
- Failed to curate:      [Y]
- Descriptions updated:  [D]

💡 Collection Content Changes for `$collection`:
- [List files from the <GIT_CONTENT_CHANGES> block here]

*NB: excludes files with only whitespace changes*
```

</example_summary_message>
