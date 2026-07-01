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
  - Bash(wc *)
  - Read
  - Write
---

Your task is to curate a source URL `$source_url` into a collection `$collection`.

## Step 1. Validate arguments

Existing collections: !`printf '<existing_collections>\n'; find ~/.claude/docs-for-ai/collections -mindepth 1 -maxdepth 1 -type d -printf '%f\n'; printf '</existing_collections>\n'`

The collection `$collection` may already exist else will be created. Parse the user's arguments first. Here are just a few examples what new users can inadvertently get wrong - you are to help them do what they intend:

<validation_failure>

- Missing args (generic):

  ```
  ## 🤔 Missing arguments!
  - Usage: `/curate-doc <collection> <url>`
  - Existing collections: `shiny`, `uv`, `tailwind`
  - Example: `/curate-doc shiny https://shiny.posit.co/py/docs/overview.html`

  [Friendly suggestion. Ask for confirmation.]
  ```

- Missing args (URL as `$collection`, smart inference):

  ```
  ## 🤔 You didn't give me a collection?
  - URL detected: `https://vite.dev/guide/cli.html`
  - My Suggestion: A new `vite` collection looks ideal!
  - Try: `/curate-doc vite https://vite.dev/guide/cli.html`

  [Shall we proceed with `vite` as a new collection? It will get created automatically 🙂]
  ```

- Typo detection:

  ```
  ## 🤔 Collection "shiyy" doesn't exist, but you have "shiny"!
  - Did you mean: `/curate-doc shiny https://example.com/docs` ?

  [Friendly suggestion. Ask for confirmation.]
  ```

- Semantic mismatch:

  ```
  ## 🤔 Mmm.. are you sure you meant `shiny`?
  - Collection: `shiny`
  - URL: `https://tailwindcss.com/docs/installation`
  - This appears to be Tailwind CSS docs, not Shiny
  - Did you mean: `/curate-doc tailwind https://tailwindcss.com/docs/installation` ?

  [Friendly recommendation in 1-2 short sentence, ask for confirmation]
  ```

</validation_failure>

<validation_success>

```
## 🙂 Super! Curating Shiny doc to collections/shiny/ collection...
```

</validation_success>

Analyse `$collection` and `$source_url` against the existing collections and decide whether to fail validation. Match the examples above — emoji-led, brief, kind to an overwhelmed new user. On failure, suggest a fix and ask for confirmation; otherwise output a success message and proceed.

## Step 2. Run the script

```shell
uv run --directory ~/.claude/docs-for-ai curate-doc "collections/$collection" "$source_url"
```

Errors print actionable info. Propose fixes but await user approval; proceed ONLY on `🎉 Curation Success!`.

## Step 3. Generate the description

Read `~/.claude/docs-for-ai/.claude/references/source-descriptions.md` and follow its rules and examples. Then:

1. Analyse the curated doc and draft a [20, 30]-word description (strict) into `~/.claude/docs-for-ai/collections/$collection/description.txt`:
    ```text
    overview-shiny-for-python.md
    Description for doc on single line
    ```
2. Apply it:
    ```shell
    uv run --directory ~/.claude/docs-for-ai update-descriptions "collections/$collection" "collections/$collection/description.txt"
    ```

Word count is enforced; on error, rewrite the description and rerun until it passes.

## Step 4. Report success

Report success in this format, filling each slot from the script's output above:

<success_message_format>

```
## 🎉 Curation Success!

🎯 What happened
- Source URL: <canonical URL from the 🎉 line — not your raw input>
- [Created/Overwrote] document: `<path, verbatim from the ✅ doc line>`
- [Added/Updated] index: `<path, verbatim from the ✅ index line>`
- Generated index description:

"_<description from Step 3>_" = <N> words ✓
```

</success_message_format>
