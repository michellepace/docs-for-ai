# Shiny Testing API

This page outlines Shiny’s _Testing_ API reference.

For an introduction to Shiny testing, see the [unit testing](https://shiny.posit.co/py/docs/unit-testing.html) and [end to end testing](https://shiny.posit.co/py/docs/end-to-end-testing.html) tutorials.

# Function reference

## UI Layouts [Anchor](https://shiny.posit.co/py/api/testing/\#ui-layouts)

Methods for interacting with Shiny app multiple UI component controller.

|     |     |
| --- | --- |
| [playwright.controller.Accordion](https://shiny.posit.co/py/api/testing/playwright.controller.Accordion.html#shiny.playwright.controller.Accordion) | Controller for [`shiny.ui.accordion`](https://shiny.posit.co/py/api/core/ui.accordion.html#shiny.ui.accordion). |
| [playwright.controller.AccordionPanel](https://shiny.posit.co/py/api/testing/playwright.controller.AccordionPanel.html#shiny.playwright.controller.AccordionPanel) | Controller for [`shiny.ui.accordion_panel`](https://shiny.posit.co/py/api/core/ui.accordion_panel.html#shiny.ui.accordion_panel). |
| [playwright.controller.Card](https://shiny.posit.co/py/api/testing/playwright.controller.Card.html#shiny.playwright.controller.Card) | Controller for [`shiny.ui.card`](https://shiny.posit.co/py/api/core/ui.card.html#shiny.ui.card). |
| [playwright.controller.Offcanvas](https://shiny.posit.co/py/api/testing/playwright.controller.Offcanvas.html#shiny.playwright.controller.Offcanvas) | Controller for [`shiny.ui.offcanvas`](https://shiny.posit.co/py/api/core/ui.offcanvas.html#shiny.ui.offcanvas). |
| [playwright.controller.Popover](https://shiny.posit.co/py/api/testing/playwright.controller.Popover.html#shiny.playwright.controller.Popover) | Controller for [`shiny.ui.popover`](https://shiny.posit.co/py/api/core/ui.popover.html#shiny.ui.popover). |
| [playwright.controller.Sidebar](https://shiny.posit.co/py/api/testing/playwright.controller.Sidebar.html#shiny.playwright.controller.Sidebar) | Controller for [`shiny.ui.sidebar`](https://shiny.posit.co/py/api/core/ui.sidebar.html#shiny.ui.sidebar). |
| [playwright.controller.Toast](https://shiny.posit.co/py/api/testing/playwright.controller.Toast.html#shiny.playwright.controller.Toast) | Controller for [`shiny.ui.toast`](https://shiny.posit.co/py/api/core/ui.toast.html#shiny.ui.toast). |
| [playwright.controller.Tooltip](https://shiny.posit.co/py/api/testing/playwright.controller.Tooltip.html#shiny.playwright.controller.Tooltip) | Controller for [`shiny.ui.tooltip`](https://shiny.posit.co/py/api/core/ui.tooltip.html#shiny.ui.tooltip). |

## UI Inputs [Anchor](https://shiny.posit.co/py/api/testing/\#ui-inputs)

Methods for interacting with Shiny app input value controller.

|     |     |
| --- | --- |
| [playwright.controller.InputActionButton](https://shiny.posit.co/py/api/testing/playwright.controller.InputActionButton.html#shiny.playwright.controller.InputActionButton) | Controller for [`shiny.ui.input_action_button`](https://shiny.posit.co/py/api/core/ui.input_action_button.html#shiny.ui.input_action_button). |
| [playwright.controller.InputActionLink](https://shiny.posit.co/py/api/testing/playwright.controller.InputActionLink.html#shiny.playwright.controller.InputActionLink) | Controller for [`shiny.ui.input_action_link`](https://shiny.posit.co/py/api/core/ui.input_action_link.html#shiny.ui.input_action_link). |
| [playwright.controller.InputBookmarkButton](https://shiny.posit.co/py/api/testing/playwright.controller.InputBookmarkButton.html#shiny.playwright.controller.InputBookmarkButton) | Controller for [`shiny.ui.input_bookmark_button`](https://shiny.posit.co/py/api/core/ui.input_bookmark_button.html#shiny.ui.input_bookmark_button). |
| [playwright.controller.InputCheckbox](https://shiny.posit.co/py/api/testing/playwright.controller.InputCheckbox.html#shiny.playwright.controller.InputCheckbox) | Controller for [`shiny.ui.input_checkbox`](https://shiny.posit.co/py/api/core/ui.input_checkbox.html#shiny.ui.input_checkbox). |
| [playwright.controller.InputCheckboxGroup](https://shiny.posit.co/py/api/testing/playwright.controller.InputCheckboxGroup.html#shiny.playwright.controller.InputCheckboxGroup) | Controller for [`shiny.ui.input_checkbox_group`](https://shiny.posit.co/py/api/core/ui.input_checkbox_group.html#shiny.ui.input_checkbox_group). |
| [playwright.controller.InputCodeEditor](https://shiny.posit.co/py/api/testing/playwright.controller.InputCodeEditor.html#shiny.playwright.controller.InputCodeEditor) | Controller for [`shiny.ui.input_code_editor`](https://shiny.posit.co/py/api/core/ui.input_code_editor.html#shiny.ui.input_code_editor). |
| [playwright.controller.InputDarkMode](https://shiny.posit.co/py/api/testing/playwright.controller.InputDarkMode.html#shiny.playwright.controller.InputDarkMode) | Controller for [`shiny.ui.input_dark_mode`](https://shiny.posit.co/py/api/core/ui.input_dark_mode.html#shiny.ui.input_dark_mode). |
| [playwright.controller.InputDate](https://shiny.posit.co/py/api/testing/playwright.controller.InputDate.html#shiny.playwright.controller.InputDate) |  |
| [playwright.controller.InputDateRange](https://shiny.posit.co/py/api/testing/playwright.controller.InputDateRange.html#shiny.playwright.controller.InputDateRange) | Controller for [`shiny.ui.input_date_range`](https://shiny.posit.co/py/api/core/ui.input_date_range.html#shiny.ui.input_date_range). |
| [playwright.controller.InputNumeric](https://shiny.posit.co/py/api/testing/playwright.controller.InputNumeric.html#shiny.playwright.controller.InputNumeric) | Controller for [`shiny.ui.input_numeric`](https://shiny.posit.co/py/api/core/ui.input_numeric.html#shiny.ui.input_numeric). |
| [playwright.controller.InputPassword](https://shiny.posit.co/py/api/testing/playwright.controller.InputPassword.html#shiny.playwright.controller.InputPassword) | Controller for [`shiny.ui.input_password`](https://shiny.posit.co/py/api/core/ui.input_password.html#shiny.ui.input_password). |
| [playwright.controller.InputRadioButtons](https://shiny.posit.co/py/api/testing/playwright.controller.InputRadioButtons.html#shiny.playwright.controller.InputRadioButtons) | Controller for [`shiny.ui.input_radio_buttons`](https://shiny.posit.co/py/api/core/ui.input_radio_buttons.html#shiny.ui.input_radio_buttons). |
| [playwright.controller.InputSelect](https://shiny.posit.co/py/api/testing/playwright.controller.InputSelect.html#shiny.playwright.controller.InputSelect) | Controller for [`shiny.ui.input_select`](https://shiny.posit.co/py/api/core/ui.input_select.html#shiny.ui.input_select). |
| [playwright.controller.InputSelectize](https://shiny.posit.co/py/api/testing/playwright.controller.InputSelectize.html#shiny.playwright.controller.InputSelectize) | Controller for [`shiny.ui.input_selectize`](https://shiny.posit.co/py/api/core/ui.input_selectize.html#shiny.ui.input_selectize). |
| [playwright.controller.InputSlider](https://shiny.posit.co/py/api/testing/playwright.controller.InputSlider.html#shiny.playwright.controller.InputSlider) | Controller for [`shiny.ui.input_slider`](https://shiny.posit.co/py/api/core/ui.input_slider.html#shiny.ui.input_slider). |
| [playwright.controller.InputSliderRange](https://shiny.posit.co/py/api/testing/playwright.controller.InputSliderRange.html#shiny.playwright.controller.InputSliderRange) | Controller for [`shiny.ui.input_slider`](https://shiny.posit.co/py/api/core/ui.input_slider.html#shiny.ui.input_slider) with a slider range. |
| [playwright.controller.InputSubmitTextarea](https://shiny.posit.co/py/api/testing/playwright.controller.InputSubmitTextarea.html#shiny.playwright.controller.InputSubmitTextarea) | Controller for [`shiny.ui.input_submit_textarea`](https://shiny.posit.co/py/api/core/ui.input_submit_textarea.html#shiny.ui.input_submit_textarea). |
| [playwright.controller.InputSwitch](https://shiny.posit.co/py/api/testing/playwright.controller.InputSwitch.html#shiny.playwright.controller.InputSwitch) | Controller for [`shiny.ui.input_switch`](https://shiny.posit.co/py/api/core/ui.input_switch.html#shiny.ui.input_switch). |
| [playwright.controller.InputTaskButton](https://shiny.posit.co/py/api/testing/playwright.controller.InputTaskButton.html#shiny.playwright.controller.InputTaskButton) | Controller for [`shiny.ui.input_task_button`](https://shiny.posit.co/py/api/core/ui.input_task_button.html#shiny.ui.input_task_button). |
| [playwright.controller.InputText](https://shiny.posit.co/py/api/testing/playwright.controller.InputText.html#shiny.playwright.controller.InputText) | Controller for [`shiny.ui.input_text`](https://shiny.posit.co/py/api/core/ui.input_text.html#shiny.ui.input_text). |
| [playwright.controller.InputTextArea](https://shiny.posit.co/py/api/testing/playwright.controller.InputTextArea.html#shiny.playwright.controller.InputTextArea) | Controller for [`shiny.ui.input_text_area`](https://shiny.posit.co/py/api/core/ui.input_text_area.html#shiny.ui.input_text_area). |
| [playwright.controller.ToolbarInputButton](https://shiny.posit.co/py/api/testing/playwright.controller.ToolbarInputButton.html#shiny.playwright.controller.ToolbarInputButton) | Controller for [`shiny.ui.toolbar_input_button`](https://shiny.posit.co/py/api/core/ui.toolbar_input_button.html#shiny.ui.toolbar_input_button). |
| [playwright.controller.ToolbarInputSelect](https://shiny.posit.co/py/api/testing/playwright.controller.ToolbarInputSelect.html#shiny.playwright.controller.ToolbarInputSelect) | Controller for [`shiny.ui.toolbar_input_select`](https://shiny.posit.co/py/api/core/ui.toolbar_input_select.html#shiny.ui.toolbar_input_select). |

## Value boxes [Anchor](https://shiny.posit.co/py/api/testing/\#value-boxes)

Methods for interacting with Shiny app valuebox controller.

|     |     |
| --- | --- |
| [playwright.controller.ValueBox](https://shiny.posit.co/py/api/testing/playwright.controller.ValueBox.html#shiny.playwright.controller.ValueBox) | Controller for [`shiny.ui.value_box`](https://shiny.posit.co/py/api/core/ui.value_box.html#shiny.ui.value_box). |

## Navigation (tab) panels [Anchor](https://shiny.posit.co/py/api/testing/\#navigation-tab-panels)

Methods for interacting with Shiny app UI content controller.

|     |     |
| --- | --- |
| [playwright.controller.NavsetBar](https://shiny.posit.co/py/api/testing/playwright.controller.NavsetBar.html#shiny.playwright.controller.NavsetBar) | Controller for [`shiny.ui.navset_bar`](https://shiny.posit.co/py/api/core/ui.navset_bar.html#shiny.ui.navset_bar). |
| [playwright.controller.NavsetCardPill](https://shiny.posit.co/py/api/testing/playwright.controller.NavsetCardPill.html#shiny.playwright.controller.NavsetCardPill) | Controller for [`shiny.ui.navset_card_pill`](https://shiny.posit.co/py/api/core/ui.navset_card_pill.html#shiny.ui.navset_card_pill). |
| [playwright.controller.NavsetCardTab](https://shiny.posit.co/py/api/testing/playwright.controller.NavsetCardTab.html#shiny.playwright.controller.NavsetCardTab) | Controller for [`shiny.ui.navset_card_tab`](https://shiny.posit.co/py/api/core/ui.navset_card_tab.html#shiny.ui.navset_card_tab). |
| [playwright.controller.NavsetCardUnderline](https://shiny.posit.co/py/api/testing/playwright.controller.NavsetCardUnderline.html#shiny.playwright.controller.NavsetCardUnderline) | Controller for [`shiny.ui.navset_card_underline`](https://shiny.posit.co/py/api/core/ui.navset_card_underline.html#shiny.ui.navset_card_underline). |
| [playwright.controller.NavsetHidden](https://shiny.posit.co/py/api/testing/playwright.controller.NavsetHidden.html#shiny.playwright.controller.NavsetHidden) | Controller for [`shiny.ui.navset_hidden`](https://shiny.posit.co/py/api/core/ui.navset_hidden.html#shiny.ui.navset_hidden). |
| [playwright.controller.NavsetPill](https://shiny.posit.co/py/api/testing/playwright.controller.NavsetPill.html#shiny.playwright.controller.NavsetPill) | Controller for [`shiny.ui.navset_pill`](https://shiny.posit.co/py/api/core/ui.navset_pill.html#shiny.ui.navset_pill). |
| [playwright.controller.NavsetPillList](https://shiny.posit.co/py/api/testing/playwright.controller.NavsetPillList.html#shiny.playwright.controller.NavsetPillList) | Controller for [`shiny.ui.navset_pill_list`](https://shiny.posit.co/py/api/core/ui.navset_pill_list.html#shiny.ui.navset_pill_list). |
| [playwright.controller.NavsetTab](https://shiny.posit.co/py/api/testing/playwright.controller.NavsetTab.html#shiny.playwright.controller.NavsetTab) | Controller for [`shiny.ui.navset_tab`](https://shiny.posit.co/py/api/core/ui.navset_tab.html#shiny.ui.navset_tab). |
| [playwright.controller.NavsetUnderline](https://shiny.posit.co/py/api/testing/playwright.controller.NavsetUnderline.html#shiny.playwright.controller.NavsetUnderline) | Controller for [`shiny.ui.navset_underline`](https://shiny.posit.co/py/api/core/ui.navset_underline.html#shiny.ui.navset_underline). |
| [playwright.controller.NavPanel](https://shiny.posit.co/py/api/testing/playwright.controller.NavPanel.html#shiny.playwright.controller.NavPanel) | Controller for [`shiny.ui.nav_panel`](https://shiny.posit.co/py/api/core/ui.nav_panel.html#shiny.ui.nav_panel). |
| [playwright.controller.PageNavbar](https://shiny.posit.co/py/api/testing/playwright.controller.PageNavbar.html#shiny.playwright.controller.PageNavbar) | Controller for [`shiny.ui.page_navbar`](https://shiny.posit.co/py/api/core/ui.page_navbar.html#shiny.ui.page_navbar). |

## Upload and download [Anchor](https://shiny.posit.co/py/api/testing/\#upload-and-download)

Methods for interacting with Shiny app uploading and downloading controller.

|     |     |
| --- | --- |
| [playwright.controller.InputFile](https://shiny.posit.co/py/api/testing/playwright.controller.InputFile.html#shiny.playwright.controller.InputFile) | Controller for [`shiny.ui.input_file`](https://shiny.posit.co/py/api/core/ui.input_file.html#shiny.ui.input_file). |
| [playwright.controller.DownloadButton](https://shiny.posit.co/py/api/testing/playwright.controller.DownloadButton.html#shiny.playwright.controller.DownloadButton) | Controller for [`shiny.ui.download_button`](https://shiny.posit.co/py/api/core/ui.download_button.html#shiny.ui.download_button) |
| [playwright.controller.DownloadLink](https://shiny.posit.co/py/api/testing/playwright.controller.DownloadLink.html#shiny.playwright.controller.DownloadLink) | Controller for [`shiny.ui.download_link`](https://shiny.posit.co/py/api/core/ui.download_link.html#shiny.ui.download_link). |

## Chat interface [Anchor](https://shiny.posit.co/py/api/testing/\#chat-interface)

Methods for interacting with Shiny app chat controller.

|     |     |
| --- | --- |
| [playwright.controller.Chat](https://shiny.posit.co/py/api/testing/playwright.controller.Chat.html#shiny.playwright.controller.Chat) | Controller for `shiny.ui.chat`. |

## Rendering Outputs [Anchor](https://shiny.posit.co/py/api/testing/\#rendering-outputs)

Render output in a variety of ways.

|     |     |
| --- | --- |
| [playwright.controller.OutputCode](https://shiny.posit.co/py/api/testing/playwright.controller.OutputCode.html#shiny.playwright.controller.OutputCode) | Controller for [`shiny.ui.output_code`](https://shiny.posit.co/py/api/core/ui.output_code.html#shiny.ui.output_code). |
| [playwright.controller.OutputDataFrame](https://shiny.posit.co/py/api/testing/playwright.controller.OutputDataFrame.html#shiny.playwright.controller.OutputDataFrame) | Controller for [`shiny.ui.output_data_frame`](https://shiny.posit.co/py/api/core/ui.output_data_frame.html#shiny.ui.output_data_frame). |
| [playwright.controller.OutputImage](https://shiny.posit.co/py/api/testing/playwright.controller.OutputImage.html#shiny.playwright.controller.OutputImage) | Controller for [`shiny.ui.output_image`](https://shiny.posit.co/py/api/core/ui.output_image.html#shiny.ui.output_image). |
| [playwright.controller.OutputPlot](https://shiny.posit.co/py/api/testing/playwright.controller.OutputPlot.html#shiny.playwright.controller.OutputPlot) | Controller for [`shiny.ui.output_plot`](https://shiny.posit.co/py/api/core/ui.output_plot.html#shiny.ui.output_plot). |
| [playwright.controller.OutputTable](https://shiny.posit.co/py/api/testing/playwright.controller.OutputTable.html#shiny.playwright.controller.OutputTable) | Controller for [`shiny.ui.output_table`](https://shiny.posit.co/py/api/core/ui.output_table.html#shiny.ui.output_table). |
| [playwright.controller.OutputText](https://shiny.posit.co/py/api/testing/playwright.controller.OutputText.html#shiny.playwright.controller.OutputText) | Controller for [`shiny.ui.output_text`](https://shiny.posit.co/py/api/core/ui.output_text.html#shiny.ui.output_text). |
| [playwright.controller.OutputUi](https://shiny.posit.co/py/api/testing/playwright.controller.OutputUi.html#shiny.playwright.controller.OutputUi) | Controller for [`shiny.ui.output_ui`](https://shiny.posit.co/py/api/core/ui.output_ui.html#shiny.ui.output_ui). |

## App test values [Anchor](https://shiny.posit.co/py/api/testing/\#app-test-values)

Read a session’s test-mode snapshot of input, output, and export values.

|     |     |
| --- | --- |
| [playwright.controller.AppTestValues](https://shiny.posit.co/py/api/testing/playwright.controller.AppTestValues.html#shiny.playwright.controller.AppTestValues) | Read a Shiny session’s test-mode snapshot of `input`, `output`, and `export` values from a running app. |

## Playwright Expect [Anchor](https://shiny.posit.co/py/api/testing/\#playwright-expect)

Methods for testing the state of a locator within a Shiny app.

|     |     |
| --- | --- |
| [playwright.expect.expect\_to\_change](https://shiny.posit.co/py/api/testing/playwright.expect.expect_to_change.html#shiny.playwright.expect.expect_to_change) | Context manager that yields when the value returned by func() changes. |
| [playwright.expect.expect\_not\_to\_have\_attribute](https://shiny.posit.co/py/api/testing/playwright.expect.expect_not_to_have_attribute.html#shiny.playwright.expect.expect_not_to_have_attribute) | Expect that the attribute does not exist. |
| [playwright.expect.expect\_to\_have\_class](https://shiny.posit.co/py/api/testing/playwright.expect.expect_to_have_class.html#shiny.playwright.expect.expect_to_have_class) | Expect a CSS class value is found. |
| [playwright.expect.expect\_not\_to\_have\_class](https://shiny.posit.co/py/api/testing/playwright.expect.expect_not_to_have_class.html#shiny.playwright.expect.expect_not_to_have_class) | Expect a CSS class value is not found. |
| [playwright.expect.expect\_to\_have\_style](https://shiny.posit.co/py/api/testing/playwright.expect.expect_to_have_style.html#shiny.playwright.expect.expect_to_have_style) | Expect the `style` attribute to have a value. |
| [playwright.expect.expect\_not\_to\_have\_style](https://shiny.posit.co/py/api/testing/playwright.expect.expect_not_to_have_style.html#shiny.playwright.expect.expect_not_to_have_style) | Expect a key within `style` attribute to not exist. |

## Pytest [Anchor](https://shiny.posit.co/py/api/testing/\#pytest)

Fixtures used for testing Shiny apps with Pytest.

|     |     |
| --- | --- |
| [pytest.create\_app\_fixture](https://shiny.posit.co/py/api/testing/pytest.create_app_fixture.html#shiny.pytest.create_app_fixture) | Create a fixture for a local Shiny app directory. |
| [pytest.ScopeName](https://shiny.posit.co/py/api/testing/pytest.ScopeName.html#shiny.pytest.ScopeName) | Pytest fixture scopes |

## Test server [Anchor](https://shiny.posit.co/py/api/testing/\#test-server)

Run a Shiny app’s server function in memory, without a browser.

|     |     |
| --- | --- |
| [testserver.test\_server](https://shiny.posit.co/py/api/testing/testserver.test_server.html#shiny.testserver.test_server) | Run a Shiny server function, Express app, or `shiny.App` in memory for testing. |
| [testserver.test\_server\_async](https://shiny.posit.co/py/api/testing/testserver.test_server_async.html#shiny.testserver.test_server_async) | The `async` counterpart to `test_server`, for use in `async` tests. |
| [testserver.TestServerSession](https://shiny.posit.co/py/api/testing/testserver.TestServerSession.html#shiny.testserver.TestServerSession) | An in-memory Shiny session driven from ordinary (non-async) test code. |
| [testserver.AsyncTestServerSession](https://shiny.posit.co/py/api/testing/testserver.AsyncTestServerSession.html#shiny.testserver.AsyncTestServerSession) | An in-memory Shiny session driven from async test code. |
| [testserver.TestServerScope](https://shiny.posit.co/py/api/testing/testserver.TestServerScope.html#shiny.testserver.TestServerScope) | A namespaced view of a `TestServerSession`. |
| [testserver.AsyncTestServerScope](https://shiny.posit.co/py/api/testing/testserver.AsyncTestServerScope.html#shiny.testserver.AsyncTestServerScope) | A namespaced view of an `AsyncTestServerSession`. |
| [testserver.TestServerValue](https://shiny.posit.co/py/api/testing/testserver.TestServerValue.html#shiny.testserver.TestServerValue) | One input, output, or exported value, and how it turned out. |
| [testserver.TestServerValues](https://shiny.posit.co/py/api/testing/testserver.TestServerValues.html#shiny.testserver.TestServerValues) | A point-in-time snapshot of a test session’s input, output, and export values. |
| [testserver.DEFAULT\_CLIENT\_DATA](https://shiny.posit.co/py/api/testing/testserver.DEFAULT_CLIENT_DATA.html#shiny.testserver.DEFAULT_CLIENT_DATA) | Stand-ins for what a browser would report, sent when the session starts. |

## Run [Anchor](https://shiny.posit.co/py/api/testing/\#run)

Methods for starting a local Shiny app in the background

|     |     |
| --- | --- |
| [run.run\_shiny\_app](https://shiny.posit.co/py/api/testing/run.run_shiny_app.html#shiny.run.run_shiny_app) | Run a Shiny app in a subprocess. |
| [run.ShinyAppProc](https://shiny.posit.co/py/api/testing/run.ShinyAppProc.html#shiny.run.ShinyAppProc) | Class that represents a running Shiny app process. |

## Deprecated [Anchor](https://shiny.posit.co/py/api/testing/\#deprecated)

|     |     |
| --- | --- |
| [playwright.controller.OutputTextVerbatim](https://shiny.posit.co/py/api/testing/playwright.controller.OutputTextVerbatim.html#shiny.playwright.controller.OutputTextVerbatim) | Deprecated. Use [`OutputCode`](https://shiny.posit.co/py/api/testing/playwright.controller.OutputCode.html#shiny.playwright.controller.OutputCode) instead. |