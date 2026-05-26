When you [install shiny](https://shiny.posit.co/py/get-started/install.html), you also install the `shiny` command line interface (CLI). You can use this interface to help you create and run your Shiny applications.

## Create a Shiny application [Anchor](https://shiny.posit.co/py/get-started/create-run.html\#create-a-shiny-application)

The best way to create a new Shiny app is with the `shiny create` command. This command asks you a series of questions about what kind of app you want to create, and then provides all the boilerplate code you need to get started with a working app.

```bash
shiny create
```

[Video](https://shiny.posit.co/py/get-started/assets/shiny-create-positron.mp4)

Running the shiny create command from a terminal, accepting default options, opening in Positron, and running the Shiny Application with the Run button.

You can also get started faster by using one of our [starter templates](https://shiny.posit.co/py/templates/). There are templates for common use cases. For example, [data dashboards](https://shiny.posit.co/py/get-started/templates/dashboard/), [applications](https://shiny.posit.co/py/templates/database-explorer/), [streaming](https://shiny.posit.co/py/templates/monitor-database/) updates, or [data entry](https://shiny.posit.co/py/templates/survey/).

## Run your Shiny application [Anchor](https://shiny.posit.co/py/get-started/create-run.html\#run-your-shiny-application)

Shiny apps can be launched from Positron, VS Code, or the command line via `shiny run`.

Name your app `app.py`

We recommend naming your shiny application `app.py`. This is the default file that `shiny run` will look for, so you can run the application in the terminal without any additional parameters.

If you need a more unique name, we recommend beginning the file name with `app`, because the [Shiny extension](https://shiny.posit.co/py/get-started/create-run.html#positron-and-vs-code) expects this naming pattern.

### Positron and VS Code [Anchor](https://shiny.posit.co/py/get-started/create-run.html\#positron-and-vs-code)

The best way to run (and develop) Shiny apps is in [Positron](https://positron.posit.co/) or [Visual Studio Code](https://code.visualstudio.com/) with the [Shiny extension](https://marketplace.visualstudio.com/items?itemName=posit.shiny). When you are editing a Shiny `app.py` file, the default behavior of the Run button (circled in red in the screenshot below) becomes “Run Shiny App”.

![](https://shiny.posit.co/py/get-started/assets/positron-run.png)

Visual Studio Code running with the Shiny extension

When you run a Shiny app in Positron, it starts a Python process in a dedicated terminal and opens the app in an internal web browser. This lets you test and interact with your app without leaving the editor.

Whenever you make changes to the app’s source code, the preview updates automatically. To view your app in a full browser window, click the icon to the right of the URL bar to open it externally.

To debug your app, use the dropdown next to the **Run** button and select **Debug Shiny App**. Before launching in debug mode, make sure to set [breakpoints](https://shiny.posit.co/py/get-started/debug.html#breakpoints) in your code. Once the app starts, you can step through your code starting from those [breakpoints](https://shiny.posit.co/py/get-started/debug.html#breakpoints). See the [debugging](https://shiny.posit.co/py/get-started/debug.html) page for more details.

### Command line [Anchor](https://shiny.posit.co/py/get-started/create-run.html\#command-line)

To run a Shiny app from the command line, use the `shiny run` command. The required argument is the path to your app’s entry point, usually a Python file like `app.py`.

You can also include optional flags to improve your development experience. For example, if your app’s entry point is `app.py` inside a folder called `app_dir`, you can run:

```bash
shiny run --reload --launch-browser app_dir/app.py
```

This will start the app and open it in your default web browser.

- The `--reload` flag enables automatic reloading. When you save changes to your source files, the app will automatically restart and update in the browser.
- The `--launch-browser` flag opens the app in a browser as soon as it starts.
