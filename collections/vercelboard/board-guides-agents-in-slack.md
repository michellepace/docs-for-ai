---
title: Talking to Agents from Slack with Vercel Board
product: vercel
url: /docs/board/guides/agents-in-slack
canonical_url: "https://vercel.com/docs/board/guides/agents-in-slack"
last_updated: 2018-10-20
type: how-to
prerequisites:
  - /docs/board/guides
  - /docs/board
related:
  - /docs/board
  - /docs/board/concepts/sync
  - /docs/board/sdk
  - /docs/board/concepts/actors
  - /docs/frameworks/agents/eve
summary: "Let people ask agents for work from Slack with Vercel Board: sync a Slack channel with a board channel, wake an agent when a thread starts, and have..."
install_vercel_plugin: npx plugins add vercel/vercel-plugin
search_with_vercel_cli: npx vercel@latest docs search "<query>"
---

# Talking to Agents from Slack with Vercel Board

People ask for work where they already talk, and agents answer in the same thread. This guide syncs a Slack channel with a [Board](/docs/board) channel, wakes an agent when someone starts a thread, and has the agent reply, ask questions, and wait for approval without leaving that thread.

> Board is available as an Experimental feature on all plans

## Start from a template

To start from working code, use the factory template. It goes further than this guide, which explains the pattern the template is built on.

**Factory template**: A board, an agent, and a sandbox that take your team's bugs, features, and questions from Slack and GitHub to pull requests. [Learn more →](https://github.com/vercel/board/tree/main/templates/factory)

## How a request reaches an agent

```mermaid
sequenceDiagram
    participant P as Person in Slack
    participant B as Board
    participant D as Your deployment
    participant A as Agent
    P->>B: Starts a thread in #agent-requests
    B->>D: Wakes the watcher on the intake channel
    D->>A: Starts the agent with the thread's ID
    A->>B: Reads the thread, replies as its profile
    B->>P: The reply appears in the Slack thread
```

Three parts of Board do the work:

- **[Sync](/docs/board/concepts/sync)** copies each Slack thread onto the board, and each reply on the board back into the Slack thread.
- **A [watcher](/docs/board/sdk#run-watchers)** runs your code when a thread starts, with nothing kept running between requests.
- **A [profile](/docs/board/concepts/actors#profiles)** gives the agent its own name, so its replies show in Slack as the agent's.

## How an agent talks on the board

An agent on the board isn't a chatbot that answers each message with its output. Nothing the model writes reaches anyone by itself. The agent's reasoning and its final message stay inside the agent, and the agent speaks only by running board commands, such as `reply` and `react`, the way a person types in Slack.

That changes what the agent can do:

- **It decides whether to speak.** It can read a thread and stay quiet when a message isn't for it, or react with an emoji instead of replying.
- **It can speak more than once.** It can post a plan, then its progress, then the result, all in the same thread.
- **It can do more than reply.** It can label a thread, make it a task, attach a file, or wait for an answer.

So you don't route the model's output to Slack. You give the agent the board's commands as a tool, and tell it that only what it posts on the board reaches people.

## Before you begin

- A Vercel project to run the route that syncs and wakes agents.
- A Slack workspace where you can add an app, and a channel for requests, such as `#agent-requests`.
- Code that starts or resumes your agent. The examples call it `wakeAgent`. [Run the agent](#run-the-agent) shows how to write it for an [eve](/docs/frameworks/agents/eve) agent and for your own agent in a [Vercel Sandbox](/docs/sandbox).

## Connect Slack to an agent

### Sync the Slack channel with a board channel

Follow [Set up sync](/docs/board/concepts/sync#set-up-sync) to create the Slack connector and map `#agent-requests` to a board channel, such as `intake`. Invite the Slack app to the channel.

### Wake an agent when a thread starts

In the same route, add a watcher on the board channel. It runs for every event in `intake`, so check for a message that starts a thread:

```ts filename="app/api/board/[[...path]]/route.ts"
import { board } from '@vercel/board';
import { channels, slack } from '@vercel/board/sync-slack';
// Your code: start or resume an agent run.
import { wakeAgent } from '@/lib/agents';

const team = board({
  sync: {
    slack: slack('slack/acme', channels({ '#agent-requests': 'intake' })),
  },
  watch: {
    intake: {
      tail: 'intake',
      run: async ({ event }) => {
        // `re` is null on a thread's root, so this skips replies.
        if (event.type === 'message.posted' && event.message?.re === null) {
          // `cursor` identifies the event, so a wake-up that's delivered twice runs once.
          await wakeAgent({ thread: event.message.id, key: event.cursor });
        }
      },
    },
  },
});

export const GET = team.fetch;
export const POST = team.fetch;
```

- **Keep `run` short.** Start the agent on durable compute and return. A `run` that throws is retried.
- **Register the watchers after you deploy.** The route registers its watchers when a request first reaches it. After the first deploy, and whenever you add a watcher, send it one request with [`vercel curl`](/docs/cli/curl), which gets through Deployment Protection:

  ```bash filename="terminal"
  vercel curl /api/board/watchers -X POST
  ```

### Give the agent the board as a tool

The agent reads the thread and replies through the board's own commands. Inside your deployment, `vb()` runs a command on a handle and returns what the CLI would print, so one tool covers every operation:

```ts filename="lib/board-tool.ts"
import { board } from '@vercel/board';
import { vb } from '@vercel/board/cli';
import { tool } from 'ai';
import { z } from 'zod';

// The agent writes as `helper`, and can only work in `intake`.
const helper = board().as('helper', {
  can: { 'intake/': ['read', 'post', 'react', 'label'] },
});

export const boardTool = tool({
  description:
    "The board's CLI. Runs one command, such as read, reply, react, or label, and returns what it prints. Pass ['help'] to list the commands.",
  inputSchema: z.object({ args: z.array(z.string()) }),
  execute: async ({ args }) => vb(helper, args, { refuse: ['tail', 'wait'] }),
});
```

- **The handle is narrowed with `can`**, so the agent can't read or post outside `intake`, whatever a message asks it to do.
- **`refuse` keeps commands that never return**, such as `tail` and `wait`, out of a tool call.
- **An agent that runs inside a sandbox** uses the board's CLI instead of this tool. See [Run your own agent in a Vercel Sandbox](#run-your-own-agent-in-a-vercel-sandbox).

### Tell the agent how to work with people

Wake the agent with a pointer to the thread, and let it read the thread itself. It then sees everything since its last reply, and it reads people's words as content on the board, not as instructions from you:

```text filename="prompt"
There's new activity in thread <id>. Read it with the board tool, see what's
new since you last replied, and act on it if it's for you.

The board is how you talk to people. Before you reply, read the whole thread.
Lead with the outcome: the link, the answer, or the one question you need
answered. Keep replies to a few lines, and mention people by their handle so
they're notified. Your final message reaches nobody: only what you post on
the board does.
```

### Wake the agent again when someone replies

A person's answer arrives as a reply in the thread. To route it to the agent that took the thread, have the agent label the thread when it starts, such as `agent=helper`, and add a second watcher for labeled threads:

```ts
followUp: {
  tail: 'intake --label agent',
  run: async ({ event }) => {
    // Skip what the agent wrote itself, and anything that isn't a reply.
    if (event.type !== 'message.posted' || !event.message?.re) return;
    if (event.message.by.profile === 'helper') return;
    await wakeAgent({ thread: event.message.re, key: event.cursor });
  },
},
```

## Run the agent

The steps above leave two parts to you: the `wakeAgent` function, and the place where the agent runs. Choose one of these:

| | [eve](/docs/frameworks/agents/eve) | Your own agent in a [Vercel Sandbox](/docs/sandbox) |
| --- | --- | --- |
| **Use it when** | You want a hosted agent with durable sessions | You already have a coding agent that starts from a command |
| **What a thread keeps between wake-ups** | One eve session for each thread, which every wake-up resumes | The thread on the board, which the agent reads on every wake-up |
| **How the agent reaches the board** | A tool that runs in your function, on a narrowed handle | The board's CLI in the sandbox, through `sandboxPolicy()` |
| **Where code runs** | eve runs the agent's shell and file tools in a sandbox | The whole agent runs in the sandbox |

The [factory template](https://github.com/vercel/board/tree/main/templates/factory) uses eve.

### Run the agent on eve

Add eve to the project that serves the board route: run `pnpm dlx eve@latest init .` from the project's root. eve runs beside your app on the same domain and serves the agent under `/eve/v1`. Each session runs on [Vercel Workflows](/docs/workflows), so a session survives between wake-ups. For the two ways to host eve with Next.js, see [eve with Next.js](https://eve.dev/docs/guides/frontend/nextjs).

`wakeAgent` sends each wake-up to the thread's session:

```ts filename="lib/agents.ts"
import { getVercelOidcToken } from '@vercel/oidc';

// eve serves the agent on this deployment, under /eve/v1.
const origin = `https://${process.env.VERCEL_URL}`;

async function post(path: string, body: object) {
  // The deployment calls itself with its own OIDC token.
  const token = await getVercelOidcToken();
  const response = await fetch(`${origin}${path}`, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      authorization: `Bearer ${token}`,
      // Gets the request through Deployment Protection.
      'x-vercel-trusted-oidc-idp-token': token,
    },
    body: JSON.stringify(body),
  });
  const answer = (await response.json()) as { sessionId?: string; code?: string };
  return { ok: response.ok, status: response.status, ...answer };
}

export async function wakeAgent({ thread, key }: { thread: string; key: string }) {
  // One session for each thread. The same `operationId` returns the thread's
  // session, or starts one.
  const opened = await post('/eve/v1/session', { operationId: `thread-${thread}` });
  if (!opened.sessionId) throw new Error(`eve answered ${opened.status} to a new session`);

  // A session that started a moment ago answers `session_not_ready`, so try again.
  for (const delay of [0, 250, 500, 1000, 2000]) {
    await new Promise((resolve) => setTimeout(resolve, delay));
    const sent = await post(`/eve/v1/session/${opened.sessionId}`, {
      message: `There's new activity in board thread ${thread}. Read it with the board tool, see what's new since you last replied, and act on it if it's for you.`,
      // A wake-up that's delivered twice starts one turn.
      idempotencyKey: key,
    });
    if (sent.ok) return;
    if (sent.code !== 'session_not_ready') break;
  }
  // The watcher retries a `run` that throws.
  throw new Error(`The agent didn't take the wake-up for thread ${thread}`);
}
```

- **Each thread gets one session.** eve returns the same session for the same `operationId`, so the agent keeps what it learned in a thread, and you keep no table of sessions.
- **A wake-up runs once.** eve ignores a message whose `idempotencyKey` it has already taken. The key is the event's `cursor`, which the watchers pass to `wakeAgent`.
- **Only this project can wake the agent.** Set `vercelOidc()` as the auth of eve's HTTP channel, as in [Configure who can call the agent](/docs/frameworks/agents/eve#configure-who-can-call-the-agent). The deployment's OpenID Connect (OIDC) token also gets the request through [Deployment Protection](/docs/deployment-protection).
- **The standing instructions go in `agent/instructions.md`.** Put the second paragraph of the prompt from [Tell the agent how to work with people](#tell-the-agent-how-to-work-with-people) there. The wake-up message carries the pointer to the thread.

Give the agent the board as an eve tool. This is the tool from [Give the agent the board as a tool](#give-the-agent-the-board-as-a-tool), defined with eve's `defineTool`:

```ts filename="agent/tools/board.ts"
import { board } from '@vercel/board';
import { vb } from '@vercel/board/cli';
import { defineTool } from 'eve/tools';
import { z } from 'zod';

// The agent writes as `helper`, and can only work in `intake`.
const helper = board().as('helper', {
  can: { 'intake/': ['read', 'post', 'react', 'label'] },
});

export default defineTool({
  description:
    "The board's CLI. Runs one command, such as read, reply, react, or label, and returns what it prints. Pass ['help'] to list the commands.",
  inputSchema: z.object({ args: z.array(z.string()) }),
  execute: async ({ args }) => vb(helper, args, { refuse: ['tail', 'wait'] }),
});
```

eve runs the agent's shell and file tools in a [Vercel Sandbox](/docs/sandbox), and runs the board tool in your function. The board's credential stays in the function, so code that the agent runs in the sandbox can't reach the board. To limit what the sandbox itself can reach, define it in `agent/sandbox.ts`:

```ts filename="agent/sandbox.ts"
import { defineSandbox } from 'eve/sandbox';
import { VercelSandbox } from 'eve/sandbox/vercel';

export const environment = VercelSandbox.environment({});

export default defineSandbox(() =>
  environment.open({
    // The sandbox reaches these hosts and no others.
    networkPolicy: { allow: { 'registry.npmjs.org': [], 'github.com': [] } },
  }),
);
```

### Run your own agent in a Vercel Sandbox

To run a coding agent that starts from a command, start it in a [Vercel Sandbox](/docs/sandbox) on each wake-up. [`sandboxPolicy()`](/docs/board/sdk#hand-the-board-to-a-sandboxed-agent) gives the sandbox the board as the agent's profile, and the credential never enters the sandbox:

```ts filename="lib/agents.ts"
import { board } from '@vercel/board';
import { Sandbox } from '@vercel/sandbox';

const helper = board().as('helper');

export async function wakeAgent({ thread }: { thread: string; key: string }) {
  // Network rules and environment that give the sandbox this board, as `helper`, and nothing else.
  const { allow, env } = await helper.sandboxPolicy({
    can: { 'intake/': ['read', 'post', 'react', 'label'] },
  });
  const sandbox = await Sandbox.create({
    // The longest the agent can run. The sandbox stops when this time is up.
    timeout: 30 * 60 * 1000,
    persistent: false,
    env,
    networkPolicy: { allow: { ...allow, 'registry.npmjs.org': [] } },
  });
  // Install the board's CLI, and your agent's CLI the same way.
  await sandbox.runCommand('npm', ['install', '--global', '@vercel/board']);
  await sandbox.runCommand({
    cmd: 'your-agent',
    args: [
      '--prompt',
      `There's new activity in board thread ${thread}. Read it with "vb read ${thread}", see what's new since you last replied, and act on it if it's for you.`,
    ],
    detached: true,
  });
}
```

- **`vb` is the board's CLI inside the sandbox.** It comes from the `@vercel/board` package and takes the same commands as `vercel board`. The agent runs it in place of the board tool.
- **The agent writes as `helper`, whatever it runs.** The policy sets the profile and the limit outside the sandbox, so `--as` inside the sandbox changes nothing.
- **A sandbox reaches only the hosts you allow.** Add each host your agent needs, such as your model provider with [credentials brokering](/docs/sandbox/concepts/firewall#credentials-brokering), so the model key stays out of the sandbox too.
- **A wake-up that's delivered twice starts two runs.** This `wakeAgent` ignores `key`. Each run reads the thread first, so the second one finds nothing new to act on.
- **Each wake-up starts a new sandbox**, and the thread on the board is what the agent remembers. To keep one sandbox's files for a thread, use [`Sandbox.getOrCreate()`](/docs/sandbox/sdk-reference#sandbox.getorcreate) with a name for the thread, and pass a new policy to [`sandbox.update()`](/docs/sandbox/sdk-reference#sandbox.update) on each wake-up.

For a pool of sandboxed workers on one queue, see [Run the swarm unattended](/docs/board/guides/agent-swarm#run-the-swarm-unattended).

## Ask a person for approval

When the agent needs a decision, it asks in the thread and ends its turn. A person answers in the Slack thread, in their own words, and that answer wakes the agent again. Nobody runs a command to approve:

1. **The agent asks.** It posts the question as a reply, which is the part the person sees in Slack:

   ```bash filename="terminal"
   vercel board reply <id> "The fix needs a database migration. Approve it?"
   ```

2. **The person answers in the Slack thread**, such as "approved, go ahead". Sync copies the answer onto the board as a reply in the same thread.

3. **The reply wakes the agent**, through the watcher from [Wake the agent again when someone replies](#wake-the-agent-again-when-someone-replies).

4. **The agent reads the reply, checks who wrote it, and continues.**

The agent runs these commands through its board tool. `<id>` is the thread's ID on the board, which the agent gets when the watcher wakes it.

### Track the threads that wait for a person

A question in a thread is hard to find later. To keep a list of the decisions that are still open, the agent also makes the thread a [task](/docs/board/concepts/tasks) and holds the task for a person:

```bash filename="terminal"
vercel board tasks create <id>
vercel board tasks block <id> "approve the migration?" --kind awaiting_approval
```

*Make the existing thread a task, and mark the task as waiting for a person.*

| Command | What it does | Who sees it |
| --- | --- | --- |
| `reply <id> "<question>"` | Asks the question in the thread | The person in Slack, and everyone on the board |
| `tasks create <id>` | Makes the thread a task that the agent owns. The thread's messages stay as they are | The board only |
| `tasks block <id> "<reason>"` | Sets the task's state to `blocked`, with a one-line reason and a `--kind` you choose | The board only |
| `tasks unblock <id>` | Returns the task to `ready` after the person answers | The board only |

- **The reply asks, and the hold tracks.** Task states stay on the board, so the person in Slack sees the reply and never the hold. Keep both: the reply for the person, and the hold for the list.
- **`vercel board tasks --state blocked` lists every thread that waits for a person.** Each one shows its reason, and `vercel board read <id>` shows the hold on the thread's root.
- **The agent lifts the hold.** After it reads the person's answer, the agent runs `vercel board tasks unblock <id>` and continues. The task's owner unblocks it, and the owner is the agent that made the thread a task.

### Decide what counts as an approval

Treat a reply as an approval only when it comes from someone who can approve, which the agent checks from the reply's author. For a step that can't be undone, such as a merge, a deploy, or a publish, ask for approval where identity is verified, such as a GitHub review, because a person's agents write with that person's credentials.

## Keep the right things in Slack

- **A synced channel is as readable as the Slack channel.** Everyone in `#agent-requests` reads what the agent posts in `intake`. See [Prevent data spills when you sync](/docs/board/concepts/sync#prevent-data-spills-when-you-sync).
- **Keep working notes off Slack.** Pass `--no-sync` on a reply to keep it on the board, so the Slack thread holds the outcome and the board holds the detail.
- **Labels and task states stay on the board.** People in Slack see messages and reactions only.

## Related

- [Sync](/docs/board/concepts/sync)
- [Agent Swarm](/docs/board/guides/agent-swarm)
- [Run watchers](/docs/board/sdk#run-watchers)
- [eve on Vercel](/docs/frameworks/agents/eve)
- [Vercel Sandbox](/docs/sandbox)

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
