[Home](https://catalyst.tailwindui.com/)

[Demo](https://catalyst-demo.tailwindui.com/) [Docs](https://catalyst.tailwindui.com/docs) [Buy UI Kit →](https://tailwindcss.com/plus/templates/catalyst)

Getting startedSidebar layoutStacked layoutAuth layoutAlertAvatarBadgeButtonCheckboxComboboxDescription listDialogDividerDropdownFieldsetHeadingInputListboxNavbarPaginationRadio buttonSelectSidebarSwitchTableTextTextarea

# Table

If you can put it in a database, you can put it in a table.

| Name | Email | Access |
| --- | --- | --- |
| Leslie Alexander | <leslie.alexander@example.com> | Admin |
| Michael Foster | <michael.foster@example.com> | Owner |
| Dries Vincent | <dries.vincent@example.com> | Member |
| Lindsay Walton | <lindsay.walton@example.com> | Member |
| Courtney Henry | <courtney.henry@example.com> | Admin |

## Component API

| Prop | Default | Description |
| :-- | :-- | :-- |
| **Table** extends the JSX `<table>` element | | |
| `bleed` | `false` | Whether the table should bleed into the gutter. |
| `dense` | `false` | Whether the table should use condensed spacing. |
| `grid` | `false` | Whether display vertical grid lines. |
| `striped` | `false` | Whether display striped table rows. |
| **TableHead** extends the JSX `<thead>` element | | |
| This component does not expose any component-specific props. | | |
| **TableBody** extends the JSX `<tbody>` element | | |
| This component does not expose any component-specific props. | | |
| **TableRow** extends the JSX `<tr>` element | | |
| `href` | - | The URL for the row when used as a link. |
| `target` | - | The target for the row when used as a link. |
| `title` | - | The title for the row whe used as a link. |
| **TableHeader** extends the JSX `<th>` element | | |
| This component does not expose any component-specific props. | | |
| **TableCell** extends the JSX `<td>` element | | |
| This component does not expose any component-specific props. | | |

## Examples

### Basic example

Use the `Table`, `TableHead`, `TableBody`, `TableRow`, `TableHeader`, and `TableCell` components to build a table:

| Name | Email | Access |
| --- | --- | --- |
| Leslie Alexander | <leslie.alexander@example.com> | Admin |
| Michael Foster | <michael.foster@example.com> | Owner |
| Dries Vincent | <dries.vincent@example.com> | Member |
| Lindsay Walton | <lindsay.walton@example.com> | Member |
| Courtney Henry | <courtney.henry@example.com> | Admin |

```tsx
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/table'

function Example({ users }) {
  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableHeader>Name</TableHeader>
          <TableHeader>Email</TableHeader>
          <TableHeader>Role</TableHeader>
        </TableRow>
      </TableHead>
      <TableBody>
        {users.map((user) => (
          <TableRow key={user.handle}>
            <TableCell className="font-medium">{user.name}</TableCell>
            <TableCell>{user.email}</TableCell>
            <TableCell className="text-zinc-500">{user.access}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
```

### Responsive tables

Tables automatically become scrollable when they are wider than their container:

| Name | Handle | Role | Email | Access |
| --- | --- | --- | --- | --- |
| Leslie Alexander | @lesliealexander | Co-Founder / CEO | <leslie.alexander@example.com> | Admin |
| Michael Foster | @michaelfoster | Co-Founder / CTO | <michael.foster@example.com> | Owner |
| Dries Vincent | @driesvincent | Business Relations | <dries.vincent@example.com> | Member |
| Lindsay Walton | @lindsaywalton | Front-end Developer | <lindsay.walton@example.com> | Member |
| Courtney Henry | @courtneyhenry | Designer | <courtney.henry@example.com> | Admin |

```tsx
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/table'

function Example({ users }) {
  return (
    <Table className="[--gutter:--spacing(6)] sm:[--gutter:--spacing(8)]">
      <TableHead>
        <TableRow>
          <TableHeader>Name</TableHeader>
          <TableHeader>Handle</TableHeader>
          <TableHeader>Role</TableHeader>
          <TableHeader>Email</TableHeader>
          <TableHeader>Access</TableHeader>
        </TableRow>
      </TableHead>
      <TableBody>
        {users.map((user) => (
          <TableRow key={user.handle}>
            <TableCell className="font-medium">{user.name}</TableCell>
            <TableCell>@{user.handle}</TableCell>
            <TableCell>{user.role}</TableCell>
            <TableCell>{user.email}</TableCell>
            <TableCell className="text-zinc-500">{user.access}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
```

Set the CSS `--gutter` variable to match the padding of the containing element to make sure the table isn't cropped
unnecessarily when it becomes scrollable. You can change the gutter responsively using media query variants, such as
`sm:[--gutter:--spacing(4)]`.

### Full-width tables

Use the `bleed` prop and set the CSS `--gutter` variable to match the padding of the containing element to make a table
full-width:

| Name | Email | Access |
| --- | --- | --- |
| Leslie Alexander | <leslie.alexander@example.com> | Admin |
| Michael Foster | <michael.foster@example.com> | Owner |
| Dries Vincent | <dries.vincent@example.com> | Member |
| Lindsay Walton | <lindsay.walton@example.com> | Member |
| Courtney Henry | <courtney.henry@example.com> | Admin |

```tsx
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/table'

function Example({ users }) {
  return (
    <Table bleed className="[--gutter:--spacing(6)] sm:[--gutter:--spacing(8)]">
      <TableHead>
        <TableRow>
          <TableHeader>Name</TableHeader>
          <TableHeader>Email</TableHeader>
          <TableHeader>Role</TableHeader>
        </TableRow>
      </TableHead>
      <TableBody>
        {users.map((user) => (
          <TableRow key={user.handle}>
            <TableCell className="font-medium">{user.name}</TableCell>
            <TableCell>{user.email}</TableCell>
            <TableCell className="text-zinc-500">{user.access}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
```

Full-width tables are still responsive and will become scrollable if they don't fit within the containing element.

### Rows as links

Use the `href` prop on the `TableRow` component to treat an entire row like a link:

| Name | Email | Access |
| --- | --- | --- |
| Leslie Alexander | <leslie.alexander@example.com> | Admin |
| Michael Foster | <michael.foster@example.com> | Owner |
| Dries Vincent | <dries.vincent@example.com> | Member |
| Lindsay Walton | <lindsay.walton@example.com> | Member |
| Courtney Henry | <courtney.henry@example.com> | Admin |

```tsx
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/table'

function Example({ users }) {
  return (
    <Table className="[--gutter:--spacing(6)] sm:[--gutter:--spacing(8)]">
      <TableHead>
        <TableRow>
          <TableHeader>Name</TableHeader>
          <TableHeader>Email</TableHeader>
          <TableHeader>Role</TableHeader>
        </TableRow>
      </TableHead>
      <TableBody>
        {users.map((user) => (
          <TableRow key={user.handle} href={user.url}>
            <TableCell className="font-medium">{user.name}</TableCell>
            <TableCell>{user.email}</TableCell>
            <TableCell className="text-zinc-500">{user.access}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
```

When used as a link, `TableRow` also accepts the `target` and `title` props like a regular link.

### With condensed spacing

Use the `dense` prop to render the table with condensed spacing:

| Rank | Player | Pos | GP | G | A | P | +/- |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Mitchell Marner | R | 80 | 30 | 69 | 99 | +18 |
| 2 | William Nylander | R | 82 | 40 | 47 | 87 | +10 |
| 3 | Auston Matthews | C | 74 | 40 | 45 | 85 | +31 |
| 4 | John Tavares | C | 80 | 36 | 44 | 80 | -7 |
| 5 | Michael Bunting | L | 82 | 23 | 26 | 49 | +21 |
| 6 | Morgan Rielly | D | 65 | 4 | 37 | 41 | -9 |
| 7 | Calle Jarnkrok | C | 73 | 20 | 19 | 39 | +9 |
| 8 | Alex Kerfoot | C | 82 | 10 | 22 | 32 | +8 |
| 9 | David Kampf | C | 82 | 7 | 20 | 27 | +6 |
| 10 | Mark Giordano | D | 78 | 4 | 20 | 24 | +27 |

```tsx
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/table'

function Example({ players }) {
  return (
    <Table dense className="[--gutter:--spacing(6)] sm:[--gutter:--spacing(8)]">
      <TableHead>
        <TableRow>
          <TableHeader>Rank</TableHeader>
          <TableHeader>Player</TableHeader>
          <TableHeader className="text-right">Pos</TableHeader>
          <TableHeader className="text-right">GP</TableHeader>
          <TableHeader className="text-right">G</TableHeader>
          <TableHeader className="text-right">A</TableHeader>
          <TableHeader className="text-right">P</TableHeader>
          <TableHeader className="text-right">+/-</TableHeader>
        </TableRow>
      </TableHead>
      <TableBody>
        {players.map((player) => (
          <TableRow key={player.rank}>
            <TableCell className="tabular-nums">{player.rank}</TableCell>
            <TableCell className="font-medium">{player.name}</TableCell>
            <TableCell className="text-right">{player.position}</TableCell>
            <TableCell className="text-right tabular-nums">{player.gamesPlayed}</TableCell>
            <TableCell className="text-right tabular-nums">{player.goals}</TableCell>
            <TableCell className="text-right tabular-nums">{player.assists}</TableCell>
            <TableCell className="text-right tabular-nums">{player.points}</TableCell>
            <TableCell className="text-right tabular-nums">{player.plusMinus}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
```

### With grid lines

Use the `grid` prop to render the table with vertical grid lines:

| Name | Email | Access |
| --- | --- | --- |
| Leslie Alexander | <leslie.alexander@example.com> | Admin |
| Michael Foster | <michael.foster@example.com> | Owner |
| Dries Vincent | <dries.vincent@example.com> | Member |
| Lindsay Walton | <lindsay.walton@example.com> | Member |
| Courtney Henry | <courtney.henry@example.com> | Admin |

```tsx
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/table'

function Example({ users }) {
  return (
    <Table grid className="[--gutter:--spacing(6)] sm:[--gutter:--spacing(8)]">
      <TableHead>
        <TableRow>
          <TableHeader>Name</TableHeader>
          <TableHeader>Email</TableHeader>
          <TableHeader>Role</TableHeader>
        </TableRow>
      </TableHead>
      <TableBody>
        {users.map((user) => (
          <TableRow key={user.handle}>
            <TableCell className="font-medium">{user.name}</TableCell>
            <TableCell>{user.email}</TableCell>
            <TableCell className="text-zinc-500">{user.access}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
```

### With striped rows

Use the `striped` prop to render the table with striped rows and no horizontal borders:

| Name | Email | Access |
| --- | --- | --- |
| Leslie Alexander | <leslie.alexander@example.com> | Admin |
| Michael Foster | <michael.foster@example.com> | Owner |
| Dries Vincent | <dries.vincent@example.com> | Member |
| Lindsay Walton | <lindsay.walton@example.com> | Member |
| Courtney Henry | <courtney.henry@example.com> | Admin |

```tsx
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/table'

function Example({ users }) {
  return (
    <Table striped className="[--gutter:--spacing(6)] sm:[--gutter:--spacing(8)]">
      <TableHead>
        <TableRow>
          <TableHeader>Name</TableHeader>
          <TableHeader>Email</TableHeader>
          <TableHeader>Role</TableHeader>
        </TableRow>
      </TableHead>
      <TableBody>
        {users.map((user) => (
          <TableRow key={user.handle}>
            <TableCell className="font-medium">{user.name}</TableCell>
            <TableCell>{user.email}</TableCell>
            <TableCell className="text-zinc-500">{user.access}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
```

### With different heading color

Use the `text-{color}` utilities on the `TableRow` component inside your `TableHead` to change the color of table
headings:

| Name | Email | Access |
| --- | --- | --- |
| Leslie Alexander | <leslie.alexander@example.com> | Admin |
| Michael Foster | <michael.foster@example.com> | Owner |
| Dries Vincent | <dries.vincent@example.com> | Member |
| Lindsay Walton | <lindsay.walton@example.com> | Member |
| Courtney Henry | <courtney.henry@example.com> | Admin |

```tsx
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/table'

function Example({ users }) {
  return (
    <Table className="[--gutter:--spacing(6)] sm:[--gutter:--spacing(8)]">
      <TableHead>
        <TableRow className="text-zinc-950 dark:text-white">
          <TableHeader>Name</TableHeader>
          <TableHeader>Email</TableHeader>
          <TableHeader>Role</TableHeader>
        </TableRow>
      </TableHead>
      <TableBody>
        {users.map((user) => (
          <TableRow key={user.handle}>
            <TableCell className="font-medium">{user.name}</TableCell>
            <TableCell>{user.email}</TableCell>
            <TableCell className="text-zinc-500">{user.access}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
```

### With complex content

Tables are unopinionated about their content and will adapt to just about anything you include:

| Name | Role | Status |
| --- | --- | --- |
| ![Leslie Alexander avatar](https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80)<br>Leslie Alexander<br>[leslie.alexander@example.com](https://catalyst.tailwindui.com/docs/table#) | Admin | Online |
| ![Michael Foster avatar](https://images.unsplash.com/photo-1519244703995-f4e0f30006d5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80)<br>Michael Foster<br>[michael.foster@example.com](https://catalyst.tailwindui.com/docs/table#) | Owner | Online |
| ![Dries Vincent avatar](https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80)<br>Dries Vincent<br>[dries.vincent@example.com](https://catalyst.tailwindui.com/docs/table#) | Member | Offline |
| ![Lindsay Walton avatar](https://images.unsplash.com/photo-1517841905240-472988babdf9?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80)<br>Lindsay Walton<br>[lindsay.walton@example.com](https://catalyst.tailwindui.com/docs/table#) | Member | Online |
| ![Courtney Henry avatar](https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80)<br>Courtney Henry<br>[courtney.henry@example.com](https://catalyst.tailwindui.com/docs/table#) | Admin | Online |

```tsx
import { Avatar } from '@/components/avatar'
import { Badge } from '@/components/badge'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/table'

export function ComplexExample({ users }) {
  return (
    <Table className="[--gutter:--spacing(6)] sm:[--gutter:--spacing(8)]">
      <TableHead>
        <TableRow>
          <TableHeader>Name</TableHeader>
          <TableHeader>Role</TableHeader>
          <TableHeader>Status</TableHeader>
        </TableRow>
      </TableHead>
      <TableBody>
        {users.map((user) => (
          <TableRow key={user.handle}>
            <TableCell>
              <div className="flex items-center gap-4">
                <Avatar src={user.avatarUrl} className="size-12" />
                <div>
                  <div className="font-medium">{user.name}</div>
                  <div className="text-zinc-500">
                    <a href="#" className="hover:text-zinc-700">
                      {user.email}
                    </a>
                  </div>
                </div>
              </div>
            </TableCell>
            <TableCell className="text-zinc-500">{user.access}</TableCell>
            <TableCell>
              {user.online ? <Badge color="lime">Online</Badge> : <Badge color="zinc">Offline</Badge>}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
```

### With pagination

Add a `Pagination` component below your table to add pagination controls:

Users

| Name | Email | Access |
| --- | --- | --- |
| Leslie Alexander | <leslie.alexander@example.com> | Admin |
| Michael Foster | <michael.foster@example.com> | Owner |
| Dries Vincent | <dries.vincent@example.com> | Member |
| Lindsay Walton | <lindsay.walton@example.com> | Member |
| Courtney Henry | <courtney.henry@example.com> | Admin |

```tsx
import {
  Pagination,
  PaginationGap,
  PaginationList,
  PaginationNext,
  PaginationPage,
  PaginationPrevious,
} from '@/components/pagination'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/table'

function Example({ users }) {
  return (
    <>
      <h1 className="mb-6 text-base font-semibold">Users</h1>
      <Table>
        <TableHead>
          <TableRow>
            <TableHeader>Name</TableHeader>
            <TableHeader>Email</TableHeader>
            <TableHeader>Access</TableHeader>
          </TableRow>
        </TableHead>
        <TableBody>
          {users.map((user) => (
            <TableRow key={user.handle}>
              <TableCell className="font-medium">{user.name}</TableCell>
              <TableCell>{user.email}</TableCell>
              <TableCell className="text-zinc-500">{user.access}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <Pagination className="mt-6">
        <PaginationPrevious href="?page=2" />
        <PaginationList>
          <PaginationPage href="?page=1">1</PaginationPage>
          <PaginationPage href="?page=2">2</PaginationPage>
          <PaginationPage href="?page=3" current>
            3
          </PaginationPage>
          <PaginationPage href="?page=4">4</PaginationPage>
          <PaginationGap />
          <PaginationPage href="?page=65">65</PaginationPage>
          <PaginationPage href="?page=66">66</PaginationPage>
        </PaginationList>
        <PaginationNext href="?page=4" />
      </Pagination>
    </>
  )
}
```

Use the `mt-*` utilities to control the space between the table and the pagination controls.

### With dropdowns

Use the `Dropdown` component within a `TableCell` to add a dropdown menu:

| Name | Email | Access | Actions |
| --- | --- | --- | --- |
| Leslie Alexander | <leslie.alexander@example.com> | Admin | |
| Michael Foster | <michael.foster@example.com> | Owner | |
| Dries Vincent | <dries.vincent@example.com> | Member | |
| Lindsay Walton | <lindsay.walton@example.com> | Member | |
| Courtney Henry | <courtney.henry@example.com> | Admin | |

```tsx
import { Dropdown, DropdownButton, DropdownItem, DropdownMenu } from '@/components/dropdown'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/table'
import { EllipsisHorizontalIcon } from '@heroicons/react/16/solid'

function Example({ users }) {
  return (
    <Table className="[--gutter:--spacing(6)] sm:[--gutter:--spacing(8)]">
      <TableHead>
        <TableRow>
          <TableHeader>Name</TableHeader>
          <TableHeader>Email</TableHeader>
          <TableHeader>Access</TableHeader>
          <TableHeader className="relative w-0">
            <span className="sr-only">Actions</span>
          </TableHeader>
        </TableRow>
      </TableHead>
      <TableBody>
        {users.map((user) => (
          <TableRow key={user.handle}>
            <TableCell className="font-medium">{user.name}</TableCell>
            <TableCell>{user.email}</TableCell>
            <TableCell className="text-zinc-500">{user.access}</TableCell>
            <TableCell>
              <div className="-mx-3 -my-1.5 sm:-mx-2.5">
                <Dropdown>
                  <DropdownButton plain aria-label="More options">
                    <EllipsisHorizontalIcon />
                  </DropdownButton>
                  <DropdownMenu anchor="bottom end">
                    <DropdownItem>View</DropdownItem>
                    <DropdownItem>Edit</DropdownItem>
                    <DropdownItem>Delete</DropdownItem>
                  </DropdownMenu>
                </Dropdown>
              </div>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
```

When adding elements like dropdowns to a table (especially with the `plain` style), consider using negative margins to
avoid increasing the size of the table cell. For instance, in the example above we've added `-my-1.5` to make sure the
dropdown only takes up 24px of vertical space in the actual layout, which matches the height of the text in the other
cells.

### In dialog

Add a `Table` to your `DialogBody` component to include a table in a dialog:

Show users

```tsx
import { Button } from '@/components/button'
import { Dialog, DialogActions, DialogBody, DialogDescription, DialogTitle } from '@/components/dialog'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/table'
import { useState } from 'react'

function Example({ users }) {
  let [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <Button type="button" onClick={() => setIsOpen(true)}>
        Show users
      </Button>
      <Dialog open={isOpen} onClose={setIsOpen} size="3xl">
        <DialogTitle>Users</DialogTitle>
        <DialogDescription>The follow users have access to your account.</DialogDescription>
        <DialogBody>
          <Table bleed compact>
            <TableHead>
              <TableRow>
                <TableHeader>Name</TableHeader>
                <TableHeader>Email</TableHeader>
                <TableHeader>Role</TableHeader>
              </TableRow>
            </TableHead>
            <TableBody>
              {users.map((user) => (
                <TableRow key={user.handle}>
                  <TableCell className="font-medium">{user.name}</TableCell>
                  <TableCell>{user.email}</TableCell>
                  <TableCell className="text-zinc-500">{user.access}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </DialogBody>
        <DialogActions>
          <Button onClick={() => setIsOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </>
  )
}
```

When using tables within dialogs, the `--gutter` variable is automatically set to match the dialog's padding.
