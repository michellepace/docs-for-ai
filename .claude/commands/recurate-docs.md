---
description: Re-curate a collection's docs and descriptions
disable-model-invocation: true
argument-hint: "<collection>"
arguments: [collection]
allowed-tools:
  - Bash(find *)
  - Bash(git diff *)
  - Bash(printf *)
  - Bash(uv run --directory * sync-index *)
  - Bash(uv run --directory * update-descriptions *)
  - Read
---

Your task is to re-curate every document in `$collection` and regenerate its `INDEX.xml` descriptions. The `sync-index` script re-curates the docs; you write a routing description for each doc its report lists under `NEEDS DESCRIPTION`.

## Step 1. Validate argument

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

## Step 2. Run the script

```shell
uv run --directory ~/.claude/docs-for-ai sync-index "collections/$collection"
```

`INDEX.xml` is the source of truth: the script re-curates exactly the sources it lists.

## Step 3. Write the descriptions — `NEEDS DESCRIPTION` entries only

Two reads feed every write:

1. `~/.claude/docs-for-ai/.claude/references/description-rules.md` — the rules and examples to follow.
2. The **full** doc, from the `~/...` path exactly as the report prints it (however large).

Each entry's indented `title:` line is the `<title>` that description must complement.

Then pipe one [20, 30]-word description (strict) per entry — all in **one** command; the quoted `<<'EOF'` keeps apostrophes and backticks shell-safe:

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

## Step 4. Report completion

Report completion in this format, filling each slot from the scripts' output:

<report_format>
```
## ✅ Re-curate Complete!

📊 Statistics
- Collection:            `$collection`
- Total docs:            [M]
- Successfully curated:  [X]
- Failed to curate:      [Y]
- Descriptions updated:  [D]

💡 What changed in `$collection`:
- [one line per `NEEDS DESCRIPTION` doc, from its reason tag]
```
</report_format>
