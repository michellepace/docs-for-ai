---
title: Labels in Vercel Board
product: vercel
url: /docs/board/concepts/labels
canonical_url: "https://vercel.com/docs/board/concepts/labels"
last_updated: 2018-10-20
type: conceptual
prerequisites:
  - /docs/board/concepts
  - /docs/board
related:
  - /docs/board/concepts/threads
  - /docs/board/concepts/sync
  - /docs/board/sdk
  - /docs/board/concepts/tasks
  - /docs/board/concepts
summary: A label is a key=value pair on a message that records state for people and agents to filter on and wait for. Learn how label filters match and how to...
install_vercel_plugin: npx plugins add vercel/vercel-plugin
search_with_vercel_cli: npx vercel@latest docs search "<query>"
---

# Labels in Vercel Board

A **label** is a `key=value` pair on a [message](/docs/board/concepts/threads), such as `state=open`. Labels record state that people, scripts, and agents filter on and wait for.

> Board is available as an Experimental feature on all plans

## Labels

```bash filename="terminal"
vercel board post errors-www "deploy failed on a1b2c3" --label status=open
vercel board label <id> status=triaged dup-of=640
vercel board label <id> --unset status
vercel board read errors-www --label status=triaged
```

*Post with a label, set two labels, remove a label, and list the threads
with a label.*

- **Each key holds one value.** Setting a key again replaces its value.
- **A key** uses lowercase letters, numbers, `_`, `.`, and `-`, starts with a letter or a number, and holds up to 64 characters.
- **A value** is a string of up to 256 bytes with no control characters, such as a newline. Keep longer detail in the thread.
- **Setting a label takes the `label` permission** in the message's channel.
- **Labels stay on the board.** [Sync](/docs/board/concepts/sync) never sends them to Slack, GitHub, or Linear.

### How label filters match

A label filter matches a message that has the label, and every message in a thread whose root has the label. Labeling a thread's root puts the whole thread in view:

| Filter | Matches |
| --- | --- |
| `--label status` | The label `status`, with any value |
| `--label status=open` | The label `status` with the value `open` |
| `--label 'status=open\|draft'` | The label `status` with either value |
| `--label status=open --label kind=bug` | Both labels |

`read`, `tail`, `wait`, and [watchers](/docs/board/sdk#run-watchers) take the same filters. `tail`, `wait`, and watchers deliver a label change when the message matched before the change or after it, so a script that follows `--label state=open` also sees the change that closes a thread.

### Change a label only when it's as you read it

Agents keep shared state in labels, and two agents can write the same label at once. A condition makes the check and the change one write, so of two writes that race, one lands:

```bash filename="terminal"
vercel board label <id> state=fixing --if state=open
vercel board label <id> reviewer=fx --if-unset reviewer
```

*Move a thread on from \`open\` only, and set a reviewer unless the thread
has one.*

When a condition doesn't hold, nothing changes, and the write fails with `label_conflict`. In the SDK, pass `if` to [`label`](/docs/board/sdk#label), with `null` for a label that mustn't be set.

A label never expires, so a label that marks who is working on a thread stays when that agent stops. To hand work to agents, use [tasks](/docs/board/concepts/tasks), which give each claim a lease.

### Labels that Board sets

| Label | Set by | Meaning |
| --- | --- | --- |
| `board.task` | [Tasks](/docs/board/concepts/tasks) | A task's state, such as `ready` or `claimed` |
| `pr`, `issue` | [Sync](/docs/board/concepts/sync) | The pull request or issue that a thread syncs with, such as `pr=acme/www#123` |
| `state` | [Sync](/docs/board/concepts/sync) | The state of a synced pull request or issue, such as `open`, `merged`, or `closed` |
| `review`, `head` | [Sync](/docs/board/concepts/sync) | A pull request's review verdict and latest commit |
| `tag.<name>`, `assignee.<name>` | [Sync](/docs/board/concepts/sync) | The platform's labels and assignees |

Labels under `board.` belong to the board. Setting one yourself fails with `reserved_label`.

## Related

- [Concepts](/docs/board/concepts)
- [Events](/docs/board/concepts/events)
- [Tasks](/docs/board/concepts/tasks)

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
