[跳到主要内容](#content-area)

[Claude Code 文档首页](/docs/en/overview)

![浅色 logo](https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/logo/light.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=78fd01ff4f4340295a4f66e2ea54903c)

![深色 logo](https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/logo/dark.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=1298a0c3b3a1da603b190d0de0e31712)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

搜索……

⌘K 询问 AI

搜索……

导航

入门

Claude Code 概览

[入门](/docs/en/overview)

[用 Claude Code 构建](/docs/en/sub-agents)

[部署](/docs/en/third-party-integrations)

[管理](/docs/en/setup)

[配置](/docs/en/settings)

[参考](/docs/en/cli-reference)

[资源](/docs/en/legal-and-compliance)

##### 入门

- /docs/en/overview
- 概览

- /docs/en/quickstart
- 快速上手

- /docs/en/changelog
- 更新日志

##### 核心概念

- /docs/en/how-claude-code-works
- Claude Code 如何工作

- /docs/en/features-overview
- 扩展 Claude Code

- /docs/en/claude-directory
- 探索 .claude 目录

- /docs/en/context-window
- 探索上下文窗口

##### 使用 Claude Code

- /docs/en/memory
- 存储指令与记忆

- /docs/en/permission-modes
- 权限模式

- /docs/en/common-workflows
- 常见工作流

- /docs/en/best-practices
- 最佳实践

##### 平台与集成

- /docs/en/platforms
- 概览

- /docs/en/remote-control
- 远程控制

- Claude Code 网页版

- Claude Code 桌面版

- /docs/en/chrome
- Chrome 扩展（beta）

- /docs/en/computer-use
- 计算机操作（预览）

- /docs/en/vs-code
- Visual Studio Code

- /docs/en/jetbrains
- JetBrains IDE

- 代码审查与 CI/CD

- /docs/en/slack
- Slack 中的 Claude Code

本页内容

- [入门](#get-started)
- [你能做什么](#what-you-can-do)
- [随处使用 Claude Code](#use-claude-code-everywhere)
- [后续步骤](#next-steps)

入门

## Claude Code 概览

复制页面

Claude Code 是一个智能体式编码工具，它能阅读你的代码库、编辑文件、运行命令，并与你的开发工具集成。它可用于终端、IDE、桌面应用与浏览器。

复制页面

Claude Code 是一个由 AI 驱动的编码助手，帮助你构建功能、修复缺陷并自动化开发任务。它理解你的整个代码库，能跨多个文件与工具把事情做成。

[​](#get-started)

# 入门

选择你的环境开始使用。大多数入口都需要

[Claude 订阅或](https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=overview_pricing)

[Anthropic Console 账号。终端 CLI 与 VS Code 还支持](https://console.anthropic.com/)

[第三方供应商。](/docs/en/third-party-integrations)

- 终端

- VS Code

- 桌面应用

- 网页

- JetBrains

功能完整的 CLI，让你直接在终端里使用 Claude Code。在命令行中编辑文件、运行命令并管理整个项目。安装 Claude Code，可用以下方式之一：

- 原生安装（推荐）

- Homebrew

- WinGet

macOS、Linux、WSL：

<!-- CODE_BLOCK_START id=c1 lang= -->
```
curl -fsSL https://claude.ai/install.sh | bash
```
<!-- CODE_BLOCK_END id=c1 -->

Windows PowerShell：

<!-- CODE_BLOCK_START id=c2 lang= -->
```
irm https://claude.ai/install.ps1 | iex
```
<!-- CODE_BLOCK_END id=c2 -->

Windows CMD：

<!-- CODE_BLOCK_START id=c3 lang= -->
```
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```
<!-- CODE_BLOCK_END id=c3 -->

如果你看到 The token '&&' is not a valid statement separator，说明你在 PowerShell 里而不是 CMD 里。请改用上面的 PowerShell 命令。在 PowerShell 中你的提示符会显示 PS C:\。Windows 需要

[Git for Windows。如果还没安装，请先安装。](https://git-scm.com/downloads/win)

原生安装会在后台自动更新，让你始终使用最新版本。

<!-- CODE_BLOCK_START id=c4 lang= -->
```
brew install --cask claude-code
```
<!-- CODE_BLOCK_END id=c4 -->

Homebrew 安装不会自动更新。请定期运行 brew upgrade claude-code 以获取最新特性与安全修复。

<!-- CODE_BLOCK_START id=c5 lang= -->
```
winget install Anthropic.ClaudeCode
```
<!-- CODE_BLOCK_END id=c5 -->

WinGet 安装不会自动更新。请定期运行 winget upgrade Anthropic.ClaudeCode 以获取最新特性与安全修复。

然后在任意项目中启动 Claude Code：

<!-- CODE_BLOCK_START id=c6 lang= -->
```
cd your-project
claude
```
<!-- CODE_BLOCK_END id=c6 -->

首次使用时会提示你登录。就这样！

[继续看快速上手 →](/docs/en/quickstart)

参见

[高级安装设置，了解安装选项、手动更新或卸载说明。如果遇到问题，请访问](/docs/en/setup)

[故障排查。](/docs/en/troubleshooting)

VS Code 扩展在你的编辑器里直接提供内联 diff、@ 提及、计划审查与对话历史。

- [为 VS Code 安装](vscode:extension/anthropic.claude-code)
- [为 Cursor 安装](cursor:extension/anthropic.claude-code)

或者在扩展视图里搜索「Claude Code」（Mac 上按 Cmd+Shift+X，Windows/Linux 上按 Ctrl+Shift+X）。安装后打开命令面板（Cmd+Shift+P / Ctrl+Shift+P），输入「Claude Code」，选择 Open in New Tab。

[开始使用 VS Code →](/docs/en/vs-code#get-started)

一个独立应用，可在 IDE 或终端之外运行 Claude Code。可视化审查 diff、并排运行多个会话、安排周期性任务，并启动云端会话。下载并安装：

- [macOS（Intel 与 Apple Silicon）](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code&utm_medium=docs)
- [Windows（x64）](https://claude.ai/api/desktop/win32/x64/setup/latest/redirect?utm_source=claude_code&utm_medium=docs)
- [Windows ARM64（仅远程会话）](https://claude.ai/api/desktop/win32/arm64/setup/latest/redirect?utm_source=claude_code&utm_medium=docs)

安装后启动 Claude，登录，点击 Code 标签页即可开始编码。需要

[付费订阅。](https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=overview_desktop_pricing)

[进一步了解桌面应用 →](/docs/en/desktop-quickstart)

在浏览器里运行 Claude Code，无需本地安装。启动长时间运行的任务，等做完再回来查看；处理本地没有的仓库；或并行运行多个任务。支持桌面浏览器与 Claude iOS 应用。到

[claude.ai/code 开始编码。](https://claude.ai/code)

[在网页版开始使用 →](/docs/en/claude-code-on-the-web#getting-started)

一个用于 IntelliJ IDEA、PyCharm、WebStorm 及其他 JetBrains IDE 的插件，支持交互式 diff 查看与选区上下文共享。从

[JetBrains Marketplace 安装 Claude Code 插件，然后重启你的 IDE。](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-)

[开始使用 JetBrains →](/docs/en/jetbrains)

[​](#what-you-can-do)

## 你能做什么

以下是你使用 Claude Code 的一些方式：

自动化你一直拖着没做的工作

Claude Code 处理那些消耗你一天的琐碎任务：为没有测试的代码写测试、修复整个项目的 lint 错误、解决合并冲突、更新依赖，以及撰写发布说明。

<!-- CODE_BLOCK_START id=c7 lang= -->
```
claude "write tests for the auth module, run them, and fix any failures"
```
<!-- CODE_BLOCK_END id=c7 -->

构建功能与修复缺陷

用自然语言描述你想要什么。Claude Code 会规划做法、跨多个文件写代码，并验证它能工作。对于缺陷，贴上报错信息或描述症状。Claude Code 会在你的代码库中追踪问题、定位根因并实施修复。更多示例见

[常见工作流。](/docs/en/common-workflows)

创建提交与拉取请求

Claude Code 直接与 git 协作。它会暂存改动、撰写提交信息、创建分支，并开启拉取请求。

<!-- CODE_BLOCK_START id=c8 lang= -->
```
claude "commit my changes with a descriptive message"
```
<!-- CODE_BLOCK_END id=c8 -->

在 CI 中，你可以用

[GitHub Actions 或](/docs/en/github-actions)

[GitLab CI/CD 自动化代码审查与 issue 分诊。](/docs/en/gitlab-ci-cd)

用 MCP 连接你的工具

[Model Context Protocol（MCP）是一个把 AI 工具连接到外部数据源的开放标准。借助 MCP，Claude Code 可以读取你 Google Drive 里的设计文档、更新 Jira 中的工单、从 Slack 拉取数据，或使用你自己的自定义工具链。](/docs/en/mcp)

用指令、技能与钩子定制

[CLAUDE.md 是放在项目根目录的 markdown 文件，Claude Code 在每次会话开始时都会读取它。用它来设定编码规范、架构决策、首选库与审查清单。Claude 在工作过程中还会构建](/docs/en/memory)

[自动记忆，跨会话保存构建命令、调试心得等经验，而你什么都不用写。创建](/docs/en/memory#auto-memory)

[自定义命令，把团队可共享的可重复工作流打包起来，比如 /review-pr 或 /deploy-staging。](/docs/en/skills)

[钩子让你能在 Claude Code 动作前后运行 shell 命令，比如每次编辑文件后自动格式化，或在提交前运行 lint。](/docs/en/hooks)

运行智能体团队并构建自定义智能体

生成

[多个 Claude Code 智能体，让它们同时处理任务的不同部分。由一个主控智能体协调工作、分配子任务并合并结果。对于完全自定义的工作流，](/docs/en/sub-agents)

[Agent SDK 让你基于 Claude Code 的工具与能力构建自己的智能体，并完全掌控编排、工具访问与权限。](https://platform.claude.com/docs/en/agent-sdk/overview)

用 CLI 做管道、脚本与自动化

Claude Code 可组合，遵循 Unix 哲学。把日志管道输入它、在 CI 中运行它，或与其他工具串联：

<!-- CODE_BLOCK_START id=c9 lang= -->
```
## Analyze recent log output

tail -200 app.log | claude -p "Slack me if you see any anomalies"

## Automate translations in CI

claude -p "translate new strings into French and raise a PR for review"

## Bulk operations across files

git diff main --name-only | claude -p "review these changed files for security issues"
```
<!-- CODE_BLOCK_END id=c9 -->

完整的命令与参数清单见

[CLI 参考。](/docs/en/cli-reference)

安排周期性任务

按计划运行 Claude，自动化那些重复的工作：早间 PR 审查、隔夜 CI 失败分析、每周依赖审计，或在 PR 合并后同步文档。

- [云端定时任务运行在 Anthropic 管理的基础设施上，所以即使你的电脑关机它们也会继续运行。可以从网页、桌面应用创建，或在 CLI 中运行 /schedule。](/docs/en/web-scheduled-tasks)
- [桌面定时任务运行在你的机器上，可直接访问本地文件与工具](/docs/en/desktop#schedule-recurring-tasks)
- [/loop 在 CLI 会话内重复一条提示词，用于快速轮询](/docs/en/scheduled-tasks)

随处工作

会话不绑定于单一入口。随着你的环境变化，可以在环境之间迁移工作：

- 离开工位后，用手机或任意浏览器通过
- [远程控制继续工作](/docs/en/remote-control) 发送消息
- [从手机派发任务，并打开它创建的桌面会话](/docs/en/desktop#sessions-from-dispatch) 在[网页或](/docs/en/claude-code-on-the-web)
- [iOS 应用上启动长时间运行的任务，然后用 claude --teleport 把它拉到你的终端里](https://apps.apple.com/app/claude-by-anthropic/id6473753684) 把终端会话交给
- [桌面应用，用 /desktop 做可视化 diff 审查](/docs/en/desktop) 从团队聊天路由任务：在
- [Slack 里 @Claude 提一个缺陷报告，然后收到一个拉取请求](/docs/en/slack)

[​](#use-claude-code-everywhere)

## 随处使用 Claude Code

每个入口都连接到同一个底层 Claude Code 引擎，所以你的 CLAUDE.md 文件、设置与 MCP 服务器在所有入口上都能用。
除了上面的

[终端、](/docs/en/quickstart)

[VS Code、](/docs/en/vs-code)

[JetBrains、](/docs/en/jetbrains)

[桌面与](/docs/en/desktop)

[网页环境之外，Claude Code 还集成了 CI/CD、聊天与浏览器工作流：](/docs/en/claude-code-on-the-web)

[网页或](/docs/en/claude-code-on-the-web)

[云端定时任务或](/docs/en/web-scheduled-tasks)

[GitHub Actions 或](/docs/en/github-actions)

| 我想…… | 最佳选择 |
| --- | --- |
| 从手机或其他设备继续本地会话 | [远程控制](/docs/en/remote-control) |
| 把来自 Telegram、Discord、iMessage 或我自己的 webhook 的事件推入会话 | [Channels](/docs/en/channels) |
| 在本地启动任务，在移动端继续 | [Claude iOS 应用](https://apps.apple.com/app/claude-by-anthropic/id6473753684) |
| 按周期计划运行 Claude | [桌面定时任务](/docs/en/desktop#schedule-recurring-tasks) |
| 自动化 PR 审查与 issue 分诊 | [GitLab CI/CD](/docs/en/gitlab-ci-cd) |
| 每个 PR 都获得自动代码审查 | [GitHub Code Review](/docs/en/code-review) |
| 把 Slack 里的缺陷报告转成拉取请求 | [Slack](/docs/en/slack) |
| 调试线上 Web 应用 | [Chrome](/docs/en/chrome) |
| 为自己的工作流构建自定义智能体 | [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) |

[​](#next-steps)

## 后续步骤

安装 Claude Code 之后，这些指南能帮你更深入。

- [快速上手：走完你的第一个真实任务，从探索代码库到提交一个修复](/docs/en/quickstart)
- [存储指令与记忆：用 CLAUDE.md 文件与自动记忆给 Claude 持久指令](/docs/en/memory) [常见工作流与](/docs/en/common-workflows)
- [最佳实践：充分利用 Claude Code 的模式](/docs/en/best-practices)
- [设置：为你的工作流定制 Claude Code](/docs/en/settings)
- [故障排查：常见问题的解决方案](/docs/en/troubleshooting)
- [code.claude.com：演示、定价与产品详情](https://code.claude.com/)

这个页面有帮助吗？

是 否

[快速上手](/docs/en/quickstart)

⌘I

助手

回复由 AI 生成，可能包含错误。
