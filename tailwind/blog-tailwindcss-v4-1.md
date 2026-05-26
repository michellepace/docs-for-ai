
# Tailwind CSS v4.1: Text shadows, masks, and tons more - April 3, 2025

Tailwind CSS v4.1 is here and it's packed with new utilities, variants, and developer experience improvements that will help you _(or your LLM, you coward)_ build even better interactive experiences.

Here's all the best stuff we got into this release:

- [New `text-shadow-*` utilities](https://tailwindcss.com/blog/tailwindcss-v4-1#new-text-shadow-utilities) — only about twenty years after they were first supported by a browser.
- [Mask elements with the `mask-*` utilities](https://tailwindcss.com/blog/tailwindcss-v4-1#mask-elements-with-the-mask-utilities) — use images and gradients to mask elements with new ergonomic APIs.
- [Improved compatibility with older browsers](https://tailwindcss.com/blog/tailwindcss-v4-1#improved-compatibility-with-older-browsers) — we've made things degrade way more gracefully for older browsers, while still taking advantage of modern features in browsers that support them.
- [Fine-grained text wrapping with `overflow-wrap`](https://tailwindcss.com/blog/tailwindcss-v4-1#fine-grained-text-wrapping-with-overflow-wrap) — defend the integrity of your layouts from even the longest German words your users will throw at you.
- [Colored `drop-shadow` support](https://tailwindcss.com/blog/tailwindcss-v4-1#colored-drop-shadow-support) — can't really remember why we didn't have these before but we do now.
- [Target input devices with `pointer-*` and `any-pointer-*`](https://tailwindcss.com/blog/tailwindcss-v4-1#target-input-devices-with-pointer-and-any-pointer-) — tweak your design for touch devices explicitly instead of relying on viewport size.
- [Align items to the last baseline](https://tailwindcss.com/blog/tailwindcss-v4-1#align-items-to-the-last-baseline) — align flex or grid items to the baseline of the last line of text using the new `items-baseline-last` and `self-baseline-last` utilities.
- [Keep content visible with `safe` alignment](https://tailwindcss.com/blog/tailwindcss-v4-1#keep-content-visible-with-safe-alignment) — center content in flex and grid layouts without it disappearing when there's not enough space.
- [Ignore specific paths with `@source not`](https://tailwindcss.com/blog/tailwindcss-v4-1#ignore-specific-paths-with-source-not) — explicitly ignore irrelevant large directories and speed up your builds even more.
- [Safelist specific utilities with `@source inline(…)`](https://tailwindcss.com/blog/tailwindcss-v4-1#safelist-specific-utilities-with-source-inline) — force Tailwind to include classes that aren't in your source files.
- [A bunch of other new variants](https://tailwindcss.com/blog/tailwindcss-v4-1#a-bunch-of-other-new-variants) — including `noscript`, `user-valid`, `inverted-colors`, and more.

## [New `text-shadow-*` utilities](https://tailwindcss.com/blog/tailwindcss-v4-1\#new-text-shadow-utilities)

We've been threatening to add text shadows for at least the last six years and today they are finally here.

We've added five text shadows to the default theme, from `text-shadow-2xs` to `text-shadow-lg`. They are particularly useful for making headings stand out against a busy background:

```html
<p class="text-shadow-2xs ...">The quick brown fox...</p>
<p class="text-shadow-xs ...">The quick brown fox...</p>
<p class="text-shadow-sm ...">The quick brown fox...</p>
<p class="text-shadow-md ...">The quick brown fox...</p>
<p class="text-shadow-lg ...">The quick brown fox...</p>
```

You can change the color of the shadow using the `text-shadow-<color>` utilities. For instance, you can create a sort of embossed effect by using a small white shadow on dark text:

```
<button class="text-sky-950 text-shadow-2xs text-shadow-sky-300 ...">Book a demo</button>
<button class="text-gray-950 dark:text-white dark:text-shadow-2xs ...">See pricing</button>
```

If you just want to adjust the opacity of a text shadow without changing the color, you can slap an opacity modifier directly on text shadow size utilities like `text-shadow-lg`.

For example, `text-shadow-lg/50` is the same as setting `text-shadow-lg` and `text-shadow-black/50` at the same time:

```html
<p class="text-shadow-lg ...">The quick brown fox...</p>
<p class="text-shadow-lg/20 ...">The quick brown fox...</p>
<p class="text-shadow-lg/30 ...">The quick brown fox...</p>
```

Check out the [`text-shadow`](https://tailwindcss.com/docs/text-shadow) docs for more details.

## [Mask elements with the `mask-*` utilities](https://tailwindcss.com/blog/tailwindcss-v4-1\#mask-elements-with-the-mask-utilities)

One of the coolest features of modern CSS is the ability to use images and gradients as masks - basically using the opacity of an image to hide certain parts of an element:

```html
<div class="mx-auto flex items-center p-16 max-sm:p-8">
  <img
    src="/img/keyboard.png"
    class="mask-radial-from-transparent mask-radial-from-15% mask-radial-to-black mask-radial-to-55% mask-radial-at-right ..."
  />
  <div class="font-medium">
    <p class="font-mono text-xs text-blue-500 uppercase dark:text-blue-400">Speed</p>
    <p class="mt-2 text-base text-gray-700 dark:text-gray-300">Built for power users</p>
    <p class="mt-1 text-sm leading-relaxed text-balance text-gray-500">
      Work faster than ever with our keyboard shortcuts
    </p>
  </div>
</div>
```

Because you can use any `background-image` as a mask, the logical thing to do was to copy the `bg-*` utilities so they share the same API. The problem with that approach is you often want to combine multiple masks together and the `bg-*` utilities are not composable.

So instead, we created a new set of utilities to work with `mask-image` that are composable and purpose-built for the masking use case. For example, you can use utilities like `mask-b-from-<value>` and `mask-t-to-<value>` to add a linear gradient mask to a single side of an element:

```html
<div class="mask-t-from-50% bg-[url(/img/mountains.jpg)] ..."></div>
<div class="mask-r-from-30% bg-[url(/img/mountains.jpg)] ..."></div>
<div class="mask-l-from-50% mask-l-to-90% bg-[url(/img/mountains.jpg)] ..."></div>
<div class="mask-b-from-20% mask-b-to-80% bg-[url(/img/mountains.jpg)] ..."></div>
```

It's more natural to think about which side you want to mask, rather than trying to work out the exact gradient you need to use.

The gradient mask utilities are also composable, so you can combine radial, conic and linear gradients together to create more complex masks:

```html
<div class="mask-b-from-50% mask-radial-[50%_90%] mask-radial-from-80% bg-[url(/img/mountains.jpg)] ..."></div>
<div class="mask-r-from-80% mask-b-from-80% mask-radial-from-70% mask-radial-to-85% bg-[url(/img/mountains.jpg)] ..."></div>
```

Masking is a super powerful technique and there's a lot more to the API than we can cover here. For a full breakdown of the new utilities, check out the [documentation](https://tailwindcss.com/docs/mask-image).

### [Improved compatibility with older browsers](https://tailwindcss.com/blog/tailwindcss-v4-1\#improved-compatibility-with-older-browsers)

We went all-in on modern platform features with Tailwind CSS v4.0 to make the best framework we could, and give this version the longest shelf-life possible.

Unfortunately some of those features degrade really poorly in older browsers, to the point where even basic things like colors and shadows might not render at all for someone visiting from an old iPhone or iPad that's stuck on Safari 15.

For Tailwind CSS v4.1, we put a bunch of effort into coming up with and testing our own framework-specific fallbacks to make your sites render as best as possible in older browsers, even if some super modern things still don't behave quite the same.

> **Safari 15.5 comparison:** v4.0 fails to render some background gradients that now render correctly in v4.1.

Here's a list of the things we've managed to improve in this release:

- Colors defined in `oklab` now render in older versions of Safari
- Features that depend on custom properties defined with `@property` (like shadows, transforms, gradients and more) now work in older versions of Safari and Firefox
- Colors using the opacity modifier now render with inlined fallbacks in older browsers
- Gradients using explicit interpolation methods fall back to the browser default when not supported

Tailwind CSS v4 is still _designed_ for modern browsers like Safari 16.4 and up and still depends on a lot of modern features for everything to work _perfectly_, but at least now your sites will render and be usable in older browsers, even if in certain specific situations the odd shadow color be different.

To learn everything you need to know about browser compatibility in Tailwind CSS v4, you can read the full [browser compatibility documentation](https://tailwindcss.com/docs/compatibility).

## [Fine-grained text wrapping with `overflow-wrap`](https://tailwindcss.com/blog/tailwindcss-v4-1\#fine-grained-text-wrapping-with-overflow-wrap)

The new `overflow-wrap` utilities let you control how text wraps within an element. The `wrap-break-word` utility is especially useful for long words or URLs that might otherwise break your layout:

```html
<p class="wrap-break-word">The longest word in any of the major...</p>
```

The one case where this doesn't quite behave like you'd expect is inside a flex container and that's where you probably want to use the new `wrap-anywhere` utility instead.

It's similar to `wrap-break-word`, but it allows mid-word line breaks when calculating the intrinsic size of the element, replacing the need to set `min-width: 0` on the child element:

```html
<div class="flex max-w-sm">
  <img class="size-16 rounded-full" src="/img/profile.jpg" />
  <div class="wrap-break-word">
    <p class="font-medium">Jay Riemenschneider</p>
    <p>jason.riemenschneider@vandelayindustries.com</p>
  </div>
</div>
<div class="flex max-w-sm">
  <img class="size-16 rounded-full" src="/img/profile.jpg" />
  <div class="wrap-anywhere">
    <p class="font-medium">Jay Riemenschneider</p>
    <p>jason.riemenschneider@vandelayindustries.com</p>
  </div>
</div>
```

There's not much more to it than that, but here's the [`overflow-wrap`](https://tailwindcss.com/docs/overflow-wrap) documentation if you want to read it again in slightly different words.

## [Colored `drop-shadow` support](https://tailwindcss.com/blog/tailwindcss-v4-1\#colored-drop-shadow-support)

While we were building out `text-shadow` support we thought we might as well add another feature we never got around to implementing: colored drop shadows.

Now you can use utilities like `drop-shadow-indigo-500` and `drop-shadow-cyan-500/50` to change the color of a drop shadow:

```html
<svg class="fill-cyan-500 drop-shadow-xl drop-shadow-cyan-500/50 ...">...</svg>
<svg class="fill-blue-500 drop-shadow-xl drop-shadow-blue-500/50 ...">...</svg>
<svg class="fill-indigo-500 drop-shadow-xl drop-shadow-indigo-500/50 ...">...</svg>
```

There isn't much more to it but here's the [`drop-shadow` documentation](https://tailwindcss.com/docs/filter-drop-shadow) anyway.

## [Target input devices with `pointer-*` and `any-pointer-*`](https://tailwindcss.com/blog/tailwindcss-v4-1\#target-input-devices-with-pointer-and-any-pointer-)

The new `pointer-fine` and `pointer-coarse` variants let you style something differently depending on whether the user is using a device with a mouse or using a touchscreen.

Use `pointer-fine` to target precise pointing devices like mouses and trackpads, and `pointer-coarse` to target devices lower precision like touchscreens:

```html
<fieldset aria-label="Choose a memory option">
  <div class="flex items-center justify-between">
    <div>RAM</div>
    <a href="#"> See performance specs </a>
  </div>
  <div class="mt-4 grid grid-cols-6 gap-2 pointer-coarse:mt-6 pointer-coarse:grid-cols-3 pointer-coarse:gap-4">
    <label class="p-2 pointer-coarse:p-4 ...">
      <input type="radio" name="memory-option" value="4 GB" className="sr-only" />
      <span>4 GB</span>
    </label>
    <!-- ... -->
  </div>
</fieldset>
```

If you're on your phone, you'll see the `pointer-coarse` styles applied, which make the touch targets larger and easier to hit. If you're on a desktop, you'll see the `pointer-fine` styles applied, which make the touch targets smaller and more precise.

The `any-pointer-*` variants work the same way but instead of just checking the user's _primary_ pointing device, they check if _any_ pointing device matches. So `any-pointer-coarse` will match on a laptop with a touchscreen for a example, even if the user also has a mouse connected.

## [Align items to the last baseline](https://tailwindcss.com/blog/tailwindcss-v4-1\#align-items-to-the-last-baseline)

When working with flex or grid layouts, sometimes you need to align something to the baseline of the last line of text rather than the end of the container.

The new `items-baseline-last` utility does just that:

```html
<div class="grid grid-cols-[1fr_auto] items-baseline-last">
  <div>
    <img src="img/spencer-sharp.jpg" />
    <h4>Spencer Sharp</h4>
    <p>Working on the future of astronaut recruitment at Space Recruit.</p>
  </div>
  <p>spacerecruit.com</p>
</div>
```

We've also added `self-baseline-last` for when you need to align just a single item, and not all items in the flex or grid container.

## [Keep content visible with `safe` alignment](https://tailwindcss.com/blog/tailwindcss-v4-1\#keep-content-visible-with-safe-alignment)

Ever had center aligned content overflow in both directions when the container got too small? Now you don't have to use a container query to switch the alignment at different sizes.

The new `safe` alignment utilities will change the alignment to `start` when the container starts to overflow, so it only overflows in one direction.

**`justify-center`** (content can overflow and become inaccessible):

```html
<ul class="flex justify-center gap-2 ...">
  <li>Sales</li>
  <li>Marketing</li>
  <li>SEO</li>
  <!-- ... -->
</ul>
```

**`justify-center-safe`** (falls back to `start` on overflow):

```html
<ul class="flex justify-center-safe gap-2 ...">
  <li>Sales</li>
  <li>Marketing</li>
  <li>SEO</li>
  <!-- ... -->
</ul>
```

These utilities work with both flexbox and grid layouts, and are available for all alignment properties.

## [Ignore specific paths with `@source not`](https://tailwindcss.com/blog/tailwindcss-v4-1\#ignore-specific-paths-with-source-not)

Sometimes you need to specifically exclude some parts of your code base from being scanned by Tailwind. Now you can use `@source not` to ignore specific paths when scanning for class names:

CSS

```css
@import "tailwindcss";@source not "./src/components/legacy";
```

This is useful when you have a large number of files in your project, but only want to scan a specific subset of them.

## [Safelist specific utilities with `@source inline(…)`](https://tailwindcss.com/blog/tailwindcss-v4-1\#safelist-specific-utilities-with-source-inline)

If you need to make sure Tailwind generates certain class names that don’t exist in your content files, you can force them to be generated by using `@source inline()`:

```css
@import "tailwindcss";@source inline("underline");
```

Generated CSS

```css
.underline {  text-decoration: underline;}
```

This is the equivalent of the `safelist` configuration option in previous versions of Tailwind, but now you can use it in your CSS files instead of your config file.

The source input is [brace-expanded](https://www.gnu.org/software/bash/manual/html_node/Brace-Expansion.html), so you can generate multiple classes at once. For example, to generate all the red shades with hover variants, you can add a range to the source input:

```css
@import "tailwindcss";@source inline("{hover:,}bg-red-{50,{100..900..100},950}");
```

Generated CSS

```css
.bg-red-50 {
  background-color: var(--color-red-50);
}
.bg-red-100 {
  background-color: var(--color-red-100);
}
.bg-red-200 {
  background-color: var(--color-red-200);
}
/* ... */
.bg-red-800 {
  background-color: var(--color-red-800);
}
.bg-red-900 {
  background-color: var(--color-red-900);
}
.bg-red-950 {
  background-color: var(--color-red-950);
}
@media (hover: hover) {
  .hover\:bg-red-50:hover {
    background-color: var(--color-red-50);
  }
  /* ... */
  .hover\:bg-red-950:hover {
    background-color: var(--color-red-950);
  }
}
```

This will generate shades of red from 100 to 900 in increments of 100, as well as the 50 and 950 shades. It also adds the `hover:` variant for each of those classes.

You can also use `@source inline()` with the `not` modifier to exclude specific classes from being generated:

```css
@import "tailwindcss";@source not inline("container");
```

This will specifically prevent the `container` class from being generated, even if the word `container` is detected in your source files.

For more details, check out the [detecting classes in source files](https://tailwindcss.com/docs/detecting-classes-in-source-files#safelisting-specific-utilities) documentation.

## [A bunch of other new variants](https://tailwindcss.com/blog/tailwindcss-v4-1\#a-bunch-of-other-new-variants)

### [Prettier accordions with `details-content`](https://tailwindcss.com/blog/tailwindcss-v4-1\#prettier-accordions-with-details-content)

While you could always add styles to the children of a `<details>` element, it's been impossible to style the content container itself.

The new `details-content` variant targets the content container which is useful for positioning the content container relative to the `<summary>` element:

```html
<details class="rounded-lg border border-transparent p-6 details-content:mt-3 details-content:-ml-0.5" open>
  <summary class="text-sm leading-6 font-semibold text-gray-900 select-none dark:text-white">
    Why do they call it Ovaltine?
  </summary>
  <div class="border-gray-200 bg-gray-50 py-3 pl-3 dark:border-white/10 dark:bg-gray-800/50 ...">
    <p>The mug is round. The jar is round. They should call it Roundtine.</p>
  </div>
</details>
```

## [Target `inverted-colors` mode](https://tailwindcss.com/blog/tailwindcss-v4-1\#target-inverted-colors-mode)

Use the `inverted-colors` variant to conditionally add styles when the user has enabled an inverted color scheme in their OS:

```html
<div class="shadow-xl inverted-colors:shadow-none ...">  <!-- ... --></div>
```

This is useful for things like preventing black shadows being turned white when inverted colors are enabled.

## [New `noscript` variant](https://tailwindcss.com/blog/tailwindcss-v4-1\#new-noscript-variant)

Yes, some people disable JavaScript and now you can tell them your app doesn't work without it. The `noscript` variant lets you conditionally apply styles when JS is disabled:

```html
<div class="hidden noscript:block">Please enable JavaScript to use this app.</div>
```

You could already do this with the `<noscript>` tag but now you can do it with CSS too, which Tailwind lets you write in your HTML, so… yeah.

## [Better form validation with `user-valid` and `user-invalid`](https://tailwindcss.com/blog/tailwindcss-v4-1\#better-form-validation-with-user-valid-and-user-invalid)

Ever tried the `:invalid` pseudo-class only for the page to be full of red invalid states as soon as it loads, before the user has even touched your form?

The new `user-valid` and `user-invalid` variants try to solve this problem, by only applying validation-related styling after the user has actually interacted with the controls:

```html
<input required class="border user-valid:border-green-500" />
<input required class="border user-invalid:border-red-500" />
```
