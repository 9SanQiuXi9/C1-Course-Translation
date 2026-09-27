---
source_file: "data/materials/CS146S_offline/pages/claude-code-best-practices.html"
origin_url: "https://www.anthropic.com/engineering/claude-code-best-practices"
title: "Get started"
extract_method: "html"
extract_warnings:
  - "AGGRESSIVE_STRIP_REVERTED：按关键词剥离 1 个区块后正文下降 100.0%（>40%），已全部加回，避免剥掉正文。该页结构特殊，建议人工抽查。"
src_sha256: "90cecb0837f3f00458512db957da5dd06d10c13fd47d1c86f4c7e94f94a2e066"
chars: 14500
code_blocks: 9
tables: 1
links: 99
garbage_rate: 0.0455
heading_levels_seen:
  h1: 1
  h2: 4
  h5: 4
---

[Skip to main content](#content-area)

[Claude Code Docs home page](/docs/en/overview)

![light logo](https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/logo/light.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=78fd01ff4f4340295a4f66e2ea54903c)

![dark logo](https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/logo/dark.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=1298a0c3b3a1da603b190d0de0e31712)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘K Ask AI

Search...

Navigation

Getting started

Claude Code overview

[Getting started](/docs/en/overview)

[Build with Claude Code](/docs/en/sub-agents)

[Deployment](/docs/en/third-party-integrations)

[Administration](/docs/en/setup)

[Configuration](/docs/en/settings)

[Reference](/docs/en/cli-reference)

[Resources](/docs/en/legal-and-compliance)

##### Getting started

- /docs/en/overview
- Overview

- /docs/en/quickstart
- Quickstart

- /docs/en/changelog
- Changelog

##### Core concepts

- /docs/en/how-claude-code-works
- How Claude Code works

- /docs/en/features-overview
- Extend Claude Code

- /docs/en/claude-directory
- Explore the .claude directory

- /docs/en/context-window
- Explore the context window

##### Use Claude Code

- /docs/en/memory
- Store instructions and memories

- /docs/en/permission-modes
- Permission modes

- /docs/en/common-workflows
- Common workflows

- /docs/en/best-practices
- Best practices

##### Platforms and integrations

- /docs/en/platforms
- Overview

- /docs/en/remote-control
- Remote Control

- Claude Code on the web

- Claude Code on desktop

- /docs/en/chrome
- Chrome extension (beta)

- /docs/en/computer-use
- Computer use (preview)

- /docs/en/vs-code
- Visual Studio Code

- /docs/en/jetbrains
- JetBrains IDEs

- Code review & CI/CD

- /docs/en/slack
- Claude Code in Slack

On this page

- [Get started](#get-started)
- [What you can do](#what-you-can-do)
- [Use Claude Code everywhere](#use-claude-code-everywhere)
- [Next steps](#next-steps)

Getting started

## Claude Code overview

Copy page

Claude Code is an agentic coding tool that reads your codebase, edits files, runs commands, and integrates with your development tools. Available in your terminal, IDE, desktop app, and browser.

Copy page

Claude Code is an AI-powered coding assistant that helps you build features, fix bugs, and automate development tasks. It understands your entire codebase and can work across multiple files and tools to get things done.

[​](#get-started)

# Get started

Choose your environment to get started. Most surfaces require a

[Claude subscription or](https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=overview_pricing)

[Anthropic Console account. The Terminal CLI and VS Code also support](https://console.anthropic.com/)

[third-party providers.](/docs/en/third-party-integrations)

- Terminal

- VS Code

- Desktop app

- Web

- JetBrains

The full-featured CLI for working with Claude Code directly in your terminal. Edit files, run commands, and manage your entire project from the command line.To install Claude Code, use one of the following methods:

- Native Install (Recommended)

- Homebrew

- WinGet

macOS, Linux, WSL:

<!-- CODE_BLOCK_START id=c1 lang= -->
```
curl -fsSL https://claude.ai/install.sh | bash
```
<!-- CODE_BLOCK_END id=c1 -->

Windows PowerShell:

<!-- CODE_BLOCK_START id=c2 lang= -->
```
irm https://claude.ai/install.ps1 | iex
```
<!-- CODE_BLOCK_END id=c2 -->

Windows CMD:

<!-- CODE_BLOCK_START id=c3 lang= -->
```
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```
<!-- CODE_BLOCK_END id=c3 -->

If you see The token '&&' is not a valid statement separator, you’re in PowerShell, not CMD. Use the PowerShell command above instead. Your prompt shows PS C:\ when you’re in PowerShell.Windows requires

[Git for Windows. Install it first if you don’t have it.](https://git-scm.com/downloads/win)

Native installations automatically update in the background to keep you on the latest version.

<!-- CODE_BLOCK_START id=c4 lang= -->
```
brew install --cask claude-code
```
<!-- CODE_BLOCK_END id=c4 -->

Homebrew installations do not auto-update. Run brew upgrade claude-code periodically to get the latest features and security fixes.

<!-- CODE_BLOCK_START id=c5 lang= -->
```
winget install Anthropic.ClaudeCode
```
<!-- CODE_BLOCK_END id=c5 -->

WinGet installations do not auto-update. Run winget upgrade Anthropic.ClaudeCode periodically to get the latest features and security fixes.

Then start Claude Code in any project:

<!-- CODE_BLOCK_START id=c6 lang= -->
```
cd your-project
claude
```
<!-- CODE_BLOCK_END id=c6 -->

You’ll be prompted to log in on first use. That’s it!

[Continue with the Quickstart →](/docs/en/quickstart)

See

[advanced setup for installation options, manual updates, or uninstallation instructions. Visit](/docs/en/setup)

[troubleshooting if you hit issues.](/docs/en/troubleshooting)

The VS Code extension provides inline diffs, @-mentions, plan review, and conversation history directly in your editor.

- [Install for VS Code](vscode:extension/anthropic.claude-code)
- [Install for Cursor](cursor:extension/anthropic.claude-code)

Or search for “Claude Code” in the Extensions view (Cmd+Shift+X on Mac, Ctrl+Shift+X on Windows/Linux). After installing, open the Command Palette (Cmd+Shift+P / Ctrl+Shift+P), type “Claude Code”, and select Open in New Tab.

[Get started with VS Code →](/docs/en/vs-code#get-started)

A standalone app for running Claude Code outside your IDE or terminal. Review diffs visually, run multiple sessions side by side, schedule recurring tasks, and kick off cloud sessions.Download and install:

- [macOS (Intel and Apple Silicon)](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code&utm_medium=docs)
- [Windows (x64)](https://claude.ai/api/desktop/win32/x64/setup/latest/redirect?utm_source=claude_code&utm_medium=docs)
- [Windows ARM64 (remote sessions only)](https://claude.ai/api/desktop/win32/arm64/setup/latest/redirect?utm_source=claude_code&utm_medium=docs)

After installing, launch Claude, sign in, and click the Code tab to start coding. A

[paid subscription is required.](https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=overview_desktop_pricing)

[Learn more about the desktop app →](/docs/en/desktop-quickstart)

Run Claude Code in your browser with no local setup. Kick off long-running tasks and check back when they’re done, work on repos you don’t have locally, or run multiple tasks in parallel. Available on desktop browsers and the Claude iOS app.Start coding at

[claude.ai/code.](https://claude.ai/code)

[Get started on the web →](/docs/en/claude-code-on-the-web#getting-started)

A plugin for IntelliJ IDEA, PyCharm, WebStorm, and other JetBrains IDEs with interactive diff viewing and selection context sharing.Install the

[Claude Code plugin from the JetBrains Marketplace and restart your IDE.](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-)

[Get started with JetBrains →](/docs/en/jetbrains)

[​](#what-you-can-do)

## What you can do

Here are some of the ways you can use Claude Code:

Automate the work you keep putting off

Claude Code handles the tedious tasks that eat up your day: writing tests for untested code, fixing lint errors across a project, resolving merge conflicts, updating dependencies, and writing release notes.

<!-- CODE_BLOCK_START id=c7 lang= -->
```
claude "write tests for the auth module, run them, and fix any failures"
```
<!-- CODE_BLOCK_END id=c7 -->

Build features and fix bugs

Describe what you want in plain language. Claude Code plans the approach, writes the code across multiple files, and verifies it works.For bugs, paste an error message or describe the symptom. Claude Code traces the issue through your codebase, identifies the root cause, and implements a fix. See

[common workflows for more examples.](/docs/en/common-workflows)

Create commits and pull requests

Claude Code works directly with git. It stages changes, writes commit messages, creates branches, and opens pull requests.

<!-- CODE_BLOCK_START id=c8 lang= -->
```
claude "commit my changes with a descriptive message"
```
<!-- CODE_BLOCK_END id=c8 -->

In CI, you can automate code review and issue triage with

[GitHub Actions or](/docs/en/github-actions)

[GitLab CI/CD.](/docs/en/gitlab-ci-cd)

Connect your tools with MCP

The

[Model Context Protocol (MCP) is an open standard for connecting AI tools to external data sources. With MCP, Claude Code can read your design docs in Google Drive, update tickets in Jira, pull data from Slack, or use your own custom tooling.](/docs/en/mcp)

Customize with instructions, skills, and hooks

[CLAUDE.md is a markdown file you add to your project root that Claude Code reads at the start of every session. Use it to set coding standards, architecture decisions, preferred libraries, and review checklists. Claude also builds](/docs/en/memory)

[auto memory as it works, saving learnings like build commands and debugging insights across sessions without you writing anything.Create](/docs/en/memory#auto-memory)

[custom commands to package repeatable workflows your team can share, like /review-pr or /deploy-staging.](/docs/en/skills)

[Hooks let you run shell commands before or after Claude Code actions, like auto-formatting after every file edit or running lint before a commit.](/docs/en/hooks)

Run agent teams and build custom agents

Spawn

[multiple Claude Code agents that work on different parts of a task simultaneously. A lead agent coordinates the work, assigns subtasks, and merges results.For fully custom workflows, the](/docs/en/sub-agents)

[Agent SDK lets you build your own agents powered by Claude Code’s tools and capabilities, with full control over orchestration, tool access, and permissions.](https://platform.claude.com/docs/en/agent-sdk/overview)

Pipe, script, and automate with the CLI

Claude Code is composable and follows the Unix philosophy. Pipe logs into it, run it in CI, or chain it with other tools:

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

See the

[CLI reference for the full set of commands and flags.](/docs/en/cli-reference)

Schedule recurring tasks

Run Claude on a schedule to automate work that repeats: morning PR reviews, overnight CI failure analysis, weekly dependency audits, or syncing docs after PRs merge.

- [Cloud scheduled tasks run on Anthropic-managed infrastructure, so they keep running even when your computer is off. Create them from the web, the Desktop app, or by running /schedule in the CLI.](/docs/en/web-scheduled-tasks)
- [Desktop scheduled tasks run on your machine, with direct access to your local files and tools](/docs/en/desktop#schedule-recurring-tasks)
- [/loop repeats a prompt within a CLI session for quick polling](/docs/en/scheduled-tasks)

Work from anywhere

Sessions aren’t tied to a single surface. Move work between environments as your context changes:

- Step away from your desk and keep working from your phone or any browser with
- [Remote Control](/docs/en/remote-control) Message
- [Dispatch a task from your phone and open the Desktop session it creates](/docs/en/desktop#sessions-from-dispatch) Kick off a long-running task on the [web or](/docs/en/claude-code-on-the-web)
- [iOS app, then pull it into your terminal with claude --teleport](https://apps.apple.com/app/claude-by-anthropic/id6473753684) Hand off a terminal session to the
- [Desktop app with /desktop for visual diff review](/docs/en/desktop) Route tasks from team chat: mention @Claude in
- [Slack with a bug report and get a pull request back](/docs/en/slack)

[​](#use-claude-code-everywhere)

## Use Claude Code everywhere

Each surface connects to the same underlying Claude Code engine, so your CLAUDE.md files, settings, and MCP servers work across all of them.
Beyond the

[Terminal,](/docs/en/quickstart)

[VS Code,](/docs/en/vs-code)

[JetBrains,](/docs/en/jetbrains)

[Desktop, and](/docs/en/desktop)

[Web environments above, Claude Code integrates with CI/CD, chat, and browser workflows:](/docs/en/claude-code-on-the-web)

[Web or](/docs/en/claude-code-on-the-web)

[Cloud scheduled tasks or](/docs/en/web-scheduled-tasks)

[GitHub Actions or](/docs/en/github-actions)

| I want to… | Best option |
| --- | --- |
| Continue a local session from my phone or another device | [Remote Control](/docs/en/remote-control) |
| Push events from Telegram, Discord, iMessage, or my own webhooks into a session | [Channels](/docs/en/channels) |
| Start a task locally, continue on mobile | [Claude iOS app](https://apps.apple.com/app/claude-by-anthropic/id6473753684) |
| Run Claude on a recurring schedule | [Desktop scheduled tasks](/docs/en/desktop#schedule-recurring-tasks) |
| Automate PR reviews and issue triage | [GitLab CI/CD](/docs/en/gitlab-ci-cd) |
| Get automatic code review on every PR | [GitHub Code Review](/docs/en/code-review) |
| Route bug reports from Slack to pull requests | [Slack](/docs/en/slack) |
| Debug live web applications | [Chrome](/docs/en/chrome) |
| Build custom agents for your own workflows | [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) |

[​](#next-steps)

## Next steps

Once you’ve installed Claude Code, these guides help you go deeper.

- [Quickstart: walk through your first real task, from exploring a codebase to committing a fix](/docs/en/quickstart)
- [Store instructions and memories: give Claude persistent instructions with CLAUDE.md files and auto memory](/docs/en/memory) [Common workflows and](/docs/en/common-workflows)
- [best practices: patterns for getting the most out of Claude Code](/docs/en/best-practices)
- [Settings: customize Claude Code for your workflow](/docs/en/settings)
- [Troubleshooting: solutions for common issues](/docs/en/troubleshooting)
- [code.claude.com: demos, pricing, and product details](https://code.claude.com/)

Was this page helpful?

Yes No

[Quickstart](/docs/en/quickstart)

⌘I

Assistant

Responses are generated using AI and may contain mistakes.
