[Home](https://catalyst.tailwindui.com/)

[Demo](https://catalyst-demo.tailwindui.com/) [Docs](https://catalyst.tailwindui.com/docs) [Buy UI Kit →](https://tailwindcss.com/plus/templates/catalyst)

Getting startedSidebar layoutStacked layoutAuth layoutAlertAvatarBadgeButtonCheckboxComboboxDescription listDialogDividerDropdownFieldsetHeadingInputListboxNavbarPaginationRadio buttonSelectSidebarSwitchTableTextTextarea

# Badge

Eventually this custom CMS you're probably building is going to need tags.

documentationhelp wantedbug

```tsx
import { Badge } from '@/components/badge'

function Example() {
  return (
    <div className="flex gap-3">
      <Badge color="lime">documentation</Badge>
      <Badge color="purple">help wanted</Badge>
      <Badge color="rose">bug</Badge>
    </div>
  )
}
```

## Component API

| Prop | Default | Description |
| :-- | :-- | :-- |
| - | - | `Badge` extends the JSX `<span>` element |
| `color` | `zinc` | The color of the badge. |
| - | - | `BadgeButton` extends the Headless UI `Button` component or the [`Link`](https://catalyst.tailwindui.com/docs#client-side-router-integration) component |
| `color` | `zinc` | The color of the badge. |
| `href` | - | The target URL when using the button as a link. |

## Examples

### Badge colors

Use the `color` prop to set the color of the badge. For a full list of included color variants, check out the [color reference](https://catalyst.tailwindui.com/docs/badge#color-reference).

### Using as buttons

Use the `BadgeButton` component to render a badge as a button:

documentation

```tsx
import { BadgeButton } from '@/components/badge'

function Example() {
  return <BadgeButton>documentation</BadgeButton>
}
```

### Using as links

Use the `BadgeButton` component with the `href` prop to render a badge as a link:

[documentation](https://catalyst.tailwindui.com/docs/badge#)

```tsx
import { BadgeButton } from '@/components/badge'

function Example() {
  return <BadgeButton href="#">documentation</BadgeButton>
}
```

## Appendix

### Color reference

Catalyst includes 18 badge colors that automatically change between light and dark modes to maintain a consistent level
of contrast:

| Color | Example |
| :-- | :-: |
| `red` | label |
| `orange` | label |
| `amber` | label |
| `yellow` | label |
| `lime` | label |
| `green` | label |
| `emerald` | label |
| `teal` | label |
| `cyan` | label |
| `sky` | label |
| `blue` | label |
| `indigo` | label |
| `violet` | label |
| `purple` | label |
| `fuchsia` | label |
| `pink` | label |
| `rose` | label |
| `zinc` | label |
