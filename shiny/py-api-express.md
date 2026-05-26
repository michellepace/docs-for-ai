# Shiny Express API

This page outlines Shiny _Express_’s API reference.

[Compared to Shiny Core](https://shiny.posit.co/py/docs/express-vs-core.html), Shiny Express is a simpler way to learn and create basic apps, but it is less flexible and powerful.

For an introduction to Shiny, see the [tutorial](https://shiny.posit.co/py/docs/overview.html).

# Function reference

## Input components [Anchor](https://shiny.posit.co/py/api/express/\#input-components)

Gather user input.

|     |     |
| --- | --- |
| [express.ui.input\_select](https://shiny.posit.co/py/api/express/express.ui.input_select.html#shiny.express.ui.input_select) | Create a select list that can be used to choose a single or multiple items from a list of values. |
| [express.ui.input\_selectize](https://shiny.posit.co/py/api/express/express.ui.input_selectize.html#shiny.express.ui.input_selectize) | Create a select list that can be used to choose a single or multiple items from a list of values. |
| [express.ui.input\_slider](https://shiny.posit.co/py/api/express/express.ui.input_slider.html#shiny.express.ui.input_slider) | Constructs a slider widget to select a number, date, or date-time from a range. |
| [express.ui.input\_dark\_mode](https://shiny.posit.co/py/api/express/express.ui.input_dark_mode.html#shiny.express.ui.input_dark_mode) | Creates a dark mode switch input that toggles the app between dark and light modes. |
| [express.ui.input\_date](https://shiny.posit.co/py/api/express/express.ui.input_date.html#shiny.express.ui.input_date) | Creates a text input which, when clicked on, brings up a calendar that the user can click on to select dates. |
| [express.ui.input\_date\_range](https://shiny.posit.co/py/api/express/express.ui.input_date_range.html#shiny.express.ui.input_date_range) | Creates a pair of text inputs which, when clicked on, bring up calendars that the user can click on to select dates. |
| [express.ui.input\_checkbox](https://shiny.posit.co/py/api/express/express.ui.input_checkbox.html#shiny.express.ui.input_checkbox) | Create a checkbox that can be used to specify logical values. |
| [express.ui.input\_checkbox\_group](https://shiny.posit.co/py/api/express/express.ui.input_checkbox_group.html#shiny.express.ui.input_checkbox_group) | Create a group of checkboxes that can be used to toggle multiple choices independently. |
| [express.ui.input\_switch](https://shiny.posit.co/py/api/express/express.ui.input_switch.html#shiny.express.ui.input_switch) | Create a switch that can be used to specify logical values. Similar to [input\_checkbox](https://shiny.posit.co/py/api/core/ui.input_checkbox.html#shiny.ui.input_checkbox), but implies to the user that the change will take effect immediately. |
| [express.ui.input\_radio\_buttons](https://shiny.posit.co/py/api/express/express.ui.input_radio_buttons.html#shiny.express.ui.input_radio_buttons) | Create a set of radio buttons used to select an item from a list. |
| [express.ui.input\_numeric](https://shiny.posit.co/py/api/express/express.ui.input_numeric.html#shiny.express.ui.input_numeric) | Create an input control for entry of numeric values. |
| [express.ui.input\_text](https://shiny.posit.co/py/api/express/express.ui.input_text.html#shiny.express.ui.input_text) | Create an input control for entry of text values. |
| [express.ui.input\_text\_area](https://shiny.posit.co/py/api/express/express.ui.input_text_area.html#shiny.express.ui.input_text_area) | Create a textarea input control for entry of unstructured text values. |
| [express.ui.input\_password](https://shiny.posit.co/py/api/express/express.ui.input_password.html#shiny.express.ui.input_password) | Create an password control for entry of passwords. |
| [express.ui.input\_action\_button](https://shiny.posit.co/py/api/express/express.ui.input_action_button.html#shiny.express.ui.input_action_button) | Creates an action button whose value is initially zero, and increments by one each time it is pressed. |
| [express.ui.input\_action\_link](https://shiny.posit.co/py/api/express/express.ui.input_action_link.html#shiny.express.ui.input_action_link) | Creates a link whose value is initially zero, and increments by one each time it is pressed. |
| [express.ui.input\_task\_button](https://shiny.posit.co/py/api/express/express.ui.input_task_button.html#shiny.express.ui.input_task_button) | Creates a button for launching longer-running operations. |

## Output components [Anchor](https://shiny.posit.co/py/api/express/\#output-components)

Reactively render output.

|     |     |
| --- | --- |
| [express.render.plot](https://shiny.posit.co/py/api/express/express.render.plot.html#shiny.express.render.plot) | Reactively render a plot object as an HTML image. |
| [express.render.table](https://shiny.posit.co/py/api/express/express.render.table.html#shiny.express.render.table) | Reactively render a pandas `DataFrame` object (or similar) as a basic HTML table. |
| [express.render.DataTable](https://shiny.posit.co/py/api/express/express.render.DataTable.html#shiny.express.render.DataTable) | Holds the data and options for a [data\_frame](https://shiny.posit.co/py/api/core/render.data_frame.html#shiny.render.data_frame) output, for a spreadsheet-like view. |
| [express.render.data\_frame](https://shiny.posit.co/py/api/express/express.render.data_frame.html#shiny.express.render.data_frame) | Decorator for a function that returns a [pandas](https://pandas.pydata.org/), [polars](https://pola.rs/), or eager [`narwhals`](https://narwhals-dev.github.io/narwhals/) compatible `DataFrame` object to render as an interactive table or grid. Features fast virtualized scrolling, sorting, filtering, and row selection (single or multiple). |
| [express.render.DataGrid](https://shiny.posit.co/py/api/express/express.render.DataGrid.html#shiny.express.render.DataGrid) | Holds the data and options for a [data\_frame](https://shiny.posit.co/py/api/core/render.data_frame.html#shiny.render.data_frame) output, for a spreadsheet-like view. |
| [express.render.text](https://shiny.posit.co/py/api/express/express.render.text.html#shiny.express.render.text) | Reactively render text. |
| [express.render.ui](https://shiny.posit.co/py/api/express/express.render.ui.html#shiny.express.render.ui) | Reactively render HTML content. |
| [express.render.download](https://shiny.posit.co/py/api/express/express.render.download.html#shiny.express.render.download) | Decorator to register a function to handle a download. |
| [express.render.image](https://shiny.posit.co/py/api/express/express.render.image.html#shiny.express.render.image) | Reactively render a image file as an HTML image. |
| [express.render.express](https://shiny.posit.co/py/api/express/express.render.express.html#shiny.express.render.express) | Reactively render HTML content with output captured as in Shiny Express |

## Layouts and other UI tools [Anchor](https://shiny.posit.co/py/api/express/\#layouts-and-other-ui-tools)

Tools for creating, arranging, and styling UI components.

|     |     |
| --- | --- |
| [express.ui.page\_opts](https://shiny.posit.co/py/api/express/express.ui.page_opts.html#shiny.express.ui.page_opts) | Set page-level options for the current app. |
| [express.ui.sidebar](https://shiny.posit.co/py/api/express/express.ui.sidebar.html#shiny.express.ui.sidebar) | Context manager for sidebar element |
| [express.ui.layout\_columns](https://shiny.posit.co/py/api/express/express.ui.layout_columns.html#shiny.express.ui.layout_columns) | Context manager for responsive, column-based grid layouts, based on a 12-column grid. |
| [express.ui.layout\_column\_wrap](https://shiny.posit.co/py/api/express/express.ui.layout_column_wrap.html#shiny.express.ui.layout_column_wrap) | Context manager for a grid-like, column-first layout |
| [express.ui.card](https://shiny.posit.co/py/api/express/express.ui.card.html#shiny.express.ui.card) | Context manager for Bootstrap card component |
| [express.ui.card\_header](https://shiny.posit.co/py/api/express/express.ui.card_header.html#shiny.express.ui.card_header) | Context manager for a card header container |
| [express.ui.card\_footer](https://shiny.posit.co/py/api/express/express.ui.card_footer.html#shiny.express.ui.card_footer) | Context manager for a card footer container |
| [express.ui.value\_box](https://shiny.posit.co/py/api/express/express.ui.value_box.html#shiny.express.ui.value_box) | Context manager for a value box |
| [express.ui.value\_box\_theme](https://shiny.posit.co/py/api/express/express.ui.value_box_theme.html#shiny.express.ui.value_box_theme) | Value box theme |
| [express.ui.popover](https://shiny.posit.co/py/api/express/express.ui.popover.html#shiny.express.ui.popover) | Context manager for a popover |
| [express.ui.tooltip](https://shiny.posit.co/py/api/express/express.ui.tooltip.html#shiny.express.ui.tooltip) | Context manager for a tooltip |
| [express.ui.accordion](https://shiny.posit.co/py/api/express/express.ui.accordion.html#shiny.express.ui.accordion) | Context manager for a vertically collapsing accordion. |
| [express.ui.accordion\_panel](https://shiny.posit.co/py/api/express/express.ui.accordion_panel.html#shiny.express.ui.accordion_panel) | Context manager for single accordion panel. |
| [express.ui.layout\_sidebar](https://shiny.posit.co/py/api/express/express.ui.layout_sidebar.html#shiny.express.ui.layout_sidebar) | Context manager for sidebar layout |

## Navigate multiple panels [Anchor](https://shiny.posit.co/py/api/express/\#navigate-multiple-panels)

Create a set of panels that can be navigated between.

|     |     |
| --- | --- |
| [express.ui.nav\_panel](https://shiny.posit.co/py/api/express/express.ui.nav_panel.html#shiny.express.ui.nav_panel) | Context manager for nav item pointing to some internal content. |
| [express.ui.navset\_card\_underline](https://shiny.posit.co/py/api/express/express.ui.navset_card_underline.html#shiny.express.ui.navset_card_underline) | Context manager for a set of nav items as a tabset inside a card container. |
| [express.ui.navset\_card\_tab](https://shiny.posit.co/py/api/express/express.ui.navset_card_tab.html#shiny.express.ui.navset_card_tab) | Context manager for a set of nav items as a tabset inside a card container. |
| [express.ui.navset\_card\_pill](https://shiny.posit.co/py/api/express/express.ui.navset_card_pill.html#shiny.express.ui.navset_card_pill) | Context manager for a set of nav items as a tabset inside a card container. |
| [express.ui.nav\_spacer](https://shiny.posit.co/py/api/express/express.ui.nav_spacer.html#shiny.express.ui.nav_spacer) | Create space between nav items. |
| [express.ui.nav\_menu](https://shiny.posit.co/py/api/express/express.ui.nav_menu.html#shiny.express.ui.nav_menu) | Context manager for a menu of nav items. |
| [express.ui.nav\_control](https://shiny.posit.co/py/api/express/express.ui.nav_control.html#shiny.express.ui.nav_control) | Context manager for a control in the navigation container. |
| [express.ui.navset\_bar](https://shiny.posit.co/py/api/express/express.ui.navset_bar.html#shiny.express.ui.navset_bar) | Context manager for a set of nav items as a tabset inside a card container. |
| [express.ui.navset\_tab](https://shiny.posit.co/py/api/express/express.ui.navset_tab.html#shiny.express.ui.navset_tab) | Context manager for a set of nav items as a tabset. |
| [express.ui.navset\_pill](https://shiny.posit.co/py/api/express/express.ui.navset_pill.html#shiny.express.ui.navset_pill) | Context manager for a set of nav items as a pillset. |
| [express.ui.navset\_underline](https://shiny.posit.co/py/api/express/express.ui.navset_underline.html#shiny.express.ui.navset_underline) | Context manager for a set of nav items whose active/focused navigation links are styled with an underline. |
| [express.ui.navset\_pill\_list](https://shiny.posit.co/py/api/express/express.ui.navset_pill_list.html#shiny.express.ui.navset_pill_list) | Context manager for a set of nav items as a tabset inside a card container. |
| [express.ui.navset\_hidden](https://shiny.posit.co/py/api/express/express.ui.navset_hidden.html#shiny.express.ui.navset_hidden) | Context manager for nav contents without the nav items. |
| [express.ui.navbar\_options](https://shiny.posit.co/py/api/express/express.ui.navbar_options.html#shiny.express.ui.navbar_options) | Configure the appearance and behavior of the navbar. |
| [express.ui.insert\_nav\_panel](https://shiny.posit.co/py/api/express/express.ui.insert_nav_panel.html#shiny.express.ui.insert_nav_panel) | Create a new nav panel in an existing navset. |
| [express.ui.remove\_nav\_panel](https://shiny.posit.co/py/api/express/express.ui.remove_nav_panel.html#shiny.express.ui.remove_nav_panel) | Remove a nav item from a navigation container. |
| [express.ui.update\_nav\_panel](https://shiny.posit.co/py/api/express/express.ui.update_nav_panel.html#shiny.express.ui.update_nav_panel) | Show/hide a navigation item |

## Chat interface [Anchor](https://shiny.posit.co/py/api/express/\#chat-interface)

Build a chatbot interface

|     |     |
| --- | --- |
| [express.ui.Chat](https://shiny.posit.co/py/api/express/express.ui.Chat.html#shiny.express.ui.Chat) | Examples ——– |

## Streaming markdown [Anchor](https://shiny.posit.co/py/api/express/\#streaming-markdown)

Stream markdown content into the UI

|     |     |
| --- | --- |
| [express.ui.MarkdownStream](https://shiny.posit.co/py/api/express/express.ui.MarkdownStream.html#shiny.express.ui.MarkdownStream) | Examples ——– |

## Reactive programming [Anchor](https://shiny.posit.co/py/api/express/\#reactive-programming)

Create reactive functions and dependencies.

|     |     |
| --- | --- |
| [reactive.calc](https://shiny.posit.co/py/api/express/reactive.calc.html#shiny.reactive.calc) | Mark a function as a reactive calculation. |
| [reactive.effect](https://shiny.posit.co/py/api/express/reactive.effect.html#shiny.reactive.effect) | Mark a function as a reactive side effect. |
| [reactive.value](https://shiny.posit.co/py/api/express/reactive.value.html#shiny.reactive.value) | Create a reactive value. |
| [reactive.event](https://shiny.posit.co/py/api/express/reactive.event.html#shiny.reactive.event) | Mark a function to react only when an “event” occurs. |
| [reactive.isolate](https://shiny.posit.co/py/api/express/reactive.isolate.html#shiny.reactive.isolate) | Create a non-reactive scope within a reactive scope. |
| [reactive.invalidate\_later](https://shiny.posit.co/py/api/express/reactive.invalidate_later.html#shiny.reactive.invalidate_later) | Scheduled Invalidation |
| [reactive.extended\_task](https://shiny.posit.co/py/api/express/reactive.extended_task.html#shiny.reactive.extended_task) | Decorator to mark an async function as a slow computation. This will cause the function to be run in a background asyncio task, and the results will be available via the [ExtendedTask](https://shiny.posit.co/py/api/core/ExtendedTask.html#shiny.reactive.ExtendedTask) object returned by the decorator. |
| [reactive.flush](https://shiny.posit.co/py/api/express/reactive.flush.html#shiny.reactive.flush) | Run any pending invalidations (i.e., flush the reactive environment). |
| [reactive.poll](https://shiny.posit.co/py/api/express/reactive.poll.html#shiny.reactive.poll) | Create a reactive polling object. |
| [reactive.file\_reader](https://shiny.posit.co/py/api/express/reactive.file_reader.html#shiny.reactive.file_reader) | Create a reactive file reader. |
| [reactive.lock](https://shiny.posit.co/py/api/express/reactive.lock.html#shiny.reactive.lock) | A lock that should be held whenever manipulating the reactive graph. |
| [req](https://shiny.posit.co/py/api/express/req.html#shiny.req) | Throw a silent exception for falsy values. |

## Reusable Express code [Anchor](https://shiny.posit.co/py/api/express/\#reusable-express-code)

Create reusable Express code.

|     |     |
| --- | --- |
| [express.ui.hold](https://shiny.posit.co/py/api/express/express.ui.hold.html#shiny.express.ui.hold) | Prevent the display of UI elements in various ways. |
| [express.expressify](https://shiny.posit.co/py/api/express/express.expressify.html#shiny.express.expressify) | Decorate a function so that output is captured as in Shiny Express |

## Update inputs [Anchor](https://shiny.posit.co/py/api/express/\#update-inputs)

Programmatically update input values.

|     |     |
| --- | --- |
| [express.ui.update\_select](https://shiny.posit.co/py/api/express/express.ui.update_select.html#shiny.express.ui.update_select) | Change the value of a select input on the client. |
| [express.ui.update\_selectize](https://shiny.posit.co/py/api/express/express.ui.update_selectize.html#shiny.express.ui.update_selectize) | Change the value of a selectize.js powered input on the client. |
| [express.ui.update\_slider](https://shiny.posit.co/py/api/express/express.ui.update_slider.html#shiny.express.ui.update_slider) | Change the value of a slider input on the client. |
| [express.ui.update\_dark\_mode](https://shiny.posit.co/py/api/express/express.ui.update_dark_mode.html#shiny.express.ui.update_dark_mode) |  |
| [express.ui.update\_date](https://shiny.posit.co/py/api/express/express.ui.update_date.html#shiny.express.ui.update_date) | Change the value of a date input on the client. |
| [express.ui.update\_date\_range](https://shiny.posit.co/py/api/express/express.ui.update_date_range.html#shiny.express.ui.update_date_range) | Change the start and end values of a date range input on the client. |
| [express.ui.update\_checkbox](https://shiny.posit.co/py/api/express/express.ui.update_checkbox.html#shiny.express.ui.update_checkbox) | Change the value of a checkbox input on the client. |
| [express.ui.update\_checkbox\_group](https://shiny.posit.co/py/api/express/express.ui.update_checkbox_group.html#shiny.express.ui.update_checkbox_group) | Change the value of a checkbox group input on the client. |
| [express.ui.update\_switch](https://shiny.posit.co/py/api/express/express.ui.update_switch.html#shiny.express.ui.update_switch) | Change the value of a switch input on the client. |
| [express.ui.update\_radio\_buttons](https://shiny.posit.co/py/api/express/express.ui.update_radio_buttons.html#shiny.express.ui.update_radio_buttons) | Change the value of a radio input on the client. |
| [express.ui.update\_numeric](https://shiny.posit.co/py/api/express/express.ui.update_numeric.html#shiny.express.ui.update_numeric) | Change the value of a number input on the client. |
| [express.ui.update\_text](https://shiny.posit.co/py/api/express/express.ui.update_text.html#shiny.express.ui.update_text) | Change the value of a text input on the client. |
| [express.ui.update\_text\_area](https://shiny.posit.co/py/api/express/express.ui.update_text_area.html#shiny.express.ui.update_text_area) | Change the value of a text input on the client. |
| [express.ui.update\_navset](https://shiny.posit.co/py/api/express/express.ui.update_navset.html#shiny.express.ui.update_navset) | Change the value of a navs container on the client. |
| [express.ui.update\_action\_button](https://shiny.posit.co/py/api/express/express.ui.update_action_button.html#shiny.express.ui.update_action_button) | Change the label and/or icon of an action button on the client. |
| [express.ui.update\_action\_link](https://shiny.posit.co/py/api/express/express.ui.update_action_link.html#shiny.express.ui.update_action_link) | Change the label and/or icon of an action link on the client. |
| [express.ui.update\_task\_button](https://shiny.posit.co/py/api/express/express.ui.update_task_button.html#shiny.express.ui.update_task_button) | Change the state of a task button on the client. |

## Update UI Layouts [Anchor](https://shiny.posit.co/py/api/express/\#update-ui-layouts)

|     |     |
| --- | --- |
| [express.ui.update\_sidebar](https://shiny.posit.co/py/api/express/express.ui.update_sidebar.html#shiny.express.ui.update_sidebar) | Update a sidebar’s visibility. |
| [express.ui.update\_tooltip](https://shiny.posit.co/py/api/express/express.ui.update_tooltip.html#shiny.express.ui.update_tooltip) | Update tooltip contents. |
| [express.ui.update\_popover](https://shiny.posit.co/py/api/express/express.ui.update_popover.html#shiny.express.ui.update_popover) | Update the contents or title of a popover. |
| [express.ui.update\_accordion](https://shiny.posit.co/py/api/express/express.ui.update_accordion.html#shiny.express.ui.update_accordion) | Dynamically set accordions’ states. |
| [express.ui.update\_accordion\_panel](https://shiny.posit.co/py/api/express/express.ui.update_accordion_panel.html#shiny.express.ui.update_accordion_panel) | Dynamically update accordion panel contents. |
| [express.ui.insert\_accordion\_panel](https://shiny.posit.co/py/api/express/express.ui.insert_accordion_panel.html#shiny.express.ui.insert_accordion_panel) | Insert an accordion panel into an existing accordion. |
| [express.ui.remove\_accordion\_panel](https://shiny.posit.co/py/api/express/express.ui.remove_accordion_panel.html#shiny.express.ui.remove_accordion_panel) | Remove an [accordion\_panel](https://shiny.posit.co/py/api/core/ui.accordion_panel.html#shiny.ui.accordion_panel). |

## Display messages [Anchor](https://shiny.posit.co/py/api/express/\#display-messages)

Display messages to the user.

|     |     |
| --- | --- |
| [express.ui.help\_text](https://shiny.posit.co/py/api/express/express.ui.help_text.html#shiny.express.ui.help_text) | Create a help text element |
| [express.ui.notification\_show](https://shiny.posit.co/py/api/express/express.ui.notification_show.html#shiny.express.ui.notification_show) | Show a notification to the user. |
| [express.ui.notification\_remove](https://shiny.posit.co/py/api/express/express.ui.notification_remove.html#shiny.express.ui.notification_remove) | Remove a notification. |
| [express.ui.modal](https://shiny.posit.co/py/api/express/express.ui.modal.html#shiny.express.ui.modal) | Creates the UI for a modal dialog, using Bootstrap’s modal class. |
| [express.ui.modal\_show](https://shiny.posit.co/py/api/express/express.ui.modal_show.html#shiny.express.ui.modal_show) | Show a modal dialog. |
| [express.ui.modal\_remove](https://shiny.posit.co/py/api/express/express.ui.modal_remove.html#shiny.express.ui.modal_remove) | Remove a modal dialog box. |
| [express.ui.modal\_button](https://shiny.posit.co/py/api/express/express.ui.modal_button.html#shiny.express.ui.modal_button) | Creates a button that will dismiss a [modal](https://shiny.posit.co/py/api/core/ui.modal.html#shiny.ui.modal). |
| [express.ui.Progress](https://shiny.posit.co/py/api/express/express.ui.Progress.html#shiny.express.ui.Progress) | Initialize a progress bar. |

## Modules [Anchor](https://shiny.posit.co/py/api/express/\#modules)

|     |     |
| --- | --- |
| [express.module](https://shiny.posit.co/py/api/express/express.module.html#shiny.express.module) | Create a Shiny module using Shiny Express syntax |

## UI panels [Anchor](https://shiny.posit.co/py/api/express/\#ui-panels)

Visually group together a section of UI components.

|     |     |
| --- | --- |
| [express.ui.panel\_absolute](https://shiny.posit.co/py/api/express/express.ui.panel_absolute.html#shiny.express.ui.panel_absolute) | Context manager for a panel of absolutely positioned content. |
| [express.ui.panel\_fixed](https://shiny.posit.co/py/api/express/express.ui.panel_fixed.html#shiny.express.ui.panel_fixed) | Context manager for a panel of absolutely positioned content. |
| [express.ui.panel\_title](https://shiny.posit.co/py/api/express/express.ui.panel_title.html#shiny.express.ui.panel_title) | Create title(s) for the application. |

## Uploads & downloads [Anchor](https://shiny.posit.co/py/api/express/\#uploads-downloads)

Allow users to upload and download files.

|     |     |
| --- | --- |
| [express.ui.input\_file](https://shiny.posit.co/py/api/express/express.ui.input_file.html#shiny.express.ui.input_file) | Create a file upload control that can be used to upload one or more files. |
| [express.render.download](https://shiny.posit.co/py/api/express/express.render.download.html#shiny.express.render.download) | Decorator to register a function to handle a download. |

## Dynamic UI [Anchor](https://shiny.posit.co/py/api/express/\#dynamic-ui)

Dynamically show/hide UI elements.

|     |     |
| --- | --- |
| [express.ui.panel\_conditional](https://shiny.posit.co/py/api/express/express.ui.panel_conditional.html#shiny.express.ui.panel_conditional) | Context manager for a conditional panel |
| [express.ui.insert\_ui](https://shiny.posit.co/py/api/express/express.ui.insert_ui.html#shiny.express.ui.insert_ui) | Insert UI objects. |
| [express.ui.remove\_ui](https://shiny.posit.co/py/api/express/express.ui.remove_ui.html#shiny.express.ui.remove_ui) | Remove UI objects. |

## User Session [Anchor](https://shiny.posit.co/py/api/express/\#user-session)

Tools for managing user sessions and accessing session-related information.

|     |     |
| --- | --- |
| [session.Session](https://shiny.posit.co/py/api/express/session.Session.html#shiny.session.Session) | Interface definition for Session-like classes, like `AppSession`, `SessionProxy`, and `ExpressStubSession`. |

## Client Data [Anchor](https://shiny.posit.co/py/api/express/\#client-data)

Access (client-side) information about the user session (e.g., URL, output info, etc).

|     |     |
| --- | --- |
| [session.ClientData](https://shiny.posit.co/py/api/express/session.ClientData.html#shiny.session.ClientData) | Access (client-side) information from the browser. |

## UI as HTML [Anchor](https://shiny.posit.co/py/api/express/\#ui-as-html)

Tools for creating HTML/CSS/JS

|     |     |
| --- | --- |
| [express.ui.Theme](https://shiny.posit.co/py/api/express/express.ui.Theme.html#shiny.express.ui.Theme) | Create a custom Shiny theme. |
| [express.ui.markdown](https://shiny.posit.co/py/api/express/express.ui.markdown.html#shiny.express.ui.markdown) | Convert a string of markdown to `ui.HTML`. |
| [express.ui.include\_css](https://shiny.posit.co/py/api/express/express.ui.include_css.html#shiny.express.ui.include_css) | Include a CSS file. |
| [express.ui.include\_js](https://shiny.posit.co/py/api/express/express.ui.include_js.html#shiny.express.ui.include_js) | Include a JavaScript file. |
| [express.ui.HTML](https://shiny.posit.co/py/api/express/express.ui.HTML.html#shiny.express.ui.HTML) | Mark a string as raw HTML. This will prevent the string from being escaped when rendered inside an HTML tag. |
| [express.ui.tags](https://shiny.posit.co/py/api/express/express.ui.tags.html#shiny.express.ui.tags) | Functions for creating HTML tags. |
| [express.ui.TagList](https://shiny.posit.co/py/api/express/express.ui.TagList.html#shiny.express.ui.TagList) | Create an HTML tag list (i.e., a fragment of HTML) |
| [express.ui.busy\_indicators.use](https://shiny.posit.co/py/api/express/express.ui.busy_indicators.use.html#shiny.express.ui.busy_indicators.use) | Enable/disable busy indication |
| [express.ui.busy\_indicators.options](https://shiny.posit.co/py/api/express/express.ui.busy_indicators.options.html#shiny.express.ui.busy_indicators.options) | Customize spinning busy indicators. |

## Application-level settings [Anchor](https://shiny.posit.co/py/api/express/\#application-level-settings)

|     |     |
| --- | --- |
| [express.app\_opts](https://shiny.posit.co/py/api/express/express.app_opts.html#shiny.express.app_opts) | Set App-level options in Shiny Express |

## Express developer tooling [Anchor](https://shiny.posit.co/py/api/express/\#express-developer-tooling)

|     |     |
| --- | --- |
| [express.is\_express\_app](https://shiny.posit.co/py/api/express/express.is_express_app.html#shiny.express.is_express_app) | Detect whether an app file is a Shiny express app |
| [express.wrap\_express\_app](https://shiny.posit.co/py/api/express/express.wrap_express_app.html#shiny.express.wrap_express_app) | Wrap a Shiny Express mode app into a Shiny `App` object. |