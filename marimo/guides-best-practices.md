<!-- Source: https://docs.marimo.io/guides/best_practices/ -->

# Best practices

Here are best practices for writing marimo notebooks.

**Use global variables sparingly.** Keep the number of global variables in your
program small to avoid name collisions. If you have intermediate variables,
encapsulate them in functions or prefix them with an underscore (`_tmp = ...`) to
make them local to a cell.

**Use descriptive names.** Use descriptive variable names, especially for
global variables. This will help you minimize name clashes, and will also
result in better code.

**Use functions.** Encapsulate logic into functions to avoid polluting the
global namespace with
temporary or intermediate variables, and to avoid code duplication.

**Use [`mo.stop`](https://docs.marimo.io/api/control_flow/#marimo.stop) to stop execution.** Use [`mo.stop`](https://docs.marimo.io/api/control_flow/#marimo.stop)
to stop a cell from running when a condition is true; this is helpful
when working with expensive notebooks. For example, prevent a cell from running
until a button is clicked using [`mo.ui.run_button`](https://docs.marimo.io/api/inputs/run_button/#marimo.ui.run_button) and
[`mo.stop`](https://docs.marimo.io/api/control_flow/#marimo.stop).

> **Expensive notebooks**
>
> For more tips on working with expensive notebooks, see the
> associated [guide](https://docs.marimo.io/guides/expensive_notebooks/).

**Use Python modules.** If your notebook gets too long, split complex logic
into helper Python modules and import them into your notebook. Use marimo's
built-in [module
reloading](https://docs.marimo.io/guides/configuration/runtime_configuration/#on-module-change)
to automatically bring changes from your modules into your notebook.

**Minimize mutations.** marimo does not track mutations to objects. Try to
only mutate an object in the cell that creates it, or create new objects
instead of mutating existing ones.

> **Example**
>
> *Don't* split up declarations and mutations over multiple cells. For example, *don't
> do this:*
> ```python
> l = [1, 2, 3]
> ```
> ```python
> l.append(new_item())
> ```
> Instead, *do* **declare and mutate in the same cell**:
> ```python
> l = [1, 2, 3]
> ...
> l.append(new_item())
> ```
> or, if working in multiple cells, **declare a new variable based on the old
> one**:
> ```python
> l = [1, 2, 3]
> ```
> ```python
> extended_list = l + [new_item()]
> ```

**Don't use state and `on_change` handlers.** Don't use `on_change` handlers
to react to UI interactions. Instead, use marimo's built-in [reactive execution
for interactive elements](https://docs.marimo.io/guides/interactivity/).

**Write idempotent cells.**
Write cells whose outputs and behavior are the same
when given the same inputs (references); such cells are called idempotent. This
will help you avoid bugs and cache expensive intermediate computations.