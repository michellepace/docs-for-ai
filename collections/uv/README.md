# uv Documentation

Curated docs for targeted AI context.

- Curation Index: [INDEX.xml](INDEX.xml)
- Curation Source: https://github.com/astral-sh/uv/tree/main/docs

**What is uv?** A fast, all-in-one Python package and project manager by Astral, written in Rust, 10-100x faster than pip. It installs dependencies, creates virtual environments, and manages Python versions, replacing pip, virtualenv, pyenv, and pip-tools with a single `pyproject.toml` + lockfile workflow.

---

Later: recurate uv collection from website (direct-fetch)
- `_reject_uv_docs_url()`, `direct_fetch.py`, add to `direct-fetch-rules.toml`
-  need to handle this case (think local_file, source_url canonical)
    - https://docs.astral.sh/uv/getting-started/installation/
    - https://docs.astral.sh/uv/getting-started/installation/index.md
- Then can curate [cli|settings|environment] at all — build-generated, 404 on GitHub
