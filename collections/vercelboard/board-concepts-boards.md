---
title: Boards in Vercel Board
product: vercel
url: /docs/board/concepts/boards
canonical_url: "https://vercel.com/docs/board/concepts/boards"
last_updated: 2018-10-20
type: conceptual
prerequisites:
  - /docs/board/concepts
  - /docs/board
related:
  - /docs/board/concepts/channels
  - /docs/board/access
  - /docs/board/concepts/events
  - /docs/board/cli-reference
  - /docs/board/concepts
summary: A board is the top-level container for a Vercel team\
install_vercel_plugin: npx plugins add vercel/vercel-plugin
search_with_vercel_cli: npx vercel@latest docs search "<query>"
---

# Boards in Vercel Board

A **board** is the top-level container for a team's messages. Every Vercel team has one board to start with, and can keep more.

> Board is available as an Experimental feature on all plans

## What a board holds

A board belongs to one Vercel team, and holds three things:

- **[Channels](/docs/board/concepts/channels)**, which hold the board's threads.
- **[Grants](/docs/board/access)**, which decide who can do what in each channel.
- **An [event log](/docs/board/concepts/events)**, which records every change to the board in order.

Nothing on one board shows on another. Use a separate board when a group's work should stay apart from the rest of the team's, such as a security team's. See [Use a separate board](/docs/board/access#use-a-separate-board).

## Names

- **Every team has a default board, named General.** `vercel board` and `board()` use it unless you name another.
- **A team can keep more boards, each with a name**, such as `security`. A name is 1 to 64 characters with no `/`, and it matches regardless of case.
- **Board names are unique across the team**, private boards included. A name that's taken fails with `board_name_taken`.
- **Each board has a URL**, `https://api.vercel.com/v1/messageboard/boards/<board>?teamId=<team>`, which `vercel board whoami` prints.

## How a named board is created

```bash filename="terminal"
vercel board read dev --name security
vercel board post dev "first post" --name security --ensure
```

*Read a named board, and create the board with its first post if the team
doesn't have one by that name.*

- **The CLI only finds a board by default.** A name the team doesn't have fails with `board_not_found`, so a typo creates nothing. Add `--ensure` to create the board.
- **The SDK creates a named board on first use.** `board({ name: 'security' })` creates the board the first time anyone uses a name the team doesn't have. Pass `ensure: false` to only find it.
- **A new board starts with the same three grants as any board**, so everyone on the team can use it until you narrow them.

## Which board a command uses

`vercel board` and `board()` use the first board that one of these sets:

1. A board's URL, from `--url` or `BOARD_URL`.
2. A team and a name, from `--scope` and `--name`, or the `team` and `name` options.
3. The team of the Vercel project you're in.
4. Your login's default team.

Run `vercel board whoami` to check which board a command uses. See [Choose a board](/docs/board/cli-reference#choose-a-board).

## Related

- [Channels](/docs/board/concepts/channels)
- [Board Access Control](/docs/board/access)
- [Concepts](/docs/board/concepts)

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
