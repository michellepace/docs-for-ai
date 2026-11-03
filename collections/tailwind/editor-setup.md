[Home](https://tailwindcss.com/) v4.3

`⌘K`  `Ctrl K` [Docs](https://tailwindcss.com/docs) [Play](https://play.tailwindcss.com/) [Blog](https://tailwindcss.com/blog) [Showcase](https://tailwindcss.com/showcase) [Partners](https://tailwindcss.com/partners) [Plus](https://tailwindcss.com/plus?ref=top) [GitHub repository](https://github.com/tailwindlabs/tailwindcss)

1. Getting started
2. Editor setup

Getting started

# Editor setup

Tooling to improve the developer experience when working with Tailwind CSS.

## [Syntax support](https://tailwindcss.com/docs/editor-setup\#syntax-support)

Tailwind CSS uses custom CSS syntax like `@theme`, `@variant`, and `@source`, and in some editors this can trigger warnings or errors where these rules aren't recognized.

If you're using VS Code, our official [Tailwind CSS IntelliSense](https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss) plugin includes a dedicated Tailwind CSS language mode that has support for all of the custom at-rules and functions Tailwind uses.

In some cases, you may need to disable native CSS linting/validations if your editor is very strict about the syntax it expects in your CSS files.

## [Cursor](https://tailwindcss.com/docs/editor-setup\#cursor)

[Cursor](https://cursor.com/?utm_source=tailwind) is an AI-native code editor with features like context-aware autocomplete and built-in coding agents. Since it supports VS Code extensions, all of the Tailwind CSS tooling you're already familiar with works out of the box – including our official [Tailwind CSS IntelliSense](https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss) extension and the [Prettier plugin](https://github.com/tailwindlabs/prettier-plugin-tailwindcss) for class sorting.

![Tailwind CSS IntelliSense extension for Cursor](https://tailwindcss.com/_next/static/media/cursor-intellisense.0wd1~kc6nuaa5.png)

Check out and download [Cursor](https://cursor.com/?utm_source=tailwind).

## [Zed](https://tailwindcss.com/docs/editor-setup\#zed)

[Zed](https://zed.dev/?utm_source=tailwind) is a fast, modern code editor, designed from the ground-up for cutting-edge development workflows, including agentic editing with AI. It has built-in support for Tailwind CSS autocompletions, linting, and hover previews, without the need to install and configure a separate extension. It also integrates tightly with Prettier, so our official [Prettier plugin](https://github.com/tailwindlabs/prettier-plugin-tailwindcss) works seamlessly with Zed when installed.

![Built-in support for Tailwind CSS in Zed via Tailwind CSS IntelliSense](https://tailwindcss.com/_next/static/media/zed-intellisense.14u74b6adm4bq.png)

Check out [Zed](https://zed.dev/?utm_source=tailwind) and learn more about [how it works with Tailwind CSS](https://zed.dev/docs/languages/tailwindcss?utm_source=tailwind).

## [IntelliSense for VS Code](https://tailwindcss.com/docs/editor-setup\#intellisense-for-vs-code)

The official [Tailwind CSS IntelliSense](https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss) extension for Visual Studio Code enhances the Tailwind development experience by providing users with advanced features such as autocomplete, syntax highlighting, and linting.

![Tailwind CSS IntelliSense extension for Visual Studio Code](https://tailwindcss.com/_next/static/media/intellisense.0tuj65em1.0j..png)

- **Autocomplete** — providing intelligent suggestions for utility classes, as well as [CSS functions and directives](https://tailwindcss.com/docs/functions-and-directives).
- **Linting** — highlighting errors and potential bugs in both your CSS and your markup.
- **Hover previews** — revealing the complete CSS for utility classes when you hover over them.
- **Syntax highlighting** — so that Tailwind features that use custom CSS syntax are highlighted correctly.

Check out the project [on GitHub](https://github.com/tailwindcss/intellisense) to learn more, or [add it to Visual Studio Code](vscode:extension/bradlc.vscode-tailwindcss) to get started now.

## [Class sorting with Prettier](https://tailwindcss.com/docs/editor-setup\#class-sorting-with-prettier)

We maintain an official [Prettier plugin](https://github.com/tailwindlabs/prettier-plugin-tailwindcss) for Tailwind CSS that automatically sorts your classes following our [recommended class order](https://tailwindcss.com/blog/automatic-class-sorting-with-prettier#how-classes-are-sorted).

![](https://tailwindcss.com/_next/static/media/prettier-banner.0tuovfv573y0i.jpg)

It works seamlessly with custom Tailwind configurations, and because it’s just a Prettier plugin, it works anywhere Prettier works — including every popular editor and IDE, and of course on the command line.

HTML

```
<!-- Before --><button class="text-white px-4 sm:px-8 py-2 sm:py-3 bg-sky-700 hover:bg-sky-800">Submit</button><!-- After --><button class="bg-sky-700 px-4 py-2 text-white hover:bg-sky-800 sm:px-8 sm:py-3">Submit</button>
```

Check out the plugin [on GitHub](https://github.com/tailwindlabs/prettier-plugin-tailwindcss) to learn more and get started.

## [JetBrains IDEs](https://tailwindcss.com/docs/editor-setup\#jetbrains-ides)

JetBrains IDEs like WebStorm, PhpStorm, and others include support for intelligent Tailwind CSS completions in your HTML.

[Learn more about Tailwind CSS support in JetBrains IDEs →](https://www.jetbrains.com/help/webstorm/tailwind-css.html)

### On this page

- [Syntax support](https://tailwindcss.com/docs/editor-setup#syntax-support)
- [Cursor](https://tailwindcss.com/docs/editor-setup#cursor)
- [Zed](https://tailwindcss.com/docs/editor-setup#zed)
- [IntelliSense for VS Code](https://tailwindcss.com/docs/editor-setup#intellisense-for-vs-code)
- [Class sorting with Prettier](https://tailwindcss.com/docs/editor-setup#class-sorting-with-prettier)
- [JetBrains IDEs](https://tailwindcss.com/docs/editor-setup#jetbrains-ides)

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