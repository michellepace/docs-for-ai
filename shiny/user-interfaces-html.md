With Shiny, you can create a wide variety of user interfaces (UI), including dashboards. Here, we’ll use the following dashboard as motivation to learn about some important UI components (e.g., [cards](https://shiny.posit.co/py/docs/user-interfaces.html#cards), [value boxes](https://shiny.posit.co/py/docs/user-interfaces.html#value-boxes)) and layouts (e.g., [columns](https://shiny.posit.co/py/docs/user-interfaces.html#multi-column-layout)).

![](https://shiny.posit.co/py/docs/assets/tipping-dashboard.png)

A Shiny dashboard with visuals for exploring restaurant tips (see [here](https://shiny.posit.co/py/docs/user-interfaces.html#all-together-now) for the code).

More UI design inspiration

See the [gallery](https://shiny.posit.co/py/gallery), [layouts](https://shiny.posit.co/py/layouts), and [components](https://shiny.posit.co/py/components) for more UI design inspiration.

## Basic dashboard [Anchor](https://shiny.posit.co/py/docs/user-interfaces.html\#basic-dashboard)

Before we walk through a more sophisticated dashboard, consider this basic dashboard with a header (i.e., page title) and a sidebar layout. In the sidebar, there are a couple [inputs](https://shiny.posit.co/py/components/#inputs) for getting different views of the data, and in the main content area, is a [plotly output](https://shiny.posit.co/py/docs/jupyter-widgets.html). That output is also placed in a card to give it some depth and the ability to go full screen. The card isn’t critical when there is only one output, but they come highly recommended when there are multiple outputs to display.

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

from shiny.express import input, render, ui

from shinywidgets import render\_plotly

ui.page\_opts(title="Penguins dashboard", fillable=True)

with ui.sidebar():

ui.input\_selectize(

"var", "Select variable",

\["bill\_length\_mm", "bill\_depth\_mm", "flipper\_length\_mm", "body\_mass\_g", "year"\]

)

ui.input\_numeric("bins", "Number of bins", 30)

with ui.card(full\_screen=True):

@render\_plotly

defhist():

import plotly.express as px

from palmerpenguins import load\_penguins

return px.histogram(load\_penguins(), x=input.var(), nbins=input.bins())

## Sophisticated dashboard [Anchor](https://shiny.posit.co/py/docs/user-interfaces.html\#sophisticated-dashboard)

Now let’s work up to a more sophisticated dashboard by walking through components and layouts that are useful for dashboards step-by-step.

### Sidebar layout [Anchor](https://shiny.posit.co/py/docs/user-interfaces.html\#sidebar-layout)

Create a sidebar layout by giving content to `ui.sidebar()`. It’s usually a good idea to place [inputs](https://shiny.posit.co/py/components/#inputs) in the sidebar and [outputs](https://shiny.posit.co/py/components/#outputs) in the main content area.

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

ui.page\_opts(title = "Title")

with ui.sidebar():

"Sidebar (input)"

"Main content (output)"

Multi-page apps

To create a sidebar layout with multiple pages, just put each page’s content in a top-level `ui.nav_panel()`, as shown [here](https://shiny.posit.co/py/docs/overview.html#layouts).

### Cards [Anchor](https://shiny.posit.co/py/docs/user-interfaces.html\#cards)

Cards are great for visually grouping together related content, and it’s best practice to place related components together in a card. Here you’ll also have an opportunity to add a header, footer, add `full_screen` capability, and more. As we’ll see later, cards are also useful for making outputs stand out from one another when there are multiple outputs to display.

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

from shiny.express import render, ui

with ui.card(full\_screen=True):

ui.card\_header("A card with a header")

@render.plot

defplot():

import matplotlib.pyplot as plt

return plt.scatter(\[1, 2, 3\], \[4, 5, 6\])

with ui.card():

ui.markdown("Another card with some \_markdown\_.")

### Value boxes [Anchor](https://shiny.posit.co/py/docs/user-interfaces.html\#value-boxes)

Value boxes are great for highlighting important summaries. They require at least two values (the title and value) and also support a `showcase` argument for adding a visual representation of the value. The `showcase` argument can technically be any UI element, but is often a [faicons](https://github.com/posit-dev/py-faicons) (i.e., [fontawesome](https://fontawesome.com/)) icon.

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

from shiny.express import render, ui

from faicons import icon\_svg as icon

with ui.value\_box(showcase=icon("piggy-bank")):

"Total sales"

"$1,000,000"

with ui.value\_box(showcase=icon("person")):

"Total customers"

@render.ui

defcustomers():

returnf"{1000:,}"

Note

Under the hood, value boxes are built on cards, so you can leverage similar options like `full_screen`.

### Multi-column layout [Anchor](https://shiny.posit.co/py/docs/user-interfaces.html\#multi-column-layout)

Create a multi-column layout based on a 12-column grid system by using `ui.layout_columns()`. By default, an intelligent equal-width layout is created, but each column width can be specified (in units of 1/12) using `col_widths`:

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

9

from shiny.express import ui

with ui.layout\_columns(col\_widths=\[6, 6, 12\]):

with ui.card():

"Card 1"

with ui.card():

"Card 2"

with ui.card():

"Card 3"

Responsive layout

By default, `col_widths` doesn’t apply on smaller width (i.e., mobile) screens (in that case, columns go full-width). However, `col_widths` also accepts a dictionary of column widths for different screen sizes (e.g., `col_widths=dict(sm=6, md=4)` yields 2 columns on small screens and 3 columns on medium (or larger) screens).

### Filling layout [Anchor](https://shiny.posit.co/py/docs/user-interfaces.html\#filling-layout)

Set `ui.page_opts(fillable=True)` to encourage content to fill the screen. Many of Shiny’s layouts and components automatically fill the screen when this option is set, which is often desirable for dashboards, but may not be what you want for things like value boxes or cards with a textual description. You can override the filling behavior on a per-component basis by setting `fill=False` or by specifying a `height`:

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

from shiny.express import ui

ui.page\_opts(fillable = True)

with ui.layout\_column\_wrap(fill=False):

with ui.value\_box():

"Value box"

"$1,000,000"

with ui.value\_box():

"Value box"

"$1,000,000"

with ui.card():

"Card that fills remaining space..."

Resizable viewer

Did you know the app viewer above is resizable? Try resizing it to see how the layout responds (the card fills the remaining space).

### Tooltips and popovers [Anchor](https://shiny.posit.co/py/docs/user-interfaces.html\#tooltips-and-popovers)

Tooltips and popovers are a useful means for both displaying and interacting with additional information in a non-obtrusive way. Tooltips are shown on hover, whereas popovers are shown on click, making them more suitable for interactive content like inputs. In the [actual dashboard](https://shiny.posit.co/py/docs/user-interfaces.html#all-together-now), we’ll leverage a popover to effectively add a toolbar with additional inputs controls to card headers.

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

from shiny.express import ui

from faicons import icon\_svg as icon

"Hover this icon: "

with ui.tooltip():

icon("circle-info")

"Tooltip message"

ui.br()

"Click this icon: "

with ui.popover(title="Popover title"):

icon("circle-info")

"Popover message"

### All together now [Anchor](https://shiny.posit.co/py/docs/user-interfaces.html\#all-together-now)

Let’s put it all together to create a dashboard for exploring restaurant tipping data.

Here we use a [sidebar](https://shiny.posit.co/py/docs/user-interfaces.html#sidebar-layout) to hold our “global” inputs, and place outputs in [cards](https://shiny.posit.co/py/docs/user-interfaces.html#cards). These cards are laid out [column-wise](https://shiny.posit.co/py/docs/user-interfaces.html#multi-column-layout), and [value boxes](https://shiny.posit.co/py/docs/user-interfaces.html#value-boxes) highlight the most important numbers. Finally, inputs that are specific to each are placed in a [popover](https://shiny.posit.co/py/docs/user-interfaces.html#tooltips-and-popovers) so that they are unobtrusive and don’t distract the user from the main application content.

app.py×requirements.txt×+

999

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

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

77

78

79

80

81

82

83

84

85

86

87

88

89

90

91

92

93

94

95

96

97

98

99

100

101

102

103

104

105

106

107

108

109

110

111

112

113

114

115

116

117

118

119

120

121

122

123

124

125

126

127

128

129

130

131

132

133

134

135

136

137

138

139

import faicons as fa

import plotly.express as px

from shinywidgets import render\_plotly

from shiny import reactive, render, req

from shiny.express import input, ui

\# Load data and compute static values

tips = px.data.tips()

bill\_rng = (min(tips.total\_bill), max(tips.total\_bill))

\# Add page title and sidebar

ui.page\_opts(title="Restaurant tipping", fillable=True)

with ui.sidebar(open="desktop"):

ui.input\_slider("total\_bill", "Bill amount", min=bill\_rng\[0\], max=bill\_rng\[1\], value=bill\_rng, pre="$")

ui.input\_checkbox\_group("time", "Food service", \["Lunch", "Dinner"\], selected=\["Lunch", "Dinner"\], inline=True)

ui.input\_action\_button("reset", "Reset filter")

\# Add main content

ICONS = {

"user": fa.icon\_svg("user", "regular"),

"wallet": fa.icon\_svg("wallet"),

"currency-dollar": fa.icon\_svg("dollar-sign"),

"gear": fa.icon\_svg("gear")

}

with ui.layout\_columns(fill=False):

with ui.value\_box(showcase=ICONS\["user"\]):

"Total tippers"

@render.express

deftotal\_tippers():

tips\_data().shape\[0\]

with ui.value\_box(showcase=ICONS\["wallet"\]):

"Average tip"

@render.express

defaverage\_tip():

d = tips\_data()

if d.shape\[0\] \> 0:

perc = d.tip / d.total\_bill

f"{perc.mean():.1%}"

with ui.value\_box(showcase=ICONS\["currency-dollar"\]):

"Average bill"

@render.express

defaverage\_bill():

d = tips\_data()

if d.shape\[0\] \> 0:

bill = d.total\_bill.mean()

f"${bill:.2f}"

with ui.layout\_columns(col\_widths=\[6, 6, 12\]):

with ui.card(full\_screen=True):

ui.card\_header("Tips data")

@render.data\_frame

deftable():

return render.DataGrid(tips\_data())

with ui.card(full\_screen=True):

with ui.card\_header(class\_="d-flex justify-content-between align-items-center"):

"Total bill vs tip"

with ui.popover(title="Add a color variable", placement="top"):

ICONS\["gear"\]

ui.input\_radio\_buttons(

"scatter\_color", None,

\["none", "sex", "smoker", "day", "time"\],

inline=True

)

@render\_plotly

defscatterplot():

color = input.scatter\_color()

return px.scatter(

tips\_data(),

x="total\_bill",

y="tip",

color=Noneif color == "none"else color,

trendline="lowess"

)

with ui.card(full\_screen=True):

with ui.card\_header(class\_="d-flex justify-content-between align-items-center"):

"Tip percentages"

with ui.popover(title="Add a color variable"):

ICONS\["gear"\]

ui.input\_radio\_buttons(

"tip\_perc\_y", "Split by:",

\["sex", "smoker", "day", "time"\],

selected="day",

inline=True

)

@render\_plotly

deftip\_perc():

from ridgeplot import ridgeplot

\# Must make a copy of this pandas dataframe before we mutate it!

\# See https://shiny.posit.co/py/docs/reactive-mutable.html

dat = tips\_data().copy()

dat\["percent"\] = dat.tip / dat.total\_bill

yvar = input.tip\_perc\_y()

uvals = dat\[yvar\].unique()

samples = \[\
\
\[ dat.percent\[dat\[yvar\] == val\] \]\
\
for val in uvals\
\
\]

plt = ridgeplot(

samples=samples, labels=uvals, bandwidth=0.01,

colorscale="viridis", colormode="row-index"

)

plt.update\_layout(

legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)

)

return plt

\# --------------------------------------------------------

\# Reactive calculations and effects

\# --------------------------------------------------------

@reactive.calc

deftips\_data():

bill = input.total\_bill()

idx1 = tips.total\_bill.between(bill\[0\], bill\[1\])

idx2 = tips.time.isin(input.time())

return tips\[idx1 & idx2\]

@reactive.effect

@reactive.event(input.reset)

def\_():

ui.update\_slider("total\_bill", value=bill\_rng)

ui.update\_checkbox\_group("time", selected=\["Lunch", "Dinner"\])

## Next steps [Anchor](https://shiny.posit.co/py/docs/user-interfaces.html\#next-steps)

If you’d like to start developing Shiny apps locally, see the get started section on [creating and running apps](https://shiny.posit.co/py/get-started/create-run.html).

Otherwise, to keep learning more about some of the topics covered here, see the following:

- [User interfaces](https://shiny.posit.co/py/docs/ui-overview.html): Learn more about the Shiny’s UI tooling.
- [Reactivity](https://shiny.posit.co/py/docs/reactive-foundations.html): Learn how to manage code execution in response to user input.
- [Jupyter Widgets](https://shiny.posit.co/py/docs/jupyter-widgets.html): Learn how all about Shiny’s Jupyter Widgets integration.