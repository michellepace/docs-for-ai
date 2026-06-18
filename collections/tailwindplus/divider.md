[Home](https://catalyst.tailwindui.com/)

[Demo](https://catalyst-demo.tailwindui.com/) [Docs](https://catalyst.tailwindui.com/docs) [Buy UI Kit →](https://tailwindcss.com/plus/templates/catalyst)

Getting startedSidebar layoutStacked layoutAuth layoutAlertAvatarBadgeButtonCheckboxComboboxDescription listDialogDividerDropdownFieldsetHeadingInputListboxNavbarPaginationRadio buttonSelectSidebarSwitchTableTextTextarea

# Divider

It's a line.

* * *

```tsx
import { Divider } from '@/components/divider'

function Example() {
  return <Divider />
}
```

## Component API

Divider extends the JSX `<hr>` element.

| Prop | Default | Description |
| :-- | :-- | :-- |
| `soft` | `false` | Whether the divider should use a softer colour. |

## Examples

### Basic example

Use the `Divider` component to add a horizontal rule between items:

* * *

```tsx
import { Divider } from '@/components/divider'

function Example() {
  return <Divider />
}
```

### With reduced contrast

Use the `soft` prop for secondary dividers:

* * *

```tsx
import { Divider } from '@/components/divider'

function Example() {
  return <Divider soft />
}
```

### With spacing

Use utility classes like `my-*` to control the vertical spacing around a divider:

* * *

```tsx
import { Divider } from '@/components/divider'

function Example() {
  return <Divider className="my-6" />
}
```
