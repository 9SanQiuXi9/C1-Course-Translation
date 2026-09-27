---
source_file: "data/materials/CS146S_offline/pages/mcp-registry-preview.html"
origin_url: "https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/"
title: "[#](#single-source-of-truth-for-mcp-servers)"
extract_method: "html"
extract_warnings:
  - "STRIPPED_BLOCKS：按 class/id 关键词剥离了 1 个非正文区块（正文下降 6.5%）"
src_sha256: "e62944b6ac577be79b070b5dedce0c3f2d817653b8fb15f6373d42da027e3632"
chars: 7379
code_blocks: 0
tables: 0
links: 44
garbage_rate: 0.0938
heading_levels_seen:
  h1: 3
  h2: 2
---

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
