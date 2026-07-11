---
title: "Claude Code: `/run`, `/verify` & Headless Mode — for docs-for-ai 🧭"
updated: 2026-07-01
status: draft / rough
---

A guide to two built-in Claude Code skills and headless mode (`claude -p`), and
how they fit a **CLI project** like this one — where the runtime surface is
`uv run curate-doc`, `uv run sync-index`, and `uv run update-descriptions`, and
the real end-to-end workflows live in `.claude/commands/` (`/curate-doc`,
`/ask-docs`, `/recurate-docs`).

______________________________________________________________________

## 1. The `/run` command 🚀

### What it does

`/run` launches and **drives your project's app so you can see a change actually
working** — not just passing tests or typechecks. It infers how to launch the
project from its type (CLI, server, TUI, Electron, browser-driven, library) and
from files like `pyproject.toml`, `package.json`, or a README. It then executes
the app with representative input, observes the real output, and reports what it
saw.

If your project needs a non-standard launch (databases, env files, multi-step
builds), inference can fail — running `/run-skill-generator` once records a
repeatable launch recipe under `.claude/skills/run-<name>/SKILL.md`, which
`/run`, `/verify`, and other agents then follow instead of rediscovering it
every time.

### When to reach for it

- You've just made a change and want to **see it working in the real app**, not
  infer it from green tests.
- You want a **screenshot or live output** of the current state of the app.
- You're debugging behaviour that only shows up at runtime (config, environment,
  integration).

### Use case examples

1. **Next.js + Playwright** 🌐 — after restyling a dashboard page, `/run` boots
   the dev server, drives a browser to the page, and screenshots it so you can
   see the layout for real.
2. **FastAPI service** — after adding a `/health` endpoint, `/run` starts
   uvicorn, curls the endpoint, and shows the actual JSON response and status
   code.
3. **TUI app (Textual/Ink)** — after changing a keybinding, `/run` launches the
   TUI, sends the keystrokes, and observes that the screen updates as intended.
4. **📌 This project** — on your current branch (`sync-index/tidy-report`), after
   tweaking the collection-status report wording, `/run` would execute something
   like `uv run sync-index nextjs` and show you the **actual rendered report**,
   so you can judge whether it really reads well for an LLM consumer — something
   a unit test can't tell you.

______________________________________________________________________

## 2. The `/verify` command ✅

### What it does

`/verify` checks that a code change **actually does what it's supposed to** by
exercising it end-to-end and observing behaviour — deliberately *not* falling
back to "tests pass" or "pyright is happy". It builds/launches the project
(using the same recorded `run-<name>` skill as `/run`, and bootstrapping a
project verify skill on first use if none exists), drives the affected flow, and
reports success or failure against the intended behaviour.

**`/run` vs `/verify` in one line:** `/run` is "show me it working"
(exploratory, during development); `/verify` is "prove this diff is correct" (a
gate, before committing).

### When to reach for it

- **Before committing a nontrivial change** to product code — the skill's own
  guidance.
- When tests pass but you're not confident the *observable* behaviour is right
  (CLI output formatting, file side-effects, exit codes).
- **Not** for diffs that only touch tests or docs — there's no runtime surface
  to drive. In this repo, that means: skip it for pure `collections/` curation
  changes; use it for changes to the Python CLI code.

### Use case examples

1. **E-commerce checkout change** 🛒 — before committing a discount-calculation
   fix, `/verify` drives the full add-to-basket → checkout flow in a browser and
   confirms the displayed total.
2. **New CLI flag in a Node/Go tool** — `/verify` builds the binary, runs it
   with and without the new flag, and checks output and exit codes match the
   intended contract.
3. **Auth middleware refactor** 🔐 — `/verify` starts the server and exercises
   both an authorised and an unauthorised request, confirming a 200 and a 401
   respectively.
4. **📌 This project** — before committing the tidy-report work, `/verify` would
   set up a temporary collection exercising each sync state (new file, moved
   file, deleted file, stale `INDEX.xml` entry), run `uv run sync-index` against
   it, and confirm the report describes each state correctly. That complements
   your "one sociable test per sync state" commit — the tests assert behaviour,
   `/verify` watches the real output land.

______________________________________________________________________

## 3. Headless mode (`claude -p`) 🤖

*(Your curated reference: `collections/claudecode/en-headless.md`)*

### What it does

`claude -p "<prompt>"` runs Claude Code **non-interactively**: one prompt in,
result out, exits. It's the CLI face of the Agent SDK and composes like any Unix
tool:

- **Pipes**:
  `cat build-error.txt | claude -p 'explain the root cause' > out.txt`
- **Structured output**: `--output-format json` (with `--json-schema` for typed
  results)
- **Permissions up front**: `--allowedTools "Bash,Read,Edit"` or
  `--permission-mode acceptEdits`
- **Conversation state**: `--continue` / `--resume <session-id>`
- **`--bare`**: fast, reproducible CI mode — but it **skips auto-discovery of
  skills, hooks, plugins, and CLAUDE.md**, which matters below ⚠️

Crucially (from your own doc): **user-invoked skills and custom commands work in
`-p` mode** — include `/skill-name` in the prompt string and Claude Code expands
it before running. Only interactive-dialog commands like `/login` are
unavailable.

### When to reach for it

- **CI/CD and scripts** — anywhere a human isn't at the keyboard.
- **Scheduled/recurring jobs** — cron, GitHub Actions on a schedule.
- **Composing Claude into pipelines** — when you want its output as data (JSON)
  for another tool.

### Use case examples

1. **PR linter in CI** 🔍 —
   `git diff main | claude -p "report typos as filename:line"` wired into a
   `package.json` script or GitHub Action.

2. **Structured extraction** —
   `claude -p "Extract function names from auth.py" --output-format json --json-schema '...' | jq '.structured_output'`
   feeding a downstream script.

3. **Nightly triage** 🌙 — a cron job runs
   `claude -p "Run the test suite and summarise any failures" --allowedTools "Bash,Read"`
   and posts the summary somewhere.

4. **📌 This project** — your commands *are* end-to-end agentic workflows, and
   `-p` is exactly how you run them unattended:

   ```bash
   # Scheduled re-curation of a collection
   claude -p "/recurate-docs uv" --permission-mode acceptEdits

   # Query a collection from another script
   claude -p "/ask-docs claudecode how does --bare affect skills?" --output-format json | jq -r '.result'
   ```

______________________________________________________________________

## Analysis: can `claude -p` combine with `/run` or `/verify`? 🔗

**Yes — technically it works, and for a CLI project like yours it's one of the
more sensible places to do it.** Since skills work in `-p` mode,
`claude -p "/verify the sync-index report change" --permission-mode acceptEdits`
is a valid invocation. But the docs stop short of blessing it as a pattern, so
treat it with judgement:

### Where the combination genuinely helps

- **Headless `/verify` as a pre-merge smoke gate** 🚦 — a CI step (or local git
  hook) that runs `/verify` on the branch diff before merge. For *this* repo
  it's a good fit: the runtime surface is a fast, non-interactive CLI
  (`uv run sync-index …`), so there's nothing awkward to observe — stdout, exit
  codes, and file effects are all headless-friendly.
- **Headless `/run` for artefact capture** — e.g. a scheduled job that runs the
  app and saves its output/report for humans to review later.

### Where it doesn't

- **Web/TUI-heavy projects** — `/run` and `/verify` often want to *watch* a live
  app; and in `-p` mode any background dev server is killed ~5 s after the
  result returns, so long-lived observation is awkward. Interactive sessions
  suit those better.
- **With `--bare`** ⚠️ — bare mode skips skill discovery, so `/run`, `/verify`,
  and your custom commands won't load. If you want them headlessly, drop
  `--bare` (and accept the slower, environment-dependent startup) or pass the
  needed context via flags.
- **Permissions** — headless runs can't prompt, so `/verify` needs its tools
  pre-approved (`--allowedTools "Bash(uv run *),Read,Edit"` or a permission
  mode), otherwise it aborts mid-flow.

### The picture for docs-for-ai 🖼️

Your instinct is right: your `.claude/commands/*.md` are the true end-to-end
workflows of this project, so the **strongest pairing is headless + your own
commands** (`claude -p "/recurate-docs …"` on a schedule,
`claude -p "/ask-docs …"` from scripts). `/run` and `/verify` sit one layer
below — they exercise the *Python CLI code* your commands rely on. A tidy
division of labour:

| Layer                        | Tool                                               | Typical moment                  |
| ---------------------------- | -------------------------------------------------- | ------------------------------- |
| Python CLI change, exploring | `/run` (interactive)                               | "Show me the new report output" |
| Python CLI change, gating    | `/verify` (interactive; optionally headless in CI) | Before committing               |
| Whole-workflow automation    | `claude -p "/curate-doc …"` etc.                   | Cron, CI, scripts               |

One caveat to close on: headless `/run`/`/verify` is *possible and sensible
here*, but not an officially documented pattern — if it ever behaves oddly in
CI, prefer running `/verify` interactively and keeping CI on plain
`uv run pytest -m "not firecrawl"`. 😊
