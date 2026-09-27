# 翻译留痕：warp-vs-claude-code

- doc_id：`warp-vs-claude-code`
- 时间：2026-09-27T16:31:24+08:00
- 原文：`extracted/warp-vs-claude-code.md`
- 译文：`translated/warp-vs-claude-code.md`
- 原文 sha256：`0da18df9ce05959839a33b9b95e484a15dc073d7e4eeb5da62a136219fa14c95`
- 译文 sha256：`5365d46727068b55dcd63f0922da67e9afd650849f941688f100fb6155bed98f`
- 术语约束条数：19

## 一、本文档涉及的术语清单

| 英文 | 译法 | handling | 出现次数 |
|---|---|---|---|
| `agent` | 智能体 | `translate` | 18 |
| `orchestration` | 编排 | `translate` | 10 |
| `model` | 模型 | `translate` | 7 |
| `privacy` | 隐私 | `translate` | 6 |
| `security` | 安全 | `translate` | 4 |
| `agentic` | 智能体的 | `translate` | 3 |
| `llm` | LLM | `acronym` | 3 |
| `mcp` | MCP | `acronym` | 2 |
| `context` | 上下文 | `translate` | 2 |
| `codebase` | 代码库 | `translate` | 2 |
| `automation` | 自动化 | `translate` | 2 |
| `token` | token | `keep_en` | 2 |
| `code review` | 代码审查 | `translate` | 1 |
| `api` | API | `acronym` | 1 |
| `pr` | PR | `acronym` | 1 |
| `training` | 训练 | `translate` | 1 |
| `observability` | 可观测性 | `translate` | 1 |
| `refactor` | 重构 | `translate` | 1 |
| `coding agent` | 编码智能体 | `translate` | 1 |

## 二、落盘校验结果

```json
{
  "non_empty": true,
  "code_blocks_total": 0,
  "code_blocks_in_translation": 0,
  "code_blocks_match": true,
  "code_blocks_byte_identical": true,
  "urls_orig": 15,
  "urls_trans": 15,
  "urls_all_present": true,
  "urls_counts_equal": true,
  "headings_orig": 1,
  "headings_trans": 1,
  "headings_match": true,
  "orig_chars": 5978,
  "trans_chars": 3870,
  "length_ratio": 0.6474,
  "length_ratio_ok": true
}
```

## 四、发出的 prompt 全文

```markdown
# 翻译任务：warp-vs-claude-code

## 一、文档元数据

- doc_id：`warp-vs-claude-code`
- title：Getting started with Warp and Oz
- origin_url：https://www.warp.dev/university/getting-started/warp-vs-claude-code
- 本段字符数：6,772

## 二、术语约束（本文档用到的，必须严格遵守）

| 英文 | 处理方式 | 出现次数 |
|---|---|---|
| `agent` | 翻译为「智能体」 | 18 |
| `orchestration` | 翻译为「编排」 | 10 |
| `model` | 翻译为「模型」 | 7 |
| `privacy` | 翻译为「隐私」 | 6 |
| `security` | 翻译为「安全」 | 4 |
| `agentic` | 翻译为「智能体的」 | 3 |
| `llm` | 保留英文缩写（首次出现给全称） | 3 |
| `mcp` | 保留英文缩写（首次出现给全称） | 2 |
| `context` | 翻译为「上下文」 | 2 |
| `codebase` | 翻译为「代码库」 | 2 |
| `automation` | 翻译为「自动化」 | 2 |
| `token` | 保留英文原形（不翻译） | 2 |
| `code review` | 翻译为「代码审查」 | 1 |
| `api` | 保留英文缩写（首次出现给全称） | 1 |
| `pr` | 保留英文缩写（首次出现给全称） | 1 |
| `training` | 翻译为「训练」 | 1 |
| `observability` | 翻译为「可观测性」 | 1 |
| `refactor` | 翻译为「重构」 | 1 |
| `coding agent` | 翻译为「编码智能体」 | 1 |

⚠️ 上表是硬约束，**不得自行更换译法**。
⚠️ 未列出的词按常规翻译；专有名词（MCP、token、vibe coding 等）保留英文。

## 三、翻译要求

- 严格按上表术语译法，不得自行更换
- 专有名词保留英文（MCP、token、vibe coding 等）
- 代码块内容**逐字节原样保留**，不翻译、不改变量名、不动缩进
- 保留所有 Markdown 结构（标题层级、列表、表格、链接）
- URL 一个字都不能改
- 保留 `<!-- CODE_BLOCK_START ... -->` 与 `<!-- CODE_BLOCK_END ... -->` 注释标记
- 标题行数量与原文一致，不要新增或删除标题
- 输出纯中文，不要中英对照
- ⚠️ 只翻译给定内容，不要补充、摘要、扩展、评论

## 四、待翻译原文

````markdown


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

````

## 五、输出要求

直接给出译文，用 ``` 包裹便于复制。**不要**输出任何解释、前言或后记。

```

## 五、AI 返回的译文全文

```markdown
https://www.warp.dev/oz

隆重推出 Oz：面向云端智能体的编排平台。

了解更多。

/

![](https://docs.warp.dev/~gitbook/image?url=https%3A%2F%2F2669883504-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Forganizations%252F-MbqIZLCtzerswjFm7mh%252Fsites%252Fsite_FKhQ8%252Ficon%252FDVgdOr0D0RoJbNfnRMiy%252Fwarp-avatar-white-on-black.png%3Falt%3Dmedia%26token%3Dca5f848d-74bd-4b2e-9af3-574c62bb61b9&width=32&dpr=3&quality=100&sign=d8de33a4&sv=2)

![](https://docs.warp.dev/~gitbook/image?url=https%3A%2F%2F2669883504-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Forganizations%252F-MbqIZLCtzerswjFm7mh%252Fsites%252Fsite_FKhQ8%252Ficon%252FDVgdOr0D0RoJbNfnRMiy%252Fwarp-avatar-white-on-black.png%3Falt%3Dmedia%26token%3Dca5f848d-74bd-4b2e-9af3-574c62bb61b9&width=32&dpr=3&quality=100&sign=d8de33a4&sv=2)

Warp

⌘Ctrlk

复制

# Warp 与 Oz 入门

开始使用 Warp（智能体开发环境）与 Oz（面向云端智能体的编排平台）。

Warp 是一个智能体开发环境，把现代终端与强大的智能体结合起来，帮助你构建、测试、部署和调试代码。Warp 的 AI 由 Oz 驱动 —— 一个面向云端智能体的编排平台。

![Warp，智能体开发环境：Warp 终端（为与智能体协作编程而打造的现代终端）与 Oz（面向云端智能体的编排平台）](https://docs.warp.dev/~gitbook/image?url=https%3A%2F%2F4009768362-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FPsjNxoJ0NFCXW6rRdHH3%252Fuploads%252Fgit-blob-6224a456c2508188d8d7035e3f03d6d8f6cd732a%252Fwarp-oz-welcome.png%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=59ed190c&sv=2)

*Warp 把现代终端与 Oz（面向云端智能体的编排平台）结合起来*

---

#warp

Warp

Warp 是你工作的地方 —— 一个快速、现代、为与智能体协作编程而打造的终端。

核心能力：

- [智能体模态：在用于命令的清爽终端与用于多轮智能体工作流的专用对话视图之间切换。](https://docs.warp.dev/agent-platform/local-agents/interacting-with-agents/agent-modality)

- [现代终端体验：光标移动、基于块的导航、多行编辑、语法高亮与丰富的补全。用 Rust 构建，性能出色。](/terminal/editor)

- [代码编辑器：文件树、支持 LSP 的代码编辑器，以及交互式代码审查体验。](/code/overview)

- [编码智能体集成：语音输入、用于处理终端内图像的 @ 选择等功能。兼容 Oz，或 Claude Code、Codex 等智能体。](https://docs.warp.dev/agent-platform/local-agents/third-party-cli-agents)

*深入了解 Warp 的核心功能*

---

#oz-the-orchestration-platform-for-cloud-agents

Oz：面向云端智能体的编排平台

Oz 是面向云端智能体的编排平台，为 Warp 的所有智能能力提供支撑。Oz 的设计目标是规模化地协调智能体 —— 理解你的代码库、自主执行任务，并适应你的工作流。Oz 从设计上就支持多模型，让你可以为每个任务灵活选择最合适的 LLM。

Oz 有两种运行模式：

#local-agents

本地智能体

直接运行在 Warp 应用中，提供实时、交互式的编码协助。

- 在你的代码库中编写和重构代码

- 调试问题并修复错误

- 运行命令并解读结果

- 规划并执行多步骤任务

本地智能体让你始终掌握控制权。你可以审查改动、在任务进行中调整智能体的方向，并在动作执行前批准它们。

→

[开始使用本地智能体](https://docs.warp.dev/agent-platform/local-agents/overview)

#cloud-agents

云端智能体

Oz 云端智能体在 Warp 的基础设施（或你自己的基础设施）上后台运行，实现规模化自动化。

- 触发器：响应来自 Slack、Linear、GitHub 或自定义 webhook 的事件

- 定时任务：运行依赖更新、死代码清理等周期性任务

- 并行：跨仓库或跨任务并发运行多个智能体

- 可观测性：每次运行都可追踪、可审计，并可与团队共享

云端智能体非常适合那些不需要你即时关注的工作，例如 PR 审查、issue 分类、日常维护，以及集成驱动的工作流。

→

[了解云端智能体](https://docs.warp.dev/agent-platform/cloud-agents/overview)

---

#how-they-work-together

它们如何协同工作

Warp 与 Oz 在本地与云端开发之间提供统一体验：

- 同一个智能体，无处不在：无论你是在 Warp 中交互式工作，还是在云端运行智能体，用的都是同一套底层智能体能力。

- 无缝交接：在云端启动任务，当你想亲自动手时可在本地 Warp 中接手，进度与上下文都不会丢失。

- 共享上下文：[Warp Drive、](/knowledge-and-collaboration/warp-drive) [Rules，以及](https://docs.warp.dev/agent-platform/capabilities/rules)
- [MCP 服务器，在本地与云端智能体上都可用，因此你团队的知识与工具始终可用。](https://docs.warp.dev/agent-platform/capabilities/mcp)

- 团队协作：共享智能体会话、审查智能体的动作、调整正在运行的任务，无论任务是谁启动的。

---

#multi-model-support

多模型支持

Oz 从设计上就支持多模型。你可以

[从一组精选的顶级模型中挑选你偏好的 LLM。](https://docs.warp.dev/agent-platform/capabilities/model-choice)

---

#privacy-and-security

隐私与安全

Warp 通过 SOC 2 合规认证，并与所有签约的 LLM 供应商实行零数据保留政策。不会保留、存储任何客户 AI 数据，也不会将其用于训练。

Warp 的 AI 功能可在「设置 > AI」中全局关闭。

→

[进一步了解数据隐私](https://www.warp.dev/privacy)

---

#next-steps

后续步骤

- [快速入门指南：安装 Warp 并开始编码](/getting-started/readme-1)

- [本地智能体概览：探索 Warp 中所有可用的 AI 功能](https://docs.warp.dev/agent-platform/local-agents/overview)

- [云端智能体概览：配置后台自动化](https://docs.warp.dev/agent-platform/cloud-agents/overview)

- [Oz 平台：了解 CLI、API、SDK 与基础设施](https://docs.warp.dev/agent-platform/cloud-agents/platform)

[下一页快速入门](/getting-started/readme-1)

最后更新于 3 天前

这个页面有帮助吗？

- [Warp](#warp)
- [Oz：面向云端智能体的编排平台](#oz-the-orchestration-platform-for-cloud-agents)
- [Local agents](#local-agents)
- [Cloud agents](#cloud-agents)
- [它们如何协同工作](#how-they-work-together)
- [多模型支持](#multi-model-support)
- [隐私与安全](#privacy-and-security)
- [后续步骤](#next-steps)

这个页面有帮助吗？

```
