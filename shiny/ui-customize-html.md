This article covers various levels of ways of customizing the overall look and feel of your Shiny app.

Customizing components

The techniques covered here are intentionally generic (i.e., applies to all UI). Some components may have additional customization options (e.g., `ui.sidebar()` has a `bg` argument to change the background color).

## Shinyswatch [Anchor](https://shiny.posit.co/py/docs/ui-customize.html\#shinyswatch)

The [shinyswatch](https://github.com/posit-dev/py-shinyswatch) package makes is very easy to change the look of your app, and provides over a dozen different [bootswatch](https://bootswatch.com/) themes to choose from. Simply choose a theme from `shinyswatch.theme.<theme_name>` and pass it to the `theme` argument of the page function (Shiny Core) or `ui.page_opts()` (Shiny Express).

app.py:

```python
from shinyswatch import theme
from shiny.express import render, ui

ui.page_opts(title="Hello shinyswatch theme", theme=theme.darkly)

with ui.sidebar():
    "Sidebar content"

"Main content"
```

requirements.txt:

```text
shinyswatch
```

## Custom CSS [Anchor](https://shiny.posit.co/py/docs/ui-customize.html\#custom-css)

If you want to customize the look of your app beyond what is available in shinyswatch, a natural next step is to add custom CSS. This is pretty straightforward to do since [UI components are HTML](https://shiny.posit.co/py/docs/ui-html.html). That said, you’ll at least want to know the basics of CSS, including [CSS selectors](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Selectors) before you get started.

### CSS string [Anchor](https://shiny.posit.co/py/docs/ui-customize.html\#css-string)

If you don’t need much CSS, you can add a string of CSS directly to your UI with `ui.tags.style()`. This is convenient because you don’t need to create an external file, but it can be a bit cumbersome if you have a lot of CSS.

app.py:

```python
from shiny.express import ui

ui.tags.style(
    ".card-header { color:white; background:#2A2A2A !important; }"
)

with ui.card():
    ui.card_header("Card header")
    "Card body"
```

### CSS file [Anchor](https://shiny.posit.co/py/docs/ui-customize.html\#css-file)

If you have a lot of CSS, put it in an external file and import it with `ui.include_css()`.

app.py:

```python
from shiny.express import ui

ui.tags.style(
    ".card-header { color:white; background:#2A2A2A !important; }"
)

with ui.card():
    ui.card_header("Card header")
    "Card body"
```

### Inline styles [Anchor](https://shiny.posit.co/py/docs/ui-customize.html\#inline-styles)

Most UI components provide the opportunity to add an inline style (i.e., CSS that is applied directly to the element). This approach may be preferrable to an external CSS file if you only need to apply the style to one element, or if you want to apply style(s) programatically.

app.py:

```python
from shiny.express import ui

with ui.card():
    ui.card_header("Card header", style="color:white; background:#2A2A2A !important;")
    "Card body"
```

### Utility classes [Anchor](https://shiny.posit.co/py/docs/ui-customize.html\#utility-classes)

Since Shiny provides Bootstrap by default, you can use [Bootstrap utility classes](https://getbootstrap.com/docs/5.3/utilities/colors/) to customize your app. For example, you can `bg-primary` to change the background color, and `lead` to change the font weight. In addition to colors and fonts, utility classes are super useful for things like spacing, alignment, and borders.

Note this approach is similar to inline styles (i.e., per element styling), but has the advantage of abstracting the actual styling away from the element itself, which is especially useful when used in conjunction with [CSS variables](https://shiny.posit.co/py/docs/ui-customize.html#css-variables).

app.py:

```python
from shiny.express import ui

with ui.card():
    ui.card_header("Card header", class_="bg-primary-subtle lead")
    "Card body"
```

### CSS Variables [Anchor](https://shiny.posit.co/py/docs/ui-customize.html\#css-variables)

Bootstrap’s [CSS variables](https://getbootstrap.com/docs/5.3/customize/css-variables/) provide another nice entry point to customizing your app, especially if you want to make sweeping changes to Bootstrap’s default styles. For example, you can change the primary color by setting the `--bs-primary-rgb` variable.

app.py:

```python
from shiny.express import ui

ui.tags.style(":root { --bs-primary-rgb: 113,46,246; }")

with ui.card():
    ui.card_header("Card header", class_="bg-primary lead"),
    "Card body"
```

Bootstrap CSS variables

To learn more about Bootstrap’s CSS variables, check out the [Bootstrap docs](https://getbootstrap.com/docs/5.3/customize/css-variables/).

### Fonts [Anchor](https://shiny.posit.co/py/docs/ui-customize.html\#fonts)

When using a custom font, its good practice to import the relevant font files into your app. This is because the font may not be available on the user’s computer, and importing the font files ensures that the font will be available to the user. One way to import font files is to import them from a service like [Google Fonts](https://fonts.google.com/).

app.py:

```python
from shiny.express import ui

ui.tags.link(
    rel="stylesheet",
    href="https://fonts.googleapis.com/css?family=Roboto"
)

ui.tags.style(
    "body { font-family: 'Roboto', sans-serif; }"
)

with ui.card():
    ui.card_header("Card header")
    "Card body"
```

That said, if you want your app to work properly offline, you’ll want to serve the font files with the app, which is covered next.

## Serve local files [Anchor](https://shiny.posit.co/py/docs/ui-customize.html\#serve-local-files)

When customizing UI with CSS (and/or JavaScript), it’s often useful to serve local files (e.g., fonts, images, CSS, etc) to the app. This can be done by providing a value for `static_assets`; the syntax for doing this is slightly different for Core and Express apps.

Express - app.py

```python
from shiny.express import ui

ui.tags.link(href="my-styles.css", rel="stylesheet")

with ui.card():
    ui.card_header("Card header")
    "Card body"
```

Express - my-styles.css

```css
.card-header {
    color: white;
    background: #2A2A2A !important;
}
```

In Shiny Express, if you have a subdirectory named `www`, the contents of that directory will automatically be available to the application’s UI at `/`.

## Distribute styles [Anchor](https://shiny.posit.co/py/docs/ui-customize.html\#distribute-styles)

The `HTMLDependency` class (from [htmltools](https://github.com/posit-dev/py-htmltools/)) provides a useful mechanism to distribute custom styles and other files, especially when the CSS/JS should be loaded only once. A useful pattern to make those assets more accessible to others is to export a function from your Python package which returns an `HTMLDependency` object (this is essentially what [shinyswatch](https://shiny.posit.co/py/docs/ui-customize.html#shinyswatch) does). This way, after a user installs your package, they will be able to call this function anywhere in their UI code to insert the theme.

```
from htmltools import HTMLDependency

def acme_theme():
    return HTMLDependency(
        name="acme_theme",
        version="0.01",
        source={"package": "acme_theme", "subdir": "acme-theme"},
        stylesheet=[{"href": "acme-theme.css"}],
        script=[{"src": "acme-theme.js"}],
        # If you want other files in the acme-theme dir to be served
        all_files=True
    )
```

Custom components

If you’re interested in creating [custom Shiny bindings](https://shiny.posit.co/py/docs/custom-component-one-off.html), you’ll learn more about using this mechanism to attach CSS/JS to your custom component.

Minified assets

If your CSS/JS assets are large, you may want to [minify](https://www.minifier.org/) them to improve app performance.
