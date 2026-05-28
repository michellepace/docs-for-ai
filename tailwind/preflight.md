# Preflight

An opinionated set of base styles for Tailwind projects.

## [Overview](https://tailwindcss.com/docs/preflight\#overview)

Built on top of [modern-normalize](https://github.com/sindresorhus/modern-normalize), Preflight is a set of base styles for Tailwind projects that are designed to smooth over cross-browser inconsistencies and make it easier for you to work within the constraints of your design system.

When you import `tailwindcss` into your project, Preflight is automatically injected into the `base` layer:

```css
@layer theme, base, components, utilities;@import "tailwindcss/theme.css" layer(theme);@import "tailwindcss/preflight.css" layer(base);@import "tailwindcss/utilities.css" layer(utilities);
```

While most of the styles in Preflight are meant to go unnoticed—they simply make things behave more like you'd expect them to—some are more opinionated and can be surprising when you first encounter them.

For the latest complete reference of all the styles applied by Preflight, [see the stylesheet](https://github.com/tailwindlabs/tailwindcss/blob/main/packages/tailwindcss/preflight.css) or as of 2025-11-14 see inbetween tags `<preflight_stylesheet>` below!

<>

### [Margins are removed](https://tailwindcss.com/docs/preflight\#margins-are-removed)

Preflight removes all of the default margins from all elements including headings, blockquotes, paragraphs, etc:

```css
*,::after,::before,::backdrop,::file-selector-button {  margin: 0;  padding: 0;}
```

This makes it harder to accidentally rely on margin values applied by the user-agent stylesheet that are not part of your spacing scale.

### [Border styles are reset](https://tailwindcss.com/docs/preflight\#border-styles-are-reset)

In order to make it easy to add a border by simply adding the `border` class, Tailwind overrides the default border styles for all elements with the following rules:

```css
*,::after,::before,::backdrop,::file-selector-button {  box-sizing: border-box;  border: 0 solid;}
```

Since the `border` class only sets the `border-width` property, this reset ensures that adding that class always adds a solid `1px` border that uses `currentColor`.

This can cause some unexpected results when integrating certain third-party libraries, like [Google maps](https://github.com/tailwindlabs/tailwindcss/issues/484) for example.

When you run into situations like this, you can work around them by overriding the Preflight styles with your own custom CSS:

```css
@layer base {  .google-map * {    border-style: none;  }}
```

### [Headings are unstyled](https://tailwindcss.com/docs/preflight\#headings-are-unstyled)

All heading elements are completely unstyled by default, and have the same font size and weight as normal text:

```css
h1,h2,h3,h4,h5,h6 {  font-size: inherit;  font-weight: inherit;}
```

The reason for this is two-fold:

- **It helps you avoid accidentally deviating from your type scale**. By default, browsers assign sizes to headings that don't exist in Tailwind's default type scale, and aren't guaranteed to exist in your own type scale.
- **In UI development, headings should often be visually de-emphasized**. Making headings unstyled by default means any styling you apply to headings happens consciously and deliberately.

You can always add default header styles to your project by [adding your own base styles](https://tailwindcss.com/docs/adding-custom-styles#adding-base-styles).

### [Lists are unstyled](https://tailwindcss.com/docs/preflight\#lists-are-unstyled)

Ordered and unordered lists are unstyled by default, with no bullets or numbers:

```css
ol,ul,menu {  list-style: none;}
```

If you'd like to style a list, you can do so using the [list-style-type](https://tailwindcss.com/docs/list-style-type) and [list-style-position](https://tailwindcss.com/docs/list-style-position) utilities:

```html
<ul class="list-inside list-disc">  <li>One</li>  <li>Two</li>  <li>Three</li></ul>
```

You can always add default list styles to your project by [adding your own base styles](https://tailwindcss.com/docs/adding-custom-styles#adding-base-styles).

#### [Accessibility considerations](https://tailwindcss.com/docs/preflight\#accessibility-considerations)

Unstyled lists are [not announced as lists by VoiceOver](https://unfetteredthoughts.net/2017/09/26/voiceover-and-list-style-type-none/). If your content is truly a list but you would like to keep it unstyled, [add a "list" role](https://www.scottohara.me/blog/2019/01/12/lists-and-safari.html) to the element:

```html
<ul role="list">  <li>One</li>  <li>Two</li>  <li>Three</li></ul>
```

### [Images are block-level](https://tailwindcss.com/docs/preflight\#images-are-block-level)

Images and other replaced elements (like `svg`, `video`, `canvas`, and others) are `display: block` by default:

```css
img,svg,video,canvas,audio,iframe,embed,object {  display: block;  vertical-align: middle;}
```

This helps to avoid unexpected alignment issues that you often run into using the browser default of `display: inline`.

If you ever need to make one of these elements `inline` instead of `block`, simply use the `inline` utility:

```html
<img class="inline" src="..." alt="..." />
```

### [Images are constrained](https://tailwindcss.com/docs/preflight\#images-are-constrained)

Images and videos are constrained to the parent width in a way that preserves their intrinsic aspect ratio:

```css
img,video {  max-width: 100%;  height: auto;}
```

This prevents them from overflowing their containers and makes them responsive by default. If you ever need to override this behavior, use the `max-w-none` utility:

```html
<img class="max-w-none" src="..." alt="..." />
```

#### [Elements with a `hidden` attribute stay hidden](https://tailwindcss.com/docs/preflight\#elements-with-a-hidden-attribute-stay-hidden)

```css
[hidden]:where(:not([hidden="until-found"])) {  display: none !important;}
```

This enforces that elements with a `hidden` attribute stay invisible unless using `hidden="until-found"`. Remove the `hidden` attribute if you want an element to be visible to the user.

## [Extending Preflight](https://tailwindcss.com/docs/preflight\#extending-preflight)

If you'd like to add your own base styles on top of Preflight, add them to the `base` CSS layer in your CSS using `@layer base`:

```css
@layer base {  h1 {    font-size: var(--text-2xl);  }  h2 {    font-size: var(--text-xl);  }  h3 {    font-size: var(--text-lg);  }  a {    color: var(--color-blue-600);    text-decoration-line: underline;  }}
```

Learn more in the [adding base styles documentation](https://tailwindcss.com/docs/adding-custom-styles#adding-base-styles).

## [Disabling Preflight](https://tailwindcss.com/docs/preflight\#disabling-preflight)

If you'd like to completely disable Preflight—perhaps because you're integrating Tailwind into an existing project or you'd prefer to define your own base styles—you can do so by importing only the parts of Tailwind that you need.

By default, this is what `@import "tailwindcss";` injects:

```css
@layer theme, base, components, utilities;@import "tailwindcss/theme.css" layer(theme);@import "tailwindcss/preflight.css" layer(base);@import "tailwindcss/utilities.css" layer(utilities);
```

To disable Preflight, simply omit its import while keeping everything else:

```css
@layer theme, base, components, utilities;@import "tailwindcss/theme.css" layer(theme);@import "tailwindcss/preflight.css" layer(base);@import "tailwindcss/utilities.css" layer(utilities);
```

When importing Tailwind CSS' files individually, features like `source()`, `theme()`, and `prefix()` should go on their respective imports.

For example, source detection affects generated utilities, so `source(…)` should be added to the `utilities.css` import:

```css
@layer theme, base, components, utilities;@import "tailwindcss/theme.css" layer(theme);@import "tailwindcss/utilities.css" layer(utilities);@import "tailwindcss/utilities.css" layer(utilities) source(none);
```

The same goes for `important`, which also affects utilities:

```css
@layer theme, base, components, utilities;@import "tailwindcss/theme.css" layer(theme);@import "tailwindcss/utilities.css" layer(utilities);@import "tailwindcss/utilities.css" layer(utilities) important;
```

Similarly, `theme(static)` and `theme(inline)` affect the generated theme variables and should be placed on the `theme.css` import:

```css
@layer theme, base, components, utilities;@import "tailwindcss/theme.css" layer(theme);@import "tailwindcss/theme.css" layer(theme) theme(static);@import "tailwindcss/utilities.css" layer(utilities);
```

Finally, using a prefix with `prefix(tw)` affects the utilities and variables, so it should go on both imports:

```css
@layer theme, base, components, utilities;@import "tailwindcss/theme.css" layer(theme);@import "tailwindcss/utilities.css" layer(utilities);@import "tailwindcss/theme.css" layer(theme) prefix(tw);@import "tailwindcss/utilities.css" layer(utilities) prefix(tw);
```

## Preflight Stylesheet as of 2025-11-17

Source: <https://github.com/tailwindlabs/tailwindcss/blob/main/packages/tailwindcss/preflight.css>

<preflight_stylesheet>

```css
/*
  1. Prevent padding and border from affecting element width. (https://github.com/mozdevs/cssremedy/issues/4)
  2. Remove default margins and padding
  3. Reset all borders.
*/

*,
::after,
::before,
::backdrop,
::file-selector-button {
  box-sizing: border-box; /* 1 */
  margin: 0; /* 2 */
  padding: 0; /* 2 */
  border: 0 solid; /* 3 */
}

/*
  1. Use a consistent sensible line-height in all browsers.
  2. Prevent adjustments of font size after orientation changes in iOS.
  3. Use a more readable tab size.
  4. Use the user's configured `sans` font-family by default.
  5. Use the user's configured `sans` font-feature-settings by default.
  6. Use the user's configured `sans` font-variation-settings by default.
  7. Disable tap highlights on iOS.
*/

html,
:host {
  line-height: 1.5; /* 1 */
  -webkit-text-size-adjust: 100%; /* 2 */
  tab-size: 4; /* 3 */
  font-family: --theme(
    --default-font-family,
    ui-sans-serif,
    system-ui,
    sans-serif,
    'Apple Color Emoji',
    'Segoe UI Emoji',
    'Segoe UI Symbol',
    'Noto Color Emoji'
  ); /* 4 */
  font-feature-settings: --theme(--default-font-feature-settings, normal); /* 5 */
  font-variation-settings: --theme(--default-font-variation-settings, normal); /* 6 */
  -webkit-tap-highlight-color: transparent; /* 7 */
}

/*
  1. Add the correct height in Firefox.
  2. Correct the inheritance of border color in Firefox. (https://bugzilla.mozilla.org/show_bug.cgi?id=190655)
  3. Reset the default border style to a 1px solid border.
*/

hr {
  height: 0; /* 1 */
  color: inherit; /* 2 */
  border-top-width: 1px; /* 3 */
}

/*
  Add the correct text decoration in Chrome, Edge, and Safari.
*/

abbr:where([title]) {
  -webkit-text-decoration: underline dotted;
  text-decoration: underline dotted;
}

/*
  Remove the default font size and weight for headings.
*/

h1,
h2,
h3,
h4,
h5,
h6 {
  font-size: inherit;
  font-weight: inherit;
}

/*
  Reset links to optimize for opt-in styling instead of opt-out.
*/

a {
  color: inherit;
  -webkit-text-decoration: inherit;
  text-decoration: inherit;
}

/*
  Add the correct font weight in Edge and Safari.
*/

b,
strong {
  font-weight: bolder;
}

/*
  1. Use the user's configured `mono` font-family by default.
  2. Use the user's configured `mono` font-feature-settings by default.
  3. Use the user's configured `mono` font-variation-settings by default.
  4. Correct the odd `em` font sizing in all browsers.
*/

code,
kbd,
samp,
pre {
  font-family: --theme(
    --default-mono-font-family,
    ui-monospace,
    SFMono-Regular,
    Menlo,
    Monaco,
    Consolas,
    'Liberation Mono',
    'Courier New',
    monospace
  ); /* 1 */
  font-feature-settings: --theme(--default-mono-font-feature-settings, normal); /* 2 */
  font-variation-settings: --theme(--default-mono-font-variation-settings, normal); /* 3 */
  font-size: 1em; /* 4 */
}

/*
  Add the correct font size in all browsers.
*/

small {
  font-size: 80%;
}

/*
  Prevent `sub` and `sup` elements from affecting the line height in all browsers.
*/

sub,
sup {
  font-size: 75%;
  line-height: 0;
  position: relative;
  vertical-align: baseline;
}

sub {
  bottom: -0.25em;
}

sup {
  top: -0.5em;
}

/*
  1. Remove text indentation from table contents in Chrome and Safari. (https://bugs.chromium.org/p/chromium/issues/detail?id=999088, https://bugs.webkit.org/show_bug.cgi?id=201297)
  2. Correct table border color inheritance in all Chrome and Safari. (https://bugs.chromium.org/p/chromium/issues/detail?id=935729, https://bugs.webkit.org/show_bug.cgi?id=195016)
  3. Remove gaps between table borders by default.
*/

table {
  text-indent: 0; /* 1 */
  border-color: inherit; /* 2 */
  border-collapse: collapse; /* 3 */
}

/*
  Use the modern Firefox focus style for all focusable elements.
*/

:-moz-focusring {
  outline: auto;
}

/*
  Add the correct vertical alignment in Chrome and Firefox.
*/

progress {
  vertical-align: baseline;
}

/*
  Add the correct display in Chrome and Safari.
*/

summary {
  display: list-item;
}

/*
  Make lists unstyled by default.
*/

ol,
ul,
menu {
  list-style: none;
}

/*
  1. Make replaced elements `display: block` by default. (https://github.com/mozdevs/cssremedy/issues/14)
  2. Add `vertical-align: middle` to align replaced elements more sensibly by default. (https://github.com/jensimmons/cssremedy/issues/14#issuecomment-634934210)
      This can trigger a poorly considered lint error in some tools but is included by design.
*/

img,
svg,
video,
canvas,
audio,
iframe,
embed,
object {
  display: block; /* 1 */
  vertical-align: middle; /* 2 */
}

/*
  Constrain images and videos to the parent width and preserve their intrinsic aspect ratio. (https://github.com/mozdevs/cssremedy/issues/14)
*/

img,
video {
  max-width: 100%;
  height: auto;
}

/*
  1. Inherit font styles in all browsers.
  2. Remove border radius in all browsers.
  3. Remove background color in all browsers.
  4. Ensure consistent opacity for disabled states in all browsers.
*/

button,
input,
select,
optgroup,
textarea,
::file-selector-button {
  font: inherit; /* 1 */
  font-feature-settings: inherit; /* 1 */
  font-variation-settings: inherit; /* 1 */
  letter-spacing: inherit; /* 1 */
  color: inherit; /* 1 */
  border-radius: 0; /* 2 */
  background-color: transparent; /* 3 */
  opacity: 1; /* 4 */
}

/*
  Restore default font weight.
*/

:where(select:is([multiple], [size])) optgroup {
  font-weight: bolder;
}

/*
  Restore indentation.
*/

:where(select:is([multiple], [size])) optgroup option {
  padding-inline-start: 20px;
}

/*
  Restore space after button.
*/

::file-selector-button {
  margin-inline-end: 4px;
}

/*
  Reset the default placeholder opacity in Firefox. (https://github.com/tailwindlabs/tailwindcss/issues/3300)
*/

::placeholder {
  opacity: 1;
}

/*
  Set the default placeholder color to a semi-transparent version of the current text color in browsers that do not
  crash when using `color-mix(…)` with `currentcolor`. (https://github.com/tailwindlabs/tailwindcss/issues/17194)
*/

@supports (not (-webkit-appearance: -apple-pay-button)) /* Not Safari */ or
  (contain-intrinsic-size: 1px) /* Safari 17+ */ {
  ::placeholder {
    color: color-mix(in oklab, currentcolor 50%, transparent);
  }
}

/*
  Prevent resizing textareas horizontally by default.
*/

textarea {
  resize: vertical;
}

/*
  Remove the inner padding in Chrome and Safari on macOS.
*/

::-webkit-search-decoration {
  -webkit-appearance: none;
}

/*
  1. Ensure date/time inputs have the same height when empty in iOS Safari.
  2. Ensure text alignment can be changed on date/time inputs in iOS Safari.
*/

::-webkit-date-and-time-value {
  min-height: 1lh; /* 1 */
  text-align: inherit; /* 2 */
}

/*
  Prevent height from changing on date/time inputs in macOS Safari when the input is set to `display: block`.
*/

::-webkit-datetime-edit {
  display: inline-flex;
}

/*
  Remove excess padding from pseudo-elements in date/time inputs to ensure consistent height across browsers.
*/

::-webkit-datetime-edit-fields-wrapper {
  padding: 0;
}

::-webkit-datetime-edit,
::-webkit-datetime-edit-year-field,
::-webkit-datetime-edit-month-field,
::-webkit-datetime-edit-day-field,
::-webkit-datetime-edit-hour-field,
::-webkit-datetime-edit-minute-field,
::-webkit-datetime-edit-second-field,
::-webkit-datetime-edit-millisecond-field,
::-webkit-datetime-edit-meridiem-field {
  padding-block: 0;
}

/*
  Center dropdown marker shown on inputs with paired `<datalist>`s in Chrome. (https://github.com/tailwindlabs/tailwindcss/issues/18499)
*/

::-webkit-calendar-picker-indicator {
  line-height: 1;
}

/*
  Remove the additional `:invalid` styles in Firefox. (https://github.com/mozilla/gecko-dev/blob/2f9eacd9d3d995c937b4251a5557d95d494c9be1/layout/style/res/forms.css#L728-L737)
*/

:-moz-ui-invalid {
  box-shadow: none;
}

/*
  Correct the inability to style the border radius in iOS Safari.
*/

button,
input:where([type='button'], [type='reset'], [type='submit']),
::file-selector-button {
  appearance: button;
}

/*
  Correct the cursor style of increment and decrement buttons in Safari.
*/

::-webkit-inner-spin-button,
::-webkit-outer-spin-button {
  height: auto;
}

/*
  Make elements with the HTML hidden attribute stay hidden by default.
*/

[hidden]:where(:not([hidden='until-found'])) {
  display: none !important;
}
```

</preflight_stylesheet>
