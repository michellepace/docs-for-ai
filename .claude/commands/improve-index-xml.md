---
description: Improve INDEX.xml descriptions for LLM reader routing
argument-hint: <collection>
arguments: [collection]
allowed-tools:
  - Bash(cat *)
  - Bash(find *)
  - Bash(printf *)
  - Bash(rm -f */descriptions_agent*.txt)
  - Bash(test *)
  - Bash(uv run update-index-descriptions *)
  - Bash(wc *)
  - Glob
  - Grep
  - Read
  - Task
  - Write
---

# Improve INDEX.xml Descriptions

Batch-improve `$collection` descriptions for LLM reader routing using parallel subagents.

## 1. Validate Collection

!`printf '<existing_collections>\n'; find . -mindepth 2 -maxdepth 2 -name INDEX.xml -printf '%h\n'; printf '</existing_collections>\n'`

Validate `$collection` against `<existing_collections>`; reject if absent, and if it looks like a typo suggest the closest match:

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
  ## 🤔 Collection `$collection` not found
  - No INDEX.xml at `$collection/INDEX.xml`
  - Existing collections: [list]
  - Did you mean: [closest match]?
  ```

</validation_failure>

<validation_success>

```
## 📋 Ready to improve `$collection` descriptions
Found [N] documents in INDEX.xml
```

</validation_success>

</validation_examples>

## 2. Analyse and Group Documents

Read `$collection/INDEX.xml` and extract all `<source>` entries into a list.

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

You are improving INDEX.xml descriptions in the `[COLLECTION]` collection. Each description is a routing signal an LLM reads to pick which files answer a question.

## Your Assigned Documents

[List of local_file values for this agent]

## Your Task

Read `.claude/references/source-descriptions.md` and follow its quality rules and reference examples.

Then, for each assigned document:

1. Analyse the markdown file at `[COLLECTION]/<local_file>`
2. Draft a description following those criteria
3. Compare to current description in INDEX.xml, ensure yours is better
4. Count words - rewrite until [20, 30]: `printf '%s' "<draft>" | wc -w`

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
   cat $collection/descriptions_agent*.txt > $collection/descriptions_improved.txt
   ```

2. Present summary to user:

```markdown
## 📊 New Descriptions for `$collection`

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
uv run update-index-descriptions "$collection" "$collection/descriptions_improved.txt"
```

Clean up any remaining agent files:

```bash
rm -f $collection/descriptions_agent*.txt
```

## 6. Report Success

```markdown
## 🎉 Description Improvement Complete

Collection: `$collection`
- Descriptions updated: [N]
- INDEX.xml: `$collection/INDEX.xml`
```

If user cancels, clean up temporary files and confirm cancellation.
