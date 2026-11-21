---
title: Channels in Vercel Board
product: vercel
url: /docs/board/concepts/channels
canonical_url: "https://vercel.com/docs/board/concepts/channels"
last_updated: 2018-10-20
type: conceptual
prerequisites:
  - /docs/board/concepts
  - /docs/board
related:
  - /docs/board/concepts/boards
  - /docs/board/concepts/threads
  - /docs/board/access
  - /docs/board/concepts/sync
summary: A channel is a named path on a board, such as dev or www/production, that holds threads. Learn how channels are named, created, grouped into...
install_vercel_plugin: npx plugins add vercel/vercel-plugin
search_with_vercel_cli: npx vercel@latest docs search "<query>"
---

# Channels in Vercel Board

A **channel** is a named path on a [board](/docs/board/concepts/boards), such as `dev`, `errors-www`, or `www/production`. A channel holds [threads](/docs/board/concepts/threads), and access to a board is decided channel by channel.

> Board is available as an Experimental feature on all plans

## Names

A channel's path is one or more segments of lowercase letters, numbers, `_`, and `-`, joined by `/`. A channel's path never changes.

## How a channel is created

```bash filename="terminal"
vercel board post errors-www "deploy failed on a1b2c3"
vercel board channels create dev/alerts
```

*Create the \`errors-www\` channel with its first post, and create an empty
channel.*

- **The first post creates the channel**, so channels need no setup.
- **`channels create` creates a channel before anything posts to it**, so a watcher can follow it or people can find it. A channel that already exists stays as it is.
- **Creating a channel takes `read` and `post`** in it.

## Subtrees

A `/` in a path groups channels. `www/production` and `www/preview` both sit under `www/`.

A trailing slash names the whole subtree wherever a channel goes:

```bash filename="terminal"
vercel board read www/
vercel board tail www/ --label kind=bug
vercel board grants create --user ada@acme.com --can 'www/=all'
```

*Read every channel under \`www/\`, follow bugs in all of them, and grant
access to the whole subtree.*

## List channels

`vercel board channels` lists the channels you can read, grouped by path prefix. A channel you can't read doesn't appear.

## Who can use a channel

On a new board, the whole team can use every channel: every person, within their team role, every project's deployments, and every installed app. [Grants](/docs/board/access) change that for one channel, a subtree, or the whole board:

- **Close a channel to all but a few people.** See [Close a channel to all but a few people](/docs/board/access#close-a-channel-to-all-but-a-few-people).
- **Create a private channel** that only you can use, with `vercel board channels create <channel> --private`. See [Create a private channel](/docs/board/access#create-a-private-channel).

A channel's grants apply on the board only. A channel that [syncs](/docs/board/concepts/sync) with a Slack channel, a GitHub repository, or a Linear team is as readable as that platform channel. See [Prevent data spills when you sync](/docs/board/concepts/sync#prevent-data-spills-when-you-sync).

## Related

- [Boards](/docs/board/concepts/boards)
- [Threads](/docs/board/concepts/threads)
- [Board Access Control](/docs/board/access)

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
