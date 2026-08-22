# MCP for Claude Code — authoring reference (hand scoped)

> For MCP server authors: building a public, unauthenticated streamable-HTTP server for Claude Code — tool search, schema/output/timeout limits, `_meta` annotations, resources and prompts — plus the two paths users install through.

## ⚠️ NOTE: Trimmed from original doc!

Trimmed from https://code.claude.com/docs/en/mcp:

- Scoped to **writing a public, unauthenticated remote server over streamable HTTP** that serves read-only content, plus the installation and verification facts to hand to a user.
- Removed: local stdio, SSE and WebSocket transports, OAuth and header auth, plugin packaging, elicitation, channels, secrets in config, and consumer-only troubleshooting.

**This file covers one thing: what the Claude Code client does to your server, and how its users install it.** It is not the protocol and not the connector story. Protocol fundamentals live in the `mcp` collection; connector auth, testing, Directory review, and MCP apps live in the `claudeai` collection. Don't answer those from this file.

---

## Build a server

- Protocol fundamentals: https://modelcontextprotocol.io/docs/develop/build-server
- Testing and Directory submission: https://claude.com/docs/connectors/building
- Reviewed connectors for reference: https://claude.ai/directory — Directory connectors use the same MCP
  infrastructure as Claude Code, so a remote server that works here also works as a claude.ai connector.

Build **streamable HTTP only**. SSE is deprecated and WebSocket is a Claude Code–only transport; one HTTP
endpoint reaches every surface.

Claude can scaffold one for you with the official
[`mcp-server-dev` plugin](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/mcp-server-dev):

```text
/plugin install mcp-server-dev@claude-plugins-official
/mcp-server-dev:build-mcp-server
```

If the marketplace isn't registered: `/plugin marketplace add anthropics/claude-plugins-official`. If the
install summary says `Run /reload-plugins to activate.`, run it. The build skill asks about your use case and
scaffolds either a remote HTTP or a local stdio server.

> **Trust:** users are told to verify each server before connecting it. A server that fetches external content
> exposes its users to [prompt injection risk](https://code.claude.com/docs/en/security#protect-against-prompt-injection).
> Design accordingly if you want people to adopt it.

---

## HTTP transport

The most widely supported transport for cloud-based services.

```bash
claude mcp add --transport http <name> <url>
```

In JSON config (`.mcp.json`, `~/.claude.json`, `claude mcp add-json`) the `type` field accepts
`streamable-http` as an alias for `http`, so configs copied from server docs that use the spec's name work
unmodified.

A JSON entry with a `url` but no `type` is a configuration error — Claude Code reads a typeless entry as stdio,
skips the server, and reports `MCP server "<name>" has a "url" but no "type"`. Always include `type` in the
install snippet you publish.

### Unauthenticated servers

Nothing to configure: no `oauth` block, no headers. The one behaviour to avoid is returning `401 Unauthorized`
or `403 Forbidden` — Claude Code flags such a server as **needs authentication** and points the user at a
sign-in flow that doesn't exist. Use other status codes for errors, with a useful body.

---

## How people will install your server

### Two install paths — publish both

One URL, two ways in. Which one a user gets depends on how they signed in, not on anything you control.

1. **`claude mcp add`** in Claude Code (below). Always works.
2. **As a claude.ai connector** — the user adds the same URL at https://claude.ai/customize/connectors, and it
   becomes available in claude.ai, Cowork, and Claude Code. On Team and Enterprise plans only admins can add
   connectors, so expect some users to need an admin.

A connector added in claude.ai appears in Claude Code automatically, labelled as coming from claude.ai — those
users never run `claude mcp add`. But this only happens when the session's active credential *is* the claude.ai
subscription login. Connectors are not loaded when any of these is active instead: `ANTHROPIC_API_KEY`,
`ANTHROPIC_AUTH_TOKEN`, `apiKeyHelper`, a third-party provider (Amazon Bedrock, Google Cloud's Agent Platform),
an Anthropic profile or federation variables, or a `CLAUDE_CODE_OAUTH_TOKEN` from `claude setup-token`. Those
users need path 1. **So your README needs both, not just the one you happen to use.**

If a user does both, the locally added server wins. Precedence is local scope → project → user → plugin →
claude.ai connector; the first three match by name, plugins and connectors match by **endpoint**, so a
connector pointing at the same URL is treated as the duplicate and `/mcp` lists it as hidden.

### Scopes

| Scope | Loads in | Shared with team | Stored in |
| --- | --- | --- | --- |
| Local (default) | Current project only | No | `~/.claude.json` |
| Project | Current project only | Yes, via version control | `.mcp.json` in project root |
| User | All your projects | No | `~/.claude.json` |

Choose the scope you recommend in your README: `--scope user` for a public utility someone wants available in
every project, `--scope project` for a `.mcp.json` checked into a repo, local (the default) for a one-off try.

```bash
claude mcp add --transport http shared-server --scope project https://example.com/mcp
```

```json
{
  "mcpServers": {
    "shared-server": {
      "type": "http",
      "url": "https://example.com/mcp"
    }
  }
}
```

Project-scoped servers from `.mcp.json` prompt for approval in interactive sessions before first use.
Non-interactive runs — `claude -p`, Agent SDK, cloud sessions — can't show that prompt and load project servers
without asking.

### From JSON

```bash
claude mcp add-json <name> '<json>'
claude mcp add-json my-server '{"type":"http","url":"https://mcp.example.com/mcp"}'
```

### Naming

Server names added through `claude mcp` may contain only letters, numbers, hyphens, and underscores. These
names are reserved for built-ins and will be rejected or skipped: `workspace`, `claude-in-chrome`,
`computer-use`, `Claude Preview`, `Claude Browser`.

The user picks the name at install time, and it becomes part of every callable tool name:
`mcp__<server-name>__<tool-name>`. That full form is what users write in permission allow rules, a subagent's
`tools` field, a skill's `allowed-tools`, and hook matchers. **Pick one short name, use it in every example you
publish, and quote the full `mcp__…` form** — otherwise everyone's allow rules differ.

### Managing and verifying

```bash
claude mcp list          # all servers, with health status
claude mcp get <name>    # details for one server
claude mcp remove <name>
# /mcp inside a session — status panel, per-server toggle
```

`claude mcp add` only writes configuration; it doesn't connect. Status shows as `✔ Connected`,
`! Needs authentication`, `✘ Failed to connect`, or `⏸ Pending approval`. On failure, `claude mcp list` appends
the HTTP status or error code plus any error text your server returned, and `claude mcp get` shows it on an
`Issue:` line — so **return a useful error body on a failed handshake**; users will see it.

`/mcp` shows a tool count next to each connected server and flags any server that advertises the tools
capability but returns none — don't declare a capability you don't populate.

---

## Tool search: how Claude finds your tools

Tool search is **on by default**. MCP tool definitions are deferred rather than loaded upfront: only tool
*names* and your *server instructions* load at session start, and Claude searches for tools when a task needs
them. There's no fixed per-server tool cap; the practical limit is context budget.

### For server authors

Server instructions are the field that decides whether your tools get found. Treat them like a
[skill](https://code.claude.com/docs/en/skills) description and state:

- what category of tasks your tools handle
- when Claude should search for your tools
- the key capabilities your server provides

**Claude Code truncates tool descriptions and server instructions at 2 KB each.** Keep them concise and put
critical details first.

### Exempting tools from deferral

Set `alwaysLoad: true` on a server (any transport) to load all its tools into context at session start:

```json
{
  "mcpServers": {
    "core-tools": { "type": "http", "url": "https://mcp.example.com/mcp", "alwaysLoad": true }
  }
}
```

Your server can also mark individual tools with `"anthropic/alwaysLoad": true` in the tool's `_meta`. Use this
sparingly — every upfront tool consumes context. Note `alwaysLoad: true` makes startup wait for your server,
capped at the 5-second connect timeout.

To test the loaded-upfront path, users can set `ENABLE_TOOL_SEARCH=false` (all tools loaded, no deferral) or
`auto` (upfront until definitions reach 10% of the context window). Tool search requires a model supporting
`tool_reference` blocks (Sonnet 4.5, Haiku 4.5, Opus 4.5, and later), and is disabled when
`ANTHROPIC_BASE_URL` points at a non-first-party host.

---

## Tool design constraints

### Input schemas: no root-level combinator

The Claude API rejects `anyOf`, `oneOf`, or `allOf` at the **top level** of a tool's input schema. Combinators
nested inside `properties` are fine and passed through unchanged.

Claude Code doesn't drop such tools: it flattens the schema into a single object and prepends a sentence to the
description explaining which parameter groups belong together (`allOf` merges and keeps each branch's
`required`; `anyOf`/`oneOf` merge properties and describe each branch's `required` in prose rather than
enforcing it). **Your server therefore receives whatever combination Claude chose — keep validating
server-side.** If no acceptable schema can be produced, that one tool is skipped and the rest stay available.

### Output size

- Warning shown when any tool output exceeds **10,000 tokens** (threshold fixed).
- Default maximum **25,000 tokens**, raisable by the user via `MAX_MCP_OUTPUT_TOKENS`.
- Results over the default persist-to-disk threshold are replaced in-conversation with a file reference.

As an author you can raise the threshold for a specific tool with `_meta["anthropic/maxResultSizeChars"]` in
your `tools/list` entry, up to a hard ceiling of **500,000 characters** — useful for inherently large outputs
like a full index or file tree:

```json
{
  "name": "get_schema",
  "description": "Returns the full database schema",
  "_meta": { "anthropic/maxResultSizeChars": 200000 }
}
```

This applies to text content independently of `MAX_MCP_OUTPUT_TOKENS`, so users don't have to raise the
variable. **Tools returning image data are always subject to `MAX_MCP_OUTPUT_TOKENS`** — the annotation has no
effect there. Paginating is the other option.

### Timeouts your server must live within

- **Per-server wall clock**: the `timeout` field (milliseconds) in the server's config, overriding
  `MCP_TOOL_TIMEOUT` for that server. A hard limit per tool call — **progress notifications do not extend it**.
- **Per-request first-byte timer**: 60 seconds to the first response byte, unless the per-server `timeout` or
  `MCP_TOOL_TIMEOUT` is set to 60s or higher, which raises it.
- **Idle timeout**: a call that sends no response *and no progress notification* aborts after 5 minutes.
  Configurable by the user via `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT` (ms, `0` disables). **Emit progress
  notifications from long-running tools.**
- **Startup**: `MCP_TIMEOUT` controls server startup; the connect timeout is 5 seconds.

These bound how long a call may run, not how long it blocks the user. A main-conversation tool call still
running after two minutes moves to a background task: Claude gets a task ID immediately, keeps working, and
the result arrives as a notification. Calls from subagents and non-interactive runs are never backgrounded.
So a slow tool is survivable; a silent one is not.

### `_meta` annotations you can set

Three keys in a tool's `tools/list` entry change how Claude Code treats it:

| Key | Effect |
| --- | --- |
| `anthropic/maxResultSizeChars` | Raise that tool's result-size threshold, up to 500,000 chars (see Output size) |
| `anthropic/alwaysLoad` | Load this tool upfront instead of deferring it to tool search |
| `anthropic/requiresUserInteraction` | Prompt the user for approval on **every** call |

`requiresUserInteraction` must be the JSON boolean `true`; anything else is ignored. The prompt appears even in
`acceptEdits`, `auto`, and `bypassPermissions` modes, allow rules don't skip it, there's no "don't ask again",
and in `dontAsk` mode the call is denied instead. Use it only where the prompt *is* the point — a consent or
access-grant step. A read-only content server generally wants none of these on by default.

### Connection lifecycle

- **Dynamic updates**: send MCP `list_changed` notifications and Claude Code refreshes your tools, prompts, and
  resources without a reconnect. If a refresh fails, it keeps the previously discovered set.
- **Reconnection**: HTTP servers that drop mid-session are retried with exponential backoff (five attempts,
  starting at 1s). Initial connection failures retry up to three times on transient errors (5xx, connection
  refused, timeout); auth and not-found errors are not retried.
- **Discovery caching**: a remote server used before can supply its tool list from cache and connect only on
  first tool call (shown as e.g. `cached 2h ago · connects on first use · 5 tools`). `MCP_DISCOVERY_CACHE=0`
  forces connection at startup.
- When a server fails to connect, Claude is told which server failed and why, so it can report the failure
  rather than behaving as if the server didn't exist.

---

## Beyond tools

### Resources

Expose resources and users reference them with `@` mentions, autocompleted alongside files:

```text
Can you analyze @github:issue://123 and suggest a fix?
Compare @postgres:schema://users with @docs:file://database/user-model
```

Format is `@server:protocol://resource/path`. Resources are fetched and included as attachments; paths are
fuzzy-searchable; content can be text, JSON, or any structured data. Claude Code automatically provides tools
to list and read resources when a server supports them.

### Prompts as slash commands

Prompts you expose appear as `/mcp__servername__promptname`, discovered dynamically and listed under `/`.
Arguments are passed space-separated and parsed against the prompt's parameters; results are injected directly
into the conversation. Spaces in server and prompt names become underscores.

```text
/mcp__github__list_prs
/mcp__github__pr_review 456
/mcp__jira__create_issue "Bug in login flow" high
```

---

## Also worth knowing

- **Organisation controls**: admins can set a connector tool to `ask` (prompts on every call, no remembering)
  or `blocked` (filtered out before Claude sees it), and can restrict which servers users may connect to at all
  — `managed-mcp.json`, `allowedMcpServers`, `deniedMcpServers`. Expect some users in managed orgs to be unable
  to add your server. See [Managed MCP configuration](https://code.claude.com/docs/en/managed-mcp).
