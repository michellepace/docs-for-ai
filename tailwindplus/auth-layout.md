[Home](https://catalyst.tailwindui.com/)

[Demo](https://catalyst-demo.tailwindui.com/) [Docs](https://catalyst.tailwindui.com/docs) [Buy UI Kit →](https://tailwindcss.com/plus/templates/catalyst)

Getting startedSidebar layoutStacked layoutAuth layoutAlertAvatarBadgeButtonCheckboxComboboxDescription listDialogDividerDropdownFieldsetHeadingInputListboxNavbarPaginationRadio buttonSelectSidebarSwitchTableTextTextarea

# Auth layout

Not sure why auth pages are always centered, but we're not here to challenge the status quo.

![Login page demo](https://catalyst.tailwindui.com/login-preview.jpeg)![Login page demo](https://catalyst.tailwindui.com/login-preview-dark.jpeg)[Open in new tab](https://catalyst.tailwindui.com/demos/auth/login)

```tsx
<AuthLayout>
  {/* Your page content */}
</AuthLayout>
```

## Component API

| Prop | Default | Description |
| :-- | :-- | :-- |
| - | - | `AuthLayout` extends the JSX `<main>` element |
| `children` | - | The page content. |

## Examples

### Login page

Wrap your login form with the `AuthLayout` component to create a centered login page:

![Auth layout demo](https://catalyst.tailwindui.com/login-preview.jpeg)![Auth layout demo](https://catalyst.tailwindui.com/login-preview-dark.jpeg)[Open in new tab](https://catalyst.tailwindui.com/demos/auth/login)

```tsx
import { AuthLayout } from '@/components/auth-layout'
import { Button } from '@/components/button'
import { Checkbox, CheckboxField } from '@/components/checkbox'
import { Field, Label } from '@/components/fieldset'
import { Heading } from '@/components/heading'
import { Input } from '@/components/input'
import { Strong, Text, TextLink } from '@/components/text'
import { Logo } from './logo'

function Example() {
  return (
    <AuthLayout>
      <form action="#" method="POST" className="grid w-full max-w-sm grid-cols-1 gap-8">
        <Logo className="h-6 text-zinc-950 dark:text-white forced-colors:text-[CanvasText]" />
        <Heading>Sign in to your account</Heading>
        <Field>
          <Label>Email</Label>
          <Input type="email" name="email" />
        </Field>
        <Field>
          <Label>Password</Label>
          <Input type="password" name="password" />
        </Field>
        <div className="flex items-center justify-between">
          <CheckboxField>
            <Checkbox name="remember" />
            <Label>Remember me</Label>
          </CheckboxField>
          <Text>
            <TextLink href="#">
              <Strong>Forgot password?</Strong>
            </TextLink>
          </Text>
        </div>
        <Button type="submit" className="w-full">
          Login
        </Button>
        <Text>
          Don't have an account?{' '}
          <TextLink href="#">
            <Strong>Sign up</Strong>
          </TextLink>
        </Text>
      </form>
    </AuthLayout>
  )
}
```

### Registration page

Wrap your registration form with the `AuthLayout` component to create a centered registration page:

![Registration page demo](https://catalyst.tailwindui.com/register-preview.jpeg)![Registration page demo](https://catalyst.tailwindui.com/register-preview-dark.jpeg)[Open in new tab](https://catalyst.tailwindui.com/demos/auth/register)

```tsx
import { AuthLayout } from '@/components/auth-layout'
import { Button } from '@/components/button'
import { Checkbox, CheckboxField } from '@/components/checkbox'
import { Field, Label } from '@/components/fieldset'
import { Heading } from '@/components/heading'
import { Input } from '@/components/input'
import { Select } from '@/components/select'
import { Strong, Text, TextLink } from '@/components/text'
import { Logo } from './logo'

function Example() {
  return (
    <AuthLayout>
      <form action="#" method="POST" className="grid w-full max-w-sm grid-cols-1 gap-8">
        <Logo className="h-6 text-zinc-950 dark:text-white forced-colors:text-[CanvasText]" />
        <Heading>Create your account</Heading>
        <Field>
          <Label>Email</Label>
          <Input type="email" name="email" />
        </Field>
        <Field>
          <Label>Full name</Label>
          <Input name="name" />
        </Field>
        <Field>
          <Label>Password</Label>
          <Input type="password" name="password" autoComplete="new-password" />
        </Field>
        <Field>
          <Label>Country</Label>
          <Select name="country">
            <option>Canada</option>
            <option>Mexico</option>
            <option>United States</option>
          </Select>
        </Field>
        <CheckboxField>
          <Checkbox name="remember" />
          <Label>Get emails about product updates and news.</Label>
        </CheckboxField>
        <Button type="submit" className="w-full">
          Create account
        </Button>
        <Text>
          Already have an account?{' '}
          <TextLink href="#">
            <Strong>Sign in</Strong>
          </TextLink>
        </Text>
      </form>
    </AuthLayout>
  )
}
```

### Forgot password page

Wrap your forgot password form with the `AuthLayout` component to create a centered forgot password page:

![Registration page demo](https://catalyst.tailwindui.com/forgot-password-preview.jpeg)![Registration page demo](https://catalyst.tailwindui.com/forgot-password-preview-dark.jpeg)[Open in new tab](https://catalyst.tailwindui.com/demos/auth/forgot-password)

```tsx
import { AuthLayout } from '@/components/auth-layout'
import { Button } from '@/components/button'
import { Field, Label } from '@/components/fieldset'
import { Heading } from '@/components/heading'
import { Input } from '@/components/input'
import { Strong, Text, TextLink } from '@/components/text'
import { Logo } from './logo'

function Example() {
  return (
    <AuthLayout>
      <form action="" method="POST" className="grid w-full max-w-sm grid-cols-1 gap-8">
        <Logo className="h-6 text-zinc-950 dark:text-white forced-colors:text-[CanvasText]" />
        <Heading>Reset your password</Heading>
        <Text>Enter your email and we'll send you a link to reset your password.</Text>
        <Field>
          <Label>Email</Label>
          <Input type="email" name="email" />
        </Field>
        <Button type="submit" className="w-full">
          Reset password
        </Button>
        <Text>
          Don't have an account?{' '}
          <TextLink href="/demos/auth/register">
            <Strong>Sign up</Strong>
          </TextLink>
        </Text>
      </form>
    </AuthLayout>
  )
}
```
