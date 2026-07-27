> ## Documentation Index
> Fetch the complete documentation index at: https://docs.coderabbit.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# CodeRabbit glossary: review, Git, and code analysis terms

> Definitions of CodeRabbit product terms, Git platform terminology across GitHub, GitLab, Bitbucket, and Azure DevOps, and common code review concepts.

This glossary covers terms specific to CodeRabbit, Git platform terminology that varies across GitHub, GitLab, Bitbucket, and Azure DevOps, and general software engineering concepts referenced in the documentation.

## CodeRabbit terms

### Code Guidelines

Files in your repository that describe your team's coding standards, such as `.cursorrules`, `CLAUDE.md`, or `AGENTS.md`. CodeRabbit reads these files and applies them as review criteria. Different from [Path-based Instructions](#path-based-instructions), which are rules you write directly in CodeRabbit's settings.

See [Knowledge Base](/knowledge-base).

### Finishing Touches

Automated actions in the PR for common cleanup tasks like generating docstrings and writing unit tests. Triggered through a checkbox in the [Walkthrough](#walkthrough) or by commenting `@coderabbitai`.

See [Docstrings](/finishing-touches/docstrings) and [Unit tests](/finishing-touches/unit-test-generation).

### Fortune

A random fun fact, tip, or trivia message displayed in the [Walkthrough](#walkthrough) while CodeRabbit is still processing the review. Replaced by the actual review summary content once complete. Named after the Unix `fortune` command.

### High-Level Summary

An AI-generated summary of a PR's purpose and key changes, written for human reviewers. By default appears in the PR description (at the end unless a placeholder string specifies a precise injection place) and can be moved to the [Walkthrough](#walkthrough) comment.

### Incremental Review

When new commits are pushed to a PR that has already been reviewed, CodeRabbit can re-review focusing on just the new changes rather than starting from scratch. This avoids repeating comments already made on previous commits.

### Knowledge Base

The collected context CodeRabbit draws on during reviews. This includes [Learnings](#learnings) from past review conversations, issues from your tracker, past PRs, [Code Guidelines](#code-guidelines) files, and integrations with Jira, Linear, and [MCP](#mcp) servers.

See [Knowledge Base](/knowledge-base).

### Learnings

When you respond to CodeRabbit's review comments (for example, "we prefer early returns over try-catch in this repo"), CodeRabbit remembers that preference and applies it to future reviews. These remembered preferences are called learnings. They can be scoped to a single repository or shared across your organization.

See [Learnings](/knowledge-base/learnings).

### Security Repository Learnings

Accepted-risk guidance saved when a code vulnerability is ignored. Security Agent can reuse this guidance in later scans to suppress equivalent findings when their behavior and file or repository scope match. Security repository Learnings are separate from the [Learnings](#learnings) used in pull request reviews.

See [Security Agent](/security-agent).

### Path Filters

Glob patterns that control which files CodeRabbit includes in or excludes from a review. For example, `!dist/**` excludes all files in the `dist` folder, and `!*.lock` excludes lock files. Files not matching any exclude pattern are included by default.

### Path-based Instructions

Custom review rules that only apply to files matching a [glob pattern](#glob-pattern). For example, you can tell CodeRabbit to "ensure all tests have meaningful descriptions" only for files matching `**/*.test.ts`. Different from [Code Guidelines](#code-guidelines), which are reference documents CodeRabbit reads.

See [Review instructions](/configuration/path-instructions).

### Pre-Merge Checks

Validation rules CodeRabbit evaluates before a PR is merged. Built-in checks include [docstring](#docstring) coverage, PR title quality, PR description completeness, and linked issue assessment. You can also define custom checks with your own pass/fail criteria.

See [Pre-merge checks](/pr-reviews/pre-merge-checks).

### Profile

Controls how much feedback CodeRabbit gives you and how strict its standards are. Think of it as a volume knob for review comments.

* **Quiet** posts only the most important comments inline — critical and major issues that are also high-impact — and groups everything else into collapsed sections in the review summary, so your pull request conversation stays focused without losing any feedback.
* **Chill** focuses on important issues — you get fewer, higher-signal comments focused on bugs, security issues, and essential fixes.
* **Assertive** provides comprehensive feedback with more comments overall, including style, best practices, and minor improvements.

### Request Changes Workflow

A two-step automation: when CodeRabbit finds issues, it submits a "Request changes" review on GitHub to signal the PR needs work. Once all CodeRabbit comments are resolved and [pre-merge checks](#pre-merge-checks) pass, CodeRabbit automatically switches its review to "Approve." This lets teams use CodeRabbit as a required reviewer that can block or unblock merging.

### Tone Instructions

A free-text field where you describe how CodeRabbit should communicate. This affects the writing style of all review comments and chat responses — for example, "Be concise and direct" or "Explain issues in detail for junior developers." Note that this only changes how comments are written, not how many are posted. Use [Profile](#profile) for that.

### Walkthrough

The main summary comment that CodeRabbit posts on every PR. It's a comprehensive, multi-section overview of everything that changed. Sections include a [high-level summary](#high-level-summary), a table of changed files, [sequence diagrams](#sequence-diagram), suggested [labels](#labels) and reviewers, and [Finishing Touches](#finishing-touches) among others. Which sections appear can be controlled through the review settings.

## Git platform terms

Terminology for the same concepts can vary across GitHub, GitLab, Bitbucket, and Azure DevOps. Where the naming differs, a comparison table is included.

### Base Branch

The branch that a PR is merging changes into. This is the destination, not the source.

| GitHub      | GitLab        | Bitbucket          | Azure DevOps  |
| ----------- | ------------- | ------------------ | ------------- |
| Base branch | Target branch | Destination branch | Target branch |

### Head / Source Branch

The branch that contains the new changes being proposed in the PR.

| GitHub      | GitLab        | Bitbucket     | Azure DevOps  |
| ----------- | ------------- | ------------- | ------------- |
| Head branch | Source branch | Source branch | Source branch |

### Status Check

An indicator (pass, pending, fail) shown on a PR that represents the result of an automated process like CI, tests, or a code review tool like CodeRabbit.

| GitHub                                    | GitLab                 | Bitbucket    | Azure DevOps             |
| ----------------------------------------- | ---------------------- | ------------ | ------------------------ |
| Status checks (UI), Commit statuses (API) | External status checks | Build status | PR status, Status checks |

### Labels

Tags attached to PRs or issues for categorization, such as `bug`, `feature`, or `urgent`. Used for filtering, automation, and organization.

| GitHub | GitLab | Bitbucket              | Azure DevOps              |
| ------ | ------ | ---------------------- | ------------------------- |
| Labels | Labels | Not supported natively | Labels (also called Tags) |

### Request Changes

A review action where the reviewer formally indicates the PR needs fixes before it can be merged. Can block merging if required reviews are configured. Not all platforms have this exact action.

| GitHub                         | GitLab                                   | Bitbucket                      | Azure DevOps             |
| ------------------------------ | ---------------------------------------- | ------------------------------ | ------------------------ |
| Request changes (blocks merge) | No direct equivalent (withhold approval) | No direct equivalent (decline) | Wait for author / Reject |

### Collapsed Section

A block of content in a PR comment that is hidden by default and expanded by clicking. Uses HTML `<details>` and `<summary>` tags. CodeRabbit wraps the [Walkthrough](#walkthrough) in one when "Collapse Walkthrough" is enabled.

| GitHub            | GitLab              | Bitbucket                    | Azure DevOps                 |
| ----------------- | ------------------- | ---------------------------- | ---------------------------- |
| Collapsed section | Collapsible section | Supported (no official name) | Supported (no official name) |

## General terms

Standard software engineering concepts referenced throughout CodeRabbit documentation.

### Docstring

A documentation comment embedded directly in source code that describes what a function, class, or module does. Format varies by language: Python uses triple-quoted strings (`"""..."""`), JavaScript uses JSDoc (`/** ... */`), etc. [Docstring coverage](/finishing-touches/docstrings) measures what percentage of functions have these.

### Glob Pattern

A file-matching syntax using wildcards. Used in [Path Filters](#path-filters) and [Path-based Instructions](#path-based-instructions) to specify which files a rule applies to. `*` matches any filename, `**` matches any directory depth, and `!` prefix excludes. Example: `src/**/*.ts` matches all TypeScript files under `src`.

### MCP

Model Context Protocol — an open standard for connecting AI tools to external data sources and services. CodeRabbit can use MCP servers configured for your organization as additional knowledge sources during reviews.

See [MCP server integrations](/integrations/mcp-servers).

### Regex

Regular expressions — a pattern-matching syntax more powerful than [glob](#glob-pattern). Used in the Base Branches setting to match branch names. Example: `release/.*` matches any branch starting with `release/`.

### Sequence Diagram

A standard UML diagram type that shows the order of interactions between components, functions, or services over time. CodeRabbit auto-generates these from changed code to help reviewers understand the flow.
