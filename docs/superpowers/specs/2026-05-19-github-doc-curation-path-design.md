# Design: reusable GitHub-doc curation path

**Date:** 2026-05-19
**Status:** Approved (ready for implementation planning)

## Problem

Doc collections are curated via FireCrawl, which scrapes *rendered HTML*. That
costs API tokens, requires an API key, and degrades quality — it flattens
admonitions, drops code-fence languages, and bakes anchor links into headings.
For docs whose source lives in a public GitHub repo, the same content is
available as raw markdown: free, faster, and cleaner.

This was proven by a once-off manual migration of the entire `uv/` collection to
raw GitHub source URLs (committed; learnings in `uv/README.md` "Migration
notes"). The goal is to make GitHub-sourced curation a first-class, repeatable
capability of the tooling.

## Constraints

- Additive only. Existing FireCrawl behaviour for non-GitHub sources stays
  unchanged, including the API-key requirement.
- A single collection may mix GitHub-raw and FireCrawl sources; both must
  coexist and be re-scrapable together.
- Migrating existing collections is out of scope (done by hand beforehand).
- House style: `uv`, Python ≥3.14, ruff/pyright clean, TDD, British spelling,
  existing test conventions.
- `.md` sources only for now; other extensions deferred.

## Settled inputs (decided upstream — not re-litigated here)

- **URL detection:** GitHub-sourced if host is `raw.githubusercontent.com`, or
  `github.com` with a `/blob/` path segment.
- **Filename rule:** strip the GitHub structural prefix to the path remainder,
  drop a single leading `docs/` segment, join remaining segments with `-`,
  append `.md`.
- **Title precedence:** (1) frontmatter `title:`; else (2) first `# H1` after
  the frontmatter block, stripping a `[text](#anchor)` wrapper; else (3) URL
  basename, split on `-`, title-cased.
- **Reporting:** existing `❌` (failure) / `✅` (success) console convention. A
  404 or unexpected layout is a clear `❌` failure for the human to resolve —
  no silent fallback.

## Decisions taken during brainstorming

| Fork | Decision |
|------|----------|
| Code structure | New dedicated module `scripts/github_source.py`; `curate_doc.py` gains a thin routing branch that delegates. |
| `<source_url>` storage | Normalise `github.com/.../blob/...` → `raw.githubusercontent.com/...` before writing INDEX.xml. Idempotent on re-scrape; matches already-committed `uv/` entries. |
| Testing | Fast no-network unit tests for the pure helpers + real-network subprocess integration tests for fetch/routing. No mocks anywhere (helpers are pure, so none are needed). |
| Fetch mechanism | Python stdlib `urllib.request`. Zero new dependencies. |

## Architecture & routing

`curate_doc.py` `main()` gains a single routing branch immediately after URL
validation, **before** any FireCrawl call:

```text
if github_source.is_github_url(source_url):
    raw_url  = github_source.to_raw_url(source_url)   # blob → raw; raw passthrough
    content  = github_source.fetch_raw(raw_url)       # ❌ + exit on 404/network
    title    = github_source.extract_title(content, raw_url)
    filename = github_source.derive_filename(raw_url) # ❌ + exit if pattern invalid
    source_url = raw_url                               # stored normalised in INDEX
else:
    ...existing FireCrawl path, completely unchanged...
```

Everything after the branch is **shared and unchanged**: README/INDEX creation,
file write, `_add_or_update_source_in_index` (matches by `source_url`),
old-file cleanup, success message. The GitHub path deliberately skips
`_slugify_title` and the duplicate-title suffix logic — GitHub filenames are
path-deterministic.

`sync_index.py` needs **zero changes**: it re-invokes `curate_doc.py` per
stored URL via subprocess, so a raw URL in INDEX.xml re-routes through the
GitHub path automatically on re-scrape. Mixed collections work for free.

### Command surface

- `curate-doc.md` — behaviourally unchanged; one clarifying sentence added to
  its Context so the human knows GitHub URLs are fetched as raw source. No
  `allowed-tools` change (stdlib fetch is in-process; no new Bash perms).
- `rescrape-docs.md` — unaffected (`sync_index.py` unchanged; delegates per URL).
- `improve-index-xml.md` — unaffected (operates on local files only).
- `ask-docs.md` — unaffected (read-only consumer).

## Module: `scripts/github_source.py`

Pure functions plus one I/O function:

- `is_github_url(url)` → `True` if host is `raw.githubusercontent.com`, **or**
  host is `github.com` with a `/blob/` path segment. A `github.com` URL
  *without* `/blob/` (repo root, `/tree/`) returns `False` and falls through to
  the FireCrawl path, exactly per the settled rule.
- `to_raw_url(url)` → `github.com/{owner}/{repo}/blob/{ref}/{path}` becomes
  `raw.githubusercontent.com/{owner}/{repo}/{ref}/{path}`; a raw URL passes
  through (trailing slash stripped).
- `derive_filename(raw_url)` → take the path after
  `/{owner}/{repo}/{ref}/`, strip a trailing `.md`, split on `/`, drop one
  leading `docs` segment, join with `-`, lowercase, append `.md`. Result must
  match `^[a-z0-9-]+\.md$` or it is a `❌` failure (no silent guess).
- `extract_title(content, raw_url)` → (1) frontmatter `title:` via a simple
  regex over the leading `---` block, surrounding quotes stripped (no YAML
  dependency); else (2) the first ATX `# H1` after the frontmatter block,
  skipping fenced code blocks, unwrapping a `[text](#anchor)` link to `text`;
  else (3) the URL basename minus `.md`, split on `-`, title-cased.
- `fetch_raw(raw_url)` → stdlib `urllib.request` GET with a `User-Agent`
  header and 30 s timeout, UTF-8 decoded, returned as text. Raises on
  404/HTTP/network failure — **no fallback**.

Exact return shape (single orchestrating call vs. individual helpers wired in
`curate_doc.main`) is left to the implementation plan; the routing pseudocode
above is the contract.

## Progress reporting (success path)

Console output is consumed by Claude Code when a slash command runs the script,
so the GitHub path emits the same short `✅` progress lines as the FireCrawl
path, letting the agent follow progress and confirm completion. It reuses the
shared tail messages (`✅ Starting to curate from`, README/INDEX creation, file
write, `✅ Added/Updated index source`, `🎉 Curation Success!`) and adds two
GitHub-specific lines mirroring FireCrawl's `✅ Scraped content|(...)|`:

- `✅ Detected GitHub source|{raw_url}|` — after URL detection/normalisation,
  showing the normalised raw URL actually fetched.
- `✅ Fetched raw markdown|({N,NNN} characters)|` — after a successful fetch,
  parallel to the FireCrawl path's character-count confirmation.

Same `|`-delimited format as existing messages; no new emoji conventions.

## Error handling

Extends the existing `❌ Error: TYPE|detail|url|` console convention. All
failures occur **before** any file or INDEX mutation (matches existing
fail-fast ordering); no partial writes.

- `GITHUB_NOT_FOUND` — HTTP 404 (raw path absent, e.g. a build-generated doc
  not present in the repo source).
- `GITHUB_FETCH` — other HTTP, network, timeout, or decode failure.
- `GITHUB_FILENAME` — derived name fails `^[a-z0-9-]+\.md$` (e.g. a
  multi-segment git ref such as `release/1.x`).
- `UNSUPPORTED_GITHUB` — a `/blob/` URL not ending in `.md` (`.md`-only scope;
  fails before any fetch).
- `FILENAME_COLLISION` — the derived filename is already mapped to a
  *different* `source_url` in INDEX.xml (cross-repo collision within one
  collection); refuse to silently overwrite.

## Testing (TDD, no mocks)

- **`tests/test_github_source.py`** (new; fast; no network) — table-driven
  pure-function tests:
  - detection: raw host; `github.com` + `/blob/`; `github.com` without
    `/blob/` (repo root, `/tree/`); non-GitHub host.
  - `to_raw_url`: blob → raw; raw passthrough; trailing slash; ref preserved.
  - `derive_filename`: leading `docs/` stripped; nested paths; `.md` not
    doubled; lowercased; pattern-violating path raises.
  - `extract_title`: frontmatter title quoted and unquoted; H1 after
    frontmatter; H1 with `[text](#anchor)` wrapper; fenced code containing
    `#` ignored; frontmatter present but no `title:` key falls through to H1;
    basename fallback title-cased.
- **`tests/test_curate_doc.py`** (extend; real network; subprocess; no mocks):
  - a stable real `raw.githubusercontent.com` `.md` URL curates into a temp
    collection — exit 0, real content, deterministic `local_file`, correct
    title, raw `source_url` in INDEX, and the `✅ Detected GitHub source` /
    `✅ Fetched raw markdown` / `🎉 Curation Success!` progress lines present
    in output (same assertion style as existing message-string tests).
  - a `github.com/.../blob/...` URL is stored normalised to raw in INDEX.
  - a real non-existent raw URL fails cleanly (`GITHUB_NOT_FOUND` /
    `GITHUB_FETCH`) with no file written and no INDEX entry added.
  - a non-`.md` `/blob/` URL is rejected as `UNSUPPORTED_GITHUB`.
- **`tests/test_sync_index.py`** (extend; optional; real network) — one
  mixed-collection round-trip: an INDEX with a GitHub raw entry survives a
  `sync_index.py` re-scrape with its description preserved on unchanged content.

TDD order: write `test_github_source.py` (red) → implement
`scripts/github_source.py` (green) → add routing in `curate_doc.py` with
integration tests (red → green) → refactor. Follow the superpowers TDD skill
during implementation.

## Known accepted limitations (documented, not coded around)

- **Multi-segment git refs** (e.g. `release/1.x`) are unsupported: the raw URL
  becomes structurally ambiguous and the derived filename fails its pattern,
  surfacing as a loud `GITHUB_FILENAME` failure for the human. No silent
  guessing.
- A **brand-new collection created from a GitHub URL** gets
  `https://raw.githubusercontent.com` as the README "Curation Source" line.
  README is hand-curated anyway (the committed `uv/README.md` proves humans
  edit it); special-casing is YAGNI.

## Out of scope

- Migrating existing FireCrawl collections to GitHub sources (done by hand).
- Non-`.md` source extensions.
- Any change to FireCrawl behaviour or its API-key requirement.
- Rendered-route fallback for build-generated docs absent from the repo
  (the once-off migration used the rendered `.md` route for `reference-cli`
  and `reference-settings`; those URLs are non-GitHub and route through
  FireCrawl as normal — no automatic fallback is implemented).
