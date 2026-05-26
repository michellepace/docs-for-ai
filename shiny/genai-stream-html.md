In this article, you’ll learn how to stream markdown/HTML content into your app via `MarkdownStream()`. This component is general purpose, but it’s particularly useful in a generative AI setting where displaying markdown strings _as it’s being generated_ is a common requirement.

Compared to [the `Chat()` component](https://shiny.posit.co/py/docs/genai-chatbots.html), `MarkdownStream()`’s API is simpler and focuses solely on a streaming display without the conversational UI elements. The possible experiences you can create around `MarkdownStream()` are vast, but as we’ll see shortly, a common pattern is populate a LLM prompt template based on user input.

## Get started [Anchor](https://shiny.posit.co/py/docs/genai-stream.html\#get-started)

### Choose a template [Anchor](https://shiny.posit.co/py/docs/genai-stream.html\#choose-a-template)

Pick from the following LLM providers below to start your streaming markdown app. Copy & paste the relevant `shiny create` terminal command to get the relevant source files on your machine.

- Ollama
- Anthropic
- OpenAI
- Google
- Bedrock Anthropic
- Azure OpenAI
- LangChain
- Other
- Help me choose!

```bash
shiny create --template stream-ai-ollama
```

```bash
shiny create --template stream-ai-anthropic
```

```bash
shiny create --template stream-ai-openai
```

```bash
shiny create --template stream-ai-gemini
```

```bash
shiny create --template stream-ai-anthropic-aws
```

```bash
shiny create --template stream-ai-azure-openai
```

```bash
shiny create --template stream-ai-langchain
```

`chatlas`’s supports a [wide variety](https://posit-dev.github.io/chatlas/#model-providers) of LLM providers including Vertex, Snowflake, Groq, Perplexity, and more. In this case, you can start from any template and swap out the `chat_client` with the relevant chat constructor (e.g., `ChatVertex()`).

If you’re not sure which provider to choose, `chatlas` provides a [great guide](https://posit-dev.github.io/chatlas/#model-choice) to help you decide.

When you run the `shiny create` command, you’ll be provided some tips on where to go to obtain the necessary API keys (if any) and how to securely get them into your app.

Also, if you’re not ready to sign up for a cloud provider (e.g., Anthropic, OpenAI, etc), you can run models locally (for free!) with the Ollama template. This is a great way to get started and learn about LLMs without any cost, and without sharing your data with a cloud provider.

Once your credentials (if any) are in place, [run the app](https://shiny.posit.co/py/docs/install-create-run.html#run). Congrats, you now have a streaming markdown interface powered by an LLM of your choice! 🎉

[![Screenshot of the streaming quick start app after a response has been generated.](https://shiny.posit.co/py/images/genai-stream-quick-start.png)](https://shiny.posit.co/py/images/genai-stream-quick-start.png "Screenshot of the streaming quick start app after a response has been generated.")

Screenshot of the streaming quick start app after a response has been generated.

### Inspect the code [Anchor](https://shiny.posit.co/py/docs/genai-stream.html\#inspect-the-code)

Go ahead and open the `app.py` file from your template, you’ll see something roughly like this:

- Express
- Core

```python
from chatlas import ChatOllama
from shiny import reactive
from shiny.express import input, ui

# Might instead be ChatAnthropic, ChatOpenAI, or some other provider
chat_client = ChatOllama(model="llama3.2")

with ui.sidebar():
    ui.input_select(
        "comic",
        "Choose a comedian",
        choices=["Jerry Seinfeld", "Ali Wong", "Mitch Hedberg"],
    )
    ui.input_action_button("go", "Tell me a joke", class_="btn-primary")

stream = ui.MarkdownStream(id="my_stream")
stream.ui(
    content="Press the button and I'll tell you a joke.",
)

@reactive.effect
@reactive.event(input.go)
async def do_joke():
    prompt = f"Pretend you are {input.comic()} and tell me a funny joke."
    response = await chat_client.stream_async(prompt)
    await stream.stream(response)
```

```python
from chatlas import ChatOllama
from shiny import App, reactive, ui

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_select(
            "comic",
            "Choose a comedian",
            choices=["Jerry Seinfeld", "Ali Wong", "Mitch Hedberg"],
        ),
        ui.input_action_button("go", "Tell me a joke"),
    ),
    ui.output_markdown_stream("my_stream"),
)

def server(input):
    stream = ui.MarkdownStream(id="my_stream")
    chat_client = ChatOllama(model="llama3.2")

    @reactive.effect
    @reactive.event(input.go)
    async def do_joke():
        prompt = f"Pretend you are {input.comic()} and tell me a funny joke."
        response = await chat_client.stream_async(prompt)
        await stream.stream(response)

app = App(app_ui, server)
```

From here, we can see the key requirements for streaming from an LLM:

1. Initialize a `chat_client` (e.g., `ChatOllama()`) to interact with the LLM.

   - [`chatlas`](https://posit-dev.github.io/chatlas/) isn’t required for this, but it’s highly recommended.
2. Initialize a `MarkdownStream()` component.
3. Display it’s UI element with `stream.ui()`.

   - Here you can specify initial content, sizing, and more.
4. Define the action which triggers the LLM to generate content.
   - In this case, it’s a button click that prompts the LLM to generate a joke.
   - Here, `chat_client` generates a `response` stream, which is passed along to the `.stream()` method for display.

In this article, our primary focus is the UI portion of the markdown stream (i.e., `stream`). That said, since LLM model choice and prompt design are so important for generating good responses, we’ll briefly touch on that first.

### Models & prompts [Anchor](https://shiny.posit.co/py/docs/genai-stream.html\#models-prompts)

With `chatlas`, it’s very easy to switch between the model and system prompt behind your `chat_client`. Just change the `model` and `system_prompt` parameters:

```python
chat_client = ChatOllama(
  model="llama3.2",
  system_prompt="You are a helpful assistant",
)
```

If you’re new to programming with LLMs, we **highly recommend** visiting the `chatlas` website for guidance on [where to start](https://posit-dev.github.io/chatlas/get-started.html), [choosing a model](https://posit-dev.github.io/chatlas/#model-choice), and [designing an effective system prompt](https://posit-dev.github.io/chatlas/prompt-design.html).

If you’re not yet ready learn about LLMs, that’s okay! We can still dive into `stream` UI features without knowing much about LLMs.

## Content APIs [Anchor](https://shiny.posit.co/py/docs/genai-stream.html\#content-apis)

### Starting content [Anchor](https://shiny.posit.co/py/docs/genai-stream.html\#starting-content)

Show content to the user when the `MarkdownStream()` UI is first displayed by providing a string to the `content` parameter in `stream.ui()`.

This is typically most useful for providing a welcome message or instructions to the user.

- Express
- Core

```python
stream.ui(
  content="Press the button and I'll tell you a joke."
)
```

```python
ui.output_markdown_stream(
  content="Press the button and I'll tell you a joke."
)
```

[![Screenshot of a starting content message.](https://shiny.posit.co/py/images/genai-stream-starting-content.png)](https://shiny.posit.co/py/images/genai-stream-starting-content.png "Screenshot of a starting content message.")

Screenshot of a starting content message.

### Appending content [Anchor](https://shiny.posit.co/py/docs/genai-stream.html\#appending-content)

When you `.stream()` content, you have the choice of whether or not to clear the existing content. By default, existing content is cleared, but you can instead append to the existing content by passing `clear=False` to `stream.stream()`.

```python
await stream.stream(response, clear=False)
```

### Content generators [Anchor](https://shiny.posit.co/py/docs/genai-stream.html\#content-generators)

In your starter template, the `response` stream is provided by [`chatlas`](https://posit-dev.github.io/chatlas/) via `chat_client.stream_async(prompt)`. As it turns out, that `response` object is an [generator](https://stackoverflow.com/q/1756096) of markdown strings, and the `.stream()` method can work with any generator of strings. This is useful to know if you want to:

1. Use another framework for reponse generation (e.g., [LangChain](https://www.langchain.com/)).
2. Transform the stream as it’s being generated (e.g., highlight keywords).
3. Manually create a generator (to say, show progress on a [non-blocking task](https://shiny.posit.co/py/docs/nonblocking.html)).

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

import asyncio

from shiny import reactive

from shiny.express import input, ui

ui.input\_action\_button("do\_stream", "Do stream", class\_="btn btn-primary")

stream = ui.MarkdownStream("stream")

stream.ui()

asyncdefsimple\_generator():

yield"Hello "

await asyncio.sleep(1)

yield"\`MarkdownStream()\`!"

@reactive.effect

@reactive.event(input.do\_stream)

asyncdef\_():

await stream.stream(simple\_generator())

### Content types [Anchor](https://shiny.posit.co/py/docs/genai-stream.html\#content-types)

`MarkdownStream()` supports several different content types through the `content_type` parameter. The default `markdown` content type is the most broadly useful, since it not only parses and renders markdown strings, but also renders HTML content.

- `markdown`: render markdown (specifically CommonMark) as HTML.

  - Currently, you can’t customize the markdown renderer. If you need to customize, apply `ui.markdown()` to the content before streaming.
- `html`: render a string of HTML as HTML.
- `text`: render a string of plain text verbatim.
- `semi-markdown`: render a string of markdown as HTML, but with HTML tags escaped.

### Interactive content [Anchor](https://shiny.posit.co/py/docs/genai-stream.html\#interactive-content)

[Similar to `Chat()`](https://shiny.posit.co/py/docs/genai-chatbots.html#interactive-messages), `MarkdownStream()` supports interactive content, meaning that content can include Shiny UI elements like [inputs](https://shiny.posit.co/py/components/#inputs), [outputs](https://shiny.posit.co/py/components/#outputs), etc. This allows you to collect user input, display rich interactive output (e.g., [Jupyter Widgets](https://shiny.posit.co/py/docs/jupyter-widgets.html)), or provide additional context (e.g. [tooltips](https://shiny.posit.co/py/components/display-messages/tooltips/)) from within the message stream.

For a basic example, here’s a startup message with an input field:

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

with ui.hold() as welcome:

"\*\*Hello!\*\* What's your name?"

ui.input\_text("name", None, placeholder="Enter name here")

chat = ui.Chat(id="chat")

chat.ui(messages=\[welcome\])

Interactive tool displays

Probably the most interesting way in which interactive messages can be used is from a custom [tool call](https://shiny.posit.co/py/docs/genai-tools.html) display. For example, you could have a tool that displays a [Data Grid](https://shiny.posit.co/py/components/outputs/data-grid/) or [Jupyter Widget](https://shiny.posit.co/py/docs/jupyter-widgets.html) (e.g., a [plotly](https://shiny.posit.co/py/components/outputs/plot-plotly/) graph).

## Card layout [Anchor](https://shiny.posit.co/py/docs/genai-stream.html\#card-layout)

When embedding a stream within a larger app, it’s often useful to place it within a `ui.card()`. This provides a clear visual separation between the stream and other content, and allows you to easily add a header, footer, or other elements around the stream.

In this case, it’s also useful to know that a sidebar layout can also placed within a card:

- Express
- Core

```python
from shiny.express import ui

# Get the card to fill the page
ui.page_opts(
    fillable=True,
    fillable_mobile=True,
    class_="bg-light-subtle",
)

# Create and display a MarkdownStream()
stream = ui.MarkdownStream(id="my_stream")

with ui.card():
    ui.card_header("Streaming Joke Generator")

    # Put sidebar layout in the card
    with ui.layout_sidebar():
        with ui.sidebar():
            ui.input_select(
                "comic",
                "Choose a comedian",
                choices=["Jerry Seinfeld", "Ali Wong", "Mitch Hedberg"],
                width="auto",
            )
            ui.input_action_button("go", "Tell me a joke", class_="btn-primary")

        stream.ui(content="Press the button and I'll tell you a joke.")
```

```python
from shiny import ui, App
from faicons import icon_svg

app_ui = ui.page_fillable(
    ui.card(
        ui.card_header("Streaming Joke Generator"),
        ui.layout_sidebar(
            ui.sidebar(
                ui.input_select(
                    "comic",
                    "Choose a comedian",
                    choices=["Jerry Seinfeld", "Ali Wong", "Mitch Hedberg"],
                    width="auto",
                ),
                ui.input_action_button("go", "Tell me a joke", class_="btn-primary"),
            ),
            ui.output_markdown_stream("stream", content="Press the button and I'll tell you a joke."),
        ),
    ),
    fillable_mobile=True,
    class_="bg-light",
)

def server(input):
    stream = ui.MarkdownStream(id="stream")

app = App(app_ui, server)
```

[![Screenshot of a stream within a card layout.](https://shiny.posit.co/py/images/genai-stream-card-layout.png)](https://shiny.posit.co/py/images/genai-stream-card-layout.png "Screenshot of a stream within a card layout.")

Screenshot of a stream within a card layout.

Multi-card layout

If you want multiple cards in an app, it’s useful to know about Shiny’s [grid layout options](https://shiny.posit.co/py/layouts/arrange/#).

Auto-scroll

A nice result of placing a stream in a card is that when it overflows the card (either because it has a specified height or because it’s in a fillable page), the card will automatically scroll to show the new content.

This can be disabled by setting `auto_scroll=False` when creating the UI element.

## Non-blocking streams [Anchor](https://shiny.posit.co/py/docs/genai-stream.html\#non-blocking-streams)

[Similar to `Chat()`](https://shiny.posit.co/py/docs/genai-chatbots.html#non-blocking-streams)’s `.append_message_stream()`, `MarkdownStream()`’s `.stream()` launches a non-blocking [extended task](https://shiny.posit.co/py/docs/nonblocking.html). This allows the app to be responsive while the AI generates the response, even when multiple concurrent users are on a single Python process.

A few other benefits of an extended task is that they make it easy to:

1. Reactively read for the `.result()`.
2. Reactively read for the `.status()`.
3. `.cancel()` the stream.

To grab the latest message stream, read the `.latest_stream` property on the `stream` object. This property always points to the most recent stream, making it easy to work with it in a reactive context. Here’s an example of reactively reading the status and result of the latest stream:

app.py×app\_utils.py×+

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

from app\_utils import stream\_generator

from shiny import reactive

from shiny.express import input, render, ui

stream = ui.MarkdownStream("stream")

ui.input\_action\_button("start\_stream", "Start stream", class\_="btn-primary")

@render.code

defstream\_status():

returnf"Status: {stream.latest\_stream.status()}"

stream.ui(content="Press the button to start streaming.")

@render.text

asyncdefstream\_result():

returnf"Result: {stream.latest\_stream.result()}"

@reactive.effect

@reactive.event(input.start\_stream)

asyncdef\_():

await stream.stream(stream\_generator())

Providing good UI/UX for canceling a stream is a bit more involved, but it can be done with a button that cancels the stream and notifies the user. See the example below for an approach to this:

Stream cancellation

app.py×app\_utils.py×+

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

from app\_utils import stream\_generator

from shiny import reactive

from shiny.express import input, ui

with ui.layout\_column\_wrap():

ui.input\_action\_button(

"do\_stream",

"Start stream",

class\_="btn btn-primary",

)

ui.input\_action\_button(

"cancel",

"Cancel stream",

class\_="btn btn-danger",

)

stream = ui.MarkdownStream("stream")

stream.ui(content="Press the button to start streaming.")

@reactive.effect

@reactive.event(input.do\_stream)

asyncdef\_():

await stream.stream(stream\_generator())

@reactive.effect

@reactive.event(input.cancel)

def\_():

stream.latest\_stream.cancel()

ui.notification\_show("Stream cancelled", type="warning")

@reactive.effect

def\_():

ui.update\_action\_button(

"cancel", disabled=stream.latest\_stream.status() != "running"

)

## Troubleshooting [Anchor](https://shiny.posit.co/py/docs/genai-stream.html\#troubleshooting)

### Error handling [Anchor](https://shiny.posit.co/py/docs/genai-stream.html\#error-handling)

Usually, when an error occurs in a `reactive.effect`, the error crashes the app, forcing the user to refresh the page. This behavior is intentional since, when an error occurs in a `reactive.effect`, the user isn’t notified of the error, and the app is in an unknown state.

Since LLM response generation can be flaky (e.g., due to rate/context limits, network issues, etc), you may want to handle errors during response more gracefully.

As it turns out, when an error occurs _inside_ a `.stream()`, the error is caught and re-thrown by a special `NotifyException` which notifies the user of the error, and allows the app to continue running. When running locally, the actual error message is shown, but in production, only a generic message is shown (i.e., the error is sanitized since it may contain sensitive information).

[![Screenshot of a chatbot with an error message.](https://shiny.posit.co/py/images/genai-stream-errors.png)](https://shiny.posit.co/py/images/genai-stream-errors.png "Screenshot of a chatbot with an error message.")

Screenshot of a chatbot with an error message.

This is should be good enough to catch most errors that occur during response generation. However, it’s also good to be aware though that other errors that might occur elsewhere in a `reactive.effect` will still crash the app. If you’d like to protect against this, you can wrap them in a `try`/`except` block, and re-raise the error as a `NotifyException`, like this:

```python
from shiny.types import NotifyException
from shiny import reactive

@reactive.effect
@reactive.event(input.go)
async def do_joke():
    try:
        prompt = f"Pretend you are {input.comic()} and tell me a funny joke."
        response = await chat_client.stream_async(prompt)
    except Exception as e:
        raise NotifyException(f"An error occurred in do_joke: {e}") from e
    await stream.stream(response)
```

Customized error handling

If you’d like to customize how `MarkdownStream()` handles errors, you can do so by setting the `on_error` parameter in the constructor. See [the documentation](https://shiny.posit.co/py/api/ui.MarkdownStream.html).

### Debugging [Anchor](https://shiny.posit.co/py/docs/genai-stream.html\#debugging)

Sometimes response generation from an LLM might not be quite what you expect, leaving you to wonder what went wrong. With `chatlas`, your primary interactive debugging tool is to set `echo="all"` in the `.stream_async()` method to see the context of the chat history (emitted to your Python console). For lower-level debugging, you can also enable logging and/or access the full chat history via the `chat_client.get_turns()` method. For more, see `chatlas`’ [troubleshooting guide](https://posit-dev.github.io/chatlas/#troubleshooting).

Monitoring in production

Since `chatlas` builds on top of official Python SDKs like `openai` and `anthropic`, [monitoring](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/monitor-openai) solutions that integrate with their [logging](https://github.com/openai/openai-python?tab=readme-ov-file#logging) mechanism can be used to monitor and debug your chatbot in production.

## Next steps [Anchor](https://shiny.posit.co/py/docs/genai-stream.html\#next-steps)

The [next article](https://shiny.posit.co/py/docs/genai-stream.html) covers a very useful technique for both [chatbots](https://shiny.posit.co/py/docs/genai-chatbots.html) and streaming markdown: [tool calling](https://shiny.posit.co/py/docs/genai-tools.html).

Skip to other articles in the series if you want to learn about other generally useful Generative AI techniques like [tool calls](https://shiny.posit.co/py/docs/genai-tools.html), [structured output](https://shiny.posit.co/py/docs/genai-structured-data.html), and [RAG](https://shiny.posit.co/py/docs/genai-rag.html).
