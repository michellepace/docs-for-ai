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
| `--version` | boolean | Show the version and exit. | `Sentinel.UNSET` |
| `-l`, `--log-level` | choice (`DEBUG` \| `INFO` \| `WARN` \| `ERROR` \| `CRITICAL`) | Choose logging level. | `WARN` |
| `-q`, `--quiet` | boolean | Suppress standard out. | `False` |
| `-y`, `--yes` | boolean | Automatic yes to prompts, running non-interactively. | `False` |
| `-d`, `--development-mode` | boolean | Run in development mode; enables debug logs and server autoreload. | `False` |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

## marimo cache

Inspect and clean up the on-disk cache.

These commands work on the `__marimo__/cache/` directories written by marimo's
caching (`mo.persistent_cache`).

**Usage:**

```text
marimo cache [OPTIONS] COMMAND [ARGS]...
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

### marimo cache clean

Delete all relevant cache entries for a notebook or directory.

When this command is given a notebook path, it deletes all corresponding cache
entries. When given a directory path, it deletes all cache entries that
correspond to notebooks in that directory and (optionally) its subdirectories.
Additionally accepts explicit cache keys, as provided to `mo.persistent_cache`.
Defaults to the current directory if no path is provided.

Pass one or more arguments. Accepts `-r`/`--recursive` to search `path`
recursively. A prompt is provided before deletion; use `-y`/`--yes` to
skip the prompt, or `--dry-run` to simulate the deletion.

Example usage:

```text
marimo cache clean my_notebook.py

marimo cache clean my_notebook.py train

marimo cache clean notebooks/
```

**Usage:**

```text
marimo cache clean [OPTIONS] [PATH] [NAME]...
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `-r`, `--recursive` | boolean | Search a directory PATH recursively for cache directories, skipping dot-folders. | `False` |
| `-y`, `--yes` | boolean | Delete without asking for confirmation. | `False` |
| `--dry-run` | boolean | Report what deletions would occur. | `False` |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

### marimo cache dir

Print the cache directories for the directory of the argument.

A blank argument defaults to the current directory, otherwise the provided
argument should be a notebook file or directory. A notebook path resolves to the
cache directory used by a given notebook. A directory resolves within that
directory, as if a notebook ran there. With `-r`/`--recursive`, the directory is
instead searched recursively for `cache` directories, skipping dot-folders.

Example usage:

```text
marimo cache dir

marimo cache dir notebook.py

marimo cache dir -r notebooks/
```

**Usage:**

```text
marimo cache dir [OPTIONS] [PATH]
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `-r`, `--recursive` | boolean | Search a directory PATH recursively for cache directories, skipping dot-folders. | `False` |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

### marimo cache prune

Delete cache entries without an associated notebook or cell.

This command deletes cache entries that cannot be reached within a notebook. For
instance, when the notebook no longer has an associated cell, or the associated
notebook is deleted.

Files that may be part of a running write are not deleted by default, nor are
files that may still be associated with a notebook. These files may still be
active, so the flag `--force` should be provided to delete all unneeded files.

Defaults to the current directory if no path is provided. Accepts
`-r`/`--recursive` to search `path` recursively. A prompt is provided
before deletion; use `-y`/`--yes` to skip the prompt, or `--dry-run` to
simulate the deletion.

Example usage:

```text
marimo cache prune my_notebook.py

marimo cache prune --dry-run -r notebooks/

marimo cache prune -y notebooks/
```

**Usage:**

```text
marimo cache prune [OPTIONS] [PATH]
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `-r`, `--recursive` | boolean | Search a directory PATH recursively for cache directories, skipping dot-folders. | `False` |
| `-y`, `--yes` | boolean | Delete without asking for confirmation. | `False` |
| `--dry-run` | boolean | Report what deletions would occur. | `False` |
| `--force` | boolean | Delete cache files from abandoned or active writes, and clear cache files that may still be associated with a notebook. Use with caution. | `False` |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

### marimo cache size

Print disk usage and entry counts for the cache.

Prints the disk usage and entry count for each cache directory that
PATH resolves to, and a total when there is more than one. Accepts
`-r`/`--recursive` to search PATH recursively.

Example usage:

```text
marimo cache size

marimo cache size -r notebooks/
```

**Usage:**

```text
marimo cache size [OPTIONS] [PATH]
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `-r`, `--recursive` | boolean | Search a directory PATH recursively for cache directories, skipping dot-folders. | `False` |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

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
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

## marimo config

Various commands for the marimo config.

**Usage:**

```text
marimo config [OPTIONS] COMMAND [ARGS]...
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

### marimo config describe

Describe the marimo config.

**Usage:**

```text
marimo config describe [OPTIONS]
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

### marimo config show

Show the marimo config.

**Usage:**

```text
marimo config show [OPTIONS] [NOTEBOOK]
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `--show-sources` | boolean | Include source comments for configuration settings and tables. | `Sentinel.UNSET` |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

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
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

## marimo edit

Create or edit notebooks.
If NAME is a url, the notebook will be downloaded to a temporary file.

- marimo edit Start the marimo notebook server
- marimo edit notebook.py Create or edit notebook.py

**Usage:**

```text
marimo edit [OPTIONS] [NAME] [ARGS]...
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `--config` | text | Override a configuration field for this invocation. Can be repeated. | `Sentinel.UNSET` |
| `-p`, `--port` | integer range (between `0` and `65535`) | Port to attach to. | None |
| `--host` | text | Host to attach to. | `127.0.0.1` |
| `--proxy` | text | Address of reverse proxy. | None |
| `--headless` | boolean | Don't launch a browser. | `False` |
| `--token` / `--no-token` | boolean | Use a token for authentication. This enables session-based authentication. A random token will be generated if --token-password is not set. If --no-token is set, session-based authentication will not be used. | `True` |
| `--token-password` | text | Use a specific token for authentication. This enables session-based authentication. A random token will be generated if not set. Pass -q before to this flag to suppress the connection message and keep the token out of logs. | None |
| `--token-password-file` | text | Path to file containing token password, or '-' for stdin. Mutually exclusive with --token-password. | None |
| `--base-url` | text | Base URL for the server. Should start with a /. | `` |
| `--allow-origins` | text | Allowed origins for HTTP and WebSocket connections. Can be repeated. Use \* for all origins. | None |
| `--skip-update-check` | boolean | Don't check if a new version of marimo is available for download. | `False` |
| `--sandbox` | choice (`uv` \| `pixi`) | Run the notebook in an isolated environment, with dependencies tracked via PEP 723 inline metadata. If already declared, dependencies will install automatically. Choose uv (default) or pixi. | None |
| `--no-sandbox` | boolean | Never run in a sandbox, and never prompt to. | `False` |
| `--trusted` / `--untrusted` | boolean | Use --trusted to run remote notebooks on the host. Use --untrusted to run one remote or local notebook in a container. | None |
| `--container-engine` | text | Engine for container execution. Use docker, podman, nerdctl, finch, container (Apple), or a Docker-compatible executable name or path. | `docker` |
| `--watch` | boolean | Watch the file for changes and reload the code when saved in another editor. | `False` |
| `--skew-protection` / `--no-skew-protection` | boolean | Enable skew protection middleware to prevent version mismatch issues. | `True` |
| `--timeout` | float | Enable a global timeout to shut down the server after specified number of minutes of no connection | None |
| `--session-ttl` | integer | Seconds to wait before closing a session on websocket disconnect. If None is provided, sessions are not automatically closed. | None |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

## marimo env

Print out environment information for debugging purposes.

**Usage:**

```text
marimo env [OPTIONS]
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

## marimo export

Export a notebook to various formats.

**Usage:**

```text
marimo export [OPTIONS] COMMAND [ARGS]...
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

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
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

### marimo export html-wasm

Export a notebook as a WASM-powered standalone HTML file.

Example:

```text
marimo export html-wasm notebook.py -o notebook.wasm.html
```

The exported HTML file runs the notebook using WebAssembly, without a local
Python or marimo installation. This lets you share interactive notebooks on
the web without setting up infrastructure to run Python code. By default, the
browser downloads the Python runtime and packages from hosted sources.

The exported notebook runs using Pyodide, which supports most
but not all Python packages. To learn more, see the Pyodide
documentation.

By default, the export must be served over HTTP. Use --single-file to load
assets from a CDN and open the HTML file directly. Internet access is required.

**Usage:**

```text
marimo export html-wasm [OPTIONS] NAME [ARGS]...
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `-o`, `--output` | path | Output directory or HTML file. | `Sentinel.UNSET` |
| `--single-file` | boolean | Export one HTML file with CDN assets that can be opened directly. | `Sentinel.UNSET` |
| `--mode` | choice (`edit` \| `run`) | Whether the notebook code should be editable or readonly. | `run` |
| `--watch` / `--no-watch` | boolean | Whether to watch the original file and export upon change | `False` |
| `--show-code` / `--no-show-code` | boolean | Whether to show code by default in the exported HTML file; only relevant for run mode. | `False` |
| `--include-cloudflare` / `--no-include-cloudflare` | boolean | Whether to include Cloudflare Worker configuration files (index.js and wrangler.jsonc) for easy deployment. | `False` |
| `--sandbox` / `--no-sandbox` | boolean | Run the command in an isolated virtual environment using `uv run --isolated`. Requires `uv`. | None |
| `-f`, `--force` | boolean | Force overwrite of the output file if it already exists. | `False` |
| `--execute` / `--no-execute` | boolean | Execute the notebook before exporting and embed outputs as a preview. Runs in an isolated environment pinned to WASM-compatible packages when possible. | `False` |
| `--offline` | boolean | Download the Python runtime and notebook packages into the export directory. | `Sentinel.UNSET` |
| `--pyodide-index-url` | text | Mirror of the Pyodide 314.0.0 full/ distribution to bundle the runtime and its packages from. Requires --offline. | `Sentinel.UNSET` |
| `--pypi-index-url` | text | Package index, such as a PyPI mirror, for packages outside the Pyodide distribution. Requires --offline. | `Sentinel.UNSET` |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

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
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

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
| `-o`, `--output` | path | Output file to save the markdown to. If --flavor is omitted, this file's extension selects the markdown flavor. If not provided, markdown will be printed to stdout; shell redirection is not inspected for flavor inference. | None |
| `--sandbox` / `--no-sandbox` | boolean | Run the command in an isolated virtual environment using `uv run --isolated`. Requires `uv`. | None |
| `--flavor` | choice (`pymdown` \| `qmd` \| `mystmd` \| `mdx`) | Markdown flavor to export. | None |
| `-f`, `--force` | boolean | Force overwrite of the output file if it already exists. | `False` |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

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
| `-o`, `--output` | path | Output PDF file to save to. | `Sentinel.UNSET` |
| `--sandbox` / `--no-sandbox` | boolean | Run the command in an isolated virtual environment using `uv run --isolated`. Requires `uv`. | None |
| `-f`, `--force` | boolean | Force overwrite of the output file if it already exists. | `False` |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

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
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

### marimo export session

Execute a notebook or directory of notebooks and export session snapshots.

**Usage:**

```text
marimo export session [OPTIONS] NAME [ARGS]...
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `--sandbox` | choice (`uv` \| `pixi`) | Execute each notebook in an isolated environment with its inline dependencies. Use --sandbox (uv), --sandbox=uv, or --sandbox=pixi. | None |
| `--no-sandbox` | boolean | Never run in a sandbox, and never prompt to. | `False` |
| `--force-overwrite` / `--no-force-overwrite` | boolean | Overwrite all existing session snapshots, even if they are already up-to-date. | `False` |
| `--continue-on-error` / `--no-continue-on-error` | boolean | Continue processing other notebooks if one notebook fails. | `True` |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

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
| `--sandbox` | choice (`uv` \| `pixi`) | Render notebooks in an isolated environment, with dependencies tracked via PEP 723 inline metadata. If already declared, dependencies will install automatically. Use --sandbox (uv), --sandbox=uv, or --sandbox=pixi. Only applies when --execute is used. | None |
| `--no-sandbox` | boolean | Never run in a sandbox, and never prompt to. | `False` |
| `--continue-on-error` / `--fail-fast` | boolean | Continue processing other notebooks if one notebook fails. | `True` |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

## marimo new

Create an empty notebook.

**Usage:**

```text
marimo new [OPTIONS]
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `--config` | text | Override a configuration field for this invocation. Can be repeated. | `Sentinel.UNSET` |
| `-p`, `--port` | integer range (between `0` and `65535`) | Port to attach to. | None |
| `--host` | text | Host to attach to. | `127.0.0.1` |
| `--proxy` | text | Address of reverse proxy. | None |
| `--headless` | boolean | Don't launch a browser. | `False` |
| `--token` / `--no-token` | boolean | Use a token for authentication. This enables session-based authentication. A random token will be generated if --token-password is not set. If --no-token is set, session-based authentication will not be used. | `True` |
| `--token-password` | text | Use a specific token for authentication. This enables session-based authentication. A random token will be generated if not set. Pass -q before to this flag to suppress the connection message and keep the token out of logs. | None |
| `--token-password-file` | text | Path to file containing token password, or '-' for stdin. Mutually exclusive with --token-password. | None |
| `--base-url` | text | Base URL for the server. Should start with a /. | `` |
| `--sandbox` | choice (`uv` \| `pixi`) | Run the notebook in an isolated environment, with dependencies tracked via PEP 723 inline metadata. If already declared, dependencies will install automatically. Choose uv (default) or pixi. | None |
| `--no-sandbox` | boolean | Never run in a sandbox, and never prompt to. | `False` |
| `--skew-protection` / `--no-skew-protection` | boolean | Enable skew protection middleware to prevent version mismatch issues. | `True` |
| `--timeout` | float | Enable a global timeout to shut down the server after specified number of minutes of no connection | None |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

## marimo pair

Pair with a live marimo notebook.

Authentication:
Local discovery and execution use private credentials automatically.
For explicit server access, pass --token or --token-file, or set
MARIMO\_TOKEN. Explicit credentials override local discovery.

Workflow:
Start a notebook if needed:
marimo edit
Execute in the selected notebook:
marimo pair execute --notebook  --code 'print("hello")'
For multiline Python, use --file , or --file - for stdin:
marimo pair execute --notebook  --file - <<'PY'
import marimo.\_code\_mode as cm
async with cm.get\_context() as ctx:
for cell in ctx.cells.values():
print(cell.id, cell.code, cell.status)
PY

Target selection:
Use `marimo pair list` if you need to find the notebook ID.
Pass the notebook ID with --notebook.
Local notebook IDs resolve their URL automatically.
--session is a legacy selector, kept for compatibility. It accepts a
notebook ID or an existing stable session ID. Stable session IDs
require --url, and pair connect does not accept them.
With either selector, --url restricts discovery to that server.
With --url alone, the server must have exactly one running notebook.
If several notebooks are open, ask the user which one.
Do not switch notebooks after authentication or connection errors,
or when execution is unconfirmed.

Agent messages (preview):
Execute automatically attempts an inbox connection in supported harnesses.
After identifying the notebook and conversation, setup is attempted once per owner process.
In a supported harness, retry once. If it fails, continue without messaging:
marimo pair connect --notebook
Codex must use its shared daemon and support codex queue.
Claude Code requires its native inbox on macOS or Linux.
OpenCode 2.0 requires its registered local service.
Inbound message settings still apply; messages can be held or refused.
Notebook agent messages arrive here as messages from marimo.
Oversized agent messages include a complete JSON file on this machine.
Files remain after detach. Cleanup removes owned files older than 24 hours.
Use pair detach --notebook  to stop the inbox.

Rules:
Cells are the unit of work. The scratchpad is temporary; only code mode edits persist.
Cells do not run on creation. Call run\_cell after create\_cell or edit\_cell.
Use async with. Do not await ctx methods.
Install packages with ctx.packages.add, not uv add or pip. Installs change
the project; confirm when the user did not ask.
If an empty cell exists, edit\_cell it instead of creating one.
delete\_cell drops the cell's variables. Ask before deleting.
Do not edit the notebook file directly. Code mode is the only write path.

Code-mode API:
Prefer marimo.\_code\_mode to inspect, create, edit, run, and delete notebook cells.
ctx.cells # each has .id .code .status .errors .console\_outputs
ctx.create\_cell(code) # returns the new cell id
ctx.edit\_cell(cid, code)
ctx.run\_cell(cid)
ctx.delete\_cell(cid)
ctx.packages.add("pandas>=2") # queued, installs on exit
If a cm call fails, run help(cm):
marimo pair execute --notebook  --code 'import marimo.\_code\_mode as cm; help(cm)'

**Usage:**

```text
marimo pair [OPTIONS] COMMAND [ARGS]...
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

### marimo pair connect

Connect this harness inbox to a live notebook.

Supported harnesses: Codex, Claude Code, and OpenCode (macOS/Linux).

OpenCode 2.0 requires its registered local service.

For other harnesses, use pair execute to work with the notebook.

**Usage:**

```text
marimo pair connect [OPTIONS]
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `--url` | text | Restrict notebook selection to this server. | `Sentinel.UNSET` |
| `--notebook` | text | Notebook ID from `marimo pair list`. | `Sentinel.UNSET` |
| `--session` | text | Legacy selector, kept for compatibility. Accepts a notebook ID or an existing stable session ID. | `Sentinel.UNSET` |
| `--token` | text | Server token. Overrides MARIMO\_TOKEN and local discovery. | `Sentinel.UNSET` |
| `--token-file` | file | Read the server token from a local file. | `Sentinel.UNSET` |
| `--harness` | choice (`codex` \| `claude` \| `opencode`) | Select the inbox harness. | `Sentinel.UNSET` |
| `--pid` | integer range (`1` and above) | Process to track for connection lifetime. Defaults to the current harness. Its start time is captured automatically. | `Sentinel.UNSET` |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

### marimo pair detach

Stop the forwarder and detach its notebook inbox.

**Usage:**

```text
marimo pair detach [OPTIONS]
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `--notebook` | text | Notebook ID to disconnect. | `Sentinel.UNSET` |
| `--harness` | choice (`codex` \| `claude` \| `opencode`) | Select the harness to disconnect. | `Sentinel.UNSET` |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

### marimo pair docs

Read notebook guidance on demand.

**Usage:**

```text
marimo pair docs [OPTIONS] [TOPIC]
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

### marimo pair execute

Run Python in the selected live notebook kernel's scratchpad.

**Usage:**

```text
marimo pair execute [OPTIONS]
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `--url` | text | Restrict notebook selection to this server. | `Sentinel.UNSET` |
| `--notebook` | text | Notebook ID from `marimo pair list`. | `Sentinel.UNSET` |
| `--session` | text | Legacy selector, kept for compatibility. Accepts a notebook ID or an existing stable session ID. | `Sentinel.UNSET` |
| `--token` | text | Server token. Overrides MARIMO\_TOKEN and local discovery. | `Sentinel.UNSET` |
| `--token-file` | file | Read the server token from a local file. | `Sentinel.UNSET` |
| `--code`, `-c` | text | Inline Python. | `Sentinel.UNSET` |
| `--file`, `--code-file`, `-f` | text | Read Python from a UTF-8 file, or from stdin when PATH is '-'. Supply exactly one input option. | `Sentinel.UNSET` |
| `--stream` | boolean | Write stdout and stderr as they arrive. Default: print one JSON result. | `Sentinel.UNSET` |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

### marimo pair list

List active notebooks and their host IDs.

**Usage:**

```text
marimo pair list [OPTIONS]
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `--url` | text | Server URL. Repeat to list more than one server. | `Sentinel.UNSET` |
| `--token-file` | file | Read the server token from a local file. | `Sentinel.UNSET` |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

### marimo pair prompt

Generate a prompt for pair programming on a running marimo notebook.

**Usage:**

```text
marimo pair prompt [OPTIONS]
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `--url` | text | URL to include in the prompt. | `Sentinel.UNSET` |
| `--notebook` | text | Notebook ID to include in the prompt. | `Sentinel.UNSET` |
| `--session` | text | Notebook ID or stable session ID to include in the prompt. | `Sentinel.UNSET` |
| `--with-token` | boolean | Prompt for an auth token and store it in a temp file. Leave empty if MARIMO\_TOKEN is set. | `False` |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

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
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

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
| `--config` | text | Override a configuration field for this invocation. Can be repeated. | `Sentinel.UNSET` |
| `-p`, `--port` | integer range (between `0` and `65535`) | Port to attach to. | None |
| `--host` | text | Host to attach to. | `127.0.0.1` |
| `--proxy` | text | Address of reverse proxy. | None |
| `--headless` | boolean | Don't launch a browser. | `False` |
| `--token` / `--no-token` | boolean | Use a token for authentication. This enables session-based authentication. A random token will be generated if --token-password is not set. If --no-token is set, session-based authentication will not be used. | `False` |
| `--token-password` | text | Use a specific token for authentication. This enables session-based authentication. A random token will be generated if not set. Pass -q before to this flag to suppress the connection message and keep the token out of logs. | None |
| `--token-password-file` | text | Path to file containing token password, or '-' for stdin. Mutually exclusive with --token-password. | None |
| `--include-code` | boolean | Send notebook source code to the client. By default, code is not sent to the client and cannot be viewed in the browser. | `False` |
| `--session-ttl` | integer | Seconds to wait before closing a session on websocket disconnect. | `120` |
| `--watch` | boolean | Watch the file for changes and reload the app. If watchdog is installed, it will be used to watch the file. Otherwise, file watcher will poll the file every 1s. | `False` |
| `--skew-protection` / `--no-skew-protection` | boolean | Enable skew protection middleware to prevent version mismatch issues. | `True` |
| `--base-url` | text | Base URL for the server. Should start with a /. | `` |
| `--allow-origins` | text | Allowed origins for HTTP and WebSocket connections. Can be repeated. | None |
| `--redirect-console-to-browser` | boolean | Redirect console logs to the browser console. | `False` |
| `--sandbox` | choice (`uv` \| `pixi`) | Run the notebook in an isolated environment, with dependencies tracked via PEP 723 inline metadata. If already declared, dependencies will install automatically. Choose uv (default) or pixi. | None |
| `--no-sandbox` | boolean | Never run in a sandbox, and never prompt to. | `False` |
| `--check` / `--no-check` | boolean | Disable a static check of the notebook before running. | `True` |
| `--trusted` / `--untrusted` | boolean | Use --trusted to run remote notebooks on the host. Use --untrusted to run one remote or local notebook in a container. | None |
| `--container-engine` | text | Engine for container execution. Use docker, podman, nerdctl, finch, container (Apple), or a Docker-compatible executable name or path. | `docker` |
| `--execute-opengraph-generators` | boolean | Execute OpenGraph generators for trusted notebooks. | `Sentinel.UNSET` |
| `--show-tracebacks` / `--no-show-tracebacks` | boolean | Show detailed error tracebacks in a modal when exceptions occur. | None |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

## marimo shell-completion

Install shell completions for marimo. Supports bash, zsh, and fish.

**Usage:**

```text
marimo shell-completion [OPTIONS]
```

**Options:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |

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
| `-p`, `--port` | integer range (between `0` and `65535`) | Port to attach to. | None |
| `--host` | text | Host to attach to. | `127.0.0.1` |
| `--proxy` | text | Address of reverse proxy. | None |
| `--headless` | boolean | Don't launch a browser. | `False` |
| `--token` / `--no-token` | boolean | Use a token for authentication. This enables session-based authentication. A random token will be generated if --token-password is not set. If --no-token is set, session-based authentication will not be used. | `True` |
| `--token-password` | text | Use a specific token for authentication. This enables session-based authentication. A random token will be generated if not set. Pass -q before to this flag to suppress the connection message and keep the token out of logs. | None |
| `--token-password-file` | text | Path to file containing token password, or '-' for stdin. Mutually exclusive with --token-password. | None |
| `--skew-protection` / `--no-skew-protection` | boolean | Enable skew protection middleware to prevent version mismatch issues. | `True` |
| `-h`, `--help` | boolean | Show this message and exit. | `Sentinel.UNSET` |