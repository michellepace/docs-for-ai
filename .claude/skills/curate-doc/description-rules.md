# Writing INDEX.xml descriptions

Claude reads every title and description in a collection's INDEX.xml at once to decide which docs to open for a user's question. It never sees the docs first. Write the description that gets this doc opened for the questions it answers, and not for the ones it doesn't.

Do:

- Make clear which questions this doc answers, judged from the whole doc
- Mention topics the title hides, especially problems users run into
- If it's a large reference to search rather than read whole, say so
- Put commands, options and file names in `backticks`
- Claim only what the doc covers
- Shorter is better: most docs need 10–20 words

Don't:

- Restate the title or the collection's topic
- Excessively keyword stuff: this is a description, not a summary

## Examples

Three kinds of doc: a how-to, a large reference, a problem guide. Borrow the approach, not the wording.

```xml
<title>Code intelligence plugins</title>
<description>Install a language server plugin so Claude sees type errors after edits and navigates code by symbol, and answer the LSP plugin recommendation dialog.</description>

<title>Plugin manifest reference</title>
<description>Complete reference for plugin.json: every field with its type, accepted path forms, and the userConfig and environment variable schemas.</description>

<title>Caching</title>
<description>Why edited local packages aren't rebuilt and how `cache-keys` or `--reinstall` fix it; plus clearing, pruning and caching in CI.</description>
```
