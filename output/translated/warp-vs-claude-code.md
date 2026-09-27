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
