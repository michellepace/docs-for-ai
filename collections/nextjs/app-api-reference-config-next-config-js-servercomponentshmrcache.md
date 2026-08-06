---
title: serverComponentsHmrCache
description: Configure whether fetch responses in Server Components are cached across HMR refresh requests.
url: "https://nextjs.org/docs/app/api-reference/config/next-config-js/serverComponentsHmrCache"
docs_index: /docs/llms.txt
version: 16.3.0
lastUpdated: 2025-06-16
prerequisites:
  - "Configuration: /docs/app/api-reference/config"
  - "next.config.js: /docs/app/api-reference/config/next-config-js"
---


> For an index of all Next.js documentation, see [/docs/llms.txt](/docs/llms.txt).

> This feature is currently experimental and subject to change, it's not recommended for production. Try it out and share your feedback on [GitHub](https://github.com/vercel/next.js/issues).

The experimental `serverComponentsHmrCache` option allows you to cache `fetch` responses in Server Components across Hot Module Replacement (HMR) refreshes in local development. This results in faster responses and reduced costs for billed API calls.

By default, the HMR cache applies to all `fetch` requests, including those with the `cache: 'no-store'` option. This means uncached requests will not show fresh data between HMR refreshes. However, the cache will be cleared on navigation or full-page reloads.

You can disable the HMR cache by setting `serverComponentsHmrCache` to `false` in your `next.config.js` file:

```ts filename="next.config.ts" switcher
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  experimental: {
    serverComponentsHmrCache: false, // defaults to true
  },
}

export default nextConfig
```

```js filename="next.config.js" switcher
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    serverComponentsHmrCache: false, // defaults to true
  },
}

module.exports = nextConfig
```

> **Good to know:** For better observability, we recommend using the [`logging.fetches`](/docs/app/api-reference/config/next-config-js/logging) option which logs fetch cache hits and misses in the console during development.
---

For a semantic overview of all documentation, see [/docs/sitemap.md](/docs/sitemap.md)

For an index of all available documentation, see [/docs/llms.txt](/docs/llms.txt)