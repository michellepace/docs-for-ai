# Heading

You get two — we're building applications here, not authoring medical journals.

```tsx
import { Heading } from '@/components/heading'

function Example() {
  return (
    <div className="flex w-full flex-wrap items-end justify-between gap-4 border-b border-zinc-950/10 pb-6 dark:border-white/10">
      <Heading>Order #1011</Heading>
      <div className="flex gap-4">
        <Button outline>Refund</Button>
        <Button>Resend invoice</Button>
      </div>
    </div>
  )
}
```

## Component API

The `Heading` component extends the JSX `<h1>` element and does not expose any component-specific props.

The `Subheading` component extends the JSX `<h2>` element and does not expose any component-specific props.

## Examples

### Basic heading example

Use the `Heading` component to add a primary heading to a page:

```tsx
import { Heading } from '@/components/heading'

function Example() {
  return <Heading>Recent orders</Heading>
}
```

The `Heading` component renders an `h1` by default, which you can customise with the `level` prop.

### Basic subheading example

Use the `Subheading` component to add a subheading to a page:

```tsx
import { Subheading } from '@/components/heading'

function Example() {
  return <Subheading>Recent orders</Subheading>
}
```

The `Subheading` component renders an `h2` by default, which you can customise with the `level` prop.

### With custom level

Use the `level` prop to render a different heading element for semantic purposes whilst still maintaining the same visual styles:

```tsx
import { Heading } from '@/components/heading'

function Example() {
  return <Heading level={2}>Recent orders</Heading>
}
```
