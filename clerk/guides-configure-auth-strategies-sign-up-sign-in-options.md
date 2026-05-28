# Sign-up and sign-in options

Clerk provides multiple options for configuring a sign-up and sign-in flow for your application. This guide will walk you through each option.

You can modify your authentication options after your application has been created by navigating to the [Clerk Dashboard](https://dashboard.clerk.com/) and selecting any of the options under **User & authentication** in the left sidenav.

## User & authentication

To configure the options available to users for authentication, navigate to the [**User & authentication**](https://dashboard.clerk.com/~/user-authentication/user-and-authentication) page in the Clerk Dashboard.

The easiest way to allow your users to create and manage their authentication options is to use the prebuilt [<UserProfile>](https://clerk.com/docs/reference/components/user/user-profile.md) component. If you're building a custom user interface using the Clerk API, refer to the [custom flow guides](https://clerk.com/docs/guides/development/custom-flows/overview.md).

### Email

Users can authenticate with their email address using the following options:

- **Email verification code**: Users receive an OTP to their email address to sign in.
- **Email verification link**: Users receive an email with a link to sign in. As a security measure, email links expire after 10 minutes to prevent the use of compromised or stale links.
  - **Require the same device and browser**: Email links are required to be verified from the same device and browser on which the sign-up or sign-in was initiated. For example:
    - A user tries to sign in from their desktop browser.
    - They open the email link on their mobile phone to verify their email address.
    - The user's sign-in on the desktop browser **gets an error**, because the link was verified on a different device and browser.

### Phone

> This feature requires a [paid plan](https://clerk.com/pricing){{ target: '_blank' }} for production use, but all features are free to use in development mode so that you can try out what works for you. See the [pricing](https://clerk.com/pricing){{ target: '_blank' }} page for more information.

Users can authenticate with their phone number and verify it with an OTP.

SMS functionality is restricted to phone numbers from countries enabled on your [SMS allowlist](#sms-allowlist).

### SMS allowlist

SMS functionality, including SMS OTPs, is restricted to phone numbers from countries that are enabled on your SMS allowlist. This can be useful for avoiding extraneous SMS fees from countries from which your app is not expected to attract traffic. **By default, only the US and Canada are enabled.**

Every instance starts off with a default set of enabled SMS country tiers. To tailor it to your needs:

1. In the Clerk Dashboard, navigate to the [**SMS**](https://dashboard.clerk.com/~/customization/sms) page.
2. Select the **Settings** tab.
3. Enable or disable countries as needed.

If a country is disabled, then phone numbers starting with the corresponding country calling code:

- Cannot receive OTPs and a request to receive an OTP will be rejected with an error
- Cannot receive notifications for password or passkey modifications
- Cannot be used upon sign-up
- Cannot be added to an existing user profile

### Username

In this section, you can allow users to set their username. Usernames must be between 4 and 64 characters long and do not allow special characters (^$!.`#+~`), but this can be customized.

> Usernames only support Latin-based characters. This restriction helps protect against Unicode spoofing and homograph attacks, where characters from non-Latin scripts can be used to impersonate users.

### Password

When **Password** is enabled, users provide a password to sign in.

Disabling **Password** will only affect new users. Existing users will still be able to sign in with their existing password.

### Passkeys

> This feature requires a [paid plan](https://clerk.com/pricing){{ target: '_blank' }} for production use, but all features are free to use in development mode so that you can try out what works for you. See the [pricing](https://clerk.com/pricing){{ target: '_blank' }} page for more information.

A passkey is a type of sign-in credential that requires one user action, but uses two authentication factors:

1. A pin number or biometric data
2. A physical device

**Users can only create passkeys after signing up**, so you'll need to enable another authentication strategy for the sign-up process. After signing in, users can create a passkey.

> When setting up passkeys with Android or Expo, there are a few additional steps to follow:
>
> - [Set up passkeys for Android](https://clerk.com/docs/reference/android/passkeys.md).
> - [Set up passkeys for Expo](https://clerk.com/docs/reference/expo/passkeys.md).

#### Passkey limitations

- Passkeys are not currently available as an [MFA](#multi-factor-authentication) option.
- Not all devices and browsers are compatible with passkeys. Passkeys are built on WebAuthn technology and you should check [the Browser Compatibility docs](https://developer.mozilla.org/en-US/docs/Web/API/Web_Authentication_API#browser_compatibility) for an up-to-date list.
- Your users can have a max of 10 passkeys per account.

#### Domain restrictions for passkeys

Passkeys are tied to the domain they are created on and **cannot be used across different domains**. However, passkeys **do work on subdomains** if they are registered on the root domain. For example:

- Passkeys created on `your-domain.com` **cannot be used** on `your-domain-admin.com` (different domains).
- Passkeys created on `your-domain.com` **can be used** on `accounts.your-domain.com` (subdomain of the same root domain).
- Passkeys created on `staging1.your-domain.com` **cannot be used** on `staging2.your-domain.com` (sibling subdomains) unless the passkey was scoped to `your-domain.com` (i.e. the shared root domain).

**If you're using [satellite domains](https://clerk.com/docs/guides/dashboard/dns-domains/satellite-domains.md)**, in both development and production, passkeys won't be portable between your primary domain and your satellite domains so you should avoid using them.

If you're **not** using satellite domains:

- **In development**, you can either:
  - **The recommended approach**. Use Clerk's [components](https://clerk.com/docs/reference/components/overview.md), [Elements](https://clerk.com/docs/guides/customizing-clerk/elements/overview.md), or custom flows, instead of the [Account Portal](https://clerk.com/docs/guides/account-portal/overview.md). This ensures the passkey is created and used entirely on your development domain, so passkeys created on `localhost` will only work on `localhost`.
  - Create a passkey directly through the Account Portal instead of your local application to keep it tied to the Account Portal's domain. Passkeys created on your Account Portal (e.g., `your-app.accounts.dev`) will only work on that domain, which can cause issues if you switch between `localhost` and the Account Portal during development. If you choose this approach, ensure all testing happens on the same domain where the passkey was created.

- **In production,** your Account Portal is usually hosted on a subdomain of your main domain (e.g. `accounts.your-domain.com`), enabling passkeys to work seamlessly across your app. However, as stated above, if you use **satellite domains**, passkeys will not work as intended.

### User model

In this section, you can:

- Allow users to set their first and last name.
- Allow users to delete their accounts.

## Restrict changes

By default, users can add, remove, and modify their own email addresses, phone numbers, and usernames after sign-up. If you need tighter control over these identifiers, you can prevent users from changing them.

To restrict identifier changes:

1. In the Clerk Dashboard, navigate to the [**User & authentication**](https://dashboard.clerk.com/~/user-authentication/user-and-authentication) page.
2. Under the identifier you want to lock down (email address, phone number, or username), enable the **Restrict changes** setting.

When enabled:

- Users can still view their identifiers in [<UserProfile />](https://clerk.com/docs/reference/components/user/user-profile.md) but cannot add, remove, or modify them.
- For email addresses, the restriction also prevents connecting an OAuth account that would add a new email address.
- Admins retain full control and can still modify user identifiers through the [Dashboard](https://dashboard.clerk.com/~/users) or the [Backend API](https://clerk.com/docs/reference/backend-api).

> This feature prevents changes _after_ sign-up. If you want to control _who can sign up_ in the first place, see [restrictions](https://clerk.com/docs/guides/secure/restricting-access.md) for allowlists, blocklists, and disposable email blocking.

## SSO connections

SSO connections are a way to allow users to authenticate with their existing accounts from other services. For example, if a user already has an account with Google, they can sign in with their Google account instead of creating a new account with your application.

Clerk offers two different types of SSO connections:

- For all users, which are also known as OAuth connections, or social connections. Read more about [OAuth connections](https://clerk.com/docs/guides/configure/auth-strategies/social-connections/overview.md).
- For specific domains and Organizations, which are also known as Enterprise SSO connections. Read more about [Enterprise SSO connections](https://clerk.com/docs/guides/configure/auth-strategies/enterprise-connections/overview.md).

To enable SSO connections, navigate to the [**SSO connections**](https://dashboard.clerk.com/~/user-authentication/sso-connections) page in the Clerk Dashboard.

## Web3 authentication

Clerk provides Web3 authentication with either [Base](https://clerk.com/docs/guides/configure/auth-strategies/web3/base.md), [MetaMask](https://clerk.com/docs/guides/configure/auth-strategies/web3/metamask.md), [Coinbase Wallet](https://clerk.com/docs/guides/configure/auth-strategies/web3/coinbase-wallet.md), or [OKX Wallet](https://clerk.com/docs/guides/configure/auth-strategies/web3/okx-wallet.md). As part of validating the accuracy of the returned Web3 account address, Clerk handles the signing of a message and verifying the signature. Because sign-in with Web3 uses the same abstraction as our other authentication factors, like passwords or email links, other Clerk features like multi-factor authentication and profile enrichment work for Web3 users out-of-the-box.

To enable Web3 authentication, navigate to the [**Web3**](https://dashboard.clerk.com/~/user-authentication/web3) page in the Clerk Dashboard.

## Multi-factor authentication

Clerk supports multi-factor authentication (MFA), also known as two-factor authentication (2FA). If a user enables MFA for their account, they are required to complete a second verification step during sign-in. This enhances security by enforcing two different types of verification. Many websites offer this as an optional step, giving users control over their own security.

The following MFA strategies are currently available:

- **SMS verification code**
- **Authenticator application (also known as TOTP - Time-based One-time Password)**
- **Backup codes**

To configure MFA strategies:

1. In the Clerk Dashboard, navigate to the [**Multi-factor**](https://dashboard.clerk.com/~/user-authentication/multi-factor) page.
2. Toggle on the MFA strategies you would like to enable.
3. If you would like to force MFA for all users in your app, toggle on **Require multi-factor authentication**. When enabled, after authenticating, users will have a pending `setup-mfa` session task and will need to fulfill the task before they are considered `active` (signed-in).
   If you leave this setting disabled, users can choose to enable MFA for their own accounts through their account settings.
4. Select **Save**.

If you're building a custom user interface instead of using the [Account Portal](https://clerk.com/docs/guides/account-portal/overview.md) or [prebuilt components](https://clerk.com/docs/reference/components/overview.md), you can use [the Clerk API](https://clerk.com/docs/guides/development/custom-flows/authentication/multi-factor-authentication.md) to build a custom flow that allows users to sign in with MFA.

### Reset a user's MFA

You can reset a user's MFA by deleting their MFA enrollments. This will remove all of their MFA methods and they will have to enroll in MFA again.

To reset a user's MFA:

1. At the top of the [Clerk Dashboard](https://dashboard.clerk.com/), select **Users**.
2. Select the user from the list.
3. Select the **Reset MFA enrollments** button.

## Restrictions

Clerk provides a set of restriction options designed to provide you with enhanced control over who can gain access to your application. Restrictions can limit sign-ups or prevent accounts with specific identifiers, such as email addresses, phone numbers, and even entire domains, from accessing your application. Learn more about [restrictions](https://clerk.com/docs/guides/secure/restricting-access.md).

---

## Sitemap

[Overview of all docs pages](https://clerk.com/docs/llms.txt)
