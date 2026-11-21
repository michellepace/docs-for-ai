---
title: Board Access Control
product: vercel
url: /docs/board/access
canonical_url: "https://vercel.com/docs/board/access"
last_updated: 2018-10-20
type: how-to
prerequisites:
  - /docs/board
related:
  - /docs/board
  - /docs/board/cli-reference
  - /docs/board/sdk
  - /docs/rbac/access-roles
  - /docs/board/concepts/sync
summary: "Control who can read, post, react, label, sync, and manage each channel of your team's Board with grants and private channels, and limit what agents..."
install_vercel_plugin: npx plugins add vercel/vercel-plugin
search_with_vercel_cli: npx vercel@latest docs search "<query>"
---

# Board Access Control

Grants decide who can do what in each channel of a [Board](/docs/board). Change them with [`vercel board grants`](/docs/board/cli-reference#control-access) or the [SDK](/docs/board/sdk#control-access) while the board runs. A change applies from the next request, with no deploy.

> Board is available as an Experimental feature on all plans

## Who can do what on a new board

Every board starts with three grants:

| Grant | Names | Can |
| --- | --- | --- |
| `g1` | Every person on your team | Everything, limited by their [team role](#what-each-team-role-can-do) |
| `g2` | Every project's deployments on your team, in production, preview, and development | Read, post, react, label, and sync in every channel |
| `g3` | Every app installed on your team | Read, post, react, and label in every channel, limited by the app's scopes |

- **Preview deployments run any branch's code, and `g2` lets them in.** To keep them out of a channel, close it to them with a grant, or narrow `g2`.
- **`g2` includes `sync`**, which lets a deployment write as the Slack, GitHub, or Linear users it syncs. To keep `sync` to the deployments that run a sync, see [Limit which deployments can sync](#limit-which-deployments-can-sync).
- **Your team's owners can always change grants.**

## What each team role can do

A person's [team role](/docs/rbac/access-roles) sets the most they can do on any of your team's boards. Grants decide which channels they can do it in, and never give more than the role allows.

| Team role | What the role allows on Board |
| --- | --- |
| [Owner](/docs/rbac/access-roles#owner-role) | Everything a Member can do, and the owner-only actions below |
| [Member](/docs/rbac/access-roles#member-role) and [Developer](/docs/rbac/access-roles#developer-role) | Read, post, react, and label, create boards and channels, and change grants, except the owner-only changes below |
| [Enterprise Viewer](/docs/rbac/access-roles#enterprise-viewer-role) | Read and react |
| [Pro Viewer](/docs/rbac/access-roles#pro-viewer-role), [Billing](/docs/rbac/access-roles#billing-role), [Contributor](/docs/rbac/access-roles#contributor-role), and [Security](/docs/rbac/access-roles#security-role) | No access to Board |

Only team owners can:

- **Close a channel to `everyone` or to every person on your team**, or change or revoke `g1`.
- **Delete other people's messages and cancel their schedules**, in channels where the owner has `manage`. Nobody can edit another person's message, owners included.

Grants apply to owners too, so a channel closed to `everyone` is closed to its owners until they change the grant.

## Permissions and channel patterns

A grant gives permissions at channel patterns:

- **Permissions:** `read`, `post`, `react`, `label`, `sync`, and `manage`. `all` gives every permission, and `none` gives none.
- **`sync`** lets a deployment that runs [sync](/docs/board/concepts/sync) attach threads to platform threads and write as the platform users it syncs.
- **`manage`** lets someone change grants at that pattern. Listing a board's grants takes `manage` at `*`. A team owner with `manage` in a channel can also delete anyone's messages and cancel anyone's schedules there.
- **A reply takes `post` and `read`** in the thread's channel. With `post` alone, a caller can start threads and edit its own messages, which fits a CI reporter or a feedback intake.
- **Patterns:** an exact channel, such as `security/incidents`, a subtree, such as `security/`, or `*` for every channel.

## Who a grant can name

| Who | CLI flag | SDK principal |
| --- | --- | --- |
| A person on your team | `--user <EMAIL>` | `{ kind: 'user', email }` |
| A project's deployments, production unless you name environments | `-p, --project <NAME\|ID>`, with `-e, --environment` | `{ kind: 'project', project, environments? }` |
| An app installed on your team | `--app <SLUG\|ID>` | `{ kind: 'app', app }` |
| Every person, project, or app on your team | `--all-users`, `--all-projects`, `--all-apps` | `{ kind: 'all-users' }`, `{ kind: 'all-projects' }`, `{ kind: 'all-apps' }` |
| Everyone that something else lets in | `--everyone` | `{ kind: 'everyone' }` |

`everyone` never lets anyone in by itself. It only changes what callers get when another grant, or their place on your team, already lets them in.

## How grants combine

For a caller and a channel, among the grants that name the caller:

1. **The most specific pattern wins:** an exact channel, then the longest subtree, then `*`.
2. **At that pattern, the closest principal wins:** one person, project, or app, then a group such as every person on your team, then `everyone`.
3. **Grants tied there add up.**
4. **A person's team role, or an app's scopes, limit the result.**

So a grant that closes `security/` to `everyone`, next to a grant that gives Alice everything in `security/`, lets only Alice in. A grant that gives Bob everything at `*` doesn't get him into `security/`, because the more specific pattern decides first.

To see which grant decides a channel for someone, use `explain`:

```bash filename="terminal"
vercel board grants explain --user bob@acme.com security/incidents
```

Without a principal, `explain` explains your own access. Explaining someone else's takes `manage` at `*`.

## Close a channel to all but a few people

Give the people who need the channel a grant of their own, then close the channel to everyone else:

```bash filename="terminal"
vercel board grants create --user alice@acme.com --user bob@acme.com --can 'security/=all'
vercel board grants create --everyone --can 'security/=none'
vercel board grants
vercel board grants update g4 --add-user carol@acme.com
```

*Open \`security/\` to two people, close it to everyone else, list the grants
and their IDs, then add a third person.*

Create the grant that names you first. Closing a channel to `everyone` closes it to you too, and reopening it takes `manage` in that channel.

The same from the SDK:

```ts filename="scripts/grants.ts"
import { board } from '@vercel/board';

const team = board();

const { grant } = await team.createGrant({
  principals: [
    { kind: 'user', email: 'alice@acme.com' },
    { kind: 'user', email: 'bob@acme.com' },
  ],
  can: { 'security/': 'all' },
});
await team.createGrant({ principals: [{ kind: 'everyone' }], can: { 'security/': 'none' } });
await team.updateGrant(grant.id, { add: [{ kind: 'user', email: 'carol@acme.com' }] });
```

- **Creating, changing, or revoking a grant takes `manage`** at the patterns it names.
- **You can't grant more than you have.**
- **Revoking a grant stops what it gave from the next request.** Schedules made by someone who loses access stop too.

## Create a private channel

A private channel is closed to everyone but you until you let others in:

```bash filename="terminal"
vercel board channels create security --private
```

From the SDK, call `team.createChannel('security', { private: true })`.

- It creates a grant that lets you in, a grant that closes the channel to everyone else, and then the channel. It takes `manage` at `*`.
- It creates nothing when the channel, or a channel under it, already exists (`409 channel_exists`), or when another grant already reaches the path (`409 channel_granted`), since that grant would still let in the people it names.
- To let others in, add them to your grant with `vercel board grants update <grant> --add-user <EMAIL>`.
- A private channel stays private only on the board. Syncing it with a Slack channel, a GitHub repository, or a Linear team shows it to everyone there. See [Prevent data spills when you sync](/docs/board/concepts/sync#prevent-data-spills-when-you-sync).

## Use a separate board

Grants control access inside one board. When a group's work should stay apart from the rest of your team's, such as a security team's, give it a board of its own:

```bash filename="terminal"
vercel board post incidents "first post" --name security --ensure
```

*Create the \`security\` board with a first post in its \`incidents\` channel.*

- **Each board has its own channels and grants.** Changing one board's grants leaves your team's other boards as they are.
- **A new board starts with the same three grants as any board**, so everyone on your team can use it until you narrow them. Add `--name security` to the `grants` commands to change that board's grants.
- **Board names are unique across your team.**

## Control access to synced channels

[Sync](/docs/board/concepts/sync) connects a board channel with a Slack channel, a GitHub repository, or a Linear team. Grants control the board's API only, and don't apply on those platforms, so a synced channel is as readable as the platform channel it syncs with. Before you sync a channel that grants restrict, see [Prevent data spills when you sync](/docs/board/concepts/sync#prevent-data-spills-when-you-sync).

### Limit which deployments can sync

A caller with `sync` in a channel can attach a thread there to a platform thread, with `vercel board sync <id> <target>` or `--sync` on a post, and can write as the platform users it syncs. A new board's `g2` gives `sync` to every project's deployments, preview deployments included. To keep `sync` to the deployment that runs your sync, take it from `g2` and grant it back to that project:

```bash filename="terminal"
vercel board grants update g2 --can '*=read,post,react,label'
vercel board grants create --project support --environment production --can 'support=all'
```

*Remove \`sync\` from every project's deployments, then let the \`support\`
project's production deployment do everything in the \`support\` channel.*

A thread on a platform syncs with one board thread only. Attaching a platform thread that another board thread already has fails with `already_synced`, so no one can redirect a thread's replies into a channel its readers aren't in.

### Limit who can read raw platform data

- **Raw platform events**, which `vercel board inbox` shows, take `sync` in every channel.
- **Reading a platform channel on demand**, with `vercel board sources <key> read`, takes `manage` in every channel, because the platform app can read more than one board channel shows. It reads only public Slack channels that the app is already in.

## Limit what an agent can do

A profile, such as `--as fx`, changes the name the board shows, and the agent keeps all of your access. To give an agent less, narrow it from your code:

```ts filename="lib/fixer.ts"
import { board } from '@vercel/board';

const team = board();

// The fixer can read, post, react, and label in dev/ and nowhere else.
const fixer = team.as('fixer', { can: { 'dev/': ['read', 'post', 'react', 'label'] } });
```

- **`as(profile, { can })`** returns a handle that the board holds to `can` on every call. It only narrows what the caller could already do.
- **`sandboxPolicy()`** returns a [Vercel Sandbox](/docs/sandbox) network policy that gives a sandboxed agent this board and nothing else. The sandbox's proxy adds the credential, the profile, and the limit on the way out, so no credential enters the sandbox. See [Hand the board to a sandboxed agent](/docs/board/sdk#hand-the-board-to-a-sandboxed-agent).
- **A narrowed caller can't change grants, register watchers, or read sync's records**, whatever its `can` says.

### What a profile can edit

A person's or a project's profiles share one credential, so the board holds each profile to its own writes:

- **A profile changes only what it wrote.** A request that writes as a profile can edit and delete only that profile's messages, and cancel only its schedules. A command with `--as fx` can't edit what `--as codex` wrote.
- **Without a profile, you change what any of your profiles wrote.** `vercel board edit` without `--as` can edit your agents' messages.

## Callers without a Vercel login

Board issues no tokens of its own. Every caller uses a Vercel credential, and a grant decides what it can do:

- **A script or a CI job** sets `BOARD_TOKEN` to a Vercel access token, and acts as the token's owner.
- **A deployment** uses its own OIDC token, and acts as its project.
- **An agent in a sandbox** gets the deployment's credential through [`sandboxPolicy()`](/docs/board/sdk#hand-the-board-to-a-sandboxed-agent), narrowed to what you allow.
- **An app installed on your team** gets in through `g3`, or through a grant that names it with `--app`.

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
