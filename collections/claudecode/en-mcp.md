# MCP for Claude Code — authoring reference (hand scoped)

> For MCP server authors: building a public, unauthenticated streamable-HTTP server for Claude Code — error responses, the two install paths and tool naming, tool search, schema/output/timeout limits, `_meta` annotations, connection lifecycle, resources and prompts.

## ⚠️ NOTE: Trimmed from original doc!

Trimmed from <https://code.claude.com/docs/en/mcp.md>:

- Scoped to **writing a public, unauthenticated remote server over streamable HTTP** that serves read-only content, plus the installation and verification facts to hand to a user.
- Removed: local stdio, SSE and WebSocket transports, OAuth and header auth, plugin packaging, elicitation, channels, secrets in config, `claude mcp serve`, Claude Desktop import, and consumer-only troubleshooting.

**This file covers what the Claude Code client does to your server, and how its users install it.** Protocol fundamentals live in the `mcp` collection; connector auth, testing, Directory review, and MCP apps live in the `claudeai` collection. Don't answer those from this file.

---

## Build a server

- Protocol fundamentals: `~/.claude/docs-for-ai/collections/mcp/2026-07-28-develop-build-server.md`
- Testing and Directory submission: `~/.claude/docs-for-ai/collections/claudeai/connectors-building.md`
- Reviewed connectors for reference: https://claude.ai/directory

Build **streamable HTTP only**: SSE is deprecated, WebSocket can't be added with `claude mcp add --transport`, and one HTTP endpoint reaches every surface.

Claude can scaffold one for you with the official [`mcp-server-dev` plugin](https://raw.githubusercontent.com/anthropics/claude-plugins-official/main/plugins/mcp-server-dev/README.md):

```text
/plugin install mcp-server-dev@claude-plugins-official
/mcp-server-dev:build-mcp-server
```

If the marketplace isn't registered, first run `/plugin marketplace add anthropics/claude-plugins-official`. Choose the remote HTTP option when the skill asks.

> **Trust:** users are told to verify each server before connecting it; servers that fetch external content can expose users to [prompt injection](https://code.claude.com/docs/en/security.md) (§ "Protect against prompt injection").

### Responses Claude Code reacts to

- **Never return `401` or `403`.** Claude Code flags the server as **needs authentication** and points users at a sign-in flow that doesn't exist. Use other status codes for errors.
- **Return a useful error body on a failed handshake.** `claude mcp list`, `claude mcp get`, and `/mcp` show the HTTP status plus your error text (credential-like text redacted), and with tool search (the default) Claude is told the server failed and why. Without tool search, Claude isn't told.
- **Don't rate-limit discovery requests** (`tools/list`, `prompts/list`, `resources/list`): a 4xx response there, 429 included, isn't retried.
- **Don't advertise a capability you don't populate.** `/mcp` flags a server that declares the tools capability but returns no tools.

---

## How people will install your server

### Two install paths — publish both

One URL, two ways in; which one reaches a user isn't up to you.

1. **`claude mcp add`** in Claude Code (below). Works with any sign-in.
2. **As a claude.ai connector** — the user adds the same URL at <https://claude.ai/customize/connectors>, and it becomes available in claude.ai, Cowork, and Claude Code. On Team and Enterprise plans only admins can add connectors. claude.ai calls your URL from Anthropic's servers, not the user's machine, and has its own result-size and timeout limits — test this path separately (see `claudeai`).

A connector added in claude.ai appears in Claude Code automatically, but only in sessions signed in with a claude.ai subscription. Sessions on an API key or auth token, `apiKeyHelper`, a cloud provider (Bedrock, Agent Platform), an Anthropic profile or federation credentials, or a `claude setup-token` token don't get connectors, and the desktop app's WSL sessions don't get them yet. Connectors are also switched off by `disableClaudeAiConnectors: true` in any settings file (a repo's checked-in `.claude/settings.json` included) or `ENABLE_CLAUDEAI_MCP_SERVERS=false`. Those users need path 1.

If a user does both, their Claude Code entry wins: connectors are matched by **URL**, so the duplicate connector shows as hidden in `/mcp`.

In managed orgs, admins can block servers (`managed-mcp.json`, `allowedMcpServers`/`deniedMcpServers`) or individual connector tools, so some users won't be able to add or use yours. See [Managed MCP configuration](https://code.claude.com/docs/en/managed-mcp.md).

### Scopes and snippets

| Scope | Loads in | Shared with team | Stored in |
| --- | --- | --- | --- |
| Local (default) | Current project only | No | `~/.claude.json` |
| Project | Current project only | Yes, via version control | `.mcp.json` in project root |
| User | All your projects | No | `~/.claude.json` |

Choose the scope you recommend in your README: `--scope user` for a public utility someone wants available in every project, `--scope project` for a `.mcp.json` checked into a repo, local (the default) for a one-off try.

```bash
claude mcp add --transport http my-server --scope project https://mcp.example.com/mcp
claude mcp add-json my-server '{"type":"http","url":"https://mcp.example.com/mcp"}'
```

```json
{
  "mcpServers": {
    "my-server": {
      "type": "http",
      "url": "https://mcp.example.com/mcp"
    }
  }
}
```

A JSON entry with a `url` but no `type` is read as stdio and skipped with an error (other clients' snippets often omit `type`), so always include `"type": "http"` in any JSON you publish; `streamable-http` is accepted as an alias.

Project-scoped servers from `.mcp.json` prompt for approval in interactive sessions; `claude -p`, Agent SDK, and cloud sessions load them without asking. Approvals committed to the repo's `.claude/settings.json` (`enableAllProjectMcpServers`, `enabledMcpjsonServers`) apply only once the user trusts the workspace.

### Naming

Server names may contain only letters, numbers, `-`, and `_`; built-in names such as `workspace`, `claude-in-chrome`, `computer-use`, `Claude Preview`, and `Claude Browser` are rejected.

For `claude mcp add` and `.mcp.json` installs the user picks the server name, and your tools are callable as `mcp__<server-name>__<tool-name>` — the form used in permission allow rules, a subagent's `tools` field, a skill's `allowed-tools`, and hook matchers. Connector users get `mcp__claude_ai_<server>__<tool-name>`, with the server name coming from claude.ai. **Pick one short name, use it in every example you publish, and quote both full forms.**

### Managing and verifying

```bash
claude mcp list        # all servers, with health status
claude mcp get <name>  # details for one server
claude mcp remove <name>
# /mcp inside a session — status panel, per-server toggle
```

`claude mcp add` only writes configuration; it doesn't connect. Statuses include `✔ Connected`, `! Needs authentication`, `✘ Failed to connect`, and `⏸ Pending approval`. Your error detail appears only with `✘ Failed to connect` (on an `Issue:` line in `claude mcp get` and `/mcp`); a `✘ Connection error` status shows none.

---

## Tool search: how Claude finds your tools

Tool search is **on by default**. MCP tool definitions are deferred rather than loaded upfront: only tool *names* and your *server instructions* load at session start, and Claude searches for tools when a task needs them. There's no fixed per-server tool cap; the practical limit is context budget.

### Server instructions and descriptions

With tool search on, server instructions help Claude decide when to search for your tools. Treat them like a skill description (`~/.claude/docs-for-ai/collections/claudecode/en-skills.md`) and state:

- what category of tasks your tools handle
- when Claude should search for your tools
- the key capabilities your server provides

Claude Code truncates tool descriptions and server instructions at 2 KB each, so **keep them concise and put critical details first**.

### Loading tools upfront

Some users load your full definitions upfront (pre-4.5 models, a non-first-party `ANTHROPIC_BASE_URL`, some cloud deployments), so keep your total tool-definition size lean. Test with `ENABLE_TOOL_SEARCH=false`.

Mark individual tools with `"anthropic/alwaysLoad": true` in their `_meta` to load them upfront. Users can do the same for all your tools with `"alwaysLoad": true` on your server's config entry, which also makes startup wait for your server (up to 5 seconds). Use this sparingly — every upfront tool consumes context.

---

## Tool design constraints

### Input schemas: no root-level combinator

The Claude API rejects `anyOf`, `oneOf`, or `allOf` at the **top level** of a tool's input schema. Combinators nested inside `properties` are fine and passed through unchanged.

Claude Code flattens such a schema into one object and prepends a sentence to the description saying which parameter groups belong together; each branch's `required` stays enforced for `allOf` but is only described for `anyOf`/`oneOf`. **Your server receives whatever combination Claude chose — validate server-side.** Where the rewrite fails or isn't available (versions before v2.1.195, some deployments), that tool is skipped. **A flat root object is the portable choice.**

### Input schemas: validity checks

The Claude API rejects the **whole request** when any one tool's input schema fails its checks. Claude Code runs two of those checks when it loads your tools (after the combinator rewrite) and excludes each failing tool:

- Top-level property names are 1–64 characters of ASCII letters, digits, `_`, `.`, and `-`.
- The schema is valid JSON Schema draft 2020-12 (declaring another `$schema` dialect skips this check).

Claude is told which tools were excluded and why, and a fixed tool comes back the next time Claude Code loads your tools. Where the exclusion isn't active (flag fetching off, air-gapped machines, versions before v2.1.216), the tool is sent anyway and every request that includes it fails with a 400. **Validate schemas before you ship.**

### Output size

- Warning shown when any tool output exceeds **10,000 tokens** (fixed).
- Default maximum **25,000 tokens**, raisable by the user via `MAX_MCP_OUTPUT_TOKENS`.
- A result with no image content over the limit is saved to a file and replaced in-conversation with a message naming the path; Claude reads the file when it needs the content.

As an author you can raise that limit for a specific tool with `_meta["anthropic/maxResultSizeChars"]` in your `tools/list` entry, up to a hard ceiling of **500,000 characters** — useful for inherently large outputs like a full index or file tree:

```json
{
  "name": "get_schema",
  "description": "Returns the full database schema",
  "_meta": { "anthropic/maxResultSizeChars": 200000 }
}
```

This applies to text content independently of `MAX_MCP_OUTPUT_TOKENS`, so users don't have to raise the variable. **Tools returning image data are always subject to `MAX_MCP_OUTPUT_TOKENS`** — the annotation has no effect there. Paginating is the other option.

### Timeouts your server must live within

- **Wall clock**: effectively none by default (~28 hours); users can cap a server's calls with its `timeout` field (ms) or `MCP_TOOL_TIMEOUT`. Progress notifications don't extend it.
- **First byte**: each HTTP request must reach its first response byte **within 60 seconds** (users can raise this, never lower it).
- **Idle**: a call that sends no response *and no progress notification* for 5 minutes is aborted (user-configurable via `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`). **Emit progress notifications from long-running tools.**
- **Startup**: connecting must finish within the startup timeout, which users set with `MCP_TIMEOUT` (`MCP_TIMEOUT=10000` for 10 seconds).

A main-conversation call still running after two minutes moves to a background task: Claude keeps working and gets the result later, with the wall-clock and idle limits still applying. So a slow tool is survivable; a silent one is not.

### `_meta` annotations you can set

Three keys in a tool's `tools/list` entry change how Claude Code treats it:

| Key | Effect |
| --- | --- |
| `anthropic/maxResultSizeChars` | Raise that tool's result-size limit, up to 500,000 chars (see Output size) |
| `anthropic/alwaysLoad` | Load this tool upfront instead of deferring it to tool search |
| `anthropic/requiresUserInteraction` | Prompt the user for approval on **every** call |

`requiresUserInteraction` (must be JSON `true`) overrides every permission mode and allow rule, and the call is denied where no person can answer (`dontAsk`, `--permission-prompt-tool`). Reserve it for consent or access-grant steps; **a read-only content server shouldn't set it.**

---

## Connection lifecycle

- **Protocol revision**: current Claude Code negotiates MCP revision `2026-07-28` with HTTP servers that support it (and with claude.ai connector servers, in sessions that fetch feature flags) and uses the earlier revision otherwise. Test both; `MCP_SDK_GENERATION=v1` or `MCP_PROTOCOL_NEGOTIATION=legacy` forces the earlier one.
- **Slow connects**: servers connect in the background. If a request needs your tools while you're still connecting, Claude waits for you (inside the `ToolSearch` call, or via `WaitForMcpServers` without tool search). With tool search, tools that finish connecting mid-turn are listed to Claude on its next request.
- **Dynamic updates**: send MCP `list_changed` notifications and Claude Code refreshes your tools, prompts, and resources without a reconnect. If a refresh fails, it keeps the previously discovered set.
- **Notification stream (`2026-07-28` revision)**: `list_changed` rides a stream Claude Code holds open. A stream that closes within 10 seconds is reopened up to three times, then abandoned for that connection. One that stays open longer and then closes, as streams to serverless hosts commonly do, is reopened until five reopens in an hour, after which Claude Code waits about six hours before the next. Until it reopens, users keep your last-fetched lists. **On a serverless host, don't count on `list_changed` arriving promptly.**
- **Retries**: mid-session drops are retried five times with exponential backoff from 1 second. First connections retry up to three times on 5xx, refused connections, or timeouts, but not on auth or not-found errors. Discovery requests retry up to three times on transient network or server errors, but not on 4xx responses or request timeouts.
- **Discovery cache** (v2.1.221+; off by default unless a gradual rollout has enabled it; users set `MCP_DISCOVERY_CACHE=1` or `0` to force it on or off): a returning user's tool list may come from the previous session, and your server isn't contacted until Claude first calls one of your tools. `/mcp` shows this as e.g. `cached 2h ago · connects on first use · 5 tools`.

---

## Beyond tools

### Resources

Expose resources and users reference them with `@` mentions, autocompleted alongside files:

```text
Can you analyze @github:issue://123 and suggest a fix?
Compare @postgres:schema://users with @docs:file://database/user-model
```

Format is `@server:protocol://resource/path`. Resources are fetched and included as attachments; paths are fuzzy-searchable; content can be text, JSON, or any structured data. Claude Code automatically provides tools to list and read resources when a server supports them.

### Prompts as slash commands

Prompts you expose are discovered dynamically and listed in the `/` menu as `/servername:promptname (MCP)`; typing `/mcp__servername__promptname` also runs one. Results are injected directly into the conversation.

Claude Code splits arguments on whitespace and parses them against the prompt's parameters, so each argument is a single token — **design arguments that never need spaces.** The prompt name is used verbatim, so keep it free of spaces too.

```text
/mcp__github__list_prs
/mcp__github__pr_review 456
/mcp__jira__create_issue login-bug high
```
