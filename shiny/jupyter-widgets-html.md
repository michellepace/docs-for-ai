Shiny fully supports [ipywidgets](https://ipywidgets.readthedocs.io/en/latest/) (aka Jupyter Widgets) via the [shinywidgets](https://github.com/posit-dev/py-shinywidgets) package. Many notable Python packages build on ipywidgets to provide highly interactive widgets in Jupyter notebooks, including:

- Plots, like [altair](https://altair-viz.github.io/), [bokeh](https://docs.bokeh.org/en/latest/index.html), and [plotly](https://plotly.com/python/).
- Maps, like [pydeck](https://deckgl.readthedocs.io/en/latest/index.html) and [ipyleaflet](https://ipyleaflet.readthedocs.io/en/latest/usage/index.html).
- Tables, [ipydatagrid](https://pypi.org/project/ipydatagrid) and [ipysheet](https://pypi.org/project/ipysheet).
- 3D visualizations, like [ipyvolume](https://pypi.org/project/ipyvolume) and [pythreejs](https://pypi.org/project/pythreejs).
- Media streaming, like [ipywebrtc](https://pypi.org/project/ipywebrtc).
- Other [awesome widgets](https://github.com/ml-tooling/best-of-jupyter#interactive-widgets--visualization)

In this article, we’ll learn how to leverage ipywidgets in Shiny, including how to [render](https://shiny.posit.co/py/docs/jupyter-widgets.html#get-started) them, [efficiently update](https://shiny.posit.co/py/docs/jupyter-widgets.html#efficient-updates) them, and [respond to user input](https://shiny.posit.co/py/docs/jupyter-widgets.html#user-input).

Not all Jupyter Widgets are ipywidgets

Although the term “Jupyter Widgets” is often used to refer to ipywidgets, it’s important to note that not all Jupyter Widgets are ipywidgets. For example, packages like [folium](https://python-visualization.github.io/folium/latest/) and [ipyvizzu](https://ipyvizzu.vizzuhq.com/latest/) aren’t compatible with ipywidgets, but do provide a [`_repr_html_` method](https://ipython.readthedocs.io/en/stable/config/integrating.html#rich-display) for getting the HTML representation. It may be possible to display these widgets using Shiny’s [`@render.ui`](https://shiny.posit.co/py/api/render.ui.html) decorator.

## Installation [Anchor](https://shiny.posit.co/py/docs/jupyter-widgets.html\#installation)

To use ipywidgets in Shiny, start by installing `shinywidgets`:

```
pip install shinywidgets
```

Then, install the ipywidgets that you’d like to use. For this article, we’ll need the following:

```
pip install altair bokeh plotly ipyleaflet pydeck==0.8.0
```

## Get started [Anchor](https://shiny.posit.co/py/docs/jupyter-widgets.html\#get-started)

To render an ipywidget you first define a reactive function that returns the widget and then decorate it with `@render_widget`. Some popular widgets like `altair` have specially-designed decorators for better ergonomics and we recommend using them if they exist.

Altair:

```python
from shiny.express import input, ui
from shinywidgets import render_altair

ui.input_selectize("var", "Select variable", choices=["bill_length_mm", "body_mass_g"])


@render_altair
def hist():
    import altair as alt
    from palmerpenguins import load_penguins
    df = load_penguins()
    return (
        alt.Chart(df)
        .mark_bar()
        .encode(x=alt.X(f"{input.var()}:Q", bin=True), y="count()")
    )
```

Requirements:

```text
altair
anywidget
palmerpenguins
```

Bokeh:

```python
from shiny.express import input, ui
from shinywidgets import render_bokeh

ui.input_selectize(
    "var", "Select variable",
    choices=["bill_length_mm", "body_mass_g"]
)

@render_bokeh
def hist():
    from bokeh.plotting import figure
    from palmerpenguins import load_penguins

    p = figure(x_axis_label=input.var(), y_axis_label="count")
    bins = load_penguins()[input.var()].value_counts().sort_index()
    p.quad(
        top=bins.values,
        bottom=0,
        left=bins.index - 0.5,
        right=bins.index + 0.5,
    )
    return p
```

Requirements:

```text
bokeh
jupyter_bokeh
xyzservices
```

Plotly:

```python
from shiny.express import input, ui
from shinywidgets import render_plotly

ui.input_selectize(
    "var", "Select variable",
    choices=["bill_length_mm", "body_mass_g"]
)

@render_plotly
def hist():
    import plotly.express as px
    from palmerpenguins import load_penguins
    df = load_penguins()
    return px.histogram(df, x=input.var())
```

Requirements:

```text
palmerpenguins
plotly
```

## Widget object [Anchor](https://shiny.posit.co/py/docs/jupyter-widgets.html\#widget-object)

In order to create rich user experiences like linked brushing, editable tables, and smooth transitions, it’s useful to know how to [efficiently update](https://shiny.posit.co/py/docs/jupyter-widgets.html#efficient-updates) and [respond to user input](https://shiny.posit.co/py/docs/jupyter-widgets.html#user-input). In either case, we’ll need access to the Python object underlying the rendered widget. This object is available as a property, named `widget`, on the render function. From this widget object, you can then access its attributes and methods. As we’ll see later, [special widget attributes](https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Basics.html#widget-properties) known as _traits_, can be used to [efficiently update](https://shiny.posit.co/py/docs/jupyter-widgets.html#efficient-updates) and [respond to user input](https://shiny.posit.co/py/docs/jupyter-widgets.html#user-input).

Discovering traits

If you’re not sure what traits are available, you can use the `widget.traits()` method to list them.

This `widget` object is always a subclass of `ipywidgets.Widget` and may be different from the object returned by the render function. For example, the `hist` function below returns `Figure`, but the `widget` property is a `FigureWidget` (a subclass of `ipywidgets.Widget`). In many cases, this is useful since `ipywidgets.Widget` provides a standard way to [efficiently update](https://shiny.posit.co/py/docs/jupyter-widgets.html#efficient-updates) and [respond to user input](https://shiny.posit.co/py/docs/jupyter-widgets.html#user-input) that shinywidgets knows how to handle. If you need the actual return value of the render function, you can access it via the `value` property.

app.py:

```python
from shiny.express import render
from shinywidgets import render_plotly

@render_plotly
def hist():
    import plotly.express as px
    return px.histogram(px.data.tips(), x="tip")

@render.code
def info():
    return str([type(hist.widget), type(hist.value)])
```

requirements:

```text
pandas
plotly
```

Typing & class coercion

The “main” API for notable packages like `altair`, `bokeh`, `plotly`, and `pydeck` don’t subclass `ipywidgets.Widget` (so that they can be used outside of a notebook). Shinywidgets is aware of this and automatically coerces to the relevant subclass (e.g, plotly’s `Figure` -\> `FigureWidget`).

As long as you’re using the dedicated decorators for these packages (e.g., `@render_altair`), the widget property’s type will know about the coercion (i.e., you’ll get proper autocomplete and type checking on the `widget` property).

## Efficient updates [Anchor](https://shiny.posit.co/py/docs/jupyter-widgets.html\#efficient-updates)

If you’ve used ipywidgets before, you may know that widgets have traits that can be updated after the widget is created. It’s often much more performant to update a widget’s traits instead of re-creating it from from scratch, and so you should update a widget’s traits when performance is critical.

For example, in a notebook, you may have written a code cell like this to first display a map:

```
import ipyleaflet as ipyl
map = ipyl.Map()
```

Then, in a later cell, you may have updated the map’s `center` trait to change the map’s location:

```
map.center = (51, 0)
```

With shinywidgets, we can do the same thing _reactively_ in Shiny by updating the `widget` property of the render function. For example, the following code creates a `map`, then updates the map’s center whenever the dropdown changes.

app.py:

```python
from shiny import reactive
from shiny.express import input, ui
from shinywidgets import render_widget
import ipyleaflet as ipyl

city_centers = {
    "London": (51.5074, 0.1278),
    "Paris": (48.8566, 2.3522),
    "New York": (40.7128, -74.0060)
}

ui.input_select("center", "Center", choices=list(city_centers.keys()))

@render_widget
def map():
    return ipyl.Map(zoom=4)

@reactive.effect
def _():
    map.widget.center = city_centers[input.center()]
```

requirements.txt:

```text
ipyleaflet
```

Re-render vs efficient update

If the app above had used `@render_widget` instead of `@reactive.effect` to perform the update, then the map would be re-rendered from stratch every time `input.center` changes, which causes the map to flicker (instead of a smooth transition to the new location).

## Respond to user input [Anchor](https://shiny.posit.co/py/docs/jupyter-widgets.html\#user-input)

There are two different ways to respond to user input:

1. [Reactive traits](https://shiny.posit.co/py/docs/jupyter-widgets.html#reactive-read)
2. [Widget event callbacks](https://shiny.posit.co/py/docs/jupyter-widgets.html#event-callbacks)

It’s usually easiest to use reactive traits but you may need to use event callbacks if the event information isn’t available as a trait.

### Reactive traits [Anchor](https://shiny.posit.co/py/docs/jupyter-widgets.html\#reactive-read)

If you’ve used ipywidgets before, you may know that widgets have traits that can be accessed and observed. For example, in a notebook, you may have written a code cell like this to display a map:

```
import ipyleaflet as ipyl
map = ipyl.Map()
```

Then, in a later cell, you may have read the map’s `center` trait to get the current map’s location:

```
map.center
```

With shinywidgets, we can do the same thing _reactively_ in Shiny by using the `reactive_read()` function to read the trait in a reactive context. For example, the following example creates a `map`, then displays/updates the map’s current center whenever the map is panned.

app.py:

```python
import ipyleaflet as ipyl
from shiny.express import render
from shinywidgets import reactive_read, render_widget

"Click and drag to pan the map"

@render_widget
def map():
    return ipyl.Map(zoom=2)

@render.text
def center():
    cntr = reactive_read(map.widget, 'center')
    return f"Current center: {cntr}"
```

requirements.txt:

```text
ipyleaflet
```

Observable traits

Under the hood, `reactive_read()` uses [ipywidgets’ `observe()` method](https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Events.html#traitlet-events) to observe changes to the relevant trait. So, any observable trait can be used with `reactive_read()`.

Some widgets have attributes that _contain_ observable traits. One practical example of this is the `selections` attribute of altair’s `JupyterChart` class, which has an [observable `point` trait](https://altair-viz.github.io/user_guide/interactions/jupyter_chart.html#point-selections).

app.py:

```python
import altair as alt
from shiny.express import render
from shinywidgets import reactive_read, render_altair
from vega_datasets import data

"Click the legend to update the selection"

@render.code
def selection():
    pt = reactive_read(jchart.widget.selections, "point")
    return str(pt)

@render_altair
def jchart():
    brush = alt.selection_point(name="point", encodings=["color"], bind="legend")
    return (
        alt.Chart(data.cars())
        .mark_point()
        .encode(
            x="Horsepower:Q",
            y="Miles_per_Gallon:Q",
            color=alt.condition(brush, "Origin:N", alt.value("grey")),
        )
        .add_params(brush)
    )


```

requirements.txt:

```text
altair
anywidget
vega_datasets
```

### Widget event callbacks [Anchor](https://shiny.posit.co/py/docs/jupyter-widgets.html\#event-callbacks)

Sometimes, you may want to capture user interaction that isn’t available through a widget trait. For example, `ipyleaflet.CircleMarker` has an `.on_click()` method that allows you to execute a callback when a marker is clicked. In this case, you’ll want to define a callback that updates some `reactive.value` everytime its triggered to capture the relevant information. That way, the callback information can be used to cause invalidation of other outputs (or trigger reactive side-effects):

app.py:

```python
import ipyleaflet as ipyl
from shiny.express import render
from shiny import reactive
from shinywidgets import render_widget

# Stores the number of clicks
n_clicks = reactive.value(0)

# A click callback that updates the reactive value
def on_click(**kwargs):
    n_clicks.set(n_clicks() + 1)

# Create the map, add the CircleMarker, and register the map with Shiny
@render_widget
def map():
    cm = ipyl.CircleMarker(location=(55, 360))
    cm.on_click(on_click)
    m = ipyl.Map(center=(53, 354), zoom=5)
    m.add_layer(cm)
    return m

@render.text
def nClicks():
    return f"Number of clicks: {n_clicks.get()}"
```

requirements.txt:

```text
ipyleaflet
```

Widgets can contain other widgets

In the example above, we created a `CircleMarker` object, then added it to a `Map` object. Both of these objects subclass `ipywidgets.Widget`, so they both have traits that can be updated and read reactively.

## Layout & styling [Anchor](https://shiny.posit.co/py/docs/jupyter-widgets.html\#layout-styling)

Layout and styling of ipywidgets can get a bit convoluted, partially due to potentially 3 levels of customization:

1. The [ipywidgets API](https://ipywidgets.readthedocs.io/en/7.6.3/examples/Widget%20Styling.html).
2. The widget implementation’s API (e.g., `altair`’s `Chart`, `plotly`’s `Figure`, etc).
3. Shiny’s UI layer.

Generally speaking, it’s preferable to use the widget’s layout API if it is available since the API is designed specifically for the widget. For example, if you want to set the size and theme of a plotly figure, can use its `update_layout` method:

app.py:

```python
import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly

ui.input_selectize(
    "theme", "Choose a theme",
    choices=["plotly", "plotly_white", "plotly_dark"]
)

@render_plotly
def plot():
    p = px.histogram(px.data.tips(), x="tip")
    p.update_layout(template=input.theme(), height=200)
    return p
```

requirements.txt:

```text
pandas
plotly
```

### Arranging widgets [Anchor](https://shiny.posit.co/py/docs/jupyter-widgets.html\#arranging-widgets)

The best way to include widgets in your application is to wrap them in one of Shiny’s UI components. In addition to being quite expressive and flexible, these components make it easy to implement filling and responsive layouts. For example, the following code arranges two widgets side-by-side, and fills the available space:

app.py:

```python
import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly

ui.page_opts(title = "Filling layout", fillable = True)

with ui.layout_columns():
  @render_plotly
  def plot1():
      return px.histogram(px.data.tips(), y="tip")

  @render_plotly
  def plot2():
      return px.histogram(px.data.tips(), y="total_bill")
      
```

requirements.txt:

```text
pandas
plotly
```

Layout gallery

For more layout inspiration, check out the [Layout Gallery](https://shiny.posit.co/py/layouts).

## Shinylive [Anchor](https://shiny.posit.co/py/docs/jupyter-widgets.html\#shinylive)

Examples on this page are powered by [shinylive](https://shiny.posit.co/py/get-started/shinylive.html), a tool for running Shiny apps in the browser (via [pyodide](https://pyodide.org/en/stable/)). Generally speaking, apps that use shinywidgets should work in shinylive as long as the widget and app code is supported by pyodide. The shinywidgets package itself comes pre-installed in shinylive, but you’ll need to include any other dependencies [in the `requirements.txt` file](https://shiny.posit.co/py/get-started/shinylive.html#requiring-extra-packages-with-requirements.txt).

## Examples [Anchor](https://shiny.posit.co/py/docs/jupyter-widgets.html\#examples)

For more shinywidgets examples, see the [`examples/` directory](https://github.com/posit-dev/py-shinywidgets/tree/main/examples) in the [shinywidgets repo](https://github.com/posit-dev/py-shinywidgets/). The [outputs](https://github.com/posit-dev/py-shinywidgets/tree/main/examples/outputs) example is a particularly useful example to see an overview of available widgets.

## Troubleshooting [Anchor](https://shiny.posit.co/py/docs/jupyter-widgets.html\#troubleshooting)

If after [installing](https://shiny.posit.co/py/docs/jupyter-widgets.html#installation)`shinywidgets`, you have trouble rendering widgets, first try running this “hello world” ipywidgets [example](https://github.com/rstudio/py-shinywidgets/blob/main/examples/ipywidgets/app.py). If that doesn’t work, it could be that you have an unsupported version of a dependency like `ipywidgets` or `shiny`.

If you can run the “hello world” example, but other widgets don’t work, first check that the extension is properly configured with `jupyter nbextension list`. If the extension is properly configured, and still isn’t working, here are some possible reasons why:

1. The widget requires initialization code to work in a notebook environment.

   - In this case, `shinywidgets` probably won’t work without providing the equivalent setup information to Shiny. A known case of this is bokeh, shinywidgets’ `@render_bokeh` decorator handles through inclusion of additional HTML [dependencies](https://github.com/posit-dev/py-shinywidgets/blob/9ea804c3/shinywidgets/_render_widget.py#L38-L42).

2. Not all widgets are compatible with ipywidgets!

   - Some web-based widgets in Python aren’t compatible with the ipywidgets framework, but do provide a `repr_html` method for getting the HTML representation (e.g., [folium](https://python-visualization.github.io/folium/latest/)). It may be possible to display these widgets using Shiny’s [`@render.ui`](https://shiny.posit.co/py/api/render.ui.html) decorator, but be aware that, you may not be able to do things mentioned in this article with these widgets.

3. The widget itself is broken.

   - If you think this is the case, try running the code in a notebook to see if it works there. If it doesn’t work in a notebook, then it’s likely a problem with the widget itself (and the issue should be reported to the widget’s maintainers).

4. The widget is otherwise misconfigured (or your offline).

   - `shinywidgets` tries its best to load widget dependencies from local files, but if it fails to do so, it will try to load them from a CDN. If you’re offline, then the CDN won’t work, and the widget will fail to load. If you’re online, and the widget still fails to load, then please let us know by [opening an issue](https://github.com/posit-dev/py-shinywidgets/issues/new).

## For developers [Anchor](https://shiny.posit.co/py/docs/jupyter-widgets.html\#for-developers)

If you’d like to create your own ipywidget that works with shinywidgets, we highly recommend using the [anywidget](https://anywidget.dev/) framework to develop that ipywidget. However, if only care about Shiny integration, and not Jupyter, then you may want to consider using a [custom Shiny binding](https://shiny.posit.co/py/docs/custom-component-one-off.html) instead of shinywidgets. If you happen to already have an ipywidget implementation, and want to use/add a dedicated decorator for it, see how it’s done [here](https://github.com/posit-dev/py-shinywidgets/blob/9ea804c3d/shinywidgets/_render_widget.py#L30-L48).
