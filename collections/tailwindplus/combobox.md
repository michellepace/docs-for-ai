[Home](https://catalyst.tailwindui.com/)

[Demo](https://catalyst-demo.tailwindui.com/) [Docs](https://catalyst.tailwindui.com/docs) [Buy UI Kit →](https://tailwindcss.com/plus/templates/catalyst)

Getting startedSidebar layoutStacked layoutAuth layoutAlertAvatarBadgeButtonCheckboxComboboxDescription listDialogDividerDropdownFieldsetHeadingInputListboxNavbarPaginationRadio buttonSelectSidebarSwitchTableTextTextarea

# Combobox

For when you know exactly what you want, but are too lazy to scroll for it.

Assigned to

```tsx
import { Combobox, ComboboxLabel, ComboboxOption } from '@/components/combobox'
import { Field, Label } from '@/components/fieldset'

function Example({ currentUser, users }) {
  return (
    <Field>
      <Label>Assigned to</Label>
      <Combobox name="user" options={users} displayValue={(user) => user?.name} defaultValue={currentUser}>
        {(user) => (
          <ComboboxOption value={user}>
            <ComboboxLabel>{user.name}</ComboboxLabel>
          </ComboboxOption>
        )}
      </Combobox>
    </Field>
  )
}
```

## Component API

**Combobox** extends the Headless UI `<Combobox>` component

| Prop | Default | Description |
| :-- | :-- | :-- |
| `disabled` | `false` | Whether or not to disable the combobox. |
| `invalid` | `false` | Whether the combobox has a validation error. |
| `anchor` | `bottom` | Where to position the combobox dropdown. |
| `name` | - | The name to use when submitting an HTML form. |
| `options` | - | A collection of options to display in the combobox. |
| `filter` | - | A function to filter the options based on the query. |
| `displayValue` | - | The string representation of your option. |
| `defaultValue` | - | The initial value for the combobox. |
| `value` | - | The controlled value of the combobox. |
| `onChange` | - | Handler to call when the value changes. |
| `placeholder` | - | The text to show when no option is selected. |

**ComboboxOption** extends the Headless UI `<ComboboxOption>` component

| Prop | Default | Description |
| :-- | :-- | :-- |
| `value` | - | The option value. |

**ComboboxLabel** extends the JSX `<span>` element

This component does not expose any component-specific props.

**ComboboxDescription** extends the JSX `<span>` element

This component does not expose any component-specific props.

**Field** extends the Headless UI `<Field>` component

| Prop | Default | Description |
| :-- | :-- | :-- |
| `disabled` | `false` | Whether or not to disable the entire field. |

**Label** extends the Headless UI `<Label>` component

This component does not expose any component-specific props.

**Description** extends the Headless UI `<Description>` component

This component does not expose any component-specific props.

**ErrorMessage** extends the Headless UI `<Description>` component

This component does not expose any component-specific props.

## Examples

### Basic example

Use the `Combobox`, `ComboboxOption`, and `ComboboxLabel` components to build a basic combobox:

```tsx
import { Combobox, ComboboxLabel, ComboboxOption } from '@/components/combobox'

function Example({ currentUser, users }) {
  return (
    <Combobox
      name="user"
      options={users}
      displayValue={(user) => user?.name}
      defaultValue={currentUser}
      aria-label="Assigned to"
    >
      {(user) => (
        <ComboboxOption value={user}>
          <ComboboxLabel>{user.name}</ComboboxLabel>
        </ComboboxOption>
      )}
    </Combobox>
  )
}
```

Make sure to provide an `aria-label` for assistive technology, or connect the `Combobox` to your own `<label>` element
using an `id`.

### With label

Wrap a `Label` and `Combobox` with the `Field` component to automatically associate them using a generated ID:

Assigned to

```tsx
import { Combobox, ComboboxLabel, ComboboxOption } from '@/components/combobox'
import { Field, Label } from '@/components/fieldset'

function Example({ currentUser, users }) {
  return (
    <Field>
      <Label>Assigned to</Label>
      <Combobox name="user" options={users} displayValue={(user) => user?.name} defaultValue={currentUser}>
        {(user) => (
          <ComboboxOption value={user}>
            <ComboboxLabel>{user.name}</ComboboxLabel>
          </ComboboxOption>
        )}
      </Combobox>
    </Field>
  )
}
```

### With description

Use the `Description` component to add a description above or below your `Combobox`:

Assigned to

This user will have full access to the project.

```tsx
import { Combobox, ComboboxLabel, ComboboxOption } from '@/components/combobox'
import { Description, Field, Label } from '@/components/fieldset'

function Example({ currentUser, users }) {
  return (
    <Field>
      <Label>Assigned to</Label>
      <Description>This user will have full access to the project.</Description>
      <Combobox name="user" options={users} displayValue={(user) => user?.name} defaultValue={currentUser}>
        {(user) => (
          <ComboboxOption value={user}>
            <ComboboxLabel>{user.name}</ComboboxLabel>
          </ComboboxOption>
        )}
      </Combobox>
    </Field>
  )
}
```

### With placeholder

Use the `placeholder` prop to add a placeholder to your `Combobox` when no value is selected:

Assigned to

```tsx
import { Combobox, ComboboxLabel, ComboboxOption } from '@/components/combobox'
import { Field, Label } from '@/components/fieldset'

function Example({ users }) {
  return (
    <Field>
      <Label>Assigned to</Label>
      <Combobox name="user" options={users} displayValue={(user) => user?.name} placeholder="Select user&hellip;">
        {(user) => (
          <ComboboxOption value={user}>
            <ComboboxLabel>{user.name}</ComboboxLabel>
          </ComboboxOption>
        )}
      </Combobox>
    </Field>
  )
}
```

### With avatars

Add an `Avatar` to a `ComboboxOption` by inserting it before your `ComboboxLabel`:

Assigned to

```tsx
import { Avatar } from '@/components/avatar'
import { Combobox, ComboboxLabel, ComboboxOption } from '@/components/combobox'
import { Field, Label } from '@/components/fieldset'

function Example({ currentUser, users }) {
  return (
    <Field>
      <Label>Assigned to</Label>
      <Combobox name="user" options={users} displayValue={(user) => user?.name} defaultValue={currentUser}>
        {(user) => (
          <ComboboxOption value={user}>
            <Avatar src={user.avatarUrl} initials={user.initials} className="bg-purple-500 text-white" alt="" />
            <ComboboxLabel>{user.name}</ComboboxLabel>
          </ComboboxOption>
        )}
      </Combobox>
    </Field>
  )
}
```

### With flags

Add a flag icon to a `ComboboxOption` by inserting it before your `ComboboxLabel`:

Country

```tsx
import { Combobox, ComboboxLabel, ComboboxOption } from '@/components/combobox'
import { Field, Label } from '@/components/fieldset'
import { Flag } from '@/flags'

function Example({ currentCountry, countries }) {
  return (
    <Field>
      <Label>Country</Label>
      <Combobox
        name="country"
        options={countries}
        displayValue={(country) => country?.name}
        defaultValue={currentCountry}
      >
        {(country) => (
          <ComboboxOption value={country}>
            <Flag className="w-5 sm:w-4" code={country.code} />
            <ComboboxLabel>{country.name}</ComboboxLabel>
          </ComboboxOption>
        )}
      </Combobox>
    </Field>
  )
}
```

We like the 16×12 flag icons from [Flagpack](https://flagpack.xyz/), a great set of open-source flag icons.

### With secondary text

Use the `ComboboxDescription` component to add secondary text to a combobox option:

Assigned to

```tsx
import { Combobox, ComboboxDescription, ComboboxLabel, ComboboxOption } from '@/components/combobox'
import { Field, Label } from '@/components/fieldset'

function Example({ currentUser, users }) {
  return (
    <Field>
      <Label>Assigned to</Label>
      <Combobox name="user" options={users} displayValue={(user) => user?.name} defaultValue={currentUser}>
        {(user) => (
          <ComboboxOption value={user}>
            <ComboboxLabel>{user.name}</ComboboxLabel>
            <ComboboxDescription>{user.role}</ComboboxDescription>
          </ComboboxOption>
        )}
      </Combobox>
    </Field>
  )
}
```

### Disabled state

Add the `disabled` prop to the `Field` component to disable a `Combobox` and the associated `Label`:

Assigned to

```tsx
import { Combobox, ComboboxLabel, ComboboxOption } from '@/components/combobox'
import { Field, Label } from '@/components/fieldset'

function Example({ currentUser, users }) {
  return (
    <Field disabled>
      <Label>Assigned to</Label>
      <Combobox name="user" options={users} displayValue={(user) => user?.name} defaultValue={currentUser}>
        {(user) => (
          <ComboboxOption value={user}>
            <ComboboxLabel>{user.name}</ComboboxLabel>
          </ComboboxOption>
        )}
      </Combobox>
    </Field>
  )
}
```

You can also disable a combobox outside of a `Field` by adding the `disabled` prop directly to the `Combobox` itself.

### Validation errors

Add the `invalid` prop to the `Combobox` component to indicate a validation error, and render the error using the
`ErrorMessage` component:

Assigned to

A user is required.

```tsx
import { Combobox, ComboboxLabel, ComboboxOption } from '@/components/combobox'
import { ErrorMessage, Field, Label } from '@/components/fieldset'

function Example({ currentUser, users }) {
  return (
    <Field>
      <Label>Assigned to</Label>
      <Combobox
        invalid
        name="user"
        options={users}
        displayValue={(user) => user?.name}
        placeholder="Select user&hellip;"
      >
        {(user) => (
          <ComboboxOption value={user}>
            <ComboboxLabel>{user.name}</ComboboxLabel>
          </ComboboxOption>
        )}
      </Combobox>
      <ErrorMessage>A user is required.</ErrorMessage>
    </Field>
  )
}
```

### Constraining width

Use the `className` prop on the `Combobox` component to make layout adjustments like adjusting the max-width:

Currency

```tsx
import { Combobox, ComboboxLabel, ComboboxOption } from '@/components/combobox'
import { Field, Label } from '@/components/fieldset'

function Example({ currentCurrency, currencies }) {
  return (
    <Field>
      <Label>Currency</Label>
      <Combobox
        className="max-w-40"
        name="currency"
        options={currencies}
        displayValue={(currency) => currency?.code}
        defaultValue={currentCurrency}
      >
        {(currency) => (
          <ComboboxOption value={currency}>
            <ComboboxLabel>{currency.code}</ComboboxLabel>
          </ComboboxOption>
        )}
      </Combobox>
    </Field>
  )
}
```

### With custom layout

Use the unstyled `Field` component from `@headlessui/react` directly instead of the styled `Field` component to
implement a custom layout:

Assigned to

```tsx
import { Combobox, ComboboxLabel, ComboboxOption } from '@/components/combobox'
import { Label } from '@/components/fieldset'
import * as Headless from '@headlessui/react'

function Example({ currentUser, users }) {
  return (
    <Headless.Field className="flex grow items-baseline justify-center gap-6">
      <Label>Assigned to</Label>
      <Combobox
        name="user"
        options={users}
        displayValue={(user) => user?.name}
        defaultValue={currentUser}
        className="max-w-48"
      >
        {(user) => (
          <ComboboxOption value={user}>
            <ComboboxLabel>{user.name}</ComboboxLabel>
          </ComboboxOption>
        )}
      </Combobox>
    </Headless.Field>
  )
}
```

### Controlled component

Use the normal `value` and `onChange` props to use the `Combobox` component as a controlled component:

Assigned to

```tsx
import { Combobox, ComboboxLabel, ComboboxOption } from '@/components/combobox'
import { Field, Label } from '@/components/fieldset'
import { useState } from 'react'

function Example({ currentUser, users }) {
  let [user, setUser] = useState(currentUser)

  return (
    <Field>
      <Label>Assigned to</Label>
      <Combobox name="user" options={users} displayValue={(user) => user?.name} value={user} onChange={setUser}>
        {(user) => (
          <ComboboxOption value={user}>
            <ComboboxLabel>{user.name}</ComboboxLabel>
          </ComboboxOption>
        )}
      </Combobox>
    </Field>
  )
}
```

### With custom filtering

Use the `filter` prop to customize how the `Combobox` filters its options:

Assigned to

```tsx
import { Combobox, ComboboxDescription, ComboboxLabel, ComboboxOption } from '@/components/combobox'
import { Field, Label } from '@/components/fieldset'

function Example({ currentUser, users }) {
  return (
    <Field>
      <Label>Assigned to</Label>
      <Combobox
        name="user"
        options={users}
        displayValue={(user) => user?.name}
        defaultValue={currentUser}
        filter={(user, query) =>
          user.name.toLowerCase().includes(query.toLowerCase()) ||
          `@${user.handle}`.toLowerCase().includes(query.toLowerCase())
        }
      >
        {(user) => (
          <ComboboxOption value={user}>
            <ComboboxLabel>{user.name}</ComboboxLabel>
            <ComboboxDescription>@{user.handle}</ComboboxDescription>
          </ComboboxOption>
        )}
      </Combobox>
    </Field>
  )
}
```
