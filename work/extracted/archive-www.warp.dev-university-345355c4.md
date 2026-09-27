---
source_file: "data/fetched/www.warp.dev/university-345355c4.html"
origin_url: "https://www.warp.dev/university?slug=university"
title: "Warp"
extract_method: "html"
extract_warnings:
  - "AGGRESSIVE_STRIP_REVERTED：按关键词剥离 1 个区块后正文下降 100.0%（>40%），已全部加回，避免剥掉正文。该页结构特殊，建议人工抽查。"
src_sha256: "504ff783207277b46485be7628d8782b3034e8deaeb64a626616e7a0b1d22c08"
chars: 14580
code_blocks: 0
tables: 0
links: 42
garbage_rate: 0.0467
heading_levels_seen:
  h1: 1
  h2: 8
  h3: 4
---

[Skip to content](#_top)

For the complete documentation in markdown, see

[llms.txt. Markdown versions of each page are available by appending .md to any URL.](/llms.txt)

[Warp](https://www.warp.dev)

[GitHub](https://github.com/warpdotdev)

Select theme DarkLightAuto

Terminal > Getting started

## Getting started with Warp

Copy

Copy page

Copy page as Markdown for LLMs

Copy agent prompt

Copy a prompt to guide you through this page

View as Markdown ↗

View this page as plain text

https://chatgpt.com/?q=Read%20https%3A%2F%2Fdocs.warp.dev%2F.%20I%20want%20to%20ask%20questions%20about%20it.

Open in ChatGPT ↗

Ask ChatGPT about this page

https://claude.ai/new?q=Read%20https%3A%2F%2Fdocs.warp.dev%2F.%20I%20want%20to%20ask%20questions%20about%20it.

Open in Claude ↗

Ask Claude about this page

Export as PDF

Save or print this page

Copied!

## Getting started with Warp

Warp is an [open source](https://github.com/warpdotdev/warp) **Agentic Development Environment** that combines a modern, high-performance terminal with powerful agents to help you build, test, deploy, and debug code. Agents in Warp are powered by the **Automation Platform**, which orchestrates agents locally or in the cloud at scale.

<figure>
![Two panels side by side: Warp, a modern terminal built for coding with agents, and Warp Factories, open infrastructure for building cloud software factories](../../assets/terminal/warp-factories-welcome.png)
<figcaption>Warp and Warp Factories in the Agentic Development Environment.</figcaption>
</figure>

---

# Warp

Warp is where you work — a fast, modern terminal built for coding with agents.

**Key capabilities:**

* [**Terminal and Agent modes**](/agents/local-agents/interacting-with-agents/terminal-and-agent-modes/): Switch between a clean terminal for commands and a dedicated conversation view for multi-turn agent workflows.
* [**Modern terminal UX**](/terminal/editor/): Cursor movement, block-based navigation, multi-line editing, syntax highlighting, and rich completions. Built with Rust for high performance.
* [**Code editor**](/code/overview/): File tree, code editor with LSP support, and interactive code review experience.
* [**Third-party CLI agents**](/agents/cli-agents/overview/): Run third-party CLI agents like Claude Code, Codex, and OpenCode with the agent toolbelt — rich input, code review, notifications, and more.

<VideoEmbed url="https://www.youtube.com/watch?v=xhkoXsE9Wqc" title="Deep dive into Warp's core features" />

---

## Three ways to use the Warp Agent

The **Warp Agent** writes and edits code, debugs issues, runs commands, and works through multi-step tasks. You reach the same agent three ways, and your account, rules, skills, and model access carry across all of them.

### In the Warp app

Real-time, interactive coding assistance alongside your terminal.

* Write and refactor code across your codebase
* Debug issues and fix errors
* Run commands and interpret results
* Plan and execute multi-step tasks

You stay in control. Review changes, steer the agent mid-task, and approve actions before they execute.

→ [Get started with agents in Warp](/agents/)

### In any terminal, with the Warp Agent CLI

The Warp Agent CLI is a standalone terminal program that runs the same agent without the Warp app. Run the `warp` command to start a conversation in whichever terminal you already use, over SSH, or on a machine where Warp isn't installed.

→ [Get started with the Warp Agent CLI](/agents/cli/quickstart/)

### In the cloud, as a cloud agent

Cloud agents run in the background on Warp's infrastructure (or your own) for automation at scale.

* **Triggers**: React to events from Slack, Linear, GitHub, or custom webhooks
* **Schedules**: Run recurring tasks like dependency updates or dead code removal
* **Parallelism**: Run many agents concurrently across repos or tasks
* **Observability**: Every run is tracked, auditable, and shareable with your team

Cloud agents are ideal for work that doesn't need your immediate attention, like PR reviews, issue triage, routine maintenance, and integration-driven workflows.

→ [Learn about cloud agents](/platform/)

### The platform behind them

The **Automation Platform** is Warp's programmable system for running and coordinating agents at scale. It provides the environments, triggers, integrations, orchestration, and observability that cloud agents run on, plus a CLI, API, and SDK.

→ [Learn about the Automation Platform](/platform/overview/)

---

## Repeatable development workflows with Warp Factories

A single cloud agent handles one task. **Warp Factories**, now in Early Access, lets your team run a software factory: a repeatable process where cloud agents triage, spec, implement, review, and verify work, and humans approve key decisions.

→ [Learn about Warp Factories](/factories/) or [request access](https://www.warp.dev/factories/request-access)

---

## How they work together

Warp and the Automation Platform provide a unified experience across local and cloud development:

* **Same agent, anywhere**: Whether you're working in the Warp app, in another terminal through the Warp Agent CLI, or running agents in the cloud, you're using the same underlying agent capabilities.
* **Seamless handoff**: Start a task in the cloud and take over locally in Warp when you want hands-on control, without losing progress or context.
* **Shared context**: [Warp Drive](/knowledge-and-collaboration/warp-drive/), [Rules](/agents/capabilities/rules/), and [MCP servers](/agents/capabilities/mcp/) work across both local and cloud agents, so your team's knowledge and tools are always available.
* **Team collaboration**: Share agent sessions, review agents' actions, and steer running tasks, regardless of who started them.

---

## Multi-model support

The Automation Platform is multi-model by design. You can [choose your preferred LLM](/agents/inference/model-choice/) from a curated set of top models.

---

## Open source

Warp's client is open source under [AGPL v3](https://github.com/warpdotdev/warp/blob/master/LICENSE-AGPL). The source lives at [`warpdotdev/warp`](https://github.com/warpdotdev/warp), where you can read the code, file issues, and contribute alongside the Warp team. Development happens in the open with an agent-first workflow managed by the Automation Platform.

→ [Contributing to Warp](/support-and-community/community/contributing/) explains how to file issues, claim work, and ship code or themes.

---

## Privacy and security

Warp is **SOC 2 compliant** and has **Zero Data Retention** policies with all contracted LLM providers. No customer AI data is retained, stored, or used for training.

Warp's AI features can be globally disabled in **Settings** > **Agents** > **Warp Agent**.

→ [Read more about data privacy](https://www.warp.dev/privacy)

---

## Next steps

* [**Quickstart**](/quickstart/): Get Warp installed and start coding
* [**Agents overview**](/agents/): What the Warp Agent does, how to control it, and where to run it
* [**Warp Agent CLI**](/agents/cli/): Run the Warp Agent in any terminal
* [**Cloud Agents overview**](/platform/): Set up background automation
* [**Automation Platform**](/platform/overview/): Learn about the CLI, API, SDK, and infrastructureTell me about this feature: https://docs.warp.dev/

Get started with Warp, the Agentic Development Environment, and the Automation Platform, which orchestrates cloud agents at scale.

Warp is an

[open source Agentic Development Environment that combines a modern, high-performance terminal with powerful agents to help you build, test, deploy, and debug code. Agents in Warp are powered by the Automation Platform, which orchestrates agents locally or in the cloud at scale.](https://github.com/warpdotdev/warp)

![Two panels side by side: Warp, a modern terminal built for coding with agents, and Warp Factories, open infrastructure for building cloud software factories](/_astro/warp-factories-welcome.rhXaWld0_2f30gX.webp?dpl=dpl_Fj6SWmikK1ueXnLLauMyaJRXwW3Q)

*Warp and Warp Factories in the Agentic Development Environment.*

---

## Warp

[Section titled “Warp”](#warp)

Warp is where you work — a fast, modern terminal built for coding with agents.

Key capabilities:

- [Terminal and Agent modes: Switch between a clean terminal for commands and a dedicated conversation view for multi-turn agent workflows.](/agents/local-agents/interacting-with-agents/terminal-and-agent-modes/)
- [Modern terminal UX: Cursor movement, block-based navigation, multi-line editing, syntax highlighting, and rich completions. Built with Rust for high performance.](/terminal/editor/)
- [Code editor: File tree, code editor with LSP support, and interactive code review experience.](/code/overview/)
- [Third-party CLI agents: Run third-party CLI agents like Claude Code, Codex, and OpenCode with the agent toolbelt — rich input, code review, notifications, and more.](/agents/cli-agents/overview/)

![Deep dive into Warp's core features](https://i.ytimg.com/vi/xhkoXsE9Wqc/sddefault.jpg)

---

## Three ways to use the Warp Agent

[Section titled “Three ways to use the Warp Agent”](#three-ways-to-use-the-warp-agent)

The Warp Agent writes and edits code, debugs issues, runs commands, and works through multi-step tasks. You reach the same agent three ways, and your account, rules, skills, and model access carry across all of them.

### In the Warp app

[Section titled “In the Warp app”](#in-the-warp-app)

Real-time, interactive coding assistance alongside your terminal.

- Write and refactor code across your codebase
- Debug issues and fix errors
- Run commands and interpret results
- Plan and execute multi-step tasks

You stay in control. Review changes, steer the agent mid-task, and approve actions before they execute.

→

[Get started with agents in Warp](/agents/)

### In any terminal, with the Warp Agent CLI

[Section titled “In any terminal, with the Warp Agent CLI”](#in-any-terminal-with-the-warp-agent-cli)

The Warp Agent CLI is a standalone terminal program that runs the same agent without the Warp app. Run the warp command to start a conversation in whichever terminal you already use, over SSH, or on a machine where Warp isn’t installed.

→

[Get started with the Warp Agent CLI](/agents/cli/quickstart/)

### In the cloud, as a cloud agent

[Section titled “In the cloud, as a cloud agent”](#in-the-cloud-as-a-cloud-agent)

Cloud agents run in the background on Warp’s infrastructure (or your own) for automation at scale.

- Triggers: React to events from Slack, Linear, GitHub, or custom webhooks
- Schedules: Run recurring tasks like dependency updates or dead code removal
- Parallelism: Run many agents concurrently across repos or tasks
- Observability: Every run is tracked, auditable, and shareable with your team

Cloud agents are ideal for work that doesn’t need your immediate attention, like PR reviews, issue triage, routine maintenance, and integration-driven workflows.

→

[Learn about cloud agents](/platform/)

### The platform behind them

[Section titled “The platform behind them”](#the-platform-behind-them)

The Automation Platform is Warp’s programmable system for running and coordinating agents at scale. It provides the environments, triggers, integrations, orchestration, and observability that cloud agents run on, plus a CLI, API, and SDK.

→

[Learn about the Automation Platform](/platform/overview/)

---

## Repeatable development workflows with Warp Factories

[Section titled “Repeatable development workflows with Warp Factories”](#repeatable-development-workflows-with-warp-factories)

A single cloud agent handles one task. Warp Factories, now in Early Access, lets your team run a software factory: a repeatable process where cloud agents triage, spec, implement, review, and verify work, and humans approve key decisions.

→

[Learn about Warp Factories or](/factories/)

[request access](https://www.warp.dev/factories/request-access)

---

## How they work together

[Section titled “How they work together”](#how-they-work-together)

Warp and the Automation Platform provide a unified experience across local and cloud development:

- Same agent, anywhere: Whether you’re working in the Warp app, in another terminal through the Warp Agent CLI, or running agents in the cloud, you’re using the same underlying agent capabilities.
- Seamless handoff: Start a task in the cloud and take over locally in Warp when you want hands-on control, without losing progress or context. Shared context: [Warp Drive,](/knowledge-and-collaboration/warp-drive/) [Rules, and](/agents/capabilities/rules/)
- [MCP servers work across both local and cloud agents, so your team’s knowledge and tools are always available.](/agents/capabilities/mcp/)
- Team collaboration: Share agent sessions, review agents’ actions, and steer running tasks, regardless of who started them.

---

## Multi-model support

[Section titled “Multi-model support”](#multi-model-support)

The Automation Platform is multi-model by design. You can

[choose your preferred LLM from a curated set of top models.](/agents/inference/model-choice/)

---

## Open source

[Section titled “Open source”](#open-source)

Warp’s client is open source under

[AGPL v3. The source lives at](https://github.com/warpdotdev/warp/blob/master/LICENSE-AGPL)

[warpdotdev/warp, where you can read the code, file issues, and contribute alongside the Warp team. Development happens in the open with an agent-first workflow managed by the Automation Platform.](https://github.com/warpdotdev/warp)

→

[Contributing to Warp explains how to file issues, claim work, and ship code or themes.](/support-and-community/community/contributing/)

---

## Privacy and security

[Section titled “Privacy and security”](#privacy-and-security)

Warp is SOC 2 compliant and has Zero Data Retention policies with all contracted LLM providers. No customer AI data is retained, stored, or used for training.

Warp’s AI features can be globally disabled in Settings > Agents > Warp Agent.

→

[Read more about data privacy](https://www.warp.dev/privacy)

---

## Next steps

[Section titled “Next steps”](#next-steps)

- [Quickstart: Get Warp installed and start coding](/quickstart/)
- [Agents overview: What the Warp Agent does, how to control it, and where to run it](/agents/)
- [Warp Agent CLI: Run the Warp Agent in any terminal](/agents/cli/)
- [Cloud Agents overview: Set up background automation](/platform/)
- [Automation Platform: Learn about the CLI, API, SDK, and infrastructure](/platform/overview/)
