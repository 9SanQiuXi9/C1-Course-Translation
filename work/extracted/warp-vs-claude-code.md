---
source_file: "data/materials/CS146S_offline/pages/warp-vs-claude-code.html"
origin_url: "https://www.warp.dev/university/getting-started/warp-vs-claude-code"
title: "Getting started with Warp and Oz"
extract_method: "html"
extract_warnings:
  - "AGGRESSIVE_STRIP_REVERTED：按关键词剥离 1 个区块后正文下降 100.0%（>40%），已全部加回，避免剥掉正文。该页结构特殊，建议人工抽查。"
src_sha256: "9d42607d326cbdbc4385e24c6048183f3bb9d921b7a68c5886bb76feb5682515"
chars: 6769
code_blocks: 0
tables: 0
links: 34
garbage_rate: 0.0606
heading_levels_seen:
  h1: 1
---

https://www.warp.dev/oz

Introducing Oz: the orchestration platform for cloud agents.

Learn more.

/

![](https://docs.warp.dev/~gitbook/image?url=https%3A%2F%2F2669883504-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Forganizations%252F-MbqIZLCtzerswjFm7mh%252Fsites%252Fsite_FKhQ8%252Ficon%252FDVgdOr0D0RoJbNfnRMiy%252Fwarp-avatar-white-on-black.png%3Falt%3Dmedia%26token%3Dca5f848d-74bd-4b2e-9af3-574c62bb61b9&width=32&dpr=3&quality=100&sign=d8de33a4&sv=2)

![](https://docs.warp.dev/~gitbook/image?url=https%3A%2F%2F2669883504-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Forganizations%252F-MbqIZLCtzerswjFm7mh%252Fsites%252Fsite_FKhQ8%252Ficon%252FDVgdOr0D0RoJbNfnRMiy%252Fwarp-avatar-white-on-black.png%3Falt%3Dmedia%26token%3Dca5f848d-74bd-4b2e-9af3-574c62bb61b9&width=32&dpr=3&quality=100&sign=d8de33a4&sv=2)

Warp

⌘Ctrlk

Copy

# Getting started with Warp and Oz

Get started with Warp, the Agentic Development Environment, and Oz, the orchestration platform for cloud agents.

Warp is an Agentic Development Environment, a modern terminal combined with powerful agents that help you build, test, deploy, and debug code. Warp's AI is powered by Oz, the orchestration platform for cloud agents.

![Warp, the Agentic Development Environment: Warp Terminal (a modern terminal built for coding with agents) and Oz (the orchestration platform for cloud agents)](https://docs.warp.dev/~gitbook/image?url=https%3A%2F%2F4009768362-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FPsjNxoJ0NFCXW6rRdHH3%252Fuploads%252Fgit-blob-6224a456c2508188d8d7035e3f03d6d8f6cd732a%252Fwarp-oz-welcome.png%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=59ed190c&sv=2)

*Warp combines a modern terminal with Oz, the orchestration platform for cloud agents*

---

#warp

Warp

Warp is where you work — a fast, modern terminal built for coding with agents.

Key capabilities:

- [Agent Modality : Switch between a clean terminal for commands and a dedicated conversation view for multi-turn agent workflows.](https://docs.warp.dev/agent-platform/local-agents/interacting-with-agents/agent-modality)

- [Modern terminal UX: Cursor movement, block-based navigation, multi-line editing, syntax highlighting, and rich completions. Built with Rust for high performance.](/terminal/editor)

- [Code editor: File tree, code editor with LSP support, and interactive code review experience.](/code/overview)

- [Coding agent integrations : Features like voice input, and @-selection for working with terminal based images. Compatible with Oz or agents like Claude Code and Codex.](https://docs.warp.dev/agent-platform/local-agents/third-party-cli-agents)

*Deep dive into Warp's core features*

---

#oz-the-orchestration-platform-for-cloud-agents

Oz: The orchestration platform for cloud agents

Oz is the orchestration platform for cloud agents that powers all of Warp's intelligent features. Oz is designed to coordinate agents at scale—understanding your codebase, executing tasks autonomously, and adapting to your workflows. Oz is multi-model by design, giving you flexibility to choose the best LLM for each task.

Oz operates in two modes:

#local-agents

Local agents

Run directly in the Warp app for real-time, interactive coding assistance.

- Write and refactor code across your codebase

- Debug issues and fix errors

- Run commands and interpret results

- Plan and execute multi-step tasks

Local agents keep you in control. You can review changes, steer the agent mid-task, and approve actions before they execute.

→

[Get started with local agents](https://docs.warp.dev/agent-platform/local-agents/overview)

#cloud-agents

Cloud agents

Oz Cloud Agents run in the background on Warp's infrastructure (or your own) for automation at scale.

- Triggers: React to events from Slack, Linear, GitHub, or custom webhooks

- Schedules: Run recurring tasks like dependency updates or dead code removal

- Parallelism: Run many agents concurrently across repos or tasks

- Observability: Every run is tracked, auditable, and shareable with your team

Cloud agents are ideal for work that doesn't need your immediate attention, like PR reviews, issue triage, routine maintenance, and integration-driven workflows.

→

[Learn about cloud agents](https://docs.warp.dev/agent-platform/cloud-agents/overview)

---

#how-they-work-together

How they work together

Warp and Oz provide a unified experience across local and cloud development:

- Same agent, anywhere: Whether you're working interactively in Warp or running agents in the cloud, you're using the same underlying agent capabilities.

- Seamless handoff: Start a task in the cloud and take over locally in Warp when you want hands-on control, without losing progress or context.

- Shared context: [Warp Drive,](/knowledge-and-collaboration/warp-drive) [Rules , and](https://docs.warp.dev/agent-platform/capabilities/rules)
- [MCP servers work across both local and cloud agents, so your team's knowledge and tools are always available.](https://docs.warp.dev/agent-platform/capabilities/mcp)

- Team collaboration: Share agent sessions, review agents' actions, and steer running tasks, regardless of who started them.

---

#multi-model-support

Multi-model support

Oz is multi-model by design. You can

[choose your preferred LLM from a curated set of top models.](https://docs.warp.dev/agent-platform/capabilities/model-choice)

---

#privacy-and-security

Privacy and security

Warp is SOC 2 compliant and has Zero Data Retention policies with all contracted LLM providers. No customer AI data is retained, stored, or used for training.

Warp's AI features can be globally disabled in Settings > AI.

→

[Read more about data privacy](https://www.warp.dev/privacy)

---

#next-steps

Next steps

- [Quickstart Guide: Get Warp installed and start coding](/getting-started/readme-1)

- [Local Agents Overview : Explore all AI features available in Warp](https://docs.warp.dev/agent-platform/local-agents/overview)

- [Cloud Agents Overview : Set up background automation](https://docs.warp.dev/agent-platform/cloud-agents/overview)

- [Oz Platform : Learn about the CLI, API, SDK, and infrastructure](https://docs.warp.dev/agent-platform/cloud-agents/platform)

[NextQuickstart](/getting-started/readme-1)

Last updated 3 days ago

Was this helpful?

- [Warp](#warp)
- [Oz: The orchestration platform for cloud agents](#oz-the-orchestration-platform-for-cloud-agents)
- [Local agents](#local-agents)
- [Cloud agents](#cloud-agents)
- [How they work together](#how-they-work-together)
- [Multi-model support](#multi-model-support)
- [Privacy and security](#privacy-and-security)
- [Next steps](#next-steps)

Was this helpful?
