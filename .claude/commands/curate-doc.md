---
description: Curate a source URL into a collection
disable-model-invocation: true
argument-hint: <collection> <url>
arguments: [collection, source_url]
allowed-tools:
  - Bash(find *)
  - Bash(printf *)
  - Bash(uv run --directory * curate-doc *)
  - Bash(uv run --directory * update-descriptions *)
  - Read
---

Your task is to curate a source URL `$source_url` into a collection `$collection`.

## Step 1. Validate arguments

Existing collections: !`printf '<existing_collections>\n'; find ~/.claude/docs-for-ai/collections -mindepth 1 -maxdepth 1 -type d -printf '%f\n'; printf '</existing_collections>\n'`

Parse `$collection` and `$source_url`, then weigh them against the existing collections. Spot what a new user likely got wrong and steer them to what they *intended* — `$collection` may already exist, or be created fresh. Keep every message emoji-led, brief, and kind. On a problem, fail with a suggested fix and ask to confirm; otherwise show success and proceed.

<validation_failure>

Every failure has the same shape: `## 🤔 <one-line diagnosis>`, then 1–3 `-` bullets (what you saw + the corrected `/curate-doc …` to run), then one warm line asking to confirm. The cases differ only in what you detect:

- **Missing args** — show usage, list existing collections, add a runnable example.
- **No collection, URL given** — infer a collection name from the URL; propose it as new.
- **Typo** — `$collection` is near an existing one (`shiyy` → `shiny`); suggest the match.
- **Semantic mismatch** — `$collection` exists but the URL is plainly another tech; point to the right one.

Anchor example (semantic mismatch):

```
## 🤔 Mmm.. are you sure you meant `shiny`?
- Collection: `shiny`
- URL: `https://tailwindcss.com/docs/installation`
- This looks like Tailwind CSS docs, not Shiny
- Did you mean: `/curate-doc tailwind https://tailwindcss.com/docs/installation` ?

[Friendly recommendation in 1–2 short sentences, ask for confirmation]
```

</validation_failure>

<validation_success>

```
## 🙂 Super! Curating Shiny doc to collections/shiny/ collection...
```

</validation_success>

## Step 2. Run the script

```shell
uv run --directory ~/.claude/docs-for-ai curate-doc "collections/$collection" "$source_url"
```

Errors print actionable info. Propose fixes but await user approval; proceed ONLY on `🏁 Success!`.

## Step 3. Write the description

Two reads feed the write:

1. `~/.claude/docs-for-ai/.claude/references/description-rules.md` — the rules and examples to follow.
2. The **full** curated doc (however large) — what you're describing.

Then pipe a [20, 30]-word description (strict) straight in — the quoted `<<'EOF'` keeps apostrophes and backticks shell-safe:

```shell
uv run --directory ~/.claude/docs-for-ai update-descriptions "collections/$collection" <<'EOF'
overview-shiny-for-python.md
Description for doc on single line
EOF
```

Word count is enforced; on ❌, rewrite the description and rerun until it passes.

## Step 4. Report success

Report success in this format, filling each slot from the script's output above:

<success_message_format>

```
## ✨ Curation Success!

🎯 What happened
- Source URL: <canonical `source_url` from `<source>` block — not your raw input>
- [Created/Overwrote] doc: `<path, verbatim from ✅ line>`
- [Indexed/Reindexed] index: `<path, verbatim from ✅ line>`
- Wrote index description <N> words ✓

"_<description from Step 3>_"
```

</success_message_format>
