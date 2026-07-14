# convex Documentation

Curated docs for targeted AI context.

- Curation Index: [INDEX.xml](INDEX.xml)
- Curation Source: https://docs.convex.dev

**What is Convex?**

Convex is an open source, reactive backend platform: a document-relational database, serverless functions, and client libraries in one. Queries and mutations are just TypeScript functions running in the database — no SQL, no ORM — and every mutation is automatically a transaction. Its sync engine tracks what each query reads and pushes updated results to subscribed clients over WebSockets, so the frontend stays live without manual caching or state management. Actions handle side effects like calling LLMs or external APIs, with built-in scheduling and cron jobs for background work.
