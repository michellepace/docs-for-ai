ContentsMenuExpandLight modeDark modeAuto light/dark, in light modeAuto light/dark, in dark mode[Skip to content](https://mdformat.readthedocs.io/en/stable/users/style.html#furo-main-content)

[Back to top](https://mdformat.readthedocs.io/en/stable/users/style.html#)

[View this page](https://mdformat.readthedocs.io/en/stable/_sources/users/style.md.txt "View this page")

Toggle Light / Dark / Auto color theme

Toggle table of contents sidebar

# Formatting style [¶](https://mdformat.readthedocs.io/en/stable/users/style.html\#formatting-style "Link to this heading")

This document describes, demonstrates, and rationalizes the formatting style that mdformat follows.

Mdformat’s formatting style is crafted so that writing, editing and collaborating on Markdown documents is as smooth as possible.
The style is consistent, and minimizes diffs (for ease of reviewing changes),
sometimes at the cost of some readability.

Mdformat makes sure to only change style, not content.
Once converted to HTML and rendered on screen,
formatted Markdown should yield a result that is visually identical to the unformatted document.
Mdformat CLI includes a safety check that will error and refuse to apply changes to a file
if Markdown AST is not equal before and after formatting.

## Headings [¶](https://mdformat.readthedocs.io/en/stable/users/style.html\#headings "Link to this heading")

For consistency, only ATX headings are used.
Setext headings are reformatted using the ATX style.
ATX headings are used because they can be consistently used for any heading level,
whereas setext headings only allow level 1 and 2 headings.

Input:

```
First level heading
===

Second level heading
---
```

Output:

```
# First level heading

## Second level heading
```

## Bullet lists [¶](https://mdformat.readthedocs.io/en/stable/users/style.html\#bullet-lists "Link to this heading")

Mdformat uses `-` as the bullet list marker.
In the case of consecutive bullet lists,
mdformat alternates between `-` and `*` markers.

## Ordered lists [¶](https://mdformat.readthedocs.io/en/stable/users/style.html\#ordered-lists "Link to this heading")

Mdformat uses `.` as ordered list marker type.
In the case of consecutive ordered lists,
mdformat alternates between `.` and `)` types.

Mdformat uses `1.` or `1)` as the ordered list marker, also for noninital list items.

Input:

```
1. Item A
2. Item B
3. Item C
```

Output:

```
1. Item A
1. Item B
1. Item C
```

This “non-numbering” style was chosen to minimize diffs. But how exactly? Lets imagine we are listing the alphabets, using a proper consecutive numbering style:

```
1. b
2. c
3. d
```

Now we notice an error was made, and that the first character “a” is missing.
We add it as the first item in the list.
As a result, the numbering of every subsequent item in the list will increase by one,
meaning that the diff will touch every line in the list.
The non-numbering style solves this issue: only the added line will show up in the diff.

Mdformat allows consecutive numbering via configuration.

## Code blocks [¶](https://mdformat.readthedocs.io/en/stable/users/style.html\#code-blocks "Link to this heading")

Only fenced code blocks are allowed.
Indented code blocks are reformatted as fenced code blocks.

Fenced code blocks are preferred because they allow setting an info string,
which indented code blocks do not support.

## Code spans [¶](https://mdformat.readthedocs.io/en/stable/users/style.html\#code-spans "Link to this heading")

Length of a code span starting/ending backtick string is reduced to minimum.
Needless space characters are stripped from the front and back,
unless the content contains backticks.

Input:

`````
````Backtick string is reduced.````

` Space is stripped from the front and back... `

```` ...unless a "`" character is present. ````
`````

Output:

```
`Backtick string is reduced.`

`Space is stripped from the front and back...`

`` ...unless a "`" character is present. ``
```

## Inline links [¶](https://mdformat.readthedocs.io/en/stable/users/style.html\#inline-links "Link to this heading")

Redundant angle brackets surrounding a link destination will be removed.

Input:

```
[Python](<https://python.org>)
```

Output:

```
[Python](https://python.org)
```

## Reference links [¶](https://mdformat.readthedocs.io/en/stable/users/style.html\#reference-links "Link to this heading")

All link reference definitions are moved to the bottom of the document,
sorted by label. Unused and duplicate references are removed.

Input:

```
[dupe ref]: https://gitlab.com
[dupe ref]: link1
[unused ref]: link2

Here's a link to [GitLab][dupe ref]
```

Output:

```
Here's a link to [GitLab][dupe ref]

[dupe ref]: https://gitlab.com
```

## Paragraph word wrapping [¶](https://mdformat.readthedocs.io/en/stable/users/style.html\#paragraph-word-wrapping "Link to this heading")

Mdformat by default will not change word wrapping.
The rationale for this is to encourage and support [Semantic Line Breaks](https://sembr.org/),
a technique described by Brian Kernighan in the early 1970s,
yet still as relevant as ever today:

> **Hints for Preparing Documents**
>
> Most documents go through several versions (always more than you
> expected) before they are finally finished. Accordingly, you should
> do whatever possible to make the job of changing them easy.
>
> First, when you do the purely mechanical operations of typing, type
> so subsequent editing will be easy. Start each sentence on a new line.
> Make lines short, and break lines at natural places, such as after
> commas and semicolons, rather than
> randomly. Since
> most people change documents by rewriting phrases and adding, deleting
> and rearranging sentences, these precautions simplify any editing you
> have to do later.
>
> _— Brian W. Kernighan. “UNIX for Beginners”. 1974_

Mdformat allows removing word wrap or setting a target wrap width via configuration.

## Thematic breaks [¶](https://mdformat.readthedocs.io/en/stable/users/style.html\#thematic-breaks "Link to this heading")

Thematic breaks are formatted as a 70 character wide string of underscores.
A wide thematic break is distinguishable,
and visually resembles how a corresponding HTML `<hr>` tag is typically rendered.

## Whitespace [¶](https://mdformat.readthedocs.io/en/stable/users/style.html\#whitespace "Link to this heading")

Mdformat applies consistent whitespace across the board:

- Convert line endings to a single newline character

- Strip paragraph trailing and leading whitespace

- Indent contents of block quotes and list items consistently

- Always separate blocks with a single empty line
(an exception being tight lists where the separator is a single newline character)

- Always end the document in a single newline character
(an exception being an empty document)


## Hard line breaks [¶](https://mdformat.readthedocs.io/en/stable/users/style.html\#hard-line-breaks "Link to this heading")

Hard line breaks are always a backslash preceding a line ending.
The alternative syntax,
two or more spaces before a line ending,
is not used because it is not visible.

Input:

```
Hard line break is here:
Can you see it?
```

Output:

```
Hard line break is here:\
Can you see it?
```

Versions[latest](https://mdformat.readthedocs.io/en/latest/users/style.html)**[stable](https://mdformat.readthedocs.io/en/stable/users/style.html)**On Read the Docs[Project Home](https://app.readthedocs.org/projects/mdformat/?utm_source=mdformat&utm_content=flyout)[Builds](https://app.readthedocs.org/projects/mdformat/builds/?utm_source=mdformat&utm_content=flyout)Search

* * *

[Addons documentation](https://docs.readthedocs.io/page/addons.html?utm_source=mdformat&utm_content=flyout) ― Hosted by
[Read the Docs](https://about.readthedocs.com/?utm_source=mdformat&utm_content=flyout)