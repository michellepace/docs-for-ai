[Home](https://catalyst.tailwindui.com/)

[Demo](https://catalyst-demo.tailwindui.com/) [Docs](https://catalyst.tailwindui.com/docs) [Buy UI Kit →](https://tailwindcss.com/plus/templates/catalyst)

Getting startedSidebar layoutStacked layoutAuth layoutAlertAvatarBadgeButtonCheckboxComboboxDescription listDialogDividerDropdownFieldsetHeadingInputListboxNavbarPaginationRadio buttonSelectSidebarSwitchTableTextTextarea

# Text

For all the lorem ipsum in your Figma designs that you're definitely going to replace with real copy before launch.

This feature is only available to users on the **Business Plan**.

To upgrade, visit your [billing settings](https://catalyst.tailwindui.com/docs/text#).

```tsx
import { Strong, Text, TextLink } from '@/components/text'

function Example() {
  return (
    <Text>
      This feature is only available to users on the <Strong>Business Plan</Strong>. To upgrade, visit your{' '}
      <TextLink href="#">billing settings</TextLink>.
    </Text>
  )
}
```

## Component API

| Prop | Default | Description |
| :-- | :-- | :-- |
| **Text** extends the JSX `<p>` element | | |
| `children` | - | The text the component should render. |
| **TextLink** extends the [`<Link>`](https://catalyst.tailwindui.com/docs#client-side-router-integration) component | | |
| `href` | - | The URL for the link. |
| `children` | - | The text the component should render. |
| **Strong** extends the JSX `<strong>` element | | |
| `children` | - | The text the component should render. |
| **Code** extends the JSX `<code>` element | | |
| `children` | - | The text the component should render. |

## Examples

### Basic example

Use the `Text` component for any custom paragraph text that should match the style of the text built in to your other
components:

Deleting your account is permanent, and your data will not be able to be recovered.

```tsx
import { Text } from '@/components/text'

function Example() {
  return <Text>Deleting your account is permanent, and your data will not be able to be recovered.</Text>
}
```

Paragraphs using `Text` are responsive and automatically adapt to dark mode.

### With link

Use the `TextLink` component for any links within a `Text` component:

Deleting your account is permanent, and your data will not be able to be recovered. If you still want to use this account in the future, learn about [pausing your subscription](https://catalyst.tailwindui.com/docs/text#) instead.

```tsx
import { Text, TextLink } from '@/components/text'

function Example() {
  return (
    <Text>
      Deleting your account is permanent, and your data will not be able to be recovered. If you still want to use this
      account in the future, learn about <TextLink href="#">pausing your subscription</TextLink> instead.
    </Text>
  )
}
```

### With strong

Use the `Strong` component for any text you want to emphasize within a `Text` component:

Deleting your account is permanent, and **your account data cannot be recovered**.

```tsx
import { Strong, Text } from '@/components/text'

function Example() {
  return (
    <Text>
      Deleting your account is permanent, and <Strong>your account data cannot be recovered</Strong>.
    </Text>
  )
}
```

### With code

Use the `Code` component for any inline code symbols within a `Text` component:

Your new API token is `BaVrRKpRMS_ndKU`. Store this token somewhere safe as it will only be displayed once.

```tsx
import { Code, Text } from '@/components/text'

function Example() {
  return (
    <Text>
      Your new API token is <Code>BaVrRKpRMS_ndKU</Code>. Store this token somewhere safe as it will only be displayed
      once.
    </Text>
  )
}
```
