<!-- Source: https://docs.marimo.io/getting_started/installation/ -->

# Installation

You can install marimo alongside your notebook's packages using any major Python
package manager. With pip or Conda, you'll first need to create and activate a
[virtual environment](https://docs.marimo.io/guides/package_management/projects/#use-an-existing-environment)
or [Conda
environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands).
Project managers such as uv and Pixi handle this setup automatically when you
launch marimo from your project with `uv run` or `pixi run`.

> **Try a standalone notebook**
>
> [uv](https://docs.astral.sh/uv/) and [Pixi](https://pixi.prefix.dev/) can manage
> Python and install marimo for you without setting up a project. To try a notebook
> with its own dependencies:
> **uv:**
>
> ```bash
> uvx marimo edit --sandbox notebook.py
> ```
>
> **Pixi:**
>
> ```bash
> pixi exec marimo edit --sandbox=pixi notebook.py
> ```
> To add marimo to an existing codebase, see
> [working in projects](https://docs.marimo.io/guides/package_management/projects/).
> See [package management](https://docs.marimo.io/guides/package_management/) to compare
> projects and notebook sandboxes.

> **Use our editor extensions**
>
> Try our [VS Code
> extension](https://marketplace.visualstudio.com/items?itemName=marimo-team.vscode-marimo),
> which works in VS Code, Cursor, and other VS Code forks, or our [PyCharm
> plugin](https://plugins.jetbrains.com/plugin/32416-marimo).

## Install with minimal dependencies

To install marimo, run the following in a terminal:

**install with pip:**

```bash
pip install marimo
```

To check if the install worked, run

```bash
marimo tutorial intro
```

**install with uv:**

From your project directory (run `uv init` first for a new project):

```bash
uv add marimo
```

To check if the install worked, run

```bash
uv run marimo tutorial intro
```

**install with Pixi:**

From your project directory (run `pixi init --format pyproject` first for a new project):

```bash
pixi add --pypi marimo
```

To check if the install worked, run

```bash
pixi run marimo tutorial intro
```

**install with conda:**

```bash
conda install -c conda-forge marimo
```

To check if the install worked, run

```bash
marimo tutorial intro
```

A tutorial notebook should open in your browser.

> **Installation issues?**
>
> Having installation issues? Reach out to us [at GitHub](https://github.com/marimo-team/marimo/issues) or [on Discord](https://marimo.io/discord?ref=docs).

## Install with recommended dependencies

marimo is lightweight, with few dependencies, to maximize compatibility with
your own environments.

To unlock additional features in the marimo editor, including SQL cells,
AI completion, server-side plotting of dataframe columns, and more, we
suggest installing `marimo[recommended]`:

**install with pip:**

```bash
pip install "marimo[recommended]"
```

**install with uv:**

```bash
uv add "marimo[recommended]"
```

**install with conda:**

```bash
conda install -c conda-forge marimo "duckdb>=1.0.0" "altair>=5.4.0" pyarrow "polars>=1.9.0" "sqlglotc>=30.11.0" "openai>=1.55.3" "ruff" "nbformat>=5.7.0" "vegafusion>=2.0.0" "vl-convert-python>=1.0.0"
```

Installing marimo in this way installs the following additional dependencies and unlocks the following features:

| Dependency | Feature |
| --- | --- |
| duckdb>=1.0.0 | SQL cells |
| altair>=5.4.0 | Plotting in datasource viewer |
| polars[pyarrow]>=1.9.0 | SQL output back in Python |
| sqlglot[c]>=30.11.0 | SQL cells parsing |
| openai>=1.55.3 | AI features |
| ruff | Formatting |
| nbformat>=5.7.0 | Export as IPYNB |
| vegafusion>=2.0.0 | Performant charting |
| vl-convert-python>=1.0.0 | Required by vegafusion |