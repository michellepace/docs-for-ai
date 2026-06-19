# <Show>

The [<Show />](https://clerk.com/docs/nextjs/reference/components/control/show.md) component protects content or even entire routes based on:

- authentication: whether the user is signed-in or not.
- authorization: whether the user has been granted a specific type of access control (Role, Permission, Feature, or Plan)

`<Show />` with `when='signed-in'` or `when='signed-out'` performs authentication checks. To perform authorization checks, you can pass different values to the `when` prop, like `when={{ role: '...' }}`, `when={{ permission: '...' }}`, `when={{ feature: '...' }}`, or `when={{ plan: '...' }}`.

`<Show />` accepts a `fallback` prop that will be rendered if the user fails the authentication or authorization checks.

`<Show />` can be used both client-side and server-side (in Server Components).

> This component only **visually hides** its children. The contents of its children remain accessible via the browser's source code even if the user fails the authentication/authorization check. Do not use this component to hide sensitive information that should be completely inaccessible to unauthorized users. For truly sensitive data, perform authorization checks on the server before sending the data to the client.

## Usage

### Authentication checks

`<Show when='signed-in'>` performs authentication checks. It will render its children if the user is signed-in, and its `fallback` prop if the user is signed-out.

filename: app/dashboard/page.tsx
```tsx
import { Show } from '@clerk/nextjs'

export default function Page() {
  return (
    <Show fallback={<p>Users that are signed-out can see this.</p>} when="signed-in">
      <p>Users that are signed-in can see this.</p>
    </Show>
  )
}
```

### Authorization checks

To limit who is able to see the content that `<Show>` renders, you can pass **one** of the access control values to the `when` prop: `when={{ permission: '...' }}`, `when={{ role: '...' }}`, `when={{ feature: '...' }}`, or `when={{ plan: '...' }}`. It's recommended to use **Permission-based** authorization over **Role-based** authorization, and **Feature-based** authorization over **Plan-based** authorization, as they are more flexible, easier to manage, and more secure.

If you use `when='signed-in'` without any access control values, `<Show>` will render its children if the user is signed in, regardless of their Role or its Permissions.

For more complex authorization logic, [pass conditional logic to the when prop](https://clerk.com/docs/nextjs/reference/components/control/show.md#render-content-conditionally).

### Render content by Permissions

The following example demonstrates how to use the `<Show />` component to protect content by checking if the user has the `org:invoices:create` Permission.

filename: app/protected/invoices/page.tsx
```jsx
import { Show } from '@clerk/nextjs'

export default function Page() {
  return (
    <Show
      when={{ permission: 'org:invoices:create' }}
      fallback={<p>You do not have the Permissions to create an invoice.</p>}
    >
      <p>Users with Permission org:invoices:create can see this.</p>
    </Show>
  )
}
```

### Render content by Role

While authorization by `when={{ permission: '...' }}` is **recommended**, for convenience, `<Show>` allows a `when={{ role: '...' }}` prop to be passed.

The following example demonstrates how to use the `<Show />` component to protect content by checking if the user has the `org:billing` Role.

filename: app/protected/billing/page.tsx
```jsx
import { Show } from '@clerk/nextjs'

export default function ProtectPage() {
  return (
    <Show
      when={{ role: 'org:billing' }}
      fallback={<p>Only a member of the Billing department can access this content.</p>}
    >
      <p>Users with Role org:billing can see this.</p>
    </Show>
  )
}
```

### Render content by Plan

The following example demonstrates how to use `<Show />` to protect content by checking if the user has a Plan.

filename: app/protected/bronze/page.tsx
```tsx
import { Show } from '@clerk/nextjs'

export default function ProtectPage() {
  return (
    <Show
      when={{ plan: 'bronze' }}
      fallback={<p>Sorry, only subscribers to the Bronze plan can access this content.</p>}
    >
      <p>Welcome, Bronze subscriber!</p>
    </Show>
  )
}
```

### Render content by Feature

The following example demonstrates how to use `<Show />` to protect content by checking if the user has a Feature.

filename: app/protected/premium-access/page.tsx
```tsx
import { Show } from '@clerk/nextjs'

export default function Page() {
  return (
    <Show
      when={{ feature: 'premium_access' }}
      fallback={
        <p>Sorry, only subscribers with the Premium Access feature can access this content.</p>
      }
    >
      <p>Congratulations! You have access to the Premium Access feature.</p>
    </Show>
  )
}
```

### Render content conditionally

The following example uses `<Show>`'s `when` prop with a callback function to conditionally render its children if the user has the correct Role.

filename: app/dashboard/settings/page.tsx
```tsx
import type { PropsWithChildren } from 'react'
import { Show } from '@clerk/nextjs'

export default function Page() {
  return (
    <Show
      when={(has) => has({ role: 'org:admin' }) || has({ role: 'org:billing_manager' })}
      fallback={<p>Only an Admin or Billing Manager can access this content.</p>}
    >
      <p>The settings page.</p>
    </Show>
  )
}
```

## Properties

| Name                     | Type                                                                                                                                         | Description                                                                                                                                                                                                                              |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| fallback?                | JSX                                                                                                                                          | An element to be rendered when a user doesn't have the correct type of access control to access the protected content.                                                                                                                   |
| treatPendingAsSignedOut? | boolean                                                                                                                                      | A boolean that indicates whether to treat pending sessions as signed out. Defaults to true.                                                                                                                                              |
| when                     | 'signed-in' | 'signed-out' | { feature: string } | { permission: string } | { plan: string } | { role: string } | (has) => boolean | Determines when to render the children. Can be 'signed-in' or 'signed-out' for authentication checks, an object with a Feature, Permission, Plan, or Role for authorization checks, or a callback function for custom conditional logic. |

---

## Sitemap

[Overview of all docs pages](https://clerk.com/docs/llms.txt)
