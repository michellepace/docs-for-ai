[Home](https://catalyst.tailwindui.com/)

[Demo](https://catalyst-demo.tailwindui.com/) [Docs](https://catalyst.tailwindui.com/docs) [Buy UI Kit →](https://tailwindcss.com/plus/templates/catalyst)

Getting startedSidebar layoutStacked layoutAuth layoutAlertAvatarBadgeButtonCheckboxComboboxDescription listDialogDividerDropdownFieldsetHeadingInputListboxNavbarPaginationRadio buttonSelectSidebarSwitchTableTextTextarea

# Description list

For when you need to take the data from just one table row and somehow turn it into its own entire table to keep the
page from feeling too empty.

CustomerMichael FosterEventBear Hug: Live in ConcertAmount$150.00 USDAmount after exchange rateUS$150.00 → CA$199.79Fee$4.79 USDNet$1,955.00

```tsx
import { DescriptionDetails, DescriptionList, DescriptionTerm } from '@/components/description-list'

function Example() {
  return (
    <DescriptionList>
      <DescriptionTerm>Customer</DescriptionTerm>
      <DescriptionDetails>Michael Foster</DescriptionDetails>

      <DescriptionTerm>Event</DescriptionTerm>
      <DescriptionDetails>Bear Hug: Live in Concert</DescriptionDetails>

      <DescriptionTerm>Amount</DescriptionTerm>
      <DescriptionDetails>$150.00 USD</DescriptionDetails>

      <DescriptionTerm>Amount after exchange rate</DescriptionTerm>
      <DescriptionDetails>US$150.00 &rarr; CA$199.79</DescriptionDetails>

      <DescriptionTerm>Fee</DescriptionTerm>
      <DescriptionDetails>$4.79 USD</DescriptionDetails>

      <DescriptionTerm>Net</DescriptionTerm>
      <DescriptionDetails>$1,955.00</DescriptionDetails>
    </DescriptionList>
  )
}
```

## Component API

| Prop | Default | Description |
| :-- | :-- | :-- |
| DescriptionList | extends the JSX `<dl>` element | This component does not expose any component-specific props. |
| DescriptionTerm | extends the JSX `<dt>` element | This component does not expose any component-specific props. |
| DescriptionDetails | extends the JSX `<dd>` element | This component does not expose any component-specific props. |

## Examples

### Basic example

Use the `DescriptionList`, `DescriptionTerm`, and `DescriptionDetails` components to build a description list:

CustomerLeslie AlexanderEmail[leslie.alexander@example.com](mailto:leslie.alexander@example.com)AccessAdmin

```tsx
import { DescriptionDetails, DescriptionList, DescriptionTerm } from '@/components/description-list'

function Example() {
  return (
    <DescriptionList>
      <DescriptionTerm>Customer</DescriptionTerm>
      <DescriptionDetails>Leslie Alexander</DescriptionDetails>

      <DescriptionTerm>Email</DescriptionTerm>
      <DescriptionDetails>leslie.alexander@example.com</DescriptionDetails>

      <DescriptionTerm>Access</DescriptionTerm>
      <DescriptionDetails>Admin</DescriptionDetails>
    </DescriptionList>
  )
}
```

### With heading

Use the `Subheading` component to add a heading to the description list:

## Order \#1011

CustomerMichael FosterEventBear Hug: Live in ConcertAmount$150.00 USDAmount after exchange rateUS$150.00 → CA$199.79Fee$4.79 USDNet$1,955.00

```tsx
import { DescriptionDetails, DescriptionList, DescriptionTerm } from '@/components/description-list'
import { Subheading } from '@/components/heading'

function Example() {
  return (
    <>
      <Subheading>Order #1011</Subheading>
      <DescriptionList className="mt-4">
        <DescriptionTerm>Customer</DescriptionTerm>
        <DescriptionDetails>Michael Foster</DescriptionDetails>

        <DescriptionTerm>Event</DescriptionTerm>
        <DescriptionDetails>Bear Hug: Live in Concert</DescriptionDetails>

        <DescriptionTerm>Amount</DescriptionTerm>
        <DescriptionDetails>$150.00 USD</DescriptionDetails>

        <DescriptionTerm>Amount after exchange rate</DescriptionTerm>
        <DescriptionDetails>US$150.00 &rarr; CA$199.79</DescriptionDetails>

        <DescriptionTerm>Fee</DescriptionTerm>
        <DescriptionDetails>$4.79 USD</DescriptionDetails>

        <DescriptionTerm>Net</DescriptionTerm>
        <DescriptionDetails>$1,955.00</DescriptionDetails>
      </DescriptionList>
    </>
  )
}
```
