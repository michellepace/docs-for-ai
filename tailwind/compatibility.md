[Home](https://tailwindcss.com/) v4.1

`⌘K`  `Ctrl K` [Docs](https://tailwindcss.com/docs) [Blog](https://tailwindcss.com/blog) [Showcase](https://tailwindcss.com/showcase) [Sponsor](https://tailwindcss.com/sponsor) [Plus](https://tailwindcss.com/plus?ref=top) [GitHub repository](https://github.com/tailwindlabs/tailwindcss)

1. Getting started
2. Compatibility

Getting started

# Compatibility

Learn about browser support and compatibility with other tooling.

## [Browser support](https://tailwindcss.com/docs/compatibility\#browser-support)

Tailwind CSS v4.0 is designed for and tested on modern browsers, and the core functionality of the framework specifically depends on these browser versions:

- **Chrome 111** _(released March 2023)_
- **Safari 16.4** _(released March 2023)_
- **Firefox 128** _(released July 2024)_

Tailwind also includes support for many bleeding-edge platform features like `field-sizing: content`, `@starting-style`, and `text-wrap: balance` that have limited browser support. It's up to you if you want to use these modern features in your projects — if the browsers you're targeting don't support them, simply don't use those utilities and variants.

If you're unsure about the support for a modern platform feature, the [Can I use](https://caniuse.com/mdn-css_at-rules_starting-style) database is a great resource.

## [Sass, Less, and Stylus](https://tailwindcss.com/docs/compatibility\#sass-less-and-stylus)

Tailwind CSS v4.0 is a full-featured CSS build tool designed for a specific workflow, and is not designed to be used with CSS preprocessors like Sass, Less, or Stylus.

**Think of Tailwind CSS itself as your preprocessor** — you shouldn't use Tailwind with Sass for the same reason you wouldn't use Sass with Stylus.

Since Tailwind is designed for modern browsers, you actually don't need a preprocessor for things like nesting or variables, and Tailwind itself will do things like bundle your imports and add vendor prefixes.

### [Build-time imports](https://tailwindcss.com/docs/compatibility\#build-time-imports)

Tailwind will automatically bundle other CSS files you include with `@import`, without the need for a separate preprocessing tool.

app.css

```
@import "tailwindcss";@import "./typography.css";
```

In this example, the `typography.css` file will be bundled into your compiled CSS for you by Tailwind, without any other tooling like Sass or `postcss-import`.

### [Variables](https://tailwindcss.com/docs/compatibility\#variables)

All modern browsers support [native CSS variables](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties) without the need for any sort of preprocessor:

typography.css

```
.typography {  font-size: var(--text-base);  color: var(--color-gray-700);}
```

Tailwind relies on CSS variables heavily internally, so if you can use Tailwind in your project, you can use native CSS variables.

### [Nesting](https://tailwindcss.com/docs/compatibility\#nesting)

Under the hood Tailwind uses [Lightning CSS](https://lightningcss.dev/) to process nested CSS like this:

typography.css

```
.typography {  p {    font-size: var(--text-base);  }  img {    border-radius: var(--radius-lg);  }}
```

Tailwind flattens that nested CSS for you so it can be understood by all modern browsers:

output.css

```
.typography p {  font-size: var(--text-base);}.typography img {  border-radius: var(--radius-lg);}
```

Native CSS nesting support is also very good these days, so you don't really need a preprocessor for nesting even if you aren't using Tailwind.

### [Loops](https://tailwindcss.com/docs/compatibility\#loops)

In Tailwind, the sorts of classes you may have used loops for in the past (like `col-span-1`, `col-span-2`, etc.) are generated for you on-demand by Tailwind whenever you use them instead of having to be predefined.

On top of that, when you're building things with Tailwind CSS, you do the vast majority of your styling in your HTML, not in CSS files. Since you're not writing tons of CSS in the first place, you just don't need features like loops that are designed for programmatically generating lots of custom CSS rules.

### [Color and math functions](https://tailwindcss.com/docs/compatibility\#color-and-math-functions)

When using preprocessors like Sass or Less, you may have used functions like `darken` or `lighten` to adjust colors.

When using Tailwind, the recommended workflow is to use a predefined color palette that includes light and dark shades of each color, like the expertly designed [default color palette](https://tailwindcss.com/docs/colors) included with the framework.

```
<button class="bg-indigo-500 hover:bg-indigo-600 ...">  <!-- ... --></button>
```

You can also use modern CSS features like [color-mix()](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/color-mix) to adjust colors at run-time directly in the browser. This even lets you adjust colors defined using CSS variables or the `currentcolor` keyword, which isn't possible with preprocessors.

Similarly, browsers support math functions like `min()`, `max()`, and `round()` natively now, so there's no need to rely on a preprocessor for these features anymore either.

## [CSS modules](https://tailwindcss.com/docs/compatibility\#css-modules)

Tailwind is compatible with CSS modules and can co-exist with them if you are introducing Tailwind into a project that already uses them, but **we don't recommend using CSS modules and Tailwind together** if you can avoid it.

### [Scoping concerns](https://tailwindcss.com/docs/compatibility\#scoping-concerns)

CSS modules are designed to solve scoping problems that just don't exist when composing utility classes in your HTML instead of writing custom CSS.

Styles are naturally scoped with Tailwind because each utility class always does the same thing, no matter where it's used — there's no risk that adding a utility class to one part of your UI creates some unexpected side effect somewhere else.

### [Performance](https://tailwindcss.com/docs/compatibility\#performance)

When using CSS modules, build tools like Vite, Parcel, and Turbopack process each CSS module separately. That means if you have 50 CSS modules in a project, **Tailwind needs to run 50 separate times**, which leads to much slower build times and a worse developer experience.

### [Explicit context sharing](https://tailwindcss.com/docs/compatibility\#explicit-context-sharing)

Since CSS modules are each processed separately, they have no `@theme` unless you import one.

This means features like `@apply` won't work the way you expect unless you explicitly import your global styles as reference:

Import your global styles as reference to make sure your theme variables are defined

Button.module.css

```
@reference "../app.css";button {  @apply bg-blue-500;}
```

Alternatively, you can also just use CSS variables instead of `@apply` which has the added benefit of letting Tailwind skip processing those files and will improve your build performance:

Button.module.css

```
button {  background: var(--color-blue-500);}
```

## [Vue, Svelte, and Astro](https://tailwindcss.com/docs/compatibility\#vue-svelte-and-astro)

Vue, Svelte, and Astro support `<style>` blocks in component files that behave very much like [CSS modules](https://tailwindcss.com/docs/compatibility#css-modules), which means they are each processed by your build tooling totally separately and have all of the same drawbacks.

If you're using Tailwind with these tools, **we recommend avoiding `<style>` blocks in your components** and just styling things with utility classes directly in your markup, the way Tailwind is meant to be used.

If you do use `<style>` blocks, make sure to import your global styles as reference if you want features like `@apply` to work as expected:

Import your global styles as reference to make sure your theme variables are
defined

Button.vue

```
<template>  <button><slot /></button></template><style scoped>  @reference "../app.css";  button {    @apply bg-blue-500;  }</style>
```

Or just use your globally defined CSS variables instead of features like `@apply`, which don't require Tailwind to process your component CSS at all:

Button.vue

```
<template>  <button><slot /></button></template><style scoped>  button {    background-color: var(--color-blue-500);  }</style>
```

### On this page

- [Browser support](https://tailwindcss.com/docs/compatibility#browser-support)
- [Sass, Less, and Stylus](https://tailwindcss.com/docs/compatibility#sass-less-and-stylus)
  - [Build-time imports](https://tailwindcss.com/docs/compatibility#build-time-imports)
  - [Variables](https://tailwindcss.com/docs/compatibility#variables)
  - [Nesting](https://tailwindcss.com/docs/compatibility#nesting)
  - [Loops](https://tailwindcss.com/docs/compatibility#loops)
  - [Color and math functions](https://tailwindcss.com/docs/compatibility#color-and-math-functions)
- [CSS modules](https://tailwindcss.com/docs/compatibility#css-modules)
  - [Scoping concerns](https://tailwindcss.com/docs/compatibility#scoping-concerns)
  - [Performance](https://tailwindcss.com/docs/compatibility#performance)
  - [Explicit context sharing](https://tailwindcss.com/docs/compatibility#explicit-context-sharing)
- [Vue, Svelte, and Astro](https://tailwindcss.com/docs/compatibility#vue-svelte-and-astro)

![Build UIs that don’t suck — 5-day mini-course](https://tailwindcss.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fcourse-promo.a67fd268.jpg&w=384&q=75)

5-day mini-course

Build UIs that don’t suck.

Short, tactical video lessons from the creator of Tailwind CSS, delivered directly to your inbox every day for a week.

[Get the free course →](https://tailwindcss.com/build-uis-that-dont-suck)

Copyright © 2025 Tailwind Labs Inc.· [Trademark Policy](https://tailwindcss.com/brand)