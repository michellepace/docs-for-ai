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

Problems of `.claude/references/description-rules.md`
1. At the very least: pulls in two directions, needs to be simplified too.
2. Another way of writting?: Anthropic, Vercel, etc. LLMs.txt (designed for routing) is very different. I'm unsure which approach to use.

Think about it, my index has always worked well. But then why doesn't Anthropic do this. But has it worked well... maybe its too expensive on the reads (so noise). Maybe thats why its grepping more than it used to. I need to do evals!! - need to eval it.

If the LLMs.txt is a clear winner... could put the llms.txt into collection and always refresh it then curate the new doc. Get the description from there. Some collections will be better than others, so not all can do this. Ergg.

<example-start>

== Reminder of how to start ===

Get https://code.claude.com/docs/llms.txt and match on INDEX.xml's `<source_url>.md` (bypass [20,30] wordcount). Some examples from 2026-08-12::

| `<title>` | `<description>` | `https://code.claude.com/docs/llms.txt` |
| :--- | :--- | :--- |
| Glossary | Definitions disambiguating near-synonyms — subagents versus agent teams, connectors versus MCP servers, sandboxing versus permission rules — plus renamed terms like headless mode, each linking its owning doc. | Definitions for Claude Code terminology. Learn what agentic loop, compaction, CLAUDE.md, hooks, subagents, MCP, and other core concepts mean. [(matched url)](https://code.claude.com/docs/en/glossary.md) |
| Run Claude Code programmatically | Headless `claude -p` for repeatable scripts — `--bare` for a fixed context, JSON and streaming output shaped by `--json-schema`, tool pre-approval, resuming sessions. CLI only. | Use the Agent SDK to run Claude Code programmatically from the CLI, Python, or TypeScript. [(matched url)](https://code.claude.com/docs/en/headless.md) |
| Plugins reference | What a plugin can ship — skills, agents, hooks, MCP and LSP servers, monitors, themes. `claude plugin` subcommands, `${CLAUDE_PLUGIN_ROOT}` versus update-surviving `${CLAUDE_PLUGIN_DATA}` and install scopes. | Complete technical reference for Claude Code plugin system, including schemas, CLI commands, and component specifications. [(matched url)](https://code.claude.com/docs/en/plugins-reference.md) |
| Run parallel sessions with worktrees | `--worktree` creating `.claude/worktrees/` checkouts, `EnterWorktree` mid-session, edits blocked against the main checkout, `isolation: worktree` subagents, `.worktreeinclude` for gitignored files, `worktree.baseRef`, cleanup, and non-git `WorktreeCreate` hooks. | Isolate parallel Claude Code sessions in separate git worktrees so changes don't collide. Covers the `--worktree` flag, subagent isolation, `.worktreeinclude`, cleanup, and non-git VCS hooks. [(matched url)](https://code.claude.com/docs/en/worktrees.md) |

</example-start>

### Data points: all written without `description-rules.md`

No point burning tokens on rules I know are wrong. Wordcount band per run, default `[20,30]`:

- **nextjs frontmatter (2026-08-14) `[5,30]`** — filled from each doc's frontmatter `description:`; only 3 sat in [20,30], median ~13 words.
- **mcp hand-written (2026-08-14) `[20,30]`** — 14 from full doc reads, Fable briefed in one sentence ("so I know when to pick it, like llms.txt"); landed [20,27] unprompted (`40417cf`). Its routing-keyword style: name the primitives, flag deprecations, say what a doc *isn't* deep on.
- **claudecode en-mcp.md (2026-08-14) `[20,30]`** — hand-wrote with Opus. Keyword-stuffed until I asked how it'd say it at lunchtime. Rare content routes: 7% of the doc, its only home.
- **claudeai (2026-08-16) `[5,40]`** — 19 verbatim from `claude.com` LLMs.txt, matched by URL; all 7–20 words, so [20,30] would have rejected most.
- **claudeplat (2026-08-16) `[10,30]`** — all 13 verbatim from each doc's frontmatter `description:`; landed [13,26] words, so [20,30] would have rejected 6.

## Idea: Curation commands should diff

So it becomes "whats changed" and shall I tweak/improve the description. Rather than "lets write the whole thing again." But sometimes I do want the descriptions all to be reset, so maybe we need a `--reset-descriptions` flag (remove the PLACEHOLDER, was a past LLM problem). Shooo, so much to do.

## Idea: Sync-index

Should be "refresh-index". But rip it out to just run a .sh shell rather with `claude -p` and the curate-doc command?
