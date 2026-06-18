<!-- Source: https://docs.marimo.io/guides/working_with_data/plotting/ -->

# Plotting

marimo supports most major plotting libraries, including Matplotlib, Seaborn,
Plotly, Altair, and HoloViews. Just import your plotting library of choice and
use it as you normally would.

For matplotlib, Altair, and Plotly plots, marimo does something special: wrap
your plot in [`mo.ui.matplotlib`](https://docs.marimo.io/api/plotting/#marimo.ui.matplotlib),
[`mo.ui.altair_chart`](https://docs.marimo.io/api/plotting/#marimo.ui.altair_chart) or
[`mo.ui.plotly`](https://docs.marimo.io/api/plotting/#marimo.ui.plotly), then select and filter with your mouse —
marimo automatically sends the selected data back to Python!

> For a video overview of reactive plots, check out our [YouTube tutorial](https://youtu.be/KFXsm1wr408).

## Reactive plots! ⚡

> **Requirements**
>
> Reactive plots currently require matplotlib, Altair, or Plotly. Matplotlib
> supports box and lasso selections (best suited for scatter plots);
> selections in Plotly are limited to scatter/scattergl plots, bar charts,
> histograms, heatmaps, treemaps, and sunburst charts; Altair supports a larger class
> of plots for selections.

### matplotlib

Use [`mo.ui.matplotlib`](https://docs.marimo.io/api/plotting/#marimo.ui.matplotlib) to make matplotlib plots
**reactive**: select data on the frontend, then use the selection to filter
your data in Python.

Two selection modes are supported:

- **Box selection** — click and drag to draw a rectangular region.
- **Lasso selection** — hold `Shift` and drag to draw a freehand
  polygon.

After selecting, use `fig.value.get_mask(x, y)` to get a boolean mask of the
points inside the selection. When nothing is selected, `fig.value` is falsy and
`get_mask()` returns an all-`False` array.

#### Example

**code:**

```python
import matplotlib.pyplot as plt
import marimo as mo
import numpy as np

x = np.random.randn(500)
y = np.random.randn(500)
plt.scatter(x, y)
# Wrap the Axes in mo.ui.matplotlib to make them reactive ⚡
ax = mo.ui.matplotlib(plt.gca())
ax
```

```python
# In another cell — filter your data using the selection
mask = ax.value.get_mask(x, y)
selected_x, selected_y = x[mask], y[mask]
```

**live example:**

[Interactive marimo example](https://marimo.app/?embed=true&mode=edit&show-chrome=false#code/JYWwDg9gTgLgBCAhlUEBQixjgXgc1AOgEEsAKAd2ABMYALHAIhAFNrgBXERgSjTQACmMIQDGLADYS01FgDM4AfUVkeALjRwtcUJFj4UICHEQBnBOm1woLGBygA7QcLGTpshctUaru6PCQYMAkIGAlgACNCMABPYNCTc2CYTW0-fQcuWMS4BzB+KwAPXFyRKEQHaggQQnLKhzIAVgAGZr4rGJK82oqqmrrqBpa21K1kwlNRRBgYFigyQoAaOBj27URivCNCDmBCQPiwyLJxgHMp1TWtDdHrW3snZyxXKRl5JRV1W6RTAGsSjaEABuiAkHBYhFOtkUP1+C2Wq1u3VEEDBIAcilMMEQojhAG1CnjYQBdBFEsy-YnEq53OyONBAA)

#### Debouncing

By default, the selection streams to Python as you drag. For expensive
downstream computations or very large datasets, pass `debounce=True` so the
value is only sent on mouse-up:

```python
ax = mo.ui.matplotlib(plt.gca(), debounce=True)
```

#### Selection types

`ax.value` is one of three types:

| Type | When | Attributes |
| --- | --- | --- |
| `EmptySelection` | Nothing selected (falsy) | — |
| `BoxSelection` | Box drag | `x_min`, `x_max`, `y_min`, `y_max` |
| `LassoSelection` | `Shift`+drag | `vertices` (tuple of `(x, y)` pairs) |

All three have a `get_mask(x, y)` method that returns a boolean NumPy array,
so you can always write:

```python
mask = ax.value.get_mask(x, y)
```

### Altair

[Interactive marimo example](https://marimo.app/?embed=true&mode=edit&show-chrome=false#code/JYWwDg9gTgLgBCAhlUEBQixjgXgc1AOgEEsAKAd2ABMYALHAIhAFNrgBXERgSjTQACmMIQDGLADYS01FgDM4AfUVkeALjRwtcUJFj4UICHEQBnBOm1woLGBygA7QcLGTpZgJ4PRcWQuWqGla60PCIEjCIwFAm5uEwmtoh+mCIDtRmsXBg1IlayfAAVqYQTlY2do78QliuUjLySirqeXCiyOZ4OYQ2iNSKxaVkAOR0MDBgpmoA9NMAbiwA5oiEi8D0HABGhMAQ80uIALQZkaa2ptMniNPtUKaEgw7DfK2idMjweEaEHMCE8VEoIo3h8yPFCABhd6wMi3Uw8QhIKAAa0UkGADhgqkILG8EFkZFaVgAHjhhgAJaBnSAUFhQYYAGiJ2g8ZIAssAJCxTGi6YoAOLhCSlRnMrSiCDCqBkgDyKDWT1aPD45Vs9iczlq4nqfiagVa3zmpkiomRZAA2iDYAyLD8-pFNlzYdCYIQ5uEOCweABdFXaCrqtBAA)

Use [`mo.ui.altair_chart`](https://docs.marimo.io/api/plotting/#marimo.ui.altair_chart) to easily
create interactive, selectable plots: *selections you make on the frontend are
automatically made available as Pandas dataframes in Python.*

[Video: https://docs.marimo.io/_static/docs-intro.mp4](https://docs.marimo.io/_static/docs-intro.mp4)

Wrap an Altair chart in [`mo.ui.altair_chart`](https://docs.marimo.io/api/plotting/#marimo.ui.altair_chart)
to make it **reactive**: select data on the frontend, access it via the chart's
`value` attribute (`chart.value`).

#### Disabling automatic selection

marimo automatically adds a default selection based on the mark type, however, you may want to customize the selection behavior of your Altair chart. You can do this by setting `chart_selection` and `legend_selection` to `False`, and using `.add_params` directly on your Altair chart.

```python
# Create an interval selection
brush = alt.selection_interval(encodings=["x"])

_chart = (
    alt.Chart(traces, height=150)
    .mark_line()
    .encode(x="index:Q", y="value:Q", color="traces:N")
    .add_params(brush) # add the selection to the chart
)

chart = mo.ui.altair_chart(
    _chart,
    # disable automatic selection
    chart_selection=False,
    legend_selection=False
)
chart # You can now access chart.value to get the selected data
```

*Reactive plots are just one way that marimo **makes your data tangible**.*

#### Example

```python
import marimo as mo
import altair as alt
import vega_datasets

# Load some data
cars = vega_datasets.data.cars()

# Create an Altair chart
chart = alt.Chart(cars).mark_point().encode(
    x='Horsepower', # Encoding along the x-axis
    y='Miles_per_Gallon', # Encoding along the y-axis
    color='Origin', # Category encoding by color
)

# Make it reactive ⚡
chart = mo.ui.altair_chart(chart)
```

```python
# In a new cell, display the chart and its data filtered by the selection
mo.vstack([chart, chart.value.head()])
```

#### Learning Altair

If you're new to **Altair**, we highly recommend exploring the
[Altair documentation](https://altair-viz.github.io/). Altair provides
a declarative, concise, and simple way to create highly interactive and
sophisticated plots.

Altair is based on [Vega-Lite](https://vega.github.io/vega-lite/), an
exceptional tool for creating interactive charts that serves as the backbone
for marimo's reactive charting capabilities.

##### Concepts

> **Learn by doing? Skip this section!**
>
> This section summarizes the main concepts used by Altair (and Vega-Lite).
> Feel free to skip this section and return later.

Our choice to use the Vega-Lite specification was driven by its robust data
model, which is well-suited for data analysis. Some key concepts are summarized
below. (For a more detailed explanation, with examples, we recommend the
[Basic Statistical Visualization](https://altair-viz.github.io/getting_started/starting.html)
tutorial from Altair.)

- **Data Source**: This is the information that will be visualized in the
  chart. It can be provided in various formats such as a dataframe, a list of
  dictionaries, or a URL pointing to the data source.
- **Mark Type**: This refers to the visual representation used for each data
  point on the chart. The options include 'bar', 'dot', 'circle', 'area', and
  'line'. Each mark type offers a different way to visualize and interpret the
  data.
- **Encoding**: This is the process of mapping various aspects or dimensions of
  the data to visual characteristics of the marks. Encodings can be of
  different types:
- **Positional Encodings**: These are encodings like 'x' and 'y' that
  determine the position of the marks in the chart.
- **Categorical Encodings**: These are encodings like 'color' and 'shape' that
  categorize data points. They are typically represented in a legend for easy
  reference.
- **Transformations**: These are operations that can be applied to the data
  before it is visualized, for example, filtering and aggregation. These
  transformations allow for more complex and nuanced visualizations.

**Automatically interactive.**
marimo adds interactivity automatically, based on the mark used and the
encodings. For example, if you use a `mark_point` and an `x` encoding, marimo
will automatically add a brush selection to the chart. If you add a `color`
encoding, marimo will add a legend and a click selection.

#### Automatic Selections

By default [`mo.ui.altair_chart`](https://docs.marimo.io/api/plotting/#marimo.ui.altair_chart)
will make the chart and legend selectable. Depending on the mark type, the
chart will either have a `point` or `interval` ("brush") selection. When using
non-positional encodings (color, size, etc),
[`mo.ui.altair_chart`](https://docs.marimo.io/api/plotting/#marimo.ui.altair_chart) will also
make the legend selectable.

Selection configurable through `*_selection` params in
[`mo.ui.altair_chart`](https://docs.marimo.io/api/plotting/#marimo.ui.altair_chart). See the [API
docs](https://docs.marimo.io/api/plotting/#marimo.ui.altair_chart) for details.

> **Note**
>
> You may still add your own selection parameters via Altair or Vega-Lite.
> marimo will not override your selections.

#### Altair transformations

Altair supports a variety of transformations, such as filtering, aggregation, and sorting. These transformations can be used to create more complex and nuanced visualizations. For example, you can use a filter to show only the points that meet a certain condition, or use an aggregation to show the average value of a variable.

In order for marimo's reactive plots to work with transformations, you must install `vegafusion`, as this feature uses `chart.transformed_data` (which requires version 1.4.0 or greater of the `vegafusion` packages).

```bash
# These can be installed with pip using:
pip install "vegafusion[embed]>=1.4.0"
# Or with conda using:
conda install -c conda-forge "vegafusion-python-embed>=1.4.0" "vegafusion>=1.4.0"
```

### Plotly

> **Supported charts**
>
> marimo can render any Plotly plot, but [`mo.ui.plotly`](https://docs.marimo.io/api/plotting/#marimo.ui.plotly) only
> supports reactive selections for scatter/scattergl plots, bar charts,
> histograms, heatmaps, treemaps, and sunburst charts. If you require other kinds of
> selection, please [file an issue](https://github.com/marimo-team/marimo/issues).

[Interactive marimo example](https://marimo.app/?embed=true&mode=edit&show-chrome=false#code/JYWwDg9gTgLgBCAhlUEBQixjgXgc1AOgEEsAKAd2ABMYALHAIhAFNrgBXERgSjTQACmMIQDGLADYS01FgDM4AfUVkeALjRwtcUJFj4UICHEQBnBOm1woLGBygA7QcLGSJZOjRaLREWTgAVKA4WPjMATwdROFkFZVUNK11oeBBgUSgIMGAwTW1ECkRgVPTM7JFgB1MYRCkyAG1GMAkIGAlw+pYADzAbU1MAXUYAGjgmxAdqM0YBviTwFLhm1vbCbt6WfpNzMC68rRs7RyWu4f5nLFcpGXklFV31faWW+DwjQg5gQmW28LInrS7QimUSIGAwFhQMhdHD1AAMowAjKMACyjACcSIAbANRuFYQi4Mi4AAmUYAZlRuLgVFoDCxcMJdBYwAA5nQYDhyYy5tpeYCXk9DvYHM9WuchJdxNdYncyD9HlYfoQAG61EJC2witBAA)

Use [`mo.ui.plotly`](https://docs.marimo.io/api/plotting/#marimo.ui.plotly) to create
selectable Plotly plots whose values are sent back to Python on selection.

## matplotlib

To output a matplotlib plot in a cell's output area, include its `Axes` or
`Figure` object as the last expression in your notebook. For example:

```python
plt.plot([1, 2])
# plt.gca() gets the current `Axes`
plt.gca()
```

or

```python
fig, ax = plt.subplots()

ax.plot([1, 2])
ax
```

If you want to output the plot in the console area, use `plt.show()` or
`fig.show()`.

### Interactive plots with pan and zoom

To make matplotlib plots interactive with pan and zoom, use
[mo.mpl.interactive](https://docs.marimo.io/api/plotting/#marimo.mpl.interactive). This does not support reactive selection.

## Chart builder

marimo comes with a built-in chart builder that makes it easy to create plots specialized to your dataframes with just a few clicks. As you make your charts, marimo generates Python code that you can add to your notebook to save them.

You can toggle the chart builder with a button at the bottom-left of a dataframe output. This provides a GUI interface to create many kinds of plots, while also generating Python code.

[Video: https://docs.marimo.io/_static/docs-chart-builder-table.mp4](https://docs.marimo.io/_static/docs-chart-builder-table.mp4)

Charts are powered by [Vega-Lite](https://vega.github.io/vega-lite/). To save a chart, click the `+` button in the `Python code` tab to add the code to a new cell.

> **Note**
>
> This feature is in active development. Please report any issues or feedback [here](https://github.com/marimo-team/marimo/issues).