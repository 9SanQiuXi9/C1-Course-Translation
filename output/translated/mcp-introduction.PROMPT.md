# 翻译留痕：mcp-introduction

- doc_id：`mcp-introduction`
- 时间：2026-09-27T17:13:45+08:00
- 原文：`extracted/mcp-introduction.md`
- 译文：`translated/mcp-introduction.md`
- 原文 sha256：`d35196d545d9ee16ddb8f7247a859544306b1f2bbc9caf304f8b4576df73cb4d`
- 译文 sha256：`c0ef3138693823b7042ff04787e15f74aaf79aaf9f6224cd3a04be33aa0aae92`
- 术语约束条数：26

## 一、本文档涉及的术语清单

| 英文 | 译法 | handling | 出现次数 |
|---|---|---|---|
| `mcp` | MCP | `acronym` | 172 |
| `server` | 服务器 | `translate` | 43 |
| `model` | 模型 | `translate` | 40 |
| `tool` | 工具 | `translate` | 39 |
| `context` | 上下文 | `translate` | 27 |
| `client` | 客户端 | `translate` | 27 |
| `api` | API | `acronym` | 25 |
| `agent` | 智能体 | `translate` | 21 |
| `llm` | LLM | `acronym` | 15 |
| `debugging` | 调试 | `translate` | 8 |
| `prompt` | 提示词 | `translate` | 4 |
| `security` | 安全 | `translate` | 3 |
| `automation` | 自动化 | `translate` | 3 |
| `token` | token | `keep_en` | 3 |
| `tool use` | 工具调用 | `translate` | 3 |
| `agentic` | 智能体式 | `translate` | 2 |
| `ide` | IDE | `acronym` | 2 |
| `privacy` | 隐私 | `translate` | 2 |
| `codebase` | 代码库 | `translate` | 1 |
| `deployment` | 部署 | `translate` | 1 |
| `spec` | 规格 | `translate` | 1 |
| `prompt engineering` | 提示词工程 | `translate` | 1 |
| `machine learning` | 机器学习 | `translate` | 1 |
| `pipeline` | 流水线 | `translate` | 1 |
| `compliance` | 合规 | `translate` | 1 |
| `system prompt` | 系统提示词 | `translate` | 1 |

## 二、落盘校验结果

```json
{
  "non_empty": true,
  "code_blocks_total": 5,
  "code_blocks_in_translation": 5,
  "code_blocks_match": true,
  "code_blocks_byte_identical": true,
  "urls_orig": 23,
  "urls_trans": 23,
  "urls_all_present": true,
  "urls_counts_equal": true,
  "headings_orig": 39,
  "headings_trans": 39,
  "headings_match": true,
  "orig_chars": 28332,
  "trans_chars": 13149,
  "length_ratio": 0.4641,
  "length_ratio_ok": true
}
```

## 四、发出的 prompt 全文

```markdown
(未找到 prompt 导出文件)
```

## 五、AI 返回的译文全文

```markdown
/blog/

#### 返回博客

## Model Context Protocol（MCP）：面向开发者的综合导论

Auth & identity

Mar 28, 2025

作者：Reed McGinley-Stempel

![Model Context Protocol（MCP）：面向开发者的综合导论](https://cdn.sanity.io/images/3jwyzebk/production/e3f8d6ac0106744a859c305e903837fa0c68108c-877x621.png?auto=format&fit=max&w=1920&q=75)

# 执行摘要

Model Context Protocol（MCP）是一项开放标准，它把 AI 模型与外部数据和服务连接起来，让大型语言模型（LLM）能以一致、安全的方式发起结构化的 API 调用。本文将介绍 MCP、解释它为何对连接 AI 系统有价值、把它与 ChatGPT 插件和手工 API 集成等既有做法做比较，并深入探讨它近期对基于 OAuth 的认证的支持。我们还会看一点代码，看看 MCP 实际怎么用。

MCP 充当 AI 工具与外部服务之间的通用适配器，免去了为每个工具或 API 编写定制集成代码的需要。就像 USB-C 简化了各种设备之间的连接一样，MCP 为 AI 模型调用外部函数、获取数据或使用预定义提示词提供了一套统一方法。其核心是：MCP 提供一个接口，连接众多不同系统。

## 什么是 Model Context Protocol（MCP）？

MCP 本质上是 AI 应用与外部工具或数据源之间的通用适配器。它

[定义了一套通用协议（构建在 JSON-RPC 2.0 之上），让 AI 助手能以结构化方式调用外部服务的函数、获取数据或使用预定义提示词。不再需要每个 LLM 应用都为每个 API 或数据库写定制代码，](https://www.anthropic.com/news/model-context-protocol#:~:text=MCP%20addresses%20this%20challenge,to%20the%20data%20they%20need)

[MCP 为所有交互提供了一种标准化的「语言」。](https://medium.com/data-and-beyond/the-model-context-protocol-mcp-the-ultimate-guide-c40539e2a8e7#:~:text=https%3A%2F%2Fmodelcontextprotocol)

MCP 这一层让 AI 应用能够安全地访问外部数据源与工具并与之交互。它充当大型语言模型（LLM）与各种数据库、应用或 API 之间的桥梁，在无需大量定制编码的前提下促成无缝的集成与功能。

MCP 用客户端—服务器架构来实现这一点。AI 驱动的应用（例如聊天机器人、IDE 助手或智能体）充当宿主，运行一个 MCP 客户端组件，而每个外部集成则作为 MCP 服务器运行。服务器通过 MCP 协议暴露能力（如函数、数据资源或提示词模板），客户端连接它来使用这些能力。这种分离意味着 AI 模型并不直接与 API 对话；相反，它走过 MCP 客户端／服务器的握手，由该握手来组织这次交换。

![MCP 服务器连接](https://cdn.sanity.io/images/3jwyzebk/production/da5293781d0d860d74d785ac249597d9e39af044-1026x629.png?auto=format&fit=max&w=3840&q=75)

[来源](https://generativeai.pub/mcp-servers-explained-python-and-agentic-ai-tool-integration-aa2ddca6cbe5)

## MCP 为何有价值

在传统做法中，把 AI 模型连接到外部数据或动作既繁琐又临时。开发者往往不得不为想给模型用的每个 API 或数据库写一次性集成，还要分别处理各自不同的认证、数据格式与错误处理。MCP 通过标准化这些交互改变了局面。主要收益

[包括：](https://huggingface.co/blog/Kseniase/mcp#:~:text=,the%20client%20will%20pick%20on)

- 快速集成工具：有了 MCP，你可以接入新能力，而不必每个都从零定制编码。如果已经存在某个 MCP 服务器（比如给 Google Drive 或某个 SQL 数据库的），任何兼容 MCP 的 AI 应用都能连上它、立刻获得那项能力。这对自动化是巨大的胜利 —— AI 智能体只需加上相应的服务器，就能按需获取文档、查询数据库或调用 API。这就像拥有一个现成「插件」库，它们全都说同一种语言。MCP 服务器充当轻量程序，通过标准化协议暴露特定能力，作为 Cursor 与各种外部工具或数据源之间的中介。
- 自主智能体：MCP 让 AI 行为更加自主。智能体不再局限于内置知识；它们能在多步工作流中主动检索信息或执行动作。例如，一个精巧的智能体可能用 MCP 从 CRM 收集数据，再通过通讯工具发一封邮件，然后在数据库里记一条记录 —— 全在一条无缝的链上完成。通过促成流畅、具上下文感知的多步交互，MCP 帮助 AI 智能体更接近真正的自主任务执行。正如一位观察者所言，MCP 通过给 AI 标准化地访问真实世界工具与数据的能力，把它从一个孤立的「大脑」变成一个多才多艺的「行动者」。
- 减少摩擦与配置：因为 MCP 充当通用接口，开发者免去了维护各自独立集成的碎片化。一旦某个应用支持 MCP，它就能通过单一机制连接任意数量的服务。这极大减少了每次想让 AI 使用新 API 时的配置工作。团队可以专注于更高层的逻辑，而不必第十次重新发明连接代码。正如 Anthropic 所说，MCP 用一套更简单、更可靠的单一数据访问协议取代了碎片化的集成。一致性与互操作性：MCP 在各工具之间强制统一的请求／响应格式。这意味着你的 AI 应用不必为服务 A 处理一种 HTTP 响应、为服务 B 处理另一种 XML，等等。模型的输出（函数调用）与工具结果全部以
- [统一的 JSON 结构传递。这种一致性让调试与扩展都更容易。它也让你集成逻辑更具前瞻性 —— 即使你更换底层的模型供应商，MCP 与工具之间的接口保持不变。](https://dev.to/fotiecodes/function-calling-vs-model-context-protocol-mcp-what-you-need-to-know-4nbo#:~:text=Purpose%20Converts%20user%20prompts%20into,Ensures%20interoperability%20across%20multiple%20tools)
- 双向上下文：与简单的 API 调用不同，MCP 支持在模型与工具之间维持上下文与持续对话。除工具之外，MCP 服务器还能提供 Prompts（针对某些任务的预定义提示词模板）与 Resources（如文档这类数据上下文）。这意味着 AI 不仅能「调用 API」，还能摄取参考数据，或遵循服务器引导的复杂工作流。该协议在设计上支持丰富的交互，而不只是一次性查询。这在编码助手（AI 可能通过 MCP 与开发环境反复迭代）或需要与多种数据源来回交互的复杂决策任务这类应用中尤其有用。

简言之，MCP 为增强 LLM 带来了一种可扩展、即插即用的做法。它让 AI 系统能安全地接入所需的「活」数据与动作，而不必让每位开发者都重新发明轮子。MCP 的早期采用者已经为 Google Drive、Slack、GitHub、数据库等工具构建了服务器 —— 展示了 AI 智能体如何用 MCP 处理企业内容仓库、DevOps 工具以及其他真实世界系统。

## MCP 架构 —— 一眼看懂它如何工作

### 客户端—服务器结构

MCP 遵循清晰的客户端—服务器架构：

- MCP 客户端：内嵌在 AI 应用（聊天机器人、IDE 助手、自动化智能体）中。
- MCP 服务器：暴露外部能力，如函数（工具）、资源（数据）与提示词（模板）。

所有交互都通过标准化的 JSON-RPC 消息进行，维持安全、结构化的交换：

JSON-RPC 请求示例：

例如，要列出可用工具，MCP 客户端会发送这样的请求：

<!-- CODE_BLOCK_START id=c1 lang= -->
```
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```
<!-- CODE_BLOCK_END id=c1 -->

服务器则回复一个结构化的 JSON，列出各工具（每个带名称、描述与输入 schema）。例如，某个服务器可能对外声明一个 `get_weather` 工具，并描述它需要什么输入。

<!-- CODE_BLOCK_START id=c2 lang= -->
```
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": [
    { "name": "get_weather", "description": "Retrieves weather data.", "schema": { "location": "string" } }
  ]
}
```
<!-- CODE_BLOCK_END id=c2 -->

之后，当 LLM 决定使用某个工具时，客户端就发起一次调用来完成它。MCP 服务器执行该函数，并以结构化 JSON 响应返回结果。MCP 客户端（位于宿主应用内）随后可以把该结果回填进模型的上下文或响应。实践中，宿主应用主导这个过程：它把 LLM 的意图（通常通过模型的函数调用输出）翻译成一次 MCP 请求，再把服务器返回的结构化结果传回 LLM。这种双向交换既安全又受控 —— 模型只能调用服务器暴露的特定工具，所有进出的数据都走既定的协议。

## 构建与部署 MCP 服务器

构建与部署 MCP 服务器，是利用 Model Context Protocol（MCP）做 AI 集成的关键一步。MCP 服务器充当 AI 模型与外部数据源或工具之间的中介，促成无缝的通信与数据交换。MCP 最突出的特性之一是它在服务器开发上的灵活性。开发者可以使用任何能向 stdout 打印、或提供 HTTP 端点的编程语言，从而自由选择自己偏好的语言与技术栈。

构建 MCP 服务器时，考虑架构与设计至关重要。MCP 遵循客户端—服务器架构，一个宿主应用可以连接多个服务器。这种架构带来可扩展性与灵活性，让开发者能设计出处理各种任务与功能的 MCP 服务器，例如数据处理、工具集成或 AI 模型管理。

MCP 服务器的部署可以在多种环境中进行，包括本地开发环境、云平台或本地机房基础设施。例如，Cloudflare 提供了一个健壮的平台来构建并部署远程 MCP 服务器，让 MCP 的部署更容易管理与扩展。这种灵活性确保 MCP 服务器能针对不同应用与环境的特定需求做定制，无论是用于开发的本地配置，还是用于生产的云端方案。

通过专注于良好的架构设计并善用 MCP 的灵活性，开发者可以创建强大且可扩展的 MCP 服务器，增强 AI 模型的能力，让它们能与外部数据源及工具无缝交互。

## MCP 客户端与工具

MCP 客户端与工具是 Model Context Protocol 生态中不可或缺的组成部分。MCP 客户端是连接 MCP 服务器以访问外部数据源或工具的应用。这些客户端可以用各种编程语言与框架构建，例如 Python、JavaScript 或 Java，让开发者能灵活选择最适合自身需求的工具。

而 MCP 工具则是为 MCP 客户端提供特定能力或功能的软件组件。这些工具可以集成进 MCP 服务器，以实现数据处理、AI 模型管理或工具集成等功能。MCP 工具的例子包括 Claude Desktop（提供与 AI 模型交互的聊天界面）与 Cursor（提供扩展 AI 能力的插件系统）。

开发者可以构建自定义的 MCP 客户端与工具来满足特定用例或需求。这种灵活性让 MCP 生态中得以创新与试验，使开发者能创造出新颖而令人兴奋的应用。无论是用于数据分析的专用工具，还是能集成多个 MCP 服务器的客户端应用，可能性都非常广阔。

通过善用 MCP 客户端与工具，开发者可以创建健壮而多才多艺的应用，充分发挥 AI 模型的潜力，让它们能与广泛的外部数据源及工具无缝交互。

## 把 MCP 与其他做法做比较

#### MCP

#### 定制集成

#### ChatGPT 插件

#### LangChain 及各类框架

#### 集成速度

#### 集成速度

✅ 快，即插即用

❌ 慢，需定制代码

⚠️ 中等，专有

⚠️ 中等，需定制代码

#### 认证

#### 认证

✅ OAuth 标准

❌ 手工管理 API key

⚠️ 插件专属 OAuth

❌ 因实现而异

#### 交互类型

#### 交互类型

✅ 持续且上下文丰富

❌ 临时性交互

❌ 单次交互

⚠️ 上下文受限

#### 开放标准

#### 开放标准

✅ 是

❌ 否

❌ 否

⚠️ 依框架而定

我们来比较几种在 MCP 之前或与之并存的做法：

- 定制集成与 API key 管理：最常见的传统做法是为每个服务写定制代码，并把凭据（API key 或 token）交给 LLM 来使用这些集成。例如，你可能写一个 Python 函数去查询某个 API，给 LLM 调用该函数的能力，并在后端手工处理 API key。这种做法劳动密集且不可扩展 —— 每个新数据源都需要新代码，每个环境都必须安全地管理 API key。它往往导致系统脆弱，因为每个集成都是独特的。相比之下，MCP 把这些交互集中化、标准化：AI 智能体只需处理 MCP 协议，任何（面向任何服务的）MCP 服务器都能即插即用地工作。新增服务器完全不需要改动客户端代码。此外，MCP 为认证提供了正式结构（后文讨论），因此把 API key 交给 AI 不再是临时为之，而是通过安全协议完成。
- ChatGPT 插件（OpenAI Plugins）：2023 年，OpenAI 为 ChatGPT 引入了一套插件系统，允许模型调用由 OpenAPI 规格定义的外部 API。这是迈向标准化工具使用的早期一步，但有局限。每个插件本质上是它自己的迷你集成（有自己的 API schema 与认证），需要单独构建／托管。只有特定平台（如 ChatGPT 或 Bing Chat）能用这些插件，因为这是专有做法。插件大多也是一次性调用 —— 模型调用一个 API 拿到信息，没有持久连接或持续交换。MCP 的不同在于它是开放的、通用的（不绑定某个供应商或界面），并支持丰富的双向交互与持续上下文。把 ChatGPT 插件想成封闭工具箱里的专用工具，而 MCP 是一套任何开发者或 AI 平台都能使用的开放标准工具集。MCP 标准化的认证（尤其是 OAuth）也意味着，相比 ChatGPT 系统里逐个插件各自为政的 OAuth 流程，它能以更统一的方式处理对用户数据的安全访问。总而言之，ChatGPT 插件展示了为 LLM 标准化 API 访问的价值，而 MCP 更进一步，把它做成开放协议，并促成了 AI 与服务之间持久的「对话」。
- LLM 工具框架（LangChain、各类智能体库）：在 MCP 之前，许多开发者用 LangChain 这类框架给模型提供工具。在这些配置中，你定义一组工具函数（带描述）以及智能体的提示逻辑，让 LLM 能决定使用它们。这样做可行，但每个工具在幕后仍然需要定制实现 —— LangChain 最终在其库中维护了数百个工具集成。本质上，LangChain 提供了面向开发者的标准（一个 Python 类接口）来把工具集成进智能体的代码库，但对模型在运行时动态发现新工具则毫无帮助。MCP 与这些框架是互补的，它把标准化转向面向模型。有了 MCP，智能体可以发现并使用任何 MCP 服务器提供的工具，即使智能体的代码事先并没有明确包含那个工具。事实上，LangChain 已经加入了支持，可以把 MCP 服务器当作又一种工具来源 —— 这意味着用 LangChain 构建的智能体能轻松调用 MCP 工具，借助不断壮大的 MCP 服务器生态。区别在于 MCP 把接口正式化为一种协议（JSON-RPC，带元数据等），使其更容易接入不同环境，而不只是 Python 框架。类似地，OpenAI 原生的函数调用能力可以看作处理函数调用的格式（模型输出一个 JSON 函数调用），而 MCP 以标准化方式处理该调用的执行。OpenAI 的函数调用与 MCP 常常配合使用：LLM 产出结构化的调用，MCP 客户端／服务器执行它并返回结果，两者合起来实现了无缝的工具使用。

本质上，MCP 并不是把 LLM 与外部 API 连接起来的第一次尝试 —— 但它从那些过往做法（插件、工具库等）中学习，并把方案统一起来。它提供了一套开放、与模型无关的协议，简化了集成与认证。尤其在安全与认证方面，MCP 的设计（支持 OAuth）避免了逐个插件配 key、或把原始 API key 交给模型的这种拼凑做法。相反，认证可以作为协议的一部分，以一致、标准化的流程来处理 —— 这相对现状是重大进步。

## MCP 实战：技术深入

我们一步步走一遍典型的 MCP 交互来巩固对它的理解，并看一点代码。设想我们有一个 AI 助手，它想使用一个提供一组工具的 MCP 服务器（比如说，为某个假设的「Neon」数据库服务）。高层流程是：

1. 连接到 MCP 服务器 —— 宿主应用（AI 助手）初始化一个 MCP 客户端，并与服务器建立连接。视服务器所在位置而定，这可以通过本地进程（stdio）或远程 HTTP 流（SSE）实现。在底层，客户端发送一条 initialize
[消息来握手协议版本与能力。](https://nshipster.com/model-context-protocol/#:~:text=Like%20LSP%2C%20MCP%20has%20clients,The%20server%20responds%20in%20kind)

2. 发现可用的工具／资源 —— 客户端随后查询服务器提供什么。如前面所示，它可能发送 `{"method": "tools/list"}` 并拿回一份工具定义清单。助手可以用它来告知 LLM（例如把工具清单放进 system prompt，或通过模型的函数 schema，视实现而定）。例如，使用某个 SDK 时，这可能只是一行代码：

<!-- CODE_BLOCK_START id=c3 lang=javascript -->
```javascript
const tools = await mcpClient.request({ method: 'tools/list' }, ListToolsResultSchema);
```
<!-- CODE_BLOCK_END id=c3 -->

它返回一份结构化的工具清单。每个工具条目都有名称、描述与输入的 JSON schema，

[这样 AI 就知道自己能做什么。](https://neon.tech/blog/building-a-cli-client-for-model-context-protocol-servers#:~:text=,can%20use%20during%20our%20interaction)

3. LLM 选择一个工具 —— 当用户向 AI 提出需要外部动作的问题时，LLM（通常通过提示词工程或函数调用能力）判定应当使用某个工具。例如，用户问：「AAPL 股票的最新价格是多少？」LLM 看出它应当调用 `get_current_stock_price(company="AAPL", format="USD")`。宿主应用捕获这个意图（例如 OpenAI 的函数调用 API 会以 JSON 返回函数名与参数）。

4. 经由 MCP 调用该工具 —— 客户端现在向服务器发送一次 `tools/call` 请求，带上所选工具名与参数。前面我们看过这样的 JSON 示例。在代码中，使用 SDK 可能长这样：

<!-- CODE_BLOCK_START id=c4 lang=javascript -->
```javascript
const result = await mcpClient.request({
    method: 'tools/call',
    params: { name: toolName, arguments: toolArgs }
}, CallToolResultSchema);
```
<!-- CODE_BLOCK_END id=c4 -->

这会让服务器在它那一侧执行该工具的处理函数。服务器可能在调用外部 API、执行数据库查询，或做那个工具封装的任何逻辑。结果（可能是简单值或复杂 JSON 对象）会在 MCP 响应的 result 字段中送回。

5. 把结果返回给 LLM —— MCP 客户端收到工具的输出。现在宿主应用可以把它整合回 AI 的响应。在许多智能体配置中，做法是把结果注入对话，然后让模型继续。例如，助手随后可能呈现：「AAPL 当前的股票价格是 173.22 美元（USD）。」如果使用自动循环，结果可以交给模型（也许作为一条系统消息追加到对话里，如「get_current_stock_price 的结果：……」），模型就能带着这个信息继续回答用户的提问。

下面是一个使用 Anthropic 的 Claude（原生支持工具使用）在对话中调用工具并使用结果的简化示意：

<!-- CODE_BLOCK_START id=c5 lang=javascript -->
```javascript
// 1. Send user prompt to LLM with available tools context
const response = await anthropicClient.complete({
  prompt: "User: Can you list my projects?\nAssistant: ",
  model: "claude-3.5",
  tools: tools // list of tools from MCP server
});
for (const msg of response.messages) {
  if (msg.type === 'tool_use') {
    // 2. LLM decided to use a tool
    const { name, args } = msg;
    // 3. Call the tool via MCP
    const toolRes = await mcpClient.request({ method: 'tools/call', params: { name, arguments: args } });
    // 4. Inject tool result and resume LLM
    await anthropicClient.send({ role: 'system', content: `Tool result: ${toolRes.result}` });
  } else {
    // 5. Handle normal LLM reply (tool result likely integrated)
    console.log("Assistant:", msg.content);
  }
}
```
<!-- CODE_BLOCK_END id=c5 -->

现实中，框架会替你处理其中大量工作，但以上伪代码勾勒了 MCP 如何嵌入这个循环。关键在于 MCP 提供了标准化的调用／响应层来执行工具，AI 智能体代码可以挂接其上。无论你用的是 OpenAI、Anthropic 还是别的 LLM，MCP 都保持不变 —— 它是模型意图与外部动作之间的胶水。

通过使用 MCP，开发者获得了一条清晰、结构化的管道来扩展 AI 能力。代码变得更容易维护（因为你在各处调用的是通用的 `mcpClient.request`，而不是每个地方都写服务专属代码），AI 也变得更强（因为它能接入任何 MCP 连接的服务）。调试也更容易 —— 你可以监控 JSON-RPC 消息，确切看到请求了什么、返回了什么，而不必从模型生成的文本里去找线索。

## 早期的局限（没有内置认证）

MCP 刚出现时（2024 年末），它提供了工具与数据交换的核心协议，但缺少用于连接远程服务器的标准化认证机制。实践中，早期的 MCP 演示与实现往往要求把 MCP 服务器跑在本地或可信环境中，那里认证不是大问题（因为 AI 与服务器跑在同一台机器上）。例如，开发者可以在自己的

[localhost 上跑一个带预获取 token 的 Google Drive MCP 服务器，然后让 AI 应用指向它。但在互联网上、或与第三方服务一起使用 MCP 时，没有正式的认证流程就很棘手。](http://localhost)

许多早期 MCP 服务器假定用户会在启动时手工向服务器提供凭据或 API key。举个例子，Anthropic 的快速上手建议通过配置或命令行提供你自己的凭据（API key、token）来运行现成的服务器。这意味着服务器本身能拿到你的 key，而 MCP 客户端只是信任那个服务器。这对个人或单用户场景可行，但对多用户应用或云端托管的智能体就不太能扩展。当时没有标准握手让 AI 智能体说：「嘿，我获准代表用户 X 访问这个服务；这是我的凭据。」

本质上，早期 MCP 客户端除了带外方式（例如预先共享一个 token，或干脆不认证运行）之外，没有办法向 MCP 服务器认证。这是一个明显的局限 —— MCP 的设计初衷是开放、基于互联网的，但没有认证标准，安全的远程使用就被束缚住了。

缺少认证标准意味着 MCP 客户端无法安全地自行连接任意服务器。你要么把 client ID／API key 硬编码进客户端（这在分布式应用中并不理想），要么只能不认证运行、并假定只有授权用户才能访问到服务器（往往靠把它留在本地）。显然，要让 MCP 发挥全部潜力（例如以安全方式把 AI 智能体连接到云端托管的数据源），需要更好的做法。好消息是社区认识到了这一点，并着手把基于 OAuth 的认证烤进 MCP。

### OAuth 2.0 认证流程

为解决最初的认证局限并增强安全连接能力，MCP 采纳了 OAuth 2.0 —— 一个被广泛认可、健壮的认证标准。OAuth 2.0 提供了安全、可扩展的框架，让 MCP 客户端能安全地与远程服务器、云端托管资源和多用户环境交互。把 OAuth 2.0 集成进 MCP 的关键组件与收益包括：

1. 动态客户端注册（DCR）：Model Context Protocol 支持动态客户端注册，让客户端能自动向 OAuth 服务器注册。这免去了手工配置客户端或硬编码凭据的需要，显著简化了开发者的部署工作。
2. 自动端点发现：MCP 利用标准化的元数据 URL（遵循 OAuth 的发现协议）让客户端自动发现 OAuth 端点。这降低了配置开销，让 MCP 部署更容易、更灵活。
3. 安全的授权与令牌管理：客户端安全地获取精确对应用户权限与访问范围的 OAuth token。这确保客户端只访问用户明确许可的资源，提升了安全性与合规性，在多用户与云环境中尤其如此。
4. 可扩展、安全的多用户支持：OAuth 2.0 的设计本身支持多个并发用户与服务，解决了 MCP 早期最显著的局限之一。应用现在能同时无缝处理众多用户的授权流程，这对云的广泛采用至关重要。

## 调试与故障排查

调试与故障排查是使用 MCP 服务器与客户端时的关键方面。MCP 提供了各种调试与排查工具及技术，确保开发者能高效定位并解决问题。这一过程中的关键工具之一是 MCP Inspector，一个面向 MCP 服务器的交互式调试工具。

MCP Inspector 让开发者能测试并检视 MCP 服务器，定位并解决 MCP 服务器集成中的问题。这个工具提供 MCP 客户端与服务器之间交互的详细视图，让定位问题和理解根本原因更容易。此外，MCP 还提供了一份详尽的调试指南，列出常见问题与解决方案，帮助开发者快速排查并解决问题。

调试 MCP 服务器时，考虑系统的架构与设计至关重要。开发者应当识别出引发问题的具体组件或模块，并使用 MCP Inspector 这类工具来诊断与解决问题。通过专注于系统化的调试方法并善用可用工具，开发者可以确保自己的 MCP 集成健壮可靠。

## MCP 的真实世界应用

Model Context Protocol（MCP）在各行各业与各领域有各种真实世界应用。MCP 的主要用例之一是在 AI 集成中，MCP 让 AI 模型与外部数据源或工具之间实现无缝的通信与数据交换。

MCP 可用于各种应用，例如：

- 构建 AI 驱动的聊天机器人：这些聊天机器人可以访问外部数据源或工具，为用户提供准确、最新的信息。
- 创建 AI 驱动的工作流：MCP 让 AI 模型能与外部系统或数据源集成，自动化复杂工作流并提升效率。
- 开发 AI 模型：这些模型能与外部工具或数据源交互，增强自身能力并提供更准确、更相关的输出。
- 实现 AI 驱动的自动化：在金融、医疗或制造等行业，MCP 可以自动化任务与流程，提升生产力并减少错误。

MCP 的灵活性与适应性，使它成为希望在自己的应用中利用 AI 与机器学习的开发者与组织的一个有吸引力的方案。通过为 AI 模型提供与数据源及工具交互的标准化接口，MCP 让 AI 生态中的创新与试验成为可能。这种标准化做法不仅简化了集成过程，也确保 AI 模型能访问它们发挥最佳水平所需的数据与工具。

总而言之，MCP 为 AI 应用打开了一个充满可能性的世界，让开发者能创造出更集成、更自主、更可扩展的方案。无论是用 AI 驱动的聊天机器人改善客户服务，还是在工业场景中自动化复杂工作流，MCP 都提供了把这些创新变为现实所需的工具与框架。

## 结论

Model Context Protocol（MCP）是 AI 开发中一个令人兴奋的进展，因为它让开发者能安全、高效地把我们日益智能的语言模型，连接到此前难以连接的广阔软件与数据世界。通过引入一套通用协议，MCP 让我们能构建更集成、更自主、更容易扩展的 AI 系统。不必为每个新工具写一次性插件、或给模型脆弱的指令，我们有了一个连贯的框架，让 AI 智能体能即时发现并使用工具，同时保有恰当的监督与安全。

虽然该协议仍在演进（认证是近期才加入的，标准化服务器发现等功能也已在望），但很明显，MCP 或类似的东西将在下一代 AI 应用中扮演关键角色。对开发者而言，现在是熟悉 MCP 概念的好时机。无论你是在用公司专属知识增强聊天机器人，还是构建自动化工作流的 AI 智能体，MCP 都能通过处理工具集成的「管道」工作，为你省下时间与烦恼。而由于它是一项有不断壮大的社区（以及 Anthropic 这类公司）支持的开放标准，它很可能成为未来 AI 基础设施的一块基石。

总而言之，Model Context Protocol 开启了一个这样的世界：AI 助手不再是孤立的天才，而是装备精良的工程师与助手 —— 能与众多系统对接、遵循流程、按需获取或创建信息，全部通过一个统一、安全的界面。这是一个强大的愿景，而有了 MCP，它正迅速变为现实。

在 Stytch，我们专注于为客户端轻松

[解决远程 MCP 服务器的认证问题，让他们能轻松为自己的应用搭起 MCP 服务器，使终端用户可以向 MCP 客户端提供经过授权的访问。](https://stytch.com/docs/guides/connected-apps/mcp-servers)

### 用 Stytch 做 MCP 认证

使用 Stytch Connected Apps 构建与 MCP 服务器的认证

[阅读文档](https://stytch.com/docs/guides/connected-apps/mcp-servers)

分享本文

https://www.linkedin.com/shareArticle?mini=true&url=https%3A%2F%2Fstytch.com%2Fblog%2Fmodel-context-protocol-introduction%2F

LinkedIn

https://x.com/intent/post?url=https%3A%2F%2Fstytch.com%2Fblog%2Fmodel-context-protocol-introduction%2F

X

https://www.facebook.com/sharer.php?u=https%3A%2F%2Fstytch.com%2Fblog%2Fmodel-context-protocol-introduction%2F

Facebook

## 相关文章

/blog/stytch-connected-apps/

![Stytch Connected Apps：把任何应用变成面向集成与 AI 智能体的 OAuth 提供方](https://cdn.sanity.io/images/3jwyzebk/production/e508e790c2042da91864ad821bfa2e329b91d4fe-1150x884.png?auto=format&fit=max&w=3840&q=75)

/blog/stytch-connected-apps/

产品

Feb 20, 2025

### Stytch Connected Apps：把任何应用变成面向集成与 AI 智能体的 OAuth 提供方

/blog/the-age-of-agent-experience/

![智能体体验的时代](https://cdn.sanity.io/images/3jwyzebk/production/debae5121d138d6b3358e3289e070b223092689e-1584x988.png?auto=format&fit=max&w=3840&q=75)

/blog/the-age-of-agent-experience/

Auth & identity

Feb 8, 2025

### 智能体体验的时代

/blog/detecting-ai-agent-use-abuse/

![检测 AI 智能体的使用与滥用](https://cdn.sanity.io/images/3jwyzebk/production/4124b124a6f5ddebe133043163ce820536175e97-1088x902.png?auto=format&fit=max&w=3840&q=75)

/blog/detecting-ai-agent-use-abuse/

Auth & identity

Feb 15, 2025

### 检测 AI 智能体的使用与滥用

开始使用
 Stytch

[免费开始构建](/start-now)

[浏览我们的文档](/docs)

/

#### 认证与授权

/b2c

面向消费者应用

/b2b

面向 B2B SaaS 应用

/admin-portal

Admin Portal

/connected-apps

Connected Apps

/lp/sso

单点登录

#### 欺诈与风险防范

/fraud

设备指纹

/docs/fraud/guides/device-fingerprinting/verdicts

主动风险评估

/docs/fraud/guides/device-fingerprinting/traffic-shaping/intelligent-rate-limiting

细粒度管控

#### 为什么选 Stytch

/stytch-vs-auth0

Stytch vs. Auth0

/stytch-vs-firebase

Stytch vs. Firebase

/stytch-vs-cognito

Stytch vs. Cognito

/stytch-vs-fingerprint

Stytch vs. Fingerprint

#### 公司

/about

关于我们

/careers

招聘

/contact

联系我们

#### 资源

/pricing

定价

/docs

文档

https://changelog.stytch.com/

更新日志

https://stytch.productlane.com/roadmap

产品路线图

https://status.stytch.com/

API 状态

/blog

博客

#### 社区

https://stytch.slack.com/join/shared_invite/zt-3aqo03e10-afWXyLzRIAlzGWJyF_~zHw

Slack 社区

https://forum.stytch.com/

技术支持

/customer-stories

客户案例

© 2020-2026 Stytch. 保留所有权利。

/legal/terms-of-service

使用条款

/legal/privacy-policy

隐私政策

```
