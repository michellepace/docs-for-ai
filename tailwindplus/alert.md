[Home](https://catalyst.tailwindui.com/)

[Demo](https://catalyst-demo.tailwindui.com/) [Docs](https://catalyst.tailwindui.com/docs) [Buy UI Kit →](https://tailwindcss.com/plus/templates/catalyst)

Getting startedSidebar layoutStacked layoutAuth layoutAlertAvatarBadgeButtonCheckboxComboboxDescription listDialogDividerDropdownFieldsetHeadingInputListboxNavbarPaginationRadio buttonSelectSidebarSwitchTableTextTextarea

# Alert

You'll still get emails from people who accidentally deleted their account, but at least you tried.

Refund payment

```tsx
import { Alert, AlertActions, AlertDescription, AlertTitle } from '@/components/alert'
import { Button } from '@/components/button'
import { useState } from 'react'

function Example() {
  let [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <Button type="button" onClick={() => setIsOpen(true)}>
        Refund payment
      </Button>
      <Alert open={isOpen} onClose={setIsOpen}>
        <AlertTitle>Are you sure you want to refund this payment?</AlertTitle>
        <AlertDescription>
          The refund will be reflected in the customer's bank account 2 to 3 business days after processing.
        </AlertDescription>
        <AlertActions>
          <Button plain onClick={() => setIsOpen(false)}>
            Cancel
          </Button>
          <Button onClick={() => setIsOpen(false)}>Refund</Button>
        </AlertActions>
      </Alert>
    </>
  )
}
```

## Component API

### Alert

Extends the Headless UI `<Dialog>` component

| Prop | Default | Description |
| :-- | :-- | :-- |
| `open` | - | Whether the alert is open or not. |
| `onClose` | - | Called when the alert is dismissed. |
| `size` | `md` | The max-width of the alert. |

### AlertTitle

Extends the Headless UI `<DialogTitle>` component. This component does not expose any component-specific props.

### AlertDescription

Extends the Headless UI `<Description>` component. This component does not expose any component-specific props.

### AlertBody

Extends the JSX `<div>` element. This component does not expose any component-specific props.

### AlertActions

Extends the JSX `<div>` element. This component does not expose any component-specific props.

## Examples

### Basic example

Use the `Alert`, `AlertTitle`, `AlertDescription`, and `AlertActions` components to build an alert:

Refund payment

```tsx
import { Alert, AlertActions, AlertDescription, AlertTitle } from '@/components/alert'
import { Button } from '@/components/button'
import { useState } from 'react'

function Example() {
  let [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <Button type="button" onClick={() => setIsOpen(true)}>
        Refund payment
      </Button>
      <Alert open={isOpen} onClose={setIsOpen}>
        <AlertTitle>Are you sure you want to refund this payment?</AlertTitle>
        <AlertDescription>
          The refund will be reflected in the customer's bank account 2 to 3 business days after processing.
        </AlertDescription>
        <AlertActions>
          <Button plain onClick={() => setIsOpen(false)}>
            Cancel
          </Button>
          <Button onClick={() => setIsOpen(false)}>Refund</Button>
        </AlertActions>
      </Alert>
    </>
  )
}
```

### Alert width

Use the `size` prop on the `Alert` component to control the max-width of the alert dialog:

Refund payment

```tsx
import { Alert, AlertActions, AlertDescription, AlertTitle } from '@/components/alert'
import { Button } from '@/components/button'
import { useState } from 'react'

function Example() {
  let [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <Button type="button" onClick={() => setIsOpen(true)}>
        Refund payment
      </Button>
      <Alert open={isOpen} onClose={setIsOpen} size="lg">
        <AlertTitle>Are you sure you want to refund this payment?</AlertTitle>
        <AlertDescription>
          The refund will be reflected in the customer's bank account 2 to 3 business days after processing.
        </AlertDescription>
        <AlertActions>
          <Button plain onClick={() => setIsOpen(false)}>
            Cancel
          </Button>
          <Button onClick={() => setIsOpen(false)}>Refund</Button>
        </AlertActions>
      </Alert>
    </>
  )
}
```

Available `size` options include `xs`, `sm`, `md`, `lg`, `xl`, `2xl`, `3xl`, `4xl`, and `5xl`.

### With body

Add content to your alert using the `AlertBody` component:

Delete repository

```tsx
import { Alert, AlertActions, AlertBody, AlertDescription, AlertTitle } from '@/components/alert'
import { Button } from '@/components/button'
import { Input } from '@/components/input'
import { useState } from 'react'

function Example() {
  let [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <Button type="button" onClick={() => setIsOpen(true)}>
        Delete repository
      </Button>
      <Alert open={isOpen} onClose={setIsOpen} size="sm">
        <AlertTitle>Verification required</AlertTitle>
        <AlertDescription>To continue, please enter your password.</AlertDescription>
        <AlertBody>
          <Input name="password" type="password" aria-label="Password" placeholder="•••••••" />
        </AlertBody>
        <AlertActions>
          <Button plain onClick={() => setIsOpen(false)}>
            Cancel
          </Button>
          <Button onClick={() => setIsOpen(false)}>Continue</Button>
        </AlertActions>
      </Alert>
    </>
  )
}
```

### Auto-focusing elements

Add the `autoFocus` prop to any form control or button in the dialog to automatically focus it when the dialog opens:

Delete repository

```tsx
import { Alert, AlertActions, AlertBody, AlertDescription, AlertTitle } from '@/components/alert'
import { Button } from '@/components/button'
import { Input } from '@/components/input'
import { useState } from 'react'

function Example() {
  let [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <Button type="button" onClick={() => setIsOpen(true)}>
        Delete repository
      </Button>
      <Alert open={isOpen} onClose={setIsOpen} size="sm">
        <AlertTitle>Verification required</AlertTitle>
        <AlertDescription>To continue, please enter your password.</AlertDescription>
        <AlertBody>
          <Input autoFocus name="password" type="password" aria-label="Password" placeholder="•••••••" />
        </AlertBody>
        <AlertActions>
          <Button plain onClick={() => setIsOpen(false)}>
            Cancel
          </Button>
          <Button onClick={() => setIsOpen(false)}>Continue</Button>
        </AlertActions>
      </Alert>
    </>
  )
}
```
