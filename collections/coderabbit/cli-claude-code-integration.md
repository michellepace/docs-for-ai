> ## Documentation Index
> Fetch the complete documentation index at: https://docs.coderabbit.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code integration

> AI-powered code review in Claude Code through the CodeRabbit plugin. Let AI code, review, and fix issues autonomously without human intervention.

## Autonomous AI development workflows

The CodeRabbit plugin for Claude Code creates autonomous AI development workflows. Claude Code can trigger CodeRabbit reviews directly through simple commands, enabling you to build features, run code reviews, and fix issues without manual intervention.

This integration makes AI coding more independent, with built-in quality gates that catch issues before they reach production.

<Info>
  This guide covers integrating CodeRabbit CLI with Claude Code. For standalone
  CLI usage, see [CLI overview](/cli/).
</Info>

<Warning>
  **Windows users:** Claude Code requires WSL (Windows Subsystem for Linux) to
  run on Windows. See our [WSL on Windows guide](/cli/wsl-windows) for setup
  instructions before proceeding with this integration.
</Warning>

CodeRabbit analyzes your code changes and surfaces specific issues, then Claude Code applies fixes based on CodeRabbit's context-rich feedback.

## Why integrate these tools

<CardGroup cols={2}>
  <Card title="Expert issue detection" icon="search">
    CodeRabbit spots race conditions, memory leaks, and logic errors that generic linters miss. Same pattern recognition that powers our PR reviews.
  </Card>

  <Card title="AI-powered fixes" icon="wand">
    Claude Code implements fixes with full context from CodeRabbit's analysis.
    Complex architectural changes handled intelligently.
  </Card>

  <Card title="Context preservation" icon="brain">
    CodeRabbit provides Claude Code with succinct context about issues,
    including location, severity, and suggested approaches.
  </Card>

  <Card title="Continuous workflow" icon="refresh-cw">
    Stay in development flow - run reviews, apply fixes, and iterate without switching tools or losing mental context.
  </Card>
</CardGroup>

## Video demo

See CodeRabbit CLI in action with Claude Code:

<iframe className="w-full aspect-video rounded-xl" src="https://www.youtube.com/embed/1mkvnU5iG1g" title="YouTube video player" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen />

## Installation

<Steps>
  <Step title="Install Claude Code">
    Install Claude Code following the platform-specific instructions. Ensure you can launch Claude Code from your terminal.
  </Step>

  <Step title="Install and authenticate CodeRabbit CLI">
    Install and authenticate the CodeRabbit CLI:

    <CodeGroup>
      ```bash Installation script theme={null}
      curl -fsSL https://cli.coderabbit.ai/install.sh | sh
      ```

      ```bash Homebrew theme={null}
      brew install coderabbit
      ```
    </CodeGroup>

    ```bash Authenticate theme={null}
    coderabbit auth login
    ```

    A browser window opens automatically. Sign in to CodeRabbit and the authentication completes in the browser.

    If you belong to multiple CodeRabbit organizations, the sign-in choice sets your default org only. Review attribution still depends on the current repository. See [Organization selection](/cli#organization-selection).
  </Step>

  <Step title="Install CodeRabbit plugin">
    In Claude Code, install the plugin using one of these methods:

    <CodeGroup>
      ```bash Claude Code theme={null}
      /plugin install coderabbit
      ```

      ```bash Command-line interface theme={null}
      claude plugin install coderabbit
      ```
    </CodeGroup>
  </Step>

  <Step title="Verify installation">
    The plugin will automatically verify your CodeRabbit CLI installation and authentication when first used. You can also test it with:

    ```bash theme={null}
    /coderabbit:review
    ```
  </Step>
</Steps>

## Usage

### Running code reviews

Use the [`/coderabbit:review`](#usage) command to trigger a review:

```bash theme={null}
/coderabbit:review
```

The command will:

* Verify CLI installation and authentication
* Run the code review
* Present findings grouped by severity

### Review options

Customize your review with these options:

```bash theme={null}
/coderabbit:review                    # Review tracked changes
/coderabbit:review committed          # Only committed changes
/coderabbit:review uncommitted        # Staged and tracked local edits
/coderabbit:review --include-untracked # Include raw untracked files
/coderabbit:review --base main        # Compare against main branch
```

### Natural language interface

You can also trigger reviews using natural language:

* "Review my code"
* "Check for security issues"
* "What's wrong with my changes?"

Claude Code will automatically invoke the CodeRabbit plugin to perform the review.

## Integration workflow

### Use CodeRabbit as part of building new features

<Steps>
  <Step title="Request implementation + review">
    Ask Claude Code to implement a feature and run a CodeRabbit review:

    ```text Sample prompt wrap theme={null}
    Please implement phase 7.3 of the planning doc and then review it with CodeRabbit. Fix any issues that are found.
    ```

    Key components:

    * **Implement the feature**: Claude codes the requested functionality
    * **Run CodeRabbit review**: Uses the plugin to analyze code
    * **Fix issues**: Claude addresses all problems CodeRabbit identifies
  </Step>

  <Step title="Claude implements and triggers review">
    Claude Code:

    1. Implements the requested feature
    2. Runs `/coderabbit:review` through the plugin
    3. Waits for the analysis to complete
  </Step>

  <Step title="CodeRabbit analysis and task creation">
    When CodeRabbit completes, Claude Code:

    1. Receives the review findings with file locations and severity
    2. Creates a task list addressing each issue
    3. Shows you the planned fixes before implementing them
  </Step>

  <Step title="Automated issue resolution">
    Claude Code systematically works through the task list, implementing fixes for each CodeRabbit finding. The cycle continues until all critical issues are resolved.
  </Step>
</Steps>

### Example: API integration implementation

This example shows the workflow implementing a webhook handler for payment processing:

<Steps>
  <Step title="Start implementation">
    ```bash theme={null}
    # Working on payment webhook feature
    git checkout -b feature/payment-webhooks
    ```
  </Step>

  <Step title="Run integrated workflow">
    Tell Claude Code to implement and review:

    ```
    Implement the payment webhook handler from the spec document.
    Then review it with CodeRabbit and fix any issues.
    ```
  </Step>

  <Step title="CodeRabbit analysis">
    CodeRabbit analyzes the webhook code and identifies issues:

    * Missing signature verification
    * Race conditions in payment state updates
    * Insufficient error handling for network failures
    * Webhook replay attack vulnerabilities
  </Step>

  <Step title="Claude Code fixes">
    Claude Code automatically applies fixes:

    * Adds HMAC signature verification
    * Implements database transactions for state consistency
    * Adds retry logic with exponential backoff
    * Includes idempotency key handling
  </Step>

  <Step title="Verification">
    The workflow continues until all critical issues are resolved. Claude Code
    reports completion.
  </Step>
</Steps>

## Advanced usage

### CLI review commands

When running the CodeRabbit CLI directly outside the plugin, use the review command that best fits your workflow:

```bash theme={null}
# Agent mode - structured JSON output for agent workflows
coderabbit --agent

# Default mode - detailed terminal output
coderabbit review

# Lighter local review policy
coderabbit --light
```

| Command             | Best for                                                              |
| ------------------- | --------------------------------------------------------------------- |
| `--agent`           | Claude Code and other agent integrations that consume structured data |
| `coderabbit review` | Human-readable terminal output during manual workflows                |
| `--light`           | Lighter local review for active development work                      |

The `/coderabbit:review` plugin command uses the appropriate mode automatically.

### Reviewing specific changes

Review only uncommitted changes:

```bash theme={null}
/coderabbit:review uncommitted
```

Review only committed changes:

```bash theme={null}
/coderabbit:review committed
```

### Comparing against different branches

Compare your changes against a specific branch:

```bash theme={null}
/coderabbit:review --base develop
/coderabbit:review --base master
```

### Combining with natural language

You can combine natural language requests with specific review options:

```
Review my uncommitted changes for security issues
```

Claude Code will interpret this and run the appropriate [`/coderabbit:review`](#usage) command with the correct options.

## Configuration

### Configure CodeRabbit for Claude Code

Pass your Claude context file with `coderabbit review -c CLAUDE.md` so CodeRabbit can include how code reviews should run, your coding standards, and architectural preferences.

<Info>This is a Pro paid plan feature.</Info>

## Troubleshooting

### Plugin not found

If the plugin isn't available:

1. **Verify marketplace access**: Ensure you've added the marketplace:
   ```bash theme={null}
   /plugin marketplace add coderabbitai/claude-plugin
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

If you see authentication errors:

1. **Check CLI authentication**: Run `coderabbit auth status` in your terminal
2. **Re-authenticate**: Run `coderabbit auth login` to refresh your credentials
3. **Verify CLI installation**: Ensure the CLI is in your PATH and accessible from Claude Code's environment

### CodeRabbit not finding issues

If CodeRabbit isn't detecting expected issues:

1. **Check git status**: CodeRabbit analyzes tracked changes by default. Run `git status` to verify the scope; brand-new untracked files require `--include-untracked`.
2. **Specify review scope**: Use options to target specific changes:
   * [`/coderabbit:review uncommitted`](#reviewing-specific-changes) - staged and tracked local edits
   * [`/coderabbit:review committed`](#reviewing-specific-changes) - only committed changes
3. **Specify base branch**: If your main branch isn't `main`, use:
   * [`/coderabbit:review --base develop`](#comparing-against-different-branches)
   * [`/coderabbit:review --base master`](#comparing-against-different-branches)
4. **Review file types**: CodeRabbit focuses on code files, not docs or configuration

### Claude Code not applying fixes

If Claude Code isn't implementing CodeRabbit's suggestions:

1. **Provide explicit context**: Tell Claude Code to "fix the issues found by CodeRabbit" explicitly
2. **Check review completion**: Ensure the review has finished before asking for fixes
3. **Review findings manually**: Ask Claude to "show me the CodeRabbit findings" to verify they were received
4. **Iterate on specific issues**: Ask Claude to focus on fixing specific issues one at a time

### Review taking too long

CodeRabbit reviews may take 7 to 30+ minutes depending on the scope of changes:

1. **Review smaller changesets**: Adjust what you're reviewing to reduce analysis time:
   * Use [`/coderabbit:review uncommitted`](#reviewing-specific-changes) to review only uncommitted changes
   * Work on smaller feature branches compared to main
   * Break large features into smaller, reviewable chunks
2. **Configure the diff scope**: Control what changes are analyzed:
   * **Review uncommitted changes only**: Use the `uncommitted` option to analyze staged and tracked local edits
   * **Configure base branch**: Use `--base` to set the comparison point
   * **Use feature branches**: Work on focused feature branches instead of large staging branches

<Note>
  The integration creates a more thorough review process than either tool alone.
  Expect comprehensive analysis that catches issues that would otherwise reach
  production.
</Note>
