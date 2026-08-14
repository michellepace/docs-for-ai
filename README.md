# Curate Docs For AI (with Claude Code)

Curate documentation from any URL into your own collections. Then ask questions against a collection to get good, grounded answers.

<div align="center">
  <img src="images/example_usage.jpg" alt="Terminal showing a three-step workflow: (1) run /curate-doc on a biome URL, (2) success output with the curated doc and new INDEX.xml entry, (3) /ask-docs queries the docs. Annotations mark each step." width="940">
  <p><em>(1) curate the doc → (2) stored and indexed → (3) ask Qs against the collection</em></p>
</div>

**Why good answers?** The data is cleaner: curated docs beat a raw web fetch or web search. The index forces focus: each collection has an `INDEX.xml` the LLM reader uses to find the docs relevant to your question.

**What is manual?** You need to hand-pick which URLs you want to curate. And every now and again, refresh.

**Curated Collection:**

```text
collections/
└── <collection>/           # eg. biome/, clerk/, uv/
    ├── INDEX.xml           # Routing index for targeted retrieval
    ├── README.md
    └── *.{md,rst,mdx,qmd}  # Curated doc files
```

---

## 📖 Usage

| I want to… | Command |
| :--------- | :------ |
| Ask a collection a question | `/ask-docs <collection> <question>` |
| Curate or refresh a doc | `/curate-doc <collection> <url>` |
| Refresh a whole collection | `/recurate-docs <collection>` |

Workflow:

```bash
# Add a doc — a new URL starts a collection or extends an existing one
/curate-doc tailwind https://tailwindcss.com/docs/theme

# Ask a question — the everyday command
/ask-docs tailwind Is my project using utility classes correctly?

# Refresh a doc — re-run the same URL to pull the latest content
/curate-doc tailwind https://tailwindcss.com/docs/theme

# Re-curate every doc in a collection at once
/recurate-docs tailwind
```

---

## 🚀 Setup

This will set up `/ask-docs`, `/curate-doc` and `/recurate-docs` to work anywhere — not just inside your repo.

```bash
# 1. Install uv
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

# print the absolute path for step 7 below
printf "\n 🌸 Use for step 7:\t" && readlink -f ~/.claude/docs-for-ai
```

**7. Let Claude read your collections from anywhere.** Add one line to your user settings (`~/.claude/settings.json`):

```json
{
  "permissions": {
    "additionalDirectories": ["<paste the path printed by step 6>"]
  }
}
```

**Tip:** GitHub URLs are always fetched, never scraped — faster, cleaner and free. If the website you are curating from has a `.md` twin, make it direct-fetch too: add the prefix to [direct-fetch-rules.toml](src/docs_for_ai/direct-fetch-rules.toml). As a last resort, FireCrawl scrapes.

---

## 📦 Repo Collections

My curations — a starting point. Keep what's useful, delete the rest, re-curate anytime to refresh.

| Collection | Collection Index | Description | Curated | Source |
| :--------- | :--------------- | :---------- | :------ | :----- |
| 📦 [`biome/`](collections/biome/) | 📄 [`INDEX.xml`](collections/biome/INDEX.xml) | Fast linter/formatter | 2025-11-04 | [Official](https://biomejs.dev) |
| 📦 [`claudecode/`](collections/claudecode/) | 📄 [`INDEX.xml`](collections/claudecode/INDEX.xml) | Agentic coding tool | 2026-08-08 | [Official](https://code.claude.com) |
| 📦 [`claudeplat/`](collections/claudeplat/) | 📄 [`INDEX.xml`](collections/claudeplat/INDEX.xml) | Claude API & SDKs | 2026-08-10 | [Official](https://platform.claude.com) |
| 📦 [`clerk/`](collections/clerk/) | 📄 [`INDEX.xml`](collections/clerk/INDEX.xml) | Authentication | 2025-12-03 | [Official](https://clerk.com) |
| 📦 [`coderabbit/`](collections/coderabbit/) | 📄 [`INDEX.xml`](collections/coderabbit/INDEX.xml) | AI code review | 2026-07-27 | [Official](https://docs.coderabbit.ai) |
| 📦 [`convex/`](collections/convex/) | 📄 [`INDEX.xml`](collections/convex/INDEX.xml) | Reactive backend | 2026-07-14 | [Official](https://docs.convex.dev) |
| 📦 [`firecrawl/`](collections/firecrawl/) | 📄 [`INDEX.xml`](collections/firecrawl/INDEX.xml) | Web scraping for AI | 2026-07-18 | [Official](https://docs.firecrawl.dev) |
| 📦 [`marimo/`](collections/marimo/) | 📄 [`INDEX.xml`](collections/marimo/INDEX.xml) | Reactive Python notebooks | 2025-11-11 | [Official](https://docs.marimo.io) |
| 📦 [`mcp/`](collections/mcp/) | 📄 [`INDEX.xml`](collections/mcp/INDEX.xml) | AI integration standard | 2026-08-14 | [Official](https://modelcontextprotocol.io) |
| 📦 [`mdformat/`](collections/mdformat/) | 📄 [`INDEX.xml`](collections/mdformat/INDEX.xml) | Markdown formatter | 2026-07-11 | [Official](https://mdformat.readthedocs.io) |
| 📦 [`nextjs/`](collections/nextjs/) | 📄 [`INDEX.xml`](collections/nextjs/INDEX.xml) | React framework | 2025-12-02 | [Official](https://nextjs.org) |
| 📦 [`playwrightcli/`](collections/playwrightcli/) | 📄 [`INDEX.xml`](collections/playwrightcli/INDEX.xml) | Browser automation CLI | 2026-07-14 | [Official](https://github.com/microsoft/playwright/tree/main/docs/src) |
| 📦 [`rich/`](collections/rich/) | 📄 [`INDEX.xml`](collections/rich/INDEX.xml) | Terminal text formatting | 2026-07-05 | [Official](https://rich.readthedocs.io) |
| 📦 [`shadcn/`](collections/shadcn/) | 📄 [`INDEX.xml`](collections/shadcn/INDEX.xml) | React UI components | 2025-12-16 | [Official](https://ui.shadcn.com), [Guide](https://shadcn.io) |
| 📦 [`shiny/`](collections/shiny/) | 📄 [`INDEX.xml`](collections/shiny/INDEX.xml) | Python web apps | 2025-11-02 | [Official](https://shiny.posit.co/py/) |
| 📦 [`tailwind/`](collections/tailwind/) | 📄 [`INDEX.xml`](collections/tailwind/INDEX.xml) | CSS framework | 2025-10-15 | [Official](https://tailwindcss.com/docs/) |
| 📦 [`tailwindplus/`](collections/tailwindplus/) | 📄 [`INDEX.xml`](collections/tailwindplus/INDEX.xml) | Paid UI components | 2025-11-16 | [Official](https://tailwindcss.com/plus) |
| 📦 [`uv/`](collections/uv/) | 📄 [`INDEX.xml`](collections/uv/INDEX.xml) | Python package manager | 2026-08-12 | [Official](https://github.com/astral-sh/uv/tree/main/docs) |
| 📦 [`vercel/`](collections/vercel/) | 📄 [`INDEX.xml`](collections/vercel/INDEX.xml) | Deployment platform | 2026-07-14 | [Official](https://vercel.com) |
| 📦 [`vitest/`](collections/vitest/) | 📄 [`INDEX.xml`](collections/vitest/INDEX.xml) | Testing framework | 2025-11-05 | [Official](https://vitest.dev) |
| 📦 [`zustand/`](collections/zustand/) | 📄 [`INDEX.xml`](collections/zustand/INDEX.xml) | React state management | 2026-01-03 | [Official](https://zustand.docs.pmnd.rs) |

---

## 🏗️ How This Repo Works

**Workflow:** `/curate-doc <collection> <url>` runs a Python script that fetches the source URL → writes the curated doc file → adds a `collections/<collection>/INDEX.xml` entry with a `PLACEHOLDER` description → Claude Code fills in the description.

The `/curate-doc` command always regenerates the description, whereas `/recurate-docs` only regenerates descriptions for files with content changes.

**Source routing:** A doc is fetched directly when its URL is a GitHub blob, ends in `.md`/`.rst.txt`, or matches a [direct-fetch-rules.toml](src/docs_for_ai/direct-fetch-rules.toml) rule; otherwise FireCrawl scrapes it.

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

---

## 📝 TODO

Regenerate "Descriptions":
- Get status `uv run scripts/collection_status.py`
- Framing shifted from "semantic search" to **LLM routing**, re-curate all.

`scripts/curate-collection.sh`
- Bulk-curates a collection from a URL file, one `claude -p` session per URL.
- One day to replace `/recurate-docs` and `sync-index`... maybe (look deeply).

direct-fetch-rules.toml
- need a new one for `collections/uv/README.md` case
- has to read the page, 404 doesn't always work
- test on https://www.mintlify.com/docs/quickstart
