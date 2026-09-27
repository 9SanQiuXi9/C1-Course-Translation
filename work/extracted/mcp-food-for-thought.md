---
source_file: "data/materials/CS146S_offline/pages/mcp-food-for-thought.html"
origin_url: "https://www.reillywood.com/blog/apis-dont-make-good-mcp-tools/"
title: "[APIs don't make good MCP tools](/blog/apis-dont-make-good-mcp-tools/)"
extract_method: "html"
extract_warnings:
  - "STRIPPED_BLOCKS：按 class/id 关键词剥离了 13 个非正文区块（正文下降 6.9%）"
src_sha256: "b122f33b67d9b2563c147f2f3369245a36a8b9c3f8e995a1ea6d0562ec6ca672"
chars: 6847
code_blocks: 3
tables: 0
links: 40
garbage_rate: 0.0233
heading_levels_seen:
  h2: 7
  h3: 8
---

# [APIs don't make good MCP tools](/blog/apis-dont-make-good-mcp-tools/)

4 minute read

The

[Model Context Protocol (MCP) is a pretty big deal these days. It’s become the de facto standard for giving LLMs access to tools that someone else wrote, which, of course, turns them into](https://modelcontextprotocol.io/overview)

[agents. But writing tools for a new MCP server is hard, and so people often propose](https://simonwillison.net/2025/May/22/tools-in-a-loop/)

[auto-converting existing APIs into MCP tools; typically using OpenAPI metadata (](https://blog.christianposta.com/semantics-matter-exposing-openapi-as-mcp-tools/)

[1,](https://jedisct1.github.io/openapi-mcp/)

[2).](https://www.gravitee.io/blog/turn-any-rest-api-into-mcp-server-inside-gravitee)

In my experience, this can work but it doesn’t work well. Here are a few reasons why:

## Agents don’t do well with large numbers of tools

Infamously,

[VS Code has a hard limit of 128 tools - but](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode)

[many models struggle with accurate tool calling well before that number. Also, each tool and its description takes up valuable context window space.](https://arxiv.org/abs/2411.15399)

Most web APIs weren’t designed with these constraints in mind! It’s fine to have umpteen APIs for a single product area when those APIs are called from code, but if each of those APIs is mapped to an MCP tool the results might not be great.

MCP tools designed from the ground up are typically

[much more flexible than individual web APIs, with each tool being able to do the work of several individual APIs.](https://engineering.block.xyz/blog/blocks-playbook-for-designing-mcp-servers)

## APIs can blow through context windows quickly

Imagine an API that returns 100 records at a time, and each record is very wide (say, 50 fields). Sending those results to an agent as-is will use up a lot of tokens; even if a query can be satisfied with only a few fields, every field ends up in the context window.

APIs are typically paginated by the number of records, but records can vary a lot in size. One record might contain a large text field that takes up 100,000

[tokens, while another might contain 10. Putting these API results directly into an agent’s context window is a gamble; sometimes it works, sometimes it will blow up.](https://learn.microsoft.com/en-us/dotnet/ai/conceptual/understanding-tokens)

The format of the data can also be an issue. Most web APIs these days return JSON, but JSON is a very token-inefficient format. Take this:

<!-- CODE_BLOCK_START id=c1 lang=json -->
```json
[
  {
    "firstName": "Alice",
    "lastName": "Johnson",
    "age": 28
  },
  {
    "firstName": "Bob",
    "lastName": "Smith",
    "age": 35
  }
]
```
<!-- CODE_BLOCK_END id=c1 -->

Compare to the same data in CSV format:

<!-- CODE_BLOCK_START id=c2 lang=csv -->
```csv
firstName,lastName,age
Alice,Johnson,28
Bob,Smith,35
```
<!-- CODE_BLOCK_END id=c2 -->

The CSV data is much more succinct - it uses up half as many tokens per record.

[Typically CSV, TSV, or YAML (for nested data) are better choices than JSON.](https://david-gilbertson.medium.com/llm-output-formats-why-json-costs-more-than-tsv-ebaf590bd541)

None of these issues are insurmountable. You could imagine automatically adding tool arguments that let agents

[project fields, automatically truncating or summarizing large results, and automatically converting JSON results to CSV (or YAML for nested data). But most servers I’ve seen do none of those things.](https://en.wikipedia.org/wiki/Projection_(relational_algebra))

## APIs don’t make the most of agents’ unique capabilities

APIs return structured data for programmatic consumption. That’s often what agents want from tool calls… but agents can also handle other, more free-form instructions.

For example an ask_question tool could perform a RAG query over some documentation, then return information in plain text that is used to inform the next tool call - skipping structured data entirely.

Or, a call to a search_cities tool could return a structured list of cities and a suggestion of what to call next:

<!-- CODE_BLOCK_START id=c3 lang=csv -->
```csv
city_name,population,country,region
Tokyo,37194000,Japan,Asia
Delhi,32941000,India,Asia
Shanghai,28517000,China,Asia

Suggestion: To get more specific information (weather, attractions, demographics), try calling get_city_details with the city_name parameter.
```
<!-- CODE_BLOCK_END id=c3 -->

That sort of layering and tool chaining

[can be very effective in MCP servers, and it’s something you’ll miss out on completely if auto-converting APIs to tools.](https://engineering.block.xyz/blog/build-mcp-tools-like-ogres-with-layers)

## If an agent needs to call an API, it could just do that

Agents like Claude Code are remarkably capable of writing+executing code these days, including scripts that call web APIs. Some people take this so far as to

[argue that MCP isn’t needed at all!](https://lucumr.pocoo.org/2025/7/3/tools/)

I disagree with that conclusion, but I do think we should skate to where the puck is going.

[Sandboxing of agents is improving rapidly, and if it’s easy+safe for an agent to call APIs directly then we might as well do that and cut out the middleman.](https://github.com/openai/codex)

## Conclusion

Agents are fundamentally different from the typical consumers of APIs. It’s possible to automatically create MCP tools from existing APIs, but doing that is unlikely to work well. Agents do best when given tools that are designed for their unique capabilities and limitations.

- [Land Values and Affordability](/blog/land-value/)
- [Tool Calls Are Expensive And Finite](/blog/tool-calls-are-expensive-and-finite/)

/

![headshot](/img/main/headshot-2025.jpg)

## [Cities & Code](/)

- /index.xml
- //github.com/rgwood
- //linkedin.com/in/reilly-wood-912a31a
- //bsky.app/profile/reillywood.com
- //bsky.app/profile/grids.reillywood.com

### Recent Posts

/blog/year-end-2025/

### 💻 2025 Retrospective

December 28, 2025

/blog/whats-mcp-good-for/

### 💻 What's MCP good for, anyway?

December 26, 2025

/blog/tool-calls-are-expensive-and-finite/

### 💻 Tool Calls Are Expensive And Finite

September 18, 2025

/blog/apis-dont-make-good-mcp-tools/

### 💻 APIs don't make good MCP tools

August 5, 2025

/blog/land-value/

### 🏗️ Land Values and Affordability

June 26, 2025

/blog/dmca-fun/

### 📝 My encounter with evil SEO

June 16, 2025

[View more posts](/blog/page/2/)

### Top Categories

[Software](/categories/software/)

[Urban Planning](/categories/urban-planning/)

[Recently](/categories/recently/)

[Rust](/categories/rust/)

[Web](/categories/web/)

[Databases](/categories/databases/)

[LLMs](/categories/llms/)

[Nushell](/categories/nushell/)

[View all categories](/categories/)
