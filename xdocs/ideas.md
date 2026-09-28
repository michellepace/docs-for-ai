# Rough ideas to improve docs-for-ai

## Idea: Make configurable by URL

Easier to manage and understand, more flexible.

Examples:

- commmon ones (`append-md`): add ".md"
- https://docs.astral.sh/uv/concepts/tools/ → https://docs.astral.sh/uv/concepts/tools/index.md (add "index.md")

Would also stip the 3 errors on `uv run sync-index collections/uv`.

## Idea: Source URL should be truthful

Currently if I curate and it has `md-append` then the source URL in the index isn't the `.md` one.

If were were truthful, then re-curate doesn't have to apply any rules, it can just use the source URL in the index.

The impact is that I can have "more than one rule" in an index.

Canonical now (2026-09-26):

- rich
- mdformat (`34ce9bb`)

## Idea: Re-write "description rules" — ✅ DONE

Done 2026-09-28: `.claude/references/description-rules.md` cut from ~1,000 words to ~130. `/curate-doc` pins `model: claude-opus-5-5` at `effort: xhigh`, and `update-descriptions` enforces [8, 25] words.

- A blind routing eval (Claude picking docs from `INDEX.xml` alone) found the short rules route at least as well as the long ones and as `llms.txt` descriptions, so no need to source descriptions from `llms.txt`.
- Keep the rules short: Opus follows each one literally (the long file's examples became a template) and ignores soft length guidance; only the script's cap bounds length.
- To revisit, re-run that eval: questions with known answer docs, written without seeing any description, routed blind from the index.

## Idea: Curation commands should diff

So it becomes "whats changed" and shall I tweak/improve the description. Rather than "lets write the whole thing again." But sometimes I do want the descriptions all to be reset, so maybe we need a `--reset-descriptions` flag (remove the PLACEHOLDER, was a past LLM problem). Shooo, so much to do.

## Idea: Sync-index

Should be "refresh-index". But rip it out to just run a .sh shell rather with `claude -p` and the curate-doc command?
