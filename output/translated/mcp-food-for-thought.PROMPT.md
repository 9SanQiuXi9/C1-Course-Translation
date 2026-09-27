# 翻译留痕：mcp-food-for-thought

- doc_id：`mcp-food-for-thought`
- 时间：2026-09-27T16:31:58+08:00
- 原文：`extracted/mcp-food-for-thought.md`
- 译文：`translated/mcp-food-for-thought.md`
- 原文 sha256：`a4faf6ae0081718a84a5e400e1b901d3def8b92943526c995b8cbd161901c721`
- 译文 sha256：`2893dbd5f0a52966929cf4e201317f6badc758a4b7805b44ddfcc7b0283a7280`
- 术语约束条数：11

## 一、本文档涉及的术语清单

| 英文 | 译法 | handling | 出现次数 |
|---|---|---|---|
| `mcp` | MCP | `acronym` | 23 |
| `tool` | 工具 | `translate` | 14 |
| `agent` | 智能体 | `translate` | 5 |
| `context` | 上下文 | `translate` | 5 |
| `api` | API | `acronym` | 4 |
| `context window` | 上下文窗口 | `translate` | 3 |
| `server` | 服务器 | `translate` | 2 |
| `model` | 模型 | `translate` | 1 |
| `llm` | LLM | `acronym` | 1 |
| `token` | token | `keep_en` | 1 |
| `rag` | RAG | `acronym` | 1 |

## 二、落盘校验结果

```json
{
  "non_empty": true,
  "code_blocks_total": 3,
  "code_blocks_in_translation": 3,
  "code_blocks_match": true,
  "code_blocks_byte_identical": true,
  "urls_orig": 14,
  "urls_trans": 14,
  "urls_all_present": true,
  "urls_counts_equal": true,
  "headings_orig": 15,
  "headings_trans": 15,
  "headings_match": true,
  "orig_chars": 5255,
  "trans_chars": 3180,
  "length_ratio": 0.6051,
  "length_ratio_ok": true
}
```

## 四、发出的 prompt 全文

```markdown
# 翻译任务：mcp-food-for-thought

## 一、文档元数据

- doc_id：`mcp-food-for-thought`
- title：[APIs don't make good MCP tools](/blog/apis-dont-make-good-mcp-tools/)
- origin_url：https://www.reillywood.com/blog/apis-dont-make-good-mcp-tools/
- 本段字符数：6,850

## 二、术语约束（本文档用到的，必须严格遵守）

| 英文 | 处理方式 | 出现次数 |
|---|---|---|
| `mcp` | 保留英文缩写（首次出现给全称） | 23 |
| `tool` | 翻译为「工具」 | 14 |
| `agent` | 翻译为「智能体」 | 5 |
| `context` | 翻译为「上下文」 | 5 |
| `api` | 保留英文缩写（首次出现给全称） | 4 |
| `context window` | 翻译为「上下文窗口」 | 3 |
| `server` | 翻译为「服务器」 | 2 |
| `model` | 翻译为「模型」 | 1 |
| `llm` | 保留英文缩写（首次出现给全称） | 1 |
| `token` | 保留英文原形（不翻译） | 1 |
| `rag` | 保留英文缩写（首次出现给全称） | 1 |

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

````

## 五、输出要求

直接给出译文，用 ``` 包裹便于复制。**不要**输出任何解释、前言或后记。

```

## 五、AI 返回的译文全文

```markdown
# [API 做不出好的 MCP 工具](/blog/apis-dont-make-good-mcp-tools/)

阅读时间 4 分钟

如今，

[Model Context Protocol（MCP）是件大事。它已成为让 LLM 访问他人所写工具的事实标准，而这当然就把 LLM 变成了](https://modelcontextprotocol.io/overview)

[智能体。但为新的 MCP 服务器编写工具很难，所以人们常常提出](https://simonwillison.net/2025/May/22/tools-in-a-loop/)

[把现有 API 自动转换成 MCP 工具；通常借助 OpenAPI 元数据（](https://blog.christianposta.com/semantics-matter-exposing-openapi-as-mcp-tools/)

[1，](https://jedisct1.github.io/openapi-mcp/)

[2）。](https://www.gravitee.io/blog/turn-any-rest-api-into-mcp-server-inside-gravitee)

以我的经验，这样做能行，但效果不好。原因有几点：

## 智能体应付不了大量工具

众所周知，

[VS Code 对工具数量有 128 个的硬性上限 —— 但](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode)

[很多模型在远低于这个数量时，工具调用就已经不够准确了。而且每个工具及其描述都会占用宝贵的上下文窗口空间。](https://arxiv.org/abs/2411.15399)

大多数 Web API 在设计时根本没考虑这些约束！当这些 API 是从代码中调用时，单个产品领域有无数个 API 也没问题；但如果把每个 API 都映射成一个 MCP 工具，结果可能就不理想了。

从头设计的 MCP 工具通常

[比单个 Web API 灵活得多，一个工具就能完成好几个 API 的工作。](https://engineering.block.xyz/blog/blocks-playbook-for-designing-mcp-servers)

## API 会很快耗尽上下文窗口

设想一个 API 每次返回 100 条记录，而每条记录都很宽（比如 50 个字段）。把这些结果原样发给智能体就会消耗大量 token；即使某个查询只需要几个字段就能满足，所有字段最终还是会进入上下文窗口。

API 通常按记录条数分页，但记录的大小可能相差极大。一条记录可能包含一个占 100,000

[token 的大文本字段，而另一条可能只占 10 个。把这些 API 结果直接放进智能体的上下文窗口是场赌博；有时可行，有时会直接爆掉。](https://learn.microsoft.com/en-us/dotnet/ai/conceptual/understanding-tokens)

数据的格式也可能是问题。如今大多数 Web API 返回 JSON，但 JSON 是一种 token 效率很低的格式。看这个：

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

对比同样的数据用 CSV 格式：

<!-- CODE_BLOCK_START id=c2 lang=csv -->
```csv
firstName,lastName,age
Alice,Johnson,28
Bob,Smith,35
```
<!-- CODE_BLOCK_END id=c2 -->

CSV 数据简洁得多 —— 每条记录消耗的 token 只有一半。

[通常 CSV、TSV，或（用于嵌套数据的）YAML 都比 JSON 更合适。](https://david-gilbertson.medium.com/llm-output-formats-why-json-costs-more-than-tsv-ebaf590bd541)

这些问题都不是无法克服的。你可以设想自动增加一些工具参数，让智能体能够

[投影字段、自动截断或摘要化大结果，以及自动把 JSON 结果转成 CSV（嵌套数据则转成 YAML）。但我见过的大多数服务器这些都没做。](https://en.wikipedia.org/wiki/Projection_(relational_algebra))

## API 没能充分利用智能体独有的能力

API 返回结构化数据，供程序化消费。这往往正是智能体想要从工具调用中得到的东西……但智能体也能处理其他更自由形式的指令。

例如，一个 ask_question 工具可以对某些文档执行 RAG 查询，然后用纯文本返回信息，用于指导下一次工具调用 —— 完全跳过结构化数据。

或者，对 search_cities 工具的一次调用可以返回一个结构化的城市列表，并附上接下来该调用什么的建议：

<!-- CODE_BLOCK_START id=c3 lang=csv -->
```csv
city_name,population,country,region
Tokyo,37194000,Japan,Asia
Delhi,32941000,India,Asia
Shanghai,28517000,China,Asia

Suggestion: To get more specific information (weather, attractions, demographics), try calling get_city_details with the city_name parameter.
```
<!-- CODE_BLOCK_END id=c3 -->

这种分层与工具链式调用

[在 MCP 服务器里可以非常有效，而如果你把 API 自动转换成工具，就会完全错过这一点。](https://engineering.block.xyz/blog/build-mcp-tools-like-ogres-with-layers)

## 如果智能体需要调用某个 API，它直接调用就行了

如今像 Claude Code 这样的智能体，在编写并执行代码方面能力强得惊人，包括调用 Web API 的脚本。有些人甚至据此

[主张根本不需要 MCP！](https://lucumr.pocoo.org/2025/7/3/tools/)

我不同意这个结论，但我确实认为我们应该朝着冰球将要到达的位置滑。

[智能体的沙箱化正在快速进步，如果智能体直接调用 API 既简单又安全，那我们不妨就这么做，省掉中间商。](https://github.com/openai/codex)

## 结论

智能体与 API 的典型使用者有着根本区别。从现有 API 自动创建 MCP 工具是可行的，但这样做不太可能效果好。智能体表现最好，是在获得为其独有能力与局限而设计的工具时。

- [土地价值与可负担性](/blog/land-value/)
- [工具调用昂贵且有限](/blog/tool-calls-are-expensive-and-finite/)

/

![头像](/img/main/headshot-2025.jpg)

## [Cities & Code](/)

- /index.xml
- //github.com/rgwood
- //linkedin.com/in/reilly-wood-912a31a
- //bsky.app/profile/reillywood.com
- //bsky.app/profile/grids.reillywood.com

### 近期文章

/blog/year-end-2025/

### 💻 2025 年度回顾

December 28, 2025

/blog/whats-mcp-good-for/

### 💻 MCP 到底有什么用？

December 26, 2025

/blog/tool-calls-are-expensive-and-finite/

### 💻 工具调用昂贵且有限

September 18, 2025

/blog/apis-dont-make-good-mcp-tools/

### 💻 API 做不出好的 MCP 工具

August 5, 2025

/blog/land-value/

### 🏗️ 土地价值与可负担性

June 26, 2025

/blog/dmca-fun/

### 📝 我与恶意 SEO 的一次遭遇

June 16, 2025

[查看更多文章](/blog/page/2/)

### 热门分类

[软件](/categories/software/)

[城市规划](/categories/urban-planning/)

[近期](/categories/recently/)

[Rust](/categories/rust/)

[Web](/categories/web/)

[数据库](/categories/databases/)

[LLM](/categories/llms/)

[Nushell](/categories/nushell/)

[查看全部分类](/categories/)

```
