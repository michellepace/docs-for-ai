---
updated: 2026-09-29
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

## Idea: Curation commands should diff

So it becomes "whats changed" and shall I tweak/improve the description. Rather than "lets write the whole thing again." But sometimes I do want the descriptions all to be reset, so maybe we need a `--reset-descriptions` flag (remove the PLACEHOLDER, was a past LLM problem). Shooo, so much to do.

## Idea: Sync-index

Should be "refresh-index". But rip it out to just run a .sh shell rather with `claude -p` and the curate-doc command?
