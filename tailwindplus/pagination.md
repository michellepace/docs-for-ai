[Home](https://catalyst.tailwindui.com/)

[Demo](https://catalyst-demo.tailwindui.com/) [Docs](https://catalyst.tailwindui.com/docs) [Buy UI Kit →](https://tailwindcss.com/plus/templates/catalyst)

Getting startedSidebar layoutStacked layoutAuth layoutAlertAvatarBadgeButtonCheckboxComboboxDescription listDialogDividerDropdownFieldsetHeadingInputListboxNavbarPaginationRadio buttonSelectSidebarSwitchTableTextTextarea

# Pagination

Because if anyone actually uses this app you're working on, your data isn't going to fit on a single page for long.

```jsx
import {
  Pagination,
  PaginationGap,
  PaginationList,
  PaginationNext,
  PaginationPage,
  PaginationPrevious,
} from '@/components/pagination'

function Example() {
  return (
    <Pagination>
      <PaginationPrevious href="?page=2" />
      <PaginationList>
        <PaginationPage href="?page=1">1</PaginationPage>
        <PaginationPage href="?page=2">2</PaginationPage>
        <PaginationPage href="?page=3" current>
          3
        </PaginationPage>
        <PaginationPage href="?page=4">4</PaginationPage>
        <PaginationGap />
        <PaginationPage href="?page=65">65</PaginationPage>
        <PaginationPage href="?page=66">66</PaginationPage>
      </PaginationList>
      <PaginationNext href="?page=4" />
    </Pagination>
  )
}
```

## Component API

### Pagination

Extends the JSX `<nav>` element.

| Prop | Default | Description |
| :-- | :-- | :-- |
| `aria-label` | `Page navigation` | The name to use when describing the pagination section for screen readers. |
| `className` | - | Any external layout classes to apply. |

### PaginationPrevious

Extends the JSX `<a>` element.

| Prop | Default | Description |
| :-- | :-- | :-- |
| `href` | - | The URL to the previous page. The link will be disabled when omitted. |
| `children` | `Previous` | The text to display in the link. |

### PaginationNext

Extends the JSX `<a>` element.

| Prop | Default | Description |
| :-- | :-- | :-- |
| `href` | - | The URL to the next page. The link will be disabled when omitted. |
| `children` | `Next` | The text to display in the link. |

### PaginationList

This component does not expose any component-specific props.

### PaginationPage

Extends the JSX `<a>` element.

| Prop | Default | Description |
| :-- | :-- | :-- |
| `href` | - | The URL to the page. |
| `children` | - | The page number. |
| `current` | `false` | Whether or not it is the current page. |

### PaginationGap

This component does not expose any component-specific props.

## Examples

### Basic example

Use the `Pagination`, `PaginationPrevious`, `PaginationList`, `PaginationPage`, `PaginationGap`, and `PaginationNext`
components to create a set of pagination links:

```jsx
import {
  Pagination,
  PaginationGap,
  PaginationList,
  PaginationNext,
  PaginationPage,
  PaginationPrevious,
} from '@/components/pagination'

function Example() {
  return (
    <Pagination>
      <PaginationPrevious href="?page=2" />
      <PaginationList>
        <PaginationPage href="?page=1">1</PaginationPage>
        <PaginationPage href="?page=2">2</PaginationPage>
        <PaginationPage href="?page=3" current>
          3
        </PaginationPage>
        <PaginationPage href="?page=4">4</PaginationPage>
        <PaginationGap />
        <PaginationPage href="?page=65">65</PaginationPage>
        <PaginationPage href="?page=66">66</PaginationPage>
      </PaginationList>
      <PaginationNext href="?page=4" />
    </Pagination>
  )
}
```

### Disabling previous/next links

Omit the `href` prop on the `PaginationPrevious` or `PaginationNext` components to disable the previous/next links when
on the first or last page:

```jsx
import {
  Pagination,
  PaginationGap,
  PaginationList,
  PaginationNext,
  PaginationPage,
  PaginationPrevious,
} from '@/components/pagination'

function Example() {
  return (
    <Pagination>
      <PaginationPrevious />
      <PaginationList>
        <PaginationPage href="?page=1" current>
          {'1'}
        </PaginationPage>
        <PaginationPage href="?page=2">2</PaginationPage>
        <PaginationPage href="?page=3">3</PaginationPage>
        <PaginationPage href="?page=4">4</PaginationPage>
        <PaginationGap />
        <PaginationPage href="?page=65">65</PaginationPage>
        <PaginationPage href="?page=66">66</PaginationPage>
      </PaginationList>
      <PaginationNext href="?page=2" />
    </Pagination>
  )
}
```

### Current page active state

Use the `current` prop on the `PaginationPage` component to indicate the current page:

```jsx
import { Pagination, PaginationList, PaginationNext, PaginationPage, PaginationPrevious } from '@/components/pagination'

function Example() {
  return (
    <Pagination>
      <PaginationPrevious href="?page=1" />
      <PaginationList>
        <PaginationPage href="?page=1">1</PaginationPage>
        <PaginationPage href="?page=2" current>
          2
        </PaginationPage>
        <PaginationPage href="?page=3">3</PaginationPage>
      </PaginationList>
      <PaginationNext href="?page=3" />
    </Pagination>
  )
}
```

### Without page links

Omit the `PaginationList` and `PaginationPage` components to render just the previous and next links:

```jsx
import { Pagination, PaginationNext, PaginationPrevious } from '@/components/pagination'

function Example() {
  return (
    <Pagination>
      <PaginationPrevious />
      <PaginationNext href="?after=421c1b0" />
    </Pagination>
  )
}
```
