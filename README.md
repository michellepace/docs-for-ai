# Curate Docs For AI (with Claude Code)

Curate and index documentation from any website into collections like
`tailwind/` or `horses/`, then `/ask-docs [collection] [your question]` for a
grounded answer — cleaner than a web-fetch, more focussed than a web-search, and
keeps AI context sharp.

Each collection is curated from source docs — fetched directly where possible
(`.md` URLs, GitHub blobs, or sites in the
[direct-fetch-rules.toml](src/docs_for_ai/direct-fetch-rules.toml)), and scraped
via FireCrawl as a last resort. Its `INDEX.xml` is a routing signal an LLM
reader uses for targeted context retrieval.

<div align="center">
  <img src="images/example_usage.jpg" alt="Terminal showing a three-step workflow: (1) run /curate-doc on a biome URL, (2) success output with the curated doc and new INDEX.xml entry, (3) /ask-docs queries the docs. Annotations mark each step." width="940">
  <p><em>Three Steps: (1) run <code>/curate-doc</code> on a URL → (2) the doc is curated and indexed → (3) <code>/ask-docs</code> to query it</em></p>
</div>

______________________________________________________________________

## 🚀 Setup

This will setup `/ask-docs`, `/curate-doc` and `/recurate-docs` to work anywhere
— not just inside this repo.

```bash
# 1. Install UV
# 👉 https://docs.astral.sh/uv/getting-started/installation/

# 2. Clone repository
git clone https://github.com/michellepace/docs-for-ai.git
cd docs-for-ai

# 3. Get free FireCrawl API key
# Visit: https://www.firecrawl.dev/app/api-keys

# 4. Add to your shell profile
echo 'export API_KEY_MCP_FIRECRAWL=your-api-key-here' >> ~/.zshrc
source ~/.zshrc  # Use ~/.bashrc if that's your shell

# 5. Install dependencies and git hooks (commit/push)
uv sync && uv run pre-commit install

# 6. Make the slash commands work anywhere
# anchor (run from repo root)
ln -sfn "$PWD" ~/.claude/docs-for-ai
# make all slash commands work from anywhere
mkdir -p ~/.claude/commands
ln -sf ~/.claude/docs-for-ai/.claude/commands/*.md ~/.claude/commands/

printf "\n 🌸 Use for step 7:\t" && readlink -f ~/.claude/docs-for-ai
```

**7. Let Claude read your collections from anywhere.** Add one line to your user
settings (`~/.claude/settings.json`):

```json
{
  "permissions": {
    "additionalDirectories": ["<paste the path printed by step 6>"]
  }
}
```

Use the absolute path printed by step 6 (`readlink -f`), not
`~/.claude/docs-for-ai` — permissions are checked against the resolved path.

To direct-fetch a site instead of scraping it — faster, cleaner, free — add its
URL prefix to the
[direct-fetch-rules.toml](src/docs_for_ai/direct-fetch-rules.toml): `append-md`
for `.md` twins (page + `.md`, e.g. `https://nextjs.org/docs/`) or `readthedocs`
for Sphinx sites. GitHub blob URLs and `.md` URLs are always direct.

## 📖 Usage

| I want to…                   | Command                             |
| :--------------------------- | :---------------------------------- |
| Ask a collection a question  | `/ask-docs <collection> <question>` |
| Add or refresh a doc         | `/curate-doc <collection> <url>`    |
| Re-curate a whole collection | `/recurate-docs <collection>`       |

Example:

```bash
# Ask a question — the everyday command
/ask-docs tailwind Is my project using utility classes correctly?

# Add a doc — a new URL starts a collection or extends an existing one
/curate-doc tailwind https://tailwindcss.com/docs/theme

# Refresh a doc — re-run the same URL to pull the latest content
/curate-doc tailwind https://tailwindcss.com/docs/theme

# Re-curate every doc in a collection at once
/recurate-docs tailwind
```

## 📦 Repo Collections

My curations — a starting point. Keep what's useful, delete the rest, re-curate
anytime to refresh.

| Collection                                      | Collection Index                                     | Description                  | Curated    | Source                                                        |
| :---------------------------------------------- | :--------------------------------------------------- | :--------------------------- | :--------- | :------------------------------------------------------------ |
| 📦 [`biome/`](collections/biome/)               | 📄 [`INDEX.xml`](collections/biome/INDEX.xml)        | Fast linter/formatter        | 2025-11-04 | [Official](https://biomejs.dev)                               |
| 📦 [`claudecode/`](collections/claudecode/)     | 📄 [`INDEX.xml`](collections/claudecode/INDEX.xml)   | Anthropic Claude Code        | 2026-02-05 | [Official](https://code.claude.com)                           |
| 📦 [`claudeplat/`](collections/claudeplat/)     | 📄 [`INDEX.xml`](collections/claudeplat/INDEX.xml)   | Anthropic Claude Platform    | 2026-01-07 | [Official](https://platform.claude.com)                       |
| 📦 [`clerk/`](collections/clerk/)               | 📄 [`INDEX.xml`](collections/clerk/INDEX.xml)        | Authentication               | 2025-12-03 | [Official](https://clerk.com)                                 |
| 📦 [`convex/`](collections/convex/)             | 📄 [`INDEX.xml`](collections/convex/INDEX.xml)       | Reactive database            | 2026-01-07 | [Official](https://docs.convex.dev)                           |
| 📦 [`marimo/`](collections/marimo/)             | 📄 [`INDEX.xml`](collections/marimo/INDEX.xml)       | Reactive Python notebooks    | 2025-11-11 | [Official](https://docs.marimo.io)                            |
| 📦 [`mdformat/`](collections/mdformat/)         | 📄 [`INDEX.xml`](collections/mdformat/INDEX.xml)     | Markdown formatter & wrapper | 2026-07-11 | [Official](https://mdformat.readthedocs.io)                   |
| 📦 [`nextjs/`](collections/nextjs/)             | 📄 [`INDEX.xml`](collections/nextjs/INDEX.xml)       | React framework              | 2025-12-02 | [Official](https://nextjs.org)                                |
| 📦 [`playwright/`](collections/playwright/)     | 📄 [`INDEX.xml`](collections/playwright/INDEX.xml)   | Browser testing              | 2025-11-07 | [Official](https://playwright.dev)                            |
| 📦 [`shadcn/`](collections/shadcn/)             | 📄 [`INDEX.xml`](collections/shadcn/INDEX.xml)       | React UI components          | 2025-12-16 | [Official](https://ui.shadcn.com), [Guide](https://shadcn.io) |
| 📦 [`shiny/`](collections/shiny/)               | 📄 [`INDEX.xml`](collections/shiny/INDEX.xml)        | Python web apps              | 2025-11-02 | [Official](https://shiny.posit.co/py/)                        |
| 📦 [`tailwind/`](collections/tailwind/)         | 📄 [`INDEX.xml`](collections/tailwind/INDEX.xml)     | CSS framework                | 2025-10-15 | [Official](https://tailwindcss.com/docs/)                     |
| 📦 [`tailwindplus/`](collections/tailwindplus/) | 📄 [`INDEX.xml`](collections/tailwindplus/INDEX.xml) | Paid UI Components           | 2025-11-16 | [Official](https://tailwindcss.com/plus)                      |
| 📦 [`uv/`](collections/uv/)                     | 📄 [`INDEX.xml`](collections/uv/INDEX.xml)           | Python projects              | 2026-05-30 | [Official](https://github.com/astral-sh/uv/tree/main/docs)    |
| 📦 [`vercel/`](collections/vercel/)             | 📄 [`INDEX.xml`](collections/vercel/INDEX.xml)       | Deployment platform          | 2025-10-20 | [Official](https://vercel.com)                                |
| 📦 [`vitest/`](collections/vitest/)             | 📄 [`INDEX.xml`](collections/vitest/INDEX.xml)       | Testing framework            | 2025-11-05 | [Official](https://vitest.dev)                                |
| 📦 [`zustand/`](collections/zustand/)           | 📄 [`INDEX.xml`](collections/zustand/INDEX.xml)      | State management             | 2026-01-03 | [Official](https://zustand.docs.pmnd.rs)                      |

## 🏗️ How This Repo Works

**Workflow:** `/curate-doc <collection> <url>` runs a Python script that fetches
the source URL → writes the curated doc file → adds a
`collections/<collection>/INDEX.xml` entry with a `PLACEHOLDER` description →
Claude Code fills in the description.

The `/curate-doc` command always regenerates the description, whereas
`/recurate-docs` only regenerates descriptions for files with content changes.

**Source routing:** A doc is fetched directly when its URL is a GitHub blob,
ends in `.md`/`.rst.txt`, or matches a
[direct-fetch-rules.toml](src/docs_for_ai/direct-fetch-rules.toml) rule;
otherwise FireCrawl scrapes it.

**Curated Collection:**

```text
collections/
└── <collection>/       # eg. biome/, clerk/, uv/
    ├── INDEX.xml       # Routing index for targeted retrieval
    ├── README.md
    └── *.{md,rst,mdx,qmd}  # Curated doc files
```

**INDEX.xml Schema:**

```xml
<docs_index>
  <source>
    <title>[curated source document title]</title>
    <description>[20-30 word routing signal an LLM reader uses to pick this file]</description>
    <source_url>[document source url]</source_url>
    <local_file>[curated doc filename]</local_file>
    <curated_at>YYYY-MM-DD</curated_at>
  </source>
  <!-- One <source> entry per curated doc file -->
</docs_index>
```

______________________________________________________________________

## 📝 TODO

Regenerate "Descriptions":

- `uv run scripts/collection_status.py`
- Framing has shifted from "semantic search" to **LLM routing**, still need to
  re-curate.
- Possibly replace `/recurate-docs` via a sequential `claude -p` shell script.
  Gets all the URLs → downloads / scrapes → does a diff (or git % change) and
  updates the index only if needed. Replace the command? Possibly related to
  `scripts/curate-batch.sh`?

Sort out `scripts/`

- delete things

direct-fetch-rules.toml

- new collection → get Claude to check for a direct-fetch twin (`.md` or RST
  source)
- has to read the page, 404 doesn't always work
- test on https://www.mintlify.com/docs/quickstart
- ✅ Read the Docs sites (e.g. rich) now fetch RST source via the `readthedocs`
  transform
