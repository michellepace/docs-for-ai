# GitHub-Doc Curation Path Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a first-class, repeatable GitHub-raw curation path so any collection can curate `.md` docs directly from GitHub instead of FireCrawl.

**Architecture:** A new pure-helper module `scripts/github_source.py` (URL detection, raw normalisation, filename derivation, title extraction, stdlib fetch). `curate_doc.py` `main()` gains one routing branch that delegates to it; everything after fetch (README/INDEX creation, file write, index update, cleanup, success message) is shared and unchanged. `sync_index.py` needs no changes — it re-invokes `curate_doc.py` per stored URL, so mixed collections re-scrape for free.

**Tech Stack:** Python ≥3.14, `uv`, stdlib `urllib`/`re`/`xml.etree`, `pytest`, `ruff` (`select = ["ALL"]`), `pyright`.

---

## Spec

Implements `docs/superpowers/specs/2026-05-19-github-doc-curation-path-design.md`. Read it before starting.

## Convention reconciliation (read once)

The spec describes helpers that "raise" on failure. The established project failure convention (see `curate_doc.py::_validate_url`, `_get_firecrawl_client`) is **print `❌ Error: TYPE|detail|url|` then `sys.exit(1)`** — no custom exception classes (this also avoids fighting `ruff`'s `TRY`/`EM` rules under `select = ["ALL"]`). We implement the project convention. It is functionally identical (terminal failure, non-zero exit, structured line) and is asserted in unit tests via `pytest.raises(SystemExit)` + `capsys`.

## File Structure

- **Create** `scripts/github_source.py` — all GitHub-source logic. One responsibility: turn a GitHub URL into `(raw_url, content, title, filename)` or fail loudly. No FireCrawl, no INDEX knowledge, no third-party deps.
- **Create** `tests/test_github_source.py` — fast, no-network, no-mock unit tests for the pure helpers (imports the module directly, mirroring `tests/test_sync_index.py`'s `from scripts.sync_index import ...`).
- **Modify** `scripts/curate_doc.py` — add `import github_source`, add `_reject_github_filename_collision`, add the routing branch in `main()`.
- **Modify** `tests/test_curate_doc.py` — add real-network subprocess integration tests for the GitHub path.
- **Modify** `.claude/commands/curate-doc.md` — one clarifying sentence in Context.
- **Modify** `tests/test_sync_index.py` — one optional mixed-collection round-trip test.

## Import note

`curate_doc.py` is executed as a script (`uv run scripts/curate_doc.py …`), so `scripts/` is `sys.path[0]` — it imports the sibling as `import github_source`. The unit tests run under `pytest` from the project root, so they import `from scripts.github_source import …` (same style as `tests/test_sync_index.py`). `github_source.py` performs no intra-package imports, so both resolution styles work.

## Pre-commit note

Committing `.py` changes triggers the repo pre-commit hooks (`ruff format`, `ruff check`, `pyright`, `pytest`). The existing `pytest` hook runs the whole suite, which includes FireCrawl integration tests needing `API_KEY_MCP_FIRECRAWL` + network. For per-task commits during TDD, run the targeted command shown in each step first; if the pre-commit `pytest` hook blocks a commit purely due to a missing FireCrawl key in your environment (unrelated to this work), commit that task with `git commit --no-verify` and ensure the **final verification task** runs the full gate green with the key set.

---

### Task 1: Module skeleton + `is_github_url`

**Files:**

- Create: `scripts/github_source.py`
- Test: `tests/test_github_source.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_github_source.py`:

```python
"""Unit tests for github_source.py (pure helpers, no network, no mocks)."""

import pytest

from scripts.github_source import is_github_url


class TestIsGithubUrl:
    @pytest.mark.parametrize(
        ("url", "expected"),
        [
            ("https://raw.githubusercontent.com/astral-sh/uv/main/docs/x.md", True),
            ("https://github.com/astral-sh/uv/blob/main/docs/x.md", True),
            ("https://github.com/astral-sh/uv/blob/main/README.md", True),
            ("https://github.com/astral-sh/uv", False),
            ("https://github.com/astral-sh/uv/tree/main/docs", False),
            ("https://docs.astral.sh/uv/reference/cli/index.md", False),
            ("https://shiny.posit.co/py/docs/overview.html", False),
        ],
    )
    def test_classifies_url(self, url: str, expected: bool) -> None:
        assert is_github_url(url) is expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_github_source.py -v`
Expected: collection/import error — `ModuleNotFoundError: No module named 'scripts.github_source'`.

- [ ] **Step 3: Create the module with header, `_fail`, and `is_github_url`**

Create `scripts/github_source.py`:

```python
"""GitHub raw-source curation: detect, normalise, fetch, and name GitHub docs.

Additive companion to the FireCrawl path in ``curate_doc.py``. The pure
helpers (detection, URL normalisation, filename, title) are unit-tested
without network; :func:`fetch_raw` performs the only I/O. Failures follow the
project's ``❌ Error: TYPE|detail|url|`` print-and-exit convention.
"""

import re
import sys
import urllib.error
import urllib.request
from typing import NoReturn
from urllib.parse import urlparse

HTTP_NOT_FOUND = 404
FETCH_TIMEOUT_SECONDS = 30
_USER_AGENT = "docs-for-ai-curate/1.0"
_FILENAME_RE = re.compile(r"^[a-z0-9-]+\.md$")
_FRONTMATTER_TITLE_RE = re.compile(r"^title:\s*(?P<val>.+?)\s*$", re.MULTILINE)
_ANCHOR_LINK_RE = re.compile(r"^\[(?P<text>.+?)\]\(#.*\)$")


def _fail(code: str, detail: str, url: str) -> NoReturn:
    """Print the project ❌ error line and exit non-zero.

    Args:
        code: Error TYPE token (e.g. ``GITHUB_NOT_FOUND``).
        detail: Human-readable cause.
        url: The offending URL.
    """
    print(f"❌ Error: {code}|{detail}|{url}|")
    sys.exit(1)


def is_github_url(url: str) -> bool:
    """Return True if ``url`` is a GitHub raw-markdown source.

    True for ``raw.githubusercontent.com`` hosts, or ``github.com`` hosts
    whose path contains a ``/blob/`` segment. A ``github.com`` URL without
    ``/blob/`` (repo root, ``/tree/``) returns False and is left to FireCrawl.

    Args:
        url: The source URL to classify.

    Returns:
        True if the URL should be curated via the GitHub raw path.
    """
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    if host == "raw.githubusercontent.com":
        return True
    if host == "github.com":
        return "/blob/" in parsed.path
    return False
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_github_source.py -v`
Expected: PASS (7 parametrised cases).

- [ ] **Step 5: Lint and commit**

```bash
uv run ruff format scripts/github_source.py tests/test_github_source.py
uv run ruff check scripts/github_source.py tests/test_github_source.py
uv run pyright scripts/github_source.py
git add scripts/github_source.py tests/test_github_source.py
git commit -m "feat(github): add github_source module with is_github_url"
```

Expected: ruff/pyright clean; commit succeeds.

---

### Task 2: `to_raw_url`

**Files:**

- Modify: `scripts/github_source.py`
- Test: `tests/test_github_source.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_github_source.py` (add `to_raw_url` to the import line):

```python
class TestToRawUrl:
    def test_blob_url_becomes_raw(self) -> None:
        url = "https://github.com/astral-sh/uv/blob/main/docs/getting-started/first-steps.md"
        assert to_raw_url(url) == (
            "https://raw.githubusercontent.com/astral-sh/uv/main/"
            "docs/getting-started/first-steps.md"
        )

    def test_raw_url_passes_through_stripped(self) -> None:
        url = "https://raw.githubusercontent.com/astral-sh/uv/main/docs/x.md/"
        assert to_raw_url(url) == (
            "https://raw.githubusercontent.com/astral-sh/uv/main/docs/x.md"
        )

    def test_malformed_blob_url_fails(self) -> None:
        with pytest.raises(SystemExit) as exc:
            to_raw_url("https://github.com/astral-sh/blob/x")
        assert exc.value.code == 1
```

Update the import line at the top of the file to:

```python
from scripts.github_source import is_github_url, to_raw_url
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_github_source.py::TestToRawUrl -v`
Expected: FAIL — `ImportError: cannot import name 'to_raw_url'`.

- [ ] **Step 3: Add `to_raw_url` to `scripts/github_source.py`**

Append after `is_github_url`:

```python
def to_raw_url(url: str) -> str:
    """Normalise a GitHub URL to its ``raw.githubusercontent.com`` form.

    A ``github.com/{owner}/{repo}/blob/{ref}/{path}`` URL becomes
    ``raw.githubusercontent.com/{owner}/{repo}/{ref}/{path}``. A URL already
    on the raw host is returned unchanged (trailing slash stripped). Assumes
    :func:`is_github_url` is True for ``url``.

    Args:
        url: A GitHub blob or raw URL.

    Returns:
        The canonical raw markdown URL.
    """
    url = url.rstrip("/")
    parsed = urlparse(url)
    if parsed.netloc.lower() == "raw.githubusercontent.com":
        return url
    parts = parsed.path.strip("/").split("/")
    min_segments = 5  # owner / repo / blob / ref / path…
    if len(parts) < min_segments or parts[2] != "blob":
        _fail("UNSUPPORTED_GITHUB", "not a github blob file URL", url)
    owner, repo, _blob, ref, *rest = parts
    return (
        "https://raw.githubusercontent.com/"
        + "/".join([owner, repo, ref, *rest])
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_github_source.py -v`
Expected: PASS (all classes).

- [ ] **Step 5: Lint and commit**

```bash
uv run ruff format scripts/github_source.py tests/test_github_source.py
uv run ruff check scripts/github_source.py tests/test_github_source.py
uv run pyright scripts/github_source.py
git add scripts/github_source.py tests/test_github_source.py
git commit -m "feat(github): add to_raw_url normalisation"
```

---

### Task 3: `derive_filename`

**Files:**

- Modify: `scripts/github_source.py`
- Test: `tests/test_github_source.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_github_source.py` and add `derive_filename` to the import line:

```python
class TestDeriveFilename:
    @pytest.mark.parametrize(
        ("raw_url", "expected"),
        [
            (
                "https://raw.githubusercontent.com/astral-sh/uv/main/"
                "docs/getting-started/features.md",
                "getting-started-features.md",
            ),
            (
                "https://raw.githubusercontent.com/astral-sh/uv/main/"
                "docs/concepts/projects/dependencies.md",
                "concepts-projects-dependencies.md",
            ),
            (
                "https://raw.githubusercontent.com/o/r/main/readme.md",
                "readme.md",
            ),
            (
                "https://raw.githubusercontent.com/o/r/main/docs/index.md",
                "index.md",
            ),
        ],
    )
    def test_derives_expected_name(self, raw_url: str, expected: str) -> None:
        assert derive_filename(raw_url) == expected

    def test_non_md_source_fails(self) -> None:
        with pytest.raises(SystemExit):
            derive_filename(
                "https://raw.githubusercontent.com/o/r/main/pyproject.toml"
            )

    def test_pattern_violating_name_fails(self) -> None:
        # Multi-segment ref shifts segments; underscore breaks the pattern.
        with pytest.raises(SystemExit):
            derive_filename(
                "https://raw.githubusercontent.com/o/r/main/docs/a_b.md"
            )
```

Update import line:

```python
from scripts.github_source import derive_filename, is_github_url, to_raw_url
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_github_source.py::TestDeriveFilename -v`
Expected: FAIL — `ImportError: cannot import name 'derive_filename'`.

- [ ] **Step 3: Add `derive_filename`**

Append to `scripts/github_source.py`:

```python
def derive_filename(raw_url: str) -> str:
    r"""Derive the collection filename from a raw GitHub URL path.

    Strips the ``{owner}/{repo}/{ref}`` structural prefix, drops a single
    leading ``docs`` segment, joins the remainder with ``-`` and appends
    ``.md``. Exits via the ❌ convention for non-``.md`` sources
    (``UNSUPPORTED_GITHUB``) or names that fail ``^[a-z0-9-]+\.md$``
    (``GITHUB_FILENAME``) — e.g. a multi-segment git ref.

    Args:
        raw_url: A ``raw.githubusercontent.com`` markdown URL.

    Returns:
        A filename such as ``getting-started-features.md``.
    """
    segments = urlparse(raw_url).path.strip("/").split("/")
    prefix_len = 3  # owner / repo / ref
    remainder = segments[prefix_len:]
    if not remainder or not remainder[-1].endswith(".md"):
        _fail("UNSUPPORTED_GITHUB", "only .md sources supported", raw_url)
    remainder = [*remainder[:-1], remainder[-1][:-3]]
    if remainder and remainder[0] == "docs":
        remainder = remainder[1:]
    filename = "-".join(remainder).lower() + ".md"
    if not _FILENAME_RE.match(filename):
        _fail(
            "GITHUB_FILENAME",
            f"derived '{filename}' fails ^[a-z0-9-]+\\.md$",
            raw_url,
        )
    return filename
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_github_source.py -v`
Expected: PASS.

- [ ] **Step 5: Lint and commit**

```bash
uv run ruff format scripts/github_source.py tests/test_github_source.py
uv run ruff check scripts/github_source.py tests/test_github_source.py
uv run pyright scripts/github_source.py
git add scripts/github_source.py tests/test_github_source.py
git commit -m "feat(github): add derive_filename with pattern guard"
```

---

### Task 4: `extract_title`

**Files:**

- Modify: `scripts/github_source.py`
- Test: `tests/test_github_source.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_github_source.py` and add `extract_title` to the import line:

```python
class TestExtractTitle:
    def test_frontmatter_title_unquoted(self) -> None:
        content = "---\ntitle: Working on projects\n---\n# Heading\n"
        assert extract_title(content, "x") == "Working on projects"

    def test_frontmatter_title_quoted(self) -> None:
        content = '---\ntitle: "Managing dependencies"\n---\n# H\n'
        assert extract_title(content, "x") == "Managing dependencies"

    def test_frontmatter_without_title_falls_to_h1(self) -> None:
        content = "---\ndescription: x\n---\n# Python versions\n"
        assert extract_title(content, "x") == "Python versions"

    def test_h1_when_no_frontmatter(self) -> None:
        content = "# First steps\n\nbody\n"
        assert extract_title(content, "x") == "First steps"

    def test_h1_anchor_link_is_unwrapped(self) -> None:
        content = "# [CLI Reference](#cli-reference)\n"
        assert extract_title(content, "x") == "CLI Reference"

    def test_fenced_hash_is_ignored(self) -> None:
        content = "```python\n# not a heading\n```\n# Real Title\n"
        assert extract_title(content, "x") == "Real Title"

    def test_basename_fallback_title_cased(self) -> None:
        content = "no headings here\n"
        url = "https://raw.githubusercontent.com/o/r/main/docs/getting-started.md"
        assert extract_title(content, url) == "Getting Started"
```

Update import line:

```python
from scripts.github_source import (
    derive_filename,
    extract_title,
    is_github_url,
    to_raw_url,
)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_github_source.py::TestExtractTitle -v`
Expected: FAIL — `ImportError: cannot import name 'extract_title'`.

- [ ] **Step 3: Add `extract_title`**

Append to `scripts/github_source.py`:

```python
def extract_title(content: str, raw_url: str) -> str:
    """Extract a document title using the settled precedence.

    (1) YAML frontmatter ``title:``; else (2) the first ATX ``# H1`` after
    the frontmatter block, skipping fenced code and unwrapping a
    ``[text](#anchor)`` link; else (3) the URL basename minus ``.md``, split
    on ``-`` and title-cased.

    Args:
        content: The raw markdown text.
        raw_url: The source URL, used for the basename fallback.

    Returns:
        The resolved title (never empty).
    """
    body = content
    if content.startswith("---\n"):
        end = content.find("\n---", len("---\n"))
        if end != -1:
            match = _FRONTMATTER_TITLE_RE.search(content[len("---\n") : end])
            if match:
                return match.group("val").strip().strip("\"'")
            newline = content.find("\n", end + 1)
            body = content[newline + 1 :] if newline != -1 else ""
    in_fence = False
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
        elif not in_fence and stripped.startswith("# "):
            heading = stripped[2:].strip()
            anchor = _ANCHOR_LINK_RE.match(heading)
            return anchor.group("text").strip() if anchor else heading
    basename = urlparse(raw_url).path.rsplit("/", 1)[-1].removesuffix(".md")
    return " ".join(w.capitalize() for w in basename.split("-")) or "Untitled"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_github_source.py -v`
Expected: PASS.

- [ ] **Step 5: Lint and commit**

```bash
uv run ruff format scripts/github_source.py tests/test_github_source.py
uv run ruff check scripts/github_source.py tests/test_github_source.py
uv run pyright scripts/github_source.py
git add scripts/github_source.py tests/test_github_source.py
git commit -m "feat(github): add extract_title with precedence rules"
```

---

### Task 5: `fetch_raw` (real network)

**Files:**

- Modify: `scripts/github_source.py`
- Test: `tests/test_github_source.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_github_source.py` and add `fetch_raw` to the import line. These two tests make real HTTPS requests to stable public URLs (no mocks):

```python
RAW_OK = (
    "https://raw.githubusercontent.com/astral-sh/uv/main/"
    "docs/getting-started/first-steps.md"
)
RAW_404 = (
    "https://raw.githubusercontent.com/astral-sh/uv/main/"
    "docs/zzz-does-not-exist-xyz.md"
)


class TestFetchRaw:
    def test_fetches_real_markdown(self, capsys: pytest.CaptureFixture[str]) -> None:
        text = fetch_raw(RAW_OK)
        assert len(text) > 0
        assert "✅ Fetched raw markdown|" in capsys.readouterr().out

    def test_404_fails_with_not_found(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        with pytest.raises(SystemExit):
            fetch_raw(RAW_404)
        assert "❌ Error: GITHUB_NOT_FOUND|" in capsys.readouterr().out
```

Update import line:

```python
from scripts.github_source import (
    derive_filename,
    extract_title,
    fetch_raw,
    is_github_url,
    to_raw_url,
)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_github_source.py::TestFetchRaw -v`
Expected: FAIL — `ImportError: cannot import name 'fetch_raw'`.

- [ ] **Step 3: Add `fetch_raw`**

Append to `scripts/github_source.py`:

```python
def fetch_raw(raw_url: str) -> str:
    """Fetch raw markdown over HTTPS using only the standard library.

    Exits via the ❌ convention on HTTP 404 (``GITHUB_NOT_FOUND``) or any
    other HTTP/network/decoding failure (``GITHUB_FETCH``) — no fallback.

    Args:
        raw_url: A ``raw.githubusercontent.com`` markdown URL.

    Returns:
        The UTF-8 decoded markdown text.
    """
    request = urllib.request.Request(  # noqa: S310
        raw_url, headers={"User-Agent": _USER_AGENT}
    )
    try:
        with urllib.request.urlopen(  # noqa: S310
            request, timeout=FETCH_TIMEOUT_SECONDS
        ) as response:
            text = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        if exc.code == HTTP_NOT_FOUND:
            _fail("GITHUB_NOT_FOUND", "404 not found", raw_url)
        _fail("GITHUB_FETCH", f"HTTP {exc.code}", raw_url)
    except (urllib.error.URLError, OSError, UnicodeDecodeError) as exc:
        _fail("GITHUB_FETCH", str(exc), raw_url)
    print(f"✅ Fetched raw markdown|({len(text):,} characters)|")
    return text
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_github_source.py -v`
Expected: PASS (requires network).

- [ ] **Step 5: Lint and commit**

```bash
uv run ruff format scripts/github_source.py tests/test_github_source.py
uv run ruff check scripts/github_source.py tests/test_github_source.py
uv run pyright scripts/github_source.py
git add scripts/github_source.py tests/test_github_source.py
git commit -m "feat(github): add stdlib fetch_raw with loud failures"
```

---

### Task 6: Route GitHub URLs through `curate_doc.py`

**Files:**

- Modify: `scripts/curate_doc.py` (import; add `_reject_github_filename_collision`; rewrite the routing region of `main()`)
- Test: `tests/test_curate_doc.py`

- [ ] **Step 1: Write the failing integration tests**

Append to `tests/test_curate_doc.py` (the existing `run_script` helper and imports stay). These run the real CLI via subprocess against stable public GitHub URLs:

```python
GH_RAW = (
    "https://raw.githubusercontent.com/astral-sh/uv/main/"
    "docs/getting-started/first-steps.md"
)
GH_BLOB = (
    "https://github.com/astral-sh/uv/blob/main/"
    "docs/getting-started/first-steps.md"
)
GH_404 = (
    "https://raw.githubusercontent.com/astral-sh/uv/main/"
    "docs/zzz-does-not-exist-xyz.md"
)
GH_NON_MD = "https://github.com/astral-sh/uv/blob/main/pyproject.toml"


class TestGithubSourcePath:
    def test_raw_url_curates_into_collection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            new_dir = Path(tmp_dir) / "uv"
            exit_code, output = run_script(str(new_dir), GH_RAW)

            assert exit_code == 0
            assert "✅ Detected GitHub source|" in output
            assert "✅ Fetched raw markdown|" in output
            assert "🎉 Curation Success!|" in output

            doc = new_dir / "getting-started-first-steps.md"
            assert doc.exists()
            assert doc.read_text().strip() != ""

            index = (new_dir / "INDEX.xml").read_text()
            assert f"<source_url>{GH_RAW}</source_url>" in index
            assert (
                "<local_file>getting-started-first-steps.md</local_file>"
                in index
            )
            assert "<description>PLACEHOLDER</description>" in index

    def test_blob_url_stored_normalised_to_raw(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            new_dir = Path(tmp_dir) / "uv"
            exit_code, _ = run_script(str(new_dir), GH_BLOB)

            assert exit_code == 0
            index = (new_dir / "INDEX.xml").read_text()
            assert f"<source_url>{GH_RAW}</source_url>" in index

    def test_404_fails_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            new_dir = Path(tmp_dir) / "uv"
            exit_code, output = run_script(str(new_dir), GH_404)

            assert exit_code != 0
            assert "❌ Error: GITHUB_NOT_FOUND|" in output
            md_files = (
                list(new_dir.glob("*.md")) if new_dir.exists() else []
            )
            assert md_files == []

    def test_non_md_blob_rejected_before_fetch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            new_dir = Path(tmp_dir) / "uv"
            exit_code, output = run_script(str(new_dir), GH_NON_MD)

            assert exit_code != 0
            assert "❌ Error: UNSUPPORTED_GITHUB|" in output

    def test_filename_collision_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            coll = Path(tmp_dir) / "uv"
            coll.mkdir()
            (coll / "getting-started-first-steps.md").write_text("# Old\n")
            (coll / "INDEX.xml").write_text(
                "<docs_index>\n"
                "  <source>\n"
                "    <title>Old</title>\n"
                "    <description>PLACEHOLDER</description>\n"
                "    <source_url>https://example.com/other</source_url>\n"
                "    <local_file>getting-started-first-steps.md</local_file>\n"
                "    <scraped_at>2026-05-19</scraped_at>\n"
                "  </source>\n"
                "</docs_index>\n"
            )
            exit_code, output = run_script(str(coll), GH_RAW)

            assert exit_code != 0
            assert "❌ Error: FILENAME_COLLISION|" in output
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_curate_doc.py::TestGithubSourcePath -v`
Expected: FAIL — GitHub URLs currently route to FireCrawl (errors / wrong filenames / no GitHub messages).

- [ ] **Step 3: Add the `import` and `_reject_github_filename_collision`**

In `scripts/curate_doc.py`, add the sibling-script import. Place it after the existing imports (ruff will order it):

```python
import github_source
```

Add this helper next to the other private helpers (e.g. directly after `_cleanup_old_file`):

```python
def _reject_github_filename_collision(
    index_path: Path, filename: str, source_url: str
) -> None:
    """Exit if ``filename`` is already mapped to a different source in INDEX.

    Prevents a cross-repo GitHub collision silently overwriting another
    source's markdown within the same collection.

    Args:
        index_path: Path to the collection INDEX.xml.
        filename: The derived local filename.
        source_url: The normalised raw URL being curated.
    """
    if not index_path.exists():
        return
    root = ET.parse(index_path).getroot()
    for source in root.findall("source"):
        file_elem = source.find("local_file")
        url_elem = source.find("source_url")
        if (
            file_elem is not None
            and file_elem.text == filename
            and url_elem is not None
            and url_elem.text != source_url
        ):
            print(
                f"❌ Error: FILENAME_COLLISION|"
                f"{filename} already mapped to {url_elem.text}|{source_url}|"
            )
            sys.exit(1)
```

- [ ] **Step 4: Rewrite the routing region of `main()`**

In `scripts/curate_doc.py::main()`, replace the block that currently runs from the FireCrawl scrape through the filename computation — i.e. these existing lines:

```python
    # Scrape with FireCrawl (do this before creating files to fail fast)
    scraped_doc = _scrape_with_firecrawl(source_url, max_attempts=2)
    content = scraped_doc["markdown"]
    metadata = scraped_doc["metadata"]

    # Confirm successful scrape
    char_count = len(content)
    print(f"✅ Scraped content|({char_count:,} characters)|")

    title = metadata.get("title", "Untitled")

    # Extract source site URL (scheme + netloc) for README collection source
    parsed_url = urlparse(source_url)
    source_site_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    # Create README and INDEX if new collection
    if not index_path.exists():
        _create_readme(dir_path, source_site_url)
        _create_index_xml(dir_path)

    # Generate filename from title (with suffix if duplicate title exists)
    base_slug = _slugify_title(title)
    duplicate_count = _get_duplicate_title_count(dir_path, title, source_url)

    if duplicate_count == 0:
        filename = f"{base_slug}.md"
    else:
        filename = f"{base_slug}-{duplicate_count + 1}.md"
```

with this:

```python
    # Route: GitHub raw source vs FireCrawl (do this before creating files
    # to fail fast). All routing lives here; sync_index.py is unaffected.
    is_github = github_source.is_github_url(source_url)

    if is_github:
        source_url = github_source.to_raw_url(source_url)
        print(f"✅ Detected GitHub source|{source_url}|")
        filename = github_source.derive_filename(source_url)  # exits if invalid
        content = github_source.fetch_raw(source_url)  # exits on 404/network
        title = github_source.extract_title(content, source_url)
    else:
        scraped_doc = _scrape_with_firecrawl(source_url, max_attempts=2)
        content = scraped_doc["markdown"]
        print(f"✅ Scraped content|({len(content):,} characters)|")
        title = scraped_doc["metadata"].get("title", "Untitled")

    # Extract source site URL (scheme + netloc) for README collection source
    parsed_url = urlparse(source_url)
    source_site_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    # Create README and INDEX if new collection
    if not index_path.exists():
        _create_readme(dir_path, source_site_url)
        _create_index_xml(dir_path)

    if is_github:
        _reject_github_filename_collision(index_path, filename, source_url)
    else:
        base_slug = _slugify_title(title)
        duplicate_count = _get_duplicate_title_count(
            dir_path, title, source_url
        )
        if duplicate_count == 0:
            filename = f"{base_slug}.md"
        else:
            filename = f"{base_slug}-{duplicate_count + 1}.md"
```

Everything after this point (`file_path = dir_path / filename`, the write, `_add_or_update_source_in_index`, `_cleanup_old_file`, the success message) is unchanged.

- [ ] **Step 5: Run the GitHub integration tests to verify they pass**

Run: `uv run pytest tests/test_curate_doc.py::TestGithubSourcePath -v`
Expected: PASS (5 tests; requires network).

- [ ] **Step 6: Run the existing FireCrawl tests to verify no regression**

Run: `uv run pytest tests/test_curate_doc.py::TestInputValidation -v`
Expected: PASS (fast, no API). The FireCrawl integration tests still require `API_KEY_MCP_FIRECRAWL` and are unchanged by this task.

- [ ] **Step 7: Lint and commit**

```bash
uv run ruff format scripts/curate_doc.py tests/test_curate_doc.py
uv run ruff check scripts/curate_doc.py tests/test_curate_doc.py
uv run pyright scripts/curate_doc.py
git add scripts/curate_doc.py tests/test_curate_doc.py
git commit -m "feat(curate): route GitHub URLs through github_source"
```

(If the pre-commit `pytest` hook blocks solely on a missing FireCrawl key in your environment, see the "Pre-commit note" above.)

---

### Task 7: Document the routing in the slash command

**Files:**

- Modify: `.claude/commands/curate-doc.md`

- [ ] **Step 1: Add one clarifying sentence to Context**

In `.claude/commands/curate-doc.md`, in the `## Context` section, after the existing paragraph that begins "The script scrapes content from $2…", add:

```markdown
GitHub source URLs (`raw.githubusercontent.com`, or `github.com` with a `/blob/` path) are fetched directly as raw markdown — no FireCrawl, no API tokens. The stored `source_url` is normalised to its `raw.githubusercontent.com` form. All other URLs use FireCrawl exactly as before.
```

- [ ] **Step 2: Lint the markdown**

Run: `npx markdownlint-cli2 --fix ".claude/commands/curate-doc.md"`
Expected: no remaining errors.

- [ ] **Step 3: Commit**

```bash
git add .claude/commands/curate-doc.md
git commit -m "docs(curate-doc): note GitHub raw routing"
```

---

### Task 8 (optional): Mixed-collection re-scrape round-trip

Confirms `sync_index.py` handles a GitHub-raw entry unchanged (no code change — proves the integration claim).

**Files:**

- Modify: `tests/test_sync_index.py`

- [ ] **Step 1: Write the test**

Append to `tests/test_sync_index.py` (uses the file's existing imports/helpers; runs `sync_index.py` via its established invocation in that file — match the surrounding test style):

```python
class TestGithubRawRescrape:
    def test_github_raw_entry_round_trips(self, tmp_path: Path) -> None:
        coll = tmp_path / "uv"
        coll.mkdir()
        raw_url = (
            "https://raw.githubusercontent.com/astral-sh/uv/main/"
            "docs/getting-started/first-steps.md"
        )
        (coll / "getting-started-first-steps.md").write_text("# stale\n")
        (coll / "INDEX.xml").write_text(
            "<docs_index>\n"
            "  <source>\n"
            "    <title>First steps</title>\n"
            "    <description>Real curated description kept verbatim</description>\n"
            f"    <source_url>{raw_url}</source_url>\n"
            "    <local_file>getting-started-first-steps.md</local_file>\n"
            "    <scraped_at>2026-05-19</scraped_at>\n"
            "  </source>\n"
            "</docs_index>\n"
        )

        exit_code, output = run_script(str(coll))

        assert exit_code == 0
        index = (coll / "INDEX.xml").read_text()
        assert f"<source_url>{raw_url}</source_url>" in index
        assert (
            "<description>Real curated description kept verbatim</description>"
            in index
        )
```

> Note: `tests/test_sync_index.py` already defines a subprocess runner for `sync_index.py`. Use that existing helper (read the top of the file); the name `run_script` above is illustrative — match whatever the file already uses.

- [ ] **Step 2: Run the test**

Run: `uv run pytest tests/test_sync_index.py::TestGithubRawRescrape -v`
Expected: PASS (requires network).

- [ ] **Step 3: Lint and commit**

```bash
uv run ruff format tests/test_sync_index.py
uv run ruff check tests/test_sync_index.py
git add tests/test_sync_index.py
git commit -m "test(sync): mixed-collection github-raw round-trip"
```

---

### Task 9: Full quality gate

**Files:** none (verification only)

- [ ] **Step 1: Format and lint everything**

```bash
uv run ruff format
uv run ruff check
```

Expected: "All checks passed!" / no diffs.

- [ ] **Step 2: Type-check**

```bash
uv run pyright
```

Expected: 0 errors.

- [ ] **Step 3: Run the new + pure suites (network, no FireCrawl key needed)**

```bash
uv run pytest tests/test_github_source.py tests/test_curate_doc.py::TestGithubSourcePath tests/test_curate_doc.py::TestInputValidation -v
```

Expected: all PASS.

- [ ] **Step 4: Run the full suite**

```bash
uv run pytest -v
```

Expected: all PASS. (Requires `API_KEY_MCP_FIRECRAWL` set + network for the pre-existing FireCrawl integration tests, which are unchanged.) If the FireCrawl key is unavailable in this environment, state that explicitly in the completion report rather than claiming the full suite passed.

- [ ] **Step 5: Final verification commit (if any formatting changed)**

```bash
git add -A
git commit -m "chore: format/lint pass for github curation path"
```

(Skip if Step 1 produced no changes and all prior task commits are clean.)

---

## Self-Review

**Spec coverage:**

- Architecture & routing (single branch in `main()`, shared tail unchanged, `sync_index.py` untouched) → Task 6 (+ Task 8 proves the sync claim).
- `is_github_url` / `to_raw_url` / `derive_filename` / `extract_title` / `fetch_raw` → Tasks 1–5.
- `<source_url>` normalised to raw in INDEX → Task 6 `test_blob_url_stored_normalised_to_raw`.
- Error types `GITHUB_NOT_FOUND`, `GITHUB_FETCH`, `GITHUB_FILENAME`, `UNSUPPORTED_GITHUB`, `FILENAME_COLLISION` → Tasks 3, 5, 6 (covered by `_fail` + `_reject_github_filename_collision`; all fail before mutation, asserted in Task 6 `test_404_fails_without_mutation`).
- Success progress lines `✅ Detected GitHub source` / `✅ Fetched raw markdown` → Tasks 5–6 (asserted in Task 6 `test_raw_url_curates_into_collection`).
- Command surface: `curate-doc.md` clarifying sentence → Task 7; `rescrape-docs.md`/`improve-index-xml.md`/`ask-docs.md` unaffected → no task needed (no code path touches them; Task 8 confirms rescrape).
- Testing approach (fast no-network unit + real-network subprocess, no mocks) → Tasks 1–6, 8.
- Known limitations (multi-segment ref → loud `GITHUB_FILENAME`; new-collection README source line) → Task 3 `test_pattern_violating_name_fails`; README behaviour intentionally unchanged (no task).
- Out of scope (migration, non-`.md`, FireCrawl behaviour, rendered fallback) → not implemented, by design.

**Placeholder scan:** No "TBD"/"TODO"/"similar to". The one "illustrative name" note in Task 8 explicitly instructs reading the file for the real helper name (Task 8 is optional and the variance is genuine, not a placeholder).

**Type consistency:** `_fail(code, detail, url) -> NoReturn`, `is_github_url(str) -> bool`, `to_raw_url(str) -> str`, `derive_filename(str) -> str`, `extract_title(str, str) -> str`, `fetch_raw(str) -> str`, `_reject_github_filename_collision(Path, str, str) -> None` — names and signatures used consistently across Tasks 1–6 and the import lines.
