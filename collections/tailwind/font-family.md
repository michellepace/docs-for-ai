# font-family

Utilities for controlling the font family of an element.

| Class | Styles |
| --- | --- |
| `font-sans` | `font-family: var(--font-sans); /* ui-sans-serif, system-ui, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji' */` |
| `font-serif` | `font-family: var(--font-serif); /* ui-serif, Georgia, Cambria, 'Times New Roman', Times, serif */` |
| `font-mono` | `font-family: var(--font-mono); /* ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace */` |
| `font-(family-name:<custom-property>)` | `font-family: var(<custom-property>);` |
| `font-[<value>]` | `font-family: <value>;` |

## [Examples](https://tailwindcss.com/docs/font-family\#examples)

### [Basic example](https://tailwindcss.com/docs/font-family\#basic-example)

Use utilities like `font-sans` and `font-mono` to set the font family of an element:

font-sans

The quick brown fox jumps over the lazy dog.

font-serif

The quick brown fox jumps over the lazy dog.

font-mono

The quick brown fox jumps over the lazy dog.

```html
<p class="font-sans ...">The quick brown fox ...</p><p class="font-serif ...">The quick brown fox ...</p><p class="font-mono ...">The quick brown fox ...</p>
```

### [Using a custom value](https://tailwindcss.com/docs/font-family\#using-a-custom-value)

Use the`font-[<value>]`syntaxto set the font family based on a completely custom value:

```html
<p class="font-[Open_Sans] ...">  Lorem ipsum dolor sit amet...</p>
```

For CSS variables, you can also use the`font-(family-name:<custom-property>)`syntax:

```html
<p class="font-(family-name:--my-font) ...">  Lorem ipsum dolor sit amet...</p>
```

This is just a shorthand for`font-[family-name:var(<custom-property>)]`that adds the `var()` function for you automatically.

### [Responsive design](https://tailwindcss.com/docs/font-family\#responsive-design)

Prefix a`font-family` utilitywith a breakpoint variant like `md:` to only apply the utility at mediumscreen sizes and above:

```html
<p class="font-sans md:font-serif ...">  Lorem ipsum dolor sit amet...</p>
```

Learn more about using variants in the [variants documentation](https://tailwindcss.com/docs/hover-focus-and-other-states).

## [Customizing your theme](https://tailwindcss.com/docs/font-family\#customizing-your-theme)

Use the `--font-*` theme variables to customize the font familyutilities in your project:

```css
@theme {  --font-display: "Oswald", sans-serif; }
```

Now the`font-display`utility can be used in your markup:

```html
<div class="font-display">  <!-- ... --></div>
```

You can also provide default `font-feature-settings` and `font-variation-settings` values for a font family:

```css
@theme {  --font-display: "Oswald", sans-serif;  --font-display--font-feature-settings: "cv02", "cv03", "cv04", "cv11";   --font-display--font-variation-settings: "opsz" 32; }
```

If needed, use the [@font-face](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face) at-rule to load custom fonts:

```css
@font-face {  font-family: Oswald;  font-style: normal;  font-weight: 200 700;  font-display: swap;  src: url("/fonts/Oswald.woff2") format("woff2");}
```

If you're loading a font from a service like [Google Fonts](https://fonts.google.com/), make sure to put the `@import` at the very top of your CSS file:

```css
@import url("https://fonts.googleapis.com/css2?family=Roboto&display=swap");@import "tailwindcss";@theme {  --font-roboto: "Roboto", sans-serif; }
```

Browsers require that `@import` statements come before any other rules, so URL imports need to be above imports like `@import "tailwindcss"` which are inlined in the compiled CSS.

Learn more about customizing your theme in the [theme documentation](https://tailwindcss.com/docs/theme#customizing-your-theme).

### On this page

- [Quick reference](https://tailwindcss.com/docs/font-family#quick-reference)
- [Examples](https://tailwindcss.com/docs/font-family#examples)
  - [Basic example](https://tailwindcss.com/docs/font-family#basic-example)
  - [Using a custom value](https://tailwindcss.com/docs/font-family#using-a-custom-value)
  - [Responsive design](https://tailwindcss.com/docs/font-family#responsive-design)
- [Customizing your theme](https://tailwindcss.com/docs/font-family#customizing-your-theme)
