[Home](https://catalyst.tailwindui.com/)

[Demo](https://catalyst-demo.tailwindui.com/) [Docs](https://catalyst.tailwindui.com/docs) [Buy UI Kit →](https://tailwindcss.com/plus/templates/catalyst)

Getting startedSidebar layoutStacked layoutAuth layoutAlertAvatarBadgeButtonCheckboxComboboxDescription listDialogDividerDropdownFieldsetHeadingInputListboxNavbarPaginationRadio buttonSelectSidebarSwitchTableTextTextarea

# Radio

With multiple choice, you've always got a chance at getting the right answer.

Resale and transfers

Decide if people buy tickets from you or from scalpers.

Allow tickets to be resold

Customers can resell or transfer their tickets if they can't make it to the event.

Don't allow tickets to be resold

Tickets cannot be resold or transferred to another person.

```tsx
import { Description, Fieldset, Label, Legend } from '@/components/fieldset'
import { Radio, RadioField, RadioGroup } from '@/components/radio'
import { Text } from '@/components/text'

function Example() {
  return (
    <Fieldset>
      <Legend>Resale and transfers</Legend>
      <Text>Decide if people buy tickets from you or from scalpers.</Text>
      <RadioGroup name="resale" defaultValue="permit">
        <RadioField>
          <Radio value="permit" />
          <Label>Allow tickets to be resold</Label>
          <Description>Customers can resell or transfer their tickets if they can't make it to the event.</Description>
        </RadioField>
        <RadioField>
          <Radio value="forbid" />
          <Label>Don't allow tickets to be resold</Label>
          <Description>Tickets cannot be resold or transferred to another person.</Description>
        </RadioField>
      </RadioGroup>
    </Fieldset>
  )
}
```

## Component API

### RadioGroup

Extends the Headless UI `<RadioGroup>` component

| Prop           | Default | Description                                      |
|:---------------|:--------|:-------------------------------------------------|
| `disabled`     | `false` | Whether or not to disable the entire list.       |
| `name`         | -       | The name to use when submitting an HTML form.    |
| `defaultValue` | -       | The initially selected value.                    |
| `value`        | -       | The controlled value of the radio group.         |
| `onChange`     | -       | Handler to call when the state changes.          |

### Radio

Extends the Headless UI `<Radio>` component

| Prop | Default | Description |
| :--- | :------ | :---------- |
| `color` | `dark/zinc` | The [color variant](https://catalyst.tailwindui.com/docs/radio#radio-colors) the radio should use. |
| `disabled` | `false` | Whether or not to disable the radio. |
| `value` | - | The value to use when submitting an HTML form. |

### RadioField

Extends the Headless UI `<Field>` component

| Prop       | Default | Description                                |
|:-----------|:--------|:-------------------------------------------|
| `disabled` | `false` | Whether or not to disable the entire field.|

### Label

Extends the Headless UI `<Label>` component

This component does not expose any component-specific props.

### Description

Extends the Headless UI `<Description>` component

This component does not expose any component-specific props.

## Examples

### Basic example

Use the `RadioGroup`, `RadioField`, `Radio`, and `Label` components to create a simple radio group:

Allow tickets to be resold

Don't allow tickets to be resold

```tsx
import { Label } from '@/components/fieldset'
import { Radio, RadioField, RadioGroup } from '@/components/radio'

function Example() {
  return (
    <RadioGroup name="resale" defaultValue="permit" aria-label="Resale and transfers">
      <RadioField>
        <Radio value="permit" />
        <Label>Allow tickets to be resold</Label>
      </RadioField>
      <RadioField>
        <Radio value="forbid" />
        <Label>Don't allow tickets to be resold</Label>
      </RadioField>
    </RadioGroup>
  )
}
```

We recommend adding an `aria-label` for assistive technology, or connecting the `RadioGroup` to your own label using
`aria-labelledby`.

### With description

Use the `RadioField`, `Label`, and `Description` components to add a description below the radio:

Allow tickets to be resold

Customers can resell or transfer their tickets if they can't make it to the event.

Don't allow tickets to be resold

Tickets cannot be resold or transferred to another person.

```tsx
import { Description, Label } from '@/components/fieldset'
import { Radio, RadioField, RadioGroup } from '@/components/radio'

function Example() {
  return (
    <RadioGroup name="resale" defaultValue="permit" aria-label="Resale and transfers">
      <RadioField>
        <Radio value="permit" />
        <Label>Allow tickets to be resold</Label>
        <Description>Customers can resell or transfer their tickets if they can't make it to the event.</Description>
      </RadioField>
      <RadioField>
        <Radio value="forbid" />
        <Label>Don't allow tickets to be resold</Label>
        <Description>Tickets cannot be resold or transferred to another person.</Description>
      </RadioField>
    </RadioGroup>
  )
}
```

### With custom layout

Use the `Radio` component with the unstyled components from `@headlessui/react` to implement custom layouts that still
use the styled radio button:

How would you rate your experience?

1

2

3

4

5

```tsx
import { Radio } from '@/components/radio'
import * as Headless from '@headlessui/react'

function Example() {
  return (
    <Headless.Fieldset>
      <Headless.Legend className="text-base/6 font-medium sm:text-sm/6">
        How would you rate your experience?
      </Headless.Legend>
      <Headless.RadioGroup name="rating" defaultValue={3} className="mt-4 flex gap-6 sm:gap-8">
        {[1, 2, 3, 4, 5].map((rating) => (
          <Headless.Field key={rating} className="flex items-center gap-2">
            <Radio value={rating} />
            <Headless.Label className="text-base/6 select-none sm:text-sm/6">{rating}</Headless.Label>
          </Headless.Field>
        ))}
      </Headless.RadioGroup>
    </Headless.Fieldset>
  )
}
```

Using the unstyled components from Headless UI will ensure important accessibility features are still handled for you
like generating IDs and associating elements using `aria-*` attributes.

### With accent color

Use the `color` prop to choose a different accent color for a checkbox:

Allow tickets to be resold

Don't allow tickets to be resold

```tsx
import { Label } from '@/components/fieldset'
import { Radio, RadioField, RadioGroup } from '@/components/radio'

function Example() {
  return (
    <RadioGroup name="resale" defaultValue="permit" aria-label="Resale and transfers">
      <RadioField>
        <Radio color="sky" value="permit" />
        <Label>Allow tickets to be resold</Label>
      </RadioField>
      <RadioField>
        <Radio color="sky" value="forbid" />
        <Label>Don't allow tickets to be resold</Label>
      </RadioField>
    </RadioGroup>
  )
}
```

For a full list of included color variants, check out the [radio color reference](https://catalyst.tailwindui.com/docs/radio#color-reference).

### Default selected state

Use the `defaultValue` prop to set the default selected option for a `RadioGroup`:

Allow tickets to be resold

Don't allow tickets to be resold

```tsx
import { Label } from '@/components/fieldset'
import { Radio, RadioField, RadioGroup } from '@/components/radio'

function Example() {
  return (
    <RadioGroup name="resale" defaultValue="permit" aria-label="Resale and transfers">
      <RadioField>
        <Radio value="permit" />
        <Label>Allow tickets to be resold</Label>
      </RadioField>
      <RadioField>
        <Radio value="forbid" />
        <Label>Don't allow tickets to be resold</Label>
      </RadioField>
    </RadioGroup>
  )
}
```

### Controlled component

Use the `value` and `onChange` props to use a `RadioGroup` as a controlled component:

Allow tickets to be resold

Don't allow tickets to be resold

```tsx
import { Label } from '@/components/fieldset'
import { Radio, RadioField, RadioGroup } from '@/components/radio'
import { useState } from 'react'

function Example() {
  let [selected, setSelected] = useState('permit')

  return (
    <RadioGroup value={selected} onChange={setSelected}>
      <RadioField>
        <Radio value="permit" />
        <Label>Allow tickets to be resold</Label>
      </RadioField>
      <RadioField>
        <Radio value="forbid" />
        <Label>Don't allow tickets to be resold</Label>
      </RadioField>
    </RadioGroup>
  )
}
```

### With fieldset

Use the `Fieldset`, `Legend`, and `Text` components to add a title and description to a radio group:

Resale and transfers

Decide if people buy tickets from you or from scalpers.

Allow tickets to be resold

Customers can resell or transfer their tickets if they can't make it to the event.

Don't allow tickets to be resold

Tickets cannot be resold or transferred to another person.

```tsx
import { Description, Fieldset, Label, Legend } from '@/components/fieldset'
import { Radio, RadioField, RadioGroup } from '@/components/radio'
import { Text } from '@/components/text'

function Example() {
  return (
    <Fieldset>
      <Legend>Resale and transfers</Legend>
      <Text>Decide if people buy tickets from you or from scalpers.</Text>
      <RadioGroup name="resale" defaultValue="permit">
        <RadioField>
          <Radio value="permit" />
          <Label>Allow tickets to be resold</Label>
          <Description>Customers can resell or transfer their tickets if they can't make it to the event.</Description>
        </RadioField>
        <RadioField>
          <Radio value="forbid" />
          <Label>Don't allow tickets to be resold</Label>
          <Description>Tickets cannot be resold or transferred to another person.</Description>
        </RadioField>
      </RadioGroup>
    </Fieldset>
  )
}
```

When used with a `Fieldset` and `Legend`, you don't need to add a separate `aria-label` to the `RadioGroup` itself.

### Disabled state

Add the `disabled` prop to a `Radio` or `RadioField` component to disable it:

Resale and transfers

Decide if people buy tickets from you or from scalpers.

Allow tickets to be resold

Customers can resell or transfer their tickets if they can't make it to the event.

Don't allow tickets to be resold

Tickets cannot be resold or transferred to another person.

```tsx
import { Description, Fieldset, Label, Legend } from '@/components/fieldset'
import { Radio, RadioField, RadioGroup } from '@/components/radio'
import { Text } from '@/components/text'

function Example() {
  return (
    <Fieldset>
      <Legend>Resale and transfers</Legend>
      <Text>Decide if people buy tickets from you or from scalpers.</Text>
      <RadioGroup name="resale" defaultValue="permit">
        <RadioField>
          <Radio value="permit" />
          <Label>Allow tickets to be resold</Label>
          <Description>Customers can resell or transfer their tickets if they can't make it to the event.</Description>
        </RadioField>
        <RadioField disabled>
          <Radio value="forbid" />
          <Label>Don't allow tickets to be resold</Label>
          <Description>Tickets cannot be resold or transferred to another person.</Description>
        </RadioField>
      </RadioGroup>
    </Fieldset>
  )
}
```

You can also add the `disabled` prop to a `RadioGroup` or `Fieldset` to disable all of the radio buttons in that group.

## Appendix

### Color reference

By default, Catalyst includes two adaptive color variants that automatically change color between and dark modes to
maintain a consistent level of contrast:

| Color        | Example |
|:-------------|:-------:|
| `dark/zinc`  |         |
| `dark/white` |         |

Catalyst also includes 20 solid colors that don't change outside of subtle global changes we make to all radios in dark
mode:

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
