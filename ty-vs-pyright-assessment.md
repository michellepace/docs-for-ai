# Type checking PEP 723 scripts: pyright, ty and the Claude Code LSP plugin

**Short answer.** Yes, PEP 723 scripts can be fully type-checked, in both pre-commit and the language server. The simplest route is ty with its uv script integration (`TY_UV=scripts` on the command line, `experimental.useUv = "scripts"` for the server). It needs uv ≥ 0.12.3. I reproduced your failure in this repo and verified that fix with real commands. The one piece I couldn't test is Claude Code itself launching a ty plugin, because Claude Code doesn't start plugin language servers in cloud sessions. I tested the ty server directly with a small LSP client instead. pyright can also be made to work, but only with machinery you'd have to build and maintain yourself.

Everything below marked **verified** was run in this repo (ty 0.0.89, pyright 1.1.414, Claude Code 2.1.303). This cloud image ships uv 0.11.32, not your 0.13.1, so I installed uv 0.13.1 into the scratchpad and used it wherever uv ≥ 0.12.3 was needed.

---

## 1. The landscape

**A type checker** reads code and reports type errors, without running it. You run it as a one-off command, for example in pre-commit or CI.

**A language server** is a long-running process that an editor (or Claude Code) talks to over the Language Server Protocol (LSP). It sends diagnostics as files change and answers questions such as "go to definition", "hover" and "find references". A Python language server produces its diagnostics by running a type checker internally.

Most modern tools ship **one engine with two front ends**: a CLI for batch checking and a server for live use. That's why you found ty described as both.

| Thing | What it is | Type checker? | Language server? | Role in this repo |
| --- | --- | --- | --- | --- |
| **pyright** (Microsoft, open source) | One engine, two binaries | Yes: `pyright` | Yes: `pyright-langserver` | Dev dependency, pre-commit hook, `[tool.pyright]` |
| **Pylance** | Microsoft's closed-source VS Code extension, built on pyright's engine plus extra editor features. Reads the same `[tool.pyright]` config. | Via the embedded pyright | Yes, VS Code only | Recommended in `.vscode/` (out of scope) |
| **`pyright-lsp` plugin** | Neither. It's a launcher entry: "for `.py`/`.pyi`, start `pyright-langserver --stdio` from `PATH`." It ships no binary and no code (see §3). | No | No (it tells Claude Code which server to start) | Enabled in `.claude/settings.json` |
| **ty** (Astral) | One engine, two modes | Yes: `ty check` | Yes: `ty server` | Not used yet. Its README calls it "a type checker *and language server*". |

**Why you have both pyright and Pylance.** pyright is what the hook runs. Its `pyright-langserver` binary is also what the Claude Code plugin starts. Pylance is VS Code's own packaging of the same engine. So up to three separately installed copies of the pyright engine read `[tool.pyright]`:

- `.venv`'s pyright, used by the hook.
- Whichever `pyright-langserver` comes first on `PATH`, used by Claude Code. In this container it's a separate `uv tool install pyright` at `/root/.local/bin`. It happens to be 1.1.414 today, but it updates independently of the `.venv` copy.
- The copy bundled inside Pylance.

That global binary is also why `venvPath`/`venv` are set, as the comment in `pyproject.toml` says. A `pyright-langserver` started by Claude Code isn't launched through `uv run`, so it needs to be told where `.venv` is. ty doesn't need this: it found `.venv` with no config (**verified** in its `-vv` log: `Resolving local virtual environment: …/.venv`).

---

## 2. Can PEP 723 scripts be fully type-checked, and how?

### Reproduction (verified)

I created a throwaway `scripts/zz_repro_genai.py` (`google-genai` + `pillow`, neither in `.venv`) with two planted bugs that mirror the other project:

1. `types.ThinkingConfig(thinking_level="minimal")`: a string where the SDK annotates its `ThinkingLevel` enum.
2. `BytesIO(part.inline_data.data)`, where `data` is `bytes | None`.

Results:

- `uv run pyright` and `pre-commit run pyright --all-files` both failed with **exactly** the three errors from the other project: `"genai" is unknown import symbol`, plus `google.genai` and `PIL` not resolved.
- Ground truth: `uv sync --script` plus pyright with a venv-free config and `--pythonpath` found **both** bugs.

Also discovered:

- **Why it doesn't fail here today.** `rich` is in the dev group, but nothing in `src/` or `tests/` imports it. Only `scripts/collection_status.py` does. So this repo is already using "option (a)" for its one script.
- **ty already isolates scripts.** Plain `uvx ty check` (no uv integration) flagged `collection_status.py` too (`rich` unresolved). ty gives every file with a `# /// script` header its own environment and deliberately ignores `.venv` for it.

### Approach A: ty with uv script integration (recommended)

When enabled, ty treats each `# /// script` file as its own mini-project. It asks uv to create or sync that script's environment (the same cached environment `uv run` uses) and resolves imports only from there. Project files keep using `.venv`.

Config:

```shell
uv add --dev ty          # pins ty in uv.lock
```

```yaml
      - id: ty
        name: ty
        entry: env TY_UV=scripts uv run ty check
        language: system
        types_or: [python, pyproject]
        pass_filenames: false
```

For the LSP, use a plugin that sends `{"experimental": {"useUv": "scripts"}}` as `initializationOptions` (see §3). This requires uv ≥ 0.12.3. With 0.11.32 every script gets `error[uv-metadata] uv 0.11.32 is too old …` (**verified**).

Verified:

- **Temporary hook in `.pre-commit-config.yaml`.**
  - With bugs: 2 diagnostics, the genai `bytes | None` bug and a second planted bug in another throwaway script.
  - After fixing them: `ty … Passed` over the whole repo, including `collection_status.py`.
  - The pyright hook on the same fixed files still failed with 4 import errors.
  - ty takes ~0.25 s for the whole repo; pyright takes 3.3–4.1 s.
- **`ty server` language server**, driven by my own minimal LSP client:

  | Setup | Result |
  | --- | --- |
  | No option | 3 `unresolved-import` errors |
  | With `useUv: "scripts"` | Imports resolve; the `bytes \| None` bug is reported live |
  | `TY_UV=scripts` env var instead of the option | Same as with the option |
  | Push and pull diagnostic modes | Both work |
  | Script whose environment had never been built | ty built it itself, then reported a planted bug |
  | Project file (`src/…/curate_doc.py`) | Clean |
  | uv too old | Clear diagnostic on line 1 |

- **Bonus:** `--warn missing-direct-dependency` flagged a script importing `httpx`, which it hadn't declared and which was only present as a google-genai dependency. This is a preview rule, off by default.

Constraints: 1 ✅ (with your own plugin; Claude Code end to end unverified), 2 ✅ (verified), 3 ✅ (verified), with the important caveat below.

Trade-offs:

- **ty caught 1 of the 2 planted bugs. This is a deliberate policy, not a resolution failure.**
  - ty models Pydantic's runtime coercion. google-genai's models are lax Pydantic models, so ty types the constructor as `thinking_level: Any | None`, `thinking_budget: LaxInt | None`, `include_thoughts: LaxBool | None`.
  - Pydantic really does accept `"minimal"` at runtime, and the SDK's enum is case-insensitive.
  - pyright reads the declared annotation (`ThinkingLevel | None`) and rejects it.
  - With a local model I confirmed that `ConfigDict(strict=True)` makes ty strict too.
  - The cost: ty also accepted `thinking_budget="lots"`, which would raise at runtime. Expect ty to be **more lenient on every lax Pydantic model**. That includes firecrawl-py, this repo's main dependency (159 `BaseModel` classes).
- **Experimental and beta.** Both the uv integration and ty itself are pre-1.0 (details in §4). Pin ty.
- **ty's own docs disagree.** The Typing FAQ still says ty "does not yet recognize" per-script dependencies (issue #691), while the rules and editor-settings pages document the integration. It works in 0.0.89.
- **`uv check` is not a substitute.** I put a logging wrapper in front of ty via uv's `TY` environment variable:
  - `uv check` runs `ty check --exclude-scripts`, so it **silently skips scripts**. It printed "All checks passed!" while the repro had a bug.
  - `uv check --script X` works (`TY_UV=scripts`), but only one script at a time.
- **Side effect:** checking runs uv, so a new script triggers a package download and environment build.

### Approach B: pyright + script environments at fixed paths + `executionEnvironments`

```toml
[tool.pyright]
# …existing keys…
executionEnvironments = [
  { root = "scripts/zz_repro_genai.py", extraPaths = [".venv-scripts/zz_repro_genai/lib/python3.15/site-packages"] },
  { root = "." },
]
```

Build each script's environment before pyright runs:

```shell
VIRTUAL_ENV="$PWD/.venv-scripts/<stem>" uv sync --script scripts/<stem>.py --active
```

You'd also need `.venv-scripts/` in `.gitignore` and a hook wrapper that loops over scripts, syncs each one, then runs `uv run pyright`.

Verified:

- `uv run pyright` reported **both** bugs.
- `pyright-langserver` also reported **both** bugs live.

I did not write or run the loop wrapper itself.

Constraints: 1 ✅ (the Anthropic plugin works unchanged), 2 ✅ (once the wrapper exists), 3 ✅. This gives the strictest result.

Trade-offs:

- One hand-written config entry per script, with a Python-version-specific path.
- A sync step you write and maintain.
- The language server shows bogus import errors until each environment exists (fresh clone, new script). Nothing builds them automatically.
- `.venv` still applies, so a script importing something it never declared goes unnoticed.

### Approach C: script dependencies in the dev group (your option a)

This is what the repo already does for `rich`. Hook and language server both work with zero machinery.

The costs:

- Every script's dependencies are mixed into `.venv`.
- Each dependency is declared twice (header and `pyproject.toml`), and the two copies drift.
- Scripts are checked against the project's resolution, not their own.
- Undeclared imports go unnoticed.

It's workable for a few small scripts and gets worse with each one.

### Approach D: hybrid, pyright for the project and ty for scripts

Add `ignore = ["scripts"]` to `[tool.pyright]` and a ty hook limited to scripts (`env TY_UV=scripts uv run ty check scripts/`).

Verified: `exclude = ["scripts"]` is **not** enough. pyright's server still reported the 3 import errors when a script was opened. Claude Code pushes those into context after every edit, which invites "fixing" them with suppressions. `ignore` silenced them.

The result: scripts get checked in the hook but have no live diagnostics, and you maintain two checkers.

### Not viable

- Per-script by hand (option b): hook only, language server stays red.
- Suppression comments.
- `uv check` on its own: skips scripts.

| Approach | 1. LSP | 2. Hook green, whole repo | 3. Real checks in scripts | Machinery |
| --- | --- | --- | --- | --- |
| A. ty + `TY_UV=scripts` | ✅ (own plugin; Claude Code end to end untested) | ✅ verified | ✅ verified (Pydantic: lenient) | None |
| B. pyright + `executionEnvironments` | ✅ verified (server) | ✅ (wrapper not written) | ✅ verified (strictest) | Per-script config + sync wrapper |
| C. Dev-group dependencies | ✅ | ✅ | ✅ (project's resolution) | Duplicate declarations |
| D. Hybrid | Project only | ✅ | ✅ (hook only) | Two checkers |

---

## 3. The LSP plugin

**What the Anthropic plugin actually is.** The plugin folder contains only `README.md` and `LICENSE`. Everything that matters is this entry in Anthropic's `marketplace.json`, which I read from the installed marketplace clone:

```json
"lspServers": { "pyright": {
  "command": "pyright-langserver", "args": ["--stdio"],
  "extensionToLanguage": { ".py": "python", ".pyi": "python" } } }
```

**Can it be pointed at a different server?** Not by configuration. It declares no `userConfig`, and the docs describe no setting that overrides a plugin's LSP command (`enabledPlugins` only switches plugins on or off). The only levers:

1. **A `PATH` shim** called `pyright-langserver` that runs something else. Claude Code looks the command up on `PATH`, so this would work mechanically, but it's a misleading hack. Untested.
2. **A same-named `--plugin-dir` plugin.** The docs say it replaces the marketplace one for that session only.
3. **Your own plugin.** This is the right answer. You must disable `pyright-lsp`: the docs say that when two enabled servers claim `.py`, the first registered one wins and the other shows `LSP server "<name>" is not used for .py files`.

**Is a ty plugin feasible?** Yes. The documented `lspServers` schema requires only `command` and `extensionToLanguage`. It also supports `initializationOptions`, `env`, `settings`, timeouts and `${CLAUDE_PROJECT_DIR}` substitution in `args`.

This manifest **passed `claude plugin validate`**. As a control, a deliberate key typo was rejected, so the LSP block really is checked:

```json
{
  "name": "ty-lsp",
  "description": "Python language server (ty) with uv PEP 723 script environments",
  "version": "0.1.0",
  "lspServers": {
    "ty": {
      "command": "uvx",
      "args": ["ty@0.0.89", "server"],
      "extensionToLanguage": { ".py": "python", ".pyi": "python" },
      "initializationOptions": { "experimental": { "useUv": "scripts" } }
    }
  }
}
```

`uvx ty@<pin> server` works in any project. In repos where ty is a dev dependency, use `"command": "uv", "args": ["run", "--project", "${CLAUDE_PROJECT_DIR}", "ty", "server"]` instead, so the language server uses exactly the ty in `uv.lock`, the same as the hook. I drove both launch forms with my LSP client; the `${…}` substitution is documented but untested. `"env": {"TY_UV": "scripts"}` is an alternative to `initializationOptions` (verified against `ty server`).

**Maintaining your own copy.** It's a single JSON block, with no code:

- Put it in `my-claude-marketplace`, either as a plugin folder with `.claude-plugin/plugin.json` or as an inline marketplace entry like Anthropic's.
- In `.claude/settings.json`, set `"ty-lsp@my-claude-marketplace": true` and `"pyright-lsp@claude-plugins-official": false`. `session-start.sh` already installs every key in `enabledPlugins`.
- Ongoing work: bump the ty pin, watch for ty renaming the experimental `useUv` option, and re-run `claude plugin validate` after Claude Code updates.

If you stay on pyright, a self-maintained copy could launch `uv run --project ${CLAUDE_PROJECT_DIR} pyright-langserver --stdio`. That removes the global-binary version drift (this launch form verified), but it does nothing for scripts by itself.

There's also a community plugin, `K-dash/typemux-cc`, that routes between pyright, ty and pyrefly. I haven't inspected it.

**Unverified:** Claude Code actually starting the ty server, passing `initializationOptions` and showing its diagnostics. The docs say: "In cloud sessions, Claude Code doesn't start plugin language servers". This has to be tested on your machine.

---

## 4. Should ty replace pyright in this repo generally?

**On today's code it's a drop-in.**

- Both checkers are clean on `src/` and `tests/` (verified).
- There are no `# pyright:` comments to migrate (grepped).
- ty needs no config to match `[tool.pyright]`: it takes 3.15 from `requires-python` and finds `.venv` itself.
- Ruff already covers the three rules you switched off in pyright.
- ty is about 15× faster on this repo (0.25 s vs 3.3–4.1 s).

**Maturity.**

- The README says "ty is currently in beta". It uses 0.0.x versions and warns that "breaking changes, including changes to diagnostics, may occur between any two versions."
- The script integration and `uv check` are both labelled experimental.
- Releases are frequent (0.0.89 on 16 Oct 2026).
- Pin it in the dev group and bump deliberately.

**Gaps and differences.**

- **Lenient on lax Pydantic models**, by design (§2). This repo's main dependency is Pydantic-based.
- No plugin system. This doesn't matter here.
- Some docs pages lag the features (the Typing FAQ on scripts).

**What would change or break.**

- The pyright hook becomes the ty hook, and `pyright` becomes `ty` in the dev group.
- `[tool.pyright]` can go. Keep it only if Pylance in VS Code should keep reading it.
- `CLAUDE.md`'s `uv run pyright` becomes `TY_UV=scripts uv run ty check`.
- Swap the plugin in `.claude/settings.json`.
- **Cloud sessions:** this image's uv 0.11.32 is too old for `TY_UV`, so `session-start.sh` needs `uv self update` before `uv sync`. A dry run showed 0.11.32 → 0.13.1 is available; I didn't run it inside the hook. Cloud sessions have no language server anyway, so the hook is the only guard there.
- `rich` can leave the dev group, since the script gets its own environment.
- VS Code: Pylance would still flag script imports (out of scope; ty has a VS Code extension).

**Verdict:** yes for this repo. It's small, Ruff-linted, uses standard mode with no pyright-specific features, and is already clean under ty. The price is somewhat weaker checking of calls into Pydantic-based SDKs, plus beta churn.

---

## 5. Recommendation

Replace pyright with ty: ty in the dev group, the `env TY_UV=scripts uv run ty check` hook, and your own `ty-lsp` plugin with `experimental.useUv = "scripts"`, replacing `pyright-lsp`. This is the only option that meets all three constraints with no per-script machinery. It also guards against scripts relying on undeclared imports.

Accept that ty is lenient on lax Pydantic models. If you mainly want pyright's stricter reading of SDK annotations, Approach B is the pyright-native alternative, but you'd own its wrapper and config.

**Next step:** on your machine, put the manifest above in a folder and run `claude --plugin-dir <folder> --debug` in this repo. Ask Claude to add a `bytes | None` bug to a PEP 723 script that imports a package not in `.venv`. Confirm the ty diagnostic arrives (press Ctrl+O) and that the `/plugin` Errors tab is empty. That's the one link I couldn't verify here. If it holds, make the repo swap.

---

## Could not verify in the cloud session

- Claude Code starting the ty (or any) plugin language server and showing its diagnostics. I tested the servers directly with my own LSP client.
- `${CLAUDE_PROJECT_DIR}` substitution in plugin `args`.
- The `PATH` shim approach.
- `uv self update` inside `session-start.sh` (dry run only).
- The `typemux-cc` plugin.
- macOS behaviour (all tests ran on Linux).

Throwaway scripts, temporary `pyproject.toml`, `uv.lock` and hook edits, and `.venv-scripts/` were all removed. `git status` is clean apart from this file.
