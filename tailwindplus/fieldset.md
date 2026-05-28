[Home](https://catalyst.tailwindui.com/)

[Demo](https://catalyst-demo.tailwindui.com/) [Docs](https://catalyst.tailwindui.com/docs) [Buy UI Kit →](https://tailwindcss.com/plus/templates/catalyst)

Getting startedSidebar layoutStacked layoutAuth layoutAlertAvatarBadgeButtonCheckboxComboboxDescription listDialogDividerDropdownFieldsetHeadingInputListboxNavbarPaginationRadio buttonSelectSidebarSwitchTableTextTextarea

# Fieldset

Something has to hold all these form controls together.

Shipping details

Without this your odds of getting your order are low.

Street address

CountryCanadaMexicoUnited States

We currently only ship to North America.

Delivery notes

If you have a tiger, we'd like to know about it.

```tsx
import { Description, Field, FieldGroup, Fieldset, Label, Legend } from '@/components/fieldset'
import { Input } from '@/components/input'
import { Select } from '@/components/select'
import { Text } from '@/components/text'
import { Textarea } from '@/components/textarea'

function Example() {
  return (
    <form action="/orders" method="POST">
      {/* ... */}
      <Fieldset>
        <Legend>Shipping details</Legend>
        <Text>Without this your odds of getting your order are low.</Text>
        <FieldGroup>
          <Field>
            <Label>Street address</Label>
            <Input name="street_address" />
          </Field>
          <Field>
            <Label>Country</Label>
            <Select name="country">
              <option>Canada</option>
              <option>Mexico</option>
              <option>United States</option>
            </Select>
            <Description>We currently only ship to North America.</Description>
          </Field>
          <Field>
            <Label>Delivery notes</Label>
            <Textarea name="notes" />
            <Description>If you have a tiger, we'd like to know about it.</Description>
          </Field>
        </FieldGroup>
      </Fieldset>
      {/* ... */}
    </form>
  )
}
```

## Component API

### Fieldset

Extends the JSX `<div>` element

| Prop | Default | Description |
| :-- | :-- | :-- |
| `disabled` | `false` | Whether or not to disable the entire fieldset. |

### Legend

Extends the JSX `<div>` element

This component does not expose any component-specific props.

### FieldGroup

Extends the JSX `<div>` element

This component does not expose any component-specific props.

## Examples

### Basic example

Use the `Fieldset`, `Legend`, `Text`, and `FieldGroup` components to group a subset of form controls together:

Shipping details

Without this your odds of getting your order are low.

Street address

CountryCanadaMexicoUnited States

We currently only ship to North America.

Delivery notes

If you have a tiger, we'd like to know about it.

```tsx
import { Description, Field, FieldGroup, Fieldset, Label, Legend } from '@/components/fieldset'
import { Input } from '@/components/input'
import { Select } from '@/components/select'
import { Text } from '@/components/text'
import { Textarea } from '@/components/textarea'

function Example() {
  return (
    <form action="/orders" method="POST">
      {/* ... */}
      <Fieldset>
        <Legend>Shipping details</Legend>
        <Text>Without this your odds of getting your order are low.</Text>
        <FieldGroup>
          <Field>
            <Label>Street address</Label>
            <Input name="street_address" />
          </Field>
          <Field>
            <Label>Country</Label>
            <Select name="country">
              <option>Canada</option>
              <option>Mexico</option>
              <option>United States</option>
            </Select>
            <Description>We currently only ship to North America.</Description>
          </Field>
          <Field>
            <Label>Delivery notes</Label>
            <Textarea name="notes" />
            <Description>If you have a tiger, we'd like to know about it.</Description>
          </Field>
        </FieldGroup>
      </Fieldset>
      {/* ... */}
    </form>
  )
}
```

### Without legend

Use a `Fieldset` with `aria-label` to group a set of form controls together without a `Legend`:

Street address

CountryCanadaMexicoUnited States

We currently only ship to North America.

Delivery notes

If you have a tiger, we'd like to know about it.

```tsx
import { Description, Field, FieldGroup, Fieldset, Label } from '@/components/fieldset'
import { Input } from '@/components/input'
import { Select } from '@/components/select'
import { Textarea } from '@/components/textarea'

function Example() {
  return (
    <form action="/orders" method="POST">
      <Fieldset aria-label="Shipping details">
        <FieldGroup>
          <Field>
            <Label>Street address</Label>
            <Input name="street_address" />
          </Field>
          <Field>
            <Label>Country</Label>
            <Select name="country">
              <option>Canada</option>
              <option>Mexico</option>
              <option>United States</option>
            </Select>
            <Description>We currently only ship to North America.</Description>
          </Field>
          <Field>
            <Label>Delivery notes</Label>
            <Textarea name="notes" />
            <Description>If you have a tiger, we'd like to know about it.</Description>
          </Field>
        </FieldGroup>
      </Fieldset>
    </form>
  )
}
```

### Without role

Use the `FieldGroup` component on its own to use it solely for layout, without adding `role="group"` and announcing it
to assistive technology like a traditional `fieldset`:

Street address

CountryCanadaMexicoUnited States

We currently only ship to North America.

Delivery notes

If you have a tiger, we'd like to know about it.

```tsx
import { Description, Field, FieldGroup, Label } from '@/components/fieldset'
import { Input } from '@/components/input'
import { Select } from '@/components/select'
import { Textarea } from '@/components/textarea'

function Example() {
  return (
    <form action="/orders" method="POST">
      <FieldGroup>
        <Field>
          <Label>Street address</Label>
          <Input name="street_address" />
        </Field>
        <Field>
          <Label>Country</Label>
          <Select name="country">
            <option>Canada</option>
            <option>Mexico</option>
            <option>United States</option>
          </Select>
          <Description>We currently only ship to North America.</Description>
        </Field>
        <Field>
          <Label>Delivery notes</Label>
          <Textarea name="notes" />
          <Description>If you have a tiger, we'd like to know about it.</Description>
        </Field>
      </FieldGroup>
    </form>
  )
}
```

### With grid layout

For more complex layouts like grids, use wrapper elements to create nested form control groups and style them yourself
with utility classes:

Shipping details

Without this your odds of getting your order are low.

First name

Last name

Street address

CountryCanadaMexicoUnited States

Postal code

Delivery notes

If you have a tiger, we'd like to know about it.

```tsx
import { Description, Field, FieldGroup, Fieldset, Label, Legend } from '@/components/fieldset'
import { Input } from '@/components/input'
import { Select } from '@/components/select'
import { Text } from '@/components/text'
import { Textarea } from '@/components/textarea'

function Example() {
  return (
    <form action="/orders" method="POST">
      {/* ... */}
      <Fieldset>
        <Legend>Shipping details</Legend>
        <Text>Without this your odds of getting your order are low.</Text>
        <FieldGroup>
          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 sm:gap-4">
            <Field>
              <Label>First name</Label>
              <Input name="first_name" />
            </Field>
            <Field>
              <Label>Last name</Label>
              <Input name="last_name" />
            </Field>
          </div>
          <Field>
            <Label>Street address</Label>
            <Input name="street_address" />
          </Field>
          <div className="grid grid-cols-1 gap-8 sm:grid-cols-3 sm:gap-4">
            <Field className="sm:col-span-2">
              <Label>Country</Label>
              <Select name="country">
                <option>Canada</option>
                <option>Mexico</option>
                <option>United States</option>
              </Select>
            </Field>
            <Field>
              <Label>Postal code</Label>
              <Input name="postal_code" />
            </Field>
          </div>
          <Field>
            <Label>Delivery notes</Label>
            <Textarea name="notes" />
            <Description>If you have a tiger, we'd like to know about it.</Description>
          </Field>
        </FieldGroup>
      </Fieldset>
      {/* ... */}
    </form>
  )
}
```

### With custom layout

Use a plain `<div>` instead of a `FieldGroup` along with the unstyled `Field` component from `@headlessui/react` to
implement a fully custom layout:

Shipping details

Without this your odds of getting your order are low.

Full name

Street address

CountryCanadaMexicoUnited States

Delivery notes

```tsx
import { Fieldset, Label, Legend } from '@/components/fieldset'
import { Input } from '@/components/input'
import { Select } from '@/components/select'
import { Text } from '@/components/text'
import { Textarea } from '@/components/textarea'
import * as Headless from '@headlessui/react'

function Example() {
  return (
    <form action="/orders" method="POST">
      {/* ... */}
      <Fieldset>
        <Legend>Shipping details</Legend>
        <Text>Without this your odds of getting your order are low.</Text>
        <div data-slot="control" className="grid grid-cols-1 items-center gap-x-4 gap-y-6 sm:grid-cols-3">
          <Headless.Field className="grid grid-cols-subgrid sm:col-span-3">
            <Label>Full name</Label>
            <Input className="mt-3 sm:col-span-2 sm:mt-0" name="full_name" />
          </Headless.Field>
          <Headless.Field className="grid grid-cols-subgrid sm:col-span-3">
            <Label>Street address</Label>
            <Input className="mt-3 sm:col-span-2 sm:mt-0" name="street_address" />
          </Headless.Field>
          <Headless.Field className="grid grid-cols-subgrid sm:col-span-3">
            <Label>Country</Label>
            <Select className="mt-3 sm:col-span-2 sm:mt-0" name="country">
              <option>Canada</option>
              <option>Mexico</option>
              <option>United States</option>
            </Select>
          </Headless.Field>
          <Headless.Field className="grid grid-cols-subgrid sm:col-span-3">
            <Label>Delivery notes</Label>
            <Textarea className="mt-3 sm:col-span-2 sm:mt-0" name="notes" />
          </Headless.Field>
        </div>
      </Fieldset>
      {/* ... */}
    </form>
  )
}
```

Add `data-slot="control"` to a child of your `Fieldset` if you want it to receive the same layout styles as a
`FieldGroup`.

### Disabled state

Add the `disabled` prop to a `Fieldset` component to disable the entire fieldset:

Shipping details

Without this your odds of getting your order are low.

Street address

CountryCanadaMexicoUnited States

We currently only ship to North America.

Delivery notes

If you have a tiger, we'd like to know about it.

```tsx
import { Description, Field, FieldGroup, Fieldset, Label, Legend } from '@/components/fieldset'
import { Input } from '@/components/input'
import { Select } from '@/components/select'
import { Text } from '@/components/text'
import { Textarea } from '@/components/textarea'

function Example() {
  return (
    <form action="/orders" method="POST">
      {/* ... */}
      <Fieldset disabled>
        <Legend>Shipping details</Legend>
        <Text>Without this your odds of getting your order are low.</Text>
        <FieldGroup>
          <Field>
            <Label>Street address</Label>
            <Input name="street_address" />
          </Field>
          <Field>
            <Label>Country</Label>
            <Select name="country">
              <option>Canada</option>
              <option>Mexico</option>
              <option>United States</option>
            </Select>
            <Description>We currently only ship to North America.</Description>
          </Field>
          <Field>
            <Label>Delivery notes</Label>
            <Textarea name="notes" />
            <Description>If you have a tiger, we'd like to know about it.</Description>
          </Field>
        </FieldGroup>
      </Fieldset>
      {/* ... */}
    </form>
  )
}
```
