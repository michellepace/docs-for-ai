---
title: "Claude Code `/run`, `/verify` & `claude -p` — how they fit docs-for-ai"
updated: 2026-09-30
---

Why three Claude Code built-ins fit this repo, and what to watch for when using them here. How each tool works is covered in the curated docs, which are kept current:

- `/run`, `/verify`, `/run-skill-generator` → `collections/claudecode/en-skills.md` ("Run and verify your app")
- `claude -p`, `--bare` → `collections/claudecode/en-headless.md`
- All built-ins, with version notes → `collections/claudecode/en-commands.md`

## `/run` and `/verify` — judge real output

**Why they fit:** this code produces text an LLM reads: sync reports, `INDEX.xml` and curated files. Tests can prove that output is correct, but only reading it shows whether it reads well. `/run` shows a change working. `/verify` gives a PASS/FAIL verdict and tries inputs you didn't. Both work here without setup, because the entry points are plain `uv run <entry-point>` commands that print to stdout. That means `/run-skill-generator` isn't needed.

What `/verify` runs depends on what the diff touches:

| Diff touches | `/verify` does |
| ------------ | -------------- |
| `src/` | Runs the CLI in a terminal |
| `.claude/skills/` | Runs the skill and watches the agent |
| Only `collections/`, tests or docs | Reports a one-line SKIP |

Using it here:

- **It never runs pytest or pyright.** That's by design, so run both yourself as well.
- **Keep skill runs free.** `/curate-doc` can fall back to FireCrawl, which is paid. When you verify a skill edit, point it at a direct-fetch URL and a scratch collection.
- **Review `.claude/skills/verify/SKILL.md` before you commit it.** If `/verify` has to work out the launch itself, it may write this file. At the repo root, that file replaces the bundled `/verify`.
- **Name the range once the branch is pushed**, for example `/verify main..HEAD`. When the branch has an upstream, `/verify` diffs against it (observed in v2.1.285), so an up-to-date branch looks like it has no changes.

## `claude -p` — run skills unattended

**Why it fits:** the skills are this project's real end-to-end workflows, and `claude -p "/<skill> …"` runs one without you at the keyboard. `scripts/curate-collection.sh` runs one URL at a time, and `scripts/run-parallel.sh` runs several prompts at once. The mechanics of calling `claude -p` safely are recorded in each script's header comments, so they aren't repeated here.

The scripts pass no `--allowedTools` or `--permission-mode` because each skill's `allowed-tools` pre-approves what it needs. A `-p` run is one turn, so the grant covers the whole session. If you add a tool call to a skill, add the tool to its `allowed-tools`. Otherwise the headless run is denied that tool.

**Watch for:** `--bare` is planned to become the default for `-p` (`en-headless.md`). Bare mode skips `.claude/skills/`, so when that change ships both scripts will quietly stop loading skills. When it lands, find the opt-out flag in the release notes and add it to both scripts.

## Untried

- A headless `/verify` as a pre-merge gate for `src/` changes. This isn't a documented pattern, so try it by hand before relying on it over `uv run pytest -m "not firecrawl"`.
- `claude -p "/ask-docs <collection> …" --output-format json | jq -r .result` to query a collection from another script.
