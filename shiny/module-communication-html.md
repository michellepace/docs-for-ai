On this page

## Communication between modules [Anchor](https://shiny.posit.co/py/docs/module-communication.html\#communication-between-modules)

Once you start breaking your app into modules, you might wonder how to pass values between your module and the rest of the application. For example, you might want to define an input label in the global application scope and pass that label to the module, or have user interactions with one module affect an output of another module. Since modules are just functions with a specific namespace, they can take and return both reactive and non-reactive arguments, which gives you a rich set of tools for handling application requirements.

There are four main patterns you should be aware of when building Shiny modules:

1. Modules that take non-reactive arguments
2. Passing callbacks to modules
3. Modules that take reactive arguments
4. Modules that return reactive arguments

## Non-reactive arguments [Anchor](https://shiny.posit.co/py/docs/module-communication.html\#non-reactive-arguments)

The easiest way to communicate with modules is to pass non-reactive arguments to them. This is just like passing an argument to a normal Python function, and allows you to set specific module options. For example, say we wanted a counter module which allowed you to set the label and starting value.

- Express
- Core

To create the module, use the `@module` decorator on a function and give it two additional parameters, `label` and `starting value`.

```
from shiny import reactive
from shiny.express import module, ui, render

@module
def counter_module(input, output, session, label="Increment counter", starting_value=0):
    count = reactive.value(starting_value)
    with ui.card():
        ui.card_header("This is " + label)
        ui.input_action_button(id="button", label=label)

        @render.code
        def out():
            return f"Click count is {count()}"

    @reactive.effect
    @reactive.event(input.button)
    def _():
        count.set(count() + 1)
```

You can then pass in values when you call the module in your app. Note that you always need to provide an `id` to the module function to define its namespace. Using arguments like this makes your modules much more flexible and allows you to encapsulate some of the logic while maintaining the flexibility that your application needs.

app.py×counter.py×+

9

1

2

3

4

5

6

from shiny.express import ui

from .counter import counter\_module

counter\_module("counter1", "Counter 1", starting\_value=5)

counter\_module("counter2", "Counter 2", starting\_value=3)

Note

Note that in the example above we used the relative import `from .counter import ...` instead of the absolute import `from counter import ...`. This is necessary when running multiple Shinylive applications on one web page as we do here, so that different apps do not cause conflicts when importing their own `counter` modules. In normal Shiny Express applications, you can use either a relative or absolute import.

To do this, you would first add an argument to the module UI function which sets the button label.

```
from shiny import module, ui, render, reactive, event, App

@module.ui
def counter_ui(custom_label = "Increment counter"):
    return ui.card(
        ui.h2("This is ", custom_label),
        ui.input_action_button(id="button", label=custom_label),
        ui.output_code(id="out"),
    )
```

Next, you would add an argument to the server function which specifies the starting value for the counter.

```
@module.server
def counter_server(input, output, session, starting_value = 0):
    count =  reactive.value(starting_value)

    @reactive.effect
    @reactive.event(input.button)
    def _():
        count.set(count() + 1)

    @render.code
    def out():
        return f"Click count is {count()}"
```

You can then set the options when you call the module in your app. Note that you always need to provide an `id` to the module function to define its namespace. Using arguments like this makes your modules much more flexible and allows you to encapsulate some of the logic while maintaining the flexibility that your application needs.

app.py×counter.py×+

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

14

15

16

17

18

19

from shiny import App, ui

\# Note: In a normal Shiny Core app, use an absolute import, as in:

\# \`from counter import ...\`

from .counter import counter\_ui, counter\_server

app\_ui = ui.page\_fluid(

counter\_ui("counter1", "Counter 1"),

counter\_ui("counter2", "Counter 2"),

)

defserver(input, output, session):

counter\_server("counter1", starting\_value=5)

counter\_server("counter2", starting\_value=3)

app = App(app\_ui, server)

Note

Note that in the example above we used the relative import `from .counter import ...` instead of the absolute import `from counter import ...`. This is necessary when running multiple Shinylive applications on one web page as we do here, so that different apps do not cause conflicts when importing their own `counter` modules. In normal Shiny Core applications, you must use the absolute import (relative imports will generally not work with Shiny Core applications).

## Passing multiple UI elements to modules [Anchor](https://shiny.posit.co/py/docs/module-communication.html\#passing-multiple-ui-elements-to-modules)

In addition to passing numeric and string values to modules you can also pass any number of UI elements. This allows you to build layout modules similar to `ui.sidebar_layout()` which can take arbitrary Shiny elements and arrange them in some fashion.

- Express
- Core

There are two sides to modules: a module can be _written_ with Shiny Express or Core syntax, and a module can be _used_ from a Shiny Express or Core application. In this section we’ll learn about both using and writing modules with Shiny Express.

If a module used from within a Shiny Express application, you can pass it UI elements, but doing so requires understanding how UI elements work in Shiny Express.

Suppose you want to use a module called `table_cards_module()`. We’ll just provide the signature here (the implementation will be later). If you want it to accept multiple arguments, they can be passed in as a list:

```
@module
def my_module(input, output, session, elements):
    for el in elements:
        with ui.card():
            el

my_module("mod1", [ui.h1("heading"), ui.p("paragraph")])
```

Notice that in order to display the elements that the user passed in, we just used a `for` loop and evaluated each element. This is similar to how you would print each item in a Jupyter notebook.

Another method is to have your module take non-keyword argument with `*args`. With this method, you don’t have two wrap the elements in a list when using the module:

```
@module
def my_module(input, output, session, *elements):
    for el in elements:
        with ui.card():
            el

my_module("mod1", ui.h1("heading"), ui.p("paragraph"))
```

For example, let’s say we wanted to display two cards, one which displayed a standard table, and the other displaying an arbitrary set of elements. One way we could do this is by writing a module which rendered a table in one card and passed `*args` to a second card.

app.py×modules.py×+

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

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

import matplotlib.pyplot as plt

import numpy as np

from .modules import table\_cards

from shiny.express import input, render, ui

text\_tags = \[ui.h1("A heading"), ui.p("Some paragraph text")\]

\# The ui.hold prevents the plot from being placed on the page here,

\# but the dot\_plot object can later be passed to the table\_cards() module.

with ui.hold():

@render.plot

defdot\_plot():

x = np.random.rand(input.dots())

y = np.random.rand(input.dots())

fig, ax = plt.subplots()

ax.scatter(x, y)

return fig

reactive\_tags = \[\
\
ui.input\_numeric("dots", "Number of points", value=25),\
\
dot\_plot\
\
\]

table\_cards("output\_example", reactive\_tags),

table\_cards("heading\_example", text\_tags),

There are two main ways to pass multiple UI elements to a module. First, you can have the module take a list as one of the arguments and pass that list to another container function.

```
@module.ui
def mod_ui(elements):
    return ui.div(elements)

ui = ui.page_fluid(mod_ui([ui.h1("heading"), ui.p("paragraph")]))
```

This is convenient because it lets the parent context pass in any number of elements to the module, but requires that you wrap the elements in a list before passing them to the module.

The second method is to have your module take non keyword argument with `*args`. This is how Shiny’s container functions are designed, and using this pattern lets you to call the module UI just like you would any Shiny function.

```
@module.ui
def mod_ui(*args):
    return ui.div(*args)

ui = ui.page_fluid(mod_ui(ui.h1("heading"), ui.p("paragraph")))
```

For example, let’s say we wanted to display two cards, one which displayed a standard table, and the other displaying an arbitrary set of elements. One way we could do this is by writing a module which rendered a table in one card and passed `*args` to a second card.

app.py×modules.py×+

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

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

import matplotlib.pyplot as plt

import numpy as np

from .modules import table\_cards\_server, table\_cards\_ui

from shiny import App, render, ui

text\_tags = \[ui.h1("A heading"), ui.p("Some paragraph text")\]

reactive\_tags = \[\
\
ui.input\_numeric("dots", "Number of points", value=25), ui.output\_plot("dot\_plot")\
\
\]

app\_ui = ui.page\_fluid(

table\_cards\_ui("output\_example", reactive\_tags),

table\_cards\_ui("heading\_example", text\_tags),

)

defserver(input, output, session):

@render.plot

defdot\_plot():

x = np.random.rand(input.dots())

y = np.random.rand(input.dots())

fig, ax = plt.subplots()

ax.scatter(x, y)

return fig

table\_cards\_server("heading\_example")

table\_cards\_server("output\_example")

app = App(app\_ui, server)

## Passing reactives to modules [Anchor](https://shiny.posit.co/py/docs/module-communication.html\#passing-reactives-to-modules)

The modules we’ve seen so far are useful for cleaning up your code base, but we can do more to integrate them in an application’s reactive structure. For example, what if we wanted a global button which reset all of the counters in an application? To accomplish this, we can pass reactive objects and use them inside the module just as you would use them in an app.

Important

It is important to distinguish between calls to reactive objects like `input.n()` and the reactive object itself, `input.n`. While `input.n` is reactive object, calling `input.n()` returns the current value that object.

- Express
- Core

app.py×modules.py×+

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

from shiny import reactive

from shiny.express import input, render, ui

from .modules import counter

with ui.card():

ui.input\_action\_button("clear", "Clear counters")

counter("counter1", starting\_value=5, global\_clear=input.clear, label="Counter 1")

counter("counter2", starting\_value=3, global\_clear=input.clear, label="Counter 2")

While this app may look it’s doing something quite different, it’s actually following the same reactive rules as any other app. When we pass `input.clear` to each module as the `global_clear` parameter, we can use it inside the module just like we would use any other reactive object. You could retrieve its value with `global_clear()` or use it with `@reactive.event(global_clear)` to trigger a side effect. Since all of the module instances are receiving the same reactive object, when that object is invalidated, it will cause elements within those modules to invalidate and re-execute.

app.py×modules.py×+

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

14

15

16

17

18

from shiny import App, module, reactive, render, ui

from .modules import counter\_ui, counter\_server

app\_ui = ui.page\_fluid(

ui.input\_action\_button("clear", "Clear counters"),

counter\_ui("counter1", "Counter 1"),

counter\_ui("counter2", "Counter 2"),

)

defserver(input, output, session):

counter\_server("counter1", starting\_value=5, global\_clear=input.clear)

counter\_server("counter2", starting\_value=3, global\_clear=input.clear)

app = App(app\_ui, server)

While this app may look it’s doing something quite different, it’s actually following the same reactive rules as any other app. When we pass `input.clear` to each module as the `global_clear` parameter, we can use it inside the module just like we would use any other reactive object. You could retrieve its value with `global_clear()` or use it with `@reactive.event(global_clear)` to trigger a side effect. Since all of the module instances are receiving the same reactive object, when that object is invalidated, it will cause elements within those modules to invalidate and re-execute.

## Passing callbacks to modules [Anchor](https://shiny.posit.co/py/docs/module-communication.html\#passing-callbacks-to-modules)

Another common problem with modules is to change some piece of application state from within the module. One intuitive way to do this is to define a state-modifying function at the application level, and pass that function down to the module. When the function is called within the module code, it will update the global application state.

For example, let’s add a text output that adds up the total number of button clicks for a session. To do this we create a `reactive.value` and a function which increments that value by one. We then pass this function down to the module and call it whenever the module button is clicked. This updates the `reactive.value` at the application level.

- Express
- Core

app.py×modules.py×+

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

14

15

16

17

18

from shiny import reactive

from shiny.express import input, render, ui

from .modules import counter

global\_tally = reactive.value(0)

defincrement\_counter():

global\_tally.set(global\_tally() + 1)

with ui.card():

@render.text

deftotal\_counts():

returnf"Total counts: {global\_tally()}"

counter("counter1", \_on\_click=increment\_counter, label="Counter 1")

counter("counter2", \_on\_click=increment\_counter, label="Counter 2")

app.py×modules.py×+

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

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

from shiny import App, module, reactive, render, ui

from .modules import counter\_ui, counter\_server

app\_ui = ui.page\_fluid(

ui.output\_text("total\_counts"),

ui.br(),

counter\_ui("counter1", "Counter 1"),

counter\_ui("counter2", "Counter 2"),

)

defserver(input, output, session):

global\_tally = reactive.value(0)

defincrement\_counter():

global\_tally.set(global\_tally() + 1)

@render.text

deftotal\_counts():

returnf"Total counts: {global\_tally()}"

counter\_server("counter1", \_on\_click=increment\_counter)

counter\_server("counter2", \_on\_click=increment\_counter)

app = App(app\_ui, server)

We could accomplish the same thing by passing the reactive value itself down to the module, and while this works, it’s not a great idea. Passing the reactive value creates a tight coupling between the module and the particular context in which it was called. The module would be expecting a particular type of reactive value and wouldn’t work for anything else. Additionally the update logic would be split between the application context and the module which makes it harder to reason about. Passing a callback is more flexible because the module can be used to do a variety of things. For example, by passing a different callback you could use the same module in another application which did something else when the button was clicked.

## Returning reactives from modules [Anchor](https://shiny.posit.co/py/docs/module-communication.html\#returning-reactives-from-modules)

Just like we can pass reactives to modules and use them inside the module code we can also _return_ reactive objects from modules to use them in the larger application. For example, one common form of dynamic user interface is to populate a drop-down menu based on another drop-down. You might have one menu which lets the user select a state, and a second which only shows cities in that state. To make it a reusable component, you can extract it into a module so that it could be easily added into other applications.

- Express
- Core

To do this, you can have the module function return one of the reactive objects which are defined in the module. This reactive object can then be used in the application context like any other reactive object.

app.py×modules.py×+

9

1

2

3

4

5

6

7

8

9

from shiny.express import render, ui

from .modules import city\_state

city = city\_state("cities")

@render.text

defselected\_city():

returnf"You selected '{city()}'"

To do this, you can have the module’s server function return one of the reactive objects which are defined in the module. This reactive object can then be used in the application context like any other reactive object.

app.py×modules.py×+

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

14

15

16

from shiny import App, render, ui

from .modules import city\_state\_ui, city\_state\_server

app\_ui = ui.page\_fluid(city\_state\_ui("cities"), ui.output\_text("selected\_city"))

defserver(input, output, session):

city = city\_state\_server("cities")

@render.text

defselected\_city():

returnf"You selected '{city()}'"

app = App(app\_ui, server)

### Multiple returns [Anchor](https://shiny.posit.co/py/docs/module-communication.html\#multiple-returns)

Sometimes you may want to retrieve multiple reactive objects from the module context. To do this you can use either a `tuple` or `namedtuple` to send multiple reactives from a module to another context. For example, if you wanted to retrieve both the city and state reactives from the module could you have the module return both of them with `return (input.cities, input.state)`. This tuple could then be unpacked in the application context with `city, state = city_state_server("cities")`.

- Express
- Core

app.py×modules.py×+

9

1

2

3

4

5

6

7

8

9

from shiny.express import render, ui

from .modules import city\_state

(city, state) = city\_state("cities")

@render.text

defselected\_city():

returnf"You selected '{city()}' in '{state()}'"

app.py×modules.py×+

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

14

15

16

from shiny import App, render, ui

from .modules import city\_state\_ui, city\_state\_server

app\_ui = ui.page\_fluid(city\_state\_ui("cities"), ui.output\_text("selected\_city"))

defserver(input, output, session):

(city, state) = city\_state\_server("cities")

@render.text

defselected\_city():

returnf"You selected '{city()}' in '{state()}'"

app = App(app\_ui, server)

If your return value has more objects, it may be useful to return a [namedtuple](https://realpython.com/python-namedtuple/). Named tuples are similar to tuples except that they allow you to set specific named attributes, which makes them useful for data validation because if you don’t pass the right attributes to a named tuple it will fail early and loudly.

## Using modules with Shiny Core and Express syntax [Anchor](https://shiny.posit.co/py/docs/module-communication.html\#using-modules-with-shiny-core-and-express-syntax)

In all the examples we’ve seen so far, a Shiny Express app uses modules created with Shiny Express syntax, or a Shiny Core app uses modules created with Shiny Core syntax. It is also possible for an Express app to use a module written with Core syntax. To do so, in your Express app, simply call both the UI and server components of the Core-syntax module.

This is a Shiny Express app which illustrates how to use both types of modules: one written with Express syntax, and the other written with Core syntax.

app.py×counter\_express.py×counter\_core.py×+

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

\# This Shiny Express app illustrates how to use modules with Express and Core syntax

from shiny.express import ui

from .counter\_express import counter\_express

from .counter\_core import counter\_server, counter\_ui

\# Use a module that was made with Shiny Express syntax

counter\_express("counter1", label="Counter 1 (Express)", starting\_value=5)

\# Use a module that was made with Shiny Core syntax: Call the ui and server components

\# with the same \`id\`, and pass in any additional arguments.

counter\_ui("counter2", label="Counter 2 (Core)")

counter\_server("counter2", starting\_value=2)

## Conclusion [Anchor](https://shiny.posit.co/py/docs/module-communication.html\#conclusion)

Modules are the main way to grow and scale your Shiny application code. They let you break up your app into tractable parts, define how those parts communicate with one another, and reuse components across applications. While mastering modules takes quite a bit of time, you can accomplish almost anything with the four patterns listed in this article.