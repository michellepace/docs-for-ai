# Refactor: generic GitHub-doc fetch path for `curate_doc.py`

**NOTE: Migrations of existing collections out of scope. As an example the `uv/` collection has already been manually migrated to raw GitHub URLs for `<source_url>` in `uv/INDEX.xml`.**

## Context

FireCrawl scrapes rendered HTML, costing API tokens and flattening admonitions, code-fence languages, and headings. Fetching the same docs as raw GitHub markdown is free, faster, and cleaner — proven on the uv collection, now worth generalizing.

This implements the authoritative spec in `uv/README.md` lines 13–22 ("Migration notes"). One intended difference: a generic basename title-fallback replaces uv's one-off explicit `Settings` fallback — no conflict, since uv's `reference/{cli,settings}` entries stay FireCrawl-routed (see Out of scope).

## `<local_file>` rule (generic)

Deterministic algorithm (no "first `/docs/`" heuristic — that mis-splits when the repo is named `docs` or the ref contains `docs`):

1. Strip the GitHub structural prefix: `raw.githubusercontent.com/<owner>/<repo>/<ref>/<rest>` or `github.com/<owner>/<repo>/blob/<ref>/<rest>` → `<rest>`.
2. If `<rest>` begins with a single leading `docs/`, drop that one segment.
3. Join the remaining path components with `-`, append `.md`.

Examples:

- `raw.githubusercontent.com/astral-sh/uv/main/docs/concepts/projects/dependencies.md` → `concepts-projects-dependencies.md`
- `github.com/evilmartians/lefthook/blob/master/docs/configuration/exclude.md` → `configuration-exclude.md`
- repo with no leading `docs/` (e.g. `…/<ref>/guide/intro.md`) → `guide-intro.md`

(No filename regex is enforced anywhere in code — `local_filename`'s output is written verbatim; this is purely the naming convention.)

## Design

New module `scripts/github_doc_fetcher.py` (four pure helpers plus one thin I/O function `fetch_github_doc` — network and stdout are its only side effects), shape-compatible with the FireCrawl return so `main()` downstream is untouched:

- `is_github_doc_url(url) -> bool` — host is `raw.githubusercontent.com`, **or** `github.com` with a `/blob/` segment; path ends `.md`. (`.mdx` deferred: would also require auditing `sync_index.py`'s markdown globbing so `.mdx` is change-detected — out of scope.)
- `to_raw_url(url) -> str` — rewrite **only** `github.com/<o>/<r>/blob/<ref>/<p>` → `raw.githubusercontent.com/<o>/<r>/<ref>/<p>`; any other URL — already-raw or the local test path — is returned unchanged. Non-canonical `github.com` forms (`?raw=`, `tree/`, `refs/heads/`) fail `is_github_doc_url` and fall to FireCrawl.
- `local_filename(url) -> str` — the `<local_file>` rule above.
- `extract_title(body, url) -> str` — (1) leading `---` frontmatter `title:`; else (2) first ATX `# H1` after the frontmatter block, stripping a `[text](#anchor)` wrapper defensively (raw headings are usually already clean); else (3) URL basename, `-`-split, title-cased.
- `fetch_github_doc(url) -> dict` — GET `to_raw_url(url)` via stdlib `urllib.request` (User-Agent header, 30 s timeout), decode UTF-8; on `HTTPError`/`URLError`, print to **stdout** in `curate_doc.py`'s exact 4-field convention then `sys.exit(1)`. Returns `{"markdown": body, "metadata": {"title": extract_title(body, url)}}` (error body matches `curate_doc.py:274/:330`):

  ```python
  def fetch_github_doc(url: str) -> dict:
      raw = to_raw_url(url)
      try:
          req = urllib.request.Request(raw, headers={"User-Agent": "docs-for-ai"})
          with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310
              body = resp.read().decode("utf-8")
      except urllib.error.HTTPError as e:
          print(f"❌ Error: NO_CONTENT|HTTP {e.code}|{url}|")
          sys.exit(1)
      except urllib.error.URLError as e:
          print(f"❌ Error: NETWORK|{e.reason}|{url}|")
          sys.exit(1)
      return {"markdown": body, "metadata": {"title": extract_title(body, url)}}
  ```

- **Imports.** `curate_doc.py` runs as a path script (only `scripts/` on `sys.path`, including when shelled by `sync_index.py`); tests use the package form (`from scripts.… import …`, `tests/test_sync_index.py:9`). Resolve both with `try: from scripts.github_doc_fetcher import … / except ImportError: from github_doc_fetcher import …`.
- **Quality bar.** `scripts/*` ruff per-file ignores are only S314/S603/DTZ011 (ruff = ALL, pyright = standard) → `github_doc_fetcher.py` needs full type annotations and docstrings; `# noqa: S310` only on the `urlopen` line.

### Backward-compatibility invariants (non-negotiable)

- Routing is per `<source_url>`, decided at scrape time. `sync_index.py` iterates each `<source>` and shells `curate_doc.py` per URL → a single `INDEX.xml` may freely mix GitHub-raw and FireCrawl sources; each is routed independently.
- When `is_github_doc_url(url)` is False the **exact current code path runs** — `_scrape_with_firecrawl`, slug + duplicate-suffix filenames, `_validate_url`, INDEX/README writing — byte-for-byte unchanged. Collections never migrated, and FireCrawl sources inside migrated collections, behave identically to today (incl. API-key requirement).
- The change is purely additive: two `if is_github_doc_url … else <unchanged>` branches. No existing function is modified; `_add_or_update_source_in_index`, `_cleanup_old_file`, `_validate_url`, and README/INDEX creation are reused as-is.

### Two injection points in `scripts/curate_doc.py`

1. **Scrape** — line 377. Replace `scraped_doc = _scrape_with_firecrawl(source_url, max_attempts=2)` with a one-line dispatcher `_scrape(source_url)` returning `fetch_github_doc(source_url)` if `is_github_doc_url(source_url)` else `_scrape_with_firecrawl(source_url, max_attempts=2)`.
2. **Filename** — lines 396–403. If `is_github_doc_url(source_url)`: `filename = local_filename(source_url)` (skips `_slugify_title` / `_get_duplicate_title_count` and the hard-coded `.md`). Else: existing slug+dup logic.

## TDD (house style, no mocks)

Strict RED→GREEN per `superpowers:test-driven-development`: for each function write the failing test first, then implement.

**Pure functions** — direct import + plain `assert`, mirroring `tests/test_sync_index.py`'s unit pattern; `from scripts.github_doc_fetcher import …`:

- `is_github_doc_url`: raw `.md` True; `github.com/<o>/<r>/blob/<ref>/x.md` True; `docs.astral.sh/...` False; `github.com/.../tree/...` False; non-`.md` False.
- `to_raw_url`: blob→raw for the lefthook example; already-raw and non-blob URLs pass through unchanged.
- `local_filename`: the uv and lefthook examples, plus a path with no leading `docs/`.
- `extract_title`: frontmatter wins; H1 when no frontmatter; basename when neither; H1 after a frontmatter block isn't shadowed; `[text](#anchor)` wrapper stripped.

**`fetch_github_doc` + dispatcher** — integration test mirroring `tests/test_curate_doc.py` exactly: `subprocess.run(["uv","run","scripts/curate_doc.py", <tmp-collection>, <url>])` inside `tempfile.TemporaryDirectory`, asserting exit code, combined stdout, and files written. No mocks, no fixtures, no `capsys`:

- 200 path: real public GitHub raw URL (lefthook `configuration/exclude.md`) — consistent with the existing suite already hitting `zustand.docs.pmnd.rs`. Assert exit 0, `configuration-exclude.md` written, INDEX entry added with `PLACEHOLDER`.
- `NO_CONTENT` path: a known-404 raw URL → assert `❌ Error: NO_CONTENT` in stdout, exit 1.
- `NETWORK` branch: one direct-import unit test calling `fetch_github_doc` with an unresolvable host, capturing stdout via `contextlib.redirect_stdout` (no mock/fixture/capsys). This single direct-call error test is the only deviation from the subprocess pattern — accepted because the closed-host path can't be triggered deterministically end-to-end.

## Explicitly out of scope / trimmed

- Migrations (git mv, INDEX.xml pre-edits, re-curation, description regeneration) — done by hand beforehand.
- No `/index.md` 404-fallback: a 404 fails clearly via `NO_CONTENT` for the human to resolve. uv's `…/reference/{cli,settings}/index.md` entries (host `docs.astral.sh`) stay FireCrawl-routed (API key required). Accepted.
- Duplicate-title suffixing for GitHub URLs (doc paths are already unique).
- `.claude/commands/*.md` and `sync_index.py` — unchanged; `/curate-doc` and `/rescrape-docs` pass URLs through and the dispatcher routes them (see invariants).

## Verification

1. `uv run pytest -v` — new + existing tests pass. New GitHub-path tests hit real public GitHub, consistent with the existing suite (which already makes external calls and needs a FireCrawl key for its FireCrawl tests); this change adds no offline guarantee and removes none. Confirm the new-module import resolves under both `uv run scripts/curate_doc.py …` and `uv run pytest`.
2. `uv run ruff check && uv run pyright` — clean (`# noqa: S310` on the `urlopen` call; host is gated by `is_github_doc_url`).
3. `uv run pre-commit run --all-files` — green; INDEX.xml stays well-formed (existing index writer unchanged).
4. Smoke (throwaway dir, no real collection mutated): seed a minimal collection in a temp dir, then `uv run scripts/curate_doc.py <tmp-collection> https://github.com/evilmartians/lefthook/blob/master/docs/configuration/exclude.md` → writes `configuration-exclude.md`, INDEX entry added with `PLACEHOLDER` description, no FireCrawl/API key needed. Discard the temp dir.
