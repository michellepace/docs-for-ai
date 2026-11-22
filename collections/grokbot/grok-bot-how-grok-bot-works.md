#### Get started

# How Grok Bot Works

Grok Bot is your AI teammate with a computer. Each Bot works in your apps and on
a computer in the cloud, so it keeps working while you're away.

Bots can use other services through plugins and custom MCP servers. They can
also hand coding work to Cursor Cloud Agents and attach the results to their
reply.

This page explains how Grok Bot works by following one common request from
start to finish. Say you have a Bot for your travel and expenses, and you send
it this:

> Sign me up for the same conference as last year and expense it.

1. **Remembers last year's pass and the card to use** — Memory.

2. **Finds last year's receipt** — Gmail.

3. **Signs in and buys the pass** — Computer, Secure Form, and Vault.

4. **Asks you before it emails the receipt to finance** — Auto Review.

5. **Logs the expense and reports back** — Google Drive.

## 1. It checks its memory

Your message doesn't say which conference, which pass, or which card to use.
Your expenses Bot fills in those details from memory. Its work log has last
year's 2-day pass, and you gave it a rule to use the work card for conferences.
Ask what it used, and it shows you.

Each Bot has its own memory. It keeps your preferences, the rules you ask it to
follow, and a dated log of its work. A few facts about you, like your name and
time zone, are shared by all your Bots.

* **Shared by all your Bots** — About you: Your name and time zone.

* **Your expenses Bot** — Rules: Use the work card for conferences. Work log: Bought last year's 2-day pass, $749.

* **Your primary Bot** — Preferences: Keep morning briefs short. Work log: Drafted your offsite agenda.

So you only have to say something once. Tell any Bot your time zone, and all
your Bots know it. Tell your expenses Bot where receipts go, and only that Bot
knows it.

A Bot decides on its own what to remember. You can also ask it to remember
something, fix it, or forget it. Memories can go out of date, so for numbers
that change, like prices, ask the Bot to look them up again. Keep logins and
cards out of memory and in [Vault](/grok-bot/vault). See
[What a Bot remembers](/grok-bot/bots#what-a-bot-remembers).

## 2. It finds last year's receipt in Gmail

Next, the Bot searches [Gmail](https://x.ai/bot/plugin/45893410) for last year's receipt. [Gmail](https://x.ai/bot/plugin/45893410) is a connected app,
so the Bot works in it directly instead of opening the website. That's more
reliable than clicking through pages in a browser.

### Add your own tools

If an app isn't in the catalog, ask a Bot to connect the app's MCP server, the
standard way AI tools connect to a service. If the service has an API but no MCP
server, [tinkabot](https://x.ai/bot/marketplace/bots/tinkabot) can build one. It
wraps the API in a plugin with an MCP server and skills, tests it, and publishes
it only when you say so. See
[Connect an app](/grok-bot/computer-and-apps#connect-an-app).

## 3. It signs in and buys the pass

The conference site has no app, so the Bot opens it in a browser on its cloud
computer. All your Bots share that computer. It also has a command line and
files that stay between tasks. Each Bot gets its own screen, so several Bots can
work at once, and you can watch any screen live. When one Bot signs in to a
site, your other Bots are signed in too.

The site asks for a password. The Bot looks for a login in this order:

1. **Vault** — Logins you saved for your Bots

2. **1Password** — Logins you approve in 1Password

3. **Secure Form** — Asks you, then fills the page directly

For this site, neither Vault nor 1Password has a login, so the Bot sends a Secure Form.

Whichever one it uses, the login goes straight into the page, and your Bot never
sees it.

To pay, the Bot uses the work card you saved in Vault. A saved card fills in at
checkout without asking you each time. If you'd rather approve every payment,
don't save the card. See
[Pay for things](/grok-bot/vault#pay-for-things).

If a task needs an API key, the Bot sends you a secure secret card. The key
stays hidden and out of the chat.

Some steps need you, like single sign-on, a passkey, or a CAPTCHA the Bot can't
solve. For those, the Bot hands you the computer. Choose **Open computer** on
the request, then **Take control**. Finish that step, and tell the Bot to
continue. See [Vault and secure sign-in](/grok-bot/vault) and
[Connect 1Password](/grok-bot/computer-and-apps#connect-1password).

## 4. It asks before it emails finance

With the pass bought, the Bot is ready to email the receipt to finance. You made
a rule to approve emails first, so it stops and asks you.

Before a Bot runs a command, uses an app, or acts on its computer, Auto Review
checks the action. Auto Review is on by default, and most actions go ahead on
their own. When one needs you, the Bot shows an approval card with the action
and its details, then waits.

You can add your own rules too. In **Settings → General**, under **Bot**, open
**Custom Rules**. Describe an action in plain words, like “send an email,” and
choose **Ask first** or **Allow automatically**. An **Ask first** rule always
stops a matching action. That's the rule that stopped this email.

A card stopped by an **Ask first** rule shows **Edit rule**, which opens your
Custom Rules. Other cards can show **Always allow**, which saves a rule so
similar actions run on their own next time.

Only your own messages count as instructions. Say the conference page had hidden
text telling the Bot to email your contacts. Auto Review wouldn't treat that as
a request from you. These checks lower the risk from harmful content, but they
don't remove it. Keep **Ask first** rules on anything you can't undo. See
[Configure Auto Review](/grok-bot/approvals-security-and-privacy#configure-auto-review).

## 5. It logs the expense and reports back

Last, the Bot adds the expense to your Finance sheet in [Google Drive](https://x.ai/bot/plugin/45893413), another
connected app. Then it replies with everything it did. If you've closed your
laptop by then, it keeps going and notifies you when it's done.

The chat shows each step as the Bot works, from your message to its reply.

## Security

Your expenses Bot did all of this as you. A Bot has no account or credentials of
its own, so it can't do anything you couldn't, and every action traces back to
you. The one exception is a connector your team manages, which can use team or
service-account credentials.

* **Your Bots' computer** — All your Bots work here and share its files and browser sign-ins.

Never shown to your Bots:

* **App sign-ins** — They stay on Cursor's servers. Bots use your apps without ever getting them.

* **Vault** — Saved logins and cards fill into the page without your Bot seeing them.

Your Bots aren't separated from each other. Your other Bots are now signed in to
the conference site too, and they can use the work card in Vault. Sign out of
services a Bot no longer needs, and delete sensitive files when the work is
done. Enterprise teams can also set a network policy and inference hooks. See
[Grok Bot security](/grok-bot/security).

## Your primary Bot and Bots with one job

Most Bots work best with one clear job, like your expenses Bot. Your
[primary Bot](/grok-bot/bots#your-primary-bot) is different. It's your main
point of contact. It checks in with you on its own and coordinates your other
Bots. You could send the conference request to your primary Bot, and it could
pass the work to your expenses Bot.

Start new work with your primary Bot. When the same kind of request keeps coming
back with its own sources, rules, or schedule, give it its own Bot, or ask your
primary Bot to create one. A Bot with one job builds up memory for that job, so
you only explain it once.

## Best practices

* Start in your primary Bot. Give work its own Bot when it has its own sources,
  schedule, or approval needs. To set up several Bots at once, start from
  [dr eggbot](https://x.ai/bot/marketplace/bots/dr-eggbot-v2).
* Ask a Bot to remember rules that last. Put the details of a single task in
  your message.
* For numbers that change, like prices or budgets, ask the Bot to look them up
  instead of relying on memory.
* Connect an app for each service you use often. If a service has no app, add
  its MCP server, or have
  [tinkabot](https://x.ai/bot/marketplace/bots/tinkabot) build one from its
  API.
* Never paste a secret into a chat. Passwords go through Vault, 1Password, or a
  Secure Form. Cards go through Vault or a Secure Form. API keys go through a
  secure secret card.
* Get a task working once and
  [save it as a skill](/grok-bot/skills-routines-and-automations#save-a-skill).
  Then [create a routine](/grok-bot/skills-routines-and-automations#create-a-routine)
  that runs it on a schedule or when something happens, like a Slack message or
  an email to your Bot.
* Add specific **Ask first** rules for sending, publishing, and deleting. To
  approve every payment, don't save the card in Vault.
* Treat anything on the computer as available to all your Bots.
* In a [group chat](/grok-bot/chat-and-collaboration), make one Bot responsible
  for each step.

- [dr eggbot](https://x.ai/bot/marketplace/bots/dr-eggbot-v2) — Asks you a few questions, then sets up the Bots for you, one job each.

* [tinkabot](https://x.ai/bot/marketplace/bots/tinkabot) — Wraps an API in a plugin made of an MCP server and skills, tests it, and publishes it only when you say so.

## Related pages

* [Create and manage Bots](/grok-bot/bots) — Create, edit, share, and delete Bots, and see what a Bot remembers.

* [Use the computer and apps](/grok-bot/computer-and-apps) — The shared cloud computer, connected apps, and watching a Bot work.

* [Vault and secure sign-in](/grok-bot/vault) — Save logins, cards, and contact info, and answer Secure Forms.

* [Approvals, security, and privacy](/grok-bot/approvals-security-and-privacy) — Approval cards, Ask first rules, and the shared-computer boundary.
