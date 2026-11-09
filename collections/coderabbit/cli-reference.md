> ## Documentation Index
> Fetch the complete documentation index at: https://docs.coderabbit.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# CLI Command Reference

> Reference for CodeRabbit CLI commands and options, generated from the CLI help output.

Generated from the help output of CodeRabbit CLI 0.9.2. `cr` is the short alias for `coderabbit`. Run `coderabbit <command> --help` to see the same information in your terminal.

## Global usage

CodeRabbit CLI for code review and cloud coding.

Usage: `coderabbit [options] [command]`

| Option | Description |
| - | - |
| `-v, --version` | Show CLI version |

| Mode | Description |
| - | - |
| `--agent` | Emit structured findings for agents |
| (default) | Plain-text review of tracked changes |

## Commands

| Command | Description |
| - | - |
| [`auth`](#auth) | Manage authentication |
| [`review`](#review) | Review local changes |
| [`pullrequest`](#pullrequest) | Inspect a CodeRabbit-reviewed GitHub pull request |
| [`stats`](#stats) | Show statistics from locally stored review history |
| [`usage`](#usage) | Show included-review availability and billing-period usage |
| [`update`](#update) | Update CodeRabbit CLI to the latest version |
| [`config`](#config) | Create or configure CodeRabbit configuration |
| [`doctor`](#doctor) | Check CodeRabbit CLI installation and local review readiness |
| [`skills`](#skills) | Manage CodeRabbit agent skills |
| [`code`](#code) | Work with the CodeRabbit cloud Coding Agent |
| [`completion`](#completion) | Print a shell completion script |

### auth

Authentication commands

Usage: `coderabbit auth [options] [command]`

| Command | Description |
| - | - |
| [`login [options]`](#auth-login) | Authenticate with CodeRabbit |
| [`logout [options]`](#auth-logout) | Clear local authentication |
| [`status [options]`](#auth-status) | Show current authentication status |
| [`org [options]`](#auth-org) | Switch the active organization |

```bash Examples theme={null}
# Authenticate with CodeRabbit
coderabbit auth login

# Show current authentication status
coderabbit auth status

# Switch the active organization
coderabbit auth org

# Clear local authentication
coderabbit auth logout
```

#### auth login

Authenticate with CodeRabbit

Usage: `coderabbit auth login [options]`

| Option | Description |
| - | - |
| `--agent` | Emit structured JSON output for agent-driven OAuth login |
| `--self-hosted` | Use self-hosted CodeRabbit instance |
| `--no-browser` | Open the login URL yourself using a browser that can reach this machine's localhost callback (port forwarding may be required) |
| `--api-key <api-key>` | Authenticate with a CodeRabbit API key |
| `--region <region>` | Use CodeRabbit's US or EU region Choices: `us`, `eu` |

```bash Examples theme={null}
# Interactive login with browser
coderabbit auth login

# Agent-friendly OAuth login with JSON output
coderabbit auth login --agent

# Manually open the URL with localhost access
coderabbit auth login --agent --no-browser

# Self-hosted instance login
coderabbit auth login --self-hosted

# Authenticate with CodeRabbit EU
coderabbit auth login --region eu

# Store an API key for CLI reviews
coderabbit auth login --api-key "<api-key>"

# Store an EU API key
coderabbit auth login --region eu --api-key "<api-key>"
```

> [!NOTE]
>
> `--agent` is only supported for localhost browser callbacks and never accepts pasted OAuth tokens.

#### auth logout

Clear local authentication

Usage: `coderabbit auth logout [options]`

| Option | Description |
| - | - |
| `--agent` | Emit structured JSON output for agent-driven logout |

```bash Examples theme={null}
# Clear local authentication
coderabbit auth logout

# Emit structured logout output
coderabbit auth logout --agent
```

#### auth status

Show current authentication status

Usage: `coderabbit auth status [options]`

| Option | Description |
| - | - |
| `--agent` | Emit structured JSON output for agent-driven status check |

```bash Examples theme={null}
# Show current authentication status
coderabbit auth status

# Emit structured auth status as JSON
coderabbit auth status --agent
```

#### auth org

Switch the active organization

Usage: `coderabbit auth org [options]`

| Option | Description |
| - | - |
| `--agent` | List available organizations as JSON without switching organizations |

```bash Examples theme={null}
# Switch the active organization
coderabbit auth org

# Emit available organizations as JSON
coderabbit auth org --agent
```

### review

AI-driven code review for the current Git workspace

Usage: `coderabbit review [options] [command]`

A review that fails or doesn't cover every file exits with code `1`, even after printing findings; see [Exit codes](https://docs.coderabbit.ai/cli/agent-mode.md#exit-codes). For which changes each scope flag selects, see [Local review](https://docs.coderabbit.ai/cli/index.md#local-review).

| Option | Description |
| - | - |
| `--deep [focus]` | Use the full pull request review policy (focus text requires early access) |
| `--fresh` | Review selected changes without reusing the previous local checkpoint |
| `--show-prompts` | Print AI prompts without starting a new review |
| `--agent` | Emit structured findings for agent workflows |
| `--gate <severity>` | Exit 2 for findings at or above this severity; review the selected diff fresh Choices: `critical`, `major`, `minor`, `trivial`, `info` |
| `--use-credits` | Use usage credits if this review exceeds included limits |
| `--committed` | Review only committed changes |
| `--uncommitted` | Review uncommitted Git changes |
| `--include-untracked` | Also review files that have not been added to Git |
| `-c, --config <files...>` | Additional instructions for CodeRabbit AI (e.g., claude.md, coderabbit.yaml) |
| `--base <branch>` | Git base branch for comparison |
| `--base-commit <commit>` | Git base commit on current branch for comparison |
| `--dir <path>` | Review only changes inside this directory |
| `--remote <owner/repo>` | Review a GitHub repository on the server without a local checkout |
| `--source-branch <ref>` | Source branch or ref to review with `--remote` |
| `--api-key <key>` | API key for authentication |
| `--usage` | Show included reviews and billing-period usage instead of reviewing (alias of `coderabbit usage`) |
| `--region <region>` | Region for inline API key authentication Choices: `us`, `eu` |

| Command | Description |
| - | - |
| [`findings [options]`](#review-findings) | Show the most recent local review with stored findings |

```bash Examples theme={null}
# Review tracked changes
coderabbit review

# Review only committed changes
coderabbit review --committed

# Review uncommitted Git changes
coderabbit review --uncommitted

# Also review files not added to Git
coderabbit review --include-untracked

# Emit structured findings for agents
coderabbit review --agent

# Exit 2 for major or critical findings
coderabbit review --agent --gate major

# Use the full pull request review policy
coderabbit review --deep

# Review selected changes without the previous local checkpoint
coderabbit review --fresh

# Print prompts from the latest local review
coderabbit review --show-prompts

# Compare current branch against main
coderabbit review --base main

# Review changes inside that directory
coderabbit review --dir /path/to/workspace

# Review with an EU API key without storing it
coderabbit review --region eu --api-key "<key>"

# Show stored local review findings
coderabbit review findings

# Forget stored findings for this scope
coderabbit review findings --clear

# Review a GitHub repository without a local clone
coderabbit review --remote acme/app --base main --source-branch my-feature
```

> [!NOTE]
>
> * Plain text is the default review mode.
> * Use `coderabbit auth login --agent` for agent-driven OAuth login.
> * `--remote` requires `--base` and `--source-branch`, and runs outside any git checkout.

#### review findings

Show the most recent local review with stored findings

Usage: `coderabbit review findings [options]`

| Option | Description |
| - | - |
| `--dir <path>` | Review directory to read findings for |
| `--clear` | Dismiss stored findings for this scope so they stop being surfaced |

```bash Examples theme={null}
# Show the most recent local review with stored findings
coderabbit review findings

# Show findings stored for a scoped review directory
coderabbit review findings --dir src

# Dismiss all stored findings for this scope
coderabbit review findings --clear
```

> [!NOTE]
>
> * A newer review with no stored findings does not hide older findings.
> * Clearing is scoped to the review directory, current branch, and base branch.
> * Findings stored under any other scope are left unchanged.

### pullrequest

Read existing CodeRabbit output without starting a review. Requires exactly one of `--show-prompts` or `--show-threads`.

Usage: `coderabbit pullrequest [options] <number-or-url>`

This command reads CodeRabbit's existing output for the pull request and does not start a review. Pass exactly one of `--show-prompts` or `--show-threads`: the command fails without one, and the two cannot be combined. If no prompt is found, check that [`reviews.enable_prompt_for_ai_agents`](https://docs.coderabbit.ai/reference/configuration#param-reviews-enable-prompt-for-ai-agents) is enabled in the configuration and that CodeRabbit has finished reviewing the pull request.

The command needs a CodeRabbit SaaS login or a stored API key, and self-hosted logins are not supported. Unlike `coderabbit review`, it does not start sign-in for you: if you have neither, run [`coderabbit auth login`](https://docs.coderabbit.ai/cli/reference#auth-login) first.

| Argument | Description |
| - | - |
| `<number-or-url>` | GitHub pull request number or URL |

| Option | Description |
| - | - |
| `--show-prompts` | Print the consolidated prompt for AI agents |
| `--show-threads` | Print CodeRabbit inline review-thread roots as JSON |
| `--agent` | Output newline-delimited JSON for agent integrations |

```bash Examples theme={null}
coderabbit pullrequest https://github.com/org/repo/pull/123 --show-prompts
coderabbit pullrequest https://github.com/org/repo/pull/123 --show-prompts --agent

# Read current inline thread roots
coderabbit pullrequest 123 --show-threads --agent

# Resolve the repository from local origin
coderabbit pullrequest 123 --show-prompts
```

> [!NOTE]
>
> * CodeRabbit SaaS sign-in or a stored agentic API key is required; the repository must be installed in the active organization.
> * Only github.com pull requests are supported. A full URL works outside a git checkout.

### stats

Show statistics from locally stored review history

Usage: `coderabbit stats [options]`

| Option | Description |
| - | - |
| `--rebuild` | Rebuild stats by rescanning review history |

```bash Examples theme={null}
# Show stats (builds on first run)
coderabbit stats

# Rescan review history and rebuild stats
coderabbit stats --rebuild
```

### usage

Show included-review availability and billing-period usage

Usage: `coderabbit usage [options]`

| Option | Description |
| - | - |
| `--agent` | Emit NDJSON usage, shared review cap, and credit balances when permitted |

```bash Examples theme={null}
# Show included reviews and billing-period usage
coderabbit usage

# Emit one machine-readable usage event
coderabbit usage --agent

# Same, via the default review command
coderabbit --usage
```

### update

Update CodeRabbit CLI to the latest version

Usage: `coderabbit update [options]`

When a newer version is available and Homebrew manages your installation, `coderabbit update` installs nothing. It prints the new version and the `brew upgrade coderabbit` command, then exits with status `0`, so a script can't treat a successful exit as proof that the CLI was updated. On Windows, the update finishes after the command exits; see [Update CodeRabbit CLI](https://docs.coderabbit.ai/cli/windows.md#update-coderabbit-cli).

```bash Examples theme={null}
# Check for and install updates
coderabbit update
```

> [!NOTE]
>
> Homebrew installations must be updated with `brew upgrade coderabbit`.

### config

Create or configure repository settings through a guided flow

Usage: `coderabbit config [options] [command]`

| Option | Description |
| - | - |
| `--agent` | Emit structured state for agent-guided setup without prompts |
| `--profile <profile>` | Review style for an agent-generated Standard proposal Choices: `chill`, `quiet`, `assertive`, `default` |
| `--generate` | Create or configure the repository settings (default) |
| `--detailed` | Manual setup: review style and path guidance (full setup via /config) |

```bash Examples theme={null}
coderabbit config
coderabbit config --generate
coderabbit config --detailed
coderabbit config --agent
coderabbit config --agent --generate
```

Schema: [https://www.coderabbit.ai/integrations/schema.v2.json](https://www.coderabbit.ai/integrations/schema.v2.json)

### doctor

Check CodeRabbit CLI installation and local review readiness

Usage: `coderabbit doctor [options]`

### skills

Install, update, or uninstall CodeRabbit skills for detected coding agents.

Usage: `coderabbit skills [options] [command]`

| Option | Description |
| - | - |
| `--agent` | Preview changes for approval in an agent conversation |
| `--confirm <plan-hash>` | Apply the exact previewed plan after user approval, without prompting |

| Command | Description |
| - | - |
| [`install [options]`](#skills-install) | Install missing skills and update existing skills |
| [`update [options]`](#skills-update) | Update existing skills without installing missing skills |
| [`uninstall [options]`](#skills-uninstall) | Uninstall skills owned by the CodeRabbit CLI |

```bash Examples theme={null}
coderabbit skills install
coderabbit skills update
coderabbit skills uninstall
```

Install also updates existing skills. Use `--agent` on a subcommand to preview a read-only plan for approval, then run its exact action\_required command.

#### skills install

Install missing skills and update existing skills

Usage: `coderabbit skills install [options]`

| Option | Description |
| - | - |
| `--agent` | Preview changes for approval in an agent conversation |
| `--confirm <plan-hash>` | Apply the exact previewed plan after user approval, without prompting |

Agent flow: run `coderabbit skills install --agent`, obtain approval for the complete plan, then run the exact command in the action\_required record.

#### skills update

Update existing skills without installing missing skills

Usage: `coderabbit skills update [options]`

| Option | Description |
| - | - |
| `--agent` | Preview changes for approval in an agent conversation |
| `--confirm <plan-hash>` | Apply the exact previewed plan after user approval, without prompting |

Agent flow: run `coderabbit skills update --agent`, obtain approval for the complete plan, then run the exact command in the action\_required record.

#### skills uninstall

Uninstall skills owned by the CodeRabbit CLI

Usage: `coderabbit skills uninstall [options]`

| Option | Description |
| - | - |
| `--agent` | Preview changes for approval in an agent conversation |
| `--confirm <plan-hash>` | Apply the exact previewed plan after user approval, without prompting |

Marketplace plugins, npx-managed skills, project copies, and other externally owned skills are never removed.

### code

Use the same Coding Agent and skill library as the web app. Coding Agent commands are in beta.

Usage: `coderabbit code [options] [command]`

Every `coderabbit code` command needs a CodeRabbit SaaS user login and acts in your selected organization. API key, self-hosted, and SSO workspace logins are not supported ([requirements](https://docs.coderabbit.ai/cli/cloud-tasks.md#requirements)). If no organization is selected, run [`coderabbit auth org`](https://docs.coderabbit.ai/cli/reference#auth-org) in an interactive terminal first. To learn what the cloud Coding Agent does with the work you send it, see [Coding Agent](https://docs.coderabbit.ai/code/index.md).

| Command | Description |
| - | - |
| [`handoff [options]`](#code-handoff) | Continue a local coding session in a new cloud task |
| [`ls [options]`](#code-ls) | List your cloud Coding Agent tasks |
| [`show [options] <task>`](#code-show) | Show a cloud Coding Agent task |
| [`new [options] [prompt]`](#code-new) | Start a cloud Coding Agent task |
| [`goal [options] <task>`](#code-goal) | Read, set, or clear a cloud task's goal |
| [`resume [options] [task]`](#code-resume) | Follow and continue a cloud Coding Agent task |
| [`cancel [options] <task>`](#code-cancel) | Stop the running turn of a cloud Coding Agent task |
| [`archive [options] <task>`](#code-archive) | Archive a cloud Coding Agent task |
| [`ask [options] <task> <question>`](#code-ask) | Ask a side question about a cloud Coding Agent task |
| [`plan [options] <task>`](#code-plan) | Show or approve the plan of a cloud Coding Agent task |
| [`push [options] <task>`](#code-push) | Push the changes of a cloud Coding Agent task |
| [`autofix\|autopilot [options] <action> [task]`](#code-autofix) | Control Autofix for a cloud task or pull request |
| [`skills`](#code-skills) | Manage cloud Coding Agent skills |

#### code handoff

Create a new CodeRabbit Cloud task with a summary, optional plan, and automatically discovered session transcript

Usage: `coderabbit code handoff [options]`

`--summary` is required. Run the command from a clean checkout of a branch that has an `origin` remote. Untracked files count as changes, so keep the summary and plan files outside the repository or commit them first. For what is uploaded and what happens next, see [Continue a local session in the cloud](https://docs.coderabbit.ai/cli/cloud-tasks.md#continue-a-local-session-in-the-cloud).

| Option | Description |
| - | - |
| `--summary <path\|->` | Session summary file, or - to read from stdin (required) |
| `--plan <path>` | Primary implementation plan file |
| `--agent` | Emit newline-delimited JSON for agent workflows |
| `--access <mode>` | Request repository access after creation; full requires browser authorization Choices: `manual`, `full` |

#### code ls

List the 20 most recently updated cloud tasks in the selected organization. Only your tasks are listed unless you pass `--all`. Archived tasks are not listed.

Usage: `coderabbit code ls [options]`

| Option | Description |
| - | - |
| `--status <state>` | Only list tasks in this web task list state Choices: `needs_attention`, `ready_for_review`, `running`, `completed`, `canceled` |
| `--repo <path>` | Only list tasks for the Git repository at this path, for example . |
| `--all` | Include tasks from other people in the organization |
| `--agent` | Emit newline-delimited JSON for agent workflows |

#### code show

Show the status, repository, delivery, and pull request health of a cloud task.

Usage: `coderabbit code show [options] <task>`

| Argument | Description |
| - | - |
| `<task>` | Task ID or task URL |

| Option | Description |
| - | - |
| `--agent` | Emit newline-delimited JSON for agent workflows |

#### code new

Start a cloud task on the current branch of the Git repository in this directory. The task starts from that branch on origin. Local commits that are not pushed and uncommitted changes are not included.

Usage: `coderabbit code new [options] [prompt]`

| Argument | Description |
| - | - |
| `[prompt]` | What the agent should do, or - to read it from stdin. Interactive mode prompts when omitted; agent mode requires it |

| Option | Description |
| - | - |
| `--plan` | Start in Plan mode: the agent writes a plan for review instead of changing code |
| `--resume` | Follow the task after it starts, as `coderabbit code resume` does |
| `--goal` | Start in Goal mode, using the prompt as the goal (1–4,000 characters) |
| `--goal-objective <text>` | Use a separate goal objective with `--goal` |
| `--agent` | Emit newline-delimited JSON for agent workflows |
| `--access <mode>` | Request repository access after creation; full requires browser authorization Choices: `manual`, `full` |
| `--private` | Create a task visible only to you from the start Default: `false` |

#### code goal

Read the goal by default. Setting an objective preserves paused/limited states; editing a completed goal restarts it. Clearing removes the goal. Use code cancel to stop a turn and code resume `-m` to send instructions.

Usage: `coderabbit code goal [options] <task>`

| Argument | Description |
| - | - |
| `<task>` | Task ID or task URL |

| Option | Description |
| - | - |
| `--set <objective>` | Set the goal (1–4,000 characters), or - to read stdin |
| `--clear` | Remove the goal |
| `--agent` | Emit newline-delimited JSON for agent workflows |

#### code resume

Open a cloud task in the terminal. Shows its trace and live updates, and lets you send messages, steer the running turn, answer agent questions, and stop the turn. Closing the view does not stop the task. With `--agent`, send at most one message, steer, or answer, then stream newline-delimited JSON until the turn ends, the agent asks a blocking question, or 9 minutes pass. Add `--interactive` for a persistent bidirectional NDJSON session: send message, steer, answer, cancel, show, or close requests on stdin; receive correlated responses and live trace events on stdout. EOF detaches without stopping the task.

Usage: `coderabbit code resume [options] [task]`

| Argument | Description |
| - | - |
| `[task]` | Task ID or task URL. In a terminal, omit it to pick one of your recent tasks; with `--agent`, pass it or `--last` |

| Option | Description |
| - | - |
| `--last` | Use your most recently updated task for the Git repository in the current directory |
| `-m, --message <message>` | With `--agent`: send a message. Use - to read it from stdin |
| `--steer <message>` | With `--agent`: steer the running turn. Use - to read it from stdin |
| `--answer <json>` | With `--agent`: answer the pending question with the JSON from its answerTemplate. Use - to read it from stdin |
| `--agent` | Emit newline-delimited JSON for agent workflows |
| `--interactive` | With `--agent`: keep a bidirectional NDJSON session open on piped stdin |

#### code cancel

Stop the running turn. Queued messages do not run after it: the server pauses or drops them. The task stays open: a new message starts a new turn.

Usage: `coderabbit code cancel [options] <task>`

| Argument | Description |
| - | - |
| `<task>` | Task ID or task URL |

| Option | Description |
| - | - |
| `--agent` | Emit newline-delimited JSON for agent workflows |

#### code archive

Archive one task without prompting: hide it from the active task list, make it read-only, and pause its schedules. It can be unarchived later. Running, starting, or stopping turns must finish first. Repeating an archive succeeds. This does not cancel turns or delete tasks.

Usage: `coderabbit code archive [options] <task>`

| Argument | Description |
| - | - |
| `<task>` | Task ID or task URL |

| Option | Description |
| - | - |
| `--agent` | Emit newline-delimited JSON for agent workflows |

#### code ask

Ask the task's side chat a question and print the answer. A side chat reads the task's conversation and repository. It does not change the task, and the turn of the task keeps running. Each question is billed. The side chat stays open for follow-up questions: pass `--follow-up` with the turn ID of an earlier answer to keep its context. A task can have 3 open side chats. An idle side chat expires after 24 hours. The CLI cannot close a side chat, so ask later questions about the task with `--follow-up`. The command waits up to 3 minutes for the task's environment and up to 15 minutes for the answer.

Usage: `coderabbit code ask [options] <task> <question>`

| Argument | Description |
| - | - |
| `<task>` | Task ID or task URL |
| `<question>` | The question. Use - to read it from stdin |

| Option | Description |
| - | - |
| `--follow-up <turn-id>` | Ask in the side chat of an earlier answer. Pass the turn ID that the answer printed |
| `--agent` | Emit newline-delimited JSON for agent workflows |

#### code plan

Show the latest finalized plan of a cloud task. With `--approve`, record your approval of that plan version. You cannot approve the plan of a task that you started, and approval does not start implementation.

Usage: `coderabbit code plan [options] <task>`

| Argument | Description |
| - | - |
| `<task>` | Task ID or task URL |

| Option | Description |
| - | - |
| `--approve` | Approve the latest plan version as a reviewer |
| `--agent` | Emit newline-delimited JSON for agent workflows |

#### code push

Deliver the ready changes of a cloud task and wait until the delivery finishes. By default, CodeRabbit commits and pushes the changes, as the web app's Commit and push action does. GitHub can first ask you to authorize CodeRabbit in a browser that is signed in to CodeRabbit.

Usage: `coderabbit code push [options] <task>`

| Argument | Description |
| - | - |
| `<task>` | Task ID or task URL |

| Option | Description |
| - | - |
| `--stacked` | Open a new pull request with the changes, as the web app's Create PR action does |
| `--agent` | Emit newline-delimited JSON for agent workflows |

#### code autofix

Autofix publishes the task's changes when the agent finishes, then fixes CodeRabbit findings, required CI, and merge conflicts. `on` starts it, `off` stops it, `resume` starts a new repair episode after a pause, and `status` shows its state. Activation does not confirm a repair turn started; a failed task may need to be retried or continued before resuming Autofix. `recover` resolves a pending delivery conflict while preserving unpublished work; `resume` after recovery finishes. Pass exactly one target: a task ID or URL, or `--pr` `<number|url>`. `on`, `resume` and `recover` check Coding Agent billing; `on` and `resume` with `--pr` can create an Autofix task for the pull request.

Usage: `coderabbit code autofix|autopilot [options] <action> [task]`

| Argument | Description |
| - | - |
| `<action>` | `on`, `off`, `resume`, `recover`, or `status` |
| `[task]` | Task ID or task URL |

| Option | Description |
| - | - |
| `--pr <number\|url>` | Target a pull request: a number in the current repository, or a GitHub pull request or GitLab merge request URL |
| `--agent` | Emit newline-delimited JSON for agent workflows |

#### code skills

Manage cloud Coding Agent skills

Usage: `coderabbit code skills [options] [command]`

| Command | Description |
| - | - |
| [`import [options] [path]`](#code-skills-import) | Import local agent skills into your cloud library |

#### code skills import

Choose an agent, select local skills, and review their import into the cloud library. Pass a skill folder or SKILL.md to import one directly. With `--yes` and no `--scope`, new skills are personal within the selected organization and existing skills keep their visibility. Importing an owned skill with the same name publishes a new version. Noninteractive imports require a path and `--yes`.

Usage: `coderabbit code skills import [options] [path]`

| Argument | Description |
| - | - |
| `[path]` | Skill folder or its SKILL.md |

| Option | Description |
| - | - |
| `--scope <scope>` | Who can use the imported skill Choices: `personal`, `organization` |
| `--yes` | Upload the specified path without prompting |

### completion

Print the shell completion script for `coderabbit` and `cr`. It completes commands, options, and the task IDs that this computer listed or opened.

Usage: `coderabbit completion [options] <shell>`

| Argument | Description |
| - | - |
| `<shell>` | Shell type for completion script Choices: `zsh`, `bash`, `fish`, `powershell` |

```bash Examples theme={null}
# Add to ~/.bashrc
eval "$(coderabbit completion bash)"

# Add to ~/.zshrc, after compinit
eval "$(coderabbit completion zsh)"

# Add to ~/.config/fish/config.fish
coderabbit completion fish | source

# Add to $PROFILE
coderabbit completion powershell | Out-String | Invoke-Expression
```

> [!NOTE]
>
> * The script completes `coderabbit` and the `cr` alias.
> * Task IDs come from the tasks that this computer listed or opened with `coderabbit code`. A Tab press makes no network call.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.