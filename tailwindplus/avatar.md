[Home](https://catalyst.tailwindui.com/)

[Demo](https://catalyst-demo.tailwindui.com/) [Docs](https://catalyst.tailwindui.com/docs) [Buy UI Kit →](https://tailwindcss.com/plus/templates/catalyst)

Getting startedSidebar layoutStacked layoutAuth layoutAlertAvatarBadgeButtonCheckboxComboboxDescription listDialogDividerDropdownFieldsetHeadingInputListboxNavbarPaginationRadio buttonSelectSidebarSwitchTableTextTextarea

# Avatar

It's more than just an image with a border radius, I promise.

![Avatar small size](https://images.unsplash.com/photo-1595211877493-41a4e5f236b3?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=3&w=256&h=256&q=80)![Avatar medium size](https://images.unsplash.com/photo-1595211877493-41a4e5f236b3?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=3&w=256&h=256&q=80)![Avatar large size](https://images.unsplash.com/photo-1595211877493-41a4e5f236b3?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=3&w=256&h=256&q=80)

```
import { Avatar } from '@/components/avatar'

function Example({ user }) {
  return (
    <>
      <Avatar className="size-6" src={user.avatarUrl} />
      <Avatar className="size-8" src={user.avatarUrl} />
      <Avatar className="size-10" src={user.avatarUrl} />
    </>
  )
}
```

```
import { Avatar } from '@/components/avatar'

function Example({ user }) {
  return (
    <>
      <Avatar className="size-6" src={user.avatarUrl} />
      <Avatar className="size-8" src={user.avatarUrl} />
      <Avatar className="size-10" src={user.avatarUrl} />
    </>
  )
}
```

## Component API

| Prop | Default | Description |
| :-- | :-- | :-- |
| **Avatar** extends the JSX `<span>` element | | |
| `src` | - | The URL of the avatar image. |
| `square` | `false` | Whether to make the avatar square. |
| `initials` | - | The initials to use when no `src` is provided. |
| **AvatarButton** extends the Headless UI `Button` component or the [`Link`](https://catalyst.tailwindui.com/docs#client-side-router-integration) component | | |
| `src` | - | The URL of the avatar image. |
| `square` | `false` | Whether to make the avatar square. |
| `initials` | - | The initials to use when no `src` is provided. |
| `href` | - | The target URL when using the button as a link. |

## Examples

### Basic example

Use the `Avatar` component along with a `size-*` utility to render an avatar image:

![Avatar small size](https://images.unsplash.com/photo-1595211877493-41a4e5f236b3?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=3&w=256&h=256&q=80)![Avatar medium size](https://images.unsplash.com/photo-1595211877493-41a4e5f236b3?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=3&w=256&h=256&q=80)![Avatar large size](https://images.unsplash.com/photo-1595211877493-41a4e5f236b3?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=3&w=256&h=256&q=80)

```
import { Avatar } from '@/components/avatar'

function Example({ user }) {
  return (
    <>
      <Avatar className="size-6" src={user.avatarUrl} />
      <Avatar className="size-8" src={user.avatarUrl} />
      <Avatar className="size-10" src={user.avatarUrl} />
    </>
  )
}
```

```
import { Avatar } from '@/components/avatar'

function Example({ user }) {
  return (
    <>
      <Avatar className="size-6" src={user.avatarUrl} />
      <Avatar className="size-8" src={user.avatarUrl} />
      <Avatar className="size-10" src={user.avatarUrl} />
    </>
  )
}
```

### With initials

Use the `initials` prop to render an avatar with initials:

twtwtw

```
import { Avatar } from '@/components/avatar'

function Example() {
  return (
    <>
      <Avatar initials="tw" className="size-6 bg-zinc-900 text-white dark:bg-white dark:text-black" />
      <Avatar initials="tw" className="size-8 bg-zinc-900 text-white dark:bg-white dark:text-black" />
      <Avatar initials="tw" className="size-10 bg-zinc-900 text-white dark:bg-white dark:text-black" />
    </>
  )
}
```

```
import { Avatar } from '@/components/avatar'

function Example() {
  return (
    <>
      <Avatar initials="tw" className="size-6 bg-zinc-900 text-white dark:bg-white dark:text-black" />
      <Avatar initials="tw" className="size-8 bg-zinc-900 text-white dark:bg-white dark:text-black" />
      <Avatar initials="tw" className="size-10 bg-zinc-900 text-white dark:bg-white dark:text-black" />
    </>
  )
}
```

Be sure to include `bg-{color}` and `text-{color}` utilities for both light mode and dark mode.

### With initials as fallback

Include both the `src` and `initials` props to show the initials as a fallback while the avatar image loads:

tw![Avatar with initials fallback small size](https://images.unsplash.com/photo-1595211877493-41a4e5f236b3?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=3&w=256&h=256&q=80)tw![Avatar with initials fallback medium size](https://images.unsplash.com/photo-1595211877493-41a4e5f236b3?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=3&w=256&h=256&q=80)tw![Avatar with initials fallback large size](https://images.unsplash.com/photo-1595211877493-41a4e5f236b3?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=3&w=256&h=256&q=80)

```
import { Avatar } from '@/components/avatar'

function Example({ user }) {
  return (
    <>
      <Avatar src={user.avatarUrl} initials={user.initials} className="size-6 bg-purple-500 text-white" />
      <Avatar src={user.avatarUrl} initials={user.initials} className="size-8 bg-purple-500 text-white" />
      <Avatar src={user.avatarUrl} initials={user.initials} className="size-10 bg-purple-500 text-white" />
    </>
  )
}
```

```
import { Avatar } from '@/components/avatar'

function Example({ user }) {
  return (
    <>
      <Avatar src={user.avatarUrl} initials={user.initials} className="size-6 bg-purple-500 text-white" />
      <Avatar src={user.avatarUrl} initials={user.initials} className="size-8 bg-purple-500 text-white" />
      <Avatar src={user.avatarUrl} initials={user.initials} className="size-10 bg-purple-500 text-white" />
    </>
  )
}
```

### Square avatars

Use the `square` prop to render a square avatar:

![Square avatar with image](https://images.unsplash.com/photo-1595211877493-41a4e5f236b3?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=3&w=256&h=256&q=80)tw

```
import { Avatar } from '@/components/avatar'

function Example({ user }) {
  return (
    <>
      <Avatar square className="size-8" src={user.avatarUrl} />
      <Avatar square initials={user.initials} className="size-8 bg-zinc-900 text-white dark:bg-white dark:text-black" />
    </>
  )
}
```

```
import { Avatar } from '@/components/avatar'

function Example({ user }) {
  return (
    <>
      <Avatar square className="size-8" src={user.avatarUrl} />
      <Avatar square initials={user.initials} className="size-8 bg-zinc-900 text-white dark:bg-white dark:text-black" />
    </>
  )
}
```

### Avatar groups

Use utility classes to overlap a list of avatars and style them as a group:

![Avatar 1](https://images.unsplash.com/photo-1519244703995-f4e0f30006d5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80)![Avatar 2](https://images.unsplash.com/photo-1550525811-e5869dd03032?ixlib=rb-1.2.1&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80)![Avatar 3](https://images.unsplash.com/photo-1500648767791-00dcc994a43e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2.25&w=256&h=256&q=80)![Avatar 4](https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80)

```
import { Avatar } from '@/components/avatar'

function Example({ users }) {
  return (
    <div className="flex items-center justify-center -space-x-2">
      {users.map((user) => (
        <Avatar src={user.avatarUrl} className="size-8 ring-2 ring-white dark:ring-zinc-900" />
      ))}
    </div>
  )
}
```

```
import { Avatar } from '@/components/avatar'

function Example({ users }) {
  return (
    <div className="flex items-center justify-center -space-x-2">
      {users.map((user) => (
        <Avatar src={user.avatarUrl} className="size-8 ring-2 ring-white dark:ring-zinc-900" />
      ))}
    </div>
  )
}
```

Use the `ring-{color}` and `dark:ring-{color}` utilities to match the notched area with your background color.

### Using as buttons

Use the `AvatarButton` component to render an avatar as a button:

![Avatar button round](https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80)![Avatar button square](https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80)

```
import { AvatarButton } from '@/components/avatar'

function Example({ user }) {
  return (
    <>
      <AvatarButton className="size-8" src={user.avatarUrl} />
      <AvatarButton square className="size-8" src={user.avatarUrl} />
    </>
  )
}
```

```
import { AvatarButton } from '@/components/avatar'

function Example({ user }) {
  return (
    <>
      <AvatarButton className="size-8" src={user.avatarUrl} />
      <AvatarButton square className="size-8" src={user.avatarUrl} />
    </>
  )
}
```

### Using as links

Use the `AvatarButton` component with the `href` prop to render an avatar as a link:

[![Avatar link round](https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80)](https://catalyst.tailwindui.com/docs/avatar#)[![Avatar link square](https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80)](https://catalyst.tailwindui.com/docs/avatar#)

```
import { AvatarButton } from '@/components/avatar'

function Example({ user }) {
  return (
    <>
      <AvatarButton href={user.url} className="size-8" src={user.avatarUrl} />
      <AvatarButton square href={user.url} className="size-8" src={user.avatarUrl} />
    </>
  )
}
```

```
import { AvatarButton } from '@/components/avatar'

function Example({ user }) {
  return (
    <>
      <AvatarButton href={user.url} className="size-8" src={user.avatarUrl} />
      <AvatarButton square href={user.url} className="size-8" src={user.avatarUrl} />
    </>
  )
}
```
