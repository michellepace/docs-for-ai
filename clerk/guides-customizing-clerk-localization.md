# Localization prop (experimental)

> This feature is currently experimental and may not behave as expected. If you encounter any issues, [contact support](https://clerk.com/contact/support){{ target: '_blank' }} with as much detail as possible.

Clerk offers the ability to override the strings for all of the elements in each of the Clerk components. This allows you to provide localization for your users or change the wording to suit your brand.

## `@clerk/localizations`

The `@clerk/localizations` package contains predefined localizations for the Clerk components.

### Languages

Clerk currently supports the following languages with English as the default:

| English name          | Language tag (BCP 47) | Key    |
| --------------------- | --------------------- | ------ |
| Arabic (Saudi)        | ar-SA                 | `arSA` |
| Belarus               | be-BY                 | `beBY` |
| Bengali               | bn-IN                 | `bnIN` |
| Bulgarian             | bg-BG                 | `bgBG` |
| Catalan               | ca-ES                 | `caES` |
| Chinese (Simplified)  | zh-CN                 | `zhCN` |
| Chinese (Traditional) | zh-TW                 | `zhTW` |
| Croatian              | hr-HR                 | `hrHR` |
| Czech                 | cs-CZ                 | `csCZ` |
| Danish                | da-DK                 | `daDK` |
| Dutch                 | nl-BE                 | `nlBE` |
| Dutch                 | nl-NL                 | `nlNL` |
| English (GB)          | en-GB                 | `enGB` |
| English (US)          | en-US                 | `enUS` |
| Farsi                 | fa-IR                 | `faIR` |
| Finnish               | fi-FI                 | `fiFI` |
| French                | fr-FR                 | `frFR` |
| German                | de-DE                 | `deDE` |
| Greek                 | el-GR                 | `elGR` |
| Hebrew                | he-IL                 | `heIL` |
| Hindi                 | hi-IN                 | `hiIN` |
| Hungarian             | hu-HU                 | `huHU` |
| Icelandic             | is-IS                 | `isIS` |
| Italian               | it-IT                 | `itIT` |
| Indonesian            | id-ID                 | `idID` |
| Japanese              | ja-JP                 | `jaJP` |
| Kazakh                | kk-KZ                 | `kkKZ` |
| Korean                | ko-KR                 | `koKR` |
| Malay                 | ms-MY                 | `msMY` |
| Mongolian             | mn-MN                 | `mnMN` |
| Norwegian             | nb-NO                 | `nbNO` |
| Polish                | pl-PL                 | `plPL` |
| Portuguese (BR)       | pt-BR                 | `ptBR` |
| Portuguese (PT)       | pt-PT                 | `ptPT` |
| Romanian              | ro-RO                 | `roRO` |
| Russian               | ru-RU                 | `ruRU` |
| Serbian               | sr-RS                 | `srRS` |
| Slovak                | sk-SK                 | `skSK` |
| Spanish               | es-ES                 | `esES` |
| Spanish (Costa Rica)  | es-CR                 | `esCR` |
| Spanish (Mexico)      | es-MX                 | `esMX` |
| Spanish (Uruguay)     | es-UY                 | `esUY` |
| Swedish               | sv-SE                 | `svSE` |
| Tamil                 | ta-IN                 | `taIN` |
| Telugu                | te-IN                 | `teIN` |
| Thai                  | th-TH                 | `thTH` |
| Turkish               | tr-TR                 | `trTR` |
| Ukrainian             | uk-UA                 | `ukUA` |
| Vietnamese            | vi-VN                 | `viVN` |

### Usage

> The localizations will only update the text in the [Clerk components](https://clerk.com/docs/reference/components/overview.md) used in your application. The hosted [Clerk Account Portal](https://clerk.com/docs/guides/account-portal/overview.md) will remain in English.

To get started, install the `@clerk/localizations` package.

```npm
npm install @clerk/localizations
```

Once the `@clerk/localizations` package is installed, you can import the localizations you need by removing the "-" from the locale. You can then pass the localization to the `localization` prop.

To apply a localization, pass the `appearance` prop to the [<ClerkProvider>](https://clerk.com/docs/reference/components/clerk-provider.md) component. The `appearance` prop accepts the property `localization`, which can be set to the imported localization.

In the following example, the fr-FR locale is imported as `frFR` and applied to all Clerk components.

```tsx
// fr-FR locale is imported as frFR
import { frFR } from '@clerk/localizations'

<ClerkProvider localization={frFR}>
  {/* ... */}
</ClerkProvider>
```

## Adding or updating a localization

Clerk's localizations are customer-sourced and we encourage customers to add or update localizations. To do so, follow these steps:

1. Fork the https://github.com/clerk/javascript/ repo.
2. Clone it locally to edit it.
3. Review Clerk's [Contributing](https://github.com/clerk/javascript/blob/main/docs/CONTRIBUTING.md) guide.
4. If you are updating an existing localization locate the file in `packages/localizations/src`
5. If you are adding a new language, copy the `en-US.ts` file and name it according to your language. The naming is the abbreviated language-region. For example, for French in Canada, it would be `fr-CA.ts.`
6. Go through the file and edit the entries.
7. If you are adding a new localization, add the language to the `packages/localizations/src/index.ts` file.
8. Commit your changes to git and push them to your fork. Create a [Pull Request](https://github.com/clerk/clerk-docs/pulls) from your fork to Clerk's repo against the `main` branch. We will review and either approve or ask for updates.

## Custom localizations

You can also provide your own localizations for the Clerk components. This is useful if you want to provide limited or quick localization for a language Clerk doesn't currently support, adjust the wording to match your brand, or customize default error messages.

First, you need to find the key for the element that you want to customize. To find the key for your translation, open up Clerk's [English localization file](https://github.com/clerk/javascript/blob/main/packages/localizations/src/en-US.ts). Search the file for the term that you want to customize.

For example, say you want to change the text of the "Continue" button on the `<SignIn />` component to say "LETS GO!". In this case, you'd search for "Continue". The first result that comes up is `formButtonPrimary`, which is the key for the "Continue" button.

Now that you know the key, you can pass it to the `localization` prop and set the value to the text you want to display. In this case, you'd set the value to "LETS GO!", as shown in the following example.

```tsx
// Set your customizations in a `localization` object
const localization = {
  formButtonPrimary: 'LETS GO!',
}

<ClerkProvider localization={localization}>
  {/* ... */}
</ClerkProvider>
```

You can also customize multiple entries by passing multiple keys. The following example updates the "to continue to" subtitles on the `<SignUp />` component to say "to access" instead.

```tsx
const localization = {
  signUp: {
    start: {
      subtitle: 'to access {{applicationName}}',
    },
    emailCode: {
      subtitle: 'to access {{applicationName}}',
    },
  },
}

<ClerkProvider localization={localization}>
  {/* ... */}
</ClerkProvider>
```

### Customize error messages

You can customize Clerk's default error messages by targeting the `unstable__errors` key. This key lets you define specific error keys for different error types and assign them custom message strings. You can find the full list of error keys in the [English localization file](https://github.com/clerk/javascript/blob/main/packages/localizations/src/en-US.ts). Search for the `unstable__errors` object to find the keys you can customize.

The following example updates the `not_allowed_access` error message. This message appears when a user tries to sign in with an email domain that isn't allowed to access your application.

```tsx
const localization = {
  unstable__errors: {
  not_allowed_access:
    'Send us an email if you want your corporate email domain allowlisted for access',
  },
}

<ClerkProvider localization={localization}>
  {/* ... */}
</ClerkProvider>
```

---

## Sitemap

[Overview of all docs pages](https://clerk.com/docs/llms.txt)
