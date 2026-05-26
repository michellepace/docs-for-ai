In the previous article, we learned the foundations of reactive programming in Shiny. Here we’ll learn about some useful utilities that make reactive programming easier in certain situations.

- [Isolation & Events](https://shiny.posit.co/py/docs/reactive-patterns.html#isolate-events)
  - Ignore changes in certain reactive dependencies.
- [Requiring input](https://shiny.posit.co/py/docs/reactive-patterns.html#req)
  - Require an input before executing a reactive function.
- [Scheduled invalidation](https://shiny.posit.co/py/docs/reactive-patterns.html#invalidate-later)
  - Invalidate a reactive function on a schedule.
- [Reactive file reading](https://shiny.posit.co/py/docs/reactive-patterns.html#file)
  - Invalidate a reactive function when a file changes.
- [Reactive polling](https://shiny.posit.co/py/docs/reactive-patterns.html#poll)
  - Periodically check for changes to a reactive dependency.

## Isolation & Events [Anchor](https://shiny.posit.co/py/docs/reactive-patterns.html\#isolate-events)

Normally, a reactive function re-executes when _any_ of its reactive dependencies change. Sometimes this leads to a function re-executing too often. Shiny provides two ways to ignore changes in reactive dependencies: `@reactive.event()` and `with isolate()`. The former is more convenient when you want “event-like” behavior (i.e., do something on button click).

For example, suppose we have an output that depends on the value of a slider, but is computationally expensive. We might want it to re-execute it only when the user presses a button. In other words, we want to ignore changes in the slider until the button is pressed. The more idiomatic way to do this is with `@reactive.event()`:

- reactive.event
- reactive.isolate

The `@reactive.event()` decorator restricts re-execution to only changes in one (or more) reactive dependency. Any other reactive dependencies inside the function being decorated are ignored.

app.py:

```python
import asyncio
from shiny import reactive
from shiny.express import input, render, ui

ui.input_slider("n", "N", min=1, max=100, value=1)
ui.input_action_button("compute", "Compute!")

@render.text
@reactive.event(input.compute) # Take a dependency on the button
async def result():
    # Any reactive dependencies inside this function are ignored.
    await asyncio.sleep(2) # Simulate a long computation
    return f"Result: {input.n()}"
```

Note

In the `@reactive.event()` example above, the function does _not_ execute the first time when the session starts; it will wait until the user presses the button. If you want it to execute once when the session starts, you can use `@reactive.event(input.compute, ignore_none=False)`.

Using `with isolate()`, a block of code is run inside a reactive function, but without taking a reactive dependency on the code inside the block. This means that any reactive inputs in that block will not cause the function to re-execute. In the example below, the `result` takes a dependency on `input.button()`, but not `input.n()`:

## Requiring input [Anchor](https://shiny.posit.co/py/docs/reactive-patterns.html\#req)

When input must be provided or a certain condition must be met before displaying output, you can use `req()` to effectively stop execution for the current reactive cycle. For example, the app below allows a user to upload a csv file, which is then used to render a table. Notice how the reactive calculation, `df`, uses `req()` to stop execution until the user has uploaded a file.

```python
import pandas as pd
from shiny import reactive, req
from shiny.express import input, render, ui

ui.input_file("file", "Upload a csv file", accept=".csv")

@reactive.calc
def df():
    # req() stops execution until input.file() is truthy
    f = req(input.file())
    return pd.read_csv(f[0]['datapath'])

@render.data_frame
def table():
    # Output won't render until input.file() is truthy
    return render.DataGrid(df())Edit in Shinylive
```

[Video](https://shiny.posit.co/py/docs/assets/file-upload.mp4)

A gif of uploading a csv file and seeing the text and table outputs update

## Scheduled invalidation [Anchor](https://shiny.posit.co/py/docs/reactive-patterns.html\#invalidate-later)

To repeatedly invalidate a reactive function on a schedule, use `reactive.invalidate_later()`. This is useful for implementing things like streaming data, or updating a clock. For example, to implement a clock that updates every second, you can use `reactive.invalidate_later(1)`:

app.py:

```python
from datetime import datetime
from shiny import reactive
from shiny.express import render

# Get the current time every second
@reactive.calc
def cur_time():
    reactive.invalidate_later(1)
    return datetime.now().strftime('%H:%M:%S')

@render.ui
def clock():
    return f"Current time: {cur_time()}"
```

## Reactive file reading [Anchor](https://shiny.posit.co/py/docs/reactive-patterns.html\#file)

If your app reads input files, you can use `@reactive.file_reader()` to invalidate the result when the file changes. For example, lets extend the example from above to write the current time to a file every second, and then read and display the contents of that file:

app.py:

```python
from datetime import datetime
from shiny import reactive
from shiny.express import render

# Get the current time every second
@reactive.calc
def cur_time():
    reactive.invalidate_later(1)
    return datetime.now().strftime('%H:%M:%S')

# Write cur_time() to a file (every second)
@reactive.effect
def _():
    with open("time.txt", "w") as f:
        f.write(cur_time())

f = open("time.txt", "w")  # Create the file if it doesn't exist

# Read and display whenever the file changes
@render.ui
@reactive.file_reader("time.txt")
def time():
    with open("time.txt") as f:
        return f"Current time {f.read()}"
```

More compelling example

See [here](https://github.com/posit-dev/py-shiny-templates/blob/main/monitor-file/app-core.py) for a more compelling example of monitoring a file for changes.

## Reactive polling [Anchor](https://shiny.posit.co/py/docs/reactive-patterns.html\#poll)

Sometimes it’s useful to invalidate a reactive function on a schedule, but only _if a certain condition is met_. For example, suppose we want to check if a (potentially large) file (or database) has changed/updated every so often, and if it has, re-read it. The `@reactive.poll()` decorator is designed for this purpose. When applying the decorator, make sure to provide a function that is relatively cheap to execute, since it will be executed repeatedly on an interval. And, in the event that that function’s value changes, the reactive function will be invalidated and re-executed.

For example, lets extend the example from above to write the current time to a file every 0.5 seconds, but only read and display the contents every 2 seconds:

app.py:

```python
import os
from datetime import datetime
from shiny import reactive
from shiny.express import input, render, ui

# Get the current time every 0.5 seconds
@reactive.calc
def cur_time():
    reactive.invalidate_later(0.5)
    return datetime.now().strftime('%H:%M:%S')

# Write cur_time() to a file (every 0.5 seconds)
@reactive.effect
def _():
    with open("time2.txt", "w") as f:
        f.write(cur_time())

f = open("time2.txt", "w")  # Create the file if it doesn't exist

# Every 2 seconds, check if the file has changed.
# If it has, re-read it, and display the contents.
# Note: checking for the modified time of a file is cheap
# compared to reading the file contents
@render.ui
@reactive.poll(lambda: os.path.getmtime("time2.txt"), 2)
def time():
    with open("time2.txt") as f:
        return f"Current time {f.read()}"
```

Monitoring a database / folder

See [here](https://github.com/posit-dev/py-shiny-templates/blob/main/monitor-database/app-core.py) for an example of monitoring a database for changes.

See [here](https://github.com/posit-dev/py-shiny-templates/blob/main/monitor-folder/app-core.py) for an example of monitoring a folder for changes.
