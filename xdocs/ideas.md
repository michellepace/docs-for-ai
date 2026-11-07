---
updated: 2026-11-07
description: unprioritised proposals; DONE ideas get deleted
---

# Rough ideas to improve docs-for-ai

## Idea: Store the URL actually fetched as `<source_url>`

Today `append-md` fetches `…/page.md` but stores `…/page` in `INDEX.xml`, so re-curate and sync must re-apply rules to know what to fetch. Standardise every collection to store the fetched URL.

Benefits:

- Re-curate and sync fetch `<source_url>` as-is, with no rules.
- A collection can mix URLs from different rules, and editing `direct-fetch-rules.toml` can't break an existing index.

Done collections: `rich`, `mdformat`, `uv`.

## Idea: Per-site URL suffixes

Restructure `direct-fetch-rules.toml` so each site prefix maps to the suffix appended when curating a matching URL:

```toml
[append]
"https://docs.astral.sh/uv/"        = "/index.md"
"https://code.claude.com/docs/"     = ".md"
"https://claude.com/docs/"          = ".md"
"https://platform.claude.com/docs/" = ".md"
```

- `https://docs.astral.sh/uv/getting-started/first-steps/` => `…/first-steps/index.md`
- `https://code.claude.com/docs/en/best-practices` => `….md`

- Builds on the idea above.
- A URL already ending in its suffix passes through unchanged.
- Longest matching prefix wins; TOML's unique keys give one rule per prefix.
- New suffix = new TOML line, no code (today `append-md` is a name defined in code).
- Only covers suffixes; a mid-URL rewrite would need its own section.
- Benefit: I can always curate from the "page url as I see it on the website"

## Idea: Curation skills should diff

So it becomes "whats changed" and shall I tweak/improve the description. Rather than "lets write the whole thing again." But sometimes I do want the descriptions all to be reset, so maybe we need a `--reset-descriptions` flag (remove the PLACEHOLDER, was a past LLM problem). Shooo, so much to do.

## Idea: Sync-index

Should be "refresh-index". But rip it out to just run a .sh shell rather with `claude -p` and the `/curate-doc` skill?

## Idea: `/ask-docs` to read a smaller INDEX

Why: fewer tokens in the context window, and one simple line per doc for Claude. Biggest win for large indexes like `claudecode`.

Rough replacement snippet:

<example-snippet>

Read the index with:

```bash
xmlstarlet sel -t -o 'LOCAL_FILE | TITLE | DESCRIPTION' -n \
    -t -m '//source' \
    -v local_file -o ' | ' -v title -o ' | ' -v description \
    -n ~/.claude/docs-for-ai/collections/$collection/INDEX.xml
```

Optional: tag on `source_url`, since it sometimes holds clues too. When a doc isn't in the collection, the other docs' URLs help Claude guess where it lives.

</example-snippet>

Still to answer:

- Which variable to use, so the path isn't hardcoded?
  - `$collection`: declare `arguments: [collection, question]` like the other skills, then use `.../collections/$collection/INDEX.xml`. Multi-word questions need quotes (the `argument-hint` already shows them).
  - `${CLAUDE_SKILL_DIR}`: the skill's own folder (where `SKILL.md` lives)
  - ~~`${CLAUDE_PROJECT_DIR}`~~: ruled out; it's the session's project root, so outside this repo it points at the other project
- Must run from anywhere outside the repo; `README.md` has the symlink setup.
- Claude loves XML; it's a best practice in the docs. Regardless of tokens saved, does `/ask-docs` perform at least as well as with the XML? (evals)
- Standardise collections on their "direct fetch" URLs (not the TOML mapping rules), otherwise Claude will likely fetch the HTML. Not done yet. E.g. when I curate a Claude Code doc, the `.md` URL only lands in INDEX.xml if that's the one I pass in.
- `xmlstarlet` has to become a dependency
- Don't use `!` bash injection for the block; Claude would only see the output, so it couldn't choose to tag on `source_url`.
- Should I add `curated_at` date too... at which point, just use the XML?!
- Should I give an example of scoping e.g. `-t -m '//source[contains(source_url, "/plugins/")]'` or `-t -m '//source[contains(description, "plugins")]'`

Comparison for `claudecode` (2026-11-07):

| Format | Scope | Lines | Bytes | vs Baseline |
| --- | --- | ---: | ---: | ---: |
| 1. Baseline `INDEX.xml` | All 36 | 254 | 14,408 | 100% |
| 2. Pipe (file, title, description) | All 36 | 37 | 6,719 | 47% |
| 3. Pipe + `source_url` | All 36 | 37 | 8,487 | 59% |
| 2. Pipe, filtered to `/plugins/` | 9 | 10 | 1,803 | 13% |
| 3. Pipe + `source_url`, filtered to `/plugins/` | 9 | 10 | 2,324 | 16% |
