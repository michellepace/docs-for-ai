# Curate Docs For AI (with Claude Code)

Curate and index documentation from any website into collections like `tailwind/`, `horses/`, etc. Reference collection indexes in your AI chats (e.g. `@tailwind/INDEX.xml what's a utility?`) so that only relevant docs are analysed. Much cleaner than a web-fetch and more focussed than a web-search. Keep your AI context sharp.

<div align="center">
  <img src=".images/example_usage.jpg" alt="Terminal showing three-step workflow: (1) Running /curate-doc biome command, (2) Curation success output showing scraped documentation and generated INDEX.xml entry, (3) Use /ask-docs to query docs. Handwritten annotations highlight each step." width="940">
  <p><em>Complete workflow: curate → auto scrape → "/ask-docs biome Validate my config file please"</em></p>
</div>

## 📦 Repo Collections

Available collections in this repo:

| Collection | Collection Index | Description | Scraped | Source |
|:-----------|:-----------------|:------------|:--------|:-------|
| 📦 [`biome/`](biome/) | 📄 [`INDEX.xml`](biome/INDEX.xml) | Fast linter/formatter | 2025-11-04 | [Official](https://biomejs.dev) |
| 📦 [`claudecode/`](claudecode/) | 📄 [`INDEX.xml`](claudecode/INDEX.xml) | Anthropic Claude Code | 2026-02-05 | [Official](https://code.claude.com) |
| 📦 [`claudeplat/`](claudeplat/) | 📄 [`INDEX.xml`](claudeplat/INDEX.xml) | Anthropic Claude Platform | 2026-01-07 | [Official](https://platform.claude.com) |
| 📦 [`clerk/`](clerk/) | 📄 [`INDEX.xml`](clerk/INDEX.xml) | Authentication | 2025-12-03 | [Official](https://clerk.com) |
| 📦 [`convex/`](convex/) | 📄 [`INDEX.xml`](convex/INDEX.xml) | Reactive database | 2026-01-07 | [Official](https://docs.convex.dev) |
| 🪝 [`lefthook/`](lefthook/) | 📄 [`INDEX.xml`](lefthook/INDEX.xml) | Git hooks manager | 2025-11-24 | [Official](https://github.com/evilmartians/lefthook) |
| 📦 [`marimo/`](marimo/) | 📄 [`INDEX.xml`](marimo/INDEX.xml) | Reactive Python notebooks | 2025-11-11 | [Official](https://docs.marimo.io) |
| 📦 [`nextjs/`](nextjs/) | 📄 [`INDEX.xml`](nextjs/INDEX.xml) | React framework | 2025-12-02 | [Official](https://nextjs.org) |
| 📦 [`playwright/`](playwright/) | 📄 [`INDEX.xml`](playwright/INDEX.xml) | Browser testing | 2025-11-07 | [Official](https://playwright.dev) |
| 📦 [`shadcn/`](shadcn/) | 📄 [`INDEX.xml`](shadcn/INDEX.xml) | React UI components | 2025-12-16 | [Official](https://ui.shadcn.com), [Guide](https://shadcn.io) |
| 📦 [`shiny/`](shiny/) | 📄 [`INDEX.xml`](shiny/INDEX.xml) | Python web apps | 2025-11-02 | [Official](https://shiny.posit.co/py/) |
| 📦 [`tailwind/`](tailwind/) | 📄 [`INDEX.xml`](tailwind/INDEX.xml) | CSS framework | 2025-10-15 | [Official](https://tailwindcss.com/docs/) |
| 📦 [`tailwindplus/`](tailwindplus/) | 📄 [`INDEX.xml`](tailwindplus/INDEX.xml) | Paid UI Components | 2025-11-16 | [Official](https://tailwindcss.com/plus) |
| 📦 [`uv/`](uv/) | 📄 [`INDEX.xml`](uv/INDEX.xml) | Python projects | 2026-05-30 | [Official](https://github.com/astral-sh/uv/tree/main/docs) |
| 📦 [`vercel/`](vercel/) | 📄 [`INDEX.xml`](vercel/INDEX.xml) | Deployment platform | 2025-10-20 | [Official](https://vercel.com) |
| 📦 [`vitest/`](vitest/) | 📄 [`INDEX.xml`](vitest/INDEX.xml) | Testing framework | 2025-11-05 | [Official](https://vitest.dev) |
| 📦 [`zustand/`](zustand/) | 📄 [`INDEX.xml`](zustand/INDEX.xml) | State management | 2026-01-03 | [Official](https://zustand.docs.pmnd.rs) |

*Curate your own collections. The [lefthook](lefthook/) collection is non-standard — docs are downloaded directly from GitHub. For Anthropic docs use [this tool](https://github.com/ericbuess/claude-code-docs).*

---

## 🚀 Setup

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
```

## 📖 Usage via Slash Commands

> [!IMPORTANT]
> Edit the paths in [.claude/commands/ask-docs.md](.claude/commands/ask-docs.md) to match your local setup. To use from anywhere, move it to `~/.claude/commands/`.

| Slash Command | Purpose | .md Files | INDEX `<source>` |
|:--------|:--------|:----------|:----------|
| `/curate-doc <collection> <url>` | Add new or re-scrape | ✅ Write | ✅ Add/update INDEX.xml |
| `/rescrape-docs <collection>` | Re-scrape all docs | ✅ Write all | ✅ Selective update INDEX.xml |
| `/improve-index-xml <collection>` | Batch improve descriptions | 📖 Read | ✅ Update INDEX.xml |
| `/ask-docs <collection> <question>` | Query any collection | Docs analysed | Relevant docs identified |

## 💡 Usage Example

Assume tailwind was not already a collection in this repo:

```bash
# Start a new collection
/curate-doc tailwind https://tailwindcss.com/docs/customizing-colors
# → Creates tailwind/ collection directory, with README.md + INDEX.xml, and first curated doc

# Re-scrape existing doc (refresh content from same URL)
/curate-doc tailwind https://tailwindcss.com/docs/customizing-colors
# → Re-scrapes, writes .md file, replaces source in INDEX.xml

# Curate a new doc into collection
/curate-doc tailwind https://tailwindcss.com/docs/styling-with-utility-classes
# → Scrapes page into collection, writes .md file, adds source to INDEX.xml

# Re-scrape all docs in collection
/rescrape-docs tailwind
# → Re-scrapes all URLs in INDEX.xml, writes all .md files, updates descriptions for changed content

# ✨ Use the docs
/ask-docs tailwind Please evaluate my project for correct usage of utility classes?
# → Searches tailwind/INDEX.xml for relevant docs, analyses these, gives you an answer
```

## 🏗️ How This Repo Works

**Workflow:** `/curate-doc <collection> <url>` runs a Python script that fetches the source URL → writes a `.md` file → adds a `collection/INDEX.xml` entry with a `PLACEHOLDER` description → Claude Code fills in the description.

The `/curate-doc` command always regenerates the description, whereas `/rescrape-docs` only regenerates descriptions for files with content changes.

**Source routing:** Direct `.md` URLs and GitHub blobs (`.md`/`.mdx`/`.qmd`) are fetched as-is; FireCrawl scrapes everything else as a fallback.

**Curated Collection:**

```text
collection-name/
├── INDEX.xml               # Index of all docs
├── README.md
├── api-reference.md        # Curated doc
├── getting-started.md      # Curated doc
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
    <scraped_at>2025-10-15</scraped_at>
  </source>
  <!-- Multiple <source> entries, one per .md file -->
</docs_index>
```

---

## 📝 TODO - Regenerate "Descriptions" (2026-05-31)

Collections still have `PLACEHOLDER` descriptions — run `/improve-index-xml` (or `/rescrape-docs`) on each.

The framing has shifted from "semantic search" to **LLM routing**, so existing descriptions should also be regenerated to match the current rules in [.claude/references/source-descriptions.md](.claude/references/source-descriptions.md).

## 👉 Improve later - Remove Scripts? (2026-05-27)

Remove the scripts in [scripts/](scripts/) I don't need. For example, what about a bash for-loop over `curate_doc.py`, then allocate to subagents (run `wc --chars *.md | sort -n` or token counts). Read the diff on each local file and assess if the description needs refining (using `head`).

Pick a cap so no agent is overloaded, on two axes:
- Input size — a target like "~X total words per agent" so context stays comfortable.
- File count — a soft cap (e.g. ≤5 files) so no single agent does too much serial reading, which hurts both speed and summary quality.

The honest rule: isolation matters in proportion to file size and similarity. Give a large or highly-similar file its own agent (where contamination/dilution is real). Batch small, distinct files 3–5 together — the interference there is negligible, and you save the overhead. It's a quality-vs-efficiency trade-off, not a flat "always isolate".

> For this task I'd set the budget as "≤5 files AND ≤~12k words per agent, whichever binds first". I'd rather use the anthropic tokeniser script in `~/projects/python/TEMP-token-counts/`.

But if there's an API cost to running these, use a multiplier (approximated across curated files): tokens ≈ characters × 0.37 (I don't think my sampling was wonky across 49 files).
