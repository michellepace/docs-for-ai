[Home](https://catalyst.tailwindui.com/)

[Demo](https://catalyst-demo.tailwindui.com/) [Docs](https://catalyst.tailwindui.com/docs) [Buy UI Kit →](https://tailwindcss.com/plus/templates/catalyst)

Getting startedSidebar layoutStacked layoutAuth layoutAlertAvatarBadgeButtonCheckboxComboboxDescription listDialogDividerDropdownFieldsetHeadingInputListboxNavbarPaginationRadio buttonSelectSidebarSwitchTableTextTextarea

# Listbox

A painstakingly re-engineered select menu, just so you can put a flag in it or have a placeholder.

Project status
Active

```tsx
import { Field, Label } from '@/components/fieldset'
import { Listbox, ListboxLabel, ListboxOption } from '@/components/listbox'

function Example() {
  return (
    <Field>
      <Label>Project status</Label>
      <Listbox name="status" defaultValue="active">
        <ListboxOption value="active">
          <ListboxLabel>Active</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="paused">
          <ListboxLabel>Paused</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="delayed">
          <ListboxLabel>Delayed</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="canceled">
          <ListboxLabel>Canceled</ListboxLabel>
        </ListboxOption>
      </Listbox>
    </Field>
  )
}
```

## Component API

### Listbox

Extends the Headless UI `<Listbox>` component

| Prop | Default | Description |
| :-- | :-- | :-- |
| `disabled` | `false` | Whether or not to disable the listbox. |
| `invalid` | `false` | Whether or not the listbox has a validation error. |
| `name` | - | The name to use when submitting an HTML form. |
| `defaultValue` | - | The initial value for the listbox. |
| `value` | - | The controlled value of the listbox. |
| `onChange` | - | Handler to call when the listbox value changes. |
| `placeholder` | - | The text to show when no option is selected. |

### ListboxOption

Extends the Headless UI `<ListboxOption>` component

| Prop | Default | Description |
| :-- | :-- | :-- |
| `value` | - | The option value. |

### ListboxLabel

Extends the JSX `<span>` element. This component does not expose any component-specific props.

### ListboxDescription

Extends the JSX `<span>` element. This component does not expose any component-specific props.

### Field

Extends the Headless UI `<Field>` component

| Prop | Default | Description |
| :-- | :-- | :-- |
| `disabled` | `false` | Whether or not to disable the entire field. |

### Label

Extends the Headless UI `<Label>` component. This component does not expose any component-specific props.

### Description

Extends the Headless UI `<Description>` component. This component does not expose any component-specific props.

### ErrorMessage

Extends the Headless UI `<Description>` component. This component does not expose any component-specific props.

## Examples

### Basic example

Use the `Listbox`, `ListboxOption`, and `ListboxLabel` components to build a basic listbox:

Active

```tsx
import { Listbox, ListboxLabel, ListboxOption } from '@/components/listbox'

function Example() {
  return (
    <Listbox name="status" defaultValue="active" aria-label="Project status">
      <ListboxOption value="active">
        <ListboxLabel>Active</ListboxLabel>
      </ListboxOption>
      <ListboxOption value="paused">
        <ListboxLabel>Paused</ListboxLabel>
      </ListboxOption>
      <ListboxOption value="delayed">
        <ListboxLabel>Delayed</ListboxLabel>
      </ListboxOption>
      <ListboxOption value="canceled">
        <ListboxLabel>Canceled</ListboxLabel>
      </ListboxOption>
    </Listbox>
  )
}
```

Make sure to provide an `aria-label` for assistive technology, or connect the `Listbox` to your own `<label>` element
using an `id`.

### With label

Wrap a `Label` and `Listbox` with the `Field` component to automatically associate them using a generated ID:

Project status
Active

```tsx
import { Field, Label } from '@/components/fieldset'
import { Listbox, ListboxLabel, ListboxOption } from '@/components/listbox'

function Example() {
  return (
    <Field>
      <Label>Project status</Label>
      <Listbox name="status" defaultValue="active">
        <ListboxOption value="active">
          <ListboxLabel>Active</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="paused">
          <ListboxLabel>Paused</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="delayed">
          <ListboxLabel>Delayed</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="canceled">
          <ListboxLabel>Canceled</ListboxLabel>
        </ListboxOption>
      </Listbox>
    </Field>
  )
}
```

### With description

Use the `Description` component to add a description above or below your `Listbox`:

Project status

This will be visible to clients on the project.

Active

```tsx
import { Description, Field, Label } from '@/components/fieldset'
import { Listbox, ListboxLabel, ListboxOption } from '@/components/listbox'

function Example() {
  return (
    <Field>
      <Label>Project status</Label>
      <Description>This will be visible to clients on the project.</Description>
      <Listbox name="status" defaultValue="active">
        <ListboxOption value="active">
          <ListboxLabel>Active</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="paused">
          <ListboxLabel>Paused</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="delayed">
          <ListboxLabel>Delayed</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="canceled">
          <ListboxLabel>Canceled</ListboxLabel>
        </ListboxOption>
      </Listbox>
    </Field>
  )
}
```

### With placeholder

Use the `placeholder` prop to add a placeholder to your `Listbox` when no value is selected:

Project statusSelect status…

```tsx
import { Field, Label } from '@/components/fieldset'
import { Listbox, ListboxLabel, ListboxOption } from '@/components/listbox'

function Example() {
  return (
    <Field>
      <Label>Project status</Label>
      <Listbox name="status" placeholder="Select status&hellip;">
        <ListboxOption value="active">
          <ListboxLabel>Active</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="paused">
          <ListboxLabel>Paused</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="delayed">
          <ListboxLabel>Delayed</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="canceled">
          <ListboxLabel>Canceled</ListboxLabel>
        </ListboxOption>
      </Listbox>
    </Field>
  )
}
```

### With avatars

Add an `Avatar` to a `ListboxOption` by inserting it before your `ListboxLabel`:

Assigned to
LA![User avatar](https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80)Leslie Alexander

```tsx
import { Avatar } from '@/components/avatar'
import { Field, Label } from '@/components/fieldset'
import { Listbox, ListboxLabel, ListboxOption } from '@/components/listbox'

function Example({ users }) {
  return (
    <Field>
      <Label>Assigned to</Label>
      <Listbox name="user">
        {users.map((user) => (
          <ListboxOption key={user.id} value={user}>
            <Avatar src={user.avatarUrl} initials={user.initials} className="bg-purple-500 text-white" alt="" />
            <ListboxLabel>{user.name}</ListboxLabel>
          </ListboxOption>
        ))}
      </Listbox>
    </Field>
  )
}
```

### With icons

Add an icon to a `ListboxOption` by inserting it before your `ListboxLabel`:

Alignment
Left

```tsx
import { Field, Label } from '@/components/fieldset'
import { Listbox, ListboxLabel, ListboxOption } from '@/components/listbox'
import { Bars3BottomLeftIcon, Bars3BottomRightIcon, Bars3Icon } from '@heroicons/react/16/solid'

function Example() {
  return (
    <Field>
      <Label>Alignment</Label>
      <Listbox name="alignment" defaultValue="left">
        <ListboxOption value="left">
          <Bars3BottomLeftIcon />
          <ListboxLabel>Left</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="right">
          <Bars3BottomRightIcon />
          <ListboxLabel>Right</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="justified">
          <Bars3Icon />
          <ListboxLabel>Justified</ListboxLabel>
        </ListboxOption>
      </Listbox>
    </Field>
  )
}
```

The `ListboxOption` component is designed to work best with 16×16 icons.

If you're using your own custom icons, make sure they include the `data-slot="icon"` prop so they receive the correct
styles.

### With flags

Add a flag icon to a `ListboxOption` by inserting it before your `ListboxLabel`, just like any other icon:

Country
Mexico

```tsx
import { Field, Label } from '@/components/fieldset'
import { Listbox, ListboxLabel, ListboxOption } from '@/components/listbox'
import { Flag } from '@/flags'

function Example({ currentCountry, countries }) {
  return (
    <Field>
      <Label>Assigned to</Label>
      <Listbox name="user" defaultValue={currentCountry}>
        {countries.map((country) => (
          <ListboxOption value={country.code} key={country.code}>
            <Flag className="w-5 sm:w-4" code={country.code} />
            <ListboxLabel>{country.name}</ListboxLabel>
          </ListboxOption>
        ))}
      </Listbox>
    </Field>
  )
}
```

We like the 16×12 flag icons from [Flagpack](https://flagpack.xyz/), a great set of open-source flag icons.

### With secondary text

Use the `ListboxDescription` component to add secondary text to a listbox option:

User
Dries Vincent@driesvincent

```tsx
import { Field, Label } from '@/components/fieldset'
import { Listbox, ListboxDescription, ListboxLabel, ListboxOption } from '@/components/listbox'

function Example({ users }) {
  return (
    <Field>
      <Label>User</Label>
      <Listbox name="user">
        {users.map((user) => (
          <ListboxOption key={user.id} value={user}>
            <ListboxLabel>{user.name}</ListboxLabel>
            <ListboxDescription>@{user.handle}</ListboxDescription>
          </ListboxOption>
        ))}
      </Listbox>
    </Field>
  )
}
```

### Disabled state

Add the `disabled` prop to the `Field` component to disable a `Listbox` and the associated `Label`:

Project status
Delayed

```tsx
import { Field, Label } from '@/components/fieldset'
import { Listbox, ListboxLabel, ListboxOption } from '@/components/listbox'

function Example() {
  return (
    <Field disabled>
      <Label>Project status</Label>
      <Listbox name="status" defaultValue="delayed">
        <ListboxOption value="active">
          <ListboxLabel>Active</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="paused">
          <ListboxLabel>Paused</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="delayed">
          <ListboxLabel>Delayed</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="canceled">
          <ListboxLabel>Canceled</ListboxLabel>
        </ListboxOption>
      </Listbox>
    </Field>
  )
}
```

You can also disable a listbox outside of a `Field` by adding the `disabled` prop directly to the `Listbox` itself.

### Validation errors

Add the `invalid` prop to the `Listbox` component to indicate a validation error, and render the error using the
`ErrorMessage` component:

Project statusSelect status…

A project status is required.

```tsx
import { ErrorMessage, Field, Label } from '@/components/fieldset'
import { Listbox, ListboxLabel, ListboxOption } from '@/components/listbox'

function Example({ errors }) {
  return (
    <Field invalid>
      <Label>Project status</Label>
      <Listbox name="status" placeholder="Select status&hellip;" invalid={errors.has('status')}>
        <ListboxOption value="active">
          <ListboxLabel>Active</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="paused">
          <ListboxLabel>Paused</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="delayed">
          <ListboxLabel>Delayed</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="canceled">
          <ListboxLabel>Canceled</ListboxLabel>
        </ListboxOption>
      </Listbox>
      {errors.has('status') && <ErrorMessage>{errors.get('status')}</ErrorMessage>}
    </Field>
  )
}
```

### Constraining width

Use the `className` prop on the `Listbox` component to make layout adjustments like adjusting the max-width:

Day of the week
Monday

```tsx
import { Field, Label } from '@/components/fieldset'
import { Listbox, ListboxLabel, ListboxOption } from '@/components/listbox'

function Example() {
  return (
    <Field>
      <Label>Day of the week</Label>
      <Listbox className="max-w-40" name="day_of_the_week" defaultValue="Monday">
        <ListboxOption value="Monday">
          <ListboxLabel>Monday</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="Tuesday">
          <ListboxLabel>Tuesday</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="Wednesday">
          <ListboxLabel>Wednesday</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="Thursday">
          <ListboxLabel>Thursday</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="Friday">
          <ListboxLabel>Friday</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="Saturday">
          <ListboxLabel>Saturday</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="Sunday">
          <ListboxLabel>Sunday</ListboxLabel>
        </ListboxOption>
      </Listbox>
    </Field>
  )
}
```

Be aware that the `className` prop is a sharp knife — make sure to only add classes that don't conflict with classes the
component already includes or you'll get unexpected results.

### With custom layout

Use the unstyled `Field` component from `@headlessui/react` directly instead of the styled `Field` component to
implement a custom layout:

Project status
Active

```tsx
import { Label } from '@/components/fieldset'
import { Listbox, ListboxLabel, ListboxOption } from '@/components/listbox'
import * as Headless from '@headlessui/react'

function Example() {
  return (
    <Headless.Field className="flex items-baseline justify-center gap-6">
      <Label>Project status</Label>
      <Listbox name="status" defaultValue="active" className="max-w-48">
        <ListboxOption value="active">
          <ListboxLabel>Active</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="paused">
          <ListboxLabel>Paused</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="delayed">
          <ListboxLabel>Delayed</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="canceled">
          <ListboxLabel>Canceled</ListboxLabel>
        </ListboxOption>
      </Listbox>
    </Headless.Field>
  )
}
```

Using the unstyled `Field` component will ensure important accessibility features are still handled for you like
generating IDs and associating elements using `aria-*` attributes.

### Controlled component

Use the normal `value` and `onChange` props to use the `Listbox` component as a controlled component:

Project status
Active

```tsx
import { Field, Label } from '@/components/fieldset'
import { Listbox, ListboxLabel, ListboxOption } from '@/components/listbox'
import { useState } from 'react'

function Example() {
  let [status, setStatus] = useState('active')

  return (
    <Field>
      <Label>Project status</Label>
      <Listbox name="status" value={status} onChange={setStatus}>
        <ListboxOption value="active">
          <ListboxLabel>Active</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="paused">
          <ListboxLabel>Paused</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="delayed">
          <ListboxLabel>Delayed</ListboxLabel>
        </ListboxOption>
        <ListboxOption value="canceled">
          <ListboxLabel>Canceled</ListboxLabel>
        </ListboxOption>
      </Listbox>
    </Field>
  )
}
```
