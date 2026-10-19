# MCP for Claude Code — authoring reference (hand scoped)

> For MCP server authors: building a public, unauthenticated streamable-HTTP server for Claude Code — error responses, the two install paths and tool naming, tool search, schema/output/timeout limits, `_meta` annotations, connection lifecycle, resources and prompts.

## ⚠️ NOTE: Trimmed from original doc!

Trimmed from https://code.claude.com/docs/en/mcp.md:

- Scoped to **writing a public, unauthenticated remote server over streamable HTTP** that serves read-only content, plus the installation and verification facts to hand to a user.
- Removed: local stdio, SSE and WebSocket transports, OAuth and header auth, plugin packaging, elicitation, channels, secrets in config, `claude mcp serve`, Claude Desktop import, and consumer-only troubleshooting.

**This file covers what the Claude Code client does to your server, and how its users install it.** Protocol fundamentals live in the `mcp` collection; connector auth, testing, Directory review, and MCP apps live in the `claudeai` collection. Don't answer those from this file.

---

## Build a server

- Protocol fundamentals: `~/.claude/docs-for-ai/collections/mcp/2026-07-28-develop-build-server.md`
- Claude's MCP client across all surfaces (supported features, claude.ai limits, distribution): `~/.claude/docs-for-ai/collections/claudeai/connectors-building.md`
- Reviewed connectors for reference: https://claude.ai/directory

Build **streamable HTTP only**. SSE is deprecated, `claude mcp add --transport` can't add WebSocket, and one HTTP endpoint reaches every Claude surface.

Claude can scaffold the server with the official [`mcp-server-dev` plugin](https://raw.githubusercontent.com/anthropics/claude-plugins-official/main/plugins/mcp-server-dev/README.md). Pick the remote HTTP option when the skill asks.

```text
/plugin install mcp-server-dev@claude-plugins-official
/mcp-server-dev:build-mcp-server
```

If the install reports `Marketplace "claude-plugins-official" not found`, run `/plugin marketplace add anthropics/claude-plugins-official` and retry.

> **Trust:** users are told to verify each server before connecting it. A server that fetches external content can expose them to [prompt injection](https://code.claude.com/docs/en/security.md) (§ "Protect against prompt injection").

### Responses Claude Code reacts to

- **Never return `401` or `403`.** Claude Code flags the server as needing authentication and sends users to a sign-in flow that doesn't exist.
- **Explain a failed handshake in the error body.** Under `✘ Failed to connect`, users see the HTTP status and your error text, credential-like text redacted, in `claude mcp list`, `claude mcp get`, and `/mcp` (v2.1.219+). With tool search on (the default), Claude is told too.
- **Don't rate-limit discovery requests** (`tools/list`, `prompts/list`, `resources/list`). A 4xx, `429` included, is never retried.
- **Don't declare the tools capability without serving tools.** `/mcp` flags a server that does.

---

## How people will install your server

### Two install paths — publish both

One URL serves both paths, and you don't control which one a user takes.

1. **`claude mcp add`** in Claude Code (below). Works with any sign-in.
2. **claude.ai connector.** The user adds the same URL at https://claude.ai/customize/connectors, and it becomes available in claude.ai, Cowork, and Claude Code. On Team and Enterprise plans only admins can add connectors. claude.ai calls your URL from Anthropic's servers, not the user's machine. claude.ai and Desktop cap results at ~150,000 characters and tool calls at 240 seconds. Test this path separately: `~/.claude/docs-for-ai/collections/claudeai/connectors-building-testing.md`.

Connectors reach Claude Code only when it's signed in with a claude.ai subscription. These users need path 1:

- Key, token, or profile sign-ins: `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `apiKeyHelper`, an Anthropic profile (`ANTHROPIC_PROFILE`) or federation variables, a `claude setup-token` token in `CLAUDE_CODE_OAUTH_TOKEN`
- Third-party providers such as Amazon Bedrock or Google Cloud's Agent Platform
- The desktop app's WSL sessions
- Connectors switched off (`disableClaudeAiConnectors: true`, `ENABLE_CLAUDEAI_MCP_SERVERS=false`)

A user whose connector is missing from `/mcp` can run `/status` to see which sign-in is active.

If a user sets up both paths, the Claude Code entry wins and `/mcp` lists the connector as hidden. The two are matched by URL. Scheme and host case, the default port (`:443`), and a trailing slash are ignored. A different path, query string, userinfo, or non-default port counts as a separate server, so **publish one canonical URL**.

Managed orgs can block your server (`managed-mcp.json`, `allowedMcpServers`, `deniedMcpServers`) or individual connector tools: [Managed MCP configuration](https://code.claude.com/docs/en/managed-mcp.md).

### Scopes and snippets

| Scope | Loads in | Shared with team | Stored in |
| --- | --- | --- | --- |
| Local (default) | Current project only | No | `~/.claude.json` |
| Project | Current project only | Yes, via version control | `.mcp.json` in project root |
| User | All your projects | No | `~/.claude.json` |

When one name is in several scopes, local beats project beats user, and the winning entry is used whole, with no field merging.

Recommend a scope in your README:

- `--scope user` for a public utility someone wants in every project
- `--scope project` for a `.mcp.json` checked into a repo
- local, the default, for a one-off try

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

**Always include `"type": "http"` in JSON you publish.** Claude Code reads an entry that has a `url` but no `type` as stdio, and skips it with an error. `streamable-http` is an accepted alias for `http`.

Interactive sessions ask users to approve a project-scoped `.mcp.json` server before it loads, so tell them to expect the prompt. `claude -p`, Agent SDK, and cloud sessions load it without asking. Approvals committed in a repo's `.claude/settings.json` (`enabledMcpjsonServers`, `enableAllProjectMcpServers`) count only once the user trusts the folder; until then the server shows `⏸ Pending approval`.

### Naming

- **Server names** may contain only letters, numbers, `-`, and `_`. Built-in names such as `workspace`, `claude-in-chrome`, and `computer-use` are rejected. `anthropic-skills` is reserved for synced skills and hides the server's prompts.
- **Tool names** are built from the server name the user picks, in `claude mcp add` or as the `.mcp.json` key: `mcp__<server-name>__<tool-name>`. Permission allow rules, a subagent's `tools` field, a skill's `allowed-tools`, and hook matchers all use this form.
- **Connector servers** are named by claude.ai, e.g. `claude.ai Slack`, not by the user. Selecting a tool in `/mcp` shows its full name.
- **Full names over 128 characters** are left out of what Claude Code sends Claude; `/mcp` still lists them, and your other tools keep working. Keep tool names well under the limit.

**Pick one short server name, use it in every example you publish, and quote full `mcp__<server-name>__<tool-name>` names.**

### Verifying a connection

`claude mcp add` only writes configuration. It doesn't connect, so check the status afterwards:

```bash
claude mcp list          # every server, with health status
claude mcp get <name>    # one server; failure detail on an Issue: line
claude mcp remove <name>
# /mcp inside a session: status detail, tool count, Reconnect, per-server toggle
```

Statuses include `✔ Connected`, `! Needs authentication`, `✘ Failed to connect`, `✘ Connection error` (never shows detail), and `⏸ Pending approval`.

---

## Tool search: how Claude finds your tools

Tool search is **on by default**. At session start, only tool *names* and your *server instructions* load. Full definitions stay deferred until Claude searches for the tools a task needs. There's no fixed per-server tool cap; the practical limit is context budget.

### Names, instructions, and descriptions

- **Tool names** are all Claude sees of a deferred tool before it searches, so make each name say what the tool does.
- **Server instructions** help Claude decide when to search for your tools. Write them like a skill description (`~/.claude/docs-for-ai/collections/claudecode/en-skills.md`) and state:
  - what category of tasks your tools handle
  - when Claude should search for your tools
  - the key capabilities your server provides
- **Length**: Claude sees only the text before the cut. Server instructions, and descriptions of tools loaded upfront, are cut at 4,096 characters. Descriptions of tools loaded through tool search are cut at 16,384, but search matches only their first 4,096. Older clients cut at 2,048: every description before v2.1.295, and instructions and upfront descriptions before v2.1.296. `CLAUDE_CODE_MAX_MCP_DESCRIPTION_LENGTH` (v2.1.280+) replaces both limits with one value. **Keep them concise and put search keywords and critical details first.**

### Loading tools upfront

Some users get all your definitions upfront, with no deferral:

- Models before Claude Opus 4, Sonnet 4, and Haiku 4.5, or before the 4.5 generation on Google Cloud's Agent Platform
- A non-first-party `ANTHROPIC_BASE_URL` proxy, or `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` set
- Microsoft Foundry deployments hosted on Azure, and sessions with the HIPAA configuration
- `ENABLE_TOOL_SEARCH=false`, or `ENABLE_TOOL_SEARCH=auto` while all deferrable definitions total under 10% of the context window

Keep your total definition size lean, and test with `ENABLE_TOOL_SEARCH=false`.

To load a tool upfront, set `"anthropic/alwaysLoad": true` in its `_meta`. Startup doesn't wait for your server because of this. Every upfront tool costs context in every session, so mark few.

The user's server-level `alwaysLoad` setting overrides your marks:

- `true` loads all your tools upfront and makes startup wait for your server, up to 5 seconds.
- `false` defers all your tools, including the ones you marked `true` (v2.1.287+).

Your `false` mark keeps a tool deferred under the user's `true` only for servers passed with `--mcp-config`, supplied by the Agent SDK, or provided by a plugin (v2.1.285+).

---

## Tool design constraints

### Input schemas: no root-level combinator

The Claude API rejects `anyOf`, `oneOf`, or `allOf` at the **root** of a tool's input schema; nested inside `properties` they pass through unchanged.

Claude Code flattens a root combinator into one object and prepends a sentence to the tool description saying which parameter groups belong together. Each `allOf` branch's `required` list stays enforced; `anyOf`/`oneOf` ones are only described. If the flattened schema still fails, or the deployment lacks the remote configuration that enables the rewrite, Claude Code skips that tool and keeps your others. **Use a flat root object, and validate inputs server-side.**

### Input schemas: validity checks

Claude Code runs two of the API's schema checks when it loads your tools, excludes each failing tool, and tells Claude which and why:

- Top-level property names are 1–64 characters of ASCII letters, digits, `_`, `.`, and `-`.
- The schema is valid JSON Schema draft 2020-12. A schema that declares another `$schema` dialect skips this check.

Where flag fetching is off, on air-gapped machines, and before v2.1.216, a failing tool is sent anyway, and the API rejects **every request** that includes it with a 400. **Validate schemas before you ship.**

### Output size

A successful text result over either cap below is saved to a file. In the conversation it's replaced by a message naming the path, and Claude reads the file when it needs the content.

| Limit | Default | Who can change it |
| --- | --- | --- |
| Warning shown to the user | 10,000 tokens | Nobody (fixed) |
| Token cap | 25,000 tokens | The user, via `MAX_MCP_OUTPUT_TOKENS` |
| Character cap | 50,000 characters | You, per tool, via `_meta["anthropic/maxResultSizeChars"]` |

Set the annotation on a tool whose output is inherently large, like a full index or file tree:

```json
{
  "name": "get_schema",
  "description": "Returns the full database schema",
  "_meta": { "anthropic/maxResultSizeChars": 200000 }
}
```

The annotated value, up to 500,000, replaces both caps for that tool's text content. **Results with image data stay subject to `MAX_MCP_OUTPUT_TOKENS`.** Paginating is the other option.

Other limits and handling:

- **HTTP response bodies: 16 MiB hard cap.** Claude Code stops reading once one JSON response body, or one event of an event stream, passes 16 MiB after decompression, and that request fails. Paginate rather than return more per response.
- **Error results** (`isError: true`) reach Claude as the tool's error message. Text over ~11,000 characters keeps only its first and last 5,000 characters.
- **Images** (PNG, JPEG, GIF, WebP) are shown to Claude inline, possibly scaled down or compressed. Claude Code also saves the original bytes to a file and gives Claude the path (v2.1.283+).

### Timeouts your server must live within

| Timer | Default | Notes |
| --- | --- | --- |
| First byte | 60 seconds per HTTP request | Raised by a longer per-server `timeout`, `MCP_TOOL_TIMEOUT`, or `MCP_TIMEOUT`; never lowered |
| Idle (no response or progress notification) | 5 minutes | Users change it with `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`; `0` disables it. A per-server `timeout` is its floor |
| Wall clock | ~28 hours, effectively none | Users cap it with the per-server `timeout` (ms; values below 1000 ignored) or `MCP_TOOL_TIMEOUT`; progress doesn't extend it |
| Startup | Not documented | Users set it with `MCP_TIMEOUT` (ms); connecting must finish within it |

**A tool that can run past 60 seconds must stream.** Answer the `tools/call` POST with a `text/event-stream` response, send a progress notification right away, and keep sending them more often than the 5-minute idle limit. A single JSON body sent at the end misses the first-byte deadline. The fallback is a README snippet with `"timeout": <ms>`, which raises the first-byte timer and the idle floor to that value but also becomes the call's hard cap.

A main-conversation call still running after two minutes moves to a background task (v2.1.212+). Claude keeps working and gets your result later. The timers above still apply, and `/tasks` shows your latest reported progress. Calls from subagents and `claude -p` runs aren't backgrounded and keep blocking.

### Tool annotations

Give every tool a `title` and `readOnlyHint: true`. Directory review requires both, and claude.ai can then run read-only tools without per-call confirmation. Other review rules, such as 64-character tool names and no instructions in descriptions: `~/.claude/docs-for-ai/collections/claudeai/connectors-building-review-criteria.md`.

### `_meta` annotations you can set

Three keys in a tool's `tools/list` entry change how Claude Code treats it:

| Key | Effect |
| --- | --- |
| `anthropic/maxResultSizeChars` | Raises that tool's character cap, up to 500,000 (see Output size) |
| `anthropic/alwaysLoad` | `true` loads the tool upfront instead of deferring it to tool search (see Loading tools upfront) |
| `anthropic/requiresUserInteraction` | `true` prompts the user for approval on **every** call, overriding permission modes and allow rules. A read-only content server shouldn't set it |

---

## Connection lifecycle

- **Protocol revision**: Claude Code negotiates MCP revision `2026-07-28` with HTTP servers that support it, and uses the earlier revision otherwise. This is the default from v2.1.274, or from v2.1.232 where Claude Code fetches feature flags. Older clients, users who set `MCP_SDK_GENERATION=v1`, and servers Anthropic pins by feature flag stay on the earlier revision. **Support both and test both:** `MCP_SDK_GENERATION=v2` forces the newer client, and `MCP_PROTOCOL_NEGOTIATION=legacy` forces the earlier revision.
- **Slow connects**: servers connect in the background. When a request needs your tools before you've connected, Claude waits for you (inside `ToolSearch`, or via `WaitForMcpServers` without tool search). In a resumed session, a call made during your first connection attempt is held up to 10 seconds and runs once you connect. If you don't connect in time, or you're already retrying a failed attempt, it fails with `No such tool available`.
- **Discovery cache** (v2.1.221+): for a remote server the user has used before, the tool list may come from the previous session. Your server then isn't contacted until Claude first calls one of your tools, and `/mcp` shows e.g. `cached 2h ago · connects on first use · 5 tools`. The cache is off unless a gradual rollout enabled it, and was on by default before v2.1.238. `MCP_DISCOVERY_CACHE=1` forces it on and `0` forces it off.

### List updates

Send an MCP `list_changed` notification and Claude Code refetches your tools, prompts, and resources without a reconnect. `claude -p` and Agent SDK sessions refetch only the tool list. If a refetch fails, the previous set stays.

On revision `2026-07-28`, `list_changed` arrives on a stream Claude Code holds open and reopens whenever it closes:

- **Closes within 10 seconds**: reopened up to three times, then abandoned for that connection.
- **Stays open longer, then closes**, as streams to serverless hosts commonly do: after five reopens in an hour, Claude Code waits about six hours.

Until the stream reopens, users keep your last-fetched lists unless they reconnect you from `/mcp`. **On a serverless host, don't count on `list_changed` arriving promptly.**

### Retries

| Failure | Retried | Not retried |
| --- | --- | --- |
| Mid-session drop | 5 attempts, backoff doubling from 1 second; `claude -p` and Agent SDK then keep retrying transient errors for ~30 minutes | Interactive sessions after 5 failures: marked failed until the user reconnects from `/mcp` |
| First connection | Up to 3 times on 5xx, a refused connection, or a timeout | Auth or not-found errors |
| Discovery request (`tools/list` etc.) | Up to 3 times on transient network or server errors | Any 4xx, request timeouts |

---

## Beyond tools

### Resources

Users reference your resources with `@` mentions, autocompleted alongside files:

```text
Can you analyze @github:issue://123 and suggest a fix?
Compare @postgres:schema://users with @docs:file://database/user-model
```

- The format is `@server:protocol://resource/path`, and paths are fuzzy-searchable.
- A referenced resource is fetched and attached to the message.
- When your server supports resources, Claude Code gives Claude tools to list and read them.
- MCP Apps UI resources (a `ui://` URI or the `text/html;profile=mcp-app` media type) are for a host to render, not for Claude to read. They're left out of `@` suggestions and the resource list tool, so a server offering only UI resources shows an empty list. Reading one by its URI still works.

### Prompts as slash commands

Your prompts appear in the `/` menu as `/<server-name>:<prompt-name> (MCP)`. Typing `/mcp__<server-name>__<prompt-name>` also runs one, and the result is injected into the conversation.

Claude Code splits arguments on whitespace into the prompt's parameters and uses the prompt name exactly as declared. **Keep prompt names and argument values free of spaces.**

```text
/mcp__github__list_prs
/mcp__github__pr_review 456
/mcp__jira__create_issue login-bug high
```
