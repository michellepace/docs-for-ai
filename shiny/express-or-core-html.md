On this page

Now that you are familiar with [the differences between Shiny Express and Shiny Core](https://shiny.posit.co/py/docs/express-vs-core.html), you might be wondering how to choose between them.

In this article, we’ll suggest some guidelines, but it’s important to note that there are not many hard and fast rules. There is a lot of overlap between the capabilities of the two syntaxes, so feel free to choose whichever feels more natural and comfortable for you.

Shiny Express is designed to get you up and running as quickly as possible. It’s also designed to let you author your app with a minimum of boilerplate. As a result, it really shines in the early stages of both the learning journey and the lifecycle of an app.

Compared to Express, Core enforces a more structured approach that requires more initial effort to use. However, that investment has its own payoff.

The bulk of the rest of this article will focus on the advantages of Shiny Core. This isn’t because we think it’s better, but because Shiny Express’s advantages—being more approachable and more concise—are fairly self-evident, while Shiny Core’s advantages are more subtle.

## Maintainability [Anchor](https://shiny.posit.co/py/docs/express-or-core.html\#maintainability)

**Consider using Shiny Core if you are building a large or long-lived app.**

The most important difference between the two syntaxes is that Express allows you to intermingle UI and server code, while Core requires you to separate them. The separation that Core requires can feel inconvenient while adding features to your app, as each new output requires you to edit two different places in your `app.py` file.

But for larger and longer-lived apps, Shiny Core’s more opinionated approach becomes an advantage. It is much easier to add, remove, or relocate pieces of your UI when all of its code is in one place, with no server code to confuse things. Similarly, when you’re trying to understand the relationship between a reactive calculation and some outputs, it’s much easier to do so when you don’t have intermingled UI code in the way.

At the [bottom of this page](https://shiny.posit.co/py/docs/express-or-core.html#appendix), you’ll find a Shiny Core version of the [dashboard app from the Essentials section](https://shiny.posit.co/py/docs/user-interfaces.html#all-together-now) of this guide. Compare their respective source code, and consider:

- Which version makes the structure of the UI more obvious?
- Which version would make you more confident in moving UI elements around?
- Which version makes it easier to understand the reactive calcs and outputs?
- Imagine you were picking up an app that had been written a year ago by someone else. Which version would you prefer?

## Feature set [Anchor](https://shiny.posit.co/py/docs/express-or-core.html\#feature-set)

**Consider using Shiny Core if you need to use Shiny Modules or dynamic UI.**

At this time, Shiny Core’s functionality is a superset of Express, meaning that anything you can do in Express, you can also do in Core. However, the reverse is not true.

Most importantly, [Shiny Modules](https://shiny.posit.co/py/docs/modules.html) are supported in Shiny Core but not (yet) in Shiny Express. Shiny Modules are extremely useful for organizing large apps into smaller, more manageable pieces, and are also a mechanism for reusing Shiny application logic.

Shiny Core also has `ui.insert_ui()` and `ui.remove_ui()` functions, which is a way to imperatively add or remove UI elements from the app at any time. Despite being available in `shiny.express.ui`, these functions do not currently work well with Shiny Express. The same goes for `ui.modal_show()`.

## Maturity [Anchor](https://shiny.posit.co/py/docs/express-or-core.html\#maturity)

**Consider using Shiny Core if you care more about maturity and stability than convenience.**

Given its longer history, Shiny Core is naturally more mature than Shiny Express in both syntax and implementation.

We’ve carefully designed the Shiny Express syntax, and hope not to have to make breaking changes to it. However, we don’t know what we don’t know, and it’s possible that user feedback or our own testing will someday require us to make significant changes.

Similarly, we are constantly testing Shiny Express, but as of this writing, it has not has as much real-world use as Shiny Core. Therefore, with Shiny Core, you are less likely to encounter bugs.

## Familiarity to R users [Anchor](https://shiny.posit.co/py/docs/express-or-core.html\#familiarity-to-r-users)

**Consider using Shiny Core if you are an R user who is already familiar with Shiny.**

While Shiny Core is not a literal translation of Shiny for R, it is much closer to it than Shiny Express. The UI/server separation, the nested UI function calls, the matching of output IDs to render functions, are all going to feel very natural to experienced Shiny for R app authors.

## Appendix [Anchor](https://shiny.posit.co/py/docs/express-or-core.html\#appendix)

The following is the dashboard application from the Essentials section of this guide, rewritten using Shiny Core. Compare it to [the original](https://shiny.posit.co/py/docs/user-interfaces.html#all-together-now).

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

140

141

142

143

144

145

146

147

148

149

150

151

152

153

154

155

156

157

158

159

160

161

162

163

164

165

166

167

168

169

170

171

172

173

174

175

import faicons as fa

import plotly.express as px

from shinywidgets import output\_widget, render\_plotly

from shiny import App, reactive, render, req, ui

\# Load data and compute static values

tips = px.data.tips()

bill\_rng = (min(tips.total\_bill), max(tips.total\_bill))

ICONS = {

"user": fa.icon\_svg("user", "regular"),

"wallet": fa.icon\_svg("wallet"),

"currency-dollar": fa.icon\_svg("dollar-sign"),

"gear": fa.icon\_svg("gear")

}

app\_ui = ui.page\_sidebar(

ui.sidebar(

ui.input\_slider("total\_bill", "Bill amount", min=bill\_rng\[0\], max=bill\_rng\[1\], value=bill\_rng, pre="$"),

ui.input\_checkbox\_group("time", "Food service", \["Lunch", "Dinner"\], selected=\["Lunch", "Dinner"\], inline=True),

ui.input\_action\_button("reset", "Reset filter"),

),

ui.layout\_columns(

ui.value\_box(

"Total tippers",

ui.output\_ui("total\_tippers"),

showcase=ICONS\["user"\],

showcase\_layout="left center",

),

ui.value\_box(

"Average tip",

ui.output\_ui("average\_tip"),

showcase=ICONS\["wallet"\],

showcase\_layout="left center",

),

ui.value\_box(

"Average bill",

ui.output\_ui("average\_bill"),

showcase=ICONS\["currency-dollar"\],

showcase\_layout="left center",

),

fill=False,

),

ui.layout\_columns(

ui.card(

ui.card\_header("Tips data"),

ui.output\_data\_frame("table"),

full\_screen=True,

),

ui.card(

ui.card\_header(

"Total bill vs tip",

ui.popover(

ICONS\["gear"\],

ui.input\_radio\_buttons(

"scatter\_color", None,

\["none", "sex", "smoker", "day", "time"\],

inline=True,

),

title="Add a color variable",

placement="top",

),

class\_="d-flex justify-content-between align-items-center"

),

output\_widget("scatterplot"),

full\_screen=True,

),

ui.card(

ui.card\_header(

"Tip percentages",

ui.popover(

ICONS\["gear"\],

ui.input\_radio\_buttons(

"tip\_perc\_y", "Split by:",

\["sex", "smoker", "day", "time"\],

selected="day",

inline=True,

),

title="Add a color variable",

),

class\_="d-flex justify-content-between align-items-center",

),

output\_widget("tip\_perc"),

full\_screen=True,

),

col\_widths=\[6, 6, 12\],

),

title="Restaurant tipping",

fillable=True,

)

defserver(input, output, session):

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

\# --------------------------------------------------------

\# Outputs

\# --------------------------------------------------------

@render.ui

deftotal\_tippers():

return tips\_data().shape\[0\]

@render.ui

defaverage\_tip():

d = tips\_data()

req(d.shape\[0\] \> 0)

perc = d.tip / d.total\_bill

returnf"{perc.mean():.1%}"

@render.ui

defaverage\_bill():

d = tips\_data()

req(d.shape\[0\] \> 0)

bill = d.total\_bill.mean()

returnf"${bill:.2f}"

@render.data\_frame

deftable():

return render.DataGrid(tips\_data())

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

@render\_plotly

deftip\_perc():

from ridgeplot import ridgeplot

dat = tips\_data().copy()

dat.loc\[:, "percent"\] = dat.tip / dat.total\_bill

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

app = App(app\_ui, server)