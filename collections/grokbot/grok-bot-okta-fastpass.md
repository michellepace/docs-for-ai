#### Teams and enterprises

# Set up Okta Verify and FastPass

This guide is for Okta admins whose sign-in policies require Okta FastPass.
Grok Bot computers ship with a setup script that installs Okta Verify and starts
the services FastPass needs, so Bots can sign in to Okta-protected apps in the
computer browser. For assigning the Cursor app and other Okta and Entra ID
settings, see [Configure identity and access](/grok-bot/identity-and-access).

> Okta Verify installs through
> [Team Setup Scripts](/grok-bot/teams-and-enterprises#team-setup-scripts),
> which is Enterprise only.

## Before you start

* You're an Okta admin and a Cursor team admin on the Enterprise plan.
* If your team restricts egress with
  [Network Controls](/grok-bot/security#network-policy), allowlist
  `anysphere.okta.com` and your own Okta org, for example `yourorg.okta.com`.
  Every team downloads the Okta Verify package from `anysphere.okta.com`,
  whatever org it signs in to.

## 1. Configure your Okta org

Do this in the Okta Admin Console before anyone uses FastPass on a Grok Bot
computer.

1. Enable the **Okta Verify for Linux** feature (`ftrl2df4GICAJ5xl1QSU`) under
   **Settings** > **Features**, or with
   `POST /api/v1/features/ftrl2df4GICAJ5xl1QSU/enable`.
2. Under **Security** > **Authenticators**, confirm the **Okta Verify**
   authenticator is active and its `signed_nonce` method is active.
3. Confirm the authentication policies for the Okta Dashboard and each app the
   Bot signs in to allow FastPass or Okta Verify as a factor. Two-factor
   assurance that includes Okta Verify is typical.
4. Keep **Email** or **Password** available as a factor. The first Okta Verify
   enrollment on each computer needs it.

## 2. Add the Team Setup Script

The setup script is part of the Grok Bot computer image. It installs a pinned
Okta Verify 7.1.3.0 build, then starts the Okta services, a login session shim,
and the `com-okta-authenticator` URI handler. When a sign-in asks for FastPass,
the handler opens the Okta Verify window on the desktop of the Bot that's
signing in. The script is idempotent and holds no embedded certificates or
secrets.

1. Go to [Grok Bot in the Cursor dashboard](https://cursor.com/dashboard/bot)
   and find **Team Setup Scripts** under **Bot Computers**.

2. Create a manifest, or open an existing one, and add a script entry, for
   example with the ID `okta-verify`.

3. Set the **Setup Script** and **Check Script**, passing your org URL to both:

   ```bash
   # Setup Script
   setup-okta.sh --org-url=https://yourorg.okta.com
   # Check Script
   setup-okta.sh --check --org-url=https://yourorg.okta.com
   ```

4. Select **Save**.

The entry names the command, not a path, so it runs from any working directory.
Computers run it at every start and on the periodic refresh. The services it
starts don't survive a restart, so the check reruns setup when they're down. A
failed setup is reported and never blocks the computer. See
[How Team Setup runs your scripts](/grok-bot/private-networks#how-team-setup-runs-your-scripts).

### Okta Verify settings

The script writes the settings you pass to the Okta Verify admin settings file,
`/etc/okta/adminconfig.json`. Pass the same options on the Check Script line,
so the check confirms they're in place. The common ones:

| Option | Values | What it does |
| --- | --- | --- |
| `--org-url` | `https://yourorg.okta.com` | Prefills your org on the sign-in URL screen. It doesn't change where the package downloads from. |
| `--enrollment-options` | `Default`, `Enabled`, `SilentEnrollmentDisabled`, `Disabled` | Controls how accounts enroll. |
| `--user-verification-enrollment` | `Disabled`, `Deferred`, `Preferred`, `Required` | Controls passcode setup at enrollment. `Disabled` skips it, so sign-ins fail if your org requires user verification. |
| `--auto-registration` | `DEVICE` | Turns on userless device registration. |

For the full list, see [Setup script reference](#setup-script-reference).

## 3. Enroll Okta Verify

Each computer enrolls once. Enrollment is stored in the computer's home
directory and survives restarts.

1. Open the Okta Verify window on your desktop. From a terminal on the
   computer, run `setup-okta.sh --display :N`, where `:N` is your desktop's
   display (the value of `$DISPLAY`).
2. Select **Get started**, then **Next**.
3. Enter `https://yourorg.okta.com` and select **Next**.
4. Sign in in the browser with whatever your policy allows, such as password
   and email.
5. Create an Okta Verify passcode. Store it privately, and never commit it or
   paste it into chat.
6. Finish when Okta Verify shows **Account added** with passcode confirmation
   on.

## 4. Verify FastPass

1. Open a fresh browser session on the computer and go to
   `https://yourorg.okta.com`.
2. Enter the username and select **Use Okta FastPass**.
3. When Okta Verify asks for the passcode, enter it within about 30 seconds.
   Type it or use right-click > **Paste**. Pressing Ctrl+V crashes the Linux
   app.
4. In the Admin Console, open **Reports** > **System Log** and confirm both
   events:
   * `user.authentication.auth_via_mfa` with **SUCCESS** and factor
     **SIGNED\_NONCE**
   * `user.session.start` with **SUCCESS** for the Okta Dashboard

## Setup script reference

The script lives at `/usr/local/bin/setup-okta.sh` on every Grok Bot computer.
Run `setup-okta.sh --help` on a computer to print every option and Okta Verify
setting it supports, with accepted values.

## Limitations

* Okta Verify runs as one window per computer user. While the window is open on
  one Bot's desktop, a FastPass sign-in from another Bot's desktop on the same
  computer shows its prompt in that window. The window closes after 5 minutes
  without a sign-in.
* Okta doesn't receive a device manufacturer or model from Grok Bot computers.
  FastPass works without them.
* Ctrl+V in the passcode prompt crashes Okta Verify on Linux. Use right-click >
  **Paste** instead.

## Related pages

* [Configure identity and access](/grok-bot/identity-and-access)
* [Grok Bot for teams and enterprises](/grok-bot/teams-and-enterprises)
* [Connect to private networks](/grok-bot/private-networks)
* [Grok Bot security](/grok-bot/security)
