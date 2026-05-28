[Home](https://catalyst.tailwindui.com/)

[Demo](https://catalyst-demo.tailwindui.com/) [Docs](https://catalyst.tailwindui.com/docs) [Buy UI Kit →](https://tailwindcss.com/plus/templates/catalyst)

Getting startedSidebar layoutStacked layoutAuth layoutAlertAvatarBadgeButtonCheckboxComboboxDescription listDialogDividerDropdownFieldsetHeadingInputListboxNavbarPaginationRadio buttonSelectSidebarSwitchTableTextTextarea

# Button

You know, those things you click to do just about anything in a web application.

Save changes

```tsx
import { Button } from '@/components/button'

function Example() {
  return <Button>Save changes</Button>
}
```

## Component API

| Prop | Default | Description |
| :-- | :-- | :-- |
| **Button** extends the Headless UI `Button` component or the [`Link`](https://catalyst.tailwindui.com/docs#client-side-router-integration) component | | |
| `type` | `button` | The button type. |
| `color` | `dark/zinc` | The [color variant](https://catalyst.tailwindui.com/docs/button#button-colors) the button should use. |
| `outline` | `false` | Whether to use the [outline button style](https://catalyst.tailwindui.com/docs/button#outline-buttons). |
| `plain` | `false` | Whether to use the [plain button style](https://catalyst.tailwindui.com/docs/button#plain-buttons). |
| `disabled` | `false` | Whether or not to disable the button. |
| `href` | - | The target URL when using the button as a link. |

## Examples

### Button colors

Use the `color` prop to set the button color:

Save changes

```tsx
import { Button } from '@/components/button'

function Example() {
  return <Button color="cyan">Save changes</Button>
}
```

For a full list of included color variants, check out the [solid color reference](https://catalyst.tailwindui.com/docs/button#solid-color-reference).

### Outline buttons

Use the `outline` prop for a secondary button style with no shadows or background color:

Save draft

```tsx
import { Button } from '@/components/button'

function Example() {
  return <Button outline>Save draft</Button>
}
```

### Plain buttons

Use the `plain` prop for a simple button style with no border, shadows or background color:

Save draft

```tsx
import { Button } from '@/components/button'

function Example() {
  return <Button plain>Save draft</Button>
}
```

### Disabled states

Use the `disabled` prop to disable a button and apply disabled styles:

Save changes

```tsx
import { Button } from '@/components/button'

function Example() {
  return <Button disabled>Save changes</Button>
}
```

The `disabled` prop is not supported when using the `href` prop.

### With icon

Icons may be place at the start or end of a button:

Add item

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

The `icon` prop accepts both component constructors like `PlusIcon`, as well as component instances like `<PlusIcon />`.

The `Button` component is designed to work best with 16×16 icons.

If you're using your own custom icons, make sure they include the `data-slot="icon"` prop so they receive the correct
styles.

### Using as a link

Add the `href` prop to render a `Link` that has the same visual styling as a button:

[Get started](https://catalyst.tailwindui.com/docs/button#)

```tsx
import { Button } from '@/components/button'

function Example() {
  return <Button href="/get-started">Get started</Button>
}
```

Link buttons support all of the same props as regular buttons except `disabled`.

## Appendix

### Solid color reference

By default, Catalyst includes three adaptive color variants that automatically change color between light and dark modes
to maintain a consistent level of contrast:

| Color | Example |
| :-- | :-: |
| `dark/zinc` | Submit |
| `light` | Submit |
| `dark/white` | Submit |

Catalyst also includes 20 solid colors that don't change outside of subtle global changes we make to all buttons in dark
mode:

| Color | Example |
| :-- | :-: |
| `dark` | Submit |
| `zinc` | Submit |
| `white` | Submit |
| `red` | Submit |
| `orange` | Submit |
| `amber` | Submit |
| `yellow` | Submit |
| `lime` | Submit |
| `green` | Submit |
| `emerald` | Submit |
| `teal` | Submit |
| `cyan` | Submit |
| `sky` | Submit |
| `blue` | Submit |
| `indigo` | Submit |
| `violet` | Submit |
| `purple` | Submit |
| `fuchsia` | Submit |
| `pink` | Submit |
| `rose` | Submit |
