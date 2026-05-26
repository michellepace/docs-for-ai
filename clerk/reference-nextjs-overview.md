# Clerk Next.js SDK

The Clerk Next.js SDK gives you access to prebuilt components, React hooks, and helpers to make user authentication easier. Refer to the [quickstart guide](https://clerk.com/docs/nextjs/getting-started/quickstart.md) to get started.

## `clerkMiddleware()`

The `clerkMiddleware()` helper integrates Clerk authentication into your Next.js application through middleware. It allows you to integrate authorization into both the client and server of your application. You can learn more [here](https://clerk.com/docs/reference/nextjs/clerk-middleware.md).

## Client-side helpers

Because the Next.js SDK is built on top of the Clerk React SDK, you can use the hooks that the React SDK provides. These hooks include access to the [Clerk](https://clerk.com/docs/reference/objects/clerk.md) object, [User object](https://clerk.com/docs/reference/objects/user.md), [Organization object](https://clerk.com/docs/reference/objects/organization.md), and a set of useful helper methods for signing in and signing up.

- [useUser()](https://clerk.com/docs/reference/hooks/use-user.md)
- [useClerk()](https://clerk.com/docs/reference/hooks/use-clerk.md)
- [useAuth()](https://clerk.com/docs/reference/hooks/use-auth.md)
- [useSignIn()](https://clerk.com/docs/reference/hooks/use-sign-in.md)
- [useSignUp()](https://clerk.com/docs/reference/hooks/use-sign-up.md)
- [useWaitlist()](https://clerk.com/docs/reference/hooks/use-waitlist.md)
- [useSession()](https://clerk.com/docs/reference/hooks/use-session.md)
- [useSessionList()](https://clerk.com/docs/reference/hooks/use-session-list.md)
- [useOrganization()](https://clerk.com/docs/reference/hooks/use-organization.md)
- [useOrganizationList()](https://clerk.com/docs/reference/hooks/use-organization-list.md)
- [useOrganizationCreationDefaults()](https://clerk.com/docs/reference/hooks/use-organization-creation-defaults.md)
- [useReverification()](https://clerk.com/docs/reference/hooks/use-reverification.md)
- [useCheckout()](https://clerk.com/docs/reference/hooks/use-checkout.md)
- [usePaymentElement()](https://clerk.com/docs/reference/hooks/use-payment-element.md)
- [usePaymentMethods()](https://clerk.com/docs/reference/hooks/use-payment-methods.md)
- [usePlans()](https://clerk.com/docs/reference/hooks/use-plans.md)
- [useSubscription()](https://clerk.com/docs/reference/hooks/use-subscription.md)
- [usePaymentAttempts()](https://clerk.com/docs/reference/hooks/use-payment-attempts.md)
- [useStatements()](https://clerk.com/docs/reference/hooks/use-statements.md)
- [useAPIKeys()](https://clerk.com/docs/reference/hooks/use-api-keys.md)

## Server-side helpers

### App router

Clerk provides first-class support for the [Next.js App Router](https://nextjs.org/docs/app). The following references show how to integrate Clerk features into apps using the latest App Router and React Server Components features.

- [auth()](https://clerk.com/docs/reference/nextjs/app-router/auth.md)
- [currentUser()](https://clerk.com/docs/reference/nextjs/app-router/current-user.md)
- [Route Handlers](https://clerk.com/docs/reference/nextjs/app-router/route-handlers.md)
- [Server Actions](https://clerk.com/docs/reference/nextjs/app-router/server-actions.md)

### Pages router

Clerk continues to provide drop-in support for the Next.js Pages Router. In addition to the main Clerk integration, the following references are available for apps using Pages Router.

- [getAuth()](https://clerk.com/docs/reference/nextjs/pages-router/get-auth.md)
- [buildClerkProps()](https://clerk.com/docs/reference/nextjs/pages-router/build-clerk-props.md)

### `Auth` object

Both `auth()` (App Router) and `getAuth()` (Pages Router) return an `Auth` object. This JavaScript object contains important information like the current user's session ID, user ID, and Organization ID. Learn more about the [`Auth` object](https://clerk.com/docs/reference/backend/types/auth-object.md){{ target: '_blank' }}.

## Objects

Learn about the [key Clerk objects](https://clerk.com/docs/reference/objects/overview.md) that power many of Clerk's SDKs.

## Types

See the [reference docs on types](https://clerk.com/docs/reference/types/overview.md) to get more information about the different types available for typing your application.

### `clerkClient`

[`clerkClient`](https://clerk.com/docs/reference/backend/overview.md) is a wrapper around the [Backend API](https://clerk.com/docs/reference/backend-api){{ target: '_blank' }} that makes it easier to interact with the API. For example, to retrieve a list of all users in your application, you can use the `users.getUserList()` method instead of manually making a fetch request to the `https://api.clerk.com/v1/users` endpoint.

To access a resource, you must first instantiate a `clerkClient` instance. See the [reference documentation](https://clerk.com/docs/reference/backend/overview.md) for more information.

## Demo repositories

For examples of Clerk's features, such as user and Organization management, integrated into a single application, see the Next.js demo repositories:

- [Clerk + Next.js App Router Demo](https://github.com/clerk/clerk-nextjs-demo-app-router)
- [Clerk + Next.js Pages Router Demo](https://github.com/clerk/clerk-nextjs-demo-pages-router)

---

## Sitemap

[Overview of all docs pages](https://clerk.com/docs/llms.txt)
