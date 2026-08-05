# Rough ideas to improve docs-for-ai

## Idea: Make configurable by URL

Easier to manage and understand, more flexible.

Examples:
- commmon ones (`append-md`): add ".md"
- https://docs.astral.sh/uv/concepts/tools/ → https://docs.astral.sh/uv/concepts/tools/index.md (add "index.md")
- https://rich.readthedocs.io/en/stable/ → https://rich.readthedocs.io/en/stable/_sources/panel.rst.txt

Would also stip the 3 errors on `uv run sync-index collections/uv`.

## Idea: Source URL should be truthful

Currently if I curate and it has `md-append` then the source URL in the index isn't the `.md` one.

If were were truthful, then re-curate doesn't have to apply any rules, it can just use the source URL in the index.

The impact is that I can have "more than one rule" in an index.

## Idea: Re-write "description rules"

Iron out the pulling in two directions. Simplify. Once it's working well, then give curation commands access to diff. So it becomes "whats changed" and shall I tweak the description.

## Idea: Sync-index

Should be "refresh-index". But rip it out to just run a .sh shell rather with `claude -p` and the curate-doc command?
