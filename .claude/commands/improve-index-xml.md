---
argument-hint: <collection>
description: Improve INDEX.xml descriptions for Claude Code semantic search
allowed-tools: Read, Glob, Grep, Bash(find:*), Bash(test:*), Bash(wc:*), Bash(cat:*), Bash(echo:*), Task, Write, Bash(uv run:scripts/update_index_descriptions.py:*)
---

# Improve INDEX.xml Descriptions

Batch-improve semantic descriptions in $1 collection for optimised Claude Code retrieval using parallel subagents.

## 1. Validate Collection

**Existing collections:** !`find . -maxdepth 1 -type d -exec test -f {}/INDEX.xml \; -printf '%P\n'`

Validate $1 is an existing collection with INDEX.xml:

<validation_examples>

<validation_failure>

- Missing argument:

  ```
  ## 🤔 Which collection?
  - Usage: `/improve-index-xml <collection>`
  - Existing collections: `shiny`, `convex`, `tailwind`
  - Example: `/improve-index-xml convex`
  ```

- Collection not found:

  ```
  ## 🤔 Collection "$1" not found
  - No INDEX.xml at `$1/INDEX.xml`
  - Existing collections: [list]
  - Did you mean: [closest match]?
  ```

</validation_failure>

<validation_success>

```
## 📋 Ready to improve `$1` descriptions
Found [N] documents in INDEX.xml
```

</validation_success>

</validation_examples>

## 2. Analyse and Group Documents

Read `$1/INDEX.xml` and extract all `<source>` entries into a list.

**Agent count:** ceil(docs / 5) - max 5 docs per agent

**Grouping strategy:**

1. Identify topic clusters by URL path segments or title prefixes
2. Distribute documents across agents in balanced groups

Output allocation summary:

```
Grouping [N] documents across [M] agents:
- Agent 1: [files]
- Agent 2: [files]
...
```

## 3. Launch Parallel Subagents

Launch subagents **in parallel** (single message with multiple Task tool calls). Use this prompt template for each agent:

<subagent_prompt>

You are improving INDEX.xml descriptions for Claude Code semantic search in the `[COLLECTION]` collection. This is to make Claude Code more effective in finding relevant documentation.

## Your Assigned Documents

[List of local_file values for this agent]

## Description Quality Criteria (20-30 words)

Descriptions must be optimised for **Claude Code semantic search**, not human readability:

1. **High-signal keyword density** - Include specific API names, function names, patterns, and technical terms Claude will search for
2. **Conceptual enumeration** - List the main topics/concepts covered, not just paraphrase the title
3. **Backticks for code** - ALWAYS use backticks for code elements: `biome.json`, `useQuery()`, `--write` flag, etc.

**Preserve high-value terms:** Retain "best practices", "anti-patterns", "patterns", "gotchas" when the document covers these topics.

**Avoid:** Do NOT include "Does not cover..." or similar exclusions — these create false positive matches in semantic search.

## Reference Examples

```xml
<!-- Good: 24 words, backticks for code, high keyword density -->
<description>Convex database fundamentals: tables, JSON-like documents, optional schemas with `defineSchema`/`defineTable`, document IDs, `v` validators. Entry point for reading/writing data.</description>

<!-- Good: 30 words, enumerates concepts with backticks -->
<description>Folder and file conventions including top-level folders, routing files (`layout`, `page`, `loading`, `error`, `route`), dynamic routes, route groups, private folders, parallel and intercepted routes, metadata conventions, colocation patterns.</description>

<!-- Good: 23 words, technical terms with backticks -->
<description>`uv add`/`uv remove` commands, dependency sources (Git, URL, path, workspace), optional dependencies, development groups, build dependencies, editable installations, dependency specifiers syntax.</description>
```

## Your Task

For each assigned document:

1. Analyse the markdown file at `[COLLECTION]/<local_file>`
2. Write a description (20-30 words) following the 3 criteria above
3. Compare to current description in INDEX.xml, ensure yours is better
4. Verify word count is 20-30 words with `echo "description" | wc -w`

## Output Format

Write to `[COLLECTION]/descriptions_agent[N].txt`:

```text
<local_file1>.md
New description text here

<local_file2>.md
New description text here
```

Then explain why new description is more effective than old description in your response:

```
## Justifications

`<local_file1>.md`
- OLD: [old description here]
- NEW: *[new description here]*
- WHY: [10-16 word terse statement of why NEW is more effective]
```

</subagent_prompt>

## 4. Collect Results and Present

After all agents complete:

1. Combine output files:

   ```bash
   cat $1/descriptions_agent*.txt > $1/descriptions_improved.txt
   ```

2. Present summary to user:

```markdown
## 📊 New Descriptions for `$1`

<details>

_______________________
`<local_file1>.md`

OLD: [old description from agent output]

NEW: *[new description from agent output]*

[✅/❌] WHY: [Agent REASON from above. Prefix with ✅/❌ if you agree/disagree]

_______________________
`<local_file2>.md`

OLD: [old description from agent output]

NEW: *[new description from agent output]*

[✅/❌] WHY: [Agent REASON from output. Prefix with ✅/❌ if you agree/disagree]

_______________________

</details>

_______________________________________

**Total:** [N] descriptions ready to update

Type "yes" to apply, or "no" to cancel.
```

## 5. Apply Updates (on confirmation)

On user confirmation ("yes"), run:

```bash
uv run scripts/update_index_descriptions.py "$1" "$1/descriptions_improved.txt"
```

Clean up any remaining agent files:

```bash
rm -f $1/descriptions_agent*.txt 2>/dev/null || true
```

## 6. Report Success

```markdown
## 🎉 Description Improvement Complete

Collection: `$1`
- Descriptions updated: [N]
- INDEX.xml: `$1/INDEX.xml`
```

If user cancels, clean up temporary files and confirm cancellation.
