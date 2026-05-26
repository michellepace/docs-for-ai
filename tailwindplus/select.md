[Home](https://catalyst.tailwindui.com/)

[Demo](https://catalyst-demo.tailwindui.com/) [Docs](https://catalyst.tailwindui.com/docs) [Buy UI Kit →](https://tailwindcss.com/plus/templates/catalyst)

Getting startedSidebar layoutStacked layoutAuth layoutAlertAvatarBadgeButtonCheckboxComboboxDescription listDialogDividerDropdownFieldsetHeadingInputListboxNavbarPaginationRadio buttonSelectSidebarSwitchTableTextTextarea

# Select

Not a component I'd recommend using for a password field.

Project statusActivePausedDelayedCanceled

```jsx
import { Field, Label } from '@/components/fieldset'
import { Select } from '@/components/select'

function Example() {
  return (
    <Field>
      <Label>Project status</Label>
      <Select name="status">
        <option value="active">Active</option>
        <option value="paused">Paused</option>
        <option value="delayed">Delayed</option>
        <option value="canceled">Canceled</option>
      </Select>
    </Field>
  )
}
```

## Component API

| Prop | Default | Description |
| :-- | :-- | :-- |
| **Select** extends the Headless UI `<Select>` component | | |
| `disabled` | `false` | Whether or not to disable the select. |
| `invalid` | `false` | Whether or not the select has a validation error. |
| `name` | - | The name to use when submitting an HTML form. |
| `defaultValue` | - | The initial value for the select. |
| `value` | - | The controlled value of the select. |
| `onChange` | - | Handler to call when the select value changes. |
| **Field** extends the Headless UI `<Field>` component | | |
| `disabled` | `false` | Whether or not to disable the entire field. |
| **Label** extends the Headless UI `<Label>` component | | |
| | | This component does not expose any component-specific props. |
| **Description** extends the Headless UI `<Description>` component | | |
| | | This component does not expose any component-specific props. |
| **ErrorMessage** extends the Headless UI `<Description>` component | | |
| | | This component does not expose any component-specific props. |

## Examples

### Basic example

Use the `Select` component on its own to render a standalone select without an associated `Label` component:

ActivePausedDelayedCanceled

```jsx
import { Select } from '@/components/select'

function Example() {
  return (
    <Select aria-label="Project status" name="status">
      <option value="active">Active</option>
      <option value="paused">Paused</option>
      <option value="delayed">Delayed</option>
      <option value="canceled">Canceled</option>
    </Select>
  )
}
```

Make sure to provide an `aria-label` for assistive technology, or connect the `Select` to your own `<label>` element
using an `id`.

### With label

Wrap a `Label` and `Select` with the `Field` component to automatically associate them using a generated ID:

Project statusActivePausedDelayedCanceled

```jsx
import { Field, Label } from '@/components/fieldset'
import { Select } from '@/components/select'

function Example() {
  return (
    <Field>
      <Label>Project status</Label>
      <Select name="status">
        <option value="active">Active</option>
        <option value="paused">Paused</option>
        <option value="delayed">Delayed</option>
        <option value="canceled">Canceled</option>
      </Select>
    </Field>
  )
}
```

### With description

Use the `Description` component to add a description above or below your `Select`:

Project status

This will be visible to clients on the project.

ActivePausedDelayedCanceled

```jsx
import { Description, Field, Label } from '@/components/fieldset'
import { Select } from '@/components/select'

function Example() {
  return (
    <Field>
      <Label>Project status</Label>
      <Description>This will be visible to clients on the project.</Description>
      <Select name="status">
        <option value="active">Active</option>
        <option value="paused">Paused</option>
        <option value="delayed">Delayed</option>
        <option value="canceled">Canceled</option>
      </Select>
    </Field>
  )
}
```

### Disabled state

Add the `disabled` prop to the `Field` component to disable a `Select` and the associated `Label`:

Project statusActivePausedDelayedCanceled

```jsx
import { Field, Label } from '@/components/fieldset'
import { Select } from '@/components/select'

function Example() {
  return (
    <Field disabled>
      <Label>Project status</Label>
      <Select name="status">
        <option value="active">Active</option>
        <option value="paused">Paused</option>
        <option value="delayed">Delayed</option>
        <option value="canceled">Canceled</option>
      </Select>
    </Field>
  )
}
```

You can also disable a select outside of a `Field` by adding the `disabled` prop directly to the `Select` itself.

### Validation errors

Add the `invalid` prop to the `Select` component to indicate a validation error, and render the error using the
`ErrorMessage` component:

Project statusSelect a status…ActivePausedDelayedCanceled

A project status is required.

```jsx
import { ErrorMessage, Field, Label } from '@/components/fieldset'
import { Select } from '@/components/select'

function Example({ errors }) {
  return (
    <Field>
      <Label>Project status</Label>
      <Select name="status" defaultValue="" invalid={errors.has('status')}>
        <option value="" disabled>
          Select a status&hellip;
        </option>
        <option value="active">Active</option>
        <option value="paused">Paused</option>
        <option value="delayed">Delayed</option>
        <option value="canceled">Canceled</option>
      </Select>
      {errors.has('status') && <ErrorMessage>{errors.get('status')}</ErrorMessage>}
    </Field>
  )
}
```

### Constraining width

Use the `className` prop on the `Select` component to make layout adjustments like adjusting the max-width:

Day of the weekMondayTuesdayWednesdayThursdayFridaySaturdaySunday

```jsx
import { Field, Label } from '@/components/fieldset'
import { Select } from '@/components/select'

function Example() {
  return (
    <Field>
      <Label>Day of the week</Label>
      <Select className="max-w-40" name="day_of_the_week">
        <option>Monday</option>
        <option>Tuesday</option>
        <option>Wednesday</option>
        <option>Thursday</option>
        <option>Friday</option>
        <option>Saturday</option>
        <option>Sunday</option>
      </Select>
    </Field>
  )
}
```

Be aware that the `className` prop is a sharp knife — make sure to only add classes that don't conflict with classes the
component already includes or you'll get unexpected results.

### With custom layout

Use the unstyled `Field` component from `@headlessui/react` directly instead of the styled `Field` component to
implement a custom layout:

Project statusActivePausedDelayedCanceled

```jsx
import { Label } from '@/components/fieldset'
import { Select } from '@/components/select'
import * as Headless from '@headlessui/react'

function Example() {
  return (
    <Headless.Field className="flex items-baseline justify-center gap-6">
      <Label>Project status</Label>
      <Select name="status" className="max-w-48">
        <option value="active">Active</option>
        <option value="paused">Paused</option>
        <option value="delayed">Delayed</option>
        <option value="canceled">Canceled</option>
      </Select>
    </Headless.Field>
  )
}
```

Using the unstyled `Field` component will ensure important accessibility features are still handled for you like
generating IDs and associating elements using `aria-*` attributes.

### Controlled component

Use the normal `value` and `onChange` props to use the `Select` component as a controlled component:

Project statusActivePausedDelayedCanceled

```jsx
import { Field, Label } from '@/components/fieldset'
import { Select } from '@/components/select'
import { useState } from 'react'

function Example() {
  let [status, setStatus] = useState('active')

  return (
    <Field>
      <Label>Project status</Label>
      <Select name="status" value={status} onChange={(e) => setStatus(e.target.value)}>
        <option value="active">Active</option>
        <option value="paused">Paused</option>
        <option value="delayed">Delayed</option>
        <option value="canceled">Canceled</option>
      </Select>
    </Field>
  )
}
```
