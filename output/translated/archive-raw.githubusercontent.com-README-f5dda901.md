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
