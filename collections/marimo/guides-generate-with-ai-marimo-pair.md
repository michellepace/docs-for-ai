<!-- Source: https://docs.marimo.io/guides/generate_with_ai/marimo_pair/ -->

# marimo pair: work on notebooks with coding agents

Use **[marimo pair](https://marimo.io/pair)** to connect coding agents like
Claude Code, Codex, and OpenCode to running marimo notebooks. Once your agent
is paired with marimo, ask it to explore data, explain results, or modify
cells. The agent can inspect variables and try code in a scratchpad before it
commits changes to the notebook. You can inspect the results and edit the same
notebook yourself, letting you pair program with the agent.

## Installation

The marimo pair skill teaches your agent how to connect to running notebooks.
Choose the installation method for your agent.

**Claude Code:**

Run these commands in your terminal:

```bash
claude plugin marketplace add marimo-team/marimo-pair
claude plugin install marimo-pair@marimo-pair
```

To update the plugin, run:

```bash
claude plugin update marimo-pair@marimo-pair
```

**Codex CLI:**

Run these commands in your terminal:

```bash
codex plugin marketplace add marimo-team/marimo-pair
codex plugin add marimo-pair@marimo-pair
```

To update the marketplace, run:

```bash
codex plugin marketplace upgrade
```

**Other agents:**

For Cursor, VS Code, Gemini CLI, OpenCode, Copilot CLI, or another agent that supports Agent Skills, run:

```bash
npx skills add marimo-team/marimo-pair
```

To update the skill, run:

```bash
npx skills upgrade marimo-team/marimo-pair
```

If you use `uv` instead of `npx`, install the skill with:

```bash
uvx deno -A npm:skills add marimo-team/marimo-pair
```

## Start pairing

### Ask your agent to start a notebook

With the skill installed, ask your agent to start a notebook:

**Claude Code:**

```text
/marimo-pair with me on notebook.py
```

**Codex CLI:**

```text
$marimo-pair with me on notebook.py
```

**Other agents:**

```text
/marimo-pair with me on notebook.py
```

The agent starts marimo and connects to the notebook.

### Connect to a running notebook

1. Open the notebook's **Actions menu** and select **Pair an agent**.
2. In the **Pair an agent** dialog, select your agent.
3. Click **Copy command**, then paste and run the command in your terminal.

**Actions menu:**

![The notebook header and Actions menu with Pair an agent highlighted.](https://docs.marimo.io/_static/marimo-pair-actions.jpg)

**Pairing dialog:**

![The Pair an agent dialog with the Claude tab selected.](https://docs.marimo.io/_static/marimo-pair-dialog.jpg)

> **Pair with notebooks on molab**
>
> You can also pair your local agent with notebooks on
> [molab](https://molab.marimo.io/notebooks). Just follow these same steps.

Watch the connection steps for your agent:

**Claude Code:**

[Video: https://cms.marimo.io/landing/pair/claude-boot.webm](https://cms.marimo.io/landing/pair/claude-boot.webm)

**Codex CLI:**

[Video: https://cms.marimo.io/landing/pair/codex-boot.webm](https://cms.marimo.io/landing/pair/codex-boot.webm)

**Other agents:**

[Video: https://cms.marimo.io/landing/pair/prompt-boot.webm](https://cms.marimo.io/landing/pair/prompt-boot.webm)

Ask your agent to explore data, explain results, or modify cells.
The agent can inspect variables and try code in a scratchpad before it changes the notebook.
You can inspect the results and edit the same notebook yourself.
Your work stays in a notebook that you can run again, modify, and share.