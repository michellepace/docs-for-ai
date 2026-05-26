Whether you’re a data scientist, analyst, or developer, Shiny makes it easy to [create](https://shiny.posit.co/py/get-started/create-run.html) rich, [interactive experiences](https://shiny.posit.co/py/docs/ui-overview.html) in pure Python with a fully [reactive framework](https://shiny.posit.co/py/docs/reactive-foundations.html). No need to learn JavaScript or front-end frameworks.

## Batteries included [Anchor](https://shiny.posit.co/py/get-started/what-is-shiny.html\#batteries-included)

Shiny for Python comes fully equipped with everything you need to build a dashboard right out of the box, including a rich set of [input](https://shiny.posit.co/py/components/#inputs) and [output](https://shiny.posit.co/py/components/#outputs) components. There is an entire [components gallery](https://shiny.posit.co/py/components/) to help you quickly build interactive applications.

[Layout options](https://shiny.posit.co/py/layouts/) let you organize your UI efficiently, while [built-in theming](https://shiny.posit.co/py/docs/ui-customize.html) (including [dark mode](https://shiny.posit.co/py/components/inputs/dark-mode)) ensures your app looks great with minimal effort.

Already have a brand guideline? You can use [brand.yml](https://posit-dev.github.io/brand-yml/) to apply consistent branding, colors, and logos across your application.

[Inputs](https://shiny.posit.co/py/components/#inputs)

[Outputs](https://shiny.posit.co/py/components/#outputs)

[Layouts](https://shiny.posit.co/py/layouts)

## Reactivity [Anchor](https://shiny.posit.co/py/get-started/what-is-shiny.html\#reactivity)

At the heart of Shiny is [reactivity](https://shiny.posit.co/py/docs/reactive-foundations.html), a system that automatically updates [outputs](https://shiny.posit.co/py/components/#outputs) when [inputs](https://shiny.posit.co/py/components/#inputs) change for seamless interactivity, without manually writing callbacks.

Shiny’s reactive engine avoids unnecessary computations by only re-calculating the outputs whose inputs have changed, making Shiny ideal for fast data-driven applications, enabling live updates for [charts, tables](https://shiny.posit.co/py/components/#outputs), and [reports](https://quarto.org/docs/interactive/shiny/) with minimal effort.

Below is a live Shiny application and its accompanying code. The first output text shows the square of the first slider value, and the second row of text shows the sum of _both_ slider values.

Try updating the sliders below and see how the text reacts. Also change what value gets returned on lines 11 or 17 and click the play button ▶️ for the app to refresh.

app.py+

99

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

from shiny import reactive

from shiny.express import ui, render, input

ui.input\_slider("s1", "Slider 1", min=0, max=10, value=5)

ui.input\_slider("s2", "Slider 2", min=0, max=100, value=50)

\# This output only reacts to the first slider

@render.text

defresult():

returnf"{input.s1()} squared is {input.s1() \*\* 2}."

\# This output reacts to both sliders

@render.text

defboth\_sliders\_output():

returnf"{input.s1()} \+ {input.s2()} is {input.s1() + input.s2()}."

## Jumpstart with templates [Anchor](https://shiny.posit.co/py/get-started/what-is-shiny.html\#templates)

Here’s a full Shiny application in action, complete with [reactivity](https://shiny.posit.co/py/docs/reactive-foundations.html) and a [user interface](https://shiny.posit.co/py/docs/ui-overview.html)!

### Please Wait

![loading](https://gallery.shinyapps.io/__static__/frontend/images/spinner.gif?v=ce6bcde20b2f6c562913c06be83f9e7c8a19b008017407a3094b76fa82bbd6b7f4048e032e07e534d4ab5442b9105294d612863735077ab13a47653a14c5866e)

Hit the ground running with one of our [starter templates](https://shiny.posit.co/py/templates/), like the app above, by using `shiny create`.

There are templates for common use cases. For example, [data dashboards](https://shiny.posit.co/py/get-started/templates/dashboard/), [data applications](https://shiny.posit.co/py/templates/database-explorer/), [streaming updates](https://shiny.posit.co/py/templates/monitor-database/), or [data entry](https://shiny.posit.co/py/templates/survey/).

Use the terminal command below to [create and run](https://shiny.posit.co/py/get-started/create-run.html) the same dashboard locally with `shiny create`, starting from a [template](https://shiny.posit.co/py/templates/).

```bash
shiny create --template dashboard
```

## Extensibility [Anchor](https://shiny.posit.co/py/get-started/what-is-shiny.html\#extensible)

While Shiny includes everything you need to build an app, it is also built on a foundation of web standards, making it highly [extensible](https://shiny.posit.co/py/docs/custom-component-one-off.html). Many of Shiny’s components are just plain HTML elements with the right classes to connect to Shiny’s client-side JavaScript.

Take the [action button](https://shiny.posit.co/py/components/inputs/action-button/), for example. You can print the input in the Python console to see that it’s just a regular HTML `<button>` element.

```python
>>> from shiny import ui
>>> ui.input_action_button("update_data", "Button")
```

```html
<button class="btn btn-default action-button" id="update_data" type="button">Button</button>
```

This means that you can use Shiny to learn web development—and [many people have](https://jnolis.com/talks/shiny_conf_2022/)!

But this also means that Shiny doesn’t lock you into a particular front-end framework. At the more advanced end of the spectrum, Shiny components can be highly sophisticated and can leverage modern web frameworks. For example, [Data Grids](https://shiny.posit.co/py/components/outputs/data-grid/) are React components that use the popular [TanStack Table](https://tanstack.com/table/latest) React library under the hood.

If you’re versed in web programming, you can use Shiny to build [one-off custom components](https://shiny.posit.co/py/docs/custom-component-one-off.html) that integrate your favorite JavaScript framework directly from Python. For more advanced needs, you can develop a [reusable component package](https://shiny.posit.co/py/docs/custom-components-pkg.html) or [customize the user interface](https://shiny.posit.co/py/docs/ui-customize.html) by incrementally [adding JavaScript](https://shiny.posit.co/py/docs/custom-component-one-off.html) or custom [HTML](https://shiny.posit.co/py/docs/ui-html.html) or [CSS](https://shiny.posit.co/py/docs/ui-customize.html).

## Install, create, and run [Anchor](https://shiny.posit.co/py/get-started/what-is-shiny.html\#install-create-and-run)

Now that you know a little more about Shiny for Python, let’s go [install Shiny](https://shiny.posit.co/py/get-started/install.html) so you can [create your first application](https://shiny.posit.co/py/get-started/create-run.html)!
