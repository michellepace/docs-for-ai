---
title: Notes for following "sociable" / "Kent Beck" style + refactoring following TDD
updated: 2026-07-08
status: draft / rough
---

## Brief for Claude Code

When referenced here: assess (or refactor) the test module against this standard.

- **Sociable tests** (Beck/Fowler classicist style): drive the real entry point with real files in `tmp_path`; fake exactly one seam — the genuine external boundary (the network).

- **Situation-named**: each test names the situation the tool handles ("whitespace-only change", "fetch failed"), never an internal function; one behaviour per test. The names alone should read as the spec.

- **Delete TDD scaffolding**: tests written while shaping the design (one unit test per helper, named after code) are scaffolding. Once the design settles, refactor the suite like production code — delete whatever is covered at the sociable level, transferring coverage first.

- **Litmus — coupling, not age**: keep tests sensitive to behaviour changes, insensitive to structure changes. Breaks under a pure refactor → scaffolding. Asserts observable behaviour through the public seam → keeper, even if TDD-written and it is the only cover.

- **Shape**: flat functions, no classes; prefix-namespaced names; file order tells the narrative (guards → happy paths → lifecycle → live smoke).

Exemplars: `tests/test_sync_index.py`, `tests/test_curate_doc.py`.

## Collected Context

Comments and extracts caught in-flight so I can remember remember.

<claude_code_comment_1>
*I think it's better, and I'd push back on "no longer textbook": you've moved from one testing textbook to another. The old suite was the mockist style — one test per private-ish function, verifying mechanism. The new suite is the classicist style (Fowler's "sociable" tests): drive the real entry point (`main()` via `run_sync`), use real filesystem/XML/git in `tmp_path`, and fake only the genuine boundary — the network, at `curate_doc.curate`. That is exactly one seam, and it's the right one. This also matches your own CLAUDE.md rule better than the old suite did: test the behaviour a caller depends on, not how the code produces it.*
</claude_code_comment_1>

<claudecode_comment_2>
> After I got Claude Code to create a table of how sync_index.py worked, the different states and subsequent behaviours. I asked "but why is this so easy to understand, but when I read test_sync_index.py I can't really make sense of how things work?"

*...so the tests are named after the functions you were shaping, not the situations the tool handles. Five of your fifteen names lead with a helper's name — they mirror sync_index.py's internal structure. Your table names things by situation ("whitespace-only change", "fetch failed"). Function-shaped names and situation-shaped names can't line up, which is exactly the "noise" you're sensing.*

*This is normal, not a mistake — **but Beck and Fowler both treat those early tests as scaffolding:** once the design settles, you refactor the test suite like production code, and delete scaffolding whose behaviour is now covered at the sociable level. Fowler's line applies directly: tests should be sensitive to behaviour changes and insensitive to structure changes. Your helper-level tests are sensitive to structure.*
</claudecode_comment_2>

<commit>
> First commit I did in the spirit of "TDD scaffolding". Keeping the message just to remember, don't need to read the diff - `test_sync_index.py` has changed since then.

`d34be542c98669cae42c1a0b3911fa5581bf491b`

test: delete TDD scaffolding; one sociable test per sync state

The suite grew test-driven: one unit test per internal helper, named after the code rather than the situation it handles. Fowler/Beck treat those early tests as scaffolding — once the design settles, delete them wherever behaviour is covered at the sociable level, keeping tests sensitive to behaviour and insensitive to structure. Goal: the test names alone reconstruct the sync state table (unchanged / whitespace-only / changed / missing / orphan / fetch-failed), so an agent reads the suite as the spec.

- each state gets one deterministic test through main(); only curate is faked, faithfully — like the real one it resets the INDEX description to PLACEHOLDER, which is what finally made the restore path testable sociably
- four helper-unit tests deleted (coverage transferred); the module now imports only main and the report formatter
- conditional @firecrawl CLI test deleted — its if/else assert could never fail on a restore bug; the @github smoke test remains
- fetch-failure test now fails the FIRST doc, actually proving the sync carries on past a failure

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
</commit>

<my_other_references>
Bookmarked conversations delving into these approaches:

- https://claude.ai/chat/82e64973-802d-41c5-a521-da69f453b5c0
- https://claude.ai/chat/b6e5f0e7-3a97-47ad-b8e4-1b3e7e3eac30
</my_other_references>
