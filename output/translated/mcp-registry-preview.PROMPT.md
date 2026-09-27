# 翻译留痕：mcp-registry-preview

- doc_id：`mcp-registry-preview`
- 时间：2026-09-27T16:37:37+08:00
- 原文：`extracted/mcp-registry-preview.md`
- 译文：`translated/mcp-registry-preview.md`
- 原文 sha256：`a168a1c8c665b8d1d071a0ccc245b1c620bc230aaa7abbed22524b966bfaea7e`
- 译文 sha256：`c9fc96045d8b6a6eed7874759a4239f8c7e7ccd017e52bd84c50d20f569cf5cd`
- 术语约束条数：9

## 一、本文档涉及的术语清单

| 英文 | 译法 | handling | 出现次数 |
|---|---|---|---|
| `mcp` | MCP | `acronym` | 39 |
| `server` | 服务器 | `translate` | 8 |
| `api` | API | `acronym` | 4 |
| `client` | 客户端 | `translate` | 4 |
| `context` | 上下文 | `translate` | 2 |
| `model` | 模型 | `translate` | 1 |
| `security` | 安全 | `translate` | 1 |
| `repository` | 仓库 | `translate` | 1 |
| `privacy` | 隐私 | `translate` | 1 |

## 二、落盘校验结果

```json
{
  "non_empty": true,
  "code_blocks_total": 0,
  "code_blocks_in_translation": 0,
  "code_blocks_match": true,
  "code_blocks_byte_identical": true,
  "urls_orig": 38,
  "urls_trans": 38,
  "urls_all_present": true,
  "urls_counts_equal": true,
  "headings_orig": 5,
  "headings_trans": 5,
  "headings_match": true,
  "orig_chars": 6511,
  "trans_chars": 4047,
  "length_ratio": 0.6216,
  "length_ratio_ok": true
}
```

## 四、发出的 prompt 全文

```markdown
# 翻译任务：mcp-registry-preview

## 一、文档元数据

- doc_id：`mcp-registry-preview`
- title：[#](#single-source-of-truth-for-mcp-servers)
- origin_url：https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/
- 本段字符数：7,382

## 二、术语约束（本文档用到的，必须严格遵守）

| 英文 | 处理方式 | 出现次数 |
|---|---|---|
| `mcp` | 保留英文缩写（首次出现给全称） | 39 |
| `server` | 翻译为「服务器」 | 8 |
| `api` | 保留英文缩写（首次出现给全称） | 4 |
| `client` | 翻译为「客户端」 | 4 |
| `context` | 翻译为「上下文」 | 2 |
| `model` | 翻译为「模型」 | 1 |
| `security` | 翻译为「安全」 | 1 |
| `repository` | 翻译为「仓库」 | 1 |
| `privacy` | 翻译为「隐私」 | 1 |

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


[Skip to content](#main-content)

Today, we’re launching the Model Context Protocol (MCP) Registry—an open catalog and API for publicly available MCP servers to improve discoverability and implementation. By standardizing how servers are distributed and discovered, we’re expanding their reach while making it easier for clients to get connected.

The MCP Registry is now available in preview. To get started:

- Add your server by following our guide on
- [Adding Servers to the MCP Registry (for server maintainers)](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/quickstart.mdx) Access server data by following our guide on
- [Accessing MCP Registry Data (for client maintainers)](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/registry-aggregators.mdx)

Single source of truth for MCP servers

# [#](#single-source-of-truth-for-mcp-servers)

In March 2025, we shared that we wanted to build a central registry for the MCP ecosystem. Today we are announcing that we’ve launched

[https://registry.modelcontextprotocol.io as the official MCP Registry. As part of the MCP project, the MCP Registry, as well as a parent](https://registry.modelcontextprotocol.io)

[OpenAPI specification, are open source—allowing everyone to build a compatible sub-registry.](https://github.com/modelcontextprotocol/registry/blob/main/docs/reference/api/official-registry-api.md)

Our goal is to standardize how servers are distributed and discovered, providing a primary source of truth that sub-registries can build upon. In turn, this will expand server reach and help clients find servers more easily across the MCP ecosystem.

Public and private sub-registries

### [#](#public-and-private-sub-registries)

In building a central registry, it was important to us not to take away from existing registries that the community and companies have built. The MCP Registry serves as a primary source of truth for publicly available MCP servers, and organizations can choose to

[create sub-registries based on custom criteria. For example:](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/registry-aggregators.mdx)

Public subregistries like opinionated “MCP marketplaces” associated with each MCP client are free to augment and enhance data they ingest from the upstream MCP Registry. Every MCP end-user persona will have different needs, and it is up to the MCP client marketplaces to properly serve their end-users in opinionated ways.

Private subregistries will exist within enterprises that have strict privacy and security requirements, but the MCP Registry gives these enterprises a single upstream data source they can build upon. At a minimum, we aim to share API schemas with these private implementations so that associated SDKs and tooling can be shared across the ecosystem.

In both cases, the MCP Registry is the starting point – it’s the centralized location where MCP server maintainers publish and maintain their self-reported information for these downstream consumers to massage and deliver to their end-users.

Community-driven mechanism for moderation

### [#](#community-driven-mechanism-for-moderation)

The MCP Registry is an official MCP project maintained by the registry working group and permissively licensed. Community members can submit issues to flag servers that violate the MCP

[moderation guidelines—such as those containing spam, malicious code, or impersonating legitimate services. Registry maintainers can then denylist these entries and retroactively remove them from public access.](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/moderation-policy.mdx)

Getting started

## [#](#getting-started)

To get started:

- Add your server by following our guide on
- [Adding Servers to the MCP Registry (for server maintainers)](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/quickstart.mdx) Access server data by following our guide on
- [Accessing MCP Registry Data (for client maintainers)](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/registry-aggregators.mdx)

This preview of the MCP Registry is meant to help us improve the user experience before general availability and does not provide data durability guarantees or other warranties. We advise MCP adopters to watch development closely as breaking changes may occur before the registry is made generally available.

As we continue to develop the registry, we encourage feedback and contributions on the

[modelcontextprotocol/registry GitHub repository: Discussion, Issues, and Pull Requests are all welcome.](https://github.com/modelcontextprotocol/registry)

Thanks to the MCP community

## [#](#thanks-to-the-mcp-community)

The MCP Registry has been a collaborative effort from the beginning and we are incredibly grateful for the enthusiasm and support from the broader developer community.

In February 2025, it began as a grassroots project when MCP creators

[David Soria Parra and](https://github.com/dsp-ant)

[Justin Spahr-Summers asked the](https://github.com/jspahrsummers)

[PulseMCP and](https://www.pulsemcp.com/)

[Goose teams to help build a centralized community registry. Registry Maintainer](https://block.github.io/goose/)

[Tadas Antanavicius from](https://github.com/tadasant)

[PulseMCP spearheaded the initial effort in collaboration with](https://www.pulsemcp.com/)

[Alex Hancock from](https://github.com/alexhancock)

[Block. They were soon joined by Registry Maintainer](https://block.xyz/)

[Toby Padilla, Head of MCP at](https://github.com/toby)

[GitHub, and more recently,](https://github.com/)

[Adam Jones from](https://github.com/domdomegg)

[Anthropic joined as Registry Maintainer to drive the project towards the launch today. The](https://www.anthropic.com/)

[initial announcement of the MCP Registry’s development lists 16 contributing individuals from at least 9 different companies.](https://github.com/modelcontextprotocol/registry/discussions/11)

Many others made crucial contributions to bring this project to life:

[Radoslav Dimitrov from](https://github.com/rdimitrov)

[Stacklok,](https://stacklok.com/)

[Avinash Sridhar from](https://github.com/sridharavinash)

[GitHub,](https://github.com/)

[Connor Peet from](https://github.com/connor4312)

[VS Code,](https://code.visualstudio.com/)

[Joel Verhagen from](https://github.com/joelverhagen)

[NuGet,](https://www.nuget.org/)

[Preeti Dewani from](https://github.com/pree-dew)

[Last9,](https://last9.io/)

[Avish Porwal from](https://github.com/Avish34)

[Microsoft,](https://www.microsoft.com/)

[Jonathan Hefner, and many Anthropic and GitHub employees that provided code reviews and development support. We are also grateful to everyone on the](https://github.com/jonathanhefner)

[Registry’s contributors log and those who participated in](https://github.com/modelcontextprotocol/registry/graphs/contributors)

[discussions and issues.](https://github.com/modelcontextprotocol/registry)

We deeply appreciate everyone investing in this foundational open source infrastructure. Together, we’re helping developers and organizations worldwide to build more reliable, context-aware AI applications. On behalf of the MCP community, thank you.

#top

````

## 五、输出要求

直接给出译文，用 ``` 包裹便于复制。**不要**输出任何解释、前言或后记。

```

## 五、AI 返回的译文全文

```markdown
[跳到内容](#main-content)

今天，我们推出 Model Context Protocol（MCP）Registry —— 一个面向公开可用 MCP 服务器的开放目录与 API，旨在提升可发现性与实现效率。通过标准化服务器的分发与发现方式，我们既扩大了它们的覆盖面，也让客户端更容易建立连接。

MCP Registry 现已开放预览。开始使用：

- 按照我们的指南添加你的服务器：
- [向 MCP Registry 添加服务器（面向服务器维护者）](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/quickstart.mdx) 按照我们的指南访问服务器数据：
- [访问 MCP Registry 数据（面向客户端维护者）](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/registry-aggregators.mdx)

MCP 服务器的单一事实来源

# [#](#single-source-of-truth-for-mcp-servers)

2025 年 3 月，我们曾表示希望为 MCP 生态构建一个中心化注册表。今天我们宣布，我们已经上线

[https://registry.modelcontextprotocol.io 作为官方 MCP Registry。作为 MCP 项目的一部分，MCP Registry 以及父级的](https://registry.modelcontextprotocol.io)

[OpenAPI 规格都是开源的 —— 任何人都可以构建兼容的子注册表。](https://github.com/modelcontextprotocol/registry/blob/main/docs/reference/api/official-registry-api.md)

我们的目标是标准化服务器的分发与发现方式，提供一个子注册表可以据以构建的单一事实来源。这反过来会扩大服务器的覆盖面，帮助客户端在 MCP 生态中更容易地找到服务器。

公开与私有子注册表

### [#](#public-and-private-sub-registries)

在构建中心化注册表时，我们很重视不去削弱社区与企业已经建立起来的现有注册表。MCP Registry 作为公开可用 MCP 服务器的单一事实来源，各组织可以选择

[基于自定义标准创建子注册表。例如：](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/registry-aggregators.mdx)

像与各个 MCP 客户端绑定的「MCP 应用市场」这类有主张的公开子注册表，可以自由地增强和扩展它们从上游 MCP Registry 摄取的数据。每一类 MCP 终端用户都有不同的需求，理应由 MCP 客户端市场以各自有主张的方式来服务好自己的终端用户。

私有子注册表将存在于有严格隐私与安全要求的企业内部，而 MCP Registry 为这些企业提供了一个可供构建的单一上游数据源。至少，我们的目标是与这些私有实现共享 API schema，使相关 SDK 与工具链能在整个生态中共享。

两种情况下，MCP Registry 都是起点 —— 它是 MCP 服务器维护者发布并维护其自报信息的集中位置，供这些下游消费者加工并交付给各自的终端用户。

社区驱动的审核机制

### [#](#community-driven-mechanism-for-moderation)

MCP Registry 是由注册表工作组维护、采用宽松许可证的官方 MCP 项目。社区成员可以提交 issue 来举报违反 MCP

[审核准则的服务器 —— 例如包含垃圾信息、恶意代码，或冒充合法服务。注册表维护者随后可以将这些条目列入拒绝名单，并追溯性地将其从公开访问中移除。](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/moderation-policy.mdx)

开始使用

## [#](#getting-started)

开始使用：

- 按照我们的指南添加你的服务器：
- [向 MCP Registry 添加服务器（面向服务器维护者）](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/quickstart.mdx) 按照我们的指南访问服务器数据：
- [访问 MCP Registry 数据（面向客户端维护者）](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/registry-aggregators.mdx)

MCP Registry 的这个预览版旨在帮助我们在正式可用之前改进用户体验，不提供数据持久性保证或其他担保。我们建议 MCP 采用者密切关注开发进展，因为在注册表正式可用之前可能会出现破坏性变更。

随着我们持续开发注册表，我们欢迎在

[modelcontextprotocol/registry GitHub 仓库上提出反馈与贡献：Discussion、Issues 和 Pull Request 都欢迎。](https://github.com/modelcontextprotocol/registry)

感谢 MCP 社区

## [#](#thanks-to-the-mcp-community)

MCP Registry 从一开始就是协作的成果，我们非常感谢广大开发者社区的热情与支持。

2025 年 2 月，它作为一个草根项目起步，当时 MCP 的创建者

[David Soria Parra 和](https://github.com/dsp-ant)

[Justin Spahr-Summers 请](https://github.com/jspahrsummers)

[PulseMCP 和](https://www.pulsemcp.com/)

[Goose 团队帮忙构建一个中心化的社区注册表。注册表维护者](https://block.github.io/goose/)

[来自 PulseMCP 的](https://github.com/tadasant)

[Tadas Antanavicius 与](https://www.pulsemcp.com/)

[来自 Block 的](https://github.com/alexhancock)

[Alex Hancock 共同推动了最初的工作。很快，注册表维护者](https://block.xyz/)

[Toby Padilla（GitHub 的 MCP 负责人）加入，最近](https://github.com/toby)

[来自](https://github.com/)

[Anthropic 的 Adam Jones 也作为注册表维护者加入，推动项目走到今天的发布。](https://github.com/domdomegg)

[Anthropic 的 Adam Jones 也作为注册表维护者加入，推动项目走到今天的发布。](https://www.anthropic.com/)

[MCP Registry 开发工作的最初公告列出了来自至少 9 家不同公司的 16 位贡献者。](https://github.com/modelcontextprotocol/registry/discussions/11)

许多其他人为这个项目落地做出了关键贡献：

[来自](https://github.com/rdimitrov)

[Stacklok 的 Radoslav Dimitrov，](https://stacklok.com/)

[来自](https://github.com/sridharavinash)

[GitHub 的 Avinash Sridhar，](https://github.com/)

[来自](https://github.com/connor4312)

[VS Code 的 Connor Peet，](https://code.visualstudio.com/)

[来自](https://github.com/joelverhagen)

[NuGet 的 Joel Verhagen，](https://www.nuget.org/)

[来自](https://github.com/pree-dew)

[Last9 的 Preeti Dewani，](https://last9.io/)

[来自](https://github.com/Avish34)

[Microsoft 的 Avish Porwal，](https://www.microsoft.com/)

[Jonathan Hefner，以及许多提供代码审查与开发支持的 Anthropic 和 GitHub 员工。我们也感谢注册表](https://github.com/jonathanhefner)

[贡献者名录上的每一位，以及所有参与](https://github.com/modelcontextprotocol/registry/graphs/contributors)

[讨论与 issue 的人。](https://github.com/modelcontextprotocol/registry)

我们深深感谢每一位为这项基础性开源基础设施投入的人。我们正携手帮助全球的开发者与组织构建更可靠、更具上下文感知能力的 AI 应用。谨代表 MCP 社区，谢谢大家。

#top

```
