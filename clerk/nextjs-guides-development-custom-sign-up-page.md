# Build your own sign-up page for your Next.js app with Clerk

By default, the [<SignIn />](https://clerk.com/docs/nextjs/reference/components/authentication/sign-in.md) component handles signing in and signing up, but if you'd like to have a dedicated sign-up page, this guide shows you how to use the [<SignUp />](https://clerk.com/docs/nextjs/reference/components/authentication/sign-up.md) component to build a custom sign-up page.

To set up a single sign-in-or-up page, follow the [custom sign-in-or-up page guide](https://clerk.com/docs/nextjs/guides/development/custom-sign-in-or-up-page.md).

> If prebuilt components don't meet your specific needs or if you require more control over the logic, you can rebuild the existing Clerk flows using the Clerk API. For more information, see the [custom flow guides](https://clerk.com/docs/guides/development/custom-flows/overview.md?sdk=nextjs).

1. ## Build a sign-up page

   The following example demonstrates how to render the [<SignUp />](https://clerk.com/docs/nextjs/reference/components/authentication/sign-up.md) component on a dedicated sign-up page using the [Next.js optional catch-all route](https://nextjs.org/docs/pages/building-your-application/routing/dynamic-routes#catch-all-segments).

   filename: app/sign-up/[[...sign-up]]/page.tsx

   ```tsx
   import { SignUp } from '@clerk/nextjs'

   export default function Page() {
     return <SignUp />
   }
   ```
2. ## Make the sign-up route public

   By default, `clerkMiddleware()` makes all routes public. **This step is specifically for applications that have configured `clerkMiddleware()` to make [all routes protected](https://clerk.com/docs/nextjs/reference/nextjs/clerk-middleware.md#protect-all-routes).** If you have not configured `clerkMiddleware()` to protect all routes, you can skip this step.

   > If you're using Next.js ≤15, name your file `middleware.ts` instead of `proxy.ts`. The code itself remains the same; only the filename changes.

   To make the sign-up route public:

   - Navigate to your `proxy.ts` file.
   - Add the sign-up route to your existing route matcher that is making routes public.

   filename: proxy.ts

   ```tsx
   import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server'

   // prettier-ignore
   const isPublicRoute = createRouteMatcher([
     '/sign-in(.*)',
     '/sign-up(.*)'
   ])

   export default clerkMiddleware(async (auth, req) => {
     if (!isPublicRoute(req)) {
       await auth.protect()
     }
   })

   export const config = {
     matcher: [
       // Skip Next.js internals and all static files, unless found in search params
       '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
       // Always run for API routes
       '/(api|trpc)(.*)',
       // Always run for Clerk-specific frontend API routes
       '/__clerk/(.*)',
     ],
   }
   ```
3. ## Update your environment variables

   - Set the `CLERK_SIGN_UP_URL` environment variable to tell Clerk where the `<SignUp />` component is being hosted.
   - Set `CLERK_SIGN_UP_FALLBACK_REDIRECT_URL` as a fallback URL incase users visit the `/sign-up` route directly.
   - Set `CLERK_SIGN_IN_FALLBACK_REDIRECT_URL` as a fallback URL incase users select the 'Already have an account? Sign in' link at the bottom of the component.

   Learn more about these environment variables and how to customize Clerk's redirect behavior in the [dedicated guide](https://clerk.com/docs/guides/development/customize-redirect-urls.md?sdk=nextjs).

   filename: .env

   ```env
   NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
   NEXT_PUBLIC_CLERK_SIGN_UP_FALLBACK_REDIRECT_URL=/
   NEXT_PUBLIC_CLERK_SIGN_IN_FALLBACK_REDIRECT_URL=/
   ```
4. ## Visit your new page

   Run your project with the following command:

   ```npm
   npm run dev
   ```

   Visit your new custom page locally at [localhost:3000/sign-up](http://localhost:3000/sign-up).

## Next steps

Learn more about Clerk components, how to customize them, and how to use Clerk's client-side helpers using the following guides.

- [Protect content and read user data](https://clerk.com/docs/nextjs/guides/users/reading.md): Learn how to use Clerk's hooks and helpers to protect content and read user data in your Next.js app.
- [Client-side helpers](https://clerk.com/docs/reference/nextjs/overview.md?sdk=nextjs#client-side-helpers): Learn more about Clerk's client-side helpers and how to use them.
- [Prebuilt components](https://clerk.com/docs/reference/components/overview.md?sdk=nextjs): Learn how to quickly add authentication to your app using Clerk's suite of components.
- [Customization & localization](https://clerk.com/docs/guides/customizing-clerk/appearance-prop/overview.md?sdk=nextjs): Learn how to customize and localize Clerk components.

---

## Sitemap

[Overview of all docs pages](https://clerk.com/docs/llms.txt)
