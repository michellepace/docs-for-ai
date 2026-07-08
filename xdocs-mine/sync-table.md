---
title: How index syncing works
updated: 2026-07-01
status: draft / rough
---


| State | How it arises | Claude's job |
| --- | --- | --- |
| ~~Stale source pruned~~ | ~~`INDEX` entry whose `local_file` is missing → dropped from `INDEX`~~| ~~none (FYI)~~ — removed: sync never drops an `INDEX` entry any more |
| Unchanged content | re-fetch identical; `restore_unchanged_descriptions` puts the old description back (only if the backup description was real, not `PLACEHOLDER`) | none (FYI) |
| Whitespace-only change| `git diff -w` treats it as unchanged → description restored | none (FYI) |
| Orphan deleted | file on disk, not in `INDEX` → `delete_orphan_files` deletes it | none (FYI) |
| Content changed | re-fetch differs → left at `PLACEHOLDER`; flagged by scanning `INDEX.xml` for placeholders (`files_needing_description`), not git | **write a description** ← the work |
| Missing file re-fetched | `INDEX` entry whose `local_file` is missing → recreated from `source_url`, then resolves as one of the rows above | none directly — usually ends in "content changed" (`PLACEHOLDER` → write a description) |
| Fetch failed | `curate` raises → entry kept intact, URL listed under `### Failed URLs` | none — retries next run; removing a dead entry is a deliberate edit to `INDEX.xml`, never sync's doing |
