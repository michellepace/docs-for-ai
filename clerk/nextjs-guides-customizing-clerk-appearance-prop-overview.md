# Appearance prop

Customizing the appearance of Clerk components is a powerful way to make your application look and feel unique. Clerk provides a way to customize the appearance of its components using the `appearance` prop.

The `appearance` prop can be used to share styles across every component, or applied individually to any of the Clerk components. When using it for global styling, the prop is available wherever you initialize the Clerk integration. For most SDKs, this means applying it to the [<ClerkProvider>](https://clerk.com/docs/nextjs/reference/components/clerk-provider.md) component, while in others, it's configured through the SDK's Clerk integration or plugin.

This applies to all of the React-based packages, like [Next.js](https://clerk.com/docs/nextjs/getting-started/quickstart.md), as well as [the pure JavaScript ClerkJS package](https://clerk.com/docs/reference/javascript/overview.md).

## Properties

The `appearance` prop accepts the following properties:

| Name          | Type                      | Description                                                                                                                                                                                                                                                                                        |
| ------------- | ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| theme?        | BaseTheme | BaseTheme[] | A theme used as the base theme for the components. For more information, see Themes.                                                                                                                                                                                                               |
| options?      | Options                   | Configuration options that affect the layout of the components, allowing customizations that are hard to implement with just CSS. For more information, see Options.                                                                                                                               |
| variables?    | Variables                 | General theme overrides. This styles will be merged with our base theme. Can override global styles like colors, fonts, etc. For more information, see Variables.                                                                                                                                  |
| elements?     | Elements                  | Fine-grained theme overrides. Useful when you want to style specific elements or elements that are under a specific state. For more information, see the Customize elements of a Clerk component section.                                                                                          |
| captcha?      | Captcha                   | Configuration options that affect the appearance of the CAPTCHA widget. For more information, see the dedicated guide.                                                                                                                                                                             |
| cssLayerName? | string                    | The name of the CSS layer for Clerk component styles. This is useful for advanced CSS customization, allowing you to control the cascade and prevent style conflicts by isolating Clerk's styles within a specific layer. For more information on CSS layers, see the MDN documentation on @layer. |

## Using a prebuilt theme

Clerk offers a set of prebuilt themes that can be used to quickly style Clerk components. See the [Themes](https://clerk.com/docs/nextjs/guides/customizing-clerk/appearance-prop/themes.md) docs for more information.

## Customize the layout

The `options` property is used to adjust the layout of the [<SignIn/>](https://clerk.com/docs/nextjs/reference/components/authentication/sign-in.md) and [<SignUp/>](https://clerk.com/docs/nextjs/reference/components/authentication/sign-up.md) components, as well as set important links to your support, terms, and privacy pages. See the [Options](https://clerk.com/docs/nextjs/guides/customizing-clerk/appearance-prop/options.md) docs for more information.

## Customize the base theme

The `variables` property is used to adjust the general styles of a component's base theme, like colors, backgrounds, and typography. See the [Variables](https://clerk.com/docs/nextjs/guides/customizing-clerk/appearance-prop/variables.md) docs for more information.

## Customize elements of a Clerk component

The `elements` property lets you apply custom styles to the underlying DOM elements of Clerk's prebuilt components. See the [Bring your own CSS](https://clerk.com/docs/nextjs/guides/customizing-clerk/appearance-prop/bring-your-own-css.md) docs for more information.

## Next steps

Here are a few resources you can utilize to customize your Clerk components further:

- [Localization](https://clerk.com/docs/guides/customizing-clerk/localization.md?sdk=nextjs): Learn how to localize your Clerk components.
- [Customize layouts](https://clerk.com/docs/guides/customizing-clerk/appearance-prop/options.md?sdk=nextjs): Learn how to change the layout and links of your&#x20;

---

## Sitemap

[Overview of all docs pages](https://clerk.com/docs/llms.txt)
