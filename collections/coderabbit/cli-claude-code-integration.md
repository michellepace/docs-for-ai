> ## Documentation Index
> Fetch the complete documentation index at: https://docs.coderabbit.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code integration

> AI-powered code review in Claude Code through the CodeRabbit plugin. Let AI code, review, and fix issues autonomously without human intervention.

## Autonomous AI development workflows

The CodeRabbit plugin for Claude Code creates autonomous AI development workflows. Claude Code can trigger CodeRabbit reviews directly through simple commands, enabling you to build features, run code reviews, and fix issues without manual intervention.

This integration makes AI coding more independent, with built-in quality gates that catch issues before they reach production.

> [!NOTE]
>
> This guide covers integrating CodeRabbit CLI with Claude Code. For standalone
> CLI usage, see [CLI overview](https://docs.coderabbit.ai/cli.md).

> [!NOTE]
>
> If you run Claude Code in a cloud environment with restricted outbound access, allow the CodeRabbit CLI domains before installation and review the non-browser authentication and secret-handling guidance. See [CLI network requirements](https://docs.coderabbit.ai/cli/network-requirements.md).

CodeRabbit analyzes your code changes and surfaces specific issues, then Claude Code applies fixes based on CodeRabbit's context-rich feedback.

## Why integrate these tools

> [card] Expert issue detection
>
> CodeRabbit spots race conditions, memory leaks, and logic errors that generic linters miss. Same pattern recognition that powers our PR reviews.

> [card] AI-powered fixes
>
> Claude Code implements fixes with full context from CodeRabbit's analysis.
> Complex architectural changes handled intelligently.

> [card] Context preservation
>
> CodeRabbit provides Claude Code with succinct context about issues,
> including location, severity, and suggested approaches.

> [card] Continuous workflow
>
> Stay in development flow - run reviews, apply fixes, and iterate without switching tools or losing mental context.

## Video demo

See CodeRabbit CLI in action with Claude Code:

[YouTube video player](https://www.youtube.com/embed/1mkvnU5iG1g)

## Installation

**1. Install Claude Code**

Install Claude Code following the platform-specific instructions. Ensure you can launch Claude Code from your terminal.

**2. Install and authenticate CodeRabbit CLI**

Install and authenticate the CodeRabbit CLI:

> [tab] Install script
>
> ```bash theme={null}
> curl -fsSL https://cli.coderabbit.ai/install.sh | sh
> ```
>
> If `coderabbit` is not available immediately after installation, start a new shell, or run the exact shell-specific reload command printed under **Next steps**. If the install script offers browser sign-in without first asking for a region, EU users should skip it and authenticate later with an explicit `--region eu`.

> [tab] Homebrew
>
> ```bash theme={null}
> brew install coderabbit
> ```
>
> If `coderabbit` is not available immediately after installation, start a new shell.

> [tab] Windows
>
> ```powershell PowerShell theme={null}
> irm https://cli.coderabbit.ai/install.ps1 | iex
> ```
>
> See [Install CodeRabbit CLI on Windows](https://docs.coderabbit.ai/cli/windows.md) for prerequisites, version pinning, and troubleshooting. If `coderabbit` is not available immediately after installation, open a new PowerShell window.

```bash Authenticate theme={null}
coderabbit auth login
```

For a first login to an EU-hosted CodeRabbit account, use `coderabbit auth login --region eu`. When no region is specified or saved, the CLI uses the US region.

A browser window opens automatically. Sign in to CodeRabbit and the authentication completes in the browser.

If you belong to multiple CodeRabbit organizations, the sign-in choice sets your default org only. Review attribution still depends on the current repository. See [Organization selection](https://docs.coderabbit.ai/cli.md#organization-selection).

**3. Install CodeRabbit plugin**

In Claude Code, install the plugin using one of these methods:

```bash Claude Code theme={null}
/plugin install coderabbit
```

```bash Command-line interface theme={null}
claude plugin install coderabbit
```

**4. Verify installation**

The plugin will automatically verify your CodeRabbit CLI installation and authentication when first used. You can also test it with:

```bash theme={null}
/coderabbit:coderabbit-review
```

## Usage

### Running code reviews

Use the [`/coderabbit:coderabbit-review`](#usage) command to trigger a review:

```bash theme={null}
/coderabbit:coderabbit-review
```

The command will:

* Verify CLI installation and authentication
* Run the code review
* Present findings grouped by severity

### Review options

Customize your review with these options:

```bash theme={null}
/coderabbit:coderabbit-review                    # Review tracked changes
/coderabbit:coderabbit-review --committed         # Only committed changes
/coderabbit:coderabbit-review --uncommitted       # Staged and tracked local edits
/coderabbit:coderabbit-review --include-untracked # Include raw untracked files
/coderabbit:coderabbit-review --base main        # Compare against main branch
```

### Natural language interface

You can also trigger reviews using natural language:

* "Review my code"
* "Check for security issues"
* "What's wrong with my changes?"

Claude Code will automatically invoke the CodeRabbit plugin to perform the review.

## Integration workflow

### Use CodeRabbit as part of building new features

**1. Request implementation + review**

Ask Claude Code to implement a feature and run a CodeRabbit review:

```text Sample prompt wrap theme={null}
Please implement phase 7.3 of the planning doc and then review it with CodeRabbit. Fix any issues that are found.
```

Key components:

* **Implement the feature**: Claude codes the requested functionality
* **Run CodeRabbit review**: Uses the plugin to analyze code
* **Fix issues**: Claude addresses all problems CodeRabbit identifies

**2. Claude implements and triggers review**

Claude Code:

1. Implements the requested feature
2. Runs `/coderabbit:coderabbit-review` through the plugin
3. Waits for the analysis to complete

**3. CodeRabbit analysis and task creation**

When CodeRabbit completes, Claude Code:

1. Receives the review findings with file locations and severity
2. Creates a task list addressing each issue
3. Shows you the planned fixes before implementing them

**4. Automated issue resolution**

Claude Code systematically works through the task list, implementing fixes for each CodeRabbit finding. The cycle continues until all critical issues are resolved.

### Example: API integration implementation

This example shows the workflow implementing a webhook handler for payment processing:

**1. Start implementation**

```bash theme={null}
# Working on payment webhook feature
git checkout -b feature/payment-webhooks
```

**2. Run integrated workflow**

Tell Claude Code to implement and review:

```
Implement the payment webhook handler from the spec document.
Then review it with CodeRabbit and fix any issues.
```

**3. CodeRabbit analysis**

CodeRabbit analyzes the webhook code and identifies issues:

* Missing signature verification
* Race conditions in payment state updates
* Insufficient error handling for network failures
* Webhook replay attack vulnerabilities

**4. Claude Code fixes**

Claude Code automatically applies fixes:

* Adds HMAC signature verification
* Implements database transactions for state consistency
* Adds retry logic with exponential backoff
* Includes idempotency key handling

**5. Verification**

The workflow continues until all critical issues are resolved. Claude Code
reports completion.

## Advanced usage

### CLI review commands

When running the CodeRabbit CLI directly outside the plugin, use the review command that best fits your workflow:

```bash theme={null}
# Agent mode - NDJSON output (one JSON object per line) for agent workflows
coderabbit --agent

# Default mode - detailed terminal output
coderabbit review

# Deeper review using the GitHub PR review policy
coderabbit --deep
```

Deep review requires CLI 0.8.0 and a compatible server. See [deep review behavior and compatibility](https://docs.coderabbit.ai/cli.md#review-modes).

| Command | Best for |
| - | - |
| `--agent` | Claude Code and other agent integrations that consume structured data |
| `coderabbit review` | Human-readable terminal output during manual workflows |
| `--deep` | Deeper review using the GitHub PR review policy |

The `/coderabbit:coderabbit-review` plugin command uses the appropriate mode automatically.

### Reviewing specific changes

Review only uncommitted changes:

```bash theme={null}
/coderabbit:coderabbit-review --uncommitted
```

Review only committed changes:

```bash theme={null}
/coderabbit:coderabbit-review --committed
```

### Comparing against different branches

Compare your changes against a specific branch:

```bash theme={null}
/coderabbit:coderabbit-review --base develop
/coderabbit:coderabbit-review --base master
```

### Combining with natural language

You can combine natural language requests with specific review options:

```
Review my uncommitted changes for security issues
```

Claude Code will interpret this and run the appropriate [`/coderabbit:coderabbit-review`](#usage) command with the correct options.

## Configuration

### Configure CodeRabbit for Claude Code

Pass your Claude context file with `coderabbit review -c CLAUDE.md` so CodeRabbit can include how code reviews should run, your coding standards, and architectural preferences.

Essentials Plan (Passing a context file to CodeRabbit CLI is available on Essentials and higher paid plans.)

## Troubleshooting

### Plugin not found

If the plugin isn't available:

1. **Refresh the marketplace**: Update the official marketplace catalog:
   ```bash theme={null}
   /plugin marketplace update
   ```
2. **Check plugin installation**: Verify the plugin is installed:
   ```bash theme={null}
   /plugin list
   ```
3. **Reinstall if needed**: Remove and reinstall the plugin:
   ```bash theme={null}
   /plugin uninstall coderabbit
   /plugin install coderabbit
   ```

### CLI not authenticated

If the agent cannot find `coderabbit`, check the trusted CLI installation in your host terminal. A missing `PATH` entry does not mean it is uninstalled. Use the quoted absolute path to that installation for the commands below, not a repository-local executable or wrapper.

`credentials_unavailable` and `callback_listener_unavailable` indicate local access failures, not proof that you are signed out. For local sessions:

1. **Check host authentication**: Run `"/absolute/path/to/coderabbit" auth status --agent` in your host terminal. In a local agent sandbox, use approved command-scoped host execution for this status check and the review. Network permission alone does not expose host credentials. If host execution is unavailable or denied, stop and report that prerequisite; do not weaken global sandbox settings.
2. **Recover a sandbox failure**: If host status reports `authenticated: true`, you do not need to log in again. When the original review failed authentication in the sandbox before analysis began, retry it once on the host with the same working directory and arguments. Do not retry a running or completed review, a failure after analysis began, or a review that already failed on the host.
3. **Log in only when signed out**: If the host check succeeds and reports `authenticated: false`, run `"/absolute/path/to/coderabbit" auth login` yourself in the host terminal, then confirm authentication before retrying. If status fails or remains unavailable, stop and report the error.

Remote sessions need authentication configured in their own environment. Let the CLI access its credentials directly; never copy tokens from the host credential store or paste them into the agent.

### CodeRabbit not finding issues

If CodeRabbit isn't detecting expected issues:

1. **Check git status**: CodeRabbit analyzes tracked changes by default. Run `git status` to verify the scope; brand-new untracked files require `--include-untracked`.
2. **Specify review scope**: Use options to target specific changes:
   * [`/coderabbit:coderabbit-review --uncommitted`](#reviewing-specific-changes) - staged and tracked local edits
   * [`/coderabbit:coderabbit-review --committed`](#reviewing-specific-changes) - only committed changes
3. **Specify base branch**: If your main branch isn't `main`, use:
   * [`/coderabbit:coderabbit-review --base develop`](#comparing-against-different-branches)
   * [`/coderabbit:coderabbit-review --base master`](#comparing-against-different-branches)

### Claude Code not applying fixes

If Claude Code isn't implementing CodeRabbit's suggestions:

1. **Provide explicit context**: Tell Claude Code to "fix the issues found by CodeRabbit" explicitly
2. **Check review completion**: Ensure the review has finished before asking for fixes
3. **Review findings manually**: Ask Claude to "show me the CodeRabbit findings" to verify they were received
4. **Iterate on specific issues**: Ask Claude to focus on fixing specific issues one at a time

### Review taking too long

CodeRabbit reviews may take 7 to 30+ minutes depending on the scope of changes:

1. **Review smaller changesets**: Adjust what you're reviewing to reduce analysis time:
   * Use [`/coderabbit:coderabbit-review --uncommitted`](#reviewing-specific-changes) to review only uncommitted changes
   * Work on smaller feature branches compared to main
   * Break large features into smaller, reviewable chunks
2. **Configure the diff scope**: Control what changes are analyzed:
   * **Review uncommitted changes only**: Use the `--uncommitted` flag to analyze staged and tracked local edits
   * **Configure base branch**: Use `--base` to set the comparison point
   * **Use feature branches**: Work on focused feature branches instead of large staging branches

> [!NOTE]
>
> The integration creates a more thorough review process than either tool alone.
> Expect comprehensive analysis that catches issues that would otherwise reach
> production.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.