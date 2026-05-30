---
description: Query curated documentation collection directory to answer the question.
argument-hint: <collection> <question>
allowed-tools:
  - Bash(awk *)
  - Bash(cut *)
  - Glob
  - Grep
  - Read
  - WebFetch
  - WebSearch
---

# Query Documentation Collection

Parse the collection name and question from these arguments: `$ARGUMENTS`

The first word is the **collection name** and the remaining words are the **question**.

## Context

Use the **Collection** name extracted above to construct these paths:

- Collection index path: `~/projects/python/docs-for-ai/<collection>/INDEX.xml`
- Collection directory: `~/projects/python/docs-for-ai/<collection>/`
- Fallback collections: `~/projects/python/docs-for-ai/README.md#repo-collections`

## Your Task

Answer the **Question** using relevant documentation.

1. Analyse the question to understand it clearly.

2. Search the collection index to identify relevant local documentation files.

3. **If relevant index sources found:** Analyse local files to answer the user's question accurately. Cite specific sections using file paths and relevant quotes. If insufficient, ask for confirmatoion to do websearch against offical docs.

4. **If there are no relevant sources:** Determine if the user has specified a relevant collection in respect to the question. Analyse the fallback collections and make a new suggestion (e.g. search another collection or do a websearch)

## Response Format

Structure your response as:

1. **Source:** Specify whether you used local docs (which files) or web search
2. **Answer:** Comprehensive answer to the question
3. **References:** Cite specific local file paths, line numbers, or URLs

## Important Notes

- **Always prefer local documentation** when available and relevant
- **Be explicit** about whether you used local files or web search
- **If the collection doesn't exist**, refer to the README table to show what's available
- **Use the exact path structure** provided above - no path variations
