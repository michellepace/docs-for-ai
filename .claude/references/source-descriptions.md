# Write Index Source Description

This task: write the one `<description>` field for each source in a collection index.

You write only the `<description>` field — `<title>`, `<source_url>`, and `<local_file>` are filled programmatically. Complement the sibling `<title>`; don't repeat it.

Each description is a **routing signal for an LLM reader** — Claude reads `INDEX.xml` to pick which files answer a question, not a vector index matching keywords. Optimise for that, then follow the quality rules (`<quality_rules>`) and reference examples (`<reference_examples>`).

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

</good>

<bad_vs_good>

Same `vercel` source — anti-pattern, then the fix:

```xml
<!-- ❌ bad -->
<title>Build a fullstack app with Next.js 16 and Prisma Postgres</title>
<description>This tutorial shows you how to build a fullstack app: it walks through Next.js 16 and Prisma Postgres step by step, covering everything you need to know.</description>
```

- ❌ framing lead-in instead of specifics ("This tutorial shows...")
- ❌ repeats the title instead of complementing it (e.g. `Next.js 16`)
- ❌ vague filler in place of high-value terms (e.g. "everything you need")

```xml
<!-- ✅ good -->
<title>Build a fullstack app with Next.js 16 and Prisma Postgres</title>
<description>Tutorial with `App Router` pages, Prisma ORM schema and queries, Sign in with Vercel `OAuth` (PKCE, `jose` ID-token verification), `Server Actions` for drafts/publishing, and `vercel` CLI deployment.</description>
```

</bad_vs_good>

</reference_examples>
