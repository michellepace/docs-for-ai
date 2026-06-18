# Users

To get started, it's important to first understand Clerk's [User object](https://clerk.com/docs/reference/objects/user.md).

The `User` object holds all of the information for a single user of your application and provides a set of methods to manage their account. Each `User` has at least one authentication identifier, which might be their email address, phone number, or a username.

A user can be contacted at their primary email address or primary phone number. They can have more than one registered email address or phone number, but only one of them will be their primary email address (`User.primaryEmailAddress`) or primary phone number (`User.primaryPhoneNumber`). At the same time, a user can also have one or more external accounts by connecting to [social providers](https://clerk.com/docs/guides/configure/auth-strategies/social-connections/overview.md) such as Google, Apple, Facebook, and many more (`User.externalAccounts`).

Finally, a `User` object holds profile data like the user's name, profile picture, and a set of [metadata](https://clerk.com/docs/guides/users/extending.md) that can be used internally to store arbitrary information. The metadata are split into `publicMetadata` and `privateMetadata`. Both types are set from the [Backend API](https://clerk.com/docs/reference/backend-api){{ target: '_blank' }}, but public metadata can also be accessed from the [Frontend API](https://clerk.com/docs/reference/frontend-api){{ target: '_blank' }}.

For more information on the `User` object, such as helper methods for retrieving and updating user information and authentication status, see the [reference docs](https://clerk.com/docs/reference/objects/user.md). The `User` object is also available in the backend, but it looks slightly different. For more information, see the [Backend `User` object reference docs](https://clerk.com/docs/reference/backend/types/backend-user.md).

## Manage users

You can manage your users [in the Clerk Dashboard](#in-the-clerk-dashboard), or [programmatically](#programmatically).

### In the Clerk Dashboard

To manage users in the Clerk Dashboard, navigate to the [**Users**](https://dashboard.clerk.com/~/users) page. For more information on what's available on each user's profile, see the [User profile](https://clerk.com/docs/guides/dashboard/user-profile.md) guide.

### Programmatically

You can manage users programmatically through the [frontend](#in-the-frontend) or [backend](#in-the-backend).

#### In the frontend

Depending on the level of abstraction you need, you can manage users in the frontend using Clerk's prebuilt components, React hooks, or lower-level JavaScript methods.

- Prebuilt components: Clerk provides the prebuilt components [<UserButton />](https://clerk.com/docs/reference/components/user/user-button.md) and [<UserProfile />](https://clerk.com/docs/reference/components/user/user-profile.md) to help your users manage their profile data.
- Hooks: Because Clerk's React-based SDKs are built on top of the Clerk React SDK, you can use the [hooks](https://clerk.com/docs/reference/react/overview.md#custom-hooks) that the React SDK provides. These hooks include access to the `User` object and helpful methods for managing user authentication and profile data.
- JavaScript methods: If Clerk's prebuilt components don't meet your specific needs or if you require more control over the logic, you can rebuild the existing Clerk flows using the Clerk API. For more information, see the [custom flow guides](https://clerk.com/docs/guides/development/custom-flows/overview.md).

#### In the backend

[`clerkClient`](https://clerk.com/docs/reference/backend/overview.md) is a wrapper around the [Backend API](https://clerk.com/docs/reference/backend-api){{ target: '_blank' }} that makes it easier to interact with the API. It includes many methods for managing users, such as `getUser()`, `createUser()`, and `deleteUser()`. For more information, see the [`clerkClient` reference docs](https://clerk.com/docs/reference/backend/overview.md).

## Create users

You can create users either [in the Clerk Dashboard](#in-the-clerk-dashboard-2) or [programmatically](#programmatically-2).

### In the Clerk Dashboard

To create a user in the Clerk Dashboard, navigate to the [**Users**](https://dashboard.clerk.com/~/users) page and select **Create user**.

### Programmatically

To create a user programmatically, you can either [make a request directly to Clerk's Backend API](https://clerk.com/docs/reference/backend/user/create-user.md#backend-api-bapi-endpoint) or use the [`createUser()`](https://clerk.com/docs/reference/backend/user/create-user.md) method as shown in the following example.

filename: app/api/example/route.ts
```ts
import { auth, clerkClient } from '@clerk/nextjs/server'
import { NextResponse } from 'next/server'

export async function POST() {
  const client = await clerkClient()

  const user = await client.users.createUser({
    emailAddress: ['test@example.com'],
    password: 'password',
  })

  return NextResponse.json({ message: 'User created', user })
}
```

## Delete users

You can delete users either [in the Clerk Dashboard](#in-the-clerk-dashboard-3) or [programmatically](#programmatically-3).

> Bulk deletion of users cannot currently be done through the Clerk Dashboard or programmatically. If you need to bulk delete users, please [contact support](https://clerk.com/contact/support){{ target: '_blank' }}.

### In the Clerk Dashboard

To delete a user in the Clerk Dashboard, navigate to the [**Users**](https://dashboard.clerk.com/~/users) page. You can either select the user and then in the side navigation menu, select **Delete user**, or select the menu icon on the right side of the user's row and select **Delete user**.

### Programmatically

To delete a user programmatically, you can either [make a request directly to Clerk's Backend API](https://clerk.com/docs/reference/backend/user/delete-user.md#backend-api-bapi-endpoint) or use the [`deleteUser()`](https://clerk.com/docs/reference/backend/user/delete-user.md) method as shown in the following example.

filename: app/api/example/route.ts
```ts
import { auth, clerkClient } from '@clerk/nextjs/server'
import { NextResponse } from 'next/server'

export async function POST() {
  const { isAuthenticated, userId } = await auth()

  // Protect the route by checking if the user is signed in
  if (!isAuthenticated) {
    return new NextResponse('Unauthorized', { status: 401 })
  }

  // Initialize clerkClient
  const client = await clerkClient()

  // Use the `deleteUser()` method to delete the user
  await client.users.deleteUser(userId)

  // Return the success status
  return NextResponse.json({ success: true })
}
```

---

## Sitemap

[Overview of all docs pages](https://clerk.com/docs/llms.txt)
