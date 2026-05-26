[Home](https://tailwindcss.com/) v4.1

`⌘K`  `Ctrl K` [Docs](https://tailwindcss.com/docs) [Blog](https://tailwindcss.com/blog) [Showcase](https://tailwindcss.com/showcase) [Sponsor](https://tailwindcss.com/sponsor) [Plus](https://tailwindcss.com/plus?ref=top) [GitHub repository](https://github.com/tailwindlabs/tailwindcss)

1. Installation
2. Install Tailwind CSS with Next.js

Installation

# Install Tailwind CSS with Next.js

Setting up Tailwind CSS in a Next.js project.

01

#### Create your project

Start by creating a new Next.js project if you don’t have one set up already. The most common approach is to use [Create Next App](https://nextjs.org/docs/api-reference/create-next-app).

Terminal

```
npx create-next-app@latest my-project --typescript --eslint --appcd my-project
```

02

#### Install Tailwind CSS

Install `@tailwindcss/postcss` and its peer dependencies via npm.

Terminal

```
npm install tailwindcss @tailwindcss/postcss postcss
```

03

#### Configure PostCSS Plugins

Create a `postcss.config.mjs` file in the root of your project and add the `@tailwindcss/postcss` plugin to your PostCSS configuration.

postcss.config.mjs

```
const config = {  plugins: {    "@tailwindcss/postcss": {},  },};export default config;
```

04

#### Import Tailwind CSS

Add an `@import` to `./app/globals.css` that imports Tailwind CSS.

globals.css

```
@import "tailwindcss";
```

05

#### Start your build process

Run your build process with `npm run dev`.

Terminal

```
npm run dev
```

06

#### Start using Tailwind in your project

Start using Tailwind’s utility classes to style your content.

page.tsx

```
export default function Home() {  return (    <h1 className="text-3xl font-bold underline">      Hello world!    </h1>  )}
```

Copyright © 2025 Tailwind Labs Inc.· [Trademark Policy](https://tailwindcss.com/brand)