# Getting started

[Catalyst](https://tailwindcss.com/plus/templates/catalyst) is a starter kit for building your own component systems with React and Tailwind CSS — designed and developed by the Tailwind CSS team. It's a collection of beautiful, production-ready UI components you drop into your projects alongside your own code that are yours to customize, adapt, and make your own.

![Catalyst demo](https://catalyst.tailwindui.com/demo-preview.jpeg)![Catalyst demo](https://catalyst.tailwindui.com/demo-preview-dark.jpeg)[Open in new tab](https://catalyst-demo.tailwindui.com/)

* * *

## Before you start

Before you do anything else, make sure you've got a Tailwind CSS project set up with Next.js that you'd like to use with Catalyst. Catalyst is built with React and works seamlessly with Next.js.

For help creating a project and configuring Tailwind CSS, check out the
[framework guides](https://tailwindcss.com/docs/installation/framework-guides) in the Tailwind CSS documentation.

Catalyst is built around Tailwind's default theme configuration and relies on the default spacing scale, color palette, shadow scale, and more. You're of course free to customize anything you like, but you won't get the expected results out-of-the-box if you've made significant changes to the default theme and will need to edit the components to adapt them for your customizations.

* * *

## Adding Catalyst to your project

To get started with Catalyst, first [download the latest version](https://tailwindcss.com/plus/templates/catalyst/download) from within your Tailwind Plus account.

Then, unzip `catalyst-ui-kit.zip` and copy the component files from either the `javascript` or `typescript` folders into wherever you keep components in your own project:

![picture of component](https://catalyst.tailwindui.com/_next/static/media/copy-components.f99ada87.png)

### Installing dependencies

Next install the dependencies used by the components in Catalyst:

```bash
npm install @headlessui/react motion clsx
```

Catalyst is also designed for the latest version of Tailwind CSS, which is currently Tailwind CSS v4.0. To make sure that you are on the latest version of Tailwind, update it via npm:

```bash
npm install tailwindcss@latest
```

### Client-side router integration

By default, the `Link` component in Catalyst renders a plain HTML `<a>` element. You should update this component in your `link.tsx` or `link.jsx` file to use the Next.js Link component (see the Next.js integration example below).

### Optional: Setup Inter font family

We've designed Catalyst using [Inter](https://rsms.me/inter) to ensure that the components look the same in all browsers and operating systems.

If you'd like to use Inter in your Next.js project, Next.js has a [dedicated font API](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) that simplifies the developer experience.

Alternatively, you can add Inter by pointing a `<link>` tag to the CDN:

```html
<link rel="stylesheet" href="https://rsms.me/inter/inter.css" />
```

Then update the `--font-sans` theme variable in your project to use Inter:

```css
@theme {
  --font-sans: Inter, sans-serif;
  --font-sans--font-feature-settings: 'cv11';
}
```

### Optional: Install Heroicons

We're using our own [Heroicons](https://heroicons.com/) icon set in Catalyst any time we need icons, and Heroicons has been designed to integrate seamlessly with Catalyst projects.

If you'd like to use Heroicons in your own projects, you can install it via npm:

```bash
npm install @heroicons/react
```

Most components in Catalyst — like the `Button`, `DropdownItem`, and `ListboxOption` components — are designed to work best with 16×16 icons, so for these components import the icons you need from `@heroicons/react/16/solid`:

```tsx
import { Button } from '@/components/button'
import { PlusIcon } from '@heroicons/react/16/solid'

function Example() {
  return (
    <Button>
      <PlusIcon />
      Add item
    </Button>
  )
}
```

The only exceptions are the `NavbarItem` and `SidebarItem` components which are designed for 20×20 icons. For these components, import from `@heroicons/react/20/solid` instead:

```tsx
import { SidebarItem, SidebarLabel } from '@/components/sidebar'
import { HomeIcon } from '@heroicons/react/20/solid'

function Example() {
  return (
    <SidebarItem href="/home">
      <HomeIcon />
      <SidebarLabel>Home</SidebarLabel>
    </SidebarItem>
  )
}
```

* * *

## Next.js integration

By default, the `Link` component in Catalyst renders a plain HTML `<a>` element. Here's how to update your `Link` component to use the Next.js `Link` component:

Update your `link.tsx` or `link.jsx` file to use the `Link` component from Next.js:

```tsx
import * as Headless from '@headlessui/react'
import NextLink, { type LinkProps } from 'next/link'
import React, { forwardRef } from 'react'

export const Link = forwardRef(function Link(
  props: LinkProps & React.ComponentPropsWithoutRef<'a'>,
  ref: React.ForwardedRef<HTMLAnchorElement>
) {
  return (
    <Headless.DataInteractive>
      <NextLink {...props} ref={ref} />
    </Headless.DataInteractive>
  )
})
```
