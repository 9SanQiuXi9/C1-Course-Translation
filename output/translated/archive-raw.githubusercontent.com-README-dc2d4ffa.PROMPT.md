# 翻译留痕：archive-raw.githubusercontent.com-README-dc2d4ffa

- doc_id：`archive-raw.githubusercontent.com-README-dc2d4ffa`
- 时间：2026-09-27T16:33:50+08:00
- 原文：`extracted/archive-raw.githubusercontent.com-README-dc2d4ffa.md`
- 译文：`translated/archive-raw.githubusercontent.com-README-dc2d4ffa.md`
- 原文 sha256：`1205d37061a96985c5869bcab55b8c8c9902b9441103aa10d565f75672c0e7e9`
- 译文 sha256：`b5a6b00a092e697476b5fb8dc63a662bca68e8c04fc091f2312099b057df3b17`
- 术语约束条数：13

## 一、本文档涉及的术语清单

| 英文 | 译法 | handling | 出现次数 |
|---|---|---|---|
| `mcp` | MCP | `acronym` | 18 |
| `server` | 服务器 | `translate` | 17 |
| `client` | 客户端 | `translate` | 12 |
| `api` | API | `acronym` | 4 |
| `tool` | 工具 | `translate` | 3 |
| `context` | 上下文 | `translate` | 3 |
| `spec` | 规格 | `translate` | 3 |
| `template` | 模板 | `translate` | 2 |
| `model` | 模型 | `translate` | 1 |
| `prompt` | 提示词 | `translate` | 1 |
| `security` | 安全 | `translate` | 1 |
| `llm` | LLM | `acronym` | 1 |
| `repository` | 仓库 | `translate` | 1 |

## 二、落盘校验结果

```json
{
  "non_empty": true,
  "code_blocks_total": 5,
  "code_blocks_in_translation": 5,
  "code_blocks_match": true,
  "code_blocks_byte_identical": true,
  "urls_orig": 24,
  "urls_trans": 24,
  "urls_all_present": true,
  "urls_counts_equal": true,
  "headings_orig": 14,
  "headings_trans": 14,
  "headings_match": true,
  "orig_chars": 5977,
  "trans_chars": 4179,
  "length_ratio": 0.6992,
  "length_ratio_ok": true
}
```

## 四、发出的 prompt 全文

```markdown
(未找到 prompt 导出文件)
```

## 五、AI 返回的译文全文

```markdown
# MCP TypeScript SDK

<!-- prettier-ignore -->
> [!IMPORTANT]
> **这是 `main` 分支 —— SDK 的 v2**（`@modelcontextprotocol/server`、`@modelcontextprotocol/client`），实现 [2026-07-28 版 MCP 规格](https://modelcontextprotocol.io/specification/2026-07-28)。
>
> **有反馈？请[提交 v2 issue](https://github.com/modelcontextprotocol/typescript-sdk/issues/new?template=v2-feedback.yml)** —— 这是目前你能为 SDK 做的最有用的事。[v2 文档](https://ts.sdk.modelcontextprotocol.io/v2/)从一个十分钟的服务器教程开始。
>
> **v2 是稳定发布线**，与 2026-07-28 版规格同期发布。v1.x 在 v2 发布后至少 6 个月内仍会收到缺陷修复与安全更新。v1 文档：[ts.sdk.modelcontextprotocol.io](https://ts.sdk.modelcontextprotocol.io/) · v2：[`/v2/`](https://ts.sdk.modelcontextprotocol.io/v2/)。

<!-- prettier-ignore -->
> [!WARNING]
> **在 v2 于 [2026-07-28 版规格](https://modelcontextprotocol.io/specification/2026-07-28)发布后趋于稳定的这段时间，我们把拉取请求限制为每位新贡献者 1 个。**
>
> 目前最有用的反馈方式是[提交 issue](https://github.com/modelcontextprotocol/typescript-sdk/issues/new?template=v2-feedback.yml) —— 等 v2 稳定后我们会重新开放 PR。

[![NPM Version - Server](https://img.shields.io/npm/v/%40modelcontextprotocol%2Fserver?label=%40modelcontextprotocol%2Fserver)](https://www.npmjs.com/package/@modelcontextprotocol/server)
[![NPM Version - Client](https://img.shields.io/npm/v/%40modelcontextprotocol%2Fclient?label=%40modelcontextprotocol%2Fclient)](https://www.npmjs.com/package/@modelcontextprotocol/client) ![MIT licensed](https://img.shields.io/npm/l/%40modelcontextprotocol%2Fserver)

<details>
<summary>目录</summary>

- [概览](#overview)
- [包](#packages)
- [安装](#installation)
- [快速上手](#getting-started)
- [文档](#documentation)
- [贡献](#contributing)
- [许可证](#license)

</details>

### 概览

Model Context Protocol（MCP）让应用能以标准化方式为 LLM 提供上下文，从而把「提供上下文」与「实际的 LLM 交互」这两件事的关注点分离开。

本仓库包含 MCP 规格的 TypeScript SDK 实现。它可运行在 **Node.js**、**Bun** 和 **Deno** 上，并提供：

- MCP **服务器**库（工具/资源/提示词、Streamable HTTP、stdio、认证辅助工具）
- MCP **客户端**库（传输层、高层辅助工具、OAuth 辅助工具）
- 针对特定运行时/框架的可选**中间件包**（Express、Fastify、Hono、Node.js HTTP）
- 可运行的**示例**（位于 [`examples/`](https://github.com/modelcontextprotocol/typescript-sdk/tree/main/examples) 下）

### 包

这个 monorepo 发布拆分的包：

- **`@modelcontextprotocol/server`**：构建 MCP 服务器
- **`@modelcontextprotocol/client`**：构建 MCP 客户端

工具与提示词的 schema 使用 [Standard Schema](https://standardschema.dev/) —— 你可以带上 Zod v4、Valibot、ArkType 或任何兼容库。

#### 中间件包（可选）

SDK 还在 [`packages/middleware/`](https://github.com/modelcontextprotocol/typescript-sdk/tree/main/packages/middleware) 下发布小型「中间件」包，帮助你**把 MCP 接入特定的运行时或 Web 框架**。

它们刻意保持为薄适配层：不应引入新的 MCP 功能或业务逻辑。详见 [`packages/middleware/README.md`](packages/middleware/README.md)。

- **`@modelcontextprotocol/node`**：针对 `IncomingMessage` / `ServerResponse` 的 Node.js Streamable HTTP 传输包装
- **`@modelcontextprotocol/express`**：Express 辅助工具（应用默认配置 + Host 头校验）
- **`@modelcontextprotocol/fastify`**：Fastify 辅助工具（应用默认配置 + Host 头校验）
- **`@modelcontextprotocol/hono`**：Hono 辅助工具（应用默认配置 + JSON 请求体解析钩子 + Host 头校验）

### 安装

#### 服务器

```bash
npm install @modelcontextprotocol/server
## or

bun add @modelcontextprotocol/server
## or

deno add npm:@modelcontextprotocol/server
```

#### 客户端

```bash
npm install @modelcontextprotocol/client
## or

bun add @modelcontextprotocol/client
## or

deno add npm:@modelcontextprotocol/client
```

#### 可选的中间件包

SDK 还发布可选的「中间件」包，帮助你**把 MCP 接入特定的运行时或 Web 框架**（例如 Express、Fastify、Hono 或 Node.js 的 `http`）。

这些包刻意保持为薄适配层，不应引入额外的 MCP 功能或业务逻辑。详见 [`packages/middleware/README.md`](packages/middleware/README.md)。

```bash
## Node.js HTTP (IncomingMessage/ServerResponse) Streamable HTTP transport:

npm install @modelcontextprotocol/node

## Express integration:

npm install @modelcontextprotocol/express express

## Fastify integration:

npm install @modelcontextprotocol/fastify fastify

## Hono integration:

npm install @modelcontextprotocol/hono hono
```

### 快速上手

下面是一个 MCP 服务器长什么样。这个最小示例通过 stdio 暴露了单个 `greet` 工具：

```typescript
import { McpServer } from '@modelcontextprotocol/server';
import { StdioServerTransport } from '@modelcontextprotocol/server/stdio';
import * as z from 'zod/v4';

const server = new McpServer({ name: 'greeting-server', version: '1.0.0' });

server.registerTool(
    'greet',
    {
        description: 'Greet someone by name',
        inputSchema: z.object({ name: z.string() })
    },
    async ({ name }) => ({
        content: [{ type: 'text', text: `Hello, ${name}!` }]
    })
);

async function main() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
}

main();
```

准备好构建真正的东西了？跟着分步教程走：

- [构建你的第一个服务器](docs/get-started/first-server.md) —— 一个 stdio 天气预警服务器，从 `npm init` 到一次工具调用
- [构建你的第一个客户端](docs/get-started/first-client.md) —— 连接到那个服务器，列出它的工具并调用它们

想看在教程之外可运行的端到端示例，请见：

- [`examples/README.md`](examples/README.md) —— 可运行、可自验证的客户端/服务器示例配对（每个目录一个故事）

### 文档

- [构建服务器](docs/get-started/first-server.md) —— 你的第一个 MCP 服务器，逐步讲解
- [构建客户端](docs/get-started/first-client.md) —— 你的第一个 MCP 客户端，逐步讲解
- [文档站点](https://ts.sdk.modelcontextprotocol.io/v2/) —— 完整指南：工具、资源、提示词、通过 HTTP 与 stdio 提供服务、客户端、OAuth 以及迁移
- [故障排查](docs/troubleshooting.md) —— 常见错误及其修复方法
- [API 参考](https://ts.sdk.modelcontextprotocol.io/v2/api/)
- [MCP 文档](https://modelcontextprotocol.io/docs)
- [MCP 规格](https://modelcontextprotocol.io/specification/latest)

#### 在本地构建文档

要在本地开发文档站点：

```bash
pnpm docs:api      # Generate the API reference markdown (output: docs/api/)
pnpm docs:dev      # Start the VitePress dev server for the V2 site
pnpm docs:build    # Build the V2 site (output: docs/.vitepress/dist/)
pnpm docs:multi    # Build the combined V1 + V2 site (output: tmp/docs-combined/)
```

`docs:multi` 脚本会从当前检出构建 V2 站点，通过 git worktree 检出 `v1.x` 分支来构建 V1 站点，产出一个合并站点：V1 文档在根路径，V2 文档在 `/v2/` 下。

### v1（旧版）文档与修复

如果你使用的是 SDK 的 **v1** 代，**v1 API 文档**可在 [`https://ts.sdk.modelcontextprotocol.io/`](https://ts.sdk.modelcontextprotocol.io/) 查看。v1 源代码以及所有 v1 专属修复都位于长期维护的
[`v1.x` 分支](https://github.com/modelcontextprotocol/typescript-sdk/tree/v1.x)。V2 API 文档在 [`/v2/`](https://ts.sdk.modelcontextprotocol.io/v2/)。

### 贡献

欢迎在 GitHub 上提交 issue 与拉取请求：<https://github.com/modelcontextprotocol/typescript-sdk>。

### 许可证

本项目的新贡献采用 Apache License 2.0 许可，既有代码采用 MIT。详见 [LICENSE](LICENSE) 文件。

```
