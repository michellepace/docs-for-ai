#### Reference

# Deep links

A deep link opens Grok Bot on your desktop or phone from a shortcut, note, or
another app. The app must be installed and signed in.

## Start a message

```text
grokbot://app/v1/prompt?id=<bot-id>&text=<message>
```

Opens the Bot's chat with `text`, up to 1,000 characters, in the message box.
The text is added only if the message box is empty, and it isn't sent until you
send it. Without `id`, the link uses your
[primary Bot](/grok-bot/bots#your-primary-bot), and does nothing if you haven't
set one. The Bot's ID is the end of its link: click the Bot's name, choose
**Share**, then **Copy link**. Encode `text`, for example `%20` for a space, or
build the link here. The web link opens the app from a browser, so it works where
`grokbot://` links aren't clickable.

## Add a plugin

```text
https://x.ai/bot/plugin/<plugin-id>
```

Opens a plugin from the marketplace in Grok Bot so you can add it and sign in.
On a Mac or Windows computer, the page opens the desktop app on the plugin, with
**Add** ready to choose. On a phone with Grok Bot installed, the link opens the
plugin in the app, where you choose **Authorize** to connect it. Anywhere else,
or without the app, the page shows the plugin with **Add to Grok Bot** and a
link to download the app.

To get a plugin's link, open it in **Connect apps** on desktop and choose
**Share**. A plugin only your team can see copies its app link instead, which
opens the same place in an installed app:

```text
grokbot://app/v1/plugin/add?id=<plugin-id>
```

A custom connector you added yourself has no link.
