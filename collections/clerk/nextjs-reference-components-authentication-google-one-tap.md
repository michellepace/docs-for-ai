# <GoogleOneTap /> component

> To use Google One Tap with Clerk, you must [enable Google as a social connection in the Clerk Dashboard](https://clerk.com/docs/guides/configure/auth-strategies/social-connections/google.md?sdk=nextjs#configure-for-your-production-instance) and make sure to use custom credentials.

The `<GoogleOneTap />` component renders the [Google One Tap](https://developers.google.com/identity/gsi/web/guides/features) UI so that users can use a single button to sign-up or sign-in to your Clerk application with their Google accounts.

By default, this component will redirect users back to the page where the authentication flow started. However, you can override this with [force redirect URL props](https://clerk.com/docs/nextjs/reference/components/authentication/google-one-tap.md#properties) or [force redirect URL environment variables](https://clerk.com/docs/guides/development/clerk-environment-variables.md?sdk=nextjs#sign-in-and-sign-up-redirects).

> `<GoogleOneTap>` does not render if the user is already signed into your Clerk application, so there's no need to manually check if a user is signed in yourself before rendering it.

## Example

The following example includes a basic implementation of the `<GoogleOneTap />` component. You can use this as a starting point for your own implementation.

filename: app/sign-in/[[...sign-in]]/page.tsx
```tsx
import { GoogleOneTap } from '@clerk/nextjs'

export default function Page() {
  return <GoogleOneTap />
}
```

## Properties

| Name                    | Type    | Description                                                                                                                                                                                                                                      |
| ----------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| cancelOnTapOutside?     | boolean | If true, the One Tap prompt closes automatically if the user clicks outside of the prompt. Defaults to true.                                                                                                                                     |
| itpSupport?             | boolean | If true, enables the ITP-specific UX when One Tap is rendered on ITP browsers such as Chrome on iOS, Safari, and FireFox. Defaults to true.                                                                                                      |
| fedCmSupport?           | boolean | If true, enables Google One Tap to use the FedCM API to sign users in. See Google's docs on best practices when disabling FedCM support. Defaults to true                                                                                        |
| signInForceRedirectUrl? | string  | Useful if you want to redirect to a path specific to Google One Tap users. If provided, this URL will always be redirected to after the user signs in, overriding any <ClerkProvider> redirect URL props or redirect URL environment variables. |
| signUpForceRedirectUrl? | string  | Useful if you want to redirect to a path specific to Google One Tap users. If provided, this URL will always be redirected to after the user signs up, overriding any <ClerkProvider> redirect URL props or redirect URL environment variables. |

## Limitations

- If your application will use the Google API on behalf of your users, the `<GoogleOneTap>` component is not recommended, as Google does not provide Clerk with an access or refresh token that you can use.
- Users with the 1Password browser extension may not be able to render the Google One Tap UI. They must disable this extension.
- When testing in development, if you select the `X` button to close the Google One Tap UI, you may encounter [a cooldown](https://developers.google.com/identity/gsi/web/guides/features#exponential_cooldown) that prevents you from rendering it again for a period of time. To bypass the cooldown, remove the `g_state` cookie.

---

## Sitemap

[Overview of all docs pages](https://clerk.com/docs/llms.txt)
