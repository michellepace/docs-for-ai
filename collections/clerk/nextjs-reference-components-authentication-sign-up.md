# <SignUp /> component

The `<SignUp />` component renders a UI for signing up users. The functionality of the `<SignUp />` component is controlled by the instance settings you specify in the [Clerk Dashboard](https://dashboard.clerk.com), such as [sign-in and sign-up options](https://clerk.com/docs/guides/configure/auth-strategies/sign-up-sign-in-options.md?sdk=nextjs) and [social connections](https://clerk.com/docs/nextjs/guides/configure/auth-strategies/social-connections/overview.md). You can further customize your `<SignUp />` component by passing additional [properties](https://clerk.com/docs/nextjs/reference/components/authentication/sign-up.md#properties) at the time of rendering. The `<SignUp />` component also displays any session tasks that are required for the user to complete after signing up.

> The `<SignUp/>` and `<SignIn/>` components cannot render when a user is already signed in, unless the application allows multiple sessions. If a user is already signed in and the application only allows a single session, Clerk will redirect the user to the Home URL instead.

## Example

The following example includes a basic implementation of the `<SignUp />` component. You can use this as a starting point for your own implementation.

If you would like to create a dedicated `/sign-up` page in your Next.js application, see the [dedicated guide](https://clerk.com/docs/nextjs/guides/development/custom-sign-up-page.md) for more information.

filename: app/sign-up/[[...sign-up]]/page.tsx
```tsx
import { SignUp } from '@clerk/nextjs'

export default function SignUpPage() {
  return <SignUp />
}
```

## Properties

All props are optional.

| Name                                                            | Type                          | Description                                                                                                                                                                                                                                                                                                                                                                         |
| --------------------------------------------------------------- | ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| appearance?                                                     | Appearance | undefined       | An object to style your components. Will only affect Clerk components and not Account Portal pages.                                                                                                                                                                                                                                                                                 |
| fallback?                                                       | ReactNode                     | An element to be rendered while the component is mounting.                                                                                                                                                                                                                                                                                                                          |
| fallbackRedirectUrl?                                            | string                        | The fallback URL to redirect to after the user signs up, if there's no redirect\_url in the path already. Defaults to /. It's recommended to use the environment variable instead.                                                                                                                                                                                                  |
| forceRedirectUrl?                                               | string                        | If provided, this URL will always be used as the redirect destination after the user signs up. It's recommended to use the environment variable instead.                                                                                                                                                                                                                            |
| initialValues?                                                  | SignUpInitialValues           | The values used to prefill the sign-up fields with.                                                                                                                                                                                                                                                                                                                                 |
| "redirect": Redirect to the OAuth provider on the current page. | "popup": Open a popup window. | Defaults to "auto".                                                                                                                                                                                                                                                                                                                                                                 |
| path?                                                           | string                        | The path where the component is mounted on when routing is set to path. It is ignored in hash-based routing. For example: /sign-up.                                                                                                                                                                                                                                                 |
| routing?                                                        | 'hash' | 'path'              | The routing strategy for your pages. Defaults to 'path' for frameworks that handle routing, such as Next.js. Defaults to hash for all other SDK's, such as React.                                                                                                                                                                                                                   |
| signInFallbackRedirectUrl?                                      | string                        | The fallback URL to redirect to after the user signs in, if there's no redirect\_url in the path already. Used for the 'Already have an account? Sign in' link that's rendered. Defaults to /. It's recommended to use the environment variable instead.                                                                                                                            |
| signInForceRedirectUrl?                                         | string                        | If provided, this URL will always be redirected to after the user signs in. Used for the 'Already have an account? Sign in' link that's rendered. It's recommended to use the environment variable instead.                                                                                                                                                                         |
| signInUrl?                                                      | string                        | The full URL or path to the sign-in page. Used for the 'Already have an account? Sign in' link that's rendered. It's recommended to use the environment variable instead.                                                                                                                                                                                                           |
| unsafeMetadata?                                                 | SignUpUnsafeMetadata          | Metadata that can be read and set from the frontend and the backend. Once the sign-up is complete, the value of this field will be automatically copied to the created user's unsafe metadata (User.unsafeMetadata). One common use case is to collect custom information about the user during the sign-up process and store it in this property. Read more about unsafe metadata. |

## Customization

To learn about how to customize Clerk components, see the [customization documentation](https://clerk.com/docs/nextjs/guides/customizing-clerk/appearance-prop/overview.md).

If Clerk's prebuilt components don't meet your specific needs or if you require more control over the logic, you can rebuild the existing Clerk flows using the Clerk API. For more information, see the [custom flow guides](https://clerk.com/docs/guides/development/custom-flows/overview.md?sdk=nextjs).

---

## Sitemap

[Overview of all docs pages](https://clerk.com/docs/llms.txt)
