---
updated: 2026-08-02
---

# Vocabulary

The domain language of this project — one canonical term per concept, so names
stay coherent across modules, tests, and docs.

**Nothing below has been renamed yet.** The glossary is the *settled target*; the
[rename ledger](#rename-ledger) maps it to what the code says today. The
reasoning lives in `assessment.md`, beside this file.

One word meaning four things is the signal that a type or module boundary is in
the wrong place; four words for one thing want to collapse. So the words are
settled on paper first, then applied as **one** pass folded into the module
re-carve — not sprinkled through. The tax for getting that order wrong is
already visible in modules renamed twice (`add_doc` → `curate_doc`;
`direct_source` + `markdown_source` + `github_source` → `direct_fetch`).

---

## Glossary

### The collection

| Term | Means | Not to be confused with |
| :--- | :--- | :--- |
| **collection** | A directory of curated docs for one documentation site (`nextjs/`, `clerk/`, `uv/`) — the index, a README, and the doc files. | The index lives *inside* a collection. |
| **doc** | The curated file on disk. Never "document". | doc entry — the index *record* about a doc. |
| **curate** | Turning a source URL into a saved, indexed doc — the umbrella verb for the pipeline. | fetch / scrape — two *ways* curation acquires content. |
| **recurate** | Re-curate a whole collection and regenerate its descriptions (`/recurate-docs` = `sync-index` + descriptions). | curate — one doc at a time. |

### The index

| Term | Means | Not to be confused with |
| :--- | :--- | :--- |
| **index** | The `INDEX.xml` manifest — one entry per curated doc. Authoritative: it *routes* an LLM reader to the right doc. | doc entry — the index is the manifest, an entry one record inside it. |
| **doc entry** | The record about a doc: the `<doc_entry>` element, the `DocEntry` dataclass, "doc entry" in prose. One term, three casings; "entry" alone is fine once context is set. | element — reserved for XML mechanics (`desc_elem`, `file_elem`). |
| **description** | An entry's 20–30-word routing signal — why you'd open this doc. | title — the title names the doc, the description sells it. |
| **placeholder** | A description not yet written; the literal `PLACEHOLDER`. | An empty description — a placeholder is a deliberate marker. |

### Identity & URLs

| Term | Means | Not to be confused with |
| :--- | :--- | :--- |
| **requested url** | The URL the user gave on the command line. | Either twin spelling is accepted here. |
| **canonical url** | A doc's identity and dedupe key, stored as `<source_url>`: query- and fragment-free, no trailing slash, a markdown twin's `.md` dropped, and a GitHub *blob* URL rather than its raw twin. Two spellings collapse to one canonical url → one file → one entry. | fetch url — what we *record* vs what we *hit*. |
| **fetch url** | The URL actually retrieved: a GitHub raw address, `page.md`, or `_sources/page.rst.txt`. | canonical url — see above. |
| **twin** | A page's directly-fetchable raw counterpart — `page.md`, `_sources/*.rst.txt`, or a blob's `raw.githubusercontent.com` URL — same content, no scraping. Bidirectional: curate either spelling, both converge on one canonical url. | scrape — a twin *avoids* scraping. |

### Acquiring content

| Term | Means | Not to be confused with |
| :--- | :--- | :--- |
| **fetch** | Acquire a doc's content — the umbrella over both modes. | Qualify with a form below whenever the mode matters. |
| **direct-fetch** | Retrieve raw markdown or rst over HTTP. Free, clean. | scrape — direct-fetch is the text path. |
| **scrape** | Convert an HTML page to markdown via FireCrawl. The paid fallback when a page has no twin. | direct-fetch — scrape is the paid, HTML path. |

### Resolving a URL to a plan

| Term | Means | Not to be confused with |
| :--- | :--- | :--- |
| **resolve** | Compute the fetch plan for a URL, in precedence order: GitHub → twin rule → raw `.md`/`.rst.txt` suffix → scrape. | — |
| **fetch plan** | The decision record for one URL: doc format, fetch url, canonical url, output filename. | route — "routing" belongs to the *index*; nothing here travels a path. |
| **rule** | A `direct-fetch-rules.toml` mapping: rule name → the URL prefixes it covers. Names state the user's membership test — `markdown-twin` (site follows the page + `.md` convention), `readthedocs-twin` (site is hosted on Read the Docs). | prefix — a rule *has* prefixes; one rule covers many sites. Also `probe-twin.md`, which numbers its detection *rules* 1–5 — a live second sense. |
| **prefix** | A URL prefix under which a rule applies (boundary-safe, trailing `/`). | — |

### Format & files

| Term | Means | Not to be confused with |
| :--- | :--- | :--- |
| **doc format** | `markdown` or `rst` — selects the title extractor and output extension. Absent ⇒ scrape. Spelled **markdown** in identifiers and values; **md** only as a literal file extension. | extension — the format is the *concept*, the extension one *consequence*. |
| **local file** | A doc's filename within its collection; stored as `<local_file>`. | canonical url — the file is the *artefact*, the url its *origin*. |
| **title** | The doc's human name — from frontmatter, else the first heading, else the URL. | description — see above. |

### Sync (the recurate machinery)

| Term | Means | Not to be confused with |
| :--- | :--- | :--- |
| **sync** | Reconcile the index against files on disk, then re-curate every entry. | recurate — sync is `sync-index`; recurate adds the descriptions pass. |
| **orphan file** | An on-disk doc with no index entry. Deleted during sync (`README.md` and dotfiles are kept) — the only file sync deletes. | An entry whose file is missing — no mirror case: the index is authoritative, so the doc is *re-fetched*, never the entry pruned. |
| **stale content** | A doc file that has drifted from its source. Overwritten on re-curate, which resets its description to the placeholder. | orphan file — staleness is about a doc's *text*, not its existence. |

---

## Rename ledger

Verified against the code on 2026-08-02. Every row is still pending.

| Today | Settled | Where |
| :--- | :--- | :--- |
| `<source>` | `<doc_entry>` | 20 `INDEX.xml` files, the schema blocks in `README.md` + `.claude/CLAUDE.md`, `curate_doc`, `sync_index`, `update_descriptions`, `scripts/collection_status.py` |
| `IndexSource` + raw `ElementTree` field-picking in 4 files | one `DocEntry` dataclass owned by `index_io` | see *missing type*, `assessment.md` |
| `FetchRoute` / `resolve_route` | `FetchPlan` / `resolve_plan` | `direct_fetch` |
| `FetchedDoc.source_url` | `.canonical_url` (deletes the compensating comment in `curate`) | `curate_doc` |
| `curate(source_url=…)` | `curate(requested_url=…)` | `curate_doc` |
| `fetch_document` / `_write_fetched_document` | `fetch_doc` / `_write_fetched_doc` | `curate_doc` |
| `extract_md_title` | `extract_markdown_title` | `direct_fetch` (its test class already says `TestExtractMarkdownTitle`) |
| toml keys `append-md` / `readthedocs` | `markdown-twin` / `readthedocs-twin` | `direct-fetch-rules.toml`, and the `_append_md_route` / `_readthedocs_route` handlers |
| `TRANSFORMS` dict, "registry"/"transform" in docstrings and test ids | `RULES`, "rule" everywhere | `direct_fetch`, `test_direct_fetch` |
| "INDEX.xml is the source of truth" | "the index is authoritative" (`ask-docs.md` already says this) | `sync_index` epilog, `recurate-docs.md` |
| `direct_fetch.py` doing three jobs | split: plan resolution · direct fetching · title extraction | `direct_fetch` |

⚠️ **The `<source>` → `<doc_entry>` migration must be atomic** — the 20
`INDEX.xml` files and the code in one commit. `read_index_sources` hard-codes
`findall("source")`, so a `<doc_entry>` index parses fine but yields `[]` →
`delete_orphan_files(dir, set())` runs **before** any curation and unlinks every
doc file; `total = 0`, so nothing restores them. Don't run `sync-index` /
`/recurate-docs` mid-migration.

---

## Decisions

Settled 2026-07-04 unless noted. Reasoning in `assessment.md`.

1. **"route" belongs to the index.** *"Routing signal"* is the product's core
   user-facing metaphor. The internal type is a decision record, not a route —
   hence `FetchPlan`.

2. **"source" is retired as a term of art.** The record → `<doc_entry>`; the
   shadow type → a `DocEntry` dataclass; "source of truth" → *authoritative*;
   the origin address → `<source_url>` stays, the only surviving "source", in
   its plain dictionary sense. (`<doc>` was rejected: it re-creates the
   file/record ambiguity, and bare "doc" is ungreppable.)

3. **"fetch" stays the umbrella; qualify with "direct-fetch".** No new word —
   `fetch_url` and the fetch plan already span both paths. Curate → fetch →
   (direct-fetch | scrape).

4. **Rule names `markdown-twin` + `readthedocs-twin`.** A user-facing config key
   should state the membership test the user performs: a *convention* test ("does
   `page.md` load?") vs a *platform* test ("is it on readthedocs.io?"). A forced
   shared axis (`rst-twin`) would hide the platform dependency.

5. **"markdown" in identifiers and values; "md" only as a literal extension.**

6. **"rule", not "registry" or "transform"** — one word for the mechanism,
   matching the filename users edit.

7. **"Doc" is the file, "doc entry" the record.** Never "document". "Element"
   stays reserved for XML mechanics; *entry* is the domain word, and the natural
   collocation with strong LLM priors.

8. **Read the Docs stays a listed twin — *don't graduate it* (2026-08-02).**
   `black.readthedocs.io` and `pip.readthedocs.io` serve `.html` pages whose
   `_sources` twin 404s; unprefixed they scrape fine, but under a host-only rule
   `_readthedocs_route` would claim them and kill `curate-doc` on
   `Fetch failed: 404`. The `_sources` twin is a Sphinx artefact, not a platform
   guarantee — so the config stays a mapping and *rule* stays in the language.
   See `refactors.md`. What survives from that sketch is the sentence that runs
   the system: **a doc is direct-fetched whenever we know its twin; otherwise
   FireCrawl scrapes it.**
