# uv Documentation

Curated docs for targeted AI context.

- Curation Index: [INDEX.xml](INDEX.xml)
- Curation Source: <https://raw.githubusercontent.com/astral-sh/uv/main/docs> — upstream source markdown, fetched directly (no API tokens)
- Exceptions: `reference-cli.md` and `reference-settings.md` are build-generated (no raw source); sourced from the token-free rendered route, e.g. <https://docs.astral.sh/uv/reference/cli/index.md>

What is uv? A fast, all-in-one Python package and project manager by Astral — it installs dependencies, creates virtual environments, and manages Python versions, replacing pip, virtualenv, pyenv, and pip-tools with one tool and a `pyproject.toml` + lockfile workflow.

---

## Migration notes (for encoding this as reusable tooling)

Once-off manual migration on `2026-05-19`: FireCrawl-scraped rendered HTML → direct raw GitHub source-markdown. Decisions to encode if automated:

- **Source routing**: fetch raw `raw.githubusercontent.com/astral-sh/uv/main/docs/<path>.md` — cleaner than rendered scrapes (real `!!!` admonitions, code-fence languages, no heading anchors, fresher, no tokens). On 404 (mkdocs build-generated docs absent from the repo), fall back to the rendered route `docs.astral.sh/uv/<path>/index.md`. Only `reference/cli` and `reference/settings` hit this; they keep anchor-linked headings and flattened admonitions (no cleaner upstream exists for generated docs). `reference-cli.md` ≈705 KB — allow a generous fetch timeout (30 s used).
- **Fetch mechanism**: a single throwaway PEP 723 script (Python stdlib `urllib.request` only — no third-party deps), run via `uv run` and deleted afterwards (not committed). HTTP GET with a `User-Agent` header and 30 s timeout; response decoded UTF-8 and written verbatim over the `git mv`-renamed file. No FireCrawl, no API tokens.
- **Content**: raw markdown had zero `--8<--` snippet includes (content complete); 3 files keep literal mkdocs content tabs (`=== "..."`). `uv/**` is markdownlint-excluded, so no normalising needed.
- **`<local_file>`**: URL path segments after `docs/` (raw) or `uv/` (rendered), joined with `-`, plus `.md` — e.g. `concepts/projects/dependencies.md` → `concepts-projects-dependencies.md`. Must match `^[a-z0-9-]+\.md$`; replaces the old `-uv` title-slug convention; no collisions.
- **`<title>`** precedence: (1) YAML frontmatter `title:` — the authored canonical title; (2) else first body ATX `# H1`, skipping leading frontmatter and fenced code, stripping a `[text](#anchor)` wrapper (`# [CLI Reference](#cli-reference)` → `CLI Reference`); (3) else explicit fallback (only `reference-settings.md` → `Settings`, having neither).
- **`INDEX.xml`**: preserve entry order; copy each `<description>` verbatim (human-curated — never regenerate or PLACEHOLDER); update `<title>`/`<source_url>`/`<local_file>`, set `<scraped_at>` to run date; keep exact format (no XML declaration, `<docs_index>` root, 2-space indent, element order title/description/source_url/local_file/scraped_at). Rename via `git mv` then overwrite body; abort the run on any fetch failure (no partial rewrite).
