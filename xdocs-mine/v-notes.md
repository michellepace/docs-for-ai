---
title: Vocabulary notes
updated: 2026-07-02
status: draft / rough
---

This is a genuinely good question to ask *before* moving code, and having read through `src/` I think your instinct is more correct than you're giving it credit for. Let me evaluate the plan, make one adjustment, and then show you the concrete evidence that the exercise is worth doing.

## Verdict: your sequence is right — with one adjustment

**words → principles → structure** is the correct order. The single adjustment I'd make: pull *renaming* out of step 1 and fold it into step 3.

Your step 1 says "establish vocab **and do a bit of renaming**". Separate those. Step 1 should touch **no code** — just settle the words on paper. Renaming is expensive and churny; it belongs in the same pass as the restructuring (step 3), because a rename and a move are usually *the same edit*, and doing them in two passes doubles the diff and the test churn.

## Why "words first" is the right instinct — and not just tidiness

Here's the deep reason, and it's exactly the thing you sensed when you wrote that vocab "would help re-carve the modules":

> **A module is a named concept. Module seams follow concept seams.**

When you write the vocabulary down and find that one word means four things, that overload *is* the signal that a module boundary or a type is in the wrong place. When you find four words for one thing, they want to collapse. So `vocab.md` isn't a preamble to the refactor — it **is** the refactor, done on paper first where it's cheap and reversible. That's why the order matters: you literally cannot carve modules well while the words are fuzzy, because the words are what you'd carve *along*.

## You've already paid for churn — which proves the point

Look at the stale bytecode and test files still lying around:

- `add_doc` → `curate_doc`
- `direct_source` + `markdown_source` + `github_source` + `github_raw_fetcher` → `direct_fetch`
- `firecrawl_source` → `firecrawl_scrape`
- `update_index_descriptions` → `update_descriptions`

You've renamed these modules *repeatedly*. That churn is the tax on renaming before the words are settled — which is exactly why your "fix vocab first" instinct is right, and exactly why renaming should be **one** deliberate pass at the end, not sprinkled through.

## What I found — proof the exercise is worth it

These are real collisions in the current code. They're also the seed rows for `vocab.md`:

**1. "route" is overloaded across two domains.** Your `CLAUDE.md` says *"INDEX.xml **routes** an LLM reader to the right doc"*. But `direct_fetch.py` has `FetchRoute` / `resolve_route` / `_github_route` — routing a *URL to a fetch method*. Two unrelated "routings". One of them should give up the word.

**2. "source" means at least four things.** `source_url` (a web address), `<source>` (an INDEX.xml entry), `CuratedSource` (a filename+url pair in `sync_index.py`), and *"source of truth"* (INDEX.xml itself). Four senses, one word.

**3. "fetch" is both broad and narrow.** `curate_doc.fetch_document()` does *fetch-or-scrape* (broad), while `direct_fetch.fetch_text()` is HTTP-only (narrow) — and the whole operation is "curate". So "fetch" straddles two levels.

**4. markdown / md / rst sit on inconsistent axes.** `DocFormat = Literal["markdown", "rst"]` (format names), extension `"md"`, and functions `extract_md_title` — then `TITLE_EXTRACTORS = {"markdown": extract_md_title}` maps the long name to the short-named function in one line. Format-name vs file-extension vs shorthand, never pinned down.

**5. The transform names use different axes.** `append-md` names the *operation* (append `.md`); `readthedocs` names the *platform*. One says *how*, the other says *where*. That's the unease you felt about `append-md` — it's not wrong, it's just not on the same axis as its sibling.

**6. A concept you use constantly but never named: "twin".** Comments all through `direct_fetch.py` and the `.toml` say "its raw twin", "its `.md` twin", "the `.rst.txt` twin" — a page and its directly-fetchable counterpart. It's doing real conceptual work but appears in no signature. That's a candidate to *promote* to a first-class word.

And one thing you got **right**, as a reference for what "settled" looks like: `canonical_url`. It's defined once (query/fragment-free identity), named consistently everywhere, and it's the reason two URL spellings collapse to one file. That's the target quality for every row in the glossary.

## The refined path

1. **Vocab pass (words only, no code).** Build `vocab.md`. For each concept: the *one* canonical term, a one-line definition, and a "not to be confused with" note. This is where we resolve route/source/fetch and decide whether "twin" becomes real.
2. **Principles, taught against your actual modules.** I won't lecture in the abstract — I'll use `vocab.md` to point at where your seams *should* move (e.g. does title-extraction belong with routing, or is it its own concept?).
3. **One restructuring pass.** Rename + move together, tests following.

## What `vocab.md` should look like

Short, code-reference-free, one row per concept — exactly as you said:

| Term | Means | Not |
| :--- | :---- | :-- |
| collection | a directory of curated docs for one site | not the INDEX |
| twin | a page's directly-fetchable raw counterpart (`.md`, `.rst.txt`) | not a scrape |
| canonical url | a doc's query/fragment-free identity, recorded as `<source_url>` | not the fetch URL |
| … | … | … |

---

The fastest way to converge is usually for me to draft a first cut of `vocab.md` from what I found above — it's far easier for you to *react to and correct* words than to invent them from a blank file. Want me to draft that first cut for you to mark up? Or would you rather talk through the three worst collisions (route, source, fetch) one at a time first and let the file grow out of that?
