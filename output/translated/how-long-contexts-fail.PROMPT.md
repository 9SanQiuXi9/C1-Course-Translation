# 翻译留痕：how-long-contexts-fail

- doc_id：`how-long-contexts-fail`
- 时间：2026-09-27T17:05:15+08:00
- 原文：`extracted/how-long-contexts-fail.md`
- 译文：`translated/how-long-contexts-fail.md`
- 原文 sha256：`402eb0c9756c80b66f4c1f2f8765e43317f6fa0fd9fffd2acc7d99b09133150b`
- 译文 sha256：`3342556b6e74f3bd1a27b38c3627e9ec43db7037b0f1dee874744327a3dbd104`
- 术语约束条数：20

## 一、本文档涉及的术语清单

| 英文 | 译法 | handling | 出现次数 |
|---|---|---|---|
| `context` | 上下文 | `translate` | 75 |
| `model` | 模型 | `translate` | 17 |
| `prompt` | 提示词 | `translate` | 12 |
| `tool` | 工具 | `translate` | 11 |
| `agent` | 智能体 | `translate` | 7 |
| `reasoning` | 推理 | `translate` | 4 |
| `mcp` | MCP | `acronym` | 3 |
| `agentic` | 智能体式 | `translate` | 3 |
| `training` | 训练 | `translate` | 3 |
| `token` | token | `keep_en` | 3 |
| `benchmark` | 基准测试 | `translate` | 3 |
| `retrieval` | 检索 | `translate` | 2 |
| `hallucination` | 幻觉 | `translate` | 2 |
| `rag` | RAG | `acronym` | 2 |
| `api` | API | `acronym` | 1 |
| `workflow` | 工作流 | `translate` | 1 |
| `llm` | LLM | `acronym` | 1 |
| `dataset` | 数据集 | `translate` | 1 |
| `context window` | 上下文窗口 | `translate` | 1 |
| `system prompt` | 系统提示词 | `translate` | 1 |

## 二、落盘校验结果

```json
{
  "non_empty": true,
  "code_blocks_total": 0,
  "code_blocks_in_translation": 0,
  "code_blocks_match": true,
  "code_blocks_byte_identical": true,
  "urls_orig": 13,
  "urls_trans": 13,
  "urls_all_present": true,
  "urls_counts_equal": true,
  "headings_orig": 7,
  "headings_trans": 7,
  "headings_match": true,
  "orig_chars": 9734,
  "trans_chars": 4575,
  "length_ratio": 0.47,
  "length_ratio_ok": true
}
```

## 四、发出的 prompt 全文

```markdown
(未找到 prompt 导出文件)
```

## 五、AI 返回的译文全文

```markdown
Jun 22, 2025

AGENTS

LLM

AI

PROMPTING

CONTEXT MANAGEMENT

## 长上下文为何失效

![](/img/overload.jpg)

### 管好你的上下文，是智能体成功的关键

随着前沿模型的上下文窗口不断增大

[1，许多已支持多达 100 万 token，我看到很多兴奋的讨论，说长上下文窗口将解锁我们梦想中的智能体。毕竟，只要窗口足够大，你就可以把所有可能需要的东西 —— 工具、文档、指令等等 —— 一股脑塞进提示词，剩下的交给模型。](#fn:longcontext)

长上下文打残了 RAG 的热情（当你能把所有东西都塞进提示词时，何必再去找最佳文档！），催生了 MCP 的热潮（连接所有工具，模型就能干任何活！），也助长了对智能体的热情

[2。](#fn:googledocs)

但现实中，更长的上下文并不会产生更好的回答。把上下文塞得过满，会让你的智能体与应用以令人意外的方式失效。上下文会被毒化、被分散注意力、被搞糊涂，或者自相冲突。这对智能体尤其成问题 —— 智能体依赖上下文来收集信息、综合发现并协调行动。

我们逐一走一遍上下文失控的方式，然后回顾缓解或彻底避免上下文失效的方法。

# 上下文的失效模式

- [上下文毒化：当幻觉进入上下文](#context-poisoning)
- [上下文分心：当上下文压过训练所得](#context-distraction)
- [上下文混淆：当多余上下文影响回答](#context-confusion)
- [上下文冲突：当上下文各部分互相矛盾](#context-clash)

---

### 上下文毒化

上下文毒化，是指幻觉或其他错误进入了上下文，并被反复引用。

Deep Mind 团队在

[Gemini 2.5 技术报告中指出了上下文毒化问题，我们](https://storage.googleapis.com/deepmind-media/gemini/gemini_v2_5_report.pdf)

[上周做了拆解。在玩 Pokémon 时，Gemini 智能体偶尔会在游戏中产生幻觉，从而毒化了它自己的上下文：](https://www.dbreunig.com/2025/06/17/an-agentic-case-study-playing-pokémon-with-gemini.html)

这个问题有一种尤其严重的形态，就是「上下文毒化」—— 上下文的许多部分（目标、摘要）都被关于游戏状态的错误信息「毒化」，而这种毒化往往要很久才能消除。结果是，模型可能变得执迷于实现不可能或不相关的目标。

如果它上下文中「目标」那一段被毒化，智能体就会发展出荒谬的策略，并为了一个根本无法达成的目标反复重复某些行为。

### 上下文分心

上下文分心，是指上下文变得太长，以至于模型过度专注于上下文，而忽略了它在训练中学到的东西。

在智能体工作流中，随着上下文增长 —— 模型收集到更多信息、积累起历史 —— 这些累积的上下文可能变得令人分心，而不是有所帮助。玩 Pokémon 的 Gemini 智能体清楚地展示了这个问题：

虽然 Gemini 2.5 Pro 支持 100 万以上的 token 上下文，但要为智能体有效利用它，
仍是一个新的研究前沿。在这个智能体配置中，可以观察到当上下文显著超过 10 万 token 后，智能体表现出一种倾向：更愿意重复它庞大历史中的既有动作，而不是综合出新的计划。这一现象虽然只是轶事性的，却凸显了一个重要区别：用于检索的长上下文，与用于多步生成式推理的长上下文，是两回事。

智能体没有用训练所得去发展新策略，而是执迷于重复它那庞大上下文历史中的过往动作。

对较小的模型来说，分心的天花板要低得多。一项

[Databricks 研究发现，Llama 3.1 405b 大约在 32k 时正确率就开始下降，更小的模型更早。](https://www.databricks.com/blog/long-context-rag-performance-llms)

如果模型在上下文窗口被填满之前很久就开始表现异常，那超大的上下文窗口意义何在？一句话：摘要

[3 与事实检索。如果你要做的不是这两件事，那就要警惕你所选模型的分心天花板。](#fn:summarization)

### 上下文混淆

上下文混淆，是指上下文里多余的内容被模型用来生成低质量的回答。

有那么一阵子，看起来人人都要发布一个

[MCP。一个强大的模型连接上你所有的服务与东西、替你处理所有琐碎任务的梦想，似乎触手可及。只要把所有工具描述都塞进提示词，然后开跑。](https://www.dbreunig.com/2025/03/18/mcps-are-apis-for-llms.html)

[Claude 的系统提示词给我们指了路，因为它的内容大多就是工具定义或使用工具的指令。](https://www.dbreunig.com/2025/05/07/claude-s-system-prompt-chatbots-are-more-than-just-models.html)

但即使

[整合与竞争没有让 MCP 慢下来，上下文混淆也会。事实证明，工具确实是可能太多的。](https://www.dbreunig.com/2025/06/16/drawbridges-go-up.html)

[Berkeley Function-Calling Leaderboard 是一个工具使用基准，评估模型有效使用工具来回应提示词的能力。现在已到第 3 版，这个排行榜显示：当提供的工具超过一个时，每个模型的表现都会变差](https://gorilla.cs.berkeley.edu/leaderboard.html)

[4。更进一步，Berkeley 团队「设计了所提供函数全都无关的场景……我们期望模型的输出是不调用任何函数。」然而，所有模型都会偶尔调用不相关的工具。](#fn:live)

浏览这个函数调用排行榜，你会看到模型越小，问题越严重：

![](/img/gemma_irrelevance.png)

上下文混淆有一个很醒目的例子，来自

[最近一篇论文，它评估小模型在](https://arxiv.org/pdf/2411.15399?)

[GeoEngine 基准上的表现 —— 这个测试包含 46 种不同的工具。当团队给一个量化（压缩）过的 Llama 3.1 8b 一个带全部 46 个工具的查询时，它失败了，尽管上下文远在 16k 的上下文窗口之内。但当他们只给模型 19 个工具时，它成功了。](https://arxiv.org/abs/2404.15500)

问题在于：只要你把某样东西放进上下文，模型就必须关注它。它可能是无关信息或无谓的工具定义，但模型会把它纳入考虑。大模型，尤其是推理模型，正越来越擅长忽略或丢弃多余的上下文，但我们仍不断看到无用信息把智能体绊倒。更长的上下文让我们能塞进更多信息，但这种能力是有代价的。

### 上下文冲突

上下文冲突，是指你在上下文中累积的新信息与工具，和上下文里的其他信息互相矛盾。

这是上下文混淆更麻烦的一种版本：这里的坏上下文不是无关，而是与提示词中的其他信息直接冲突。

一个 Microsoft 与 Salesforce 的团队在

[最近一篇论文中精彩地记录了这一点。该团队从多个基准取来提示词，把其中的信息「分片」到多条提示词里。可以这样理解：有时你会坐下来，在按回车之前往 ChatGPT 或 Claude 里敲好几段话，把每个必要细节都考虑进去。另一些时候，你会先给一句简单的提示词，等聊天机器人的答案不满意时再补充细节。Microsoft/Salesforce 团队把基准提示词改造成了这类多步对话的样子：](https://arxiv.org/pdf/2505.06120)

![](/img/sharded_prompt.png)

左侧提示词里的全部信息，都包含在右侧的几条消息中，而这些消息会在多轮对话中依次展开。

分片后的提示词带来的结果显著变差，平均下降 39%。团队测试了一系列模型 —— OpenAI 备受推崇的 o3 得分从 98.1 掉到 64.1。

这是怎么回事？为什么信息分阶段给出、而不是一次性给全，模型表现反而更差？

答案是上下文混淆：组装起来的上下文包含了整段对话往来，其中含有模型在尚未掌握全部信息时给出的早期尝试。这些错误答案仍然留在上下文里，并在模型生成最终答案时影响它。团队写道：

我们发现，LLM 常在早期轮次做出假设，并过早地尝试给出最终解法，然后又过度依赖这些解法。用更简单的话说，我们发现当 LLM 在对话中走错一步，它们就会迷失，且无法恢复。

这对智能体构建者可不是好兆头。智能体从文档、工具调用以及被派去解决子问题的其他模型那里组装上下文。所有这些来自不同来源的上下文，都有可能自相矛盾。更进一步，当你连接的不是自己创建的 MCP 工具时，它们的描述与指令和你提示词其余部分冲突的可能性更大。

---

百万 token 上下文窗口的出现曾让人觉得是一场变革。能把智能体可能需要的一切都塞进提示词，激发了这样的想象：一个超级智能助手，能访问任何文档、连接每一个工具，并保持完美的记忆。

但正如我们所见，更大的上下文带来了新的失效模式。上下文毒化会埋下随时间累积的错误。上下文分心让智能体严重依赖上下文、重复过往动作，而不是向前推进。上下文混淆导致使用无关的工具或文档。上下文冲突制造内部矛盾，让推理脱轨。

这些失效对智能体打击最重，因为智能体恰恰运行在上下文膨胀的场景里：从多个来源收集信息、进行连续的工具调用、参与多轮推理，并累积大量历史。

幸运的是，是有解法的！在下一篇文章中，我们将介绍缓解或避免这些问题的技术，从动态加载工具的方法到建立上下文隔离区。

阅读后续文章《

[如何修好你的上下文》。](/2025/06/26/how-to-fix-your-context.html)

---

输入你的邮箱，偶尔接收更新。

1. Gemini 2.5 与 GPT-4.1 拥有 100 万 token 的上下文窗口，大到足以把 [《无尽的笑话》整本塞进去还绰绰有余。](https://en.wikipedia.org/wiki/Infinite_Jest)
2. [↩](#fnref:longcontext)

3. Gemini 文档中「[长文本」那一节很好地总结了这种乐观。](https://ai.google.dev/gemini-api/docs/long-context#long-form-text)
4. [↩](#fnref:googledocs)

5. 事实上，在上面引用的 Databricks 研究里，模型在长上下文下最常见的失败方式，就是返回对所给上下文的摘要，而忽略提示词中包含的任何指令。
6. [↩](#fnref:summarization)

7. 如果你也在那个排行榜上，留意「Live (AST)」那几列。[这些指标使用企业贡献给产品的真实工具定义，「避免数据集污染与基准偏差带来的弊端」。](https://gorilla.cs.berkeley.edu/blogs/12_bfcl_v2_live.html)
8. [↩](#fnref:live)

/2025/06/22/how-contexts-fail-and-how-to-fix-them.html

```
