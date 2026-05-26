It’s often useful to programmatically update the UI based on user input or other server-side state. Shiny provides several mechanisms for doing this, including conditional UI, updating inputs, and dynamic UI. Amongst these [dynamic UI](https://shiny.posit.co/py/docs/ui-dynamic.html#dynamic-ui) is the most general and powerful, but also comes with the most overhead.

### Conditional UI [Anchor](https://shiny.posit.co/py/docs/ui-dynamic.html\#conditional-ui)

The most basic way to create dynamic UIs is by conditionally hiding a UI element on the client side. `ui.panel_conditional()` enables this by showing/hiding UI based on a JavaScript condition. This condition can reference input values, and can be used to make any sort of UI conditional.

app.py+

9

1

2

3

4

5

6

7

8

from shiny.express import ui

ui.input\_radio\_buttons("display", None, \["hidden", "shown"\], inline=True)

\# The 1st string is a JavaScript condition, and the child UI is shown if it's truthy

\# NOTE: JS input values are read via \`input\[id\]\`, not \`input\[id\]()\`

with ui.panel\_conditional("input.display === 'shown'"):

"Hidden content"

### Updating inputs [Anchor](https://shiny.posit.co/py/docs/ui-dynamic.html\#updating-inputs)

In addition to hiding elements on the client side, you can also update input elements from the server. This is used in cases where you want to change on part of an input without regenerating it entirely. For example you might want to change `ui.input_select` choices when a user takes a particular action.

app.py+

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

from shiny import reactive

from shiny.express import input, ui

CHOICES = {

"lower": \["a", "b", "c"\],

"upper": \["A", "B", "C"\]

}

ui.input\_switch("uppercase", "Uppercase choices", value=False)

ui.input\_selectize("x", None, choices=CHOICES\["lower"\])

@reactive.effect

def\_():

choices = "upper"if input.uppercase() else"lower"

ui.update\_selectize("x", choices=CHOICES\[choices\])

### Dynamic UI [Anchor](https://shiny.posit.co/py/docs/ui-dynamic.html\#dynamic-ui)

Finally, `@render.ui` lets you generate UI element(s) entirely on the server, which is an extremely flexible way to dynamically generate UIs. This is the most general mechanism for dynamic UI, but also comes with the most overhead.

app.py+

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

from shiny.express import input, render, ui

ui.input\_text("message", "Message", value="Hello, world!")

ui.input\_checkbox\_group(

"styles", "Styles",

choices=\["Bold", "Italic"\],

selected=\["Bold"\],

inline=True

)

@render.ui

defresult():

x = input.message()

if"Bold"in input.styles():

x = ui.strong(x)

if"Italic"in input.styles():

x = ui.em(x)

return x

Render UI vs display

Shiny Express code that works via side-effects needs to be used with `@render.express`, not `@render.ui`. See [this section](https://shiny.posit.co/py/docs/express-in-depth.html#reactive-displays) to learn more.

Tip

Anything that’s statically renderable can also be rendered dynamically (e.g., `ui.markdown()`, `ui.HTML()`, `ui.div()`, inputs, outputs, etc).

Dynamic UI vs. updating inputs vs. conditional UI

Dynamic UI is a more general mechanism than the updating inputs and conditional UI patterns, and can be used to update any UI component(s) (not just inputs). However, updating inputs is more efficient than dynamic UI, and should be preferred where possible.