[Home](https://tailwindcss.com/) v4.3

`⌘K`  `Ctrl K` [Docs](https://tailwindcss.com/docs) [Play](https://play.tailwindcss.com/) [Blog](https://tailwindcss.com/blog) [Showcase](https://tailwindcss.com/showcase) [Partners](https://tailwindcss.com/partners) [Plus](https://tailwindcss.com/plus?ref=top) [GitHub repository](https://github.com/tailwindlabs/tailwindcss)

1. Filters
2. blur

Filters

# backdrop-filter: blur()

Utilities for applying backdrop blur filters to an element.

| Class | Styles |
| --- | --- |
| `backdrop-blur-xs` | `backdrop-filter: blur(var(--blur-xs)); /* 4px */` |
| `backdrop-blur-sm` | `backdrop-filter: blur(var(--blur-sm)); /* 8px */` |
| `backdrop-blur-md` | `backdrop-filter: blur(var(--blur-md)); /* 12px */` |
| `backdrop-blur-lg` | `backdrop-filter: blur(var(--blur-lg)); /* 16px */` |
| `backdrop-blur-xl` | `backdrop-filter: blur(var(--blur-xl)); /* 24px */` |
| `backdrop-blur-2xl` | `backdrop-filter: blur(var(--blur-2xl)); /* 40px */` |
| `backdrop-blur-3xl` | `backdrop-filter: blur(var(--blur-3xl)); /* 64px */` |
| `backdrop-blur-none` | `backdrop-filter: ;` |
| `backdrop-blur-(<custom-property>)` | `backdrop-filter: blur(var(<custom-property>));` |
| `backdrop-blur-[<value>]` | `backdrop-filter: blur(<value>);` |

## [Examples](https://tailwindcss.com/docs/backdrop-filter-blur\#examples)

### [Basic example](https://tailwindcss.com/docs/backdrop-filter-blur\#basic-example)

Use utilities like `backdrop-blur-sm` and `backdrop-blur-lg` to control an element’s backdrop blur:

backdrop-blur-none

![](https://images.unsplash.com/photo-1554629947-334ff61d85dc?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&h=1000&q=90)

backdrop-blur-sm

![](https://images.unsplash.com/photo-1554629947-334ff61d85dc?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&h=1000&q=90)

backdrop-blur-md

![](https://images.unsplash.com/photo-1554629947-334ff61d85dc?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&h=1000&q=90)

```
<div class="bg-[url(/img/mountains.jpg)]">  <div class="bg-white/30 backdrop-blur-none ..."></div></div><div class="bg-[url(/img/mountains.jpg)]">  <div class="bg-white/30 backdrop-blur-sm ..."></div></div><div class="bg-[url(/img/mountains.jpg)]">  <div class="bg-white/30 backdrop-blur-md ..."></div></div>
```

### [Using a custom value](https://tailwindcss.com/docs/backdrop-filter-blur\#using-a-custom-value)

Use the`backdrop-blur-[<value>]`syntaxto set the backdrop blur based on a completely custom value:

```
<div class="backdrop-blur-[2px] ...">  <!-- ... --></div>
```

For CSS variables, you can also use the`backdrop-blur-(<custom-property>)`syntax:

```
<div class="backdrop-blur-(--my-backdrop-blur) ...">  <!-- ... --></div>
```

This is just a shorthand for`backdrop-blur-[var(<custom-property>)]`that adds the `var()` function for you automatically.

### [Responsive design](https://tailwindcss.com/docs/backdrop-filter-blur\#responsive-design)

Prefix a`backdrop-filter: blur()` utilitywith a breakpoint variant like `md:` to only apply the utility at mediumscreen sizes and above:

```
<div class="backdrop-blur-none md:backdrop-blur-lg ...">  <!-- ... --></div>
```

Learn more about using variants in the [variants documentation](https://tailwindcss.com/docs/hover-focus-and-other-states).

## [Customizing your theme](https://tailwindcss.com/docs/backdrop-filter-blur\#customizing-your-theme)

Use the `--blur-*` theme variables to customize the backdrop blurutilities in your project:

```
@theme {  --blur-2xs: 2px; }
```

Now the`backdrop-blur-2xs`utility can be used in your markup:

```
<div class="backdrop-blur-2xs">  <!-- ... --></div>
```

Learn more about customizing your theme in the [theme documentation](https://tailwindcss.com/docs/theme#customizing-your-theme).

### On this page

- [Quick reference](https://tailwindcss.com/docs/backdrop-filter-blur#quick-reference)
- [Examples](https://tailwindcss.com/docs/backdrop-filter-blur#examples)
  - [Basic example](https://tailwindcss.com/docs/backdrop-filter-blur#basic-example)
  - [Using a custom value](https://tailwindcss.com/docs/backdrop-filter-blur#using-a-custom-value)
  - [Responsive design](https://tailwindcss.com/docs/backdrop-filter-blur#responsive-design)
- [Customizing your theme](https://tailwindcss.com/docs/backdrop-filter-blur#customizing-your-theme)

[![Refactoring UI](https://tailwindcss.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fbook-promo.0xtl10.r4k91k.png&w=256&q=75)\\
\\
From the creators of Tailwind CSS\\
\\
Make your ideas look awesome, without relying on a designer.\\
\\
> “This is the survival kit I wish I had when I started building apps.”\\
> \\
> Derrick Reimer, SavvyCal](https://www.refactoringui.com/?ref=sidebar)

Copyright © 2026 Tailwind Labs Inc.· [Trademark Policy](https://tailwindcss.com/brand)