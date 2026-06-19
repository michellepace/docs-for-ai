# Tailwind CSS v4.0 - January 22, 2025

Tailwind CSS v4.0 is an all-new version of the framework, with a reimagined configuration and customisation experience, taking full advantage of the latest advancements the web platform has to offer.

## Key Features

- **New high-performance engine** — full builds up to 5x faster, incremental builds over 100x faster, measured in microseconds.
- **Designed for the modern web** — built on cascade layers, registered custom properties with `@property`, and `color-mix()`.
- **Simplified installation** — fewer dependencies, zero configuration, single line of CSS.
- **First-party Vite plugin** — tight integration for maximum performance and minimum configuration.
- **Automatic content detection** — template files discovered automatically, no configuration required.
- **Built-in import support** — no additional tooling to bundle multiple CSS files.
- **CSS-first configuration** — customise and extend the framework directly in CSS instead of JavaScript.
- **CSS theme variables** — design tokens exposed as native CSS variables.
- **Dynamic utility values and variants** — no configuration needed for spacing scale values or basic data attributes.
- **Modernised P3 colour palette** — redesigned, more vivid colours using wider gamut.
- **Container queries** — first-class APIs for styling based on container size, no plugins required.
- **New 3D transform utilities** — transform elements in 3D space directly in HTML.
- **Expanded gradient APIs** — radial and conic gradients, interpolation modes, and more.
- **@starting-style support** — create enter and exit transitions without JavaScript.
- **not-\* variant** — style elements only when they don't match another variant, selector, or query.
- **Even more new utilities and variants** — `color-scheme`, `field-sizing`, complex shadows, `inert`, and more.

---

## New high-performance engine

Tailwind CSS v4.0 is a ground-up rewrite of the framework, optimised to be as fast as possible.

Benchmark results on Catalyst:

| Aspect | v3.4 | v4.0 | Improvement |
| --- | --- | --- | --- |
| Full build | 378ms | 100ms | 3.78x |
| Incremental rebuild with new CSS | 44ms | 5ms | 8.8x |
| Incremental rebuild with no new CSS | 35ms | 192µs | 182x |

The most impressive improvement is on incremental builds that don't compile new CSS — these complete in microseconds. The longer you work on a project, the more of these builds you encounter because you're using classes you've already used before.

---

## Designed for the modern web

v4.0 takes full advantage of modern CSS features:

```css
@layer theme, base, components, utilities;

@layer utilities {
  .mx-6 {
    margin-inline: calc(var(--spacing) * 6);
  }
  .bg-blue-500\/50 {
    background-color: color-mix(in oklab, var(--color-blue-500) 50%, transparent);
  }
}

@property --tw-gradient-from {
  syntax: "<color>";
  inherits: false;
  initial-value: #0000;
}
```

Modern CSS features leveraged:

- **Native cascade layers** — more control over how style rules interact.
- **Registered custom properties** — enables animating gradients and improves performance on large pages.
- **color-mix()** — adjust opacity of any colour value, including CSS variables and `currentColor`.
- **Logical properties** — simplifies RTL support and reduces generated CSS size.

---

## Simplified installation

1. Install Tailwind CSS:

```bash
npm i tailwindcss @tailwindcss/postcss
```

1. Add the PostCSS plugin:

```js
export default {
  plugins: ["@tailwindcss/postcss"],
};
```

1. Import Tailwind in your CSS:

```css
@import "tailwindcss";
```

Key improvements:

- **Just one line of CSS** — no more `@tailwind` directives, just `@import "tailwindcss"`.
- **Zero configuration** — start using the framework without configuring anything.
- **No external plugins required** — `@import` rules bundled out of the box, Lightning CSS handles vendor prefixing and modern syntax transforms.

---

## First-party Vite plugin

For Vite users, integrate using `@tailwindcss/vite` instead of PostCSS:

```ts
import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [
    tailwindcss(),
  ],
});
```

The Vite plugin provides even better performance than the PostCSS plugin.

---

## Automatic content detection

No more configuring the `content` array. v4.0 uses heuristics to detect template files automatically:

- Automatically ignores anything in `.gitignore` to avoid scanning dependencies or generated files:

```text
/node_modules
/coverage
/.next/
/build
```

- Automatically ignores binary extensions (images, videos, .zip files, etc.).

To explicitly add a source excluded by default, use the `@source` directive:

```css
@import "tailwindcss";
@source "../node_modules/@my-company/ui-lib";
```

The `@source` directive uses the same heuristics, excluding binary file types automatically.

---

## Built-in import support

Before v4.0, inlining CSS files with `@import` required `postcss-import`. Now handled out of the box, so you don't need any other tools - `postcss.config.js`:

```js
export default {
  plugins: [
    "postcss-import",
    "@tailwindcss/postcss",
  ],
};
```

---

## CSS-first configuration

Configure your project in CSS instead of JavaScript. Instead of `tailwind.config.js`, customise directly in your CSS file:

```css
@import "tailwindcss";

@theme {
  --font-display: "Satoshi", "sans-serif";
  --breakpoint-3xl: 1920px;
  --color-avocado-100: oklch(0.99 0 0);
  --color-avocado-200: oklch(0.98 0.04 113.22);
  --color-avocado-300: oklch(0.94 0.11 115.03);
  --color-avocado-400: oklch(0.92 0.19 114.08);
  --color-avocado-500: oklch(0.84 0.18 117.33);
  --color-avocado-600: oklch(0.53 0.12 118.34);
  --ease-fluid: cubic-bezier(0.3, 0, 0, 1);
  --ease-snappy: cubic-bezier(0.2, 0, 0, 1);
  /* ... */
}
```

CSS-first configuration supports everything from `tailwind.config.js`: design tokens, custom utilities, variants, and more.

---

## CSS theme variables

All design tokens are exposed as CSS variables by default for runtime access:

```css
:root {
  --font-display: "Satoshi", "sans-serif";
  --breakpoint-3xl: 1920px;
  --color-avocado-100: oklch(0.99 0 0);
  --color-avocado-200: oklch(0.98 0.04 113.22);
  --color-avocado-300: oklch(0.94 0.11 115.03);
  --color-avocado-400: oklch(0.92 0.19 114.08);
  --color-avocado-500: oklch(0.84 0.18 117.33);
  --color-avocado-600: oklch(0.53 0.12 118.34);
  --ease-fluid: cubic-bezier(0.3, 0, 0, 1);
  --ease-snappy: cubic-bezier(0.2, 0, 0, 1);
  /* ... */
}
```

Reuse these values as inline styles or pass them to libraries like Motion to animate them.

---

## Dynamic utility values and variants

Many utilities and variants now accept values without configuration or arbitrary value syntax.

Create grids of any size out of the box:

```html
<div class="grid grid-cols-15">
  <!-- ... -->
</div>
```

Target custom boolean data attributes without defining them:

```html
<div data-current class="opacity-75 data-current:opacity-100">
  <!-- ... -->
</div>
```

Spacing utilities (`px-*`, `mt-*`, `w-*`, `h-*`, etc.) are dynamically derived from a single spacing scale variable:

```css
@layer theme {
  :root {
    --spacing: 0.25rem;
  }
}

@layer utilities {
  .mt-8 {
    margin-top: calc(var(--spacing) * 8);
  }
  .w-17 {
    width: calc(var(--spacing) * 17);
  }
  .pr-29 {
    padding-right: calc(var(--spacing) * 29);
  }
}
```

The upgrade tool will simplify arbitrary values that are no longer needed.

---

## Modernised P3 colour palette

The default colour palette upgraded from `rgb` to `oklch`, using wider gamut for more vivid colours where previously limited by sRGB. The balance between colours remains the same as v3.

---

## Container queries

Container query support is now in core, no `@tailwindcss/container-queries` plugin needed:

```html
<div class="@container">
  <div class="grid grid-cols-1 @sm:grid-cols-3 @lg:grid-cols-4">
    <!-- ... -->
  </div>
</div>
```

Max-width container queries using `@max-*`:

```html
<div class="@container">
  <div class="grid grid-cols-3 @max-md:grid-cols-1">
    <!-- ... -->
  </div>
</div>
```

Stack `@min-*` and `@max-*` for container query ranges:

```html
<div class="@container">
  <div class="flex @min-md:@max-xl:hidden">
    <!-- ... -->
  </div>
</div>
```

---

## New 3D transform utilities

APIs for 3D transforms: `rotate-x-*`, `rotate-y-*`, `scale-z-*`, `translate-z-*`, and more:

```html
<div class="perspective-distant">
  <article class="rotate-x-51 rotate-z-43 transform-3d ...">
    <!-- ... -->
  </article>
</div>
```

See `transform-style`, `rotate`, `perspective`, and `perspective-origin` documentation.

---

## Expanded gradient APIs

### Linear gradient angles

Use utilities like `bg-linear-45` for gradients at specific angles:

```html
<div class="bg-linear-45 from-indigo-500 via-purple-500 to-pink-500"></div>
```

Note: `bg-gradient-*` renamed to `bg-linear-*`.

### Gradient interpolation modifiers

Control colour interpolation mode with modifiers — `bg-linear-to-r/srgb` interpolates using sRGB, `bg-linear-to-r/oklch` uses OKLCH:

```html
<div class="bg-linear-to-r/srgb from-indigo-500 to-teal-400">...</div>
<div class="bg-linear-to-r/oklch from-indigo-500 to-teal-400">...</div>
```

Polar colour spaces (OKLCH, HSL) produce more vivid gradients when colours are far apart on the colour wheel. v4.0 defaults to OKLAB.

### Conic and radial gradients

New `bg-conic-*` and `bg-radial-*` utilities:

```html
<div class="size-24 rounded-full bg-conic/[in_hsl_longer_hue] from-red-600 to-red-600"></div>
<div class="size-24 rounded-full bg-radial-[at_25%_25%] from-white to-zinc-900 to-75%"></div>
```

Work with existing `from-*`, `via-*`, and `to-*` utilities. Include modifiers for interpolation method and arbitrary value support for gradient position.

---

## @starting-style support

The `starting` variant adds support for CSS `@starting-style`, enabling transitions when elements first display:

```html
<div>
  <button popovertarget="my-popover">Check for updates</button>
  <div popover id="my-popover" class="transition-discrete starting:open:opacity-0 ...">
    <!-- ... -->
  </div>
</div>
```

Animate elements as they appear without JavaScript.

---

## not-* variant

Support for the CSS `:not()` pseudo-class:

```html
<div class="not-hover:opacity-75">
  <!-- ... -->
</div>
```

Generated CSS:

```css
.not-hover\:opacity-75:not(*:hover) {
  opacity: 75%;
}

@media not (hover: hover) {
  .not-hover\:opacity-75 {
    opacity: 75%;
  }
}
```

Also negates media queries and `@supports` queries:

```html
<div class="not-supports-hanging-punctuation:px-4">
  <!-- ... -->
</div>
```

Generated CSS:

```css
.not-supports-hanging-punctuation\:px-4 {
  @supports not (hanging-punctuation: var(--tw)) {
    padding-inline: calc(var(--spacing) * 4);
  }
}
```

---

## Even more new utilities and variants

- **`inset-shadow-*` and `inset-ring-*` utilities** — stack up to four layers of box shadows on a single element.
- **`field-sizing` utilities** — auto-resize textareas without JavaScript.
- **`color-scheme` utilities** — fix light scrollbars in dark mode.
- **`font-stretch` utilities** — tweak variable fonts supporting different widths.
- **`inert` variant** — style non-interactive elements with the `inert` attribute.
- **`nth-*` variants** — target nth-child elements.
- **`in-*` variant** — like `group-*` but without the `group` class.
- **`:popover-open` support** — using the `open` variant to target open popovers.
- **Descendant variant** — style all descendant elements.
