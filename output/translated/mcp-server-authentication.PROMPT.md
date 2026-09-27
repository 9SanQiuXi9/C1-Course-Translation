# 翻译留痕：mcp-server-authentication

- doc_id：`mcp-server-authentication`
- 时间：2026-09-27T17:01:50+08:00
- 原文：`extracted/mcp-server-authentication.md`
- 译文：`translated/mcp-server-authentication.md`
- 原文 sha256：`590ea6e600a5ea3e641251cfe186b2e1af544183b610da91248a52d494d342ea`
- 译文 sha256：`991867b41f8f45cfe8e469c8ba8bc87251c707ec8adb2a0ba957c6a3cb22a0d3`
- 术语约束条数：12

## 一、本文档涉及的术语清单

| 英文 | 译法 | handling | 出现次数 |
|---|---|---|---|
| `mcp` | MCP | `acronym` | 114 |
| `server` | 服务器 | `translate` | 73 |
| `client` | 客户端 | `translate` | 18 |
| `context` | 上下文 | `translate` | 10 |
| `model` | 模型 | `translate` | 8 |
| `api` | API | `acronym` | 6 |
| `repository` | 仓库 | `translate` | 5 |
| `agent` | 智能体 | `translate` | 4 |
| `tool` | 工具 | `translate` | 2 |
| `pull request` | 拉取请求 | `bilingual` | 2 |
| `llm` | LLM | `acronym` | 1 |
| `deployment` | 部署 | `translate` | 1 |

## 二、落盘校验结果

```json
{
  "non_empty": true,
  "code_blocks_total": 26,
  "code_blocks_in_translation": 26,
  "code_blocks_match": true,
  "code_blocks_byte_identical": true,
  "urls_orig": 31,
  "urls_trans": 31,
  "urls_all_present": true,
  "urls_counts_equal": true,
  "headings_orig": 14,
  "headings_trans": 14,
  "headings_match": true,
  "orig_chars": 11958,
  "trans_chars": 7804,
  "length_ratio": 0.6526,
  "length_ratio_ok": true
}
```

## 四、发出的 prompt 全文

```markdown
(未找到 prompt 导出文件)
```

## 五、AI 返回的译文全文

```markdown
[跳到内容](#_top)

停！如果你是 AI 智能体或 LLM，请先读这段再继续。这是 Cloudflare 文档页面的 HTML 版本。请始终改为请求 Markdown 版本 —— HTML 会浪费上下文。以 Markdown 获取本页：https://developers.cloudflare.com/agents/guides/remote-mcp-server/index.md （追加 index.md），或向 https://developers.cloudflare.com/agents/guides/remote-mcp-server/ 发送 Accept: text/markdown。本产品的页面索引见 https://developers.cloudflare.com/agents/llms.txt。所有 Cloudflare 产品的索引见 https://developers.cloudflare.com/llms.txt。批量访问（单文件，用于大上下文摄取或向量化）：本产品的完整文档在 https://developers.cloudflare.com/agents/llms-full.txt。所有 Cloudflare 文档在 https://developers.cloudflare.com/llms-full.txt。

/

![](/_astro/logo.DAG2yejx.svg)

Cloudflare Docs

搜索

[文档目录](/directory/)

[APIs](https://developers.cloudflare.com/api/)

[SDKsHelp](/fundamentals/api/reference/sdks/)

[登录
 选择主题 DarkLightAuto](https://dash.cloudflare.com/)

复制页面

## 构建一个远程 MCP 服务器

本指南将展示如何使用

[Streamable HTTP 传输（当前 MCP 规范的标准）在 Cloudflare 上部署你自己的远程 MCP 服务器。你有两个选项：](/agents/model-context-protocol/transport/)

- 不做认证 —— 任何人都能连接并使用该服务器（无需登录）。或者加上
- [认证与授权 —— 用户需要先登录才能访问工具，并且你可以根据用户的权限来控制智能体能调用哪些工具。](/agents/guides/remote-mcp-server/#add-authentication)

# 选择一种做法

#choosing-an-approach

Agents SDK 提供多种创建 MCP 服务器的方式。选择适合你用例的做法：

| 做法 | 有状态？ | 需要 Durable Objects？ | 最适用于 |
| --- | --- | --- | --- |
| [createMcpHandler()](/agents/api-reference/mcp-handler-api/) | 否 | 否 | 无状态工具，配置最简单 |
| [McpAgent](/agents/api-reference/mcp-agent-api/) | 是 | 是 | 有状态工具、按会话的状态、elicitation |
| 原始 WebStandardStreamableHTTPServerTransport | 否 | 否 | 完全控制，不依赖 SDK |

- createMcpHandler() 是跑起一个无状态 MCP 服务器最快的方式。当你的工具不需要按会话维护状态时使用它。
- McpAgent 为每个会话提供一个 Durable Object，内置状态管理、elicitation 支持，以及 SSE 与 Streamable HTTP 两种传输。
- 原始传输让你在不想用 Agents SDK 辅助工具、而要直接使用 @modelcontextprotocol/sdk 时获得完全控制。

## 部署你的第一个 MCP 服务器

#deploy-your-first-mcp-server

你可以先部署一个

[公开的 MCP 服务器 —— 不做认证，之后再添加用户认证与带范围的授权。如果你已经知道自己的服务器需要认证，可以跳到](https://github.com/cloudflare/ai/tree/main/demos/remote-mcp-authless)

[下一节。](/agents/guides/remote-mcp-server/#add-authentication)

### 通过控制台

#via-the-dashboard

下面这个按钮会引导你完成部署一个

[示例 MCP 服务器 —— 到你的 Cloudflare 账号所需的全部操作：](https://github.com/cloudflare/ai/tree/main/demos/remote-mcp-authless)

https://deploy.workers.cloudflare.com/?url=https://github.com/cloudflare/ai/tree/main/demos/remote-mcp-authless

![Deploy to Workers](https://deploy.workers.cloudflare.com/button)

部署后，该服务器将在你的 workers.dev 子域上线（例如 remote-mcp-server-authless.your-account.workers.dev/mcp）。你可以立刻用

[AI Playground ——（一个远程 MCP 客户端）、](https://playground.ai.cloudflare.com/)

[MCP inspector —— 或](https://github.com/modelcontextprotocol/inspector)

[其他 MCP 客户端连接它。](/agents/guides/remote-mcp-server/#connect-from-an-mcp-client-via-a-local-proxy)

系统会在你的 GitHub 或 GitLab 账号上为这个 MCP 服务器建立一个新 git 仓库，并配置成每当你向仓库主分支推送改动或合并拉取请求时自动部署到 Cloudflare。你可以克隆这个仓库，

[在本地开发，并开始用你自己的](/agents/guides/remote-mcp-server/#via-the-cli)

[工具定制这个 MCP 服务器。](/agents/model-context-protocol/tools/)

### 通过 CLI

#via-the-cli

你可以使用

[Wrangler CLI 在本地机器上创建新的 MCP Server，并将其部署到 Cloudflare。](/workers/wrangler)

1. 打开终端并运行以下命令：

2. npm yarn pnpm

<!-- CODE_BLOCK_START id=c1 lang= -->
```
npm create cloudflare@latest -- remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless
```
<!-- CODE_BLOCK_END id=c1 -->

<!-- CODE_BLOCK_START id=c2 lang= -->
```
yarn create cloudflare remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless
```
<!-- CODE_BLOCK_END id=c2 -->

<!-- CODE_BLOCK_START id=c3 lang= -->
```
pnpm create cloudflare@latest remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless
```
<!-- CODE_BLOCK_END id=c3 -->

3. 在初始化过程中，选择以下选项： - 对于 Do you want to add an AGENTS.md file to help AI coding tools understand
Cloudflare APIs?，选择 No。 - 对于 Do you want to use git for version control?，选择 No。 - 对于 Do you want to deploy your application?，选择 No（我们会在部署前先测试这个服务器）。

4. 现在你的 MCP 服务器已经建好，依赖也安装完毕。

5. 进入项目文件夹：

*终端窗口*

<!-- CODE_BLOCK_START id=c4 lang= -->
```
cd remote-mcp-server-authless
```
<!-- CODE_BLOCK_END id=c4 -->

6. 在新项目所在的目录中，运行以下命令启动开发服务器：

*终端窗口*

<!-- CODE_BLOCK_START id=c5 lang= -->
```
npm start
```
<!-- CODE_BLOCK_END id=c5 -->

<!-- CODE_BLOCK_START id=c6 lang= -->
```
â Starting local server...[wrangler:info] Ready on http://localhost:8788
```
<!-- CODE_BLOCK_END id=c6 -->

7. 查看命令输出中的本地端口。在这个例子里，MCP 服务器运行在 8788 端口，MCP 端点 URL 是 http://localhost:8788/mcp。

8. 在本地测试该服务器：

  1. 在一个新终端里运行
  2. [MCP inspector ——。MCP inspector 是一个交互式 MCP 客户端，让你能从浏览器连接到 MCP 服务器并调用工具。](https://github.com/modelcontextprotocol/inspector)

*终端窗口*

<!-- CODE_BLOCK_START id=c7 lang= -->
```
npx @modelcontextprotocol/inspector@latest
```
<!-- CODE_BLOCK_END id=c7 -->

<!-- CODE_BLOCK_START id=c8 lang= -->
```
ð MCP Inspector is up and running at:  http://localhost:5173/?MCP_PROXY_AUTH_TOKEN=46ab..cd3
ð Opening browser...
```
<!-- CODE_BLOCK_END id=c8 -->

  3. MCP Inspector 会在你的浏览器中启动。你也可以手动打开浏览器并访问 http://localhost:<PORT> 来启动它。查看命令输出中 MCP Inspector 运行的本地端口。在这个例子里，MCP Inspector 服务在 5173 端口。

  4. 在 MCP inspector 里输入你 MCP 服务器的 URL（http://localhost:8788/mcp），然后选择 Connect。选择 List Tools 即可看到你的 MCP 服务器暴露的工具。

9. 现在你可以把 MCP 服务器部署到 Cloudflare。在项目目录中运行：

*终端窗口*

<!-- CODE_BLOCK_START id=c9 lang= -->
```
npx wrangler@latest deploy
```
<!-- CODE_BLOCK_END id=c9 -->

10. 如果你已经
11. [把 git 仓库连接到了承载你 MCP 服务器的 Worker，那么你可以通过向仓库主分支推送改动或合并拉取请求来部署 MCP 服务器。](/workers/ci-cd/builds/)

12. MCP 服务器将部署到你的 *.workers.dev 子域：https://remote-mcp-server-authless.your-account.workers.dev/mcp。

13. 要测试这个远程 MCP 服务器，请取你已部署 MCP 服务器的 URL（https://remote-mcp-server-authless.your-account.workers.dev/mcp），填入运行在 http://localhost:5173 的 MCP inspector。

现在你就有了一个 MCP 客户端可以连接的远程 MCP 服务器。

## 从 MCP 客户端经由本地代理连接

#connect-from-an-mcp-client-via-a-local-proxy

现在你的远程 MCP 服务器已经在运行，你可以用

[mcp-remote 本地代理 —— 把 Claude Desktop 或其他 MCP 客户端连接到它 —— 即使你的 MCP 客户端不支持远程传输或客户端侧授权也可以。这让你能用一个真实的 MCP 客户端来体验与远程 MCP 服务器交互是什么样。](https://www.npmjs.com/package/mcp-remote)

例如，从 Claude Desktop 连接：

1. 更新你的 Claude Desktop 配置，指向你 MCP 服务器的 URL：

<!-- CODE_BLOCK_START id=c10 lang= -->
```
{  "mcpServers": {    "math": {      "command": "npx",      "args": [        "mcp-remote",        "https://remote-mcp-server-authless.your-account.workers.dev/mcp"      ]    }  }}
```
<!-- CODE_BLOCK_END id=c10 -->

2. 重启 Claude Desktop 以加载该 MCP Server。完成后，Claude 就能调用你的远程 MCP 服务器了。

3. 要测试，可以让 Claude 使用你的某个工具。例如：

<!-- CODE_BLOCK_START id=c11 lang= -->
```
Could you use the math tool to add 23 and 19?
```
<!-- CODE_BLOCK_END id=c11 -->

4. Claude 应当会调用该工具，并显示远程 MCP 服务器生成的结果。

想了解如何在其他 MCP 客户端中使用远程 MCP 服务器，请参考

[测试远程 MCP 服务器。](/agents/guides/test-remote-mcp-server)

## 添加认证

#add-authentication

你之前部署的公开 MCP 服务器示例允许任何客户端无需登录即可连接并调用工具。要给你的 MCP 服务器添加用户认证，你可以接入 Cloudflare Access，或把第三方服务作为 OAuth 提供方。你的 MCP 服务器负责处理安全的登录流程，并签发访问令牌，供 MCP 客户端用来发起经过认证的工具调用。用户通过 OAuth 提供方登录，并授权其 AI 智能体以带范围的权限与你的 MCP 服务器暴露的工具交互。

### Cloudflare Access OAuth

#cloudflare-access-oauth

你可以把 MCP 服务器配置为要求通过 Cloudflare Access 做用户认证。Cloudflare Access 充当身份聚合器，验证用户邮箱、来自你现有

[身份提供方（如 GitHub 或 Google）的信号，以及其他属性如 IP 地址或设备证书。当用户连接 MCP 服务器时，他们会被提示登录所配置的身份提供方，并且只有通过你的](/cloudflare-one/integrations/identity-providers/)

[Access 策略才会被放行。](/cloudflare-one/access-controls/policies/#selectors)

分步部署指南请参考

[用 Access for SaaS 保护 MCP 服务器。](/cloudflare-one/access-controls/ai-controls/saas-mcp/)

### 第三方 OAuth

#third-party-oauth

你可以把 MCP 服务器与任何

[支持 OAuth 2.0 规范的 OAuth 提供方连接起来，包括 GitHub、Google、Slack、](/agents/model-context-protocol/authorization/#2-third-party-oauth-provider)

[Stytch、](/agents/model-context-protocol/authorization/#stytch)

[Auth0、](/agents/model-context-protocol/authorization/#auth0)

[WorkOS 等等。](/agents/model-context-protocol/authorization/#workos)

下面的示例演示如何用 GitHub 作为 OAuth 提供方。

#### 第 1 步 —— 创建一个新的 MCP 服务器

#step-1--create-a-new-mcp-server

运行以下命令，创建一个带 GitHub OAuth 的 MCP 服务器：

npm yarn pnpm

<!-- CODE_BLOCK_START id=c12 lang= -->
```
npm create cloudflare@latest -- my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth
```
<!-- CODE_BLOCK_END id=c12 -->

<!-- CODE_BLOCK_START id=c13 lang= -->
```
yarn create cloudflare my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth
```
<!-- CODE_BLOCK_END id=c13 -->

<!-- CODE_BLOCK_START id=c14 lang= -->
```
pnpm create cloudflare@latest my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth
```
<!-- CODE_BLOCK_END id=c14 -->

现在你的 MCP 服务器已经建好，依赖也安装完毕。进入那个项目文件夹：

*终端窗口*

<!-- CODE_BLOCK_START id=c15 lang= -->
```
cd my-mcp-server-github-auth
```
<!-- CODE_BLOCK_END id=c15 -->

你会注意到，在这个示例 MCP 服务器里，如果你打开 src/index.ts，主要区别在于 defaultHandler 被设置成了 GitHubHandler：

*TypeScript*

<!-- CODE_BLOCK_START id=c16 lang= -->
```
import GitHubHandler from "./github-handler";
export default new OAuthProvider({  apiRoute: "/mcp",  apiHandler: MyMCP.serve("/mcp"),  defaultHandler: GitHubHandler,  authorizeEndpoint: "/authorize",  tokenEndpoint: "/token",  clientRegistrationEndpoint: "/register",});
```
<!-- CODE_BLOCK_END id=c16 -->

这确保你的用户会被重定向到 GitHub 进行认证。不过要让它跑起来，你还需要按下面的步骤创建 OAuth 客户端应用。

#### 第 2 步 —— 创建一个 OAuth 应用

#step-2--create-an-oauth-app

你需要创建两个

[GitHub OAuth Apps —— 才能用 GitHub 作为你 MCP 服务器的认证提供方 —— 一个用于本地开发，一个用于生产。](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app)

#### 第 2.1 步 —— 为本地开发创建新的 OAuth 应用

#step-21--create-a-new-oauth-app-for-local-development

1. 前往
2. [github.com/settings/developers —— 创建一个新的 OAuth App，配置如下：](https://github.com/settings/developers)

  - Application name：My MCP Server (local)
  - Homepage URL：http://localhost:8788
  - Authorization callback URL：http://localhost:8788/callback

3. 对于你刚创建的 OAuth 应用，把该应用的 client ID 作为 GITHUB_CLIENT_ID 加入，并生成一个 client secret 作为 GITHUB_CLIENT_SECRET 加入项目根目录的 .env 文件，这个文件
4. [将用于在本地开发中设置密钥。](/workers/configuration/secrets/)

*终端窗口*

<!-- CODE_BLOCK_START id=c17 lang= -->
```
touch .envecho 'GITHUB_CLIENT_ID="your-client-id"' >> .envecho 'GITHUB_CLIENT_SECRET="your-client-secret"' >> .envcat .env
```
<!-- CODE_BLOCK_END id=c17 -->

5. 运行以下命令启动开发服务器：

*终端窗口*

<!-- CODE_BLOCK_START id=c18 lang= -->
```
npm start
```
<!-- CODE_BLOCK_END id=c18 -->

6. 你的 MCP 服务器现在运行在 http://localhost:8788/mcp。

7. 在一个新终端里运行
8. [MCP inspector ——。MCP inspector 是一个交互式 MCP 客户端，让你能从浏览器连接到 MCP 服务器并调用工具。](https://github.com/modelcontextprotocol/inspector)

*终端窗口*

<!-- CODE_BLOCK_START id=c19 lang= -->
```
npx @modelcontextprotocol/inspector@latest
```
<!-- CODE_BLOCK_END id=c19 -->

9. 在浏览器中打开 MCP inspector：

*终端窗口*

<!-- CODE_BLOCK_START id=c20 lang= -->
```
open http://localhost:5173
```
<!-- CODE_BLOCK_END id=c20 -->

10. 在 inspector 中，输入你 MCP 服务器的 URL：http://localhost:8788/mcp

11. 在右侧主面板中，点击 OAuth Settings 按钮，然后点击 Quick OAuth Flow。

12. 你应当会被重定向到 GitHub 登录或授权页面。在授权 MCP Client（即 inspector）访问你的 GitHub 账号后，你会被重定向回 inspector。

13. 点击侧边栏里的 Connect，你应该会看到 List Tools 按钮，点击它会列出你的 MCP 服务器暴露的工具。

#### 第 2.2 步 —— 为生产创建新的 OAuth 应用

#step-22--create-a-new-oauth-app-for-production

你需要重复

[第 2.1 步，为生产创建新的 OAuth App。](#step-21--create-a-new-oauth-app-for-local-development)

1. 前往
2. [github.com/settings/developers —— 创建一个新的 OAuth App，配置如下：](https://github.com/settings/developers)

- Application name：My MCP Server (production)
- Homepage URL：填入你已部署 MCP 服务器的 workers.dev URL（例：worker-name.account-name.workers.dev）
- Authorization callback URL：填入你已部署 MCP 服务器 workers.dev URL 的 /callback 路径（例：worker-name.account-name.workers.dev/callback）

1. 对于你刚创建的 OAuth 应用，用 Wrangler CLI 加入 client ID 与 client secret：

*终端窗口*

<!-- CODE_BLOCK_START id=c21 lang= -->
```
npx wrangler secret put GITHUB_CLIENT_ID
```
<!-- CODE_BLOCK_END id=c21 -->

*终端窗口*

<!-- CODE_BLOCK_START id=c22 lang= -->
```
npx wrangler secret put GITHUB_CLIENT_SECRET
```
<!-- CODE_BLOCK_END id=c22 -->

<!-- CODE_BLOCK_START id=c23 lang= -->
```
npx wrangler secret put COOKIE_ENCRYPTION_KEY # add any random string here e.g. openssl rand -hex 32
```
<!-- CODE_BLOCK_END id=c23 -->

1. 配置一个 KV 命名空间

2. a. 创建该 KV 命名空间：

*终端窗口*

<!-- CODE_BLOCK_START id=c24 lang= -->
```
npx wrangler kv namespace create "OAUTH_KV"
```
<!-- CODE_BLOCK_END id=c24 -->

3. b. 用生成的 KV ID 更新 wrangler.jsonc 文件：

<!-- CODE_BLOCK_START id=c25 lang= -->
```
{  "kvNamespaces": [    {      "binding": "OAUTH_KV",      "id": "<YOUR_KV_NAMESPACE_ID>"    }  ]}
```
<!-- CODE_BLOCK_END id=c25 -->

4. 把 MCP 服务器部署到你的 Cloudflare workers.dev 域：

*终端窗口*

<!-- CODE_BLOCK_START id=c26 lang= -->
```
npm run deploy
```
<!-- CODE_BLOCK_END id=c26 -->

5. 用 [AI Playground ——、MCP Inspector 或](https://playground.ai.cloudflare.com/) 连接到运行在 worker-name.account-name.workers.dev/mcp 的服务器
6. [其他 MCP 客户端，并用 GitHub 认证。](/agents/guides/test-remote-mcp-server/)

## 后续步骤

#next-steps

[MCP 工具：为你的 MCP 服务器添加工具。](/agents/model-context-protocol/tools/)

[授权：定制认证与授权。](/agents/model-context-protocol/authorization/)

```
