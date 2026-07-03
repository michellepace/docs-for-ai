# Write Doc Descriptions for `INDEX.xml`

Each `<source>` entry in a collection's `INDEX.xml` indexes one curated doc. Write that entry's `<description>` — nothing else.

The description is a **routing signal** — a future Claude Code session reads all entries' `<title>` + `<description>` at once, picks the docs relevant to a user's question, and answers from those. Optimise for that, then apply the quality rules (`<quality_rules>`) and examples (`<reference_examples>`).

<quality_rules>
- Route by meaning, not term overlap: an LLM *reads* this to pick a file (there is no keyword index), so state relationships rather than a bag of nouns. Orient first — what the doc is / when to reach for it — then embed the top few discriminating terms. Avoid a table-of-contents of disconnected fragments; the `<good>` examples bind terms with relationships (`.venv` managed by `run`/`sync`; `uv.lock` versus `pylock.toml`), they don't just enumerate.
- No colon intros like 'Here's the X:' — give me X directly (see `<good>`)
- Length 20-30 words; every word earns its place — terse and direct. Don't glue terms like `sync`/`uv.lock` to fake one word
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

<bad_vs_good>

Same `claudecode` skills source — keyword-dump, then the fix:

```xml
<!-- ❌ bad -->
<title>Extend Claude with skills</title>
<description>`SKILL.md` frontmatter, `disable-model-invocation`/`user-invocable` invocation control, personal/project/plugin/enterprise precedence, `$ARGUMENTS` substitutions, `!command` dynamic injection, `context: fork` subagents, `allowed-tools`, `skillOverrides`, bundled skills, and `skill-creator` evals.</description>
```

- ❌ a table of contents — disconnected fragments with no relationships for the router to read
- ❌ no orientation — never says what the doc is or when to reach for it
- ❌ mixed granularity — `allowed-tools` (one field) sits as a peer of `frontmatter` (its parent)

```xml
<!-- ✅ good -->
<title>Extend Claude with skills</title>
<description>`SKILL.md` frontmatter for authoring skills, invocation control (`disable-model-invocation`/`user-invocable`), location precedence across personal/project/plugin, `$ARGUMENTS` and `!command` injection, `context: fork` subagents, and evaluation with `skill-creator`.</description>
```

</bad_vs_good>

</reference_examples>
