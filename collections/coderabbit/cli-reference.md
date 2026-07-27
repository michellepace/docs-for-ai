> ## Documentation Index
> Fetch the complete documentation index at: https://docs.coderabbit.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# CLI Command Reference

> Complete reference for all CodeRabbit CLI commands and options.

## Commands

`cr` is the short alias for `coderabbit`. Both work identically — use whichever fits your workflow.

| Command              | Description                                                                                                                                                              |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `cr`                 | Run code review in non-interactive plain text mode (default)                                                                                                             |
| `cr --agent`         | Output structured JSON for agent-driven workflows                                                                                                                        |
| `cr review --light`  | Request a lighter CLI review for active local development                                                                                                                |
| `cr auth`            | Authentication commands                                                                                                                                                  |
| `cr auth login`      | Authenticate via browser OAuth, [self-hosted](/cli/cli-with-self-hosted-CodeRabbit) (`--self-hosted`), or [API key](/cli/headless-cli-integration) (`--api-key "<key>"`) |
| `cr auth logout`     | Log out from CodeRabbit                                                                                                                                                  |
| `cr auth status`     | Show current authentication status                                                                                                                                       |
| `cr auth org`        | Choose or switch the login/default organization for browser-based auth                                                                                                   |
| `cr stats`           | Show review statistics                                                                                                                                                   |
| `cr doctor`          | Check the CLI installation, local storage, authentication, Git repository state, update policy, and service connectivity                                                 |
| `cr review`          | AI-driven code reviews with plain text or agent output                                                                                                                   |
| `cr review findings` | Show review comments stored locally for the current review context                                                                                                       |
| `cr skills`          | Install or update verified CodeRabbit skills for supported coding agents                                                                                                 |
| `cr update`          | Check for and install the latest CLI version                                                                                                                             |

## Review modes

| Mode                       | Description                                                        |
| -------------------------- | ------------------------------------------------------------------ |
| Default (no flag required) | Detailed plain text feedback in the terminal                       |
| `--agent`                  | Structured JSON output for coding agents and automation            |
| `--light`                  | Faster local review policy for feedback on active development work |

## Review scope

`cr review` reviews tracked changes by default: committed changes, staged changes (including new files added with `git add`), and unstaged edits to tracked files.

| Command                         | Files reviewed                                          |
| ------------------------------- | ------------------------------------------------------- |
| `cr review`                     | Tracked changes                                         |
| `cr review --committed`         | Only committed changes                                  |
| `cr review --uncommitted`       | Staged changes and unstaged edits to tracked files      |
| `cr review --include-untracked` | Tracked changes plus non-ignored files not added to Git |

<Info>
  New files are included once staged with `git add`. To review them before staging, use `--include-untracked`. You can combine it with `--uncommitted`, but not with `--committed`. Contradictory scope flags, such as `--committed` with `--uncommitted`, are rejected before a review starts.
</Info>

## `--agent` review output

`cr review --agent` writes one JSON object per line to `stdout`. Read the stream line by line and handle events by their `type`.

Finding events use these fields:

| Field                 | Description                                                                 |
| --------------------- | --------------------------------------------------------------------------- |
| `type`                | Always `finding` for review results                                         |
| `severity`            | One of: `critical`, `major`, `minor`, `trivial`, `info`                     |
| `fileName`            | File path for the finding                                                   |
| `codegenInstructions` | Agent-oriented fix instructions                                             |
| `suggestions`         | Suggested fix commands or snippets                                          |
| `comment`             | Human-readable review comment, included when `codegenInstructions` is empty |

Other event types in the stream include `review_context`, `status`, `heartbeat`, `complete`, and `error`.

`heartbeat` events are periodic keep-alive signals — reset timeout timers on receipt and otherwise ignore them. For `finding` events, use `codegenInstructions` for agent fix logic and fall back to `comment` when it is absent.

When the selected review scope is skipped because it contains too many files, the review fails with an `error` event. The event can include these optional, additive fields:

| Field            | Description                                                                                                                                                                                                                                                                                                                                                                                         |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `candidates`     | Mutually exclusive narrower-scope suggestions computed from the submitted files. Suggestions can use `--committed`, `--uncommitted`, or up to five `--dir` scopes, and include an estimated local file count and a fit indicator relative to the server-reported limit. The estimate is intentionally conservative, so a candidate marked over the limit may still fit after server-side filtering. |
| `candidatesNote` | Guidance that accompanies the narrower-scope suggestions.                                                                                                                                                                                                                                                                                                                                           |

These fields do not change the existing error contract, so integrations do not need to handle them. Candidates are alternatives, not an automatic partition of the full change set. The CLI does not select a candidate or retry the review. The user or agent must choose one suggestion and rerun the narrower command manually.

In plain mode, the same failure can print a **Narrower scopes found in this diff** block with concrete commands, estimated file counts, and fit indicators. The CLI does not increase the limit, split the review, or retry automatically; choose one command and rerun it manually.

When the selected review scope has no file changes, `cr review --agent` still emits the `review_context` event, then emits a `status` event with `status: "review_skipped"` and a `complete` event with `status: "review_skipped"`, `findings: 0`, and `message: "No changes detected"`. Plain mode prints a no-changes message and exits without starting a review.

## Diagnostics

Run `cr doctor` when installation, authentication, or review startup fails. The command checks:

* CLI runtime and version
* Local CodeRabbit storage directory
* Authentication state and auth environment
* Current Git repository and branch metadata
* Auto-update policy
* CodeRabbit backend reachability
* CodeRabbit WebSocket reachability

`cr doctor` exits with status code `1` when any check fails. Warnings are shown in the report, but they do not cause a non-zero exit code.

## Skills command

Run `cr skills` in an interactive terminal to install or update CodeRabbit skills for detected Codex, Claude Code, Cursor, Gemini CLI, and GitHub Copilot setups. The command verifies the latest published skills release, previews every planned path and change, and asks once for confirmation with **No** selected by default.

```bash theme={null}
cr skills
```

The command has no installation flags or subcommands. Non-interactive invocations do not write files. It preserves externally managed ownership, leaves unsafe or ambiguous conflicts unchanged, and reports project-level copies without modifying them. See [CodeRabbit Skills](/cli/skills) for installation and ownership details.

## Stats command

| Command              | Description                             |
| -------------------- | --------------------------------------- |
| `cr stats`           | Show stats (builds on first run)        |
| `cr stats --rebuild` | Rescan review history and rebuild stats |

## Agent-friendly auth commands

| Command                  | Description                                                                                           |
| ------------------------ | ----------------------------------------------------------------------------------------------------- |
| `cr auth login --agent`  | Browser-based OAuth login with structured JSON events for agents                                      |
| `cr auth logout --agent` | Log out with structured JSON events for agents                                                        |
| `cr auth status --agent` | Return authentication status as structured JSON                                                       |
| `cr auth org --agent`    | Return organization data as structured JSON for agent workflows; starts browser OAuth first if needed |

For GitHub Actions and other non-interactive environments, use `cr auth login --api-key "<key>"` and follow the [Headless CLI integration](/cli/headless-cli-integration) guide.

`cr auth org` changes the login/default org for browser-based auth. Review attribution still depends on the current repository, while API-key auth always uses the API key's organization.

## Options

| Option                    | Description                                                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `--agent`                 | Output structured JSON for agent-driven workflows                                                                                                      |
| `--light`                 | Request the lighter CLI review policy                                                                                                                  |
| `--committed`             | Review only committed changes                                                                                                                          |
| `--uncommitted`           | Review staged changes and unstaged edits to tracked files                                                                                              |
| `--include-untracked`     | Also review non-ignored files not added to Git                                                                                                         |
| `-c, --config <files...>` | Additional instructions for CodeRabbit AI (for example, `CLAUDE.md` or `coderabbit.yaml`)                                                              |
| `--base <branch>`         | Base branch for comparison                                                                                                                             |
| `--base-commit <commit>`  | Base commit on current branch for comparison                                                                                                           |
| `--api-key "<key>"`       | Agentic [API key](/cli/headless-cli-integration) for non-browser or headless authentication (auto-detected if logged in via `cr auth login --api-key`) |
| `--dir <path>`            | Review directory path (must contain an initialized Git repository)                                                                                     |
| `--show-prompts`          | Print saved AI prompts from the most recent local review without running a new review                                                                  |

<Info>
  `--agent` is supported in authentication workflows as well as reviews.
  `cr auth login --agent` applies to the browser-based OAuth login flow and is
  not used with `--self-hosted` or `--api-key` login.
</Info>

<Info>
  PR reviews and CLI reviews will differ, even if run on the same code. CLI
  reviews optimize for immediate feedback during active development, while PR
  reviews provide comprehensive team collaboration context and broader
  repository analysis.
</Info>
