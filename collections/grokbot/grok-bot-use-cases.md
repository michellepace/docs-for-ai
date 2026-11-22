#### Get started

# Use Cases

The use cases on this page build in three steps. Connect the apps you already
use and ask a Bot to help with your work. When you notice a task you keep asking
for, turn it into a Bot of its own. Once you have a few of those, put them on a
team that works toward a bigger goal.

1. [An assistant](/grok-bot/use-cases#connect-your-apps-and-get-help-with-your-work) — Finds information and drafts work in your apps

2. [A Bot with a job](/grok-bot/use-cases#turn-tasks-you-repeat-into-a-bot) — Takes over a task you keep repeating

3. [A team of Bots](/grok-bot/use-cases#build-a-team-of-bots-for-a-bigger-goal) — Works together toward a bigger goal

Every example stops for your review. Keep sending, publishing, purchasing, and
production changes behind
[approval](/grok-bot/approvals-security-and-privacy#review-an-action).

## Connect your apps and get help with your work

Connect your mail, calendar, chat, and docs, and every Bot you run can read and
work in them. For services without an app, a Bot uses the browser on the cloud
computer. See [Connect an app](/grok-bot/computer-and-apps#connect-an-app).

* [Google Drive](https://x.ai/bot/plugin/45893413) — Draft from what’s already there. Reads the briefs and past decks in a folder, drafts the next one in your format, and leaves it in Drive for your edits.

* [Google Calendar](https://x.ai/bot/plugin/45893411) — Start each week with a plan. Every Sunday evening, reads the week ahead, flags clashes and packed days, and sends you a short plan for Monday.

* [Gmail](https://x.ai/bot/plugin/45893410) — Wake up to a sorted inbox. Sorts the night’s mail before you’re up, drafts replies to the threads that need you, and leaves every draft for you to send.

* [Granola](https://x.ai/bot/plugin/5609) — Turn notes into next steps. Each evening, reads the day’s Granola notes, pulls out every action item with its owner, and drafts a post for your team’s Slack channel that goes out once you approve.

* [Slack](https://x.ai/bot/plugin/674) — Pick up requests as they come in. Watches for mentions of your name, starts on the ask, like marketing copy or a campaign brief, and sends you a draft to approve before it replies in the thread.

* [Notion](https://x.ai/bot/plugin/404) — Keep project pages current. Every Friday, drafts a progress update for each project page, highlights what changed, and adds it once you approve.

[Browse all apps](https://cursor.com/marketplace)

Then ask a Bot for things you'd otherwise look up yourself, like what changed
overnight, who's in your next meeting, or what a competitor shipped this week.
It reads across the apps you connected and drafts the next step for you.

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

### Meeting prep

A one-page brief on who's in the room, your last touch, and open threads.

**Starter prompt**

> Prep me for my 2 PM: who is attending, what we last discussed, and any open threads. Keep it to one page.

## Turn tasks you repeat into a Bot

Watch for the asks you make every week, like qualifying inbound leads or matching
invoices. Give each one to a Bot with that single job, so it builds up the
context to do it well.

### Sales development

Inbound leads qualified, with every reply drafted.

**Starter prompt**

> Qualify this morning's inbound leads against our ideal customer profile. Draft intro replies with times I'm free for good fits and a polite no for the rest; don't send anything.

### Invoice coordinator

Invoices matched to purchase orders, with mismatches flagged.

**Starter prompt**

> Match this week's invoices in the finance inbox to their purchase orders. List the ones that don't match and draft a note to each owner; don't approve or pay anything.

### Content marketer

The newsletter and posts drafted in your voice.

**Starter prompt**

> Pull what we shipped this week from the changelog and Slack, and draft the newsletter and three posts in our voice. Bring me the drafts; don't publish anything.

### Talent scout

A sourced shortlist, with outreach drafted in your voice.

**Starter prompt**

> Find 20 candidates for this role who meet the must-haves and aren't already in our ATS. Draft outreach in my voice; don't contact anyone.

### Paid media

A budget reallocation backed by spend and acquisition cost, for your approval.

**Starter prompt**

> Compare this month's spend by campaign with our budget and target CAC, and recommend where to move money. Don't change any budgets.

### Expense manager

A weekly expense summary with receipts matched and follow-ups drafted.

**Starter prompt**

> Build this week's expense summary, match receipts from the finance inbox, and flag policy exceptions. Draft one follow-up per owner; don't send them.

### Product performance

A short write-up of the likeliest hotspot, with screenshots and links.

**Starter prompt**

> Find out why checkout got slower after yesterday's release. Send me the likeliest hotspot with screenshots and links, and don't change production settings.

### Bug reproduction

A repro pack with exact steps, screenshots, and browser details.

**Starter prompt**

> Reproduce this bug in staging with a fresh test account. Send me the exact steps, screenshots, and browser details; don't use customer data.

### Account health

A ranked watch list of accounts at risk or ready to expand, with the evidence.

**Starter prompt**

> Rank the accounts in my book by churn risk and expansion potential from usage, tickets, and renewal dates. Suggest a next step for each; don't contact anyone.

When the Bot does the job the way you want, make it run on its own:

* Tell the Bot its job and its limits in chat, and
  [ask it to remember them](/grok-bot/bots#edit-a-bot).
* [Save the steps as a skill](/grok-bot/skills-routines-and-automations#save-a-skill),
  then [create a routine](/grok-bot/skills-routines-and-automations#create-a-routine)
  to run it on a schedule.
* Save test logins in [Vault](/grok-bot/vault) or enter them in a
  [Secure Form](/grok-bot/vault#secure-forms), never in chat.

## Build a team of Bots for a bigger goal

Some goals take more than one job, like a launch campaign or the month-end close.
Ask your primary Bot to set up a few Bots that each own one part. They pass the
work along, and you check the result. To get help splitting the work into jobs,
start from dr eggbot.

* [dr eggbot](https://x.ai/bot/marketplace/bots/dr-eggbot-v2) — Asks you a few questions, then sets up the Bots for you, one job each.

### Campaign team

Launch posts drafted from the numbers and checked before you see them.

1. **Sign-ups** — Pulls last week's sign-ups by channel

2. **Launch drafts** — Drafts a launch note and three posts from the numbers

3. **Fact check** — Checks the drafts against the numbers and brand doc

Runs Mondays at 9 AM. Ask your primary Bot to set up this team.

### Month-end close

Invoices matched, expenses reconciled, and exceptions listed for your sign-off.

1. **Invoices** — Matches invoices in the finance inbox to purchase orders

2. **Expenses** — Reconciles expense reports with receipts

3. **Exceptions** — Lists every mismatch for your sign-off

Runs on the 1st of each month. Ask your primary Bot to set up this team.

### Support queue

Tickets sorted, replies drafted, and bugs reproduced for your review.

1. **Ticket triage** — Sorts new tickets and drafts replies

2. **Bug repro** — Reproduces bug reports in staging with a test account

3. **Help pages** — Flags help pages that need fixing

Runs weekdays at 9 AM. Ask your primary Bot to set up this team.
