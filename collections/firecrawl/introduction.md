> ## Documentation Index
> Fetch the complete documentation index at: https://docs.firecrawl.dev/llms.txt
> Use this file to discover all available pages before exploring further.

# Introduction

> Search the web, scrape any page, and interact with it, all through one API.

export const McpClientSelector = () => {
  const writeClipboard = async text => {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch {
      const textarea = document.createElement("textarea");
      textarea.value = text;
      textarea.setAttribute("readonly", "");
      textarea.style.position = "fixed";
      textarea.style.top = "-9999px";
      document.body.appendChild(textarea);
      textarea.select();
      let copied = false;
      try {
        copied = document.execCommand("copy");
      } catch {
        copied = false;
      }
      document.body.removeChild(textarea);
      return copied;
    }
  };
  const mcpUrl = "https://mcp.firecrawl.dev/v2/mcp";
  const cursorInstallUrl = "cursor://anysphere.cursor-deeplink/mcp/install?name=firecrawl&config=eyJ1cmwiOiJodHRwczovL21jcC5maXJlY3Jhd2wuZGV2L3YyL21jcCJ9";
  const cursorConfig = `{
  "mcpServers": {
    "firecrawl": {
      "url": "${mcpUrl}"
    }
  }
}`;
  const opencodeConfig = `{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "firecrawl": {
      "type": "remote",
      "url": "${mcpUrl}",
      "enabled": true
    }
  }
}`;
  const clients = [{
    id: "claude-code",
    name: "Claude Code",
    detail: "Run in terminal",
    icon: "/images/agent-clients/claude-code.svg",
    iconClassName: "",
    command: `claude mcp add --transport http firecrawl ${mcpUrl}`,
    description: "Run this in your terminal to add Firecrawl as a remote MCP server in Claude Code.",
    hint: <>
          Then run <code>/mcp</code> and confirm <strong>firecrawl</strong> is connected.
        </>
  }, {
    id: "codex",
    name: "Codex",
    detail: "Run in terminal",
    icon: "/images/agent-clients/codex.svg",
    iconClassName: "",
    command: `codex mcp add firecrawl --url ${mcpUrl}`,
    description: "Run this in your terminal to add Firecrawl as a remote MCP server in Codex.",
    hint: <>
          Then run <code>codex mcp list</code> and confirm <strong>firecrawl</strong> is
          enabled.
        </>
  }, {
    id: "cursor",
    name: "Cursor",
    detail: "One-click + JSON",
    icon: "/images/agent-clients/cursor.svg",
    iconClassName: "fc-client-icon-mono",
    code: cursorConfig,
    codeLabel: "mcp.json",
    codeClassName: "",
    installUrl: cursorInstallUrl,
    description: "Install the hosted MCP server in one click, or copy the configuration below.",
    hint: <>
          Open <strong>Cursor Settings</strong>, select <strong>MCP</strong>, and confirm{" "}
          <strong>firecrawl</strong> is connected.
        </>
  }, {
    id: "opencode",
    name: "OpenCode",
    detail: "Copy config",
    icon: "/images/agent-clients/opencode.svg",
    iconClassName: "fc-client-icon-mono",
    code: opencodeConfig,
    codeLabel: "opencode.json",
    codeClassName: "",
    description: "Add this remote server configuration to your global or project config.",
    hint: <>
          Then run <code>opencode mcp list</code> and confirm{" "}
          <strong>firecrawl</strong> is connected.
        </>
  }];
  const [activeId, setActiveId] = useState(clients[0].id);
  const [copiedId, setCopiedId] = useState(null);
  const [status, setStatus] = useState("");
  const tabRefs = useRef([]);
  const timeoutRef = useRef(null);
  useEffect(() => () => window.clearTimeout(timeoutRef.current), []);
  const copy = async (id, text, label) => {
    const copied = await writeClipboard(text);
    if (copied) {
      window.clearTimeout(timeoutRef.current);
      setCopiedId(id);
      setStatus(`${label} copied to clipboard.`);
      timeoutRef.current = window.setTimeout(() => {
        setCopiedId(null);
        setStatus("");
      }, 2000);
    } else {
      setCopiedId(null);
      setStatus(`Could not copy ${label.toLowerCase()}.`);
    }
  };
  const copyIcon = () => <svg aria-hidden="true" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect width="14" height="14" x="8" y="8" rx="2" />
      <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2" />
    </svg>;
  const checkIcon = () => <svg aria-hidden="true" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="m20 6-11 11-5-5" />
    </svg>;
  const arrowIcon = () => <svg aria-hidden="true" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M5 12h14" />
      <path d="m13 6 6 6-6 6" />
    </svg>;
  const curvyCorners = () => {
    const path = "M11 1L11 11L10 11L10 7C10 3.68629 7.31371 1 4 1L0 1L0 0L11 0L11 1Z";
    return <span className="fc-curvy-corners" aria-hidden="true">
        <svg className="fc-curve fc-curve-tl" viewBox="0 0 11 11">
          <path d={path} />
        </svg>
        <svg className="fc-curve fc-curve-tr" viewBox="0 0 11 11">
          <path d={path} />
        </svg>
        <svg className="fc-curve fc-curve-bl" viewBox="0 0 11 11">
          <path d={path} />
        </svg>
        <svg className="fc-curve fc-curve-br" viewBox="0 0 11 11">
          <path d={path} />
        </svg>
      </span>;
  };
  const copyButton = ({id, text, label}) => {
    const copied = copiedId === id;
    return <button type="button" className={`fc-copy-button${copied ? " is-copied" : ""}`} onClick={() => copy(id, text, label)} aria-label={copied ? `${label} copied` : `Copy ${label}`}>
        {copied ? checkIcon() : copyIcon()}
        <span>{copied ? "Copied" : "Copy"}</span>
      </button>;
  };
  const commandRow = ({id, command, label, prompt}) => <div className="fc-command-row">
      <div className="fc-command-scroll" tabIndex={0}>
        {prompt && <span className="fc-command-prompt" aria-hidden="true">
            $
          </span>}
        <code>{command}</code>
      </div>
      {copyButton({
    id,
    text: command,
    label
  })}
    </div>;
  const codeBlock = ({client}) => <div className={`fc-code-block ${client.codeClassName || ""}`.trim()}>
      <div className="fc-code-header">
        <span>{client.codeLabel}</span>
        {copyButton({
    id: `code-${client.id}`,
    text: client.code,
    label: client.codeLabel
  })}
      </div>
      <pre>
        <code>{client.code}</code>
      </pre>
    </div>;
  const selectTab = index => {
    const client = clients[index];
    setActiveId(client.id);
    tabRefs.current[index]?.focus();
  };
  const handleKeyDown = (event, index) => {
    let nextIndex = index;
    if (event.key === "ArrowRight") nextIndex = (index + 1) % clients.length; else if (event.key === "ArrowLeft") nextIndex = (index - 1 + clients.length) % clients.length; else if (event.key === "Home") nextIndex = 0; else if (event.key === "End") nextIndex = clients.length - 1; else return;
    event.preventDefault();
    selectTab(nextIndex);
  };
  return <section className="fc-agent-first not-prose" aria-labelledby="fc-mcp-heading">
      {curvyCorners()}
      <div className="fc-agent-first-header">
        <div>
          <h3 id="fc-mcp-heading">Setup Firecrawl MCP Server</h3>
          <p>No API key required. Sign up only when you need more.</p>
        </div>
        <a className="fc-all-options-link" href="/mcp-server">
          See all setup options {arrowIcon()}
        </a>
      </div>

      <div className="fc-client-tabs" role="tablist" aria-label="Choose an MCP client">
        {clients.map((client, index) => {
    const selected = activeId === client.id;
    return <button key={client.id} id={`fc-tab-${client.id}`} ref={element => {
      tabRefs.current[index] = element;
    }} type="button" role="tab" className={`fc-client-tab${selected ? " is-active" : ""}`} aria-selected={selected} aria-controls={`fc-panel-${client.id}`} tabIndex={selected ? 0 : -1} onClick={() => setActiveId(client.id)} onKeyDown={event => handleKeyDown(event, index)}>
              <span className={`fc-client-icon ${client.iconClassName}`} style={{
      backgroundImage: `url("${client.icon}")`
    }} aria-hidden="true" />
              <span className="fc-client-tab-copy">
                <strong>{client.name}</strong>
                <span>{client.detail}</span>
              </span>
            </button>;
  })}
      </div>

      <div className="fc-client-panels">
        {clients.map(client => {
    const selected = activeId === client.id;
    return <div key={client.id} id={`fc-panel-${client.id}`} role="tabpanel" aria-labelledby={`fc-tab-${client.id}`} hidden={!selected} className="fc-client-panel">
              <p className="fc-client-description">{client.description}</p>
              {client.installUrl && <a className="fc-install-button" href={client.installUrl}>
                  Add to Cursor {arrowIcon()}
                </a>}
              {client.command ? commandRow({
      id: `code-${client.id}`,
      command: client.command,
      label: "Command",
      prompt: true
    }) : codeBlock({
      client
    })}
              <p className="fc-client-hint">{client.hint}</p>
            </div>;
  })}
      </div>
      <div className="fc-agent-first-footer">
        <p className="fc-footer-lead">Using another MCP client? Point it at:</p>
        {commandRow({
    id: "endpoint-url",
    command: mcpUrl,
    label: "Endpoint URL"
  })}
      </div>
      <span className="fc-sr-only" aria-live="polite">
        {status}
      </span>
    </section>;
};

export const AgentSetupButton = () => {
  const prompt = "Read and follow https://www.firecrawl.dev/agent-onboarding/SKILL.md";
  const writeClipboard = async text => {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch {
      const textarea = document.createElement("textarea");
      textarea.value = text;
      textarea.setAttribute("readonly", "");
      textarea.style.position = "fixed";
      textarea.style.top = "-9999px";
      document.body.appendChild(textarea);
      textarea.select();
      let copied = false;
      try {
        copied = document.execCommand("copy");
      } catch {
        copied = false;
      }
      document.body.removeChild(textarea);
      return copied;
    }
  };
  const [copied, setCopied] = useState(false);
  const [status, setStatus] = useState("");
  const timeoutRef = useRef(null);
  useEffect(() => () => window.clearTimeout(timeoutRef.current), []);
  const copyPrompt = async () => {
    const copied = await writeClipboard(prompt);
    if (copied) {
      window.clearTimeout(timeoutRef.current);
      setCopied(true);
      setStatus("Agent setup prompt copied to clipboard.");
      timeoutRef.current = window.setTimeout(() => {
        setCopied(false);
        setStatus("");
      }, 2000);
    } else {
      setCopied(false);
      setStatus("Could not copy the agent setup prompt.");
    }
  };
  const icon = copied ? <svg aria-hidden="true" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="m20 6-11 11-5-5" />
    </svg> : <svg aria-hidden="true" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect width="14" height="14" x="8" y="8" rx="2" />
      <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2" />
    </svg>;
  return <div className="fc-agent-prompt not-prose">
      <button type="button" className={`fc-agent-prompt-button${copied ? " is-copied" : ""}`} onClick={copyPrompt} aria-label={copied ? "Copied agent setup prompt" : "Setup for agents"}>
        {icon}
        <span>{copied ? "Copied" : "Setup for agents"}</span>
      </button>
      <span className="fc-sr-only" aria-live="polite">
        {status}
      </span>
    </div>;
};

<Note>
  **For AI agents:** Use [llms.txt](/llms.txt) for a full index of all documentation.
</Note>

## Get started

<McpClientSelector />

### Install the Firecrawl CLI

One command installs the Firecrawl CLI, authenticates in your browser, and adds skills to every detected coding agent.

```bash theme={null}
npx -y firecrawl-cli@latest init --all --browser
```

<Note>
  Restart your coding agent after setup so it can discover the new skills. See
  [Skills + CLI](/sdks/cli) for the full setup.
</Note>

### Set up with an agent

Provide your agent with this Firecrawl setup prompt.

<AgentSetupButton />

### Build and test directly

<CardGroup cols={2}>
  <Card title="Get your API key" icon="key" href="https://www.firecrawl.dev/app/api-keys">
    Create a free account for direct API access and higher limits
  </Card>

  <Card title="Try it in the Playground" icon="play" href="https://www.firecrawl.dev/playground">
    Test Firecrawl in the browser without writing code
  </Card>
</CardGroup>

***

## What can Firecrawl do?

<CardGroup cols={3}>
  <Card title="Search" icon="magnifying-glass" href="#search">
    Search the web and get full page content from results
  </Card>

  <Card title="Scrape" icon="file-lines" href="#scrape">
    Extract content from any URL as markdown, HTML, or structured JSON
  </Card>

  <Card title="Interact" icon="hand-pointer" href="#interact">
    Continue working with any scraped page: click, fill forms, extract dynamic
    content
  </Card>
</CardGroup>

### Why Firecrawl?

* **LLM-ready output**: Clean markdown, structured JSON, screenshots, and more.
* **Handles the hard stuff**: Proxies, anti-bot, JavaScript rendering, and dynamic content.
* **Reliable**: Built for production with high uptime and consistent results.
* **Fast**: Results in seconds, optimized for high throughput.
* **MCP Server**: Connect Firecrawl to any AI tool via the [Model Context Protocol](/mcp-server).

***

## Search

Search the web and get full page content from results in one call. See the [Search feature docs](/features/search) for all options.

<CodeGroup>
  ```python Python theme={null}
  from firecrawl import Firecrawl

  firecrawl = Firecrawl(
    # No API key needed to get started — add one for higher rate limits:
    # api_key="fc-YOUR-API-KEY",
  )

  results = firecrawl.search(
      query="firecrawl",
      limit=3,
  )
  print(results)
  ```

  ```js Node theme={null}
  import { Firecrawl } from 'firecrawl';

  const firecrawl = new Firecrawl({
    // No API key needed to get started — add one for higher rate limits:
    // apiKey: "fc-YOUR-API-KEY",
  });

  const results = await firecrawl.search('firecrawl', {
    limit: 3,
    scrapeOptions: { formats: ['markdown'] }
  });
  console.log(results);
  ```

  ```bash cURL theme={null}
  # No API key needed to get started — add -H "Authorization: Bearer $FIRECRAWL_API_KEY" for higher rate limits:
  curl -s -X POST "https://api.firecrawl.dev/v2/search" \
    -H "Content-Type: application/json" \
    -d '{
      "query": "firecrawl",
      "limit": 3
    }'
  ```

  ```bash CLI theme={null}
  # Search the web
  firecrawl search "firecrawl web scraping" --limit 5 --pretty
  ```
</CodeGroup>

<Accordion title="Response">
  SDKs will return the data object directly. cURL will return the complete payload.

  ```json JSON theme={null}
  {
    "success": true,
    "data": {
      "web": [
        {
          "url": "https://www.firecrawl.dev/",
          "title": "Firecrawl - The Web Data API for AI",
          "description": "The web crawling, scraping, and search API for AI. Built for scale. Firecrawl delivers the entire internet to AI agents and builders.",
          "position": 1
        },
        {
          "url": "https://github.com/firecrawl/firecrawl",
          "title": "mendableai/firecrawl: Turn entire websites into LLM-ready ... - GitHub",
          "description": "Firecrawl is an API service that takes a URL, crawls it, and converts it into clean markdown or structured data.",
          "position": 2
        },
        ...
      ],
      "images": [
        {
          "title": "Quickstart | Firecrawl",
          "imageUrl": "https://mintlify.s3.us-west-1.amazonaws.com/firecrawl/logo/logo.png",
          "imageWidth": 5814,
          "imageHeight": 1200,
          "url": "https://docs.firecrawl.dev/",
          "position": 1
        },
        ...
      ],
      "news": [
        {
          "title": "Y Combinator startup Firecrawl is ready to pay $1M to hire three AI agents as employees",
          "url": "https://techcrunch.com/2025/05/17/y-combinator-startup-firecrawl-is-ready-to-pay-1m-to-hire-three-ai-agents-as-employees/",
          "snippet": "It's now placed three new ads on YC's job board for “AI agents only” and has set aside a $1 million budget total to make it happen.",
          "date": "3 months ago",
          "position": 1
        },
        ...
      ]
    }
  }
  ```
</Accordion>

## Scrape

Scrape any URL and get its content in markdown, HTML, or other formats. See the [Scrape feature docs](/features/scrape) for all options.

<CodeGroup>
  ```python Python theme={null}
  from firecrawl import Firecrawl

  firecrawl = Firecrawl(
    # No API key needed to get started — add one for higher rate limits:
    # api_key="fc-YOUR-API-KEY",
  )

  # Scrape a website:
  doc = firecrawl.scrape("https://firecrawl.dev", formats=["markdown", "html"])
  print(doc)
  ```

  ```js Node theme={null}
  import { Firecrawl } from 'firecrawl';

  const firecrawl = new Firecrawl({
    // No API key needed to get started — add one for higher rate limits:
    // apiKey: "fc-YOUR-API-KEY",
  });

  // Scrape a website:
  const doc = await firecrawl.scrape('https://firecrawl.dev', { formats: ['markdown', 'html'] });
  console.log(doc);
  ```

  ```bash cURL theme={null}
  # No API key needed to get started — add -H "Authorization: Bearer $FIRECRAWL_API_KEY" for higher rate limits:
  curl -s -X POST "https://api.firecrawl.dev/v2/scrape" \
    -H "Content-Type: application/json" \
    -d '{
      "url": "https://firecrawl.dev",
      "formats": ["markdown", "html"]
    }'
  ```

  ```bash CLI theme={null}
  # Scrape a URL and get markdown
  firecrawl https://firecrawl.dev

  # With multiple formats (returns JSON)
  firecrawl https://firecrawl.dev --format markdown,html,links --pretty
  ```
</CodeGroup>

<Accordion title="Response">
  SDKs will return the data object directly. cURL will return the payload exactly as shown below.

  ```json theme={null}
  {
    "success": true,
    "data" : {
      "markdown": "Launch Week I is here! [See our Day 2 Release 🚀](https://www.firecrawl.dev/blog/launch-week-i-day-2-doubled-rate-limits)[💥 Get 2 months free...",
      "html": "<!DOCTYPE html><html lang=\"en\" class=\"light\" style=\"color-scheme: light;\"><body class=\"__variable_36bd41 __variable_d7dc5d font-inter ...",
      "metadata": {
        "title": "Home - Firecrawl",
        "description": "Firecrawl crawls and converts any website into clean markdown.",
        "language": "en",
        "keywords": "Firecrawl,Markdown,Data,Mendable,Langchain",
        "robots": "follow, index",
        "ogTitle": "Firecrawl",
        "ogDescription": "Turn any website into LLM-ready data.",
        "ogUrl": "https://www.firecrawl.dev/",
        "ogImage": "https://www.firecrawl.dev/og.png?123",
        "ogLocaleAlternate": [],
        "ogSiteName": "Firecrawl",
        "sourceURL": "https://firecrawl.dev",
        "statusCode": 200,
        "contentType": "text/html"
      }
    }
  }
  ```
</Accordion>

## Interact

Scrape a page, then keep working with it: click buttons, fill forms, extract dynamic content, or navigate deeper. Describe what you want in plain English or write code for full control. See the [Interact feature docs](/features/interact) for all options.

<CodeGroup>
  ```python Python theme={null}
  from firecrawl import Firecrawl

  app = Firecrawl(
    # No API key needed to get started — add one for higher rate limits:
    # api_key="fc-YOUR-API-KEY",
  )

  # 1. Scrape Amazon's homepage
  result = app.scrape("https://www.amazon.com", formats=["markdown"])
  scrape_id = result.metadata.scrape_id

  # 2. Interact — search for a product and get its price
  app.interact(scrape_id, prompt="Search for iPhone 16 Pro Max")
  response = app.interact(scrape_id, prompt="Click on the first result and tell me the price")
  print(response.output)

  # 3. Stop the session
  app.stop_interaction(scrape_id)
  ```

  ```js Node theme={null}
  import { Firecrawl } from 'firecrawl';

  const app = new Firecrawl({
    // No API key needed to get started — add one for higher rate limits:
    // apiKey: 'fc-YOUR-API-KEY',
  });

  // 1. Scrape Amazon's homepage
  const result = await app.scrape('https://www.amazon.com', { formats: ['markdown'] });
  const scrapeId = result.metadata?.scrapeId;

  // 2. Interact — search for a product and get its price
  await app.interact(scrapeId, { prompt: 'Search for iPhone 16 Pro Max' });
  const response = await app.interact(scrapeId, { prompt: 'Click on the first result and tell me the price' });
  console.log(response.output);

  // 3. Stop the session
  await app.stopInteraction(scrapeId);
  ```

  ```bash cURL theme={null}
  # 1. Scrape Amazon's homepage
  # No API key needed to get started — add -H "Authorization: Bearer $FIRECRAWL_API_KEY" for higher rate limits:
  RESPONSE=$(curl -s -X POST "https://api.firecrawl.dev/v2/scrape" \
    -H "Content-Type: application/json" \
    -d '{"url": "https://www.amazon.com", "formats": ["markdown"]}')

  SCRAPE_ID=$(echo $RESPONSE | jq -r '.data.metadata.scrapeId')

  # 2. Interact — search for a product and get its price
  curl -s -X POST "https://api.firecrawl.dev/v2/scrape/$SCRAPE_ID/interact" \
    -H "Content-Type: application/json" \
    -d '{"prompt": "Search for iPhone 16 Pro Max"}'

  curl -s -X POST "https://api.firecrawl.dev/v2/scrape/$SCRAPE_ID/interact" \
    -H "Content-Type: application/json" \
    -d '{"prompt": "Click on the first result and tell me the price"}'

  # 3. Stop the session
  curl -s -X DELETE "https://api.firecrawl.dev/v2/scrape/$SCRAPE_ID/interact"
  ```

  ```bash CLI theme={null}
  # 1. Scrape Amazon's homepage (scrape ID is saved automatically)
  firecrawl scrape https://www.amazon.com

  # 2. Interact — search for a product and get its price
  firecrawl interact "Search for iPhone 16 Pro Max"
  firecrawl interact "Click on the first result and tell me the price"

  # 3. Stop the session
  firecrawl interact stop
  ```
</CodeGroup>

<Accordion title="Response">
  ```json Response theme={null}
  {
    "success": true,
    "cdpUrl": "wss://browser.firecrawl.dev/...",
    "liveViewUrl": "https://liveview.firecrawl.dev/...",
    "interactiveLiveViewUrl": "https://liveview.firecrawl.dev/...",
    "output": "The iPhone 16 Pro Max (256GB) is priced at $1,199.00.",
    "exitCode": 0,
    "killed": false
  }
  ```
</Accordion>

***

## More capabilities

<CardGroup cols={2}>
  <Card title="Agent" icon="robot" href="/features/agent">
    Autonomous web data gathering powered by AI
  </Card>

  <Card title="Interact" icon="hand-pointer" href="/features/interact">
    Click, fill forms, extract dynamic content
  </Card>

  <Card title="Webhooks" icon="webhook" href="/webhooks">
    Async event delivery
  </Card>

  <Card title="Browser Sandbox" icon="browser" href="/features/browser">
    Managed browser sessions for interactive workflows
  </Card>

  <Card title="Map" icon="map" href="/features/map">
    Discover all URLs on a website
  </Card>

  <Card title="Crawl" icon="spider-web" href="/features/crawl">
    Recursively gather content from entire sites
  </Card>
</CardGroup>

***

## Resources

<CardGroup cols={2}>
  <Card title="API Reference" icon="code" href="/api-reference/v2-introduction">
    Complete API documentation with interactive examples
  </Card>

  <Card title="SDKs" icon="boxes-stacked" href="/sdks/overview">
    Python, Node.js, CLI, and community SDKs
  </Card>

  <Card title="Open Source" icon="github" href="/contributing/open-source-or-cloud">
    Self-host Firecrawl or contribute to the project
  </Card>

  <Card title="Integrations" icon="puzzle-piece" href="/developer-guides/llm-sdks-and-frameworks/openai">
    LangChain, LlamaIndex, OpenAI, and more
  </Card>
</CardGroup>
