[Home](https://catalyst.tailwindui.com/)

[Demo](https://catalyst-demo.tailwindui.com/) [Docs](https://catalyst.tailwindui.com/docs) [Buy UI Kit →](https://tailwindcss.com/plus/templates/catalyst)

Getting startedSidebar layoutStacked layoutAuth layoutAlertAvatarBadgeButtonCheckboxComboboxDescription listDialogDividerDropdownFieldsetHeadingInputListboxNavbarPaginationRadio buttonSelectSidebarSwitchTableTextTextarea

# Input

If web applications didn't need inputs, computers wouldn't have keyboards.

Full name

```tsx
import { Field, Label } from '@/components/fieldset'
import { Input } from '@/components/input'

function Example() {
  return (
    <Field>
      <Label>Full name</Label>
      <Input name="full_name" />
    </Field>
  )
}
```

## Component API

### Input

Extends the Headless UI `<Input>` component

| Prop | Default | Description |
| :-- | :-- | :-- |
| `disabled` | `false` | Whether or not to disable the input. |
| `invalid` | `false` | Whether or not the input has a validation error. |
| `name` | - | The name to use when submitting an HTML form. |
| `defaultValue` | - | The initial value for the input. |
| `value` | - | The controlled value of the input. |
| `onChange` | - | Handler to call when the input value changes. |

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

Use the `Input` component on its own to render a standalone input without an associated `Label` component:

```tsx
import { Input } from '@/components/input'

function Example() {
  return <Input aria-label="Full name" name="full_name" />
}
```

Make sure to provide an `aria-label` for assistive technology, or connect the `Input` to your own `<label>` element
using an `id`.

### With label

Wrap a `Label` and `Input` with the `Field` component to automatically associate them using a generated ID:

Full name

```tsx
import { Field, Label } from '@/components/fieldset'
import { Input } from '@/components/input'

function Example() {
  return (
    <Field>
      <Label>Full name</Label>
      <Input name="full_name" />
    </Field>
  )
}
```

### With description

Use the `Description` component to add a description above or below your `Input`:

Product name

Use the name you'd like people to see in their cart.

```tsx
import { Description, Field, Label } from '@/components/fieldset'
import { Input } from '@/components/input'

function Example() {
  return (
    <Field>
      <Label>Product name</Label>
      <Description>Use the name you'd like people to see in their cart.</Description>
      <Input name="product_name" />
    </Field>
  )
}
```

### With icon

Wrap an icon and `Input` with the `InputGroup` component to render an input with an icon:

```tsx
import { Input, InputGroup } from '@/components/input'
import { MagnifyingGlassIcon } from '@heroicons/react/16/solid'

function Example() {
  return (
    <InputGroup>
      <MagnifyingGlassIcon />
      <Input name="search" placeholder="Search&hellip;" aria-label="Search" />
    </InputGroup>
  )
}
```

The `InputGroup` component is designed to work best with 16×16 icons.

If you're using your own custom icons, make sure they include the `data-slot="icon"` prop so they receive the correct
styles.

### Setting the type

Use the `type` prop to set the input type to any supported text input type:

Your website

```tsx
import { Field, Label } from '@/components/fieldset'
import { Input } from '@/components/input'

function Example() {
  return (
    <Field>
      <Label>Your website</Label>
      <Input type="url" name="url" />
    </Field>
  )
}
```

The supported types are `email`, `number`, `password`, `search`, `tel`, `text`, `url`, `date`, `datetime-local`,
`month`, `time`, and `week`.

### Disabled state

Add the `disabled` prop to the `Field` component to disable an `Input` and the associated `Label`:

Full name

```tsx
import { Field, Label } from '@/components/fieldset'
import { Input } from '@/components/input'

function Example() {
  return (
    <Field disabled>
      <Label>Full name</Label>
      <Input name="full_name" />
    </Field>
  )
}
```

You can also disable an input outside of a `Field` by adding the `disabled` prop directly to the `Input` itself.

### Validation errors

Add the `invalid` prop to the `Input` component to indicate a validation error, and render the error using the
`ErrorMessage` component:

Full name

This field is required.

```tsx
import { ErrorMessage, Field, Label } from '@/components/fieldset'
import { Input } from '@/components/input'

function Example({ errors }) {
  return (
    <Field>
      <Label>Full name</Label>
      <Input name="full_name" invalid={errors.has('full_name')} />
      {errors.has('full_name') && <ErrorMessage>{errors.get('full_name')}</ErrorMessage>}
    </Field>
  )
}
```

### Constraining width

Use the `className` prop on the `Input` component to make layout adjustments like adjusting the max-width:

CVC

```tsx
import { Field, Label } from '@/components/fieldset'
import { Input } from '@/components/input'

function Example() {
  return (
    <Field>
      <Label>CVC</Label>
      <Input className="max-w-24" name="cvc" pattern="[0-9]*" />
    </Field>
  )
}
```

Be aware that the `className` prop is a sharp knife — make sure to only add classes that don't conflict with classes the
component already includes or you'll get unexpected results.

### With custom layout

Use the unstyled `Field` component from `@headlessui/react` directly instead of the styled `Field` component to
implement a custom layout:

Full name

```tsx
import { Label } from '@/components/fieldset'
import { Input } from '@/components/input'
import * as Headless from '@headlessui/react'

function Example() {
  return (
    <Headless.Field className="flex items-center justify-center gap-6">
      <Label>Full name</Label>
      <Input name="full_name" className="max-w-48" />
    </Headless.Field>
  )
}
```

Using the unstyled `Field` component will ensure important accessibility features are still handled for you like
generating IDs and associating elements using `aria-*` attributes.

### Controlled component

Use the normal `value` and `onChange` props to use the `Input` component as a controlled component:

Full name

```tsx
import { Field, Label } from '@/components/fieldset'
import { Input } from '@/components/input'
import { useState } from 'react'

function Example() {
  let [name, setName] = useState('')

  return (
    <Field>
      <Label>Full name</Label>
      <Input name="full_name" value={name} onChange={(e) => setName(e.target.value)} />
    </Field>
  )
}
```
