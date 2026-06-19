[Home](https://catalyst.tailwindui.com/)

[Demo](https://catalyst-demo.tailwindui.com/) [Docs](https://catalyst.tailwindui.com/docs) [Buy UI Kit →](https://tailwindcss.com/plus/templates/catalyst)

Getting startedSidebar layoutStacked layoutAuth layoutAlertAvatarBadgeButtonCheckboxComboboxDescription listDialogDividerDropdownFieldsetHeadingInputListboxNavbarPaginationRadio buttonSelectSidebarSwitchTableTextTextarea

# Textarea

For the times when you really just have a lot to say.

Description

```
import { Field, Label } from '@/components/fieldset'
import { Textarea } from '@/components/textarea'

function Example() {
  return (
    <Field>
      <Label>Description</Label>
      <Textarea name="description" />
    </Field>
  )
}
```

```
import { Field, Label } from '@/components/fieldset'
import { Textarea } from '@/components/textarea'

function Example() {
  return (
    <Field>
      <Label>Description</Label>
      <Textarea name="description" />
    </Field>
  )
}
```

## Component API

| Prop | Default | Description |
| :-- | :-- | :-- |
| Textareaextends the Headless UI`<Textarea>` component |
| `disabled` | `false` | Whether or not to disable the textarea. |
| `invalid` | `false` | Whether the textarea has a validation error. |
| `resizable` | `true` | Whether the textarea can be resized vertically. |
| `name` | - | The name to use when submitting an HTML form. |
| `defaultValue` | - | The initial value for the textarea. |
| `value` | - | The controlled value of the textarea. |
| `onChange` | - | Handler to call when the textarea value changes. |
| `rows` | - | The number of visible lines in the textarea. |
| Fieldextends the Headless UI`<Field>` component |
| `disabled` | `false` | Whether or not to disable the entire field. |
| Labelextends the Headless UI`<Label>` component |
| This component does not expose any component-specific props. |
| Descriptionextends the Headless UI`<Description>` component |
| This component does not expose any component-specific props. |
| ErrorMessageextends the Headless UI`<Description>` component |
| This component does not expose any component-specific props. |

## Examples

### Basic example

Use the `Textarea` component on its own to render a standalone textarea without an associated `Label` component:

```
import { Textarea } from '@/components/textarea'

function Example() {
  return <Textarea aria-label="Description" name="description" />
}
```

```
import { Textarea } from '@/components/textarea'

function Example() {
  return <Textarea aria-label="Description" name="description" />
}
```

Make sure to provide an `aria-label` for assistive technology, or connect the `Textarea` to your own `<label>` element
using an `id`.

### With label

Wrap a `Label` and `Textarea` with the `Field` component to automatically associate them using a generated ID:

Description

```
import { Field, Label } from '@/components/fieldset'
import { Textarea } from '@/components/textarea'

function Example() {
  return (
    <Field>
      <Label>Description</Label>
      <Textarea name="description" />
    </Field>
  )
}
```

```
import { Field, Label } from '@/components/fieldset'
import { Textarea } from '@/components/textarea'

function Example() {
  return (
    <Field>
      <Label>Description</Label>
      <Textarea name="description" />
    </Field>
  )
}
```

### With description

Use the `Description` component to add a description above or below your `Textarea`:

Description

This will be shown under the product title.

```
import { Description, Field, Label } from '@/components/fieldset'
import { Textarea } from '@/components/textarea'

function Example() {
  return (
    <Field>
      <Label>Description</Label>
      <Description>This will be shown under the product title.</Description>
      <Textarea name="name" />
    </Field>
  )
}
```

```
import { Description, Field, Label } from '@/components/fieldset'
import { Textarea } from '@/components/textarea'

function Example() {
  return (
    <Field>
      <Label>Description</Label>
      <Description>This will be shown under the product title.</Description>
      <Textarea name="name" />
    </Field>
  )
}
```

### Disabled state

Add the `disabled` prop to the `Field` component to disable an `Textarea` and the associated `Label`:

Description

```
import { Field, Label } from '@/components/fieldset'
import { Textarea } from '@/components/textarea'

function Example() {
  return (
    <Field disabled>
      <Label>Description</Label>
      <Textarea name="description" />
    </Field>
  )
}
```

```
import { Field, Label } from '@/components/fieldset'
import { Textarea } from '@/components/textarea'

function Example() {
  return (
    <Field disabled>
      <Label>Description</Label>
      <Textarea name="description" />
    </Field>
  )
}
```

You can also disable a textarea outside of a `Field` by adding the `disabled` prop directly to the `Textarea` itself.

### Validation errors

Add the `invalid` prop to the `Field` component to indicate a validation error, and render the error using the
`ErrorMessage` component:

Description

This field is required.

```
import { ErrorMessage, Field, Label } from '@/components/fieldset'
import { Textarea } from '@/components/textarea'

function Example({ errors }) {
  return (
    <Field>
      <Label>Description</Label>
      <Textarea name="description" invalid={errors.has('description')} />
      {errors.has('description') && <ErrorMessage>{errors.get('description')}</ErrorMessage>}
    </Field>
  )
}
```

```
import { ErrorMessage, Field, Label } from '@/components/fieldset'
import { Textarea } from '@/components/textarea'

function Example({ errors }) {
  return (
    <Field>
      <Label>Description</Label>
      <Textarea name="description" invalid={errors.has('description')} />
      {errors.has('description') && <ErrorMessage>{errors.get('description')}</ErrorMessage>}
    </Field>
  )
}
```

### With custom layout

Use the unstyled `Field` component from `@headlessui/react` directly instead of the styled `Field` component to
implement a custom layout:

Description

This will be shown under the product title.

```
import { Description, Label } from '@/components/fieldset'
import { Textarea } from '@/components/textarea'
import * as Headless from '@headlessui/react'

function Example() {
  return (
    <Headless.Field className="grid grid-cols-12 gap-6">
      <div className="col-span-5">
        <Label>Description</Label>
        <Description className="mt-1">This will be shown under the product title.</Description>
      </div>
      <div className="col-span-7">
        <Textarea name="description" rows="3" />
      </div>
    </Headless.Field>
  )
}
```

```
import { Description, Label } from '@/components/fieldset'
import { Textarea } from '@/components/textarea'
import * as Headless from '@headlessui/react'

function Example() {
  return (
    <Headless.Field className="grid grid-cols-12 gap-6">
      <div className="col-span-5">
        <Label>Description</Label>
        <Description className="mt-1">This will be shown under the product title.</Description>
      </div>
      <div className="col-span-7">
        <Textarea name="description" rows="3" />
      </div>
    </Headless.Field>
  )
}
```

Using the unstyled `Field` component will ensure important accessibility features are still handled for you like
generating IDs and associating elements using `aria-*` attributes.

### Controlled component

Use the normal `value` and `onChange` props to use the `Textarea` component as a controlled component:

Description

```
import { Field, Label } from '@/components/fieldset'
import { Textarea } from '@/components/textarea'
import { useState } from 'react'

function Example() {
  let [name, setName] = useState('')

  return (
    <Field>
      <Label>Description</Label>
      <Textarea name="description" value={name} onChange={(e) => setName(e.target.value)} />
    </Field>
  )
}
```

```
import { Field, Label } from '@/components/fieldset'
import { Textarea } from '@/components/textarea'
import { useState } from 'react'

function Example() {
  let [name, setName] = useState('')

  return (
    <Field>
      <Label>Description</Label>
      <Textarea name="description" value={name} onChange={(e) => setName(e.target.value)} />
    </Field>
  )
}
```