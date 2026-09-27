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
