#### Use Grok Bot

# Use Grok Bot in Microsoft Teams

Bring a [Team Bot](/grok-bot/team-bots) into Microsoft Teams so your team can
mention it in channels, chat with it directly, and add it to group chats. It
works the way it does in Slack: it acts for the person who asked, uses their
usage, and asks before risky actions.

## What do I need before adding a Bot to Microsoft Teams?

* A published Team Bot. You must be its owner or a Manager.
* Microsoft Teams turned on for your Cursor team by a team admin. See [How does
  a team admin turn on Microsoft
  Teams?](#how-does-a-team-admin-turn-on-microsoft-teams)
* A Microsoft account in the organization that uses Teams.

## How does a team admin turn on Microsoft Teams?

1. On the Grok Bot page of the team dashboard, under **Shared Bots**, choose
   **Enable** next to **Enable Microsoft Teams**.
2. Sign in with a Microsoft Teams or Global administrator account and accept
   the permissions Microsoft shows.

The row then shows that Microsoft Teams is enabled for your organization. Bot
owners on the team can now connect their own Bots. **Revoke** turns it off. A
Microsoft Teams admin still approves each Bot in the Teams admin center.

## How do I add a Team Bot to Microsoft Teams?

The owner or a Manager connects it, after publishing:

1. Open the Bot's details and find **Bring to your team's Microsoft Teams**, or
   choose **Manage** and look under **Channels**. Choose **Connect Microsoft
   Teams**.
2. Finish signing in with Microsoft in the browser window that opens. Confirm
   it's the right account, and choose an organization if you belong to more
   than one.
3. While the dialog says **Waiting on admin approval**, a Microsoft Teams admin
   needs to approve the Bot in the Teams admin center, under **Teams apps** >
   **Manage apps** > **Pending approval**. Microsoft doesn't notify them, so
   send them the link the dialog shows. Choose **Check again** right after they
   approve, or **Cancel request** to stop.

Once it's approved, Microsoft Teams finishes setting up the Bot on its own,
which can take up to an hour. The dialog then says the Bot is in Microsoft
Teams, with **Open in Teams**. To use it in a channel, add it to a team from
Microsoft Teams, and the dialog lists the teams it's been added to.

If a Teams admin declines the Bot, the dialog shows their note. Make any changes
and choose **Resubmit**.

## How do I link my Microsoft Teams account?

The Bot needs to know who you are before it can act for you. The first time you
message it, it replies with a **Link Account** card that only you can see.
Choose it and sign in with your Microsoft account.

You can also link first: open **Settings** > **General** > **Team Bots** and
choose **Link** next to **Microsoft Teams account**. If it says your admin
hasn't turned on Microsoft Teams for your organization yet, ask a Cursor team
admin to enable it.

## What can a Bot do in Microsoft Teams?

* **Answer in channels and chats.** Mention the Bot in a channel of a team it
  joined, add it to a group chat, or message it directly.
* **Read the conversation.** It reads the thread it's in, and the channels of
  the teams it joined.
* **Work with files.** It reads files attached to posts and sends you files
  through your OneDrive. If you ask for a file in a channel or group chat, it
  asks you to message it directly instead.
* **Act for you.** It uses your usage and asks you before risky actions, the
  same as in Slack. See [Whose computer and
  usage](/grok-bot/team-bots#whose-computer-and-usage)

To have a Bot join a Teams call and transcribe it, see [Add a Bot to your
meetings](/grok-bot/meetings).

## How do I update or remove a Bot in Microsoft Teams?

* **Name or picture.** After you change them, the dialog says the Bot's name or
  avatar changed. Choose **Update in Teams**. If your Teams admin has to approve
  the change, it shows **An update is waiting for your Teams admin**.
* **Remove it.** Choose **Remove from Microsoft Teams** in the same dialog. This
  removes the app from your Microsoft Teams organization, and teammates can't
  reach the Bot there until it's added again.
* **Disconnect your Microsoft account.** This disconnects it from every Bot you
  own in that organization, not only this one. Bots already in Teams keep
  answering there.
* **Delete the Bot.** Deleting a Bot also removes it from Microsoft Teams.

## Why isn't my Bot in Microsoft Teams?

| What you see | What it means |
| --- | --- |
| **Microsoft Teams isn't enabled** for your team | A team admin needs to choose **Enable Microsoft Teams** on the Grok Bot page of the team dashboard. |
| **Publish this Bot to your team first, then add it to Microsoft Teams** | The Bot is still a draft. Choose **Publish**, then connect. |
| **Waiting on admin approval** | Your Teams admin hasn't approved the Bot. Send them the link in the dialog, then choose **Check again**. |
| **Your Teams admin declined** the Bot | Check their note, make changes, and choose **Resubmit**. |
| **Microsoft Teams didn't accept the app** | Your organization doesn't allow custom apps in Teams. A Teams admin can allow them. Choose **Download app package** and send it to your Teams admin to upload. |
| **Blocked by your organization's Teams app policy** | A Microsoft Teams admin needs to allow the app in the Teams admin center. |
| **Need admin approval** | The Microsoft sign-in needs an admin's consent. Send a Microsoft Teams or Global admin the link the dialog shows, then connect again. |
| **Microsoft Teams stopped working for your team** | The team's connection expired. A Cursor team admin needs to choose **Reconnect Microsoft Teams** on the dashboard. |
| **Finishing setup in Microsoft Teams** | The Bot is approved and Teams is still setting it up. This can take up to an hour and finishes on its own. |
| A **Link Account** card | Your Microsoft account isn't linked yet. Choose it and sign in. |

If none of these match, [contact support](/grok-bot/troubleshooting) with the
Bot's name, the exact message, and your Grok Bot version.

## Related pages

* [Team Bots](/grok-bot/team-bots)
* [Add a Bot to your meetings](/grok-bot/meetings)
* [Approvals, security, and privacy](/grok-bot/approvals-security-and-privacy)
* [Grok Bot for teams and enterprises](/grok-bot/teams-and-enterprises#microsoft-teams)
