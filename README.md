# Curate Docs For AI (with Claude Code)

Curate and index documentation from any website into collections like `tailwind/` or `horses/`, then `/ask-docs [collection] [your question]` for a grounded answer — cleaner than a web-fetch, more focussed than a web-search, and keeps AI context sharp.

Each collection is curated from source docs — fetched directly where possible (`.md` URLs, GitHub blobs, or [markdown-allowlist.txt](src/docs_for_ai/markdown-allowlist.txt)), and scraped via the FireCrawl Python SDK only as a last resort. Its `INDEX.xml` is a routing signal an LLM reader uses for targeted context retrieval.

<div align="center">
  <img src="images/example_usage.jpg" alt="Terminal showing three-step workflow: (1) Running /curate-doc biome command, (2) Curation success output showing curated documentation and generated INDEX.xml entry, (3) Use /ask-docs to query docs. Handwritten annotations highlight each step." width="940">
  <p><em>Three Steps: (1) run <code>/curate-doc</code> on a URL → (2) the doc is curated and indexed → (3) <code>/ask-docs</code> to query it</em></p>
</div>

---

## 🚀 Setup

This will setup `/ask-docs`, `/curate-doc` and `/recurate-docs` to work anywhere — not just inside this repo.

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

# 6. Symlink slash commands so they work anywhere
mkdir -p ~/.claude/commands
ln -s "$PWD" ~/.claude/docs-for-ai # anchor (run from repo root)
ln -s ~/.claude/docs-for-ai/.claude/commands/*.md ~/.claude/commands/
```

If a site serves a plain `.md` twin of each page (page URL + ".md"), add its URL prefix (e.g. `https://nextjs.org/docs/`) to [markdown-allowlist.txt](src/docs_for_ai/markdown-allowlist.txt) to fetch those pages directly instead of scraping — faster, cleaner, and free. GitHub URLs and `.md` URLs are always fetched directly.

## 📖 Usage

| I want to… | Command |
|:--|:--|
| Ask a collection a question | `/ask-docs <collection> <question>` |
| Add or refresh a doc | `/curate-doc <collection> <url>` |
| Re-curate a whole collection | `/recurate-docs <collection>` |

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

My curations — a starting point. Keep what's useful, delete the rest, re-curate anytime to refresh.

| Collection | Collection Index | Description | Curated | Source |
|:-----------|:-----------------|:------------|:--------|:-------|
| 📦 [`biome/`](collections/biome/) | 📄 [`INDEX.xml`](collections/biome/INDEX.xml) | Fast linter/formatter | 2025-11-04 | [Official](https://biomejs.dev) |
| 📦 [`claudecode/`](collections/claudecode/) | 📄 [`INDEX.xml`](collections/claudecode/INDEX.xml) | Anthropic Claude Code | 2026-02-05 | [Official](https://code.claude.com) |
| 📦 [`claudeplat/`](collections/claudeplat/) | 📄 [`INDEX.xml`](collections/claudeplat/INDEX.xml) | Anthropic Claude Platform | 2026-01-07 | [Official](https://platform.claude.com) |
| 📦 [`clerk/`](collections/clerk/) | 📄 [`INDEX.xml`](collections/clerk/INDEX.xml) | Authentication | 2025-12-03 | [Official](https://clerk.com) |
| 📦 [`convex/`](collections/convex/) | 📄 [`INDEX.xml`](collections/convex/INDEX.xml) | Reactive database | 2026-01-07 | [Official](https://docs.convex.dev) |
| 🪝 [`lefthook/`](collections/lefthook/) | 📄 [`INDEX.xml`](collections/lefthook/INDEX.xml) | Git hooks manager | 2025-11-24 | [Official](https://github.com/evilmartians/lefthook) |
| 📦 [`marimo/`](collections/marimo/) | 📄 [`INDEX.xml`](collections/marimo/INDEX.xml) | Reactive Python notebooks | 2025-11-11 | [Official](https://docs.marimo.io) |
| 📦 [`nextjs/`](collections/nextjs/) | 📄 [`INDEX.xml`](collections/nextjs/INDEX.xml) | React framework | 2025-12-02 | [Official](https://nextjs.org) |
| 📦 [`playwright/`](collections/playwright/) | 📄 [`INDEX.xml`](collections/playwright/INDEX.xml) | Browser testing | 2025-11-07 | [Official](https://playwright.dev) |
| 📦 [`shadcn/`](collections/shadcn/) | 📄 [`INDEX.xml`](collections/shadcn/INDEX.xml) | React UI components | 2025-12-16 | [Official](https://ui.shadcn.com), [Guide](https://shadcn.io) |
| 📦 [`shiny/`](collections/shiny/) | 📄 [`INDEX.xml`](collections/shiny/INDEX.xml) | Python web apps | 2025-11-02 | [Official](https://shiny.posit.co/py/) |
| 📦 [`tailwind/`](collections/tailwind/) | 📄 [`INDEX.xml`](collections/tailwind/INDEX.xml) | CSS framework | 2025-10-15 | [Official](https://tailwindcss.com/docs/) |
| 📦 [`tailwindplus/`](collections/tailwindplus/) | 📄 [`INDEX.xml`](collections/tailwindplus/INDEX.xml) | Paid UI Components | 2025-11-16 | [Official](https://tailwindcss.com/plus) |
| 📦 [`uv/`](collections/uv/) | 📄 [`INDEX.xml`](collections/uv/INDEX.xml) | Python projects | 2026-05-30 | [Official](https://github.com/astral-sh/uv/tree/main/docs) |
| 📦 [`vercel/`](collections/vercel/) | 📄 [`INDEX.xml`](collections/vercel/INDEX.xml) | Deployment platform | 2025-10-20 | [Official](https://vercel.com) |
| 📦 [`vitest/`](collections/vitest/) | 📄 [`INDEX.xml`](collections/vitest/INDEX.xml) | Testing framework | 2025-11-05 | [Official](https://vitest.dev) |
| 📦 [`zustand/`](collections/zustand/) | 📄 [`INDEX.xml`](collections/zustand/INDEX.xml) | State management | 2026-01-03 | [Official](https://zustand.docs.pmnd.rs) |

## 🏗️ How This Repo Works

**Workflow:** `/curate-doc <collection> <url>` runs a Python script that fetches the source URL → writes a `.md` file → adds a `collections/<collection>/INDEX.xml` entry with a `PLACEHOLDER` description → Claude Code fills in the description.

The `/curate-doc` command always regenerates the description, whereas `/recurate-docs` only regenerates descriptions for files with content changes.

**Source routing:** Direct `.md` URLs and GitHub blobs (`.md`/`.mdx`/`.qmd`) are fetched as-is; FireCrawl scrapes everything else as a fallback.

**Curated Collection:**

```text
collections/
└── <collection>/       # eg. biome/, clerk/, uv/
    ├── INDEX.xml       # Routing index for targeted retrieval
    ├── README.md
    └── *.md            # Curated doc files
```

**INDEX.xml Schema:**

```xml
<docs_index>
  <source>
    <title>[curated source document title]</title>
    <description>[20-30 word routing signal an LLM reader uses to pick this file]</description>
    <source_url>[document source url]</source_url>
    <local_file>[curated .md filename]</local_file>
    <curated_at>YYYY-MM-DD</curated_at>
  </source>
  <!-- One <source> entry per curated .md file -->
</docs_index>
```

---

## 📝 TODO

Regenerate "Descriptions":
- `uv run scripts/collection_status.py`
- Framing has shifted from "semantic search" to **LLM routing**, still need to re-curate.
- Possibly replace `/recurate-docs` via a sequential `claude -p` shell script. Gets all the URLs → downloads / scrapes → does a diff (or git % change) and updates the index only if needed. Replace the command? Possibly related to `scripts/curate-batch.sh`?

Sort out `scripts/`
- delete things

Markdown allowlist
- new collection → get Claude to check for .md twin
- has to read the page, 404 doesn't always work
- test on https://www.mintlify.com/docs/quickstart
- rich blows my paradigm https://rich.readthedocs.io/en/stable/_sources/panel.rst.txt
