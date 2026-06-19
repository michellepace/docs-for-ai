[Home](https://catalyst.tailwindui.com/)

[Demo](https://catalyst-demo.tailwindui.com/) [Docs](https://catalyst.tailwindui.com/docs) [Buy UI Kit →](https://tailwindcss.com/plus/templates/catalyst)

Getting startedSidebar layoutStacked layoutAuth layoutAlertAvatarBadgeButtonCheckboxComboboxDescription listDialogDividerDropdownFieldsetHeadingInputListboxNavbarPaginationRadio buttonSelectSidebarSwitchTableTextTextarea

# Checkbox

People need to be able to accept the terms and conditions they don't read somehow.

Discoverability

Decide where your events can be found across the web.

Show on events page

Make this event visible on your profile.

Allow embedding

Allow others to embed your event details on their own site.

```tsx
import { Checkbox, CheckboxField, CheckboxGroup } from '@/components/checkbox'
import { Description, Fieldset, Label, Legend } from '@/components/fieldset'
import { Text } from '@/components/text'

function Example() {
  return (
    <Fieldset>
      <Legend>Discoverability</Legend>
      <Text>Decide where your events can be found across the web.</Text>
      <CheckboxGroup>
        <CheckboxField>
          <Checkbox name="discoverability" value="show_on_events_page" defaultChecked />
          <Label>Show on events page</Label>
          <Description>Make this event visible on your profile.</Description>
        </CheckboxField>
        <CheckboxField>
          <Checkbox name="discoverability" value="allow_embedding" />
          <Label>Allow embedding</Label>
          <Description>Allow others to embed your event details on their own site.</Description>
        </CheckboxField>
      </CheckboxGroup>
    </Fieldset>
  )
}
```

## Component API

**Checkbox** extends the Headless UI `<Checkbox>` component

| Prop | Default | Description |
| :-- | :-- | :-- |
| `color` | `dark/zinc` | The [color variant](https://catalyst.tailwindui.com/docs/checkbox#checkbox-colors) the checkbox should use. |
| `disabled` | `false` | Whether or not to disable the checkbox. |
| `name` | - | The name to use when submitting an HTML form. |
| `value` | - | The value to use when submitting an HTML form. |
| `defaultChecked` | - | The initial state of the checkbox. |
| `checked` | - | The controlled state of the checkbox. |
| `onChange` | - | Handler to call when the checkbox state changes. |

**CheckboxField** extends the Headless UI `<Field>` component

| Prop | Default | Description |
| :-- | :-- | :-- |
| `disabled` | `false` | Whether or not to disable the entire field. |

**CheckboxGroup** extends the JSX `<div>` element

This component does not expose any component-specific props.

**Label** extends the Headless UI `<Label>` component

This component does not expose any component-specific props.

**Description** extends the Headless UI `<Description>` component

This component does not expose any component-specific props.

## Examples

### Basic example

Use the `Checkbox` component on its own to render a standalone checkbox without an associated `Label` component:

```tsx
import { Checkbox } from '@/components/checkbox'

function Example() {
  return <Checkbox aria-label="Allow embedding" name="allow_embedding" />
}
```

Make sure to provide an `aria-label` for assistive technology, or connect the `Checkbox` to your own `<label>` element
using an `id`.

### With label

Wrap a `Label` and `Checkbox` with the `CheckboxField` component to automatically associate them using a generated ID:

Allow embedding

```tsx
import { Checkbox, CheckboxField } from '@/components/checkbox'
import { Label } from '@/components/fieldset'

function Example() {
  return (
    <CheckboxField>
      <Checkbox name="allow_embedding" />
      <Label>Allow embedding</Label>
    </CheckboxField>
  )
}
```

### With description

Use the `CheckboxField`, `Label`, and `Description` components to add a description below the checkbox:

Allow embedding

Allow others to embed your event details on their own site.

```tsx
import { Checkbox, CheckboxField } from '@/components/checkbox'
import { Description, Label } from '@/components/fieldset'

function Example() {
  return (
    <CheckboxField>
      <Checkbox name="allow_embedding" />
      <Label>Allow embedding</Label>
      <Description>Allow others to embed your event details on their own site.</Description>
    </CheckboxField>
  )
}
```

### With custom layout

Use the unstyled `Field` component from `@headlessui/react` directly instead of the styled `CheckboxField` component to
implement a custom layout:

Allow embedding

```tsx
import { Checkbox } from '@/components/checkbox'
import { Label } from '@/components/fieldset'
import * as Headless from '@headlessui/react'

function Example() {
  return (
    <Headless.Field className="flex items-center justify-between gap-4">
      <Label>Allow embedding</Label>
      <Checkbox name="allow_embedding" />
    </Headless.Field>
  )
}
```

Using the unstyled `Field` component will ensure important accessibility features are still handled for you like
generating IDs and associating elements using `aria-*` attributes.

### With accent color

Use the `color` prop to choose a different accent color for a checkbox:

```tsx
import { Checkbox } from '@/components/checkbox'

function Example() {
  return <Checkbox color="sky" defaultChecked />
}
```

For a full list of included color variants, check out the [checkbox color reference](https://catalyst.tailwindui.com/docs/checkbox#color-reference).

### With custom value

Use the `value` prop to specify a custom value to use when submitting a form:

```tsx
import { Checkbox } from '@/components/checkbox'

function Example() {
  return <Checkbox name="embed" value="allow" />
}
```

### Default checked state

Use the `defaultChecked` prop to set the default state when using the `Checkbox` as an uncontrolled component:

```tsx
import { Checkbox } from '@/components/checkbox'

function Example() {
  return <Checkbox defaultChecked />
}
```

### Indeterminate state

Use the `indeterminate` prop to indicate that the `Checkbox` is in an indeterminate state, neither toggled on nor off:

Select all

Show on events page

Allow embedding

```tsx
import { Checkbox, CheckboxField, CheckboxGroup } from '@/components/checkbox'
import { Label } from '@/components/fieldset'
import { useState } from 'react'

const options = ['Show on events page', 'Allow embedding']

function Example() {
  let [selected, setSelected] = useState(['Show on events page'])

  return (
    <CheckboxGroup role="group" aria-label="Discoverability">
      <CheckboxField>
        <Checkbox
          checked={selected.length > 0}
          indeterminate={selected.length !== options.length}
          onChange={(checked) => setSelected(checked ? options : [])}
        />
        <Label>Select all</Label>
      </CheckboxField>

      {options.map((option) => (
        <CheckboxField key={option}>
          <Checkbox
            name={option}
            checked={selected.includes(option)}
            onChange={(checked) => {
              return setSelected((pending) => {
                return checked ? [...pending, option] : pending.filter((item) => item !== option)
              })
            }}
          />
          <Label>{option}</Label>
        </CheckboxField>
      ))}
    </CheckboxGroup>
  )
}
```

### Controlled component

Use the `checked` and `onChange` props to use a `Checkbox` as a controlled component:

```tsx
import { Checkbox } from '@/components/checkbox'
import { useState } from 'react'

function Example() {
  let [checked, setChecked] = useState(true)

  return <Checkbox checked={checked} onChange={setChecked} />
}
```

### Multiple checkboxes

Use the `CheckboxGroup` component to stack multiple checkboxes together in a list:

Show on events page

Make this event visible on your profile.

Allow embedding

Allow others to embed your event details on their own site.

```tsx
import { Checkbox, CheckboxField, CheckboxGroup } from '@/components/checkbox'
import { Description, Label } from '@/components/fieldset'

function Example() {
  return (
    <CheckboxGroup>
      <CheckboxField>
        <Checkbox name="show_on_events_page" defaultChecked />
        <Label>Show on events page</Label>
        <Description>Make this event visible on your profile.</Description>
      </CheckboxField>
      <CheckboxField>
        <Checkbox name="allow_embedding" />
        <Label>Allow embedding</Label>
        <Description>Allow others to embed your event details on their own site.</Description>
      </CheckboxField>
    </CheckboxGroup>
  )
}
```

You can optionally add `role="group"` and an `aria-label` to the `CheckboxGroup` if all of the checkboxes are related
and you want them announced to assistive technology as a group.

### With fieldset

Use the `Fieldset`, `Legend`, and `Text` components to add a title and description to a group of checkboxes:

Discoverability

Decide where your events can be found across the web.

Show on events page

Make this event visible on your profile.

Allow embedding

Allow others to embed your event details on their own site.

```tsx
import { Checkbox, CheckboxField, CheckboxGroup } from '@/components/checkbox'
import { Description, Fieldset, Label, Legend } from '@/components/fieldset'
import { Text } from '@/components/text'

function Example() {
  return (
    <Fieldset>
      <Legend>Discoverability</Legend>
      <Text>Decide where your events can be found across the web.</Text>
      <CheckboxGroup>
        <CheckboxField>
          <Checkbox name="discoverability" value="show_on_events_page" defaultChecked />
          <Label>Show on events page</Label>
          <Description>Make this event visible on your profile.</Description>
        </CheckboxField>
        <CheckboxField>
          <Checkbox name="discoverability" value="allow_embedding" />
          <Label>Allow embedding</Label>
          <Description>Allow others to embed your event details on their own site.</Description>
        </CheckboxField>
      </CheckboxGroup>
    </Fieldset>
  )
}
```

### Disabled state

Add the `disabled` prop to a `Checkbox` or `CheckboxField` component to disable it:

Discoverability

Decide where your events can be found across the web.

Show on events page

Make this event visible on your profile.

Allow embedding

Allow others to embed your event details on their own site.

```tsx
import { Checkbox, CheckboxField, CheckboxGroup } from '@/components/checkbox'
import { Description, Fieldset, Label, Legend } from '@/components/fieldset'
import { Text } from '@/components/text'

function Example() {
  return (
    <Fieldset>
      <Legend>Discoverability</Legend>
      <Text>Decide where your events can be found across the web.</Text>
      <CheckboxGroup>
        <CheckboxField>
          <Checkbox name="discoverability" value="show_on_events_page" />
          <Label>Show on events page</Label>
          <Description>Make this event visible on your profile.</Description>
        </CheckboxField>
        <CheckboxField disabled>
          <Checkbox name="discoverability" value="allow_embedding" />
          <Label>Allow embedding</Label>
          <Description>Allow others to embed your event details on their own site.</Description>
        </CheckboxField>
      </CheckboxGroup>
    </Fieldset>
  )
}
```

You can also add the `disabled` prop to a `Fieldset` to disable the entire fieldset.

## Appendix

### Color reference

By default, Catalyst includes two adaptive color variants that automatically change color between light and dark modes
to maintain a consistent level of contrast:

| Color        | Example |
|:-------------|:-------:|
| `dark/zinc`  |         |
| `dark/white` |         |

Catalyst also includes 20 solid colors that don't change outside of subtle global changes we make to all checkboxes in
dark mode:

| Color      | Example |
|:-----------|:-------:|
| `dark`     |         |
| `zinc`     |         |
| `white`    |         |
| `red`      |         |
| `orange`   |         |
| `amber`    |         |
| `yellow`   |         |
| `lime`     |         |
| `green`    |         |
| `emerald`  |         |
| `teal`     |         |
| `cyan`     |         |
| `sky`      |         |
| `blue`     |         |
| `indigo`   |         |
| `violet`   |         |
| `purple`   |         |
| `fuchsia`  |         |
| `pink`     |         |
| `rose`     |         |
