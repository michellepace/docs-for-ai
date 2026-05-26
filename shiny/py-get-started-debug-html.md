## Common issues [Anchor](https://shiny.posit.co/py/get-started/debug.html\#common-issues)

Before jumping into general debugging techniques, lets cover some common issues that you may encounter when developing Shiny applications, and explain why they happen.

### Missing output [Anchor](https://shiny.posit.co/py/get-started/debug.html\#missing-output)

Sometimes, output won’t appear at all. This most commonly happens when an output reads a non-existent input, for example:

app.py×fixed.py×+

99

1

2

3

4

5

6

7

8

9

10

11

from shiny.express import input, render, ui

ui.input\_slider("val", "Slider value", min=0, max=10, value=5)

\# Nothing renders because input.wrong\_id() doesn't exist!

@render.text

defslider\_val():

returnf"Slider value: {input.wrong\_id()}"

This happens because, if a non-existent input is read, a [`SilentException`](https://shiny.posit.co/py/api/express/req.html#shiny) is raised. That behavior is useful for events and [dynamic ui](https://shiny.posit.co/py/docs/ui-dynamic.html), but it can be confusing when you mistype an input id.

Tip

These are live Shiny apps that you can edit. Try fixing the problem yourself! You can also take a look at the `fixed.py` file to see the solution. You will need to copy the code to `app.py` if you want to run the fixed solution.

### Output errors [Anchor](https://shiny.posit.co/py/get-started/debug.html\#output-errors)

When an error occurs inside a `render` decorator function, the relevant error message is displayed in red font where the output would normally be located, for example:

app.py×fixed.py×+

99

1

2

3

4

5

6

7

8

9

10

11

12

13

from shiny.express import render

@render.text

defgood():

return"This output is fine, but the next one is not."

@render.text

defbad():

return str(a\_missing\_variable)

The error displayed in the app is only the final part of the stack trace, but the full trace can be read in the console where you used `shiny run`.

Sanitized error messages

When Shiny apps are deployed, error messages are sanitized to the eliminate the possibility of leaking sensitive information. To unsanitize error messages, you’ll need to set `sanitize_errors=False` in the `App` constructor (of a [Shiny core app](https://shiny.posit.co/py/docs/express-vs-core.html)).

## Debugging [Anchor](https://shiny.posit.co/py/get-started/debug.html\#debugging)

There are many ways you can debug you code. Most likely, your IDE will have the ability to create breakpoints and debug your code. However, you can manual edit your code to help with debugging as well.

### Positron and VS Code debugger [Anchor](https://shiny.posit.co/py/get-started/debug.html\#positron-and-vs-code-debugger)

The [Positron and VS Code debugger](https://code.visualstudio.com/docs/editor/debugging) is a powerful tool for debugging Python code. To set a breakpoint in Positron or VS Code, you will need to click the gutter next to the line number. The gutter is empty space immediately to the left of the line number. When you click this area, a red circle will mark that particular line.

![](https://shiny.posit.co/py/get-started/assets/debug-positron-gutter-marked.jpg)

Red circle next to the line number in the editor is where you will click to mark a breakpoint.

Once the breakpoint is set, you can click the dropdown arrow next to the play button and select “Debug Shiny App”.

![](https://shiny.posit.co/py/get-started/assets/debug-positron-run.png)

Showing the dropdown menu next to the Run icon.

This will run the shiny application in debug mode, and will pause the application when it reaches the code you have just marked. From there you can open the Debug Console by click the 3 dots in the debug menu. Once you are in the debug console, you can explore all the variables at that moment in the application, including any `input` variables. You can Mark as many points in your application you want at the same time, and you can step through the code using the debugging toolbar.

![](https://shiny.posit.co/py/get-started/assets/debug-positron-console-marked.jpg)

Image of Positron highlighting where to enable the debug console towards the top left, running code in the debug console on the bottom, and moving through the code on the top right.

### Manual debugging methods [Anchor](https://shiny.posit.co/py/get-started/debug.html\#manual-debugging-methods)

Here we define manual debugging methods. These methods are less recommended because they require a manual change to your codebase, and potentially restarting your application.

#### Shiny debug mode [Anchor](https://shiny.posit.co/py/get-started/debug.html\#shiny-debug-mode)

An advanced option for debugging is to use the debug mode when running your application.

For Shiny Express applications, you can use the `shiny.express.app_opts(debug=True)` function call at the top of your application after the imports.

![](https://shiny.posit.co/py/get-started/assets/debug-mode-express.png)

Importing and using `app_opts` from `shiny.express` within Positron. The highlighted line in the Terminal on the bottom shows an example of the communication between server and web browser.

For [Shiny Core apps](https://shiny.posit.co/py/docs/express-vs-core.html), pass the `debug=True` argument to the `App()` call, e.g., `App(..., debug=True)` at the bottom of your application.

When you run a Shiny app in debug mode, you’ll see detailed messages in the terminal. These messages show the communication between the server and the web browser.

This is an example of the raw data behind how your app works:

```json
SEND: {"busy": "busy"}
SEND: {"recalculating": {"name": "my_cool_output", "status": "recalculating"}}
SEND: {"recalculating": {"name": "my_cool_output", "status": "recalculated"}}
SEND: {"busy": "idle"}
SEND: {"values": {}, "inputMessages": [], "errors": {}}
```

- When a user changes an input, the browser sends a message to the server.
- The server responds with updates, like re-running a calculation or updating a plot.

Note also that Shiny applications use Python’s [asyncio](https://docs.python.org/3/library/asyncio.html) under the hood, so it may be useful to set [asyncio’s debug mode](https://docs.python.org/3/library/asyncio-dev.html#debug-mode).

### Manual breakpoints [Anchor](https://shiny.posit.co/py/get-started/debug.html\#breakpoints)

You can use `breakpoint()` to pause your app while it’s running and inspect what’s going on. This serves the same purpose as clicking and marking a breakpoint in the Positron IDE a, but requires you manually adding new code to the application. This lets you debug using the .

```
@render.text
def bad():
    breakpoint()
    return str(a_missing_variable)
```

When Python hits the `breakpoint()`, it will pause and open the debugger in your terminal.

From there, you can run commands like:

- `continue`: resume running the app
- `exit` or `Ctrl` \+ `D`: exit the debugger and stop the app

This is helpful for figuring out where things go wrong in your code.

#### Print statements [Anchor](https://shiny.posit.co/py/get-started/debug.html\#print-statements)

A quick and simple way to debug Shiny applications is to add `print()` statements. This lets you see the value of different variables, and how they change when you toggle different inputs.

![](https://shiny.posit.co/py/get-started/assets/debug-print.png)

Adding a print statement to a `render.txt` output. The terminal output on the bottom shows the different values printed as the slider was moved.

Warning

If your Shiny application is running with [Shinylive (Python in the browser)](https://shiny.posit.co/py/get-started/shinylive.html), and there is not a visible Python console, then error messages will show up in your browser’s JavaScript console.

## Get Help [Anchor](https://shiny.posit.co/py/get-started/debug.html\#get-help)

### Shiny [Anchor](https://shiny.posit.co/py/get-started/debug.html\#shiny)

1. The first place to look for help with Shiny is [Posit Community](https://community.rstudio.com/c/shiny), which is a warm and welcoming place to ask any questions you might have about Shiny (as well as tidyverse and all things Posit). The web site is running Discourse, which is an excellent community discussion platform. Our developers monitor Posit Community and answer questions periodically.

2. Shiny users (and the Shiny team!) regularly talk on [Shiny’s Discord server](https://discord.gg/yMGCamUMnS). Discord has more of a chat interface than Posit Community, and is not indexed by search engines. It’s a great forum for casual conversations or networking with other Shiny developers.

3. You can also check the [“shiny+python” tag on Stack Overflow](https://stackoverflow.com/questions/tagged/shiny+python) for existing answers, or post your own question. (Keep in mind that general [Shiny for R answers](https://stackoverflow.com/questions/tagged/shiny) may also point you in the right direction.) Note that questions posted on Stack Overflow are not closely monitored by our developers.

### Posit Connect Cloud [Anchor](https://shiny.posit.co/py/get-started/debug.html\#posit-connect-cloud)

1. For information about [Posit Connect Cloud](https://connect.posit.cloud/), see the [Connect Cloud Documentation](https://docs.posit.co/connect-cloud/)

2. For community support, there is a [community forum for Connect Cloud](https://forum.posit.co/c/posit-professional-hosted/posit-connect-cloud/67).

3. Customers with Starter, Basic, Standard or Pro subscriptions can get direct access to our support engineers by opening a case on [the Posit Support site](https://support.posit.co/). Questions are answered from 9AM - 5PM(EST) Monday - Friday.

### shinyapps.io [Anchor](https://shiny.posit.co/py/get-started/debug.html\#shinyapps.io)

1. For documentation and instructions on how to use [shinyapps.io](http://shinyapps.io/), see the [shinyapps.io user guide](https://docs.posit.co/shinyapps.io/).

2. The best place to get community support for shinyapps.io is the [shinyapps.io category on Posit Community](https://community.rstudio.com/tags/shinyappsio). If you’re having difficulties with shinyapps.io, feel free to ask questions there. Another option is to file an issue in the [rsconnect-python package repo](https://github.com/rstudio/rsconnect-python/issues).

3. Customers with Starter, Basic, Standard or Pro subscriptions can get direct access to our support engineers by opening a case on [the Posit Support site](https://support.posit.co/). Questions are answered from 9AM - 5PM(EST) Monday - Friday.

### Posit Connect and Shiny Server Pro [Anchor](https://shiny.posit.co/py/get-started/debug.html\#posit-connect-and-shiny-server-pro)

Customers with Posit Connect or Shiny Server Pro subscriptions can [contact our dedicated support team](https://support.posit.co/) for our commercial offerings.

### Sales [Anchor](https://shiny.posit.co/py/get-started/debug.html\#sales)

For sales questions, please email [sales@posit.co](mailto:sales@posit.co).
