---
updated: 2026-08-02
---

# Domain Language Assessment — `docs-for-ai`

**Assessed** 2026-07-03 · **re-verified against the code** 2026-08-02
**Scope:** `src/`, `tests/`, `scripts/`, `.claude/`, `README.md`, `direct-fetch-rules.toml`

This is the *reasoning*. The settled words and the pending rename ledger live in
`vocab.md`, beside this file. Symbols are named rather than line-numbered, so
this survives edits.

---

## TL;DR

The domain language is **healthier than it feels**. The core nouns — *collection,
doc, index, curate, scrape, twin* — are strong and consistent across five layers
(README → CLAUDE.md → commands → CLI help → code). The confusion is real but
concentrated in three places:

1. **"source" does four jobs** — and the overload hides a genuinely missing type.
2. **One URL travels under three names** in a single code path.
3. **The two rule names sit on different axes** (`append-md` says *how*,
   `readthedocs` says *where*).

Fix those three; the rest is polish.

---

## The shape of the thing

A **collection** holds an **index** of **doc entries**; each entry's
`<source_url>` is a doc's canonical url (its identity) and its `<local_file>`
names the doc file sitting beside the index. What happens to a URL:

```text
        /curate-doc <collection> <url>
                    │                      (/recurate-docs = sync + this, per doc)
     requested URL  ▼
   ╔═ CURATE — the whole pipeline, one doc ═══════════════════════════════╗
   ║                                                                      ║
   ║  RESOLVE ─ pick a fetch plan, in precedence order:                   ║
   ║    github blob → twin rule match → raw .md/.rst.txt → scrape         ║
   ║        │                                                             ║
   ║        ▼  PLAN: doc format · fetch url · canonical url · filename    ║
   ║                                                                      ║
   ║  FETCH ─ two modes:                                                  ║
   ║    direct-fetch (free, raw text — often via a TWIN)                  ║
   ║    scrape       (FireCrawl, HTML → markdown, paid, last resort)      ║
   ║        │                                                             ║
   ║        ▼                                                             ║
   ║  WRITE the doc file  +  INDEX an entry (description: PLACEHOLDER)    ║
   ║        │                                                             ║
   ║        ▼                                                             ║
   ║  DESCRIBE ─ Claude writes the 20–30-word routing description         ║
   ╚══════════════════════════════════════════════════════════════════════╝
```

---

## 1. "source" — one word, four jobs

| Sense | Where |
| :-- | :-- |
| The `<source>` index record | 20 `INDEX.xml` files, the schema blocks in `README.md` + `.claude/CLAUDE.md`, `curate_doc`, `sync_index`, `update_descriptions`, `scripts/collection_status.py` |
| The origin web address | `source_url` — CLI arg, XML tag, variables |
| A filename + url pair | `IndexSource` in `sync_index` |
| "INDEX.xml is the **source of truth**" | `sync_index`'s CLI epilog, `recurate-docs.md` |

Plus drive-bys: "Curation Source" meaning *the website* (the scaffolded README),
"fetch source" meaning *the plan* (`resolve_route`'s docstring), and "Source
routing" meaning *fetch precedence* (README).

**Settled: rename `<source>` → `<doc_entry>` and retire "source" as a term of
art.** `<source>` names the record after **one of its five fields**
(provenance) — but the record's customer is the LLM router, which reads
`<title>` + `<description>` to pick a `<local_file>`. The record is *about a
doc*; its name should say so.

Why `<doc_entry>` and not the shorter `<doc>`: tag, class, and prose become one
word in three standard casings (`<doc_entry>` / `DocEntry` / "doc entry"), the
file/record ambiguity is deleted rather than managed by a footnote, and
`grep -i doc_entry` hits nothing else — where bare "doc" has ~390 hits repo-wide.
It also fits the snake_case schema family (`source_url`, `local_file`,
`curated_at`).

> 🚨 **The rename must be atomic** — see the migration trap in `vocab.md`. Worth
> adding while there: a guard that aborts sync when the index parses but yields
> zero entries while doc files exist. That trap exists today for any hand-edited
> index.

## 2. "doc" vs "document" vs "entry"

The codebase has already voted — *doc* outnumbers *document* by roughly 20:1.
The stragglers are `fetch_document`, `_write_fetched_document`, "every document"
in `recurate-docs.md`, "[curated source document title]" in the CLAUDE.md and
README schema blocks, and `FetchedDoc`'s docstring — *"A fetched **source
document**"* — which piles three contested words into one phrase.

The three-word rule: **doc** is the file on disk, only ever the file; **doc
entry** is the index record ("entry" alone once context is set); **source** is
retired, surviving only inside `<source_url>`. *Entry* beats *element* because
"element" is already taken by XML mechanics here (`desc_elem`, `file_elem`) and
is serialization-true rather than domain-true.

## 3. "canonical" — the dedupe key, not decoration

*Canonical* = **the one official spelling, chosen among several meaning the same
page.** The pipeline meets one page under many spellings — `panel.html` vs
`_sources/panel.rst.txt`, `css` vs `css.md`, with or without
`?query`/`#fragment`/trailing `/` — and must collapse them to **one identity →
one file → one entry**.

Qualify only when two URLs are in scope. There are exactly three roles:

| Role | Meaning | Today's name |
| :-- | :-- | :-- |
| **requested url** | what the user typed | `source_url` arg in `curate()` 😕 |
| **canonical url** | the doc's identity — recorded as `<source_url>` | `route.canonical_url` ✅ |
| **fetch url** | what's actually hit on the wire | `route.fetch_url` ✅ |

The leak: one value travels as `source_url` (CLI) → `canonical_url`
(`FetchRoute`) → `source_url` again (`FetchedDoc`), forcing a compensating
comment in `curate()`: *"doc.source_url is canonical"*. **A comment doing a
name's job.** Rename `FetchedDoc.source_url` → `canonical_url` and `curate()`'s
parameter → `requested_url`; let `source_url` exist only at the moment the XML
tag is written.

## 4. "route" — two routings, keep the better one

Today the index *"routes an LLM reader to the right doc"* (README, CLAUDE.md,
`description-rules.md`, `ask-docs.md`) **and** `FetchRoute`/`resolve_route`
route a URL to a fetch method.

- **"Routing" belongs to the index.** It's user-facing and doing real work;
  rewriting it costs meaning.
- **The internal type isn't a route — it's a plan.** Nothing travels a path;
  `FetchRoute` is a decision record (format + fetch url + canonical url +
  filename). `FetchPlan` / `resolve_plan` is more accurate *and* a tiny, private
  diff.

## 5. `append-md` and `readthedocs` — different kinds of thing

- `append-md` describes a **cross-domain convention**: "page + `.md` is the twin"
  works on Clerk, Next.js, Vercel, Convex… The prefix list is an allowlist of
  sites *known to follow the convention*.
- `readthedocs` describes a **platform**: the `_sources/*.rst.txt` layout is
  reliable because Read the Docs hosting serves it. The test is "is this a
  `*.readthedocs.io` URL?", not "is this rst?"

A rule name in a **user-facing config** should answer the question the user asks
when deciding where to put their prefix. Forcing one axis (`rst-twin`) would
*hide* the platform dependency and invite prefixes that don't work. Hence
`markdown-twin` + `readthedocs-twin` — shared suffix for the shared concept,
differing stems for the differing applicability tests. (*Rejected 2026-08-02:*
graduating Read the Docs to hostname detection beside GitHub, and deleting
*rule/transform/registry* from the language — see `refactors.md` and decision 8
in `vocab.md`.)

While in the toml: **retire "transform".** The comment says *rule*, the filename
says *rules*, the loader says *rules*, docstrings say *registry*, and the
dispatch dict says `TRANSFORMS` — four words for one mechanism. **rule**
everywhere, including the `registry-*` test ids in `test_direct_fetch`.

**New since the first pass:** `probe-twin.md` numbers its twin-detection *rules*
1–5 — a second live sense of *rule*, unrelated to the toml mapping. Harmless
while the probe is a note; needs a distinct word if that logic ships.

---

## Where words surfaced design smells

**1. The "source" overload is a missing type.** No class represents an index
entry. Four files hand-pick fields out of raw `ElementTree` nodes —
`curate_doc` (three separate places), `sync_index` (two), `update_descriptions`,
`scripts/collection_status.py` — and `IndexSource` is a 2-of-5-field shadow of
the concept. One **`DocEntry`** dataclass (title, description, canonical_url,
local_file, curated_at) owned by `index_io`, with parse/write functions, collapses
the vocabulary *and* the duplication in one move. `for entry in read_index(path):`
reads like prose, with the type name carrying the file/record distinction exactly
where the destructive sync logic needs it. **The overloaded word was the symptom;
the missing abstraction is the disease.**

**2. `direct_fetch.py`'s name lies about its contents.** It resolves plans for
**all** paths *including the FireCrawl fallback* (`_firecrawl_route`), and hosts
all title extraction. Three responsibilities under a name describing one — and
not coincidentally, exactly where the "route" clash lives.

**3. "Source of truth"** stacks a fourth sense onto the most overloaded word in
the project, for a phrase `ask-docs.md` already replaces better ("authoritative").

---

## Rename volume

Word-family occurrences, `collections/` excluded; `source_url` excluded from the
*source* row since it survives. Re-counted 2026-08-02 with
`grep -roiE "\b<word>[a-z_]*"`.

| Word | code (`src` + `tests`) | prose (`.claude` + `README`) | Total |
| :-- | --: | --: | --: |
| source † | 128 | 31 | **159** |
| rule | 62 | 11 | **73** |
| twin | 47 | 1 | **48** |
| route ‡ | 32 | 5 | **37** |
| document † | 10 | 9 | **19** |
| registry † | 18 | 0 | **18** |
| transform † | 14 | 0 | **14** |
| plan | 0 | 0 | **0** |

† retiring · ‡ splitting (the index keeps *routing*; the type becomes *plan*)

- **`source` is the heavyweight, and overwhelmingly code** — mostly a
  code-and-tests sweep; only 9 user-facing README hits. **`plan` lands on virgin
  ground** — `FetchPlan` is uniquely greppable from its first commit. (`rule` is
  inflated by `probe-twin.md`: 37 of its 62 code hits are a note, not code.)
- **`twin` has one prose hit and none in `.claude/`** — the project's best
  metaphor is nearly absent from the layer every AI session reads first. A short
  glossary at the top of CLAUDE.md (doc, doc entry, canonical url, twin, rule)
  fixes this for free, and is still not done.
- **`recurate` has zero presence in `src/`** — confirms the intended layering:
  the user layer says *recurate*, the script layer says *sync*.

---

## Path

1. **Words on paper** ✅ *done* — every verdict is in `vocab.md`. No code touched.
2. **One deliberate rename pass, folded into the module re-carve** — a rename and
   a move are usually the same edit. The shortlist is the rename ledger in
   `vocab.md`; do the `<doc_entry>` migration atomically.
3. **Guard the language** — the 5-line glossary at the top of CLAUDE.md, so every
   future session inherits the settled words for free.

---

*The words chosen with care — collection, curate, twin, stale/orphan — are the
ones that never confuse. That's the whole lesson.*
