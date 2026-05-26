Create efficient, reactive, and robust web applications and dashboards.

```python
from palmerpenguins import load_penguins
from plotnine import aes, geom_histogram, ggplot, theme_minimal
from shiny.express import input, render, ui

dat = load_penguins()
species = dat["species"].unique().tolist()

ui.input_radio_buttons("species", "Species", species, inline=True)

@render.plot(height=300)
def plot():
    sel = dat[dat["species"] == input.species()]
    return (
        ggplot(aes(x="bill_length_mm"))
        + geom_histogram(dat, fill="#C2C2C4", binwidth=1)
        + geom_histogram(sel, fill="#447099", binwidth=1)
        + theme_minimal()
    )
```

## Why Shiny? [Anchor](https://shiny.posit.co/py/get-started/\#why-shiny)

Shiny for Python empowers you to bring your data to life with interactive applications that are easy to build, customize, and share.

- **Pure Python – no JS required**

Create sophisticated web apps in pure Python, using libraries you already know and love. Get started now by [trying Shiny in your browser](https://shinylive.io/py/examples/), asking [Shiny Assistant](https://shiny.posit.co/blog/posts/shiny-assistant/) to build you an app, or develop locally by [installing](https://shiny.posit.co/py/get-started/install.html) and [running](https://shiny.posit.co/py/get-started/create-run.html) a starter [template](https://shiny.posit.co/py/templates/).

- **Batteries Included**

Build delightful user interfaces using an extensive library of simple yet composable [components](https://shiny.posit.co/py/components/) and [layouts](https://shiny.posit.co/py/layouts/). As your app grows, you’ll also appreciate advanced features like [modules](https://shiny.posit.co/py/docs/modules.html), [theming](https://shiny.posit.co/py/docs/ui-customize.html), [non-blocking tasks](https://shiny.posit.co/py/docs/nonblocking.html), [bookmarking](https://shiny.posit.co/blog/posts/shiny-python-1.4/), and more.

- **Ready for AI**

Quickly build [beautiful AI apps](https://shiny.posit.co/py/docs/genai-inspiration.html) like [chatbots](https://shiny.posit.co/py/docs/genai-chatbots.html) and other [streaming](https://shiny.posit.co/py/docs/genai-stream.html) interfaces.

- **Efficiently scalable**

[Reactivity](https://shiny.posit.co/py/docs/reactive-foundations.html) enables Shiny to perform minimal updates, allowing you to develop sophisticated apps without the hassle of state management.

- **From demo to production-ready**

Shiny is great for one-off apps that help you [demo a concept](https://shinylive.io/py/app/#orbit-simulation) or quickly [see your data](https://gallery.shinyapps.io/superzip/). But Shiny apps aren’t toy apps–Shiny’s powerful [reactive framework](https://shiny.posit.co/py/docs/reactive-foundations.html) and [extensible components](https://shiny.posit.co/py/docs/custom-component-one-off.html) mean your applications can evolve alongside your needs. Start simple, then [customize and scale](https://gallery.shinyapps.io/aws-community-builders-dashboard/) without switching frameworks.

- **Plays well with others**

Bring to life the Python packages you know and love with Shiny. Turn polars and pandas data frames into [dynamic data grids](https://shiny.posit.co/py/components/outputs/data-grid/). Breathe interactivity into any [matplotlib](https://shiny.posit.co/py/components/outputs/plot-matplotlib/) or [seaborn](https://shiny.posit.co/py/components/outputs/plot-seaborn/) plot. Go further and build an app around sophisticated displays from [altair](https://shiny.posit.co/py/docs/jupyter-widgets.html), [plotly](https://shiny.posit.co/py/components/outputs/plot-plotly/), or any [Jupyter Widget](https://shiny.posit.co/py/docs/jupyter-widgets.html).

- **Deploy with confidence**

When it’s time to put your Shiny app on the web, you can choose to deploy [on your own servers](https://shiny.posit.co/py/get-started/deploy-on-prem.html), on our [hosting services](https://shiny.posit.co/py/get-started/deploy-cloud.html), or even [serverless with shinylive](https://shiny.posit.co/py/get-started/shinylive.html).

- **Open source**

Inspect, adapt, contribute, or join the [forum](https://forum.posit.co/c/shiny) or [discord](https://discord.com/invite/yMGCamUMnS) community! You can check out the [code](https://github.com/posit-dev/py-shiny/) or make your own [extensions](https://shiny.posit.co/py/docs/custom-component-one-off.html).


Ready to dive deeper? [Learn more about what makes Shiny unique](https://shiny.posit.co/py/get-started/what-is-shiny.html).

## Gallery and templates [Anchor](https://shiny.posit.co/py/get-started/\#gallery-and-templates)

Check out the [Shiny Gallery](https://shiny.posit.co/py/gallery/) for inspiration. Or kick start a new project with one of our [starter templates](https://shiny.posit.co/py/templates/).

[**Superzip explorer**](https://gallery.shinyapps.io/superzip/)

[View app](https://gallery.shinyapps.io/superzip/)

[View source](https://github.com/posit-dev/py-shinywidgets/tree/main/examples/superzip/ "View source code")

[**Restaurant tips dashboard**](https://gallery.shinyapps.io/template-dashboard-tips1/)

[View app](https://gallery.shinyapps.io/template-dashboard-tips1/)

[View source](https://shiny.posit.co/py/templates/dashboard-tips/ "View source code")

[**Stock prices**](https://gallery.shinyapps.io/template-stock-app/)

[View app](https://gallery.shinyapps.io/template-stock-app/)

[View source](https://shiny.posit.co/py/templates/stock-app/ "View source code")

[**Respiratory Disease data**](https://gallery.shinyapps.io/respiratory_disease_pyshiny/)

[View app](https://gallery.shinyapps.io/respiratory_disease_pyshiny/)

[View source](https://github.com/rstudio/shiny-gallery/tree/master/respiratory_disease_pyshiny "View source code")

[**AWS Community Builders Dashboard**](https://gallery.shinyapps.io/aws-community-builders-dashboard/)

[View app](https://gallery.shinyapps.io/aws-community-builders-dashboard/)

[View source](https://github.com/robertgv/aws-community-builders-dashboard "View source code")

[**Identify Outliers**](https://connect.posit.cloud/skaltman/content/01922aab-06e0-fc8f-8958-30dd67f9af51)

[View app](https://connect.posit.cloud/skaltman/content/01922aab-06e0-fc8f-8958-30dd67f9af51)

[View source](https://github.com/skaltman/outliers-app-db-python "View source code")

No matching items

## Take Shiny for a spin [Anchor](https://shiny.posit.co/py/get-started/\#take-shiny-for-a-spin)

The next pages in this guide will help you [install shiny](https://shiny.posit.co/py/get-started/install.html), [create and run](https://shiny.posit.co/py/get-started/create-run.html) your first application, help you find [troubleshooting help](https://shiny.posit.co/py/get-started/debug.html), and [deploy your app](https://shiny.posit.co/py/get-started/deploy.html) to the web ( [for free](https://shiny.posit.co/py/get-started/deploy-cloud.html)).

Or skip installation and [try the shinylive playground in the browser](https://shinylive.io/py/examples/)!

Have a question? Join our community on our [Discord server](https://discord.com/invite/yMGCamUMnS)!