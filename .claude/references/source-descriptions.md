# Write Index Source Description

This task: write the one `<description>` field for each source in a collection index.

You write only the `<description>` field — `<title>`, `<source_url>`, and `<local_file>` are filled programmatically. Complement the sibling `<title>`; don't repeat it.

Each description is a **routing signal for an LLM reader** — Claude reads `INDEX.xml` to pick which files answer a question, not a vector index matching keywords. Optimise for that, then follow the quality rules and reference examples.

<quality_rules>
- Length 20-30 words; every word earns its place — terse and direct
- No colon intros like 'Here's the X:' — give me X directly (see `<good>`)
- Apply DRY:
  - complement the title; surface high-value terms it lacks (e.g. "anti-patterns", "best-practices")
  - assume every sibling shares the collection's topic — don't spend words on it
- Use backticks for code elements e.g. `config.json`

</quality_rules>

<reference_examples>

Match the style of these good examples and avoid the bad:

<good>

```xml
<!-- uv Collection -->
<title>Project structure and files</title>
<description>`pyproject.toml` metadata, the gitignored `.venv` managed by `run` and `sync`, and the committed cross-platform `uv.lock` versus the standardised, tool-agnostic `pylock.toml` export target.</description>
```

```xml
<!-- tailwind Collection -->
<title>Responsive design - Core concepts - Tailwind CSS</title>
<description>Mobile-first breakpoint prefixes (`sm`–`2xl`), `max-*` range variants, custom `--breakpoint-*` themes, arbitrary values, and `@container` queries for styling utilities based on viewport or parent size.</description>
```

```xml
<!-- vercel Collection -->
<title>Build a fullstack app with Next.js 16 and Prisma Postgres</title>
<description>Tutorial with `App Router` pages, Prisma ORM schema and queries, Sign in with Vercel `OAuth` (PKCE, `jose` ID-token verification), `Server Actions` for drafts/publishing, and `vercel` CLI deployment.</description>
```

```xml
<!-- uv Collection -->
<title>Features</title>
<description>`python` version management, `run` for scripts, the `add`, `sync`, and `lock` project commands, `tool` execution via `uvx`, the legacy `pip` interface, and `cache` and `self update` maintenance.</description>
```

</good>

<bad>

```xml
<title>Features</title>
<description>Tour of uv's command surface grouped by purpose: `uv python` version management, `uv run` scripts, `uv add`/`sync`/`lock` projects, `uvx` tools, the legacy `uv pip` interface, and `uv cache`/`self` utilities.</description>
```

- ❌ opens with a framing lead-in ("Tour of...:") instead of the specifics
- ❌ spends words on the collection topic (`uv`)
- ❌ glues words together "`uv add`/`sync`/`lock`"

</bad>

</reference_examples>
