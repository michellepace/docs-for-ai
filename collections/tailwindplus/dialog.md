[Home](https://catalyst.tailwindui.com/)

[Demo](https://catalyst-demo.tailwindui.com/) [Docs](https://catalyst.tailwindui.com/docs) [Buy UI Kit →](https://tailwindcss.com/plus/templates/catalyst)

Getting startedSidebar layoutStacked layoutAuth layoutAlertAvatarBadgeButtonCheckboxComboboxDescription listDialogDividerDropdownFieldsetHeadingInputListboxNavbarPaginationRadio buttonSelectSidebarSwitchTableTextTextarea

# Dialog

Back in my day we used to just put this sort of content on a separate page.

Refund payment

```tsx
import { Button } from '@/components/button'
import { Dialog, DialogActions, DialogBody, DialogDescription, DialogTitle } from '@/components/dialog'
import { Field, Label } from '@/components/fieldset'
import { Input } from '@/components/input'
import { useState } from 'react'

function Example() {
  let [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <Button type="button" onClick={() => setIsOpen(true)}>
        Refund payment
      </Button>
      <Dialog open={isOpen} onClose={setIsOpen}>
        <DialogTitle>Refund payment</DialogTitle>
        <DialogDescription>
          The refund will be reflected in the customer's bank account 2 to 3 business days after processing.
        </DialogDescription>
        <DialogBody>
          <Field>
            <Label>Amount</Label>
            <Input name="amount" placeholder="$0.00" />
          </Field>
        </DialogBody>
        <DialogActions>
          <Button plain onClick={() => setIsOpen(false)}>
            Cancel
          </Button>
          <Button onClick={() => setIsOpen(false)}>Refund</Button>
        </DialogActions>
      </Dialog>
    </>
  )
}
```

## Component API

### Dialog

Extends the Headless UI `<Dialog>` component.

| Prop | Default | Description |
| :-- | :-- | :-- |
| `open` | - | Whether the dialog is open or not. |
| `onClose` | - | Called when the dialog is dismissed. |
| `size` | `lg` | The max-width of the dialog. |

### DialogTitle

Extends the Headless UI `<DialogTitle>` component.

This component does not expose any component-specific props.

### DialogDescription

Extends the Headless UI `<Description>` component.

This component does not expose any component-specific props.

### DialogBody

Extends the JSX `<div>` element.

This component does not expose any component-specific props.

### DialogActions

Extends the JSX `<div>` element.

This component does not expose any component-specific props.

## Examples

### Basic example

Use the `Dialog`, `DialogTitle`, `DialogDescription`, `DialogBody`, and `DialogActions` components to build a dialog:

Refund payment

```tsx
import { Button } from '@/components/button'
import { Dialog, DialogActions, DialogBody, DialogDescription, DialogTitle } from '@/components/dialog'
import { Field, Label } from '@/components/fieldset'
import { Input } from '@/components/input'
import { useState } from 'react'

function Example() {
  let [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <Button type="button" onClick={() => setIsOpen(true)}>
        Refund payment
      </Button>
      <Dialog open={isOpen} onClose={setIsOpen}>
        <DialogTitle>Refund payment</DialogTitle>
        <DialogDescription>
          The refund will be reflected in the customer's bank account 2 to 3 business days after processing.
        </DialogDescription>
        <DialogBody>
          <Field>
            <Label>Amount</Label>
            <Input name="amount" placeholder="$0.00" />
          </Field>
        </DialogBody>
        <DialogActions>
          <Button plain onClick={() => setIsOpen(false)}>
            Cancel
          </Button>
          <Button onClick={() => setIsOpen(false)}>Refund</Button>
        </DialogActions>
      </Dialog>
    </>
  )
}
```

Dialogs are controlled components and can be opened and closed using the `open` and `onClose` props.

### Dialog width

Use the `size` prop on the `Dialog` component to control the max-width of the dialog:

Refund payment

```tsx
import { Button } from '@/components/button'
import { Dialog, DialogActions, DialogBody, DialogDescription, DialogTitle } from '@/components/dialog'
import { Field, Label } from '@/components/fieldset'
import { Input } from '@/components/input'
import { useState } from 'react'

function Example() {
  let [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <Button type="button" onClick={() => setIsOpen(true)}>
        Refund payment
      </Button>
      <Dialog size="xl" open={isOpen} onClose={setIsOpen}>
        <DialogTitle>Refund payment</DialogTitle>
        <DialogDescription>
          The refund will be reflected in the customer's bank account 2 to 3 business days after processing.
        </DialogDescription>
        <DialogBody>
          <Field>
            <Label>Amount</Label>
            <Input name="amount" placeholder="$0.00" />
          </Field>
        </DialogBody>
        <DialogActions>
          <Button plain onClick={() => setIsOpen(false)}>
            Cancel
          </Button>
          <Button onClick={() => setIsOpen(false)}>Refund</Button>
        </DialogActions>
      </Dialog>
    </>
  )
}
```

Available `size` options include `xs`, `sm`, `md`, `lg`, `xl`, `2xl`, `3xl`, `4xl`, and `5xl`.

### Opening from dropdown

When opening a `Dialog` from a dropdown menu, make sure the dialog is rendered outside of the dropdown:

Options

```tsx
import { Button } from '@/components/button'
import { Dialog, DialogActions, DialogBody, DialogDescription, DialogTitle } from '@/components/dialog'
import { Dropdown, DropdownButton, DropdownItem, DropdownMenu } from '@/components/dropdown'
import { Field, Label } from '@/components/fieldset'
import { Input } from '@/components/input'
import { ChevronDownIcon } from '@heroicons/react/16/solid'
import { useState } from 'react'

function Example() {
  let [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <Dropdown>
        <DropdownButton outline>
          Options
          <ChevronDownIcon />
        </DropdownButton>
        <DropdownMenu>
          <DropdownItem onClick={() => setIsOpen(true)}>Refund</DropdownItem>
          <DropdownItem href="#" disabled>
            Download
          </DropdownItem>
        </DropdownMenu>
      </Dropdown>

      <Dialog open={isOpen} onClose={setIsOpen}>
        <DialogTitle>Refund payment</DialogTitle>
        <DialogDescription>
          The refund will be reflected in the customer's bank account 2 to 3 business days after processing.
        </DialogDescription>
        <DialogBody>
          <Field>
            <Label>Amount</Label>
            <Input name="amount" placeholder="$0.00" />
          </Field>
        </DialogBody>
        <DialogActions>
          <Button plain onClick={() => setIsOpen(false)}>
            Cancel
          </Button>
          <Button onClick={() => setIsOpen(false)}>Refund</Button>
        </DialogActions>
      </Dialog>
    </>
  )
}
```

If your `Dialog` is placed inside the dropdown, it won't open as expected because it will be immediately unmounted when
the dropdown menu closes.

### Auto-focusing elements

Add the `autoFocus` prop to any form control or button in the dialog to automatically focus it when the dialog opens:

Refund payment

```tsx
import { Button } from '@/components/button'
import { Dialog, DialogActions, DialogBody, DialogDescription, DialogTitle } from '@/components/dialog'
import { Field, Label } from '@/components/fieldset'
import { Input } from '@/components/input'
import { useState } from 'react'

function Example() {
  let [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <Button type="button" onClick={() => setIsOpen(true)}>
        Refund payment
      </Button>
      <Dialog open={isOpen} onClose={setIsOpen}>
        <DialogTitle>Refund payment</DialogTitle>
        <DialogDescription>
          The refund will be reflected in the customer's bank account 2 to 3 business days after processing.
        </DialogDescription>
        <DialogBody>
          <Field>
            <Label>Amount</Label>
            <Input name="amount" placeholder="$0.00" autoFocus />
          </Field>
        </DialogBody>
        <DialogActions>
          <Button plain onClick={() => setIsOpen(false)}>
            Cancel
          </Button>
          <Button onClick={() => setIsOpen(false)}>Refund</Button>
        </DialogActions>
      </Dialog>
    </>
  )
}
```

Elements will not be automatically focused on touch devices to prevent layout shifts caused by the software keyboard
opening.

### With scrolling content

Dialogs automatically become scrollable if their content is taller than the viewport:

Agree to terms

```tsx
import { Button } from '@/components/button'
import { Dialog, DialogActions, DialogBody, DialogDescription, DialogTitle } from '@/components/dialog'
import { useState } from 'react'

function Example() {
  let [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <Button type="button" onClick={() => setIsOpen(true)}>
        Agree to terms
      </Button>
      <Dialog open={isOpen} onClose={setIsOpen} size="xl">
        <DialogTitle>Terms and conditions</DialogTitle>
        <DialogDescription>Please agree to the following terms and conditions to continue.</DialogDescription>
        <DialogBody className="text-sm/6 text-zinc-900 dark:text-white">
          <p className="mt-4">
            By accessing and using our services, you are agreeing to these terms, which have been meticulously tailored
            for our benefit and your compliance.
          </p>
          <h3 className="mt-6 font-bold">Comprehensive Acceptance of Terms</h3>
          <p className="mt-4">
            Your engagement with our application signifies your irrevocable acceptance of these terms, which are binding
            regardless of your awareness or understanding of them. Your continued use acts as a silent nod of agreement
            to any and all stipulations outlined herein.
          </p>
          {/* ... */}
        </DialogBody>
        <DialogActions>
          <Button plain onClick={() => setIsOpen(false)}>
            Cancel
          </Button>
          <Button onClick={() => setIsOpen(false)}>I agree</Button>
        </DialogActions>
      </Dialog>
    </>
  )
}
```
