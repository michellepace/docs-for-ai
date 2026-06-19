---
description: Curate a source URL into a collection
argument-hint: <collection> <source_url>
arguments: [collection, source_url]
allowed-tools:
  - Bash(find *)
  - Bash(printf *)
  - Bash(uv run --directory * curate-doc *)
  - Bash(uv run --directory * update-index-descriptions *)
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

```bash
uv run --directory ~/.claude/docs-for-ai curate-doc "collections/$collection" "$source_url"
```

## Step 3. On script error

Script errors print actionable information. If recovery is possible, propose specific fixes but wait for explicit user approval. Proceed ONLY when script outputs `🎉 Curation Success!` - don't waste effort if the script failed.

## Step 4. Write the description

Read `~/.claude/docs-for-ai/.claude/references/source-descriptions.md` and follow its quality rules and reference examples. Then:

1. Analyse the curated markdown file
2. Draft a description
3. Count words - rewrite until [20, 30]: `printf '%s' "<draft>" | wc -w`
4. Write it to `~/.claude/docs-for-ai/collections/$collection/description.txt`:

      ```text
      overview-shiny-for-python.md
      Description for this file here
      ```

5. Apply it:

   ```bash
   uv run --directory ~/.claude/docs-for-ai update-index-descriptions "collections/$collection" "collections/$collection/description.txt"
   ```

## Step 5. Report success

Output the final success message following the `<example_success_message>` format. Use the URL from the script's final `🎉 Curation Success!|...|<URL>|` line (this is the canonical form stored in `INDEX.xml`). For the document and index paths, use them **exactly as the script printed them** in its `✅ Created/Overwrote ... document|<path>|` and `✅ ... index source|<path>|` lines — these are absolute (`~/...`) so the reader sees the real location.

<example_success_message>

```
## 🎉 Curation Success!

🎯 What happened
- Source URL: https://shiny.posit.co/py/docs/overview.html
- [Created/Overwrote] document: `~/path/<file>.md`
- [Added/Updated] index: `~/path/INDEX.xml`
- Generated index description:

"_[your generated description]_" = [actual word count] words ✓
```

</example_success_message>
