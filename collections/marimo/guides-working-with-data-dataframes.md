<!-- Source: https://docs.marimo.io/guides/working_with_data/dataframes/ -->

# Interactive dataframes

**marimo makes you more productive when working with dataframes**.

- [Display dataframes](#displaying-dataframes) in a rich, interactive table and chart views
- [Transform dataframes](#transforming-dataframes) with filters, groupbys,
  aggregations, and more, **no code required**
- [Select data](#selecting-dataframes) from tables or charts and get selections
  back in Python as dataframes

*marimo integrates with [Pandas](https://pandas.pydata.org/) and
[Polars](https://pola.rs) dataframes natively*.

For a video overview on interactive dataframes,
check out our [YouTube tutorial](https://www.youtube.com/watch?v=ZTs7vHzsqlQ).

## Displaying dataframes

marimo lets you page through, search, sort, and filter dataframes, making it
extremely easy to get a feel for your data.

[Video: https://docs.marimo.io/_static/docs-df.mp4](https://docs.marimo.io/_static/docs-df.mp4)

*marimo brings dataframes to life.*

Display dataframes by including them in the last expression of the
cell, just like any other object.

**pandas:**

```python
import pandas as pd

df = pd.read_json(
    "https://raw.githubusercontent.com/vega/vega-datasets/master/data/cars.json"
)
df
```

**polars:**

```python
import polars as pl
import urllib.request

url = "https://raw.githubusercontent.com/vega/vega-datasets/master/data/cars.json"

with urllib.request.urlopen(url) as response:
    df = pl.read_json(response.read())
df
```

**live example:**

[Interactive marimo example](https://marimo.app/?embed=true&mode=edit&show-chrome=false#code/JYWwDg9gTgLgBCAhlUEBQixjgXgc1AOgEEsAKAd2ABMYALHAIhAFNrgBXERgSjTQACmMIQDGLADYS01FgDM4AfUVkeALjRwtcUJFj4UICHEQBnBOm1woLGBygA7QcLGTpshctUaru6PDBEB2ozE3Mwan4rCMIbRGpFACtTCAcyTW1GOhgYMFM1AHoCqEQKQgBzYHoOACMOUxYoUVSYFgcYMQgQAoA3FnLEXv7EAFoQmDNbUwKkU1aoAvHB0WRTQmTUxgytPisbO0c0IA)

To opt out of the rich dataframe viewer, use [`mo.plain`](https://docs.marimo.io/api/layouts/plain/#marimo.plain):

**pandas:**

```python
import pandas as pd
import marimo as mo

df = pd.read_json(
"https://raw.githubusercontent.com/vega/vega-datasets/master/data/cars.json"
)
mo.plain(df)
```

**polars:**

```python
import polars as pl
import marimo as mo

df = pl.read_json(
"https://raw.githubusercontent.com/vega/vega-datasets/master/data/cars.json"
)
mo.plain(df)
```

**live example:**

[Interactive marimo example](https://marimo.app/?embed=true&mode=edit&show-chrome=false#code/JYWwDg9gTgLgBCAhlUEBQixjgXgc1AOgEEsAKAd2ABMYALHAIhAFNrgBXERgSjTQACmMIQDGLADYS01FgDM4AfUVkeALjRwtcUJFj4UICHEQBnBOm1woLGBygA7QcLGTpshctUaru6PDBEB2ozE3Mwan4ragU8CMIbRGpFACtTCAcyTW1GOhgYMFM1AHpiqEQKQgBzYHoOACMOUxYoUQyYFgcYMQgQYoA3FirEAaHEAFoQmDNbU2KkUw6oYqmR0WRTQjSMxmytPisjQjAJRGBMmIPtGztHNCA)

## Transforming dataframes

### No-code transformations

Use [`mo.ui.dataframe`](https://docs.marimo.io/api/inputs/dataframe/#marimo.ui.dataframe) to interactively
transform a dataframe with a GUI, no coding required. When you're done, you
can copy the code that the GUI generated for you and paste it into your
notebook.

[Video: https://docs.marimo.io/_static/docs-dataframe-transform.webm](https://docs.marimo.io/_static/docs-dataframe-transform.webm)

*Build transformations using a GUI*

The transformations you apply will turn into code which is accessible via the "code" tab.

![](https://docs.marimo.io/_static/docs-dataframe-transform-code.png)

*Copy the code of the transformation*

**pandas:**

```python
# Cell 1
import marimo as mo
import pandas as pd

df = pd.DataFrame({"person": ["Alice", "Bob", "Charlie"], "age": [20, 30, 40]})
transformed_df = mo.ui.dataframe(df)
transformed_df
```

```python
# Cell 2
# transformed_df.value holds the transformed dataframe
transformed_df.value
```

**polars:**

```python
# Cell 1
import marimo as mo
import polars as pl

df = pl.DataFrame({"person": ["Alice", "Bob", "Charlie"], "age": [20, 30, 40]})
transformed_df = mo.ui.dataframe(df)
transformed_df
```

```python
# Cell 2
# transformed_df.value holds the transformed dataframe
transformed_df.value
```

**live example:**

[Interactive marimo example](https://marimo.app/?embed=true&mode=edit&show-chrome=false#code/JYWwDg9gTgLgBCAhlUEBQixjgXgc1AOgEEsAKAd2ABMYALHAIhAFNrgBXERgSjTQACmMIQDGLADYS01FgDM4AfUVkeALjRwtcUJFj4UICHEQBnBOm1woLGBygA7QcLGTpshctUaru6PDBEB2ozE3Mwan4ragU8CMIAEUQYRAAxKERWMgBvRjAWKFMIB0Y1OABtRmIJYHFGABo4RgAhCAAjBqaAYTpkGpZGAF1GxkQAcwGy8oAmAAZGgGZ5uAAWWcGAXz4rGAyHUzloVmpFGNwLQg5gQhCUuQysmO3tXaCDo7ZTuU1tGztHfhCLCuKQyeRKFTqH5aV77Q5QY5fQgAN0QEg4LCiv1s9icQA)

### Formatting values

Use `format_mapping` to format values for display in the dataframe UI. This
affects how values appear in the table but does not change the underlying
data returned by `.value` or downloads.

```python
import marimo as mo
import pandas as pd

df = pd.DataFrame(
    {"person": ["Alice", "Bob"], "age": [20, 30], "height_cm": [165.2, 180.4]}
)

def format_height(value: float) -> str:
    return f"{value:.1f} cm"

mo.ui.dataframe(
    df,
    format_mapping={
        "age": "{:d} years".format,
        "height_cm": format_height,
    },
)
```

### Custom filters

Create custom filters with marimo UI elements, like sliders and dropdowns.

**pandas:**

```python
# Cell 1 - create a dataframe
df = pd.DataFrame({"person": ["Alice", "Bob", "Charlie"], "age": [20, 30, 40]})
```

```python
# Cell 2 - create a filter
age_filter = mo.ui.slider(start=0, stop=100, value=50, label="Max age")
age_filter
```

```python
# Cell 3 - display the transformed dataframe
filtered_df = df[df["age"] < age_filter.value]
mo.ui.table(filtered_df)
```

**polars:**

```python
# Cell 1
import marimo as mo
import polars as pl

df = pl.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "David"],
    "age": [25, 30, 35, 40],
    "city": ["New York", "London", "Paris", "Tokyo"]
})

age_filter = mo.ui.slider.from_series(df["age"], label="Max age")
city_filter = mo.ui.dropdown.from_series(df["city"], label="City")

mo.hstack([age_filter, city_filter])
```

```python
# Cell 2
filtered_df = df.filter((pl.col("age") <= age_filter.value) & (pl.col("city") == city_filter.value))
mo.ui.table(filtered_df)
```

**live example:**

[Interactive marimo example](https://marimo.app/?embed=true&mode=edit&show-chrome=false#code/JYWwDg9gTgLgBCAhlUEBQixjgXgc1AOgEEsAKAd2ABMYALHAIhAFNrgBXERgSjTQACmMIQDGLADYS01FgDM4AfUVkeALjRwtcUJFj4UICHEQBnBOm1woLGBygA7QcLGTpshctUaru6PDBEB2ozE3Mwan4ragU8CMIAEUQYRAAxKERWMgBvRjAWKFMIB0Y1OABtRmIJYHFGABo4RgAhCAAjBqaAYTpkGpZGAF1GxkQAcwGy8oAmAAZGgGZ5uAAWWcGAXz4rGztHfiEsVykZeSUVdU1tcZZFOWAJGALcC0IOYEJTGtkoMlMU2A4Zb-CBgHAARlmywAbogJBwWDgAKzLCSINqSJgAWUQAA8TBNeFctDc7g8nlBidZbPYnM4juITh5zt4qfdHgU2IoYi8YuU+aNCYM4AAeAm3dkUwiw+EsQZUoxvD4pNoSFhkSWc6jcuTbbS7WloIA)

## Select dataframe rows

Display dataframes as interactive, [selectable charts](https://docs.marimo.io/guides/working_with_data/plotting/) using
[`mo.ui.altair_chart`](https://docs.marimo.io/api/plotting/#marimo.ui.altair_chart) or
[`mo.ui.plotly`](https://docs.marimo.io/api/plotting/#marimo.ui.plotly), or as a row-selectable table with
[`mo.ui.table`](https://docs.marimo.io/api/inputs/table/#marimo.ui.table). Select points in the chart, or select a table
row, and your selection is *automatically sent to Python as a subset of the original
dataframe*.

[Video: https://docs.marimo.io/_static/docs-dataframe-table.webm](https://docs.marimo.io/_static/docs-dataframe-table.webm)

*Select rows in a table, get them back as a dataframe*

**pandas:**

```python
# Cell 1 - display a dataframe
import marimo as mo
import pandas as pd

df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
table = mo.ui.table(df, selection="multi")
table
```

```python
# Cell 2 - display the selection
table.value
```

**polars:**

```python
# Cell 1 - display a dataframe
import marimo as mo
import polars as pl

df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
table = mo.ui.table(df, selection="multi")
table
```

```python
# Cell 2 - display the selection
table.value
```

**live example:**

[Interactive marimo example](https://marimo.app/?embed=true&mode=edit&show-chrome=false#code/JYWwDg9gTgLgBCAhlUEBQixjgXgc1AOgEEsAKAd2ABMYALHAIhAFNrgBXERgSjTQACmMIQDGLADYS01FgDM4AfUVkeALjRwtcUJFj4UICHEQBnBOm1woLGBygA7QcLGTpshctUaru6PDBEB2ozE3Mwan4ragU8CMIAEUQYRAAxKERWMgBvRkRGNTgAbQBGABo4ACYKgGYAXQrGACMC4oAWCoBWCoA2OoBfPisUpokWXAtCDmBCEbGyGIrTSRZRGGAIByYQDgl13k1tOZZDrRs7R34hLFcpGXklFXVTuGPCADdECQ4Tq3P7JxAA)

## Dataframe panels

Dataframe outputs in marimo come with several panels to help you visualize, explore, and page through your data interactively. These panels are accessible via toggles at the bottom-left of a dataframe output. If you need further control, after opening a panel you can

- **pin the panel** to the side of your editor for persistent access;
- **toggle focus** to automatically display the currently focused dataframe in the panel.

> **Note**
>
> Toggles are visible when editing notebooks (with `marimo edit ...`) but not when running notebooks as apps (with `marimo run ...`), except for the row viewer which is available in both.

### Row viewer panel

[Video: https://docs.marimo.io/_static/docs-row-viewer-panel.mp4](https://docs.marimo.io/_static/docs-row-viewer-panel.mp4)

To inspect individual rows, open the **row viewer**. This presents a vertical view of the selected row.

- **Press `Space`** to select/deselect the current row
- **Use arrow keys** (`←` `→`) to navigate between rows
- **Click** on any row in the dataframe to view its data in the panel

### Column explorer panel

[Video: https://docs.marimo.io/_static/docs-column-explorer-table.mp4](https://docs.marimo.io/_static/docs-column-explorer-table.mp4)

To explore your data, open the **column explorer** where you can find summary statistics and charts for each column. Click the `+` button to add the chart code to a new cell.

This requires the `altair` package to be installed. For large dataframes, `vegafusion` is also needed to render charts. To use the generated Python code, enable vegafusion in your notebook:

```python
import altair

altair.data_transformers.enable("vegafusion")
```

### Chart builder

The chart builder toggle lets you rapidly develop charts using a GUI, while also generating Python code to insert in your notebook. Refer to the [chart builder guide](https://docs.marimo.io/guides/working_with_data/plotting/#chart-builder) for more details.

## Preferences

When you run a SQL cell in marimo, you can get the output returned as a dataframe. If you have a preference for a specific dataframe library as a default you can configure the "default SQL output" in the user settings by going to the "Runtime" tab.

![](https://docs.marimo.io/_static/docs-dataframe-default-setting.png)

*Configure the default SQL output*

Alternatively you can also use the [marimo configuration file](https://docs.marimo.io/guides/configuration/#user-configuration) to configure the default SQL output.

```toml
[runtime]
default_sql_output = "native"
```

## Example notebook

For a comprehensive example of using Polars with marimo, check out our [Polars example notebook](https://github.com/marimo-team/marimo/blob/main/examples/third_party/polars/polars_example.py).

Run it with:

```bash
marimo edit https://raw.githubusercontent.com/marimo-team/marimo/main/examples/third_party/polars/polars_example.py
```