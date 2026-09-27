# 翻译留痕：archive-raw.githubusercontent.com-README-704a0e2c

- doc_id：`archive-raw.githubusercontent.com-README-704a0e2c`
- 时间：2026-09-27T16:53:08+08:00
- 原文：`extracted/archive-raw.githubusercontent.com-README-704a0e2c.md`
- 译文：`translated/archive-raw.githubusercontent.com-README-704a0e2c.md`
- 原文 sha256：`b4725e28576c5c7177ff78c62d7021ed3868e822450cd952a349a59e7d0438d6`
- 译文 sha256：`29ab4bb52a7d2d46ba62fb31e49d7cb5055f8cd9c672c0efba8b9384b469eb99`
- 术语约束条数：9

## 一、本文档涉及的术语清单

| 英文 | 译法 | handling | 出现次数 |
|---|---|---|---|
| `api` | API | `acronym` | 10 |
| `agent` | 智能体 | `translate` | 9 |
| `best practices` | 最佳实践 | `translate` | 3 |
| `context` | 上下文 | `translate` | 2 |
| `token` | token | `keep_en` | 2 |
| `mcp` | MCP | `acronym` | 1 |
| `security` | 安全 | `translate` | 1 |
| `codebase` | 代码库 | `translate` | 1 |
| `orchestration` | 编排 | `translate` | 1 |

## 二、落盘校验结果

```json
{
  "non_empty": true,
  "code_blocks_total": 7,
  "code_blocks_in_translation": 7,
  "code_blocks_match": true,
  "code_blocks_byte_identical": true,
  "urls_orig": 7,
  "urls_trans": 7,
  "urls_all_present": true,
  "urls_counts_equal": true,
  "headings_orig": 22,
  "headings_trans": 22,
  "headings_match": true,
  "orig_chars": 6947,
  "trans_chars": 4624,
  "length_ratio": 0.6656,
  "length_ratio_ok": true
}
```

## 四、发出的 prompt 全文

```markdown
# 翻译任务：archive-raw.githubusercontent.com-README-704a0e2c

## 一、文档元数据

- doc_id：`archive-raw.githubusercontent.com-README-704a0e2c`
- title：Awesome Claude Agents - AI Development Team 🚀
- origin_url：https://github.com/vijaythecoder/awesome-claude-agents
- 本段字符数：8,929

## 二、术语约束（本文档用到的，必须严格遵守）

| 英文 | 处理方式 | 出现次数 |
|---|---|---|
| `api` | 保留英文缩写（首次出现给全称） | 10 |
| `agent` | 翻译为「智能体」 | 9 |
| `best practices` | 翻译为「最佳实践」 | 3 |
| `context` | 翻译为「上下文」 | 2 |
| `token` | 保留英文原形（不翻译） | 2 |
| `mcp` | 保留英文缩写（首次出现给全称） | 1 |
| `security` | 翻译为「安全」 | 1 |
| `codebase` | 翻译为「代码库」 | 1 |
| `orchestration` | 翻译为「编排」 | 1 |

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


# Awesome Claude Agents - AI Development Team 🚀

**Supercharge Claude Code with a team of specialized AI agents** that work together to build complete features, debug complex issues, and handle any technology stack with expert-level knowledge.

### ⚠️ Important Notice

**This project is experimental and token-intensive.** I'm actively testing these agents with Claude subscription - expect high token consumption during complex workflows. Multi-agent orchestration can consume 10-50k tokens per complex feature. Use with caution and monitor your usage.

### 🚀 Quick Start (3 Minutes)

#### Prerequisites

- **Claude Code CLI** installed and authenticated
- **Claude subscription** - required for intensive agent workflows
- Active project directory with your codebase
- **Optional**: [Context7 MCP](docs/dependencies.md) for enhanced documentation access

#### 1. Install the Agents

```bash
git clone https://github.com/vijaythecoder/awesome-claude-agents.git
```

##### Option A: Symlink (Recommended - auto-updates)

**macOS/Linux:**
```bash
## Create agents directory if it doesn't exist (preserves existing agents)

mkdir -p ~/.claude/agents

## Symlink the awesome-claude-agents collection

ln -sf "$(pwd)/awesome-claude-agents/agents/" ~/.claude/agents/awesome-claude-agents
```

**Windows (PowerShell):**
```powershell
## Create agents directory

New-Item -Path "$env:USERPROFILE\.claude\agents" -ItemType Directory -Force

## Create symlink

cmd /c mklink /D "$env:USERPROFILE\.claude\agents\awesome-claude-agents" "$(Get-Location)\awesome-claude-agents\agents"
```

##### Option B: Copy (Static - no auto-updates)

```bash
## Create agents directory if it doesn't exist

mkdir -p ~/.claude/agents

## Copy all agents

cp -r awesome-claude-agents/agents ~/.claude/agents/awesome-claude-agents
```

#### 2. Verify Installation

```bash
claude /agents
## Should show all 24 agents.

```

#### 3. Initialize Your Project

**Navigate** to your **project directory** and run the following command to configure your AI team:

```bash
claude "use @agent-team-configurator and optimize my project to best use the available subagents."
```

#### 4. Start Building

```bash
claude "use @agent-tech-lead-orchestrator and build a user authentication system"
```

Your AI team will automatically detect your stack and use the right specialists!

### 🎯 How Auto-Configuration Works

The @agent-team-configurator automatically sets up your perfect AI development team. When invoked, it:

1. **Locates CLAUDE.md** - Finds existing project configuration and preserves all your custom content outside the "AI Team Configuration" section
2. **Detects Technology Stack** - Inspects package.json, composer.json, requirements.txt, go.mod, Gemfile, and build configs to understand your project
3. **Discovers Available Agents** - Scans ~/.claude/agents/ and .claude/ folders, building a capability table of all available specialists
4. **Selects Specialists** - Prefers framework-specific agents over universal ones, always includes @agent-code-reviewer and @agent-performance-optimizer for quality assurance
5. **Updates CLAUDE.md** - Creates a timestamped "AI Team Configuration" section with your detected stack and a Task|Agent|Notes mapping table
6. **Provides Usage Guidance** - Shows you the detected stack, selected agents, and gives sample commands to start building

### 👥 Meet Your AI Development Team

#### 🎭 Orchestrators (3 agents)

- **[Tech Lead Orchestrator](agents/orchestrators/tech-lead-orchestrator.md)** - Senior technical lead who analyzes complex projects and coordinates multi-step development tasks
- **[Project Analyst](agents/orchestrators/project-analyst.md)** - Technology stack detection specialist who enables intelligent agent routing
- **[Team Configurator](agents/orchestrators/team-configurator.md)** - AI team setup expert who detects your stack and configures optimal agent mappings

#### 💼 Framework Specialists (13 agents)

- **Laravel (2 agents)**
  - **[Backend Expert](agents/specialized/laravel/laravel-backend-expert.md)** - Comprehensive Laravel development with MVC, services, and Eloquent patterns
  - **[Eloquent Expert](agents/specialized/laravel/laravel-eloquent-expert.md)** - Advanced ORM optimization, complex queries, and database performance
- **Django (3 agents)**
  - **[Backend Expert](agents/specialized/django/django-backend-expert.md)** - Models, views, services following current Django conventions
  - **[API Developer](agents/specialized/django/django-api-developer.md)** - Django REST Framework and GraphQL implementations
  - **[ORM Expert](agents/specialized/django/django-orm-expert.md)** - Query optimization and database performance for Django applications
- **Rails (3 agents)**
  - **[Backend Expert](agents/specialized/rails/rails-backend-expert.md)** - Full-stack Rails development following conventions
  - **[API Developer](agents/specialized/rails/rails-api-developer.md)** - RESTful APIs and GraphQL with Rails patterns
  - **[ActiveRecord Expert](agents/specialized/rails/rails-activerecord-expert.md)** - Complex queries and database optimization
- **React (2 agents)**
  - **[Component Architect](agents/specialized/react/react-component-architect.md)** - Modern React patterns, hooks, and component design
  - **[Next.js Expert](agents/specialized/react/react-nextjs-expert.md)** - SSR, SSG, ISR, and full-stack Next.js applications
- **Vue (3 agents)**
  - **[Component Architect](agents/specialized/vue/vue-component-architect.md)** - Vue 3 Composition API and component patterns
  - **[Nuxt Expert](agents/specialized/vue/vue-nuxt-expert.md)** - SSR, SSG, and full-stack Nuxt applications
  - **[State Manager](agents/specialized/vue/vue-state-manager.md)** - Pinia and Vuex state architecture

#### 🌐 Universal Experts (4 agents)

- **[Backend Developer](agents/universal/backend-developer.md)** - Polyglot backend development across multiple languages and frameworks
- **[Frontend Developer](agents/universal/frontend-developer.md)** - Modern web technologies and responsive design for any framework
- **[API Architect](agents/universal/api-architect.md)** - RESTful design, GraphQL, and framework-agnostic API architecture
- **[Tailwind Frontend Expert](agents/universal/tailwind-css-expert.md)** - Tailwind CSS styling, utility-first development, and responsive components

#### 🔧 Core Team (4 agents)

- **[Code Archaeologist](agents/core/code-archaeologist.md)** - Explores, documents, and analyzes unfamiliar or legacy codebases
- **[Code Reviewer](agents/core/code-reviewer.md)** - Rigorous security-aware reviews with severity-tagged reports
- **[Performance Optimizer](agents/core/performance-optimizer.md)** - Identifies bottlenecks and applies optimizations for scalable systems
- **[Documentation Specialist](agents/core/documentation-specialist.md)** - Crafts comprehensive READMEs, API specs, and technical documentation

**Total: 24 specialized agents** working together to build your projects!

[Browse all agents →](agents/)

### 🔥 Why Teams Beat Solo AI

- **Specialized Expertise**: Each agent masters their domain with deep, current knowledge
- **Real Collaboration**: Agents coordinate seamlessly, sharing context and handing off tasks
- **Tailored Solutions**: Get code that matches your exact stack and follows its best practices
- **Parallel Execution**: Multiple specialists work simultaneously for faster delivery

### 📈 The Impact

- **Ship Faster** - Complete features in minutes, not days
- **Better Code Quality** - Every line follows best practices
- **Learn As You Code** - See how experts approach problems
- **Scale Confidently** - Architecture designed for growth

### 📚 Learn More

- [Creating Custom Agents](docs/creating-agents.md) - Build specialists for your needs
- [Best Practices](docs/best-practices.md) - Get the most from your AI team

### 💬 Join The Community

- ⭐ **Star this repo** to show support
- 🐛 [Report issues](https://github.com/vijaythecoder/awesome-claude-agents/issues)
- 💡 [Share ideas](https://github.com/vijaythecoder/awesome-claude-agents/discussions)
- 🎉 [Success stories](https://github.com/vijaythecoder/awesome-claude-agents/discussions/categories/show-and-tell)

### 📄 License

MIT License - Use freely in your projects!

### Star History

[![Star History Chart](https://api.star-history.com/svg?repos=vijaythecoder/awesome-claude-agents&type=Date)](https://www.star-history.com/#vijaythecoder/awesome-claude-agents&Date)
---

<p align="center">
  <strong>Transform Claude Code into an AI development team that ships production-ready features</strong><br>
  <em>Simple setup. Powerful results. Just describe and build.</em>
</p>

<p align="center">
  <a href="https://github.com/vijaythecoder/awesome-claude-agents">GitHub</a> •
  <a href="docs/creating-agents.md">Documentation</a> •
  <a href="https://github.com/vijaythecoder/awesome-claude-agents/discussions">Community</a>
</p>

````

## 五、输出要求

直接给出译文，用 ``` 包裹便于复制。**不要**输出任何解释、前言或后记。

```

## 五、AI 返回的译文全文

```markdown
# Awesome Claude Agents - AI Development Team 🚀

**用一支专业化的 AI 智能体团队为 Claude Code 提速**：它们协同工作，构建完整功能、调试复杂问题，并以专家级知识应对任何技术栈。

### ⚠️ 重要提示

**本项目处于实验阶段，且非常消耗 token。** 我正在用 Claude 订阅积极测试这些智能体 —— 复杂工作流中的 token 消耗会很高。多智能体编排在每个复杂功能上可能消耗 10-50k token。请谨慎使用并留意你的用量。

### 🚀 快速开始（3 分钟）

#### 前置条件

- 已安装并完成认证的 **Claude Code CLI**
- **Claude 订阅** —— 密集的智能体工作流需要它
- 一个包含你代码库的可用项目目录
- **可选**：[Context7 MCP](docs/dependencies.md)，用于增强文档访问

#### 1. 安装智能体

```bash
git clone https://github.com/vijaythecoder/awesome-claude-agents.git
```

##### 方案 A：符号链接（推荐 —— 可自动更新）

**macOS/Linux：**
```bash
## Create agents directory if it doesn't exist (preserves existing agents)

mkdir -p ~/.claude/agents

## Symlink the awesome-claude-agents collection

ln -sf "$(pwd)/awesome-claude-agents/agents/" ~/.claude/agents/awesome-claude-agents
```

**Windows（PowerShell）：**
```powershell
## Create agents directory

New-Item -Path "$env:USERPROFILE\.claude\agents" -ItemType Directory -Force

## Create symlink

cmd /c mklink /D "$env:USERPROFILE\.claude\agents\awesome-claude-agents" "$(Get-Location)\awesome-claude-agents\agents"
```

##### 方案 B：复制（静态 —— 不会自动更新）

```bash
## Create agents directory if it doesn't exist

mkdir -p ~/.claude/agents

## Copy all agents

cp -r awesome-claude-agents/agents ~/.claude/agents/awesome-claude-agents
```

#### 2. 验证安装

```bash
claude /agents
## Should show all 24 agents.

```

#### 3. 初始化你的项目

**进入**你的**项目目录**，运行下面这条命令来配置你的 AI 团队：

```bash
claude "use @agent-team-configurator and optimize my project to best use the available subagents."
```

#### 4. 开始构建

```bash
claude "use @agent-tech-lead-orchestrator and build a user authentication system"
```

你的 AI 团队会自动识别你的技术栈，并调用合适的专家！

### 🎯 自动配置如何工作

@agent-team-configurator 会自动为你组建一支完美的 AI 开发团队。被调用时，它会：

1. **定位 CLAUDE.md** —— 找到现有项目配置，并完整保留你在「AI Team Configuration」区段之外的所有自定义内容
2. **识别技术栈** —— 检查 package.json、composer.json、requirements.txt、go.mod、Gemfile 以及构建配置，从而理解你的项目
3. **发现可用智能体** —— 扫描 ~/.claude/agents/ 与 .claude/ 目录，构建一张包含所有可用专家的能力表
4. **挑选专家** —— 优先选择框架专属智能体而非通用智能体，并始终纳入 @agent-code-reviewer 与 @agent-performance-optimizer 以保证质量
5. **更新 CLAUDE.md** —— 生成一个带时间戳的「AI Team Configuration」区段，写入识别到的技术栈与一张 Task|Agent|Notes 映射表
6. **给出使用指引** —— 向你展示识别到的技术栈、选中的智能体，并给出可以立即开始的示例命令

### 👥 认识你的 AI 开发团队

#### 🎭 编排者（3 个智能体）

- **[Tech Lead Orchestrator](agents/orchestrators/tech-lead-orchestrator.md)** —— 资深技术负责人，负责分析复杂项目并协调多步骤开发任务
- **[Project Analyst](agents/orchestrators/project-analyst.md)** —— 技术栈识别专家，为智能体的智能路由提供支撑
- **[Team Configurator](agents/orchestrators/team-configurator.md)** —— AI 团队组建专家，识别你的技术栈并配置最优的智能体映射

#### 💼 框架专家（13 个智能体）

- **Laravel（2 个智能体）**
  - **[Backend Expert](agents/specialized/laravel/laravel-backend-expert.md)** —— 全面的 Laravel 开发，涵盖 MVC、服务与 Eloquent 模式
  - **[Eloquent Expert](agents/specialized/laravel/laravel-eloquent-expert.md)** —— 高级 ORM 优化、复杂查询与数据库性能
- **Django（3 个智能体）**
  - **[Backend Expert](agents/specialized/django/django-backend-expert.md)** —— 遵循当前 Django 惯例的模型、视图与服务
  - **[API Developer](agents/specialized/django/django-api-developer.md)** —— Django REST Framework 与 GraphQL 实现
  - **[ORM Expert](agents/specialized/django/django-orm-expert.md)** —— 面向 Django 应用的查询优化与数据库性能
- **Rails（3 个智能体）**
  - **[Backend Expert](agents/specialized/rails/rails-backend-expert.md)** —— 遵循惯例的全栈 Rails 开发
  - **[API Developer](agents/specialized/rails/rails-api-developer.md)** —— 以 Rails 模式实现 RESTful API 与 GraphQL
  - **[ActiveRecord Expert](agents/specialized/rails/rails-activerecord-expert.md)** —— 复杂查询与数据库优化
- **React（2 个智能体）**
  - **[Component Architect](agents/specialized/react/react-component-architect.md)** —— 现代 React 模式、hooks 与组件设计
  - **[Next.js Expert](agents/specialized/react/react-nextjs-expert.md)** —— SSR、SSG、ISR 与全栈 Next.js 应用
- **Vue（3 个智能体）**
  - **[Component Architect](agents/specialized/vue/vue-component-architect.md)** —— Vue 3 Composition API 与组件模式
  - **[Nuxt Expert](agents/specialized/vue/vue-nuxt-expert.md)** —— SSR、SSG 与全栈 Nuxt 应用
  - **[State Manager](agents/specialized/vue/vue-state-manager.md)** —— Pinia 与 Vuex 状态架构

#### 🌐 通用专家（4 个智能体）

- **[Backend Developer](agents/universal/backend-developer.md)** —— 跨多种语言与框架的多语言后端开发
- **[Frontend Developer](agents/universal/frontend-developer.md)** —— 面向任意框架的现代 Web 技术与响应式设计
- **[API Architect](agents/universal/api-architect.md)** —— RESTful 设计、GraphQL 与框架无关的 API 架构
- **[Tailwind Frontend Expert](agents/universal/tailwind-css-expert.md)** —— Tailwind CSS 样式、实用优先开发与响应式组件

#### 🔧 核心团队（4 个智能体）

- **[Code Archaeologist](agents/core/code-archaeologist.md)** —— 探索、记录并分析陌生或遗留的代码库
- **[Code Reviewer](agents/core/code-reviewer.md)** —— 严谨且具安全意识代码审查，报告带严重级别标注
- **[Performance Optimizer](agents/core/performance-optimizer.md)** —— 定位瓶颈，并为可扩展系统实施优化
- **[Documentation Specialist](agents/core/documentation-specialist.md)** —— 撰写完整的 README、API 规格与技术文档

**共 24 个专业化智能体**，协同构建你的项目！

[浏览全部智能体 →](agents/)

### 🔥 为什么团队胜过单打独斗的 AI

- **专业化能力**：每个智能体都以深入且最新的知识精通自己的领域
- **真正的协作**：智能体之间无缝协调，共享上下文并交接任务
- **量身定制的方案**：拿到的代码贴合你的确切技术栈，并遵循其最佳实践
- **并行执行**：多个专家同时工作，交付更快

### 📈 带来的效果

- **更快交付** —— 几分钟而不是几天完成一个功能
- **更好的代码质量** —— 每一行都遵循最佳实践
- **边写边学** —— 看专家如何着手解决问题
- **放心扩展** —— 架构为增长而设计

### 📚 了解更多

- [创建自定义智能体](docs/creating-agents.md) —— 为你的需求打造专家
- [最佳实践](docs/best-practices.md) —— 让你的 AI 团队发挥最大价值

### 💬 加入社区

- ⭐ **给本仓库点星** 以示支持
- 🐛 [报告问题](https://github.com/vijaythecoder/awesome-claude-agents/issues)
- 💡 [分享想法](https://github.com/vijaythecoder/awesome-claude-agents/discussions)
- 🎉 [成功案例](https://github.com/vijaythecoder/awesome-claude-agents/discussions/categories/show-and-tell)

### 📄 许可证

MIT License —— 可在你的项目中自由使用！

### Star History

[![Star History Chart](https://api.star-history.com/svg?repos=vijaythecoder/awesome-claude-agents&type=Date)](https://www.star-history.com/#vijaythecoder/awesome-claude-agents&Date)
---

<p align="center">
  <strong>把 Claude Code 变成一支能交付生产就绪功能的 AI 开发团队</strong><br>
  <em>配置简单。效果强大。只需描述，然后构建。</em>
</p>

<p align="center">
  <a href="https://github.com/vijaythecoder/awesome-claude-agents">GitHub</a> •
  <a href="docs/creating-agents.md">Documentation</a> •
  <a href="https://github.com/vijaythecoder/awesome-claude-agents/discussions">Community</a>
</p>

```
