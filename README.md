# Curate Docs For AI (with Claude Code)

Curate and index documentation from any website into collections like `tailwind/` or `horses/`, then `/ask-docs [collection] [your question]` for a grounded answer — cleaner than a web-fetch, more focussed than a web-search, and keeps AI context sharp.

Each collection is curated from source docs — fetched directly where possible (`.md` URLs, GitHub blobs, or [markdown-allowlist.txt](src/docs_for_ai/markdown-allowlist.txt)), and scraped via the FireCrawl Python SDK only as a last resort. Its `INDEX.xml` is a routing signal an LLM reader uses for targeted context retrieval.

<div align="center">
  <img src="images/example_usage.jpg" alt="Terminal showing three-step workflow: (1) Running /curate-doc biome command, (2) Curation success output showing curated documentation and generated INDEX.xml entry, (3) Use /ask-docs to query docs. Handwritten annotations highlight each step." width="940">
  <p><em>Three Steps: (1) run <code>/curate-doc</code> on a URL → (2) the doc is curated and indexed → (3) <code>/ask-docs</code> to query it</em></p>
</div>

## 📦 Repo Collections

Available collections in this repo:

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

*Curate your own collections. The [lefthook](collections/lefthook/) collection is non-standard — docs are downloaded directly from GitHub. For Anthropic docs use [this tool](https://github.com/ericbuess/claude-code-docs).*

---

## 🚀 Setup

**(1) First these 5 steps:**

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

# 5. Install git hooks (lint, type-check & test on commit/push)
uv run pre-commit install
```

**(2) Anchor the repo at a fixed location** (run from the repo root). The commands reference the repo through this single symlink — universal across machines, so the command files never need editing no matter where you cloned:

```bash
ln -s "$PWD" ~/.claude/docs-for-ai
```

**(3) Symlink the commands you want available everywhere** (pointed *through* the anchor):

```bash
mkdir -p ~/.claude/commands
ln -s ~/.claude/docs-for-ai/.claude/commands/ask-docs.md      ~/.claude/commands/ask-docs.md
ln -s ~/.claude/docs-for-ai/.claude/commands/curate-doc.md    ~/.claude/commands/curate-doc.md
ln -s ~/.claude/docs-for-ai/.claude/commands/recurate-docs.md ~/.claude/commands/recurate-docs.md
```

Now `/ask-docs`, `/curate-doc` and `/recurate-docs` work from any directory. Everything routes through the `~/.claude/docs-for-ai` anchor, so there's one source of truth — to relocate the repo, just re-point that one symlink.

## 📖 Usage via Slash Commands

| Slash Command | Purpose | .md Files | INDEX `<source>` |
|:--------|:--------|:----------|:----------|
| `/curate-doc <collection> <url>` | Add new or re-curate | ✅ Write | ✅ Add/update INDEX.xml |
| `/recurate-docs <collection>` | Re-curate all docs | ✅ Write all | ✅ Selective update INDEX.xml |
| `/ask-docs <collection> <question>` | Query any collection | Docs analysed | Relevant docs identified |

## 💡 Usage Example

Assume tailwind was not already a collection in this repo:

```bash
# Start a new collection
/curate-doc tailwind https://tailwindcss.com/docs/customizing-colors
# → Creates collections/tailwind/ collection directory, with README.md + INDEX.xml, and first curated doc

# Re-curate existing doc (refresh content from same URL)
/curate-doc tailwind https://tailwindcss.com/docs/customizing-colors
# → Re-curates, writes .md file, replaces source in INDEX.xml

# Curate a new doc into collection
/curate-doc tailwind https://tailwindcss.com/docs/styling-with-utility-classes
# → Curates page into collection, writes .md file, adds source to INDEX.xml

# Re-curate all docs in collection
/recurate-docs tailwind
# → Re-curates all URLs in INDEX.xml, writes all .md files, updates descriptions for changed content

# ✨ Use the docs
/ask-docs tailwind Please evaluate my project for correct usage of utility classes?
# → Searches collections/tailwind/INDEX.xml for relevant docs, analyses these, gives you an answer
```

## 🏗️ How This Repo Works

**Workflow:** `/curate-doc <collection> <url>` runs a Python script that fetches the source URL → writes a `.md` file → adds a `collections/<collection>/INDEX.xml` entry with a `PLACEHOLDER` description → Claude Code fills in the description.

The `/curate-doc` command always regenerates the description, whereas `/recurate-docs` only regenerates descriptions for files with content changes.

**Source routing:** Direct `.md` URLs and GitHub blobs (`.md`/`.mdx`/`.qmd`) are fetched as-is; FireCrawl scrapes everything else as a fallback.

**Curated Collection:**

```text
collections/
└── collection-name/
    ├── INDEX.xml           # Index of all docs
    ├── README.md
    ├── api-reference.md    # Curated doc
    ├── getting-started.md  # Curated doc
    └── ...
```

**INDEX.xml Schema:**

```xml
<docs_index>
  <source>
    <title>Hello Document Title</title>
    <description>20-30 word routing signal an LLM reader uses to pick this file...</description>
    <source_url>https://docs.example.com/hello</source_url>
    <local_file>hello-document-title.md</local_file>
    <curated_at>2025-10-15</curated_at>
  </source>
  <!-- Multiple <source> entries, one per .md file -->
</docs_index>
```

---

## 📝 TODO - Regenerate "Descriptions" (2026-05-31)

Collections still have `PLACEHOLDER` descriptions — run `/recurate-docs` on each.

The framing has shifted from "semantic search" to **LLM routing**, so existing descriptions should also be regenerated to match the current rules in [.claude/references/source-descriptions.md](.claude/references/source-descriptions.md).

## 📝 TODO - Replace `/recurate-docs`

Use `claude -p` sequentially - gets all the URLs → downloads / scrapes → does a diff (or git % change) and updates the index only if needed. Replace the command and iterate on that?

## 📝 TODO - sort out `scripts/`

Improve `scripts/curate-batch.sh` and raise into README

Also the others or DELETE.

## 📝 TODO - populate `markdown-allowlist.txt`

When a new collection is made, get claude command in `/curate-doc` to establish if we can add it e.g https://www.mintlify.com/docs/quickstart. Need to handle not everyone does a 404 - "did it return x lines and expected content?"

Exclude new collections in `recurate-docs/` whatever I do there.
