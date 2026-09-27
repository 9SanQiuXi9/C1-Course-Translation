# 翻译留痕：archive-raw.githubusercontent.com-README-f5dda901

- doc_id：`archive-raw.githubusercontent.com-README-f5dda901`
- 时间：2026-09-27T16:52:53+08:00
- 原文：`extracted/archive-raw.githubusercontent.com-README-f5dda901.md`
- 译文：`translated/archive-raw.githubusercontent.com-README-f5dda901.md`
- 原文 sha256：`96d9090ba05c1a5385fc34ec4f9bf47a260acf3e507837a46fa3ebb311e8bebc`
- 译文 sha256：`2e67f7a70196572ab218a578a8967038e12409c814be9293ce8e09491f69316e`
- 术语约束条数：14

## 一、本文档涉及的术语清单

| 英文 | 译法 | handling | 出现次数 |
|---|---|---|---|
| `mcp` | MCP | `acronym` | 32 |
| `server` | 服务器 | `translate` | 14 |
| `repository` | 仓库 | `translate` | 10 |
| `model` | 模型 | `translate` | 5 |
| `security` | 安全 | `translate` | 5 |
| `context` | 上下文 | `translate` | 4 |
| `api` | API | `acronym` | 3 |
| `client` | 客户端 | `translate` | 3 |
| `retrieval` | 检索 | `translate` | 3 |
| `agent` | 智能体 | `translate` | 1 |
| `automation` | 自动化 | `translate` | 1 |
| `llm` | LLM | `acronym` | 1 |
| `best practices` | 最佳实践 | `translate` | 1 |
| `threat model` | 威胁模型 | `translate` | 1 |

## 二、落盘校验结果

```json
{
  "non_empty": true,
  "code_blocks_total": 5,
  "code_blocks_in_translation": 5,
  "code_blocks_match": true,
  "code_blocks_byte_identical": true,
  "urls_orig": 35,
  "urls_trans": 35,
  "urls_all_present": true,
  "urls_counts_equal": true,
  "headings_orig": 14,
  "headings_trans": 14,
  "headings_match": true,
  "orig_chars": 6773,
  "trans_chars": 4609,
  "length_ratio": 0.6805,
  "length_ratio_ok": true
}
```

## 四、发出的 prompt 全文

```markdown
# 翻译任务：archive-raw.githubusercontent.com-README-f5dda901

## 一、文档元数据

- doc_id：`archive-raw.githubusercontent.com-README-f5dda901`
- title：Model Context Protocol servers
- origin_url：https://github.com/modelcontextprotocol/servers
- 本段字符数：8,695

## 二、术语约束（本文档用到的，必须严格遵守）

| 英文 | 处理方式 | 出现次数 |
|---|---|---|
| `mcp` | 保留英文缩写（首次出现给全称） | 32 |
| `server` | 翻译为「服务器」 | 14 |
| `repository` | 翻译为「仓库」 | 10 |
| `model` | 翻译为「模型」 | 5 |
| `security` | 翻译为「安全」 | 5 |
| `context` | 翻译为「上下文」 | 4 |
| `api` | 保留英文缩写（首次出现给全称） | 3 |
| `client` | 翻译为「客户端」 | 3 |
| `retrieval` | 翻译为「检索」 | 3 |
| `agent` | 翻译为「智能体」 | 1 |
| `automation` | 翻译为「自动化」 | 1 |
| `llm` | 保留英文缩写（首次出现给全称） | 1 |
| `best practices` | 翻译为「最佳实践」 | 1 |
| `threat model` | 翻译为「威胁模型」 | 1 |

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


# Model Context Protocol servers

This repository is a collection of *reference implementations* for the [Model Context Protocol](https://modelcontextprotocol.io/) (MCP), as well as references to community-built servers and additional resources.

> [!IMPORTANT]
> If you are looking for a list of MCP servers, you can browse published servers on [the MCP Registry](https://registry.modelcontextprotocol.io/). The repository served by this README is dedicated to housing just the small number of reference servers maintained by the MCP steering group.

> [!WARNING]
> The servers in this repository are intended as **reference implementations** to demonstrate MCP features and SDK usage. They are meant to serve as educational examples for developers building their own MCP servers, not as production-ready solutions. Developers should evaluate their own security requirements and implement appropriate safeguards based on their specific threat model and use case.

The servers in this repository showcase the versatility and extensibility of MCP, demonstrating how it can be used to give Large Language Models (LLMs) secure, controlled access to tools and data sources.
Typically, each MCP server is implemented with an MCP SDK:

- [C# MCP SDK](https://github.com/modelcontextprotocol/csharp-sdk)
- [Go MCP SDK](https://github.com/modelcontextprotocol/go-sdk)
- [Java MCP SDK](https://github.com/modelcontextprotocol/java-sdk)
- [Kotlin MCP SDK](https://github.com/modelcontextprotocol/kotlin-sdk)
- [PHP MCP SDK](https://github.com/modelcontextprotocol/php-sdk)
- [Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Ruby MCP SDK](https://github.com/modelcontextprotocol/ruby-sdk)
- [Rust MCP SDK](https://github.com/modelcontextprotocol/rust-sdk)
- [Swift MCP SDK](https://github.com/modelcontextprotocol/swift-sdk)
- [TypeScript MCP SDK](https://github.com/modelcontextprotocol/typescript-sdk)

### 🌟 Reference Servers

These servers aim to demonstrate MCP features and the official SDKs.

- **[Everything](src/everything)** - Reference / test server with prompts, resources, and tools.
- **[Fetch](src/fetch)** - Web content fetching and conversion for efficient LLM usage.
- **[Filesystem](src/filesystem)** - Secure file operations with configurable access controls.
- **[Git](src/git)** - Tools to read, search, and manipulate Git repositories.
- **[Memory](src/memory)** - Knowledge graph-based persistent memory system.
- **[Sequential Thinking](src/sequentialthinking)** - Dynamic and reflective problem-solving through thought sequences.
- **[Time](src/time)** - Time and timezone conversion capabilities.

#### Archived

The following reference servers are now archived and can be found at [servers-archived](https://github.com/modelcontextprotocol/servers-archived).

- **[AWS KB Retrieval](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/aws-kb-retrieval-server)** - Retrieval from AWS Knowledge Base using Bedrock Agent Runtime.
- **[Brave Search](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/brave-search)** - Web and local search using Brave's Search API. Has been replaced by the [official server](https://github.com/brave/brave-search-mcp-server) ([`@brave/brave-search-mcp-server`](https://www.npmjs.com/package/@brave/brave-search-mcp-server)).
- **[EverArt](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/everart)** - AI image generation using various models.
- **[GitHub](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/github)** - Repository management, file operations, and GitHub API integration.
- **[GitLab](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/gitlab)** - GitLab API, enabling project management.
- **[Google Drive](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/gdrive)** - File access and search capabilities for Google Drive.
- **[Google Maps](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/google-maps)** - Location services, directions, and place details.
- **[PostgreSQL](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/postgres)** - Read-only database access with schema inspection.
- **[Puppeteer](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/puppeteer)** - Browser automation and web scraping.
- **[Redis](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/redis)** - Interact with Redis key-value stores.
- **[Sentry](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/sentry)** - Retrieving and analyzing issues from Sentry.io.
- **[Slack](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/slack)** - Channel management and messaging capabilities. Now maintained by [Zencoder](https://github.com/zencoderai/slack-mcp-server)
- **[SQLite](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/sqlite)** - Database interaction and business intelligence capabilities.

### 🚀 Getting Started

#### Using MCP Servers in this Repository

TypeScript-based servers in this repository can be used directly with `npx`.

For example, this will start the [Memory](src/memory) server:
```sh
npx -y @modelcontextprotocol/server-memory
```

Python-based servers in this repository can be used directly with [`uvx`](https://docs.astral.sh/uv/concepts/tools/) or [`pip`](https://pypi.org/project/pip/). `uvx` is recommended for ease of use and setup.

For example, this will start the [Git](src/git) server:
```sh
## With uvx

uvx mcp-server-git

## With pip

pip install mcp-server-git
python -m mcp_server_git
```

Follow [these](https://docs.astral.sh/uv/getting-started/installation/) instructions to install `uv` / `uvx` and [these](https://pip.pypa.io/en/stable/installation/) to install `pip`.

#### Using an MCP Client

However, running a server on its own isn't very useful, and should instead be configured into an MCP client. For example, here's the Claude Desktop configuration to use the above server:

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

On Windows, wrap `npx` with `cmd /c`:

```json
{
  "mcpServers": {
    "memory": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

Additional examples of using the Claude Desktop as an MCP client might look like:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/files"]
    },
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "path/to/git/repo"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_TOKEN>"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
    }
  }
}
```

On Windows, apply the same wrapper to each `npx`-based entry above by changing `"command"` to `"cmd"` and prepending `"/c", "npx"` to the existing `args`. Leave `uvx` entries unchanged.

### 🛠️ Creating Your Own Server

Interested in creating your own MCP server? Visit the official documentation at [modelcontextprotocol.io](https://modelcontextprotocol.io/introduction) for comprehensive guides, best practices, and technical details on implementing MCP servers.

### 📚 Learn More

See [ADDITIONAL.md](ADDITIONAL.md) for a curated list of frameworks and resources that simplify building MCP servers and clients.

### 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for information about contributing to this repository.

### 📦 Releasing

See [RELEASING.md](RELEASING.md) for how packages are published (OIDC trusted publishing from CI — no registry tokens) and how to retry a failed publish.

### 🔒 Security

See [SECURITY.md](SECURITY.md) for reporting security vulnerabilities.

### 📜 License

This project is licensed under the Apache License, Version 2.0 for new contributions, with existing code under MIT - see the [LICENSE](LICENSE) file for details.

### 💬 Community

- [GitHub Discussions](https://github.com/orgs/modelcontextprotocol/discussions)

### ⭐ Support

If you find MCP servers useful, please consider starring the repository and contributing new servers or improvements!

---

Managed by Anthropic, but built together with the community. The Model Context Protocol is open source and we encourage everyone to contribute their own servers and improvements!

````

## 五、输出要求

直接给出译文，用 ``` 包裹便于复制。**不要**输出任何解释、前言或后记。

```

## 五、AI 返回的译文全文

```markdown
# Model Context Protocol servers

本仓库收录了 [Model Context Protocol](https://modelcontextprotocol.io/)（MCP）的*参考实现*集合，以及社区构建的服务器与附加资源的索引。

> [!IMPORTANT]
> 如果你在找 MCP 服务器清单，可以在 [MCP Registry](https://registry.modelcontextprotocol.io/) 上浏览已发布的服务器。本 README 所对应的仓库只用于存放 MCP 指导组维护的少量参考服务器。

> [!WARNING]
> 本仓库中的服务器旨在作为**参考实现**，用于演示 MCP 特性与 SDK 用法。它们是给自建 MCP 服务器的开发者参考的教学示例，并非生产可用的方案。开发者应自行评估自身安全要求，并根据自己的威胁模型与用例实施恰当的防护措施。

本仓库中的服务器展示了 MCP 的通用性与可扩展性，演示如何用它为大型语言模型（LLM）提供安全、受控的工具与数据源访问。
通常，每个 MCP 服务器都是用某个 MCP SDK 实现的：

- [C# MCP SDK](https://github.com/modelcontextprotocol/csharp-sdk)
- [Go MCP SDK](https://github.com/modelcontextprotocol/go-sdk)
- [Java MCP SDK](https://github.com/modelcontextprotocol/java-sdk)
- [Kotlin MCP SDK](https://github.com/modelcontextprotocol/kotlin-sdk)
- [PHP MCP SDK](https://github.com/modelcontextprotocol/php-sdk)
- [Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Ruby MCP SDK](https://github.com/modelcontextprotocol/ruby-sdk)
- [Rust MCP SDK](https://github.com/modelcontextprotocol/rust-sdk)
- [Swift MCP SDK](https://github.com/modelcontextprotocol/swift-sdk)
- [TypeScript MCP SDK](https://github.com/modelcontextprotocol/typescript-sdk)

### 🌟 参考服务器

这些服务器旨在演示 MCP 特性与官方 SDK。

- **[Everything](src/everything)** —— 含提示词、资源与工具的参考/测试服务器。
- **[Fetch](src/fetch)** —— 抓取网页内容并转换，以便 LLM 高效使用。
- **[Filesystem](src/filesystem)** —— 带可配置访问控制的安全文件操作。
- **[Git](src/git)** —— 读取、搜索与操作 Git 仓库的工具。
- **[Memory](src/memory)** —— 基于知识图谱的持久记忆系统。
- **[Sequential Thinking](src/sequentialthinking)** —— 通过思维序列进行动态、反思式的问题求解。
- **[Time](src/time)** —— 时间与时区转换能力。

#### 已归档

以下参考服务器现已归档，可在 [servers-archived](https://github.com/modelcontextprotocol/servers-archived) 中找到。

- **[AWS KB Retrieval](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/aws-kb-retrieval-server)** —— 使用 Bedrock Agent Runtime 从 AWS Knowledge Base 检索。
- **[Brave Search](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/brave-search)** —— 使用 Brave 的 Search API 做网页与本地搜索。已被[官方服务器](https://github.com/brave/brave-search-mcp-server)取代（[`@brave/brave-search-mcp-server`](https://www.npmjs.com/package/@brave/brave-search-mcp-server)）。
- **[EverArt](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/everart)** —— 使用多种模型进行 AI 图像生成。
- **[GitHub](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/github)** —— 仓库管理、文件操作与 GitHub API 集成。
- **[GitLab](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/gitlab)** —— GitLab API，支持项目管理。
- **[Google Drive](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/gdrive)** —— Google Drive 的文件访问与搜索能力。
- **[Google Maps](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/google-maps)** —— 位置服务、路线导航与地点详情。
- **[PostgreSQL](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/postgres)** —— 带 schema 检视的只读数据库访问。
- **[Puppeteer](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/puppeteer)** —— 浏览器自动化与网页抓取。
- **[Redis](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/redis)** —— 与 Redis 键值存储交互。
- **[Sentry](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/sentry)** —— 从 Sentry.io 检索并分析 issue。
- **[Slack](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/slack)** —— 频道管理与消息能力。现由 [Zencoder](https://github.com/zencoderai/slack-mcp-server) 维护。
- **[SQLite](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/sqlite)** —— 数据库交互与商业智能能力。

### 🚀 快速上手

#### 使用本仓库中的 MCP 服务器

本仓库中基于 TypeScript 的服务器可以直接用 `npx` 运行。

例如，下面这条命令会启动 [Memory](src/memory) 服务器：
```sh
npx -y @modelcontextprotocol/server-memory
```

本仓库中基于 Python 的服务器可以直接用 [`uvx`](https://docs.astral.sh/uv/concepts/tools/) 或 [`pip`](https://pypi.org/project/pip/) 运行。推荐用 `uvx`，更易用也更省配置。

例如，下面这条命令会启动 [Git](src/git) 服务器：
```sh
## With uvx

uvx mcp-server-git

## With pip

pip install mcp-server-git
python -m mcp_server_git
```

请按[这些](https://docs.astral.sh/uv/getting-started/installation/)说明安装 `uv` / `uvx`，按[这些](https://pip.pypa.io/en/stable/installation/)说明安装 `pip`。

#### 使用 MCP 客户端

不过，单独运行一个服务器没什么用，应当把它配置进一个 MCP 客户端。例如，下面是用 Claude Desktop 配置上述服务器的写法：

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

在 Windows 上，要用 `cmd /c` 包一层 `npx`：

```json
{
  "mcpServers": {
    "memory": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

用 Claude Desktop 作为 MCP 客户端的其他示例可能长这样：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/files"]
    },
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "path/to/git/repo"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_TOKEN>"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
    }
  }
}
```

在 Windows 上，对上面每个基于 `npx` 的条目套用同样的包装：把 `"command"` 改成 `"cmd"`，并在原有 `args` 前面加上 `"/c", "npx"`。`uvx` 条目保持不变。

### 🛠️ 创建你自己的服务器

有兴趣自己写一个 MCP 服务器吗？请访问官方文档 [modelcontextprotocol.io](https://modelcontextprotocol.io/introduction)，获取实现 MCP 服务器的完整指南、最佳实践与技术细节。

### 📚 了解更多

请见 [ADDITIONAL.md](ADDITIONAL.md)，其中收录了可简化 MCP 服务器与客户端构建的框架与资源清单。

### 🤝 贡献

关于如何为本仓库做贡献，请见 [CONTRIBUTING.md](CONTRIBUTING.md)。

### 📦 发布

关于软件包如何发布（从 CI 使用 OIDC 可信发布 —— 无需 registry token），以及如何重试失败的发布，请见 [RELEASING.md](RELEASING.md)。

### 🔒 安全

关于如何报告安全漏洞，请见 [SECURITY.md](SECURITY.md)。

### 📜 许可证

本项目的新贡献采用 Apache License 2.0 许可，既有代码采用 MIT —— 详见 [LICENSE](LICENSE) 文件。

### 💬 社区

- [GitHub Discussions](https://github.com/orgs/modelcontextprotocol/discussions)

### ⭐ 支持

如果你觉得 MCP 服务器有用，欢迎给本仓库点星，并贡献新的服务器或改进！

---

由 Anthropic 管理，但与社区共同构建。Model Context Protocol 是开源的，我们鼓励每个人都贡献自己的服务器与改进！

```
