> ## Documentation Index
> Fetch the complete documentation index at: https://docs.coderabbit.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Plans and pricing

> Compare CodeRabbit plans and understand per-developer review rate limits and feature limits.

export const Hint = ({type, children, headline, tip, href, cta}) => {
  const TIPS = {
    learnings: {
      headline: "Learnings",
      tip: "Review preferences CodeRabbit learns from your chat conversations and applies automatically to future reviews.",
      cta: "Learn about Learnings",
      href: "/knowledge-base/learnings",
      content: "Learnings"
    },
    walkthrough: {
      headline: "PR Walkthrough",
      tip: "A structured comment posted by CodeRabbit at the top of every pull request, summarizing changes, sequence diagrams, review effort, and more.",
      cta: "Learn about PR Walkthroughs",
      href: "/pr-reviews/walkthroughs",
      content: "Walkthrough"
    },
    "finishing-touches": {
      headline: "Finishing Touches",
      tip: "Post-review agentic actions (Autofix, writing docstrings or unit tests, and more) you trigger from a PR comment or a checkbox in the Walkthrough.",
      cta: "See all Finishing Touches",
      href: "/finishing-touches",
      content: "Finishing Touches"
    },
    "coding-plan": {
      headline: "Coding Plan",
      tip: "A detailed, codebase-aware implementation plan CodeRabbit generates from an issue or description, ready to hand off to any coding agent.",
      cta: "Learn about Coding Plans",
      href: "/plan",
      content: "Coding Plan"
    },
    "knowledge-base": {
      headline: "Knowledge Base",
      tip: "The collected context sources CodeRabbit draws on during reviews: Learnings, Code Guidelines, issue trackers, connected MCP servers, and cross-repo analysis.",
      cta: "Explore the Knowledge Base",
      href: "/knowledge-base",
      content: "Knowledge Base"
    },
    "path-instructions": {
      headline: "Path Instructions",
      tip: "Custom review rules that only apply to files matching a glob pattern, e.g. 'src/controllers/**'.",
      cta: "Configure path instructions",
      href: "/configuration/path-instructions",
      content: "Path Instructions"
    },
    "change-stack": {
      headline: "Change Stack",
      tip: "An improved code inspection interface that reorganizes a pull request from a flat file list into a structured, layer-by-layer walkthrough with range-specific summaries and diagrams when useful.",
      cta: "Learn about Change Stack",
      href: "/pr-reviews/change-stack",
      content: "Change Stack"
    },
    scope: {
      headline: "Scope",
      tip: "A named set of repositories, connections, and spend limits that controls what CodeRabbit Agent can access in a given Slack conversation.",
      cta: "Learn about Scopes",
      href: "/slack-agent/scopes",
      content: "Scope"
    },
    "coderabbit-agent": {
      headline: "CodeRabbit Agent for Slack",
      tip: "An AI agent built into Slack that investigates issues, generates implementation plans, and opens pull requests right from the Slack threads.",
      cta: "Explore CodeRabbit Agent",
      href: "/slack-agent",
      content: "CodeRabbit Agent"
    },
    "configuration-inheritance": {
      headline: "Configuration Inheritance",
      tip: "A setting that merges configuration values across multiple levels — repository YAML, central YAML, and UI settings — instead of using only the highest-priority source.",
      cta: "Learn about Configuration Inheritance",
      href: "/configuration/configuration-inheritance",
      content: "Configuration Inheritance"
    }
  };
  const defaults = TIPS[type] || ({});
  return <Tooltip headline={headline ?? defaults.headline} tip={tip ?? defaults.tip} cta={cta ?? defaults.cta} href={href ?? defaults.href}>
      {children ?? defaults.content}
    </Tooltip>;
};

CodeRabbit offers five plans with per-developer review rate limits; **Pro**, **Pro+**, and **Enterprise** subscribers can also enable the [usage-based add-on](/management/usage-based-addon) to pay for usage beyond those limits.

This page covers what each plan includes, the review rate limits enforced **per developer**, and feature limits that vary by plan.

## Plans

<CardGroup cols={1}>
  <Card icon="gift" horizontal>
    ### Free plan

    Unlimited public and private repositories, no credit card required.

    PR summarization only, code reviews are available via the VS Code extension and CLI. Includes a **14-day Pro+ trial**. When the trial expires, choose Pro or Pro+ to continue, or revert to Free with lower [rate limits](#rate-limits).
  </Card>

  <Card icon="code" horizontal>
    ### Open source

    Unlimited public repositories, no credit card required.

    Open-source projects receive Pro+ features with no paid subscription required. OSS reviews use a separate rate-limit tier that varies with the project's community and popularity; see [Rate limits](#rate-limits).
  </Card>

  <Card icon="shield-check" horizontal>
    ### Pro plan

    **\$24 per developer per month** billed annually, or **\$30** month-to-month.

    Includes everything in Free, plus PR reviews, higher rate limits, integration, Knowledge base, linter and SAST tool support, analytics, docstrings, autofix, and [usage-based add-on](/management/usage-based-addon) access.
  </Card>

  <Card icon="shield-plus" horizontal>
    ### Pro+ plan

    **\$48 per developer per month** billed annually, or **\$60** month-to-month.

    Everything in Pro, plus tasks and actions upstream and downstream of the review process: [CodeRabbit Plan](/plan/index) and issue planning, unit test generation, merge conflict resolution, and other pre/post-merge actions. Pro+ also offers higher [rate limits](#rate-limits).
  </Card>

  <Card icon="building-2" horizontal>
    ### Enterprise plan

    **Contact sales** — [coderabbit.ai/contact-us/sales](https://www.coderabbit.ai/contact-us/sales)

    Includes everything in Pro+, plus self-hosting options, multi-organization support, SSO, SLA support with a dedicated Customer Success Manager, AWS and GCP Marketplace billing, API access, custom RBAC, and audit logging.
  </Card>
</CardGroup>

## Rate limits

The following review and chat limits are enforced **per developer** over rolling time windows. Each one is a rolling allowance rather than a one-time quota: you can use your full hourly amount in a burst, and additional reviews become available as earlier reviews age out of the window instead of resetting all at once at the top of the hour. For example, Pro includes 5 PR reviews per hour.

The **Files/review** column is the maximum number of files CodeRabbit reviews in a single review, not an hourly limit. The files per review are counted after path filter exclusions.

| Plan       | PR   | IDE | CLI | Files/review | Chat |
| ---------- | ---- | --- | --- | ------------ | ---- |
| Free       | 1    | 3   | 3   | 150          | N/A  |
| OSS        | 1–10 | 1   | 3   | 50–150       | 25   |
| Pro        | 5    | 5   | 5   | 150          | 50   |
| Pro+       | 10   | 10  | 10  | 300          | 100  |
| Enterprise | 12   | 12  | 12  | 300          | 100  |

PR, IDE, and CLI columns are reviews per developer per hour. Free PR reviews are summaries only. OSS PR review and file limits vary by project community and popularity. For sustained high-volume PR review activity, review availability may adjust under the [Fair Usage Limits Policy](#fair-usage-limits-policy).

Pro, Pro+, and Enterprise organizations can enable the [usage-based add-on](/management/usage-based-addon) (subject to billing-method eligibility) to continue processing eligible over-limit reviews without interruption.

The file limits in the table apply to pull request and merge request reviews after path filters are applied. When an eligible GitHub or GitHub Enterprise review exceeds its included file limit but contains no more than 300 files, CodeRabbit can offer a **Review on demand using usage pricing** action. Reviews with more than 300 files are not supported through usage pricing.

Each PR review run uses one PR review from this allowance, including automatic incremental reviews after new pushes, manual `@coderabbitai review`, and manual `@coderabbitai full review`. To check your own PR review limit without starting a new review, comment `@coderabbitai rate limit` or ask a clear question like `@coderabbitai reviews remaining?`.

<Info>
  When no PR reviews are available, CodeRabbit pauses new reviews until more reviews become available or eligible over-limit reviews continue through the usage-based add-on.
</Info>

### Default Pro+ trial limits

The default 14-day trial starts on **Pro+**. The limits below apply to that default Pro+ trial experience.

| Category                                                                      | Default Pro+ trial |
| ----------------------------------------------------------------------------- | ------------------ |
| PR reviews per developer per hour                                             | 10                 |
| Files per pull request or merge request                                       | 300                |
| [Custom Finishing Touch recipes](/finishing-touches/custom-finishing-touches) | 20                 |
| [Custom Pre-Merge Checks](/pr-reviews/custom-checks)                          | 20                 |
| [Linked repositories](/knowledge-base/multi-repo-analysis)                    | 10                 |

The default Pro+ trial also includes access to <Hint type="finishing-touches" />
, [Pre-Merge Checks](/pr-reviews/pre-merge-checks), and [CodeRabbit Plan](/issue
s/planner).

### Fair Usage Limits Policy

CodeRabbit's PR review limits are designed for modern development workflows where humans, coding agents, and automation may all request reviews. Each PR review uses compute. Fair usage limits keep review capacity reliable and economically sustainable for all customers.

Your plan allowance is not changed. Pro includes 5 PR reviews per hour, Pro+ includes 10 PR reviews per hour, and Enterprise uses the rate shown in the table above. During typical usage, reviews become available at the normal plan rate. When one developer identity reaches the 95th percentile or higher of recent CodeRabbit PR review usage, CodeRabbit gradually spaces out additional reviews for that developer.

Reducing or pausing review activity lets recent usage come down over time, which can restore faster review availability.

The following limits apply per developer identity in an organization:

<Tabs>
  <Tab title="Pro" icon="shield-check">
    | Recent PR review activity        | Review availability                 |
    | -------------------------------- | ----------------------------------- |
    | 0-29 reviews in the last 7 days  | 5 reviews/hour                      |
    | 30-39 reviews in the last 7 days | 4 reviews/hour                      |
    | 40-49 reviews in the last 7 days | 3 reviews/hour                      |
    | 50-59 reviews in the last 7 days | 2 reviews/hour                      |
    | 60+ reviews in the last 7 days   | 1 review/hour, one review at a time |
  </Tab>

  <Tab title="Pro+" icon="shield-plus">
    | Recent PR review activity        | Review availability                 |
    | -------------------------------- | ----------------------------------- |
    | 0-29 reviews in the last 7 days  | 10 reviews/hour                     |
    | 30-39 reviews in the last 7 days | 8 reviews/hour                      |
    | 40-49 reviews in the last 7 days | 6 reviews/hour                      |
    | 50-59 reviews in the last 7 days | 5 reviews/hour                      |
    | 60-69 reviews in the last 7 days | 4 reviews/hour                      |
    | 70-79 reviews in the last 7 days | 3 reviews/hour                      |
    | 80-89 reviews in the last 7 days | 2 reviews/hour                      |
    | 90+ reviews in the last 7 days   | 1 review/hour, one review at a time |
  </Tab>
</Tabs>

### When a review is rate-limited

When a push is rate-limited, CodeRabbit posts a rate-limit comment on the pull request and a passing check titled **"Review rate limited"** — the check passes by design so it never blocks merging on protected branches. The comment is the authoritative signal that no review ran. A previously approved PR keeps its approval.

Comment `@coderabbitai rate limit` to see remaining capacity, then `@coderabbitai review` to trigger a review once capacity is restored.

<Info>
  A blocked push does not consume a review or delay when your next review becomes available. Capacity is limited by earlier reviews in the rolling window, not by the current push.
</Info>

#### How to continue with credits

If your team expects sustained high-volume review activity, buy on-demand credits and enable the [usage-based add-on](/management/usage-based-addon). Eligible over-limit PR reviews can then continue without waiting for the next included review to become available.

#### How to avoid reaching limits

Reduce unnecessary automatic reviews before relying on credits:

* Set [`reviews.auto_review.auto_pause_after_reviewed_commits`](/configuration/auto-review#auto_pause_after_reviewed_commits) to `1` or `2` so CodeRabbit pauses automatic incremental reviews earlier.
* Use [label-based opt-in](/configuration/auto-review#labels) so CodeRabbit reviews only PRs marked ready for review.
* Use [title-based exclusions](/configuration/auto-review#ignore_title_keywords) for WIP, generated, or automation-heavy PRs.
* Turn off automatic reviews for noisy repositories and request reviews manually when the PR is ready.

## Feature limits

Some features have per-plan limits that are separate from the rate limits above.

### Linked repositories

[Multi-Repo Analysis](/knowledge-base/multi-repo-analysis) lets CodeRabbit detect cross-repository breaking changes during reviews. The number of linked repositories you can activate depends on your plan:

| Free | Pro | Pro+ | Enterprise |
| ---- | --- | ---- | ---------- |
| 0    | 1   | 10   | 20         |

For details on how limits are enforced when your configuration exceeds your plan's allowance, see [Multi-Repo Analysis — Plan limits](/knowledge-base/multi-repo-analysis#plan-limits).

### MCP servers

[MCP server](/integrations/mcp-servers) connections let CodeRabbit pull in richer context from your external tools during reviews. The number of MCP server connections you can configure depends on your plan:

| Pro | Pro+ | Enterprise |
| --- | ---- | ---------- |
| 5   | 15   | 20         |

### Custom Finishing Touch recipes

[Custom Finishing Touch recipes](/finishing-touches/custom-finishing-touches) let you define your own post-review automation. The number of custom recipes you can define per repository depends on your plan:

| Pro+ | Enterprise |
| ---- | ---------- |
| 20   | 20         |

### Custom Pre-Merge Checks

[Custom Pre-Merge Checks](/pr-reviews/custom-checks) let you define organization-specific gating checks. The number of custom checks you can define per organization depends on your plan:

| Pro+ | Enterprise |
| ---- | ---------- |
| 20   | 20         |

## What's next

<CardGroup cols={1}>
  <Card title="Manage your subscription" href="/management/billing" icon="credit-card" horizontal>
    View invoices, change your subscription plan, and adjust seat counts
  </Card>

  <Card title="Seat assignment" href="/management/seat-assignment" icon="users" horizontal>
    Control how CodeRabbit assigns seats to team members automatically or manually
  </Card>

  <Card title="Pricing page" href="https://coderabbit.ai/pricing" icon="tag" horizontal>
    See the full plan comparison and contact sales for Enterprise pricing
  </Card>
</CardGroup>
