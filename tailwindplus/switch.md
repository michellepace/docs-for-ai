[Home](https://catalyst.tailwindui.com/)

[Demo](https://catalyst-demo.tailwindui.com/) [Docs](https://catalyst.tailwindui.com/docs) [Buy UI Kit →](https://tailwindcss.com/plus/templates/catalyst)

Getting startedSidebar layoutStacked layoutAuth layoutAlertAvatarBadgeButtonCheckboxComboboxDescription listDialogDividerDropdownFieldsetHeadingInputListboxNavbarPaginationRadio buttonSelectSidebarSwitchTableTextTextarea

# Switch

It's basically just a fancy checkbox, let's not kid ourselves.

Allow embedding

Allow others to embed your event details on their own site.

```tsx
import { Description, Label } from '@/components/fieldset'
import { Switch, SwitchField } from '@/components/switch'

function Example() {
  return (
    <SwitchField>
      <Label>Allow embedding</Label>
      <Description>Allow others to embed your event details on their own site.</Description>
      <Switch name="allow_embedding" defaultChecked />
    </SwitchField>
  )
}
```

## Component API

| Prop | Default | Description |
| :-- | :-- | :-- |
| **Switch** extends the Headless UI `<Switch>` component | | |
| `color` | `dark/zinc` | The [color variant](https://catalyst.tailwindui.com/docs/switch#switch-colors) the switch should use. |
| `disabled` | `false` | Whether or not to disable the switch. |
| `name` | - | The name to use when submitting an HTML form. |
| `value` | - | The value to use when submitting an HTML form. |
| `defaultChecked` | - | The initial state of the switch. |
| `checked` | - | The controlled state of the switch. |
| `onChange` | - | Handler to call when the switch state changes. |
| **SwitchField** extends the Headless UI `<Field>` component | | |
| `disabled` | `false` | Whether or not to disable the entire field. |
| **SwitchGroup** extends the JSX `<div>` element | | |
| This component does not expose any component-specific props. | | |
| **Label** extends the Headless UI `<Label>` component | | |
| This component does not expose any component-specific props. | | |
| **Description** extends the Headless UI `<Description>` component | | |
| This component does not expose any component-specific props. | | |

## Examples

### Basic example

Use the `Switch` component on its own to render a standalone switch without an associated `Label` component:

```tsx
import { Switch } from '@/components/switch'

function Example() {
  return <Switch aria-label="Allow embedding" name="allow_embedding" />
}
```

Make sure to provide an `aria-label` for assistive technology, or connect the `Switch` to your own `<label>` element
using an `id`.

### With label

Wrap a `Label` and `Switch` with the `SwitchField` component to automatically associate them using a generated ID:

Allow embedding

```tsx
import { Label } from '@/components/fieldset'
import { Switch, SwitchField } from '@/components/switch'

function Example() {
  return (
    <SwitchField>
      <Label>Allow embedding</Label>
      <Switch name="allow_embedding" />
    </SwitchField>
  )
}
```

### With description

Use the `SwitchField`, `Label`, and `Description` components to add a label and description to a switch:

Allow embedding

Allow others to embed your event details on their own site.

```tsx
import { Description, Label } from '@/components/fieldset'
import { Switch, SwitchField } from '@/components/switch'

function Example() {
  return (
    <SwitchField>
      <Label>Allow embedding</Label>
      <Description>Allow others to embed your event details on their own site.</Description>
      <Switch name="allow_embedding" />
    </SwitchField>
  )
}
```

### With custom layout

Use the unstyled `Field` component from `@headlessui/react` directly instead of the styled `SwitchField` component to
implement a custom layout:

Allow embedding

```tsx
import { Label } from '@/components/fieldset'
import { Switch } from '@/components/switch'
import * as Headless from '@headlessui/react'

function Example() {
  return (
    <Headless.Field className="flex items-center gap-4">
      <Switch name="allow_embedding" />
      <Label>Allow embedding</Label>
    </Headless.Field>
  )
}
```

Using the unstyled components from Headless UI will ensure important accessibility features are still handled for you
like generating IDs and associating elements using `aria-*` attributes.

### With accent color

Use the `color` prop to choose a different accent color for a switch:

```tsx
import { Switch } from '@/components/switch'

function Example() {
  return <Switch color="sky" defaultChecked />
}
```

For a full list of included color variants, check out the [switch color reference](https://catalyst.tailwindui.com/docs/switch#color-reference).

### With custom value

Use the `value` prop to specify a custom value to use when submitting a form:

```tsx
import { Switch } from '@/components/switch'

function Example() {
  return <Switch name="embed" value="allow" />
}
```

### Default checked state

Use the `defaultChecked` prop to set the default state when using the `Switch` as an uncontrolled component:

```tsx
import { Switch } from '@/components/switch'

function Example() {
  return <Switch defaultChecked />
}
```

### Controlled component

Use the `checked` and `onChange` props to use a `Switch` as a controlled component:

```tsx
import { Switch } from '@/components/switch'
import { useState } from 'react'

function Example() {
  let [checked, setChecked] = useState(true)

  return <Switch checked={checked} onChange={setChecked} />
}
```

### Multiple switches

Use the `SwitchGroup` component to stack multiple switches together in a list:

Show on events page

Make this event visible on your profile.

Allow embedding

Allow others to embed your event details on their own site.

```tsx
import { Description, Label } from '@/components/fieldset'
import { Switch, SwitchField, SwitchGroup } from '@/components/switch'

function Example() {
  return (
    <SwitchGroup>
      <SwitchField>
        <Label>Show on events page</Label>
        <Description>Make this event visible on your profile.</Description>
        <Switch name="show_on_events_page" defaultChecked />
      </SwitchField>
      <SwitchField>
        <Label>Allow embedding</Label>
        <Description>Allow others to embed your event details on their own site.</Description>
        <Switch name="allow_embedding" />
      </SwitchField>
    </SwitchGroup>
  )
}
```

You can optionally add `role="group"` and an `aria-label` to the `SwitchGroup` if all of the switches are related and
you want them announced to assistive technology as a group.

### With fieldset

Use the `Fieldset`, `Legend`, and `Text` components to add a title and description to a group of switches:

Discoverability

Decide where your events can be found across the web.

Show on events page

Make this event visible on your profile.

Allow embedding

Allow others to embed your event details on their own site.

```tsx
import { Description, Fieldset, Label, Legend } from '@/components/fieldset'
import { Switch, SwitchField, SwitchGroup } from '@/components/switch'
import { Text } from '@/components/text'

function Example() {
  return (
    <Fieldset>
      <Legend>Discoverability</Legend>
      <Text>Decide where your events can be found across the web.</Text>
      <SwitchGroup>
        <SwitchField>
          <Label>Show on events page</Label>
          <Description>Make this event visible on your profile.</Description>
          <Switch name="show_on_events_page" defaultChecked />
        </SwitchField>
        <SwitchField>
          <Label>Allow embedding</Label>
          <Description>Allow others to embed your event details on their own site.</Description>
          <Switch name="allow_embedding" />
        </SwitchField>
      </SwitchGroup>
    </Fieldset>
  )
}
```

### Disabled state

Add the `disabled` prop to a `Switch` or `SwitchField` component to disable it:

Discoverability

Decide where your events can be found across the web.

Show on events page

Make this event visible on your profile.

Allow embedding

Allow others to embed your event details on their own site.

```tsx
import { Description, Fieldset, Label, Legend } from '@/components/fieldset'
import { Switch, SwitchField, SwitchGroup } from '@/components/switch'
import { Text } from '@/components/text'

function Example() {
  return (
    <Fieldset>
      <Legend>Discoverability</Legend>
      <Text>Decide where your events can be found across the web.</Text>
      <SwitchGroup>
        <SwitchField>
          <Label>Show on events page</Label>
          <Description>Make this event visible on your profile.</Description>
          <Switch name="discoverability" value="show_on_events_page" />
        </SwitchField>
        <SwitchField disabled>
          <Label>Allow embedding</Label>
          <Description>Allow others to embed your event details on their own site.</Description>
          <Switch name="discoverability" value="allow_embedding" />
        </SwitchField>
      </SwitchGroup>
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

Catalyst also includes 20 solid colors that don't change outside of subtle global changes we make to all switches in
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
