# Testing

Testing is an important part of every application. Each framework may require a slightly different setup. If you're having trouble getting testing to work properly, [contact support](https://clerk.com/contact/support){{ target: '_blank' }}.

## Test with one time passcodes

To avoid sending an email or SMS message with a one-time password (OTP) during testing, you can use a fake email address or phone number that has a fixed code. Read the complete documentation [here](https://clerk.com/docs/guides/development/testing/test-emails-and-phones.md).

## Get a valid session token

When writing tests using Clerk, if you need to get a valid session token, use the following flow:

1. If you have not already, [create a new user](https://clerk.com/docs/reference/backend-api/tag/users/post/users){{ target: '_blank' }}.
2. [Create a new session](https://clerk.com/docs/reference/backend-api/tag/sessions/post/sessions){{ target: '_blank' }} for the user.
3. [Create a session token](https://clerk.com/docs/reference/backend-api/tag/sessions/post/sessions/%7Bsession_id%7D/tokens){{ target: '_blank' }} using the session ID returned in the previous step.
4. Pass the returned session token as the value of an Authorization header to any other requests you're making, as such: `Authorization: Bearer <session_token>`.

Note that Clerk's session tokens are short-lived and are valid only for 60 seconds. Read more [here](https://clerk.com/docs/guides/how-clerk-works/overview.md).

If the session token expires, you will need to refresh it with the same [create session token endpoint](https://clerk.com/docs/reference/backend-api/tag/sessions/post/sessions/%7Bsession_id%7D/tokens){{ target: '_blank' }}. The most common ways to do this are to either hit this endpoint before every test to ensure you have a valid session token, or to run an interval timer that refreshes the token before it expires.

For more information, feedback or issues, visit the [`@clerk/testing`](https://github.com/clerk/javascript/tree/main/packages/testing) package.

## Agent Tasks

Agent Tasks allow you to create authenticated sessions on behalf of users without going through the standard sign-in flow. This is useful for automated end-to-end testing and AI agent workflows. Read the complete [Agent Tasks guide](https://clerk.com/docs/guides/development/testing/agent-tasks.md).

## Testing Tokens

Testing Tokens allow you to bypass bot detection mechanisms that protect Clerk applications from malicious bots, ensuring your test suites run smoothly. Without Testing Tokens, you may encounter "Bot traffic detected" errors in your requests.

> While you can manually implement the following logic in your test suite, Clerk provides [Playwright](https://clerk.com/docs/guides/development/testing/playwright/overview.md) and [Cypress](https://clerk.com/docs/guides/development/testing/cypress/overview.md) integrations that handle this automatically.

Obtained via the [Backend API](https://clerk.com/docs/reference/backend-api/tag/Testing-Tokens){{ target: '_blank' }}, Testing Tokens are short-lived and valid only for the specific instance for which they are issued.

Once retrieved, include the token value in the `__clerk_testing_token` query parameter in your Frontend API requests. For example, a sign-up request using a Testing Token would look like this:

```shell
POST https://happy-hippo-1.clerk.accounts.dev/v1/client/sign_ups?__clerk_testing_token=1713877200-c_2J2MvPu9PnXcuhbPZNao0LOXqK9A7YrnBn0HmIWxy
```

### Testing Tokens production limitations

Testing Tokens work in both development and production environments, but there are limitations to be aware of when trying to use Testing Tokens in production.

The testing helpers do not currently support **code-based** authentication methods in production environments. Authenticating a user must be done via email and password or by signing in via email address directly.

---

## Sitemap

[Overview of all docs pages](https://clerk.com/docs/llms.txt)
