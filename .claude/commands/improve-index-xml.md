---
argument-hint: <collection>
description: Improve INDEX.xml descriptions for LLM reader routing
allowed-tools:
  - Bash(cat *)
  - Bash(echo *)
  - Bash(find *)
  - Bash(printf *)
  - Bash(test *)
  - Bash(uv run scripts/update_index_descriptions.py *)
  - Bash(wc *)
  - Glob
  - Grep
  - Read
  - Task
  - Write
---

# Improve INDEX.xml Descriptions

Batch-improve `$1` collection descriptions for LLM reader routing using parallel subagents.

## 1. Validate Collection

!`printf '<existing_collections>\n'; find . -mindepth 2 -maxdepth 2 -name INDEX.xml -printf '%h\n'; printf '</existing_collections>\n'`

Validate `$1` against `<existing_collections>`; reject if absent, and if it looks like a typo suggest the closest match:

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

You are improving INDEX.xml descriptions in the `[COLLECTION]` collection. Each description is a routing signal an LLM reads to pick which files answer a question.

## Your Assigned Documents

[List of local_file values for this agent]

## Your Task

Read `.claude/references/source-descriptions.md` and follow its quality rules and reference examples.

Then, for each assigned document:

1. Analyse the markdown file at `[COLLECTION]/<local_file>`
2. Write a description following those criteria
3. Compare to current description in INDEX.xml, ensure yours is better
4. **COUNT THE WORDS** with `echo "description text" | wc -w` to verify it's 20-30 words — if not, rewrite until it is

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
