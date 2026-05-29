---
argument-hint: <collection> <source_url>
description: Curate a source URL into a collection
allowed-tools:
  - Bash(find *)
  - Bash(printf *)
  - Bash(uv run scripts/curate_doc.py *)
  - Bash(uv run scripts/update_index_descriptions.py *)
  - Read
  - Write
---

Curate source URL `$2` into collection directory `$1`. The script (Step 2) fetches the document and registers its `$1/INDEX.xml` entry; **your task:** write that entry's description.

Existing collections: !`printf '<existing_collections>\n'; find . -mindepth 2 -maxdepth 2 -name INDEX.xml -printf '%h\n'; printf '</existing_collections>\n'`

## Step 1. Validate arguments

The collection `$1` may be an existing one (see `<existing_collections>`) or a new one to create.

Here are just a few examples what new users can inadvertently get wrong - you are to help them do what they intend:

<validation_failure>

- Missing args (generic):

  ```
  ## 🤔 Missing arguments!
  - Usage: `/curate-doc <collection> <url>`
  - Existing collections: `shiny`, `uv`, `tailwind`
  - Example: `/curate-doc shiny https://shiny.posit.co/py/docs/overview.html`

  [Friendly suggestion. Ask for confirmation.]
  ```

- Missing args (URL as $1, smart inference):

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
## 🙂 Super! Curating Shiny doc to shiny/ collection...
```

</validation_success>

Analyse `$1` (collection) and `$2` (URL) against the existing collections and decide whether to fail validation. Match the examples above — emoji-led, brief, kind to an overwhelmed new user. On failure, suggest a fix and ask for confirmation; otherwise output a success message and proceed.

## Step 2. Run the script

```bash
uv run scripts/curate_doc.py "$1" "$2"
```

## Step 3. On script error

Script errors print actionable information. If recovery is possible, propose specific fixes but wait for explicit user approval. Proceed ONLY when script outputs `🎉 Curation Success!` - don't waste effort if the script failed.

## Step 4. Write the description

Read `.claude/references/source-descriptions.md` and follow its quality rules and reference examples. Then:

1. Analyse the curated markdown file
2. Draft a description
3. Validate 20-30 words, rewrite if needed: `echo "description text" | wc -w`
4. Write it to `$1/description.txt`:

      ```text
      overview-shiny-for-python.md
      Description for this file here
      ```

5. Apply it:

   ```bash
   uv run scripts/update_index_descriptions.py "$1" "$1/description.txt"
   ```

## Step 5. Report success

Output the final success message following the `<example_success_message>` format. Use the URL from the script's final `🎉 Curation Success!|...|<URL>|` line (this is the canonical form stored in `INDEX.xml`).

<example_success_message>

```
## 🎉 Curation Success!

🎯 What happened
- Source URL: https://shiny.posit.co/py/docs/overview.html
- [Created/Overwrote] document: `shiny/overview.md`
- Generated description: (see below!)
- [Added/Updated] index: `shiny/INDEX.xml`

"_[your generated description]_" = [actual word count] words ✓
```

</example_success_message>
