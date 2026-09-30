# Writing INDEX.xml descriptions

Claude reads every title and description in a collection's INDEX.xml at once to decide which docs to open for a user's question. It never sees the docs first. Write the description that gets this doc opened for the questions it answers, and not for the ones it doesn't.

- Say what the doc covers, judged from the whole doc, not its heading. Don't label what kind of doc it is, unless it's a large reference to search rather than read whole; then say so.
- Mention topics the title hides, especially problems users run into.
- Claim only what the doc covers.
- Use the words a user would ask with. Name a command, file or API only if users would type it, and skip option names.
- Don't restate the title or the collection's topic.
- Shorter is better: most docs need 10–20 words.
