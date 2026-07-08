---
title: Vocabulary
updated: 2026-07-02
status: draft / rough
---

The domain language of this project — the *words*, not the code. One canonical
term per concept, so names stay coherent across modules, tests, and docs.

**Status: draft for review.** Rows marked ⚠ are collisions that need a decision
(see [Open decisions](#open-decisions)). Everything else is proposed as settled.

---

## The collection

| Term | Means | Not to be confused with |
| :--- | :--- | :--- |
| **collection** | A directory of curated docs for one documentation site (`nextjs/`, `clerk/`, `uv/`). Holds the index, a README, and the doc files. | The index — the index is *inside* a collection. |
| **curate** | The whole act of turning a source URL into a saved, indexed doc. The umbrella verb for the pipeline. | fetch / scrape — those are two *ways* curation acquires content. |
| **recurate** | Re-curate every doc in a collection and regenerate its descriptions. | curate — recurate is the batch, whole-collection form. |

## The index

| Term | Means | Not to be confused with |
| :--- | :--- | :--- |
| **index** | The `INDEX.xml` manifest in a collection — one entry per curated doc. What an LLM reader consults to find the right doc. | ⚠ *"source of truth"* — currently used for the index; see Open decisions. |
| **source** ⚠ | One `<source>` entry in the index (title, description, canonical url, local file, curated date). | ⚠ Badly overloaded today; see Open decisions. |
| **description** | The short LLM-routing text for a source. Written to guide a reader to the right doc. | title — the title is the doc's name; the description is *why you'd open it*. |
| **placeholder** | A description not yet written (a freshly curated doc). | An empty description — a placeholder is a deliberate marker. |

## Identity & URLs

| Term | Means | Not to be confused with |
| :--- | :--- | :--- |
| **canonical url** | A doc's stable identity: query- and fragment-free, with view suffixes normalised. Stored as `<source_url>`. Two spellings of the same page collapse to one canonical url → one file. | fetch url — see below. |
| **fetch url** | The URL actually retrieved, which may differ from the canonical url (a GitHub *raw* address, or a page with `.md` appended). | canonical url — what we *record*; the fetch url is what we *hit*. |
| **twin** | A page's directly-fetchable raw counterpart (`.md`, or a `.rst.txt`) that yields the same content without scraping. | scrape — a twin *avoids* scraping. (New term — promote from comments.) |

## Acquiring content

| Term | Means | Not to be confused with |
| :--- | :--- | :--- |
| **fetch** ⚠ | Retrieve a doc directly over HTTP (a raw markdown or rst file / a twin). | ⚠ Also used loosely for "fetch-or-scrape"; see Open decisions. |
| **scrape** | Convert an HTML page to markdown via FireCrawl. The fallback when a page has no twin. | fetch — scrape is the paid, HTML path; fetch is the direct, text path. |

## Routing a URL to a plan

| Term | Means | Not to be confused with |
| :--- | :--- | :--- |
| **route** ⚠ | The resolved plan for one URL: its format, the fetch url, the canonical url, and the output filename. | ⚠ Clashes with "the index *routes* a reader"; see Open decisions. |
| **resolve** | Compute the route for a URL, in precedence order (GitHub → transform → raw → scrape). | — |
| **transform** ⚠ | A rule that maps a page URL to its twin's fetch url (e.g. append `.md`; find the readthedocs `.rst.txt`). | ⚠ The two transform names sit on different axes; see Open decisions. |
| **prefix** | A URL-prefix under which a transform applies (boundary-safe, trailing `/`). | — |
| **registry / rules** ⚠ | The table of *transform → URL prefixes* (the `.toml`). | ⚠ Two words for one thing; pick one. |

## Format & files

| Term | Means | Not to be confused with |
| :--- | :--- | :--- |
| **doc format** ⚠ | `markdown` or `rst` — selects the title extractor and output extension. Absent ⇒ scrape. | ⚠ Spelled `markdown` in some names, `md` in others; see Open decisions. |
| **extension** | The output file's suffix (`md`, `rst`). | doc format — the format is the *concept*; the extension is one *consequence* of it. |
| **local file** | A curated doc's filename within its collection; stored as `<local_file>`. | canonical url — the file is the *artefact*; the canonical url is its *origin*. |
| **title** | The doc's human name — from frontmatter, first heading, or the URL as fallback. | description — the title names it; the description sells it. |

## Sync (the recurate machinery)

| Term | Means | Not to be confused with |
| :--- | :--- | :--- |
| **sync** | Reconcile the index against files on disk before re-curating all of them. | recurate — sync is the *reconcile* step; recurate is the whole batch. |
| **stale source** | An index entry whose file is missing, blank, or malformed. Pruned during sync. | orphan file — the mirror problem (below). |
| **orphan file** | An on-disk doc with no matching index entry. Deleted during sync. | stale source — an entry with no file. |

---

## Open decisions

Six clashes to resolve. My recommendation on each — react and overrule freely.

1. **"route" — pick one meaning.** Today the index *"routes a reader to the right
   doc"* (user-facing prose) *and* a fetch plan is a `route` (internal type). They're
   far apart in the code, so the cheap fix is to change the prose: say the index
   *"points a reader to"* / *"helps a reader find"* the right doc, and keep **route**
   for the fetch plan. → *Recommend: free up "route" for the fetch plan.*

2. **"source" — split the four senses.** It currently means: the `<source>` index
   entry, the origin web address (`source_url`), a filename+url pair, and *"source of
   truth"*. Keep **source** for the index entry only. Reserve the origin address as
   **canonical url**. Rename the pair to something like **indexed doc**. Drop *"source
   of truth"* — just say **the index**. → *Recommend: "source" = the index entry, nothing else.*

3. **"fetch" — narrow it.** Reserve **fetch** for direct HTTP retrieval. The broad
   "fetch-or-scrape" step needs its own word — **acquire** (or **retrieve**). Then
   *curate → acquire → (fetch | scrape)* reads as three clean levels. → *Recommend: "acquire" for the broad step.*

4. **transform names — one axis.** `append-md` names the *operation*; `readthedocs`
   names the *platform*. Name both by operation (what they do to the URL), so a reader
   predicts behaviour from the name. → *Recommend: rename by mechanism (exact names TBD together).*

5. **`markdown` vs `md` — one spelling in names.** Use **markdown** in identifiers and
   values; let **md** appear only as the literal file extension. → *Recommend: "markdown" everywhere but the extension.*

6. **registry vs rules — one word.** Pick **rules** (plain) or **registry** (implies a
   lookup table). → *Recommend: "rules".*
