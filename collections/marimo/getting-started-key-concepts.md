<!-- Source: https://docs.marimo.io/getting_started/key_concepts/ -->

# Key concepts

This page covers marimo's key concepts:

- marimo lets you rapidly experiment with data using Python, SQL, and interactive
  elements in a reproducible **notebook environment**.
- Unlike Jupyter notebooks, marimo notebooks are reusable software artifacts.
  marimo notebooks can be shared as as **interactive web apps** and executed as
  **Python scripts**.

## Editing notebooks

marimo notebooks are **reactive**: they automatically react to your code
changes and UI interactions and keep your notebook up-to-date, not unlike a
spreadsheet. This makes your notebooks reproducible, [eliminating hidden
state](https://docs.marimo.io/faq/#faq-problems); it's also what enables marimo notebooks to double as
apps and Python scripts.

> **Working with expensive notebooks**
>
> If you don't want cells to run automatically, the [runtime can be
> configured](https://docs.marimo.io/guides/configuration/runtime_configuration/) to be lazy, only
> running cells when you ask for them to be run and marking affected cells as
> stale. **See our guide on working with [expensive
> notebooks](https://docs.marimo.io/guides/expensive_notebooks/) for more tips.**

**Create your first notebook.** After [installing
marimo](https://docs.marimo.io/getting_started/installation/), create your first notebook with

```bash
marimo edit my_notebook.py
```

at the command-line.

**The marimo library**.
We recommend starting each marimo notebook with a cell containing a single
line of code,

```python3
import marimo as mo
```

The marimo library lets you use interactive UI elements, layout elements,
dynamic markdown, and more in your marimo notebooks.

### How marimo executes cells

A marimo notebook is made of small blocks of Python code called **cells**.
*When you run a cell, marimo automatically runs all cells that read any global
variables defined by that cell.* This is reactive execution.

[Video: https://docs.marimo.io/_static/reactive.mp4](https://docs.marimo.io/_static/reactive.mp4)

**Execution order.**
The order of cells on the page has no bearing on the order cells are
executed in: execution order is determined by the variables
cells define and the variables they read.

You have full freedom over how to organize your code and tell your stories:
move helper functions and other "appendices" to the bottom of your notebook, or
put cells with important outputs at the top.

**No hidden state.**
marimo notebooks have no hidden state because the program state is
automatically synchronized with your code changes and UI interactions. And if
you delete a cell, marimo automatically deletes that cell's variables,
preventing painful bugs that arise in traditional notebooks.

**No magical syntax.**
There's no magical syntax or API required to opt-in to reactivity: cells are
Python and *only Python*. Behind-the-scenes, marimo statically analyzes each
cell's code just once, creating a directed acyclic graph based on the
global names each cell defines and reads. This is how data flows
in a marimo notebook.

> **Minimize variable mutation.**
>
> marimo's understanding of your code is based on variable definitions and
> references; marimo does not track mutations to objects at runtime. For this
> reason, if you need to mutate a variable (such as adding a new column to a
> dataframe), you should perform the mutation in the same cell as the one that
> defines it.

Learn more in our [reactivity guide](https://docs.marimo.io/guides/reactivity/#reactivity-mutations).

For more on reactive execution, open the dataflow tutorial

```bash
marimo tutorial dataflow
```

or read the [reactivity guide](https://docs.marimo.io/guides/reactivity/). To visualize and understand how data flows through your notebook, check out our [dataflow tools](https://docs.marimo.io/guides/editor_features/dataflow/).

### Visualizing outputs

marimo visualizes the last expression of each cell as its **output**. Outputs
can be any Python value, including markdown and interactive elements created
with the marimo library, (*e.g.*, [`mo.md`](https://docs.marimo.io/api/markdown/#marimo.md), [`mo.ui.slider`](https://docs.marimo.io/api/inputs/slider/#marimo.ui.slider)).
You can even interpolate Python values into markdown (using `mo.md(f"...")`) and
other marimo elements to build rich composite outputs:

[Video: https://docs.marimo.io/_static/outputs.mp4](https://docs.marimo.io/_static/outputs.mp4)

> Thanks to reactive execution, running a cell refreshes all the relevant outputs in your notebook.

The marimo library also comes with elements for laying out outputs, including
[`mo.hstack`](https://docs.marimo.io/api/layouts/stacks/#marimo.hstack), [`mo.vstack`](https://docs.marimo.io/api/layouts/stacks/#marimo.vstack),
[`mo.accordion`](https://docs.marimo.io/api/layouts/accordion/#marimo.accordion), [`mo.ui.tabs`](https://docs.marimo.io/api/inputs/tabs/#marimo.ui.tabs), [`mo.sidebar`](https://docs.marimo.io/api/layouts/sidebar/#marimo.sidebar),
[`mo.nav_menu`](https://docs.marimo.io/api/inputs/nav_menu/#marimo.nav_menu), [`mo.ui.table`](https://docs.marimo.io/api/inputs/table/#marimo.ui.table),
and [many more](https://docs.marimo.io/api/layouts/).

For more on outputs, try these tutorials:

```bash
marimo tutorial markdown
marimo tutorial plots
marimo tutorial layout
```

or read the [visualizing outputs guide](https://docs.marimo.io/guides/outputs/).

### Creating interactive elements

The marimo library comes with many interactive stateful elements in
[`marimo.ui`](https://docs.marimo.io/api/inputs/), including simple ones like sliders, dropdowns, text fields, and file
upload areas, as well as composite ones like forms, arrays, and dictionaries
that can wrap other UI elements.

[Video: https://docs.marimo.io/_static/readme-ui.webm](https://docs.marimo.io/_static/readme-ui.webm)

**Using UI elements.**
To use a UI element, create it with `mo.ui` and **assign it to a global
variable.** When you interact with a UI element in your browser (*e.g.*,
sliding a slider), *marimo sends the new value back to Python and reactively
runs all cells that use the element*, which you can access via its `value`
attribute.

> **This combination of interactivity and reactivity is very powerful**: use it
> to make your data tangible during exploration and to build all kinds of tools
> and apps.

*marimo can only synchronize UI elements that are assigned to
global variables.* Use composite elements like [`mo.ui.array`](https://docs.marimo.io/api/inputs/array/#marimo.ui.array) and
[`mo.ui.dictionary`](https://docs.marimo.io/api/inputs/dictionary/#marimo.ui.dictionary) if the set of UI elements is not
known until runtime.

> **Using buttons to execute cells**
>
> Use [`mo.ui.run_button`](https://docs.marimo.io/api/inputs/run_button/#marimo.ui.run_button) to create a button that
> triggers computation when clicked; see our recipes for [an example](https://docs.marimo.io/recipes/#create-a-button-that-triggers-computation-when-clicked).

For more on interactive elements, run the UI tutorial

```bash
marimo tutorial ui
```

or read the [interactivity guide](https://docs.marimo.io/guides/interactivity/).

### Querying dataframes and databases with SQL

marimo has built-in support for SQL: you can query Python dataframes,
databases, CSVs, Google Sheets, or anything else. After executing your query,
marimo returns the result to you as a dataframe, making it seamless
to go back and forth between SQL and Python.

![](https://docs.marimo.io/_static/docs-sql-df.png)

*Query a dataframe using SQL!*

To create a SQL cell, click on the SQL button that appears at the bottom of the
cell array, or right click the create cell button next to a cell. Today,
SQL in marimo is executed using [duckdb](https://duckdb.org/docs/).

To learn more, run the SQL tutorial

```bash
marimo tutorial sql
```

or read the [SQL guide](https://docs.marimo.io/guides/working_with_data/sql/).

## Running notebooks as applications

You can use marimo as a notebook, similar to how you might use Jupyter.

But you can also do more: because marimo notebooks are reactive and can include
interactive elements, hiding notebook code gives you a simple web app!

You can run your notebook as a read-only web app from the command-line:

```bash
marimo run my_notebook.py
```

The default renderer just hides the notebook code and concatenates outputs
vertically. But marimo also supports [other layouts](https://docs.marimo.io/guides/apps/),
such as slides and grid.

## Running notebooks as scripts

Because marimo notebooks are stored as pure Python files, each notebook
can be executed as a script from the command-line:

```python
python my_notebook.py
```

You can also [pass command-line arguments](https://docs.marimo.io/guides/scripts/) to scripts.