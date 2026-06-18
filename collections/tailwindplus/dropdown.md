[Home](https://catalyst.tailwindui.com/)

[Demo](https://catalyst-demo.tailwindui.com/) [Docs](https://catalyst.tailwindui.com/docs) [Buy UI Kit →](https://tailwindcss.com/plus/templates/catalyst)

Getting startedSidebar layoutStacked layoutAuth layoutAlertAvatarBadgeButtonCheckboxComboboxDescription listDialogDividerDropdownFieldsetHeadingInputListboxNavbarPaginationRadio buttonSelectSidebarSwitchTableTextTextarea

# Dropdown

Probably the number one reason you're looking for a UI kit in the first place.

Options

```tsx
import { Dropdown, DropdownButton, DropdownItem, DropdownMenu } from '@/components/dropdown'
import { ChevronDownIcon } from '@heroicons/react/16/solid'

function Example() {
  function deleteUser() {
    if (confirm('Are you sure you want to delete this user?')) {
      // ...
    }
  }

  return (
    <Dropdown>
      <DropdownButton outline>
        Options
        <ChevronDownIcon />
      </DropdownButton>
      <DropdownMenu>
        <DropdownItem href="/users/1">View</DropdownItem>
        <DropdownItem href="/users/1/edit">Edit</DropdownItem>
        <DropdownItem onClick={() => deleteUser()}>Delete</DropdownItem>
      </DropdownMenu>
    </Dropdown>
  )
}
```

## Component API

| Component / Prop | Default | Description |
| :-- | :-- | :-- |
| **Dropdown** extends the Headless UI `<Menu>` component | | |
| `children` | - | The dropdown button and menu. |
| **DropdownButton** extends the [`<Button>`](https://catalyst.tailwindui.com/docs/button) component | | |
| `color` | `dark/zinc` | The [color variant](https://catalyst.tailwindui.com/docs/button#button-colors) the button should use. |
| `outline` | `false` | Whether to use the [outline button style](https://catalyst.tailwindui.com/docs/button#outline-buttons). |
| `plain` | `false` | Whether to use the [plain button style](https://catalyst.tailwindui.com/docs/button#plain-buttons). |
| `disabled` | `false` | Whether or not to disable the button. |
| **DropdownMenu** extends the Headless UI `<MenuItems>` component | | |
| `anchor` | `bottom` | Where to position the dropdown menu. |
| `children` | - | The dropdown items and sections. |
| **DropdownItem** extends the Headless UI `<MenuItem>` component | | |
| `href` | - | The target URL when using the item as a link. |
| `onClick` | - | Handler to call when the item is selected. |
| `children` | - | The dropdown item text. |
| **DropdownHeader** extends the JSX `<div>` element | | |
| `children` | - | The dropdown header content. |
| **DropdownSection** extends the Headless UI `<MenuSection>` component | | |
| `children` | - | The dropdown items for the section. |
| **DropdownHeading** extends the Headless UI `<MenuHeading>` component | | |
| `children` | - | The section heading content. |
| **DropdownDivider** extends the Headless UI `<MenuSeparator>` component | | |
| (This component does not expose any component-specific props.) | | |
| **DropdownLabel** extends the Headless UI `<Label>` component | | |
| `children` | - | The label text. |
| **DropdownDescription** extends the Headless UI `<Description>` component | | |
| `children` | - | The description text. |
| **DropdownShortcut** extends the Headless UI `<Description>` component | | |
| `keys` | - | The keyboard shortcut. |

## Examples

### Basic example

Use the `Dropdown`, `DropdownButton`, `DropdownMenu`, and `DropdownItem` components to build a basic dropdown menu:

Options

```tsx
import { Dropdown, DropdownButton, DropdownItem, DropdownMenu } from '@/components/dropdown'
import { ChevronDownIcon } from '@heroicons/react/16/solid'

function Example() {
  function deleteUser() {
    if (confirm('Are you sure you want to delete this user?')) {
      // ...
    }
  }

  return (
    <Dropdown>
      <DropdownButton outline>
        Options
        <ChevronDownIcon />
      </DropdownButton>
      <DropdownMenu>
        <DropdownItem href="/users/1">View</DropdownItem>
        <DropdownItem href="/users/1/edit">Edit</DropdownItem>
        <DropdownItem onClick={() => deleteUser()}>Delete</DropdownItem>
      </DropdownMenu>
    </Dropdown>
  )
}
```

Use the `href` prop for dropdown items that are links, and the `onClick` prop for dropdown items that should invoke a
callback when selected.

### Button style

The `DropdownButton` component is rendered as a [`Button`](https://catalyst.tailwindui.com/docs/button) by default and directly accepts all of the same
styling props, such as `color`, `outline`, and `plain`:

Options

```tsx
import { Dropdown, DropdownButton, DropdownItem, DropdownMenu } from '@/components/dropdown'
import { ChevronDownIcon } from '@heroicons/react/16/solid'

function Example() {
  return (
    <Dropdown>
      <DropdownButton color="cyan">
        Options
        <ChevronDownIcon />
      </DropdownButton>
      <DropdownMenu>
        <DropdownItem href="#">View</DropdownItem>
        <DropdownItem href="#">Edit</DropdownItem>
        <DropdownItem href="#">Export as CSV&hellip;</DropdownItem>
      </DropdownMenu>
    </Dropdown>
  )
}
```

You can also use the `as` prop to render a completely different button component with your own custom styles.

### Menu placement

Use the `anchor` prop on the `DropdownMenu` component to position the dropdown menu relative to the trigger:

Options

```tsx
import { Dropdown, DropdownButton, DropdownItem, DropdownMenu } from '@/components/dropdown'
import { ChevronUpIcon } from '@heroicons/react/16/solid'

function Example() {
  return (
    <Dropdown>
      <DropdownButton outline>
        Options
        <ChevronUpIcon />
      </DropdownButton>
      <DropdownMenu anchor="top start">
        <DropdownItem href="#">View</DropdownItem>
        <DropdownItem href="#">Edit</DropdownItem>
        <DropdownItem href="#">Export as CSV&hellip;</DropdownItem>
      </DropdownMenu>
    </Dropdown>
  )
}
```

Use the values `top`, `right`, `bottom`, `left` to center the menu along the appropriate edge, or combine it with
`start` or `end` to align the menu to a specific corner, such as `top start` or `bottom end`.

### With disabled items

Use the `disabled` prop on a `DropdownItem` to disable that item and prevent it from being selected:

Options

```tsx
import { Dropdown, DropdownButton, DropdownItem, DropdownMenu } from '@/components/dropdown'
import { ChevronDownIcon } from '@heroicons/react/16/solid'

function Example({ url, renameFile, deleteFile }) {
  return (
    <Dropdown>
      <DropdownButton outline>
        Options
        <ChevronDownIcon />
      </DropdownButton>
      <DropdownMenu>
        <DropdownItem href={url}>Open</DropdownItem>
        <DropdownItem onClick={() => renameFile()} disabled>
          Rename
        </DropdownItem>
        <DropdownItem onClick={() => deleteFile()}>Delete</DropdownItem>
      </DropdownMenu>
    </Dropdown>
  )
}
```

### With sections

Use the `DropdownSection`, `DropdownHeading`, and `DropdownDivider` components to group dropdown items into sections:

Options

```tsx
import {
  Dropdown,
  DropdownButton,
  DropdownDivider,
  DropdownHeading,
  DropdownItem,
  DropdownMenu,
  DropdownSection,
} from '@/components/dropdown'
import { ChevronDownIcon } from '@heroicons/react/16/solid'

function Example() {
  return (
    <Dropdown>
      <DropdownButton outline>
        Options
        <ChevronDownIcon />
      </DropdownButton>
      <DropdownMenu>
        <DropdownSection aria-label="Account">
          <DropdownItem href="/account">Account</DropdownItem>
          <DropdownItem href="/notifications">Notifications</DropdownItem>
          <DropdownItem href="/billing">Billing</DropdownItem>
        </DropdownSection>
        <DropdownDivider />
        <DropdownSection>
          <DropdownHeading>My events</DropdownHeading>
          <DropdownItem href="/upcoming-events">Upcoming events</DropdownItem>
          <DropdownItem href="/past-events">Past events</DropdownItem>
        </DropdownSection>
      </DropdownMenu>
    </Dropdown>
  )
}
```

Headings are optional but be sure to add an `aria-label` to sections without headings for assistive technology.

### With descriptions

Use the `DropdownDescription` component along with a `DropdownLabel` to add a description to a dropdown item:

Options

```tsx
import {
  Dropdown,
  DropdownButton,
  DropdownDescription,
  DropdownItem,
  DropdownLabel,
  DropdownMenu,
} from '@/components/dropdown'
import { ChevronDownIcon } from '@heroicons/react/16/solid'

function Example({ url, renameFile, deleteFile }) {
  return (
    <Dropdown>
      <DropdownButton outline>
        Options
        <ChevronDownIcon />
      </DropdownButton>
      <DropdownMenu>
        <DropdownItem href={url} target="_blank">
          <DropdownLabel>Open</DropdownLabel>
          <DropdownDescription>Open the file in a new tab.</DropdownDescription>
        </DropdownItem>
        <DropdownItem onClick={() => renameFile()}>
          <DropdownLabel>Rename</DropdownLabel>
          <DropdownDescription>Rename the file.</DropdownDescription>
        </DropdownItem>
        <DropdownItem onClick={() => deleteFile()}>
          <DropdownLabel>Delete</DropdownLabel>
          <DropdownDescription>Move the file to the trash.</DropdownDescription>
        </DropdownItem>
      </DropdownMenu>
    </Dropdown>
  )
}
```

### With icons

Add an icon as the first child of a `DropdownItem` to render it alongside the `DropdownLabel`:

Options

```tsx
import {
  Dropdown,
  DropdownButton,
  DropdownDivider,
  DropdownItem,
  DropdownLabel,
  DropdownMenu,
} from '@/components/dropdown'
import {
  ArrowRightStartOnRectangleIcon,
  ChevronDownIcon,
  Cog8ToothIcon,
  InformationCircleIcon,
  MoonIcon,
  UserIcon,
} from '@heroicons/react/16/solid'

function Example() {
  return (
    <Dropdown>
      <DropdownButton outline>
        Options
        <ChevronDownIcon />
      </DropdownButton>
      <DropdownMenu anchor="bottom">
        <DropdownItem href="#">
          <UserIcon />
          <DropdownLabel>Account</DropdownLabel>
        </DropdownItem>
        <DropdownItem href="#">
          <Cog8ToothIcon />
          <DropdownLabel>Settings</DropdownLabel>
        </DropdownItem>
        <DropdownItem href="#">
          <InformationCircleIcon />
          <DropdownLabel>Help center</DropdownLabel>
        </DropdownItem>
        <DropdownDivider />
        <DropdownItem href="#">
          <MoonIcon />
          <DropdownLabel>Dark mode</DropdownLabel>
        </DropdownItem>
        <DropdownDivider />
        <DropdownItem href="#">
          <ArrowRightStartOnRectangleIcon />
          <DropdownLabel>Sign out</DropdownLabel>
        </DropdownItem>
      </DropdownMenu>
    </Dropdown>
  )
}
```

The `DropdownItem` component is designed to work best with 16×16 icons.

If you're using your own custom icons, make sure they include the `data-slot="icon"` prop so they receive the correct
styles.

### With keyboard shortcuts

Use the `DropdownShortcut` component along with a `DropdownLabel` to surface any keyboard shortcuts you've implemented
in your application:

Options

```tsx
import {
  Dropdown,
  DropdownButton,
  DropdownItem,
  DropdownLabel,
  DropdownMenu,
  DropdownShortcut,
} from '@/components/dropdown'
import { ChevronDownIcon } from '@heroicons/react/16/solid'

function Example({ url, renameFile, deleteFile }) {
  return (
    <Dropdown>
      <DropdownButton outline>
        Options
        <ChevronDownIcon />
      </DropdownButton>
      <DropdownMenu anchor="bottom start">
        <DropdownItem href={url}>
          <DropdownLabel>Open</DropdownLabel>
          <DropdownShortcut keys="⌘O" />
        </DropdownItem>
        <DropdownItem onClick={() => renameFile()}>
          <DropdownLabel>Rename</DropdownLabel>
          <DropdownShortcut keys="⌘R" />
        </DropdownItem>
        <DropdownItem onClick={() => deleteFile()}>
          <DropdownLabel>Delete</DropdownLabel>
          <DropdownShortcut keys="⇧⌘⌫" />
        </DropdownItem>
      </DropdownMenu>
    </Dropdown>
  )
}
```

### With header

Use the `DropdownHeader` component to add a custom header section to the top of a dropdown menu:

Options

```tsx
import {
  Dropdown,
  DropdownButton,
  DropdownDivider,
  DropdownHeader,
  DropdownItem,
  DropdownMenu,
} from '@/components/dropdown'
import { ChevronDownIcon } from '@heroicons/react/16/solid'

function Example({ signOut }) {
  return (
    <Dropdown>
      <DropdownButton outline>
        Options
        <ChevronDownIcon />
      </DropdownButton>
      <DropdownMenu>
        <DropdownHeader>
          <div className="pr-6">
            <div className="text-xs text-zinc-500 dark:text-zinc-400">Signed in as Tom Cook</div>
            <div className="text-sm/7 font-semibold text-zinc-800 dark:text-white">tom@example.com</div>
          </div>
        </DropdownHeader>
        <DropdownDivider />
        <DropdownItem href="/my-profile">My profile</DropdownItem>
        <DropdownItem href="/notifications">Notifications</DropdownItem>
        <DropdownItem href="/security">Security</DropdownItem>
        <DropdownItem href="/billing">Billing</DropdownItem>
        <DropdownItem onClick={() => signOut()}>Sign out</DropdownItem>
      </DropdownMenu>
    </Dropdown>
  )
}
```

It's important to note that assistive technology will not announce any content in a dropdown header, so keep this in
mind when deciding what type of content to include.

### With disabled button

Use the `disabled` prop on the `DropdownButton` component to disable a dropdown:

Options

```tsx
import { Dropdown, DropdownButton, DropdownItem, DropdownMenu } from '@/components/dropdown'
import { ChevronDownIcon } from '@heroicons/react/16/solid'

function Example({ deleteUser }) {
  return (
    <Dropdown>
      <DropdownButton outline disabled>
        Options
        <ChevronDownIcon />
      </DropdownButton>
      <DropdownMenu>
        <DropdownItem href="/users/1">View</DropdownItem>
        <DropdownItem href="/users/1/edit">Edit</DropdownItem>
        <DropdownItem onClick={() => deleteUser()}>Delete</DropdownItem>
      </DropdownMenu>
    </Dropdown>
  )
}
```

### With icon trigger

Use a `DropdownButton` with the `plain` prop in combination with an icon to make an icon-only dropdown trigger:

```tsx
import { Dropdown, DropdownButton, DropdownItem, DropdownMenu } from '@/components/dropdown'
import { EllipsisHorizontalIcon } from '@heroicons/react/16/solid'

function Example({ deleteUser }) {
  return (
    <Dropdown>
      <DropdownButton plain aria-label="More options">
        <EllipsisHorizontalIcon />
      </DropdownButton>
      <DropdownMenu>
        <DropdownItem href="/users/1">View</DropdownItem>
        <DropdownItem href="/users/1/edit">Edit</DropdownItem>
        <DropdownItem onClick={() => deleteUser()}>Delete</DropdownItem>
      </DropdownMenu>
    </Dropdown>
  )
}
```

Be sure to include an `aria-label` so the button is announced properly to assistive technology.

### With avatar trigger

Render the `DropdownButton` component as an `AvatarButton` component to use an avatar as the dropdown trigger:

![Avatar example](https://images.unsplash.com/photo-1595211877493-41a4e5f236b3?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=3&w=256&h=256&q=80)

```tsx
import { AvatarButton } from '@/components/avatar'
import { Dropdown, DropdownButton, DropdownDivider, DropdownItem, DropdownMenu } from '@/components/dropdown'

function Example({ currentUser, signOut }) {
  return (
    <Dropdown>
      <DropdownButton className="size-8" as={AvatarButton} src={currentUser.avatarUrl} aria-label="Account options" />
      <DropdownMenu placement="bottom">
        <DropdownItem href="/profile">My profile</DropdownItem>
        <DropdownItem href="/settings">Settings</DropdownItem>
        <DropdownDivider />
        <DropdownItem onClick={() => signOut()}>Sign out</DropdownItem>
      </DropdownMenu>
    </Dropdown>
  )
}
```

### With custom trigger

Use the `MenuButton` component from `@headlessui/react` directly to render your own custom dropdown trigger:

![Custom trigger example showing Whitney as Admin](https://images.unsplash.com/photo-1517365830460-955ce3ccd263?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80)

```tsx
import { Dropdown, DropdownDivider, DropdownItem, DropdownMenu } from '@/components/dropdown'
import * as Headless from '@headlessui/react'
import { ChevronUpDownIcon } from '@heroicons/react/16/solid'

function Example({ currentUser, signOut }) {
  return (
    <Dropdown>
      <Headless.MenuButton
        className="flex w-48 items-center gap-3 rounded-xl border border-transparent p-1 data-active:border-zinc-200 data-hover:border-zinc-200 dark:data-active:border-zinc-700 dark:data-hover:border-zinc-700"
        aria-label="Account options"
      >
        <img className="size-10 rounded-lg" src={currentUser.avatarUrl} alt="" />
        <span className="block text-left">
          <span className="block text-sm/5 font-medium">{currentUser.name}</span>
          <span className="block text-xs/5 text-zinc-500">{currentUser.role}</span>
        </span>
        <ChevronUpDownIcon className="mr-1 ml-auto size-4 shrink-0 stroke-zinc-400" />
      </Headless.MenuButton>
      <DropdownMenu className="min-w-(--button-width)">
        <DropdownItem href="/profile">My profile</DropdownItem>
        <DropdownItem href="/settings">Settings</DropdownItem>
        <DropdownDivider />
        <DropdownItem onClick={() => signOut()}>Sign out</DropdownItem>
      </DropdownMenu>
    </Dropdown>
  )
}
```

### With custom menu width

Use `min-w-*` utilities to increase the minimum width of a `DropdownMenu`, and `max-w-*` utilities to prevent it from
getting wider than a specific size:

Options

```tsx
import { Dropdown, DropdownButton, DropdownItem, DropdownMenu } from '@/components/dropdown'
import { ChevronDownIcon } from '@heroicons/react/16/solid'

function Example() {
  return (
    <Dropdown>
      <DropdownButton outline>
        Options
        <ChevronDownIcon />
      </DropdownButton>
      <DropdownMenu className="min-w-48">
        <DropdownItem href="/account">Account</DropdownItem>
        <DropdownItem href="/notifications">Notifications</DropdownItem>
        <DropdownItem href="/billing">Billing</DropdownItem>
      </DropdownMenu>
    </Dropdown>
  )
}
```

Dropdown menus are sized based on the width of their content by default, so this level of control can be helpful for
menus that have very short or very long items.
