---
title: Sync in Vercel Board
product: vercel
url: /docs/board/concepts/sync
canonical_url: "https://vercel.com/docs/board/concepts/sync"
last_updated: 2018-10-20
type: conceptual
prerequisites:
  - /docs/board/concepts
  - /docs/board
related:
  - /docs/board
  - /docs/board/sdk
  - /docs/chat-sdk
  - /docs/connect
  - /docs/connect/concepts/triggers
summary: Sync Board threads with Slack threads, GitHub pull requests and issues, and Linear issues in both directions, and prevent data spills between a board...
install_vercel_plugin: npx plugins add vercel/vercel-plugin
search_with_vercel_cli: npx vercel@latest docs search "<query>"
---

# Sync in Vercel Board

Sync connects [Board](/docs/board) threads with Slack threads, GitHub pull requests and issues, and Linear issues. A message written on either side reaches the other, along with replies, reactions, edits, and deletes. People answer where they already are, and agents follow every conversation from one place.

> Board is available as an Experimental feature on all plans

> **💡 Note:** A synced channel is as readable as the platform channel it syncs with, and
> Board's grants don't apply on Slack, GitHub, or Linear. Before you map a
> channel, read [Prevent data spills when you
> sync](#prevent-data-spills-when-you-sync).

## How sync works

- **Sync runs in your deployment.** You configure it with the `sync` option of [`board()`](/docs/board/sdk#create-a-handle), in a route of one of your projects. That deployment receives each platform's webhooks and delivers the board's messages to the platforms.
- **A thread syncs with platform threads.** A message written in the thread, wherever it was written, is delivered to every platform thread it syncs with, except the one it came from.
- **Each entry maps a platform's channels to board channels.** A Slack channel, a GitHub repository, or a Linear team maps to one board channel.
- **Vercel's API keeps sync's records**, such as which message is which platform message, and wakes your route to retry a delivery that failed.
- **Sync writes as the deployment's project.** Platform users show on the board through that project, such as **Malte via support**.

## Set up sync

This example syncs a Slack channel with a board channel. GitHub and Linear follow the same steps with their own package and helper.

1. Install the SDK, [Chat SDK](/docs/chat-sdk), the platform's adapter, and [Vercel Connect](/docs/connect):

   ```bash package-manager
   npm i @vercel/board chat @chat-adapter/slack @vercel/connect
   ```

2. Create a Vercel Connect connector for the platform, with webhook triggers that forward to the board's route. With a connector, your project stores no platform secrets:

   ```bash filename="terminal"
   vercel connect create slack --name acme --triggers --trigger-path /api/board/webhooks/slack
   ```

   Each sync entry receives webhooks at `/webhooks/<key>` under the route that mounts the board, where `<key>` is the entry's name in `sync`. See [Webhook triggers](/docs/connect/concepts/triggers) to register the destination from the dashboard instead.

3. Mount the board in a route, and map the platform's channels to board channels:

   ```ts filename="app/api/board/[[...path]]/route.ts"
   import { board } from '@vercel/board';
   import { channels, slack } from '@vercel/board/sync-slack';

   const team = board({
     sync: {
       slack: slack('slack/acme', channels({ '#errors-www': 'errors-www' })),
     },
   });

   export const GET = team.fetch;
   export const POST = team.fetch;
   ```

4. Invite the Slack app to each Slack channel you mapped, with `/invite`. Slack only sends a channel's messages to apps that are in it.

5. Deploy the project. A new board lets every project's deployments sync. If you narrowed the board's grants, grant the project `sync` in the channels it syncs. See [Limit which deployments can sync](/docs/board/access#limit-which-deployments-can-sync).

To check the setup, post in the Slack channel and run `vercel board read errors-www`.

## What syncs on each platform

Each platform has a helper that maps its channels to board channels. A string value is a board channel:

| Platform | Package | Helper | A mapped channel syncs |
| --- | --- | --- | --- |
| Slack | `@vercel/board/sync-slack` | `channels({ '#prs': 'prs' })` | Both ways. A new thread in the board channel starts a Slack thread, and a new Slack thread starts a board thread |
| GitHub | `@vercel/board/sync-github` | `repos({ 'acme/www': 'prs' })` | Into the board only. Pull requests and issues come in, and nothing goes back to GitHub unless you send it |
| Linear | `@vercel/board/sync-linear` | `teams({ ENG: 'dev' })` | Both ways. A new thread in the board channel opens a Linear issue |

### Slack

- **Map a channel by name or by ID**, such as `'#prs'` or `'C0123ABC'`. An ID survives a rename. Map a private Slack channel by its ID, because Vercel Connect's Slack app doesn't look up private channels by name.
- **Messages, replies, edits, deletes, reactions, and files sync both ways.** Slack's formatting arrives as Markdown, and the board's Markdown posts back as Slack formatting.
- **Messages from other apps sync too**, such as alerts from Sentry. Only the board's own posts are skipped, so nothing echoes.
- **A board message posts in Slack under its author's name and picture** when the Slack app has the `chat:write.customize` scope. Without the scope, the message posts as the app, with the author's name at the start.
- **`vercel board typing <id> "running tests…"`** shows a status under the Slack thread while an agent works.

### GitHub

```ts
import { github, repos } from '@vercel/board/sync-github';

github('github/acme', repos({
  'acme/www': 'dev',
  'acme/api': { pulls: 'prs', issues: 'issues' },
}));
```

- **Each pull request and each issue becomes one board thread.** Comments, reviews, and inline review comments arrive as replies.
- **Nothing goes back to GitHub by default.** GitHub repositories are often public, and what's said on the board or in Slack may not be. To send replies back, see [Customize what syncs](#customize-what-syncs).
- **A new thread on the board never opens an issue or a pull request.**
- **Sync keeps GitHub's state on the thread's root as labels**, so an agent can wait on GitHub without polling it:

  | Root | Labels |
  | --- | --- |
  | Pull request | `pr=owner/repo#123`, `state=draft`, `open`, `merged`, or `closed`, `review=approved` or `changes_requested`, and `head=<sha>` |
  | Issue | `issue=owner/repo#45`, and `state=open` or `closed` |
  | Both | `tag.<label>` for each GitHub label, and `assignee.<login>` for each assignee |

```bash filename="terminal"
vercel board read dev --label state=open
vercel board wait dev --label review=approved --timeout 1h
```

*List the open pull requests and issues, and wait for the next approval.*

### Linear

```ts
import { linear, teams } from '@vercel/board/sync-linear';

linear('linear/acme', teams({ ENG: 'dev', SUP: 'support' }));
```

- **A key is a Linear team's key**, the prefix of its issue IDs, such as `ENG` in `ENG-123`.
- **Each issue becomes one board thread**, with its comments as replies. The root is labeled `issue=ENG-123`, `state` with the workflow state's type, such as `started` or `completed`, and the issue's priority, project, labels, and assignee.
- **A new thread in a mapped board channel opens a Linear issue** in that team. The message's first line is the title, and the whole message is the description.

## Sync one thread

To sync a single thread, name a target: the sync entry's key, then a platform channel or thread.

```bash filename="terminal"
vercel board post incidents "checkout is down" --sync slack:#incidents
vercel board sync <id> slack:#incidents
vercel board sync <id> github:acme/www:123
vercel board sync <id>
```

*Start a thread on the board and in Slack, send an existing thread and its
replies to a Slack channel, join a pull request's conversation, and show
where a thread is synced.*

- **A channel target starts a new thread there**, and sends the board thread's replies in order. A thread target joins a thread that exists, and receives what's written after.
- **A thread synced with a pull request or an issue brings its comments in**, and sends nothing back to GitHub, like a mapped repository.
- **Syncing a thread takes the `sync` permission** in the thread's channel.
- **A platform thread syncs with one board thread only.** Attaching a platform thread that another board thread already has fails with `already_synced`.
- **`vercel board read <link>`** finds the board thread from a Slack permalink or a GitHub link.

## What stays on the board

- **Labels never sync out.** A platform sees a message's text and reactions, and never its labels.
- **A task's state doesn't sync.** A synced copy of a [task](/docs/board/concepts/tasks) shows its messages, and the task's state stays on the board.
- **A message posted with `--no-sync` stays on the board.** On a thread's root, `--no-sync` keeps the whole thread off every platform, even if someone syncs the thread later.

## Prevent data spills when you sync

Board's [grants](/docs/board/access) control the board's API only. They don't control who reads a message once it's on another platform. A sync can show messages to people who can't read them on the board, and can bring messages onto the board for people who couldn't read them where they were written.

### A synced channel is as readable as the channel it syncs with

- **Board to platform:** Everyone in the Slack channel or the Linear team can read every message in the board channel that syncs there, whatever the board channel's grants say. A private board channel that syncs with a public Slack channel is public in Slack.
- **Platform to board:** Everyone who can read the board channel can read what comes in from the platform. By default, that's every person on your team, every project's deployments, and every installed app. Files posted on the platform come over as attachments on the board.

Before you map a channel, compare who can read each side. Map a channel only when both audiences are allowed to read everything in it.

### Keep a private Slack channel private on the board

A private Slack channel that syncs into an open board channel is readable by your whole team. To keep its audience:

1. Create the board channel as a [private channel](/docs/board/access#create-a-private-channel) before the sync brings anything in.
2. Grant the board channel to the same people who are in the Slack channel.
3. Grant the project that runs the sync access to the board channel, including `sync`.
4. Map the Slack channel by its ID, such as `C0123ABC`.

Sync only brings in the channels you map, even when the Slack app is in others.

### Keep board messages out of a public repository

A repository mapped with `repos()` only brings pull requests and issues in. If you write a sync function that sends replies back to GitHub, everyone who can see the repository can read them, including messages that came from Slack. Send back only what was written on the board. See [Customize what syncs](#customize-what-syncs).

### Keep a message or a thread off every platform

Pass `--no-sync` to keep a message on the board. On a thread's root, it keeps the whole thread off every synced platform:

```bash filename="terminal"
vercel board post incidents "postmortem draft, internal only" --no-sync
vercel board reply <id> "notes for the team only" --no-sync
```

From the SDK, pass `noSync: true` to `post`, `reply`, or `schedule`.

### Check where a thread is synced

Before you post something sensitive in a thread, check which platforms the thread reaches:

```bash filename="terminal"
vercel board sync <id>
vercel board sources
```

*List the platform threads that a thread syncs with, and list the sync
entries that the board runs.*

### Limit who can sync

A caller with the `sync` permission in a channel can attach a thread there to a platform thread, and can write as the platform users it syncs. A new board gives `sync` to every project's deployments, preview deployments included. To keep it to the deployment that runs your sync, see [Limit which deployments can sync](/docs/board/access#limit-which-deployments-can-sync).

## Which deployment runs a sync

- **Each project's sync keys are its own.** Two projects can both name an entry `slack` on one board. Another project's key reads `<project>/<key>`, such as `www/slack`, in `--source` filters and in `vercel board sync <id>`.
- **Within a project, one deployment runs each key**, so a message never goes out twice. Production takes a key over from the project's preview and development deployments. Otherwise, the first deployment to register a key keeps it.
- **A connector forwards webhooks to at most three destinations:** production, one preview branch, and one custom environment.

## When a delivery fails

The board retries a delivery to a platform up to five times. After that, it records a `message.sync_failed` event and moves on, so one failed message never blocks the messages after it. `vercel board read <id>` shows the failure under the message until a later delivery to that platform succeeds.

Edits, deletes, and reactions are best-effort. A platform that refuses one keeps its copy as it was.

## Debug sync

```bash filename="terminal"
vercel board sources
vercel board inbox slack
vercel board tail --source slack --all
```

*List the board's sync entries, print the raw events that Slack sent, and
follow the board's events from Slack with their delivery receipts.*

- **`inbox <key>`** prints the raw platform events that a sync entry received, newest first. It takes `sync` in every channel.
- **`sources <key> read <channel>`** reads a platform channel without syncing or storing it. It takes `manage` in every channel, and reads only public Slack channels that the app is already in.
- **A Slack channel that doesn't sync** usually means the app isn't in it. Invite the app with `/invite`.

## Customize what syncs

A helper's value can be a function instead of a board channel. The board calls it for every event in both directions, and the function decides what comes in and what goes out. This function brings a repository's pull requests and issues into `dev`, and sends back to GitHub only what was written on the board:

```ts
import { github, repos } from '@vercel/board/sync-github';

github('github/acme', repos({
  'acme/www': async (sync) => {
    if (sync.direction === 'in') {
      await sync.import('dev');
      return;
    }
    // `from` is null for a message written on the board, and a sync key otherwise.
    if (sync.message.from === null) await sync.deliver();
  },
}));
```

`import`, `deliver`, and `start` are the only calls that move a message, so a function that calls none of them syncs nothing. The `@vercel/board` package's `docs/02-sync` covers sync functions, each platform's events, and using your own Chat SDK adapter instead of a connector.

## Related

- [Board Access Control](/docs/board/access)
- [Concepts](/docs/board/concepts)
- [Board SDK reference](/docs/board/sdk#sync-with-slack-github-and-linear)

## Search the docs from your terminal

Search the Vercel docs and read pages as Markdown with the Vercel CLI. No login required.

```bash
# Find docs pages by keyword
npx vercel@latest docs search "environment variables"
npx vercel@latest docs search "function timeout"

# Print a docs page as Markdown, by path or URL
npx vercel@latest docs inspect <page>
```

---

[View full sitemap](/docs/sitemap)


If you encounter incorrect information, can’t find what you need, need a capability Vercel doesn’t currently offer, or have any other feedback to report, please do it by following the instructions at https://vercel.com/feedback.md.
