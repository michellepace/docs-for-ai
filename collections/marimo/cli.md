<!-- Source: https://docs.marimo.io/cli/ -->

# marimo

Welcome to marimo!
Getting started:

- marimo tutorial intro

Example usage:

- marimo edit create or edit notebooks
- marimo edit notebook.py create or edit a notebook called notebook.py
- marimo run notebook.py run a notebook as a read-only app
- marimo tutorial --help list tutorials

**Usage:**

```text
marimo [OPTIONS] COMMAND [ARGS]...
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `--version` | boolean | Show the version and exit. | `False` |
| `-l`, `--log-level` | choice (`DEBUG` \| `INFO` \| `WARN` \| `ERROR` \| `CRITICAL`) | Choose logging level. | `WARN` |
| `-q`, `--quiet` | boolean | Suppress standard out. | `False` |
| `-y`, `--yes` | boolean | Automatic yes to prompts, running non-interactively. | `False` |
| `-d`, `--development-mode` | boolean | Run in development mode; enables debug logs and server autoreload. | `False` |
| `-h`, `--help` | boolean | Show this message and exit. | `False` |

## marimo check

Check and format marimo files.

**Usage:**

```text
marimo check [OPTIONS] [FILES]...
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `--fix` | boolean | Whether to in place update files. | `False` |
| `--strict` | boolean | Whether warnings return a non-zero exit code. | `False` |
| `-v`, `--verbose` / `-q`, `--quiet` | boolean | Whether to print detailed messages. | `True` |
| `--unsafe-fixes` | boolean | Enable fixes that may change code behavior (e.g., removing empty cells). | `False` |
| `--ignore-scripts` | boolean | Ignore files that are not recognizable as marimo notebooks. | `False` |
| `--format` | choice (`full` \| `json`) | Output format for diagnostics. | `full` |
| `--select` | text | Comma-separated rule codes/prefixes to enable, replacing config. e.g. --select MB,MR001 | None |
| `--ignore` | text | Comma-separated rule codes/prefixes to ignore. e.g. --ignore MF004,MF007 | None |
| `-h`, `--help` | boolean | Show this message and exit. | `False` |

## marimo config

Various commands for the marimo config.

**Usage:**

```text
marimo config [OPTIONS] COMMAND [ARGS]...
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `-h`, `--help` | boolean | Show this message and exit. | `False` |

### marimo config describe

Describe the marimo config.

**Usage:**

```text
marimo config describe [OPTIONS]
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `-h`, `--help` | boolean | Show this message and exit. | `False` |

### marimo config show

Show the marimo config.

**Usage:**

```text
marimo config show [OPTIONS]
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `-h`, `--help` | boolean | Show this message and exit. | `False` |

## marimo convert

Convert a Jupyter notebook, Markdown file, or Python script to a marimo notebook.

Supported input formats:
- `.ipynb` (local or GitHub-hosted)
- `.md` files with `{python}` code fences
- `.py` scripts in py:percent format

Behavior:
- Jupyter notebooks: outputs are stripped.

- Markdown files: only `{python}` fenced code blocks are converted.

Example:
```text
x = 1 + 2
print(x)
```

- Python scripts:
- If already a valid marimo notebook, no conversion is performed.
- Otherwise, marimo attempts to convert using py:percent formatting,
preserving top-level comments and docstrings.

Example usage:

```text
marimo convert your_nb.ipynb -o your_nb.py
```

or

```text
marimo convert your_nb.md -o your_nb.py
```

or

```text
marimo convert script.py -o your_nb.py
```

You can also pass global flags to the main marimo command.
For example, use `-q` to suppress output or `-y`
to automatically accept all prompts of the command.

```text
marimo -q -y convert script.py -o your_nb.py
```

After conversion:

```text
marimo edit your_nb.py
```

Note:
Since marimo's reactive execution differs from traditional notebooks,
you may need to refactor code that mutates variables across cells
(e.g., modifying a dataframe in multiple cells), which can lead to
unexpected behavior.

**Usage:**

```text
marimo convert [OPTIONS] FILENAME
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `-o`, `--output` | path | Output file to save the converted notebook to. If not provided, the converted notebook will be printed to stdout. | None |
| `-h`, `--help` | boolean | Show this message and exit. | `False` |

## marimo edit

Create or edit notebooks.
If NAME is a url, the notebook will be downloaded to a temporary file.
\* marimo edit Start the marimo notebook server
\* marimo edit notebook.py Create or edit notebook.py

**Usage:**

```text
marimo edit [OPTIONS] [NAME] [ARGS]...
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `-p`, `--port` | integer | Port to attach to. | None |
| `--host` | text | Host to attach to. | `127.0.0.1` |
| `--proxy` | text | Address of reverse proxy. | None |
| `--headless` | boolean | Don't launch a browser. | `False` |
| `--token` / `--no-token` | boolean | Use a token for authentication. This enables session-based authentication. A random token will be generated if --token-password is not set. If --no-token is set, session-based authentication will not be used. | `True` |
| `--token-password` | text | Use a specific token for authentication. This enables session-based authentication. A random token will be generated if not set. | None |
| `--token-password-file` | text | Path to file containing token password, or '-' for stdin. Mutually exclusive with --token-password. | None |
| `--base-url` | text | Base URL for the server. Should start with a /. | `` |
| `--allow-origins` | text | Allowed origins for CORS. Can be repeated. Use \* for all origins. | None |
| `--skip-update-check` | boolean | Don't check if a new version of marimo is available for download. | `False` |
| `--sandbox` / `--no-sandbox` | boolean | Run the notebook in an isolated environment, with dependencies tracked via PEP 723 inline metadata. If already declared, dependencies will install automatically. Requires uv. | None |
| `--trusted` / `--untrusted` | boolean | Run notebooks hosted remotely on the host machine; if --untrusted, runs marimo in a Docker container. | None |
| `--watch` | boolean | Watch the file for changes and reload the code when saved in another editor. | `False` |
| `--skew-protection` / `--no-skew-protection` | boolean | Enable skew protection middleware to prevent version mismatch issues. | `True` |
| `--timeout` | float | Enable a global timeout to shut down the server after specified number of minutes of no connection | None |
| `--session-ttl` | integer | Seconds to wait before closing a session on websocket disconnect. If None is provided, sessions are not automatically closed. | None |
| `-h`, `--help` | boolean | Show this message and exit. | `False` |

## marimo env

Print out environment information for debugging purposes.

**Usage:**

```text
marimo env [OPTIONS]
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `-h`, `--help` | boolean | Show this message and exit. | `False` |

## marimo export

Export a notebook to various formats.

**Usage:**

```text
marimo export [OPTIONS] COMMAND [ARGS]...
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `-h`, `--help` | boolean | Show this message and exit. | `False` |

### marimo export html

Run a notebook and export it as an HTML file.

Example:

```text
marimo export html notebook.py -o notebook.html
```

Optionally pass CLI args to the notebook:

```text
marimo export html notebook.py -o notebook.html -- -arg1 foo -arg2 bar
```

**Usage:**

```text
marimo export html [OPTIONS] NAME [ARGS]...
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `--include-code` / `--no-include-code` | boolean | Include notebook code in the exported HTML file. | `True` |
| `--watch` / `--no-watch` | boolean | Watch notebook for changes and regenerate the output on modification. If watchdog is installed, it will be used to watch the file. Otherwise, file watcher will poll the file every 1s. | `False` |
| `-o`, `--output` | path | Output file to save the HTML to. If not provided, the HTML will be printed to stdout. | None |
| `--sandbox` / `--no-sandbox` | boolean | Run the command in an isolated virtual environment using `uv run --isolated`. Requires `uv`. | None |
| `-f`, `--force` | boolean | Force overwrite of the output file if it already exists. | `False` |
| `-h`, `--help` | boolean | Show this message and exit. | `False` |

### marimo export html-wasm

Export a notebook as a WASM-powered standalone HTML file.

Example:

```text
marimo export html-wasm notebook.py -o notebook.wasm.html
```

The exported HTML file will run the notebook using WebAssembly, making it
completely self-contained and executable in the browser. This lets you
share interactive notebooks on the web without setting up
infrastructure to run Python code.

The exported notebook runs using Pyodide, which supports most
but not all Python packages. To learn more, see the Pyodide
documentation.

In order for this file to be able to run, it must be served over HTTP,
and cannot be opened directly from the file system (e.g. file://).

**Usage:**

```text
marimo export html-wasm [OPTIONS] NAME [ARGS]...
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `-o`, `--output` | path | Output directory to save the HTML to. | \_required |
| `--mode` | choice (`edit` \| `run`) | Whether the notebook code should be editable or readonly. | `run` |
| `--watch` / `--no-watch` | boolean | Whether to watch the original file and export upon change | `False` |
| `--show-code` / `--no-show-code` | boolean | Whether to show code by default in the exported HTML file; only relevant for run mode. | `False` |
| `--include-cloudflare` / `--no-include-cloudflare` | boolean | Whether to include Cloudflare Worker configuration files (index.js and wrangler.jsonc) for easy deployment. | `False` |
| `--sandbox` / `--no-sandbox` | boolean | Run the command in an isolated virtual environment using `uv run --isolated`. Requires `uv`. | None |
| `-f`, `--force` | boolean | Force overwrite of the output file if it already exists. | `False` |
| `--execute` / `--no-execute` | boolean | Execute the notebook before exporting and embed outputs as a preview. Runs in an isolated environment pinned to WASM-compatible packages when possible. | `False` |
| `-h`, `--help` | boolean | Show this message and exit. | `False` |

### marimo export ipynb

Export a marimo notebook as a Jupyter notebook in topological order.

Example:

```text
marimo export ipynb notebook.py -o notebook.ipynb
```

Watch for changes and regenerate the script on modification:

```text
marimo export ipynb notebook.py -o notebook.ipynb --watch
```

Optionally pass CLI args to the notebook:

```text
marimo export ipynb notebook.py -o notebook.ipynb --include-outputs -- -arg1 foo -arg2 bar
```

Requires nbformat to be installed.

**Usage:**

```text
marimo export ipynb [OPTIONS] NAME [ARGS]...
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `--sort` | choice (`top-down` \| `topological`) | Sort cells top-down or in topological order. | `topological` |
| `--watch` / `--no-watch` | boolean | Watch notebook for changes and regenerate the output on modification. If watchdog is installed, it will be used to watch the file. Otherwise, file watcher will poll the file every 1s. | `False` |
| `-o`, `--output` | path | Output file to save the ipynb file to. If not provided, the ipynb contents will be printed to stdout. | None |
| `--include-outputs` / `--no-include-outputs` | boolean | Run the notebook and include outputs in the exported ipynb file. | `False` |
| `--sandbox` / `--no-sandbox` | boolean | Run the command in an isolated virtual environment using `uv run --isolated`. Requires `uv`. | None |
| `-f`, `--force` | boolean | Force overwrite of the output file if it already exists. | `False` |
| `-h`, `--help` | boolean | Show this message and exit. | `False` |

### marimo export md

Export a marimo notebook as a code fenced Markdown file.

Example:

```text
marimo export md notebook.py -o notebook.md
```

Watch for changes and regenerate the script on modification:

```text
marimo export md notebook.py -o notebook.md --watch
```

**Usage:**

```text
marimo export md [OPTIONS] NAME
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `--watch` / `--no-watch` | boolean | Watch notebook for changes and regenerate the output on modification. If watchdog is installed, it will be used to watch the file. Otherwise, file watcher will poll the file every 1s. | `False` |
| `-o`, `--output` | path | Output file to save the markdown to. If not provided, markdown will be printed to stdout. | None |
| `--sandbox` / `--no-sandbox` | boolean | Run the command in an isolated virtual environment using `uv run --isolated`. Requires `uv`. | None |
| `-f`, `--force` | boolean | Force overwrite of the output file if it already exists. | `False` |
| `-h`, `--help` | boolean | Show this message and exit. | `False` |

### marimo export pdf

Export a marimo notebook as a PDF file.

Example:

```text
marimo export pdf notebook.py -o notebook.pdf
```

Optionally pass CLI args to the notebook:

```text
marimo export pdf notebook.py -o notebook.pdf -- -arg1 foo -arg2 bar
```

Export PDFs in a specific format such as slides:

```text
marimo export pdf notebook.py -o notebook.pdf --as=slides
```

Requires nbformat and nbconvert to be installed.

**Usage:**

```text
marimo export pdf [OPTIONS] NAME [ARGS]...
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `--include-outputs` / `--no-include-outputs` | boolean | Run the notebook and include outputs in the exported PDF file. | `True` |
| `--include-inputs` / `--no-include-inputs` | boolean | Include code cell inputs in the exported PDF file. | `True` |
| `--webpdf` / `--no-webpdf` | boolean | Use nbconvert's WebPDF exporter (Chromium). If disabled, marimo will try standard PDF export (pandoc + TeX) first and fall back to WebPDF. | `True` |
| `--rasterize-outputs` / `--no-rasterize-outputs` | boolean | Rasterize marimo widget HTML and Vega outputs to PNG fallbacks before PDF conversion (enabled by default). | `True` |
| `--raster-scale` | float range (between `1.0` and `4.0`) | Scale factor for rasterized output screenshots. | `4.0` |
| `--raster-server` | choice (`static` \| `live`) | Server mode used for raster capture. Use 'static' (default) for faster captures, or 'live' if outputs require a live Python connection. For --as=slides, 'live' is recommended. | `static` |
| `--as` | choice (`document` \| `slides`) | PDF export preset. Use `slides` for reveal.js slide-style output. If omitted, marimo exports as a standard document PDF. | None |
| `--watch` / `--no-watch` | boolean | Watch notebook for changes and regenerate the output on modification. If watchdog is installed, it will be used to watch the file. Otherwise, file watcher will poll the file every 1s. | `False` |
| `-o`, `--output` | path | Output PDF file to save to. | \_required |
| `--sandbox` / `--no-sandbox` | boolean | Run the command in an isolated virtual environment using `uv run --isolated`. Requires `uv`. | None |
| `-f`, `--force` | boolean | Force overwrite of the output file if it already exists. | `False` |
| `-h`, `--help` | boolean | Show this message and exit. | `False` |

### marimo export script

Export a marimo notebook as a flat script, in topological order.

Example:

```text
marimo export script notebook.py -o notebook.script.py
```

Watch for changes and regenerate the script on modification:

```text
marimo export script notebook.py -o notebook.script.py --watch
```

**Usage:**

```text
marimo export script [OPTIONS] NAME
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `--watch` / `--no-watch` | boolean | Watch notebook for changes and regenerate the output on modification. If watchdog is installed, it will be used to watch the file. Otherwise, file watcher will poll the file every 1s. | `False` |
| `-o`, `--output` | path | Output file to save the script to. If not provided, the script will be printed to stdout. | None |
| `--sandbox` / `--no-sandbox` | boolean | Run the command in an isolated virtual environment using `uv run --isolated`. Requires `uv`. | None |
| `-f`, `--force` | boolean | Force overwrite of the output file if it already exists. | `False` |
| `-h`, `--help` | boolean | Show this message and exit. | `False` |

### marimo export session

Execute a notebook or directory of notebooks and export session snapshots.

**Usage:**

```text
marimo export session [OPTIONS] NAME [ARGS]...
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `--sandbox` / `--no-sandbox` | boolean | Run the command in an isolated virtual environment using `uv run --isolated`. Requires `uv`. | None |
| `--force-overwrite` / `--no-force-overwrite` | boolean | Overwrite all existing session snapshots, even if they are already up-to-date. | `False` |
| `--continue-on-error` / `--no-continue-on-error` | boolean | Continue processing other notebooks if one notebook fails. | `True` |
| `-h`, `--help` | boolean | Show this message and exit. | `False` |

### marimo export thumbnail

Generate OpenGraph thumbnails for notebooks.

**Usage:**

```text
marimo export thumbnail [OPTIONS] NAME [ARGS]...
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `--width` | integer | Viewport width for the screenshot. | `1200` |
| `--height` | integer | Viewport height for the screenshot. | `630` |
| `--scale` | integer range (between `1` and `4`) | Device scale factor for screenshots. Output resolution will be `width*scale` x `height*scale`. | `2` |
| `--timeout-ms` | integer | Additional time to wait after page load before screenshot. | `1500` |
| `--output` | path | Output filename. If omitted, writes to `<notebook_dir>/__marimo__/assets/<notebook_stem>/opengraph.png`. | None |
| `--overwrite` / `--no-overwrite` | boolean | Overwrite existing thumbnails. | `False` |
| `--include-code` / `--no-include-code` | boolean | Whether to include code in the rendered HTML before screenshot. | `False` |
| `--execute` / `--no-execute` | boolean | Execute notebooks and include their outputs in thumbnails. In --no-execute mode (default), thumbnails are generated from notebook structure without running code (and will not include outputs). | `False` |
| `--sandbox` / `--no-sandbox` | boolean | Render notebooks in an isolated environment, with dependencies tracked via PEP 723 inline metadata. If already declared, dependencies will install automatically. Requires uv. Only applies when --execute is used. | None |
| `--continue-on-error` / `--fail-fast` | boolean | Continue processing other notebooks if one notebook fails. | `True` |
| `-h`, `--help` | boolean | Show this message and exit. | `False` |

## marimo new

Create an empty notebook, or generate from a prompt with AI

- marimo new Create an empty notebook
- marimo new prompt.txt Generate a notebook from a prompt in a file.
- marimo new "Plot an interactive 3D surface with matplotlib." Generate a notebook from a prompt.

Visit [https://marimo.app/ai](https://marimo.app/ai) for more prompt examples.

**Usage:**

```text
marimo new [OPTIONS] [PROMPT]
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `-p`, `--port` | integer | Port to attach to. | None |
| `--host` | text | Host to attach to. | `127.0.0.1` |
| `--proxy` | text | Address of reverse proxy. | None |
| `--headless` | boolean | Don't launch a browser. | `False` |
| `--token` / `--no-token` | boolean | Use a token for authentication. This enables session-based authentication. A random token will be generated if --token-password is not set. If --no-token is set, session-based authentication will not be used. | `True` |
| `--token-password` | text | Use a specific token for authentication. This enables session-based authentication. A random token will be generated if not set. | None |
| `--token-password-file` | text | Path to file containing token password, or '-' for stdin. Mutually exclusive with --token-password. | None |
| `--base-url` | text | Base URL for the server. Should start with a /. | `` |
| `--sandbox` / `--no-sandbox` | boolean | Run the notebook in an isolated environment, with dependencies tracked via PEP 723 inline metadata. If already declared, dependencies will install automatically. Requires uv. | None |
| `--skew-protection` / `--no-skew-protection` | boolean | Enable skew protection middleware to prevent version mismatch issues. | `True` |
| `--timeout` | float | Enable a global timeout to shut down the server after specified number of minutes of no connection | None |
| `-h`, `--help` | boolean | Show this message and exit. | `False` |

## marimo pair

Commands for pair programming with AI.

**Usage:**

```text
marimo pair [OPTIONS] COMMAND [ARGS]...
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `-h`, `--help` | boolean | Show this message and exit. | `False` |

### marimo pair prompt

Generate a prompt for pair programming on a running marimo notebook.

**Usage:**

```text
marimo pair prompt [OPTIONS]
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `--url` | text | URL of the running marimo kernel. | \_required |
| `--claude` | boolean | Validate that the marimo-pair Claude Code skill is installed. | `False` |
| `--codex` | boolean | Validate that the marimo-pair Codex skill is installed. | `False` |
| `--opencode` | boolean | Validate that the marimo-pair opencode skill is installed. | `False` |
| `--with-token` | boolean | Prompt for an auth token and store it in a temp file. | `False` |
| `-h`, `--help` | boolean | Show this message and exit. | `False` |

## marimo recover

Recover a marimo notebook from a JSON file.

When the frontend loses its connection to the kernel, marimo auto-saves
unsaved cell changes to a JSON recovery file. Use this command to convert
that JSON file back into a marimo notebook (.py), printing the recovered
source to stdout.

Example:

```text
marimo recover notebook_recovery.json > recovered_notebook.py
```

**Usage:**

```text
marimo recover [OPTIONS] NAME
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `-h`, `--help` | boolean | Show this message and exit. | `False` |

## marimo run

Run a notebook as an app in read-only mode.

If NAME is a url, the notebook will be downloaded to a temporary file.

Example:

```text
marimo run notebook.py
marimo run folder another_folder
marimo run app.py -- --arg value
```

**Usage:**

```text
marimo run [OPTIONS] NAME [ARGS]...
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `-p`, `--port` | integer | Port to attach to. | None |
| `--host` | text | Host to attach to. | `127.0.0.1` |
| `--proxy` | text | Address of reverse proxy. | None |
| `--headless` | boolean | Don't launch a browser. | `False` |
| `--token` / `--no-token` | boolean | Use a token for authentication. This enables session-based authentication. A random token will be generated if --token-password is not set. If --no-token is set, session-based authentication will not be used. | `False` |
| `--token-password` | text | Use a specific token for authentication. This enables session-based authentication. A random token will be generated if not set. | None |
| `--token-password-file` | text | Path to file containing token password, or '-' for stdin. Mutually exclusive with --token-password. | None |
| `--include-code` | boolean | Send notebook source code to the client. By default, code is not sent to the client and cannot be viewed in the browser. | `False` |
| `--session-ttl` | integer | Seconds to wait before closing a session on websocket disconnect. | `120` |
| `--watch` | boolean | Watch the file for changes and reload the app. If watchdog is installed, it will be used to watch the file. Otherwise, file watcher will poll the file every 1s. | `False` |
| `--skew-protection` / `--no-skew-protection` | boolean | Enable skew protection middleware to prevent version mismatch issues. | `True` |
| `--base-url` | text | Base URL for the server. Should start with a /. | `` |
| `--allow-origins` | text | Allowed origins for CORS. Can be repeated. | None |
| `--redirect-console-to-browser` | boolean | Redirect console logs to the browser console. | `False` |
| `--sandbox` / `--no-sandbox` | boolean | Run the notebook in an isolated environment, with dependencies tracked via PEP 723 inline metadata. If already declared, dependencies will install automatically. Requires uv. | None |
| `--check` / `--no-check` | boolean | Disable a static check of the notebook before running. | `True` |
| `--trusted` / `--untrusted` | boolean | Run notebooks hosted remotely on the host machine; if --untrusted, runs marimo in a Docker container. | None |
| `--show-tracebacks` / `--no-show-tracebacks` | boolean | Show detailed error tracebacks in a modal when exceptions occur. | None |
| `-h`, `--help` | boolean | Show this message and exit. | `False` |

## marimo shell-completion

Install shell completions for marimo. Supports bash, zsh, and fish.

**Usage:**

```text
marimo shell-completion [OPTIONS]
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `-h`, `--help` | boolean | Show this message and exit. | `False` |

## marimo tutorial

Open a tutorial.

marimo is a powerful library for making reactive notebooks
and apps. To get the most out of marimo, get started with a few
tutorials, starting with the intro:

```text
marimo tutorial intro
```

Recommended sequence:

```text
- intro
- dataflow
- ui
- markdown
- plots
- sql
- layout
- fileformat
- external-dependencies
- markdown-format
- for-jupyter-users
```

**Usage:**

```text
marimo tutorial [OPTIONS] {intro|dataflow|ui|markdown|plots|sql|layout|filefor
                mat|external-dependencies|markdown-format|for-jupyter-users}
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `-p`, `--port` | integer | Port to attach to. | None |
| `--host` | text | Host to attach to. | `127.0.0.1` |
| `--proxy` | text | Address of reverse proxy. | None |
| `--headless` | boolean | Don't launch a browser. | `False` |
| `--token` / `--no-token` | boolean | Use a token for authentication. This enables session-based authentication. A random token will be generated if --token-password is not set. If --no-token is set, session-based authentication will not be used. | `True` |
| `--token-password` | text | Use a specific token for authentication. This enables session-based authentication. A random token will be generated if not set. | None |
| `--token-password-file` | text | Path to file containing token password, or '-' for stdin. Mutually exclusive with --token-password. | None |
| `--skew-protection` / `--no-skew-protection` | boolean | Enable skew protection middleware to prevent version mismatch issues. | `True` |
| `-h`, `--help` | boolean | Show this message and exit. | `False` |