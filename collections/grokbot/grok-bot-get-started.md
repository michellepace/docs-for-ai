#### Get started

# Get started

Grok Bot gives you Bots that do work for you on a cloud computer they share. In
this guide, you'll install the app, sign in, hand your first Bot a real task,
and set it to repeat that task on a schedule.

## 1. Install the desktop app

Download Grok Bot from [x.ai/bot](https://x.ai/bot) and open it.

**Other downloads and supported systems**

On a team, the Grok Bot page of the
[Cursor dashboard](https://cursor.com/dashboard/bot) has a **Download Grok Bot**
row that installs the app or copies a link you can share. If you don't have
dashboard access, ask your admin for the link. If you're the admin, see
[Deploy Grok Bot to your organization](/grok-bot/deployment).

The app runs on macOS (Apple silicon and Intel), Windows (x64 and Arm64), and
Linux (x64 and Arm64). It checks for updates automatically. Linux `.deb` and
`.rpm` installs update through your package manager instead.

## 2. Sign in

Choose **Sign in** on the welcome screen and finish in your browser.

**Which plans include Grok Bot**

Premium, Super, and Ultra on The X Subscription include Grok Bot, for an
individual or a team seat. On a legacy Cursor plan, every paid individual plan
and self-serve Cursor Teams include it. You can also link an individual SuperGrok,
SuperGrok Plus, SuperGrok Heavy, or X Premium+ subscription, or use a seat on a
self-serve Grok Business plan. See
[Grok Bot on The X Subscription](/x-subscription/grok-bot) and
[Plans and billing](https://grok.com/help/grok-bot/plans).

Grok Bot needs cloud data storage, so if your account is on Privacy Mode
(Legacy), the app asks you to switch to Privacy Mode first. On a team, a team
admin changes the team's privacy setting.

**Single sign-on and Grok accounts**

Grok Bot uses your Cursor account, so there's no separate login. If your company
uses single sign-on, sign in the usual way; your Cursor SSO setup applies.

If your access comes from a seat on a self-serve Grok Business plan, choose
**Sign in with Grok** in the browser and use the Grok account that holds the
seat.

If your access comes from a SuperGrok or X Premium+ subscription, add a Grok
account link. On desktop, choose **Link Grok Account** on the **Get Started with
Grok Bot** page at [cursor.com/bot/onboarding](https://cursor.com/bot/onboarding).
On iPhone and Android, choose **Link Grok Account** on the access screen, finish
signing in to Grok, then choose **Finished Linking? Refresh My Status**.

If you already have access, open **Settings → Usage & Billing** and look under
**Manage Plan** for **Get Access with Grok**. It appears only when linking would
raise your usage.

If sign-in doesn't finish, see
[Sign-in does not complete](/grok-bot/troubleshooting#sign-in-does-not-complete).

## 3. Meet your first Bot

After a short intro, the app sets up your first Bot, named **Grok Bot**, and
opens a chat with it.

You can also start from a Bot that's already set up for a job.

* [Overheard](https://x.ai/bot/marketplace/bots/overheard) — Watches Reddit, Hacker News, news sites, and X for third-party mentions of your name, brand, and URLs, then sends a short weekday digest when something clears the bar. Stays quiet on dead days and never posts on your behalf.

* [Tradbot](https://x.ai/bot/marketplace/bots/tradbot-2) — Watches your personal email and calendar so school forms, bills, and RSVPs don't slip. Drafts the reply, catches the pickup clash, and never sends without you.

* [Meeting Recap Deck](https://x.ai/bot/marketplace/bots/echo) — Turns your meeting notes into a recap deck in your slide template. Works from notes you paste or upload, and never invents a quote.

* [Pitch Deck Coach](https://x.ai/bot/marketplace/bots/pitch-deck-coach) — Reviews a pitch deck and reports what an investor is likely to understand, believe, question, and remember, then helps strengthen the story, evidence, and slides.

[Browse the marketplace](https://x.ai/bot/marketplace)

**Set up more Bots**

Choose **New Bot** (the **+** button) at the top of the sidebar, or press
`Cmd/Ctrl+N`. Name the Bot and choose **Create**. On a team, **+** opens a menu.
Choose **Create a Bot** to make one, or **Browse Team Bots** to use a Bot a
teammate shared. To share your own Bot with teammates, see
[Team Bots](/grok-bot/team-bots).

To rename a Bot later, click its name at the top of the chat to open its
details, then click the name again to edit it.

Give each Bot one job in its first message and ask it to remember how you want
the work done. A Bot with one job builds more useful context than a catch-all
helper. See
[Your primary Bot and Bots with one job](/grok-bot/how-grok-bot-works#your-primary-bot-and-bots-with-one-job).

## 4. Hand it a first task

Ask the way you'd ask a coworker. Say what you want back, which sources to use,
any limits, and when to check with you. When an action needs your OK, the Bot
shows an [approval card](/grok-bot/approvals-security-and-privacy#review-an-action)
and waits.

### Morning briefing

Your morning brief of what needs you, ready to post.

**Starter prompt**

> Sum up what changed since yesterday in my inbox, calendar, Slack, and docs, and flag what needs me. Draft it as a post for #team; don't send it.

### Inbox manager

Urgent threads first, with replies drafted for your OK.

**Starter prompt**

> Sort my unread email into urgent, needs a reply, and FYI. Draft replies to the urgent ones and don't send anything.

### Competitive intelligence

What competitors launched or repriced this week, with links.

**Starter prompt**

> Check these three competitors for anything they launched or repriced this week. Send me a short list with links and what it means for our messaging.

### Travel coordinator

The two best flights and hotels, ready for you to pick.

**Starter prompt**

> Find flights to Austin for Thursday, back Sunday, with no red-eyes, and a hotel near downtown. Send me the two best options; don't book anything.

**Talk instead of typing**

To dictate, choose **Start voice input** (`Cmd/Ctrl+D`) on desktop or
**Start dictation** on iPhone and Android. For a live conversation, choose
**Start voice chat**.

**When a task needs a login**

To sign in, the Bot uses a login saved in [Vault](/grok-bot/vault) first, then a
connected password manager such as
[1Password](/grok-bot/computer-and-apps#connect-1password), then asks you with a
[Secure Form](/grok-bot/vault#secure-forms). It never sees the password, and the
session usually stays signed in on the Bot's computer for next time. For
supported services, you can
[connect an app](/grok-bot/computer-and-apps#connect-an-app) instead.

For single sign-on, a passkey, or another step a form can't handle, the Bot
hands you the computer. Choose **Open computer** on the request, then **Take
control**, finish the step, and tell the Bot to continue.

## 5. Make it a routine

Tell the Bot what to fix and which preferences to keep, like a report format.
When the result is right, ask it to do the task on a schedule, and it becomes a
[routine](/grok-bot/skills-routines-and-automations#create-a-routine).

## What's next

Your Bot now runs that task on a schedule. Next, connect more of the apps you
use, turn the tasks you keep repeating into Bots of their own, then put a few
Bots on a team with a bigger goal.

1. [An assistant](/grok-bot/use-cases#connect-your-apps-and-get-help-with-your-work) — Finds information and drafts work in your apps

2. [A Bot with a job](/grok-bot/use-cases#turn-tasks-you-repeat-into-a-bot) — Takes over a task you keep repeating

3. [A team of Bots](/grok-bot/use-cases#build-a-team-of-bots-for-a-bigger-goal) — Works together toward a bigger goal

On your phone, install Grok Bot from the App Store or Google Play and sign in
with the same account. See [Grok Bot on mobile](/grok-bot/mobile).

**What works on your phone**

The iPhone app needs iOS 18 or later, and the Android app needs Android 9 or
later.

Both apps reach the same Bots, conversations, routines, and cloud computer as
desktop. Access from your plan or Grok account link carries over without a
second purchase. From your phone you can message Bots, watch and take over the
computer, approve actions, and pause or resume routines.

If something doesn't work, quit and reopen the app. If that doesn't fix it, see
[Troubleshooting](/grok-bot/troubleshooting) or
[contact support](/grok-bot/troubleshooting#before-contacting-support).
