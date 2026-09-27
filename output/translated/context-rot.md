Products

[Sync](/products/sync)

[Database](/products/chromadb)

[Agent](/products/agent)

[Docs](https://docs.trychroma.com/)

[Enterprise](/enterprise)

[Pricing](/pricing)

[Research](/research)

Resources

[Changelog](/changelog)

[Updates](/updates)

[Community](https://discord.gg/MMeYNTmh3x)

[GitHub](https://github.com/chroma-core/chroma)

[Package Search](/package-search)

Log inSign up

![Chroma logo](/_next/static/media/logo-bw.11x653ba80g9x.svg?dpl=dpl_egYxRPRkHPqmMiuZksw8CbEt9xxU)

Chroma 技术报告

July 14, 2025

---

## 上下文腐化：输入 token 增长如何影响 LLM 表现

---

[Kelly Hong](https://x.com/kellyhongsn)

[Anton Troynikov](https://x.com/atroyn)

[Jeff Huber](https://x.com/jeffreyhuber)

人们通常假定大型语言模型（LLM）会**均匀地**处理上下文 —— 也就是说，模型应当以处理第 100 个 token 那样可靠的方式处理第 10,000 个 token。然而在实践中，这个假设并不成立。我们观察到，即使是在简单任务上，模型表现也会随输入长度变化而显著波动。

在本报告中，我们评估了 18 个 LLM，包括最先进的 GPT-4.1、Claude 4、Gemini 2.5 与 Qwen3 模型。我们的结果揭示：模型并不会均匀地使用它们的上下文；相反，随着输入长度增长，它们表现出的可靠性越来越低。

![上下文腐化：输入 token 增长如何影响 LLM 表现](/img/context_rot/header_plot.png)

![上下文腐化：输入 token 增长如何影响 LLM 表现](/img/context_rot/hero_plot.png)

*Claude Sonnet 4、GPT-4.1、Qwen3-32B 与 Gemini 2.5 Flash 在重复词任务上的表现*

LLM 近期的进展呈现出上下文窗口越来越长的趋势，最新模型的输入 token 数已达数百万。由于这些模型在「大海捞针」（NIAH）这类被广泛采用的基准上能取得近乎满分的成绩 [

[1]，人们常常假定它们在长上下文任务上的表现是均匀的。](#niah)

然而，NIAH 本质上是一个简单的检索任务：把一句已知的句子（「针」）放进一篇由无关文本构成的长文档（「草堆」）中，然后提示模型把它检索出来。这个基准虽然可扩展，但它通常考察的是直接的词面匹配，未必能代表灵活的、以语义为导向的任务。

![](/img/context_rot/niah_lexical.png)

*大海捞针（NIAH）设置示例*

我们扩展了标准的 NIAH 任务，以考察模型在此前探索不足的设置中的行为。我们考察了「针与问题之间是语义匹配而非直接词面匹配」的效果，以及给草堆内容引入变化所带来的效果。

此外，我们还加入了基于 LongMemEval 的对话式问答评估 [

[2]，以及一个合成任务：模型需要复述一系列重复的词。每个任务都被刻意设计得简单并受到严格控制，以便单独分离出上下文长度的影响。](#longmemeval)

我们证明，即使在这些最小条件下，模型表现也会随输入长度增长而退化，而且往往呈现出意外且不均匀的方式。真实世界的应用通常复杂度高得多，这意味着输入长度的影响在实践中可能更为显著。

我们的深度技术报告在下方继续。如果你觉得我们的工作有用，欢迎引用我们：

<!-- CODE_BLOCK_START id=c1 lang= -->
```
@techreport{hong2025context,
  title = {Context Rot: How Increasing Input Tokens Impacts LLM Performance},
  author = {Hong, Kelly and Troynikov, Anton and Huber, Jeff},
  year = {2025},
  month = {July},
  institution = {Chroma},
  url = {https://trychroma.com/research/context-rot},
}
```
<!-- CODE_BLOCK_END id=c1 -->

有兴趣改进 AI 应用的检索吗？

[Chroma 正在招聘](https://careers.trychroma.com/)

---

## 引言#

现代 LLM 拥有数百万 token 的输入上下文长度已是常态。Gemini 1.5 Pro [

[3] 在 2024 年初率先引入其 100 万上下文窗口，随后是近期 GPT-4.1 的 100 万上下文窗口 [](#gemini-1.5-pro)

[4] 以及 Llama 4 的 1000 万 [](#gpt-4.1)

[5]。长上下文的用例很有说服力：更长的上下文意味着 LLM 每次调用能处理更多信息、产出更有依据的输出。](#llama-4)

这些模型的长上下文评估往往显示其表现在各输入长度上是一致的。然而，这些评估范围狭窄，不能代表长上下文在实践中是如何被使用的。最常用的测试「大海捞针」（NIAH）是一个简单的词面检索任务，常被用来概括模型可靠处理长上下文的能力。真实应用 —— 例如智能体任务或摘要 —— 需要对更广泛、往往更含糊的信息做多得多的处理与推理。

设计贴近现实的长上下文基准很有挑战。任务往往会随输入长度增加而变得更复杂，因此很难分离出「表现下降究竟是因为输入更长，还是因为问题本身更难」。为解决这一点，我们的实验保持任务复杂度不变，只改变输入长度 —— 从而让我们能直接度量输入长度本身的影响。

# 贡献#

我们呈现以下内容：

- 一项覆盖 18 个 LLM（包括领先的闭源与开放权重模型）的评估，揭示了随输入长度增加而出现的不均匀表现。

- 一份关于模型在处理干扰项、以及问题—答案相似度变化时所表现出的模型特有行为模式的记述。

- [用于复现我们结果的完整代码库。](https://github.com/chroma-core/context-rot)

---

## 相关工作#

评估模型长上下文能力最广泛使用的基准之一是大海捞针（NIAH）。它作为一项可扩展的测试很有用，但它度量的能力很窄：词面检索。模型在 NIAH 上通常表现良好，这导致了「长上下文问题基本已解决」的印象。

然而，NIAH 低估了大多数长上下文任务在实践中的要求。NIAH 的变体，如 NoLiMa [

[6]（其针—问题对包含非词面匹配），揭示了显著的性能下降。其他在难度上看起来相似的任务，如 AbsenceBench [](#nolima)

[7]（测试模型能否识别出某段文本的缺失），也表现出随输入长度增长而出现的性能退化。](#absencebench)

此外，长上下文任务往往把「在干扰项之间做消歧」作为任务的一部分。一个例子是多轮共指消解（MRCR）[

[8] [](#michelangelo)

[9]，它涉及在多轮对话中、在若干相似的用户请求之间，检索出第 i 个特定用户请求。然而，关于长上下文设置中干扰项影响的研究仍然缺乏。](#oai-mrcr)

长上下文任务中的一个重要因素是输入长度是如何被放大的。Latent List [

[8] 是一个让模型在不同输入长度上执行固定数量 Python 列表操作的任务。该工作测试了多种填充无关上下文的方式，揭示了它们对模型表现的不均匀影响 [](#michelangelo)

[1]。例如，加入那些在局部相互抵消的列表操作，相比加入 print 语句，会更显著地降低模型表现。这凸显了「无关内容」的类型很重要，因为有些内容会随输入长度增加而引入递增的复杂度。](#clarification)

类似地，Graphwalks [

[10] 是一个图遍历任务：给模型一个由十六进制哈希构成的有向图，然后要求它从某个随机节点开始做广度优先搜索。增加输入长度意味着增大要遍历的图的规模，因此也就提高了任务难度。这里很难把递增的任务复杂度与输入长度区分开，因此难以单独分离出输入长度对表现的影响。这说明把输入长度作为唯一关注变量隔离出来很重要，而这对理解 LLM 在长输入下实际如何表现是必不可少的。](#graphwalks)

---

## 大海捞针扩展#

经典的大海捞针任务，是把一个随机事实（「针」）放进一个长上下文窗口（「草堆」）的中间，然后就此向模型提问。

该任务的原始实现使用词面匹配的针—问题对。然而，长上下文在实践中的使用，往往需要对含糊任务做语义理解。

![](/img/context_rot/niah/lexical_2.png)

*带词面匹配的大海捞针（NIAH）设置示例*

NoLiMa 已证明，随着上下文长度增加，非词面匹配会对模型构成挑战。该任务使用的针—问题对要求模型推断潜在的关联，例如：

问题：哪个角色去过赫尔辛基？

针：其实，Yuki 住在 Kiasma 博物馆隔壁。

*NoLiMa —— 一个针—问题对样例*

要回答这个问题，模型首先得知道 Kiasma 博物馆位于赫尔辛基，然后建立那条潜在关联。这不仅测试模型的非词面匹配能力，也测试它的世界知识。NoLiMa 中有 72.4% 的针—问题对需要这类外部知识，这使该基准更接近于同时考察这两项任务，而不只是纯粹的非词面匹配。

单独考察非词面匹配的影响，仍属探索不足。而且，这种「词面」对「非词面」的二元划分，把真实世界问答的复杂度过度简化了。针—问题对处在相似度的一个连续谱上，却都被归入这些宽泛的类别。

模型还常常需要处理干扰项，已有研究表明这会降低表现 [

[11]。](#distractors)

在整份报告中，我们区分干扰项与无关内容：

![](/img/context_rot/niah/distractor_irrelevance.png)

*对比 —— 干扰项 vs. 无关上下文*

- 干扰项在主题上与针相关，但并不真正回答问题
- 无关内容与针及问题都不相关

此前工作已证明干扰项有非均匀影响，但大多数评估只涉及较短输入长度与较老的模型。当前最先进的模型被声称对干扰项更具韧性，但它们在不同输入长度下的表现尚未被广泛测试。

NIAH 另一个探索不足的方面是草堆本身，它往往只被当作放大输入长度的手段，但这假定草堆内容本身对任务表现没有影响。如果模型确实对草堆内容不敏感，那么改变这些内容 —— 例如草堆的主题或叙事流 —— 就不应对结果有任何影响。然而这个假设基本上未被检验。

我们设计了四个受控实验来考察这些因素的影响：

## 针—问题相似度#

我们用 embedding 计算针—问题对之间的余弦相似度。为稳妥起见，我们在五个 embedding 模型上取平均：text-embedding-3-small、text-embedding-3-large、jina-embeddings-v3、voyage-3-large 与 all-MiniLM-L6-v2。我们度量随输入长度增加，模型表现如何受针—问题相似度影响。

## 干扰项的影响#

我们取一个高相似度的针—问题对，写了四个干扰项。我们有以下设置：

- 基线：只有针，无干扰项
- 单个干扰项：针 + 一个随机位置的干扰项
- 多个干扰项：针 + 全部四个干扰项，随机分布

我们测试随输入长度增加干扰项对模型表现的影响，以度量干扰项与输入长度之间的非均匀性。

## 针—草堆相似度#

我们使用两个主题上截然不同的草堆：Paul Graham 的文章与 arXiv 论文 [

[12]，并为各自撰写相应的针。为度量针—草堆相似度，我们把草堆做 embedding，为每根针检索相似度最高的 5 个块，然后对它们的余弦相似度取平均。该过程在五个不同的 embedding 模型上重复，以增强稳健性。](#arxiv)

## 草堆结构#

在典型的 NIAH 设置中，草堆是连贯文本的拼接，每段文本都各自有合乎逻辑的思想流。例如，原始 NIAH 基准使用一系列 Paul Graham 的文章，每篇文章都按结构化的思想组织来构成一个论证。为评估这种结构是否影响模型表现，我们比较两种条件：

- 原始：保留每个节选内部自然的思想流
- 打乱：句子在整个草堆中被随机重排，以保持整体主题相同但逻辑不连贯

我们证明以下结论：

- 在所有实验中，模型表现都随输入长度增加而持续退化。
- 针—问题相似度越低，性能退化的速度越快。
- 干扰项对模型表现的影响是非均匀的 —— 取决于它们彼此之间有多「干扰」。这种影响随输入长度增加更明显，我们也观察到不同模型对它们的反应存在差异。
- 针—草堆相似度对模型表现没有统一的影响，说明需要进一步研究。
- 草堆的结构模式一贯地影响模型处理长输入的方式。

## 细节#

对针类型、草堆主题与草堆结构的每一种独特组合，我们都在以下维度上测试每个模型：

- 8 个输入长度
- 11 个针的位置

我们在每个模型的最大上下文窗口内评估它，temperature=0，除非该设置不兼容（如 o3）或被明确劝阻（如 Qwen 的「思考模式」）。对 Qwen 模型，我们应用 YaRN 方法 [

[13] 从 32,768 扩展到 131,072 token。](#yarn)

在适用的情况下，我们同时包含标准模式与「思考模式」的模型。

我们用对齐过的 GPT-4.1 评判器评估模型输出，所用方法见附录。

我们注意到少数模型拒绝尝试该任务的罕见情形（总计 194,480 次 LLM 调用中有 69 次 —— 0.035%）。例如 Claude Opus 4 有时会输出为空，stop_reason=”refusal”。

## 针—问题相似度#

在真实应用中，模型常被期望处理含糊任务、在不依赖精确词面匹配的情况下找出相关信息。例如，当智能体拿到一个需要在大规模语料中检索的任务时，用户很少会为相关部分指定精确关键词。相反，模型必须自行推断相关性。

我们改变针—问题对的相似度，以其 embedding 的余弦相似度来量化。我们发现，随着针—问题相似度降低，模型表现随输入长度增加而退化得更显著。这反映出更贴近现实的场景：精确的问题—答案匹配很少见，而语义含糊会加剧长输入处理的难度。

## 实验#

我们的草堆内容来自两个领域：Paul Graham 的文章（与原 NIAH 实验一致）与 arXiv 论文。对每个草堆主题（PG 文章、arXiv），我们先确定常见主题，以指导我们撰写问题与针。

我们用聚类来识别给定语料中出现最多的主题：

1. 把文档切成 1-3 句的块

2. 用 text-embedding-3-large 对每个块做 embedding

3. 用 UMAP [
4. [14] 做降维，参数为：n_neighbors=30、min_dist=0.05、n_components=50、random_state=42](#umap)

5. 用 HDBSCAN [
6. [15] 生成聚类，参数为：min_cluster_size=10、min_samples=15](#hdbscan)

7. 用最大边际相关性（MMR）为最大的几个聚类各取 20 个代表性块

8. 人工检查最大的聚类，确定它们的主题与风格

用这种方法，我们识别出「写作建议」是 PG 文章的一个常见主题，且常以轶事形式出现。对 arXiv 论文，我们识别出「信息检索」是常见主题，具体来说是重排序。

我们为每个主题写一个相应的问题：

PG 文章：「我从大学同学那里得到的最好的写作建议是什么？」

arXiv 论文：「科学领域偏好哪种低延迟重排序器？」

*Paul Graham 文章与 arXiv 论文的问题*

写针之前，我们先确认草堆内容中不存在这些问题的答案：

1. 把此前计算好的草堆块 embedding 存入向量数据库。
2. 用我们的问题 embedding 从该向量数据库查询前 10 条结果。
3. 人工检查这些结果，确认它们没有回答给定的问题。

这建立了一个公平的测试环境，因为它确保不存在替代答案，任何错误答案都归因于模型幻觉。

对每个问题，我们写 8 根针，每根都属于那个大聚类（我们用近似预测来验证）。属于写作／检索聚类且概率 >0.9 的针，被视为在主题上融入了草堆。我们手工撰写这些针，以避免数据污染。

对这 8 根针，我们还通过以下方法改变含糊程度：

1. 用一个 embedding 模型，计算针与问题的 embedding 及它们的余弦相似度。
2. 在五个 embedding 模型上重复（text-embedding-3-small、text-embedding-3-large、jina-embeddings-v3、voyage-3-large 与 all-MiniLM-L6-v2）。

对 PG 文章主题，我们的针—问题相似度范围是 0.445-0.775，五个 embedding 模型间的标准差 <0.1。对 arXiv 主题，针—问题相似度范围为 0.521-0.829，标准差同样 <0.1。

## 结果#

我们观察到一个清晰的模式：针—问题相似度越低，表现随输入长度退化得越快。

![](/img/context_rot/longmemeval/needle_question_sim_arxiv.png)

*NIAH：针—问题相似度（同一模型的思考／非思考模式分别对待）—— arXiv 草堆/arXiv 针
 高性能：表现处于前 33%
 蓝色：高相似度针（相似度前 50%）
 红色：低相似度针（相似度后 50%）*

在较短的输入长度下，即使对低相似度对，模型表现也不错。我们在高／中表现的模型上看得最清楚，说明这些模型有能力在**所有**针—问题对上完成这项任务。

在较长输入长度上观察到的性能退化，并非源于针—问题配对本身的内在难度。通过固定针—问题对、只改变无关内容的数量，我们分离出输入规模是表现下降的主要因素。

我们还考察了针的位置是否影响表现。在 11 个针位置上测试，我们发现在这个特定的 NIAH 任务上表现没有明显变化。

## 干扰项的影响#

用较老的模型已经确认，干扰项会降低模型表现，且影响是非均匀的。较新的模型被声称能可靠处理任何干扰项，但随着输入长度增加，这一点还成立吗？

我们的实验揭示：跨模型来看，干扰项的影响及其非均匀性会随输入长度增长而放大，包括最新的最先进模型。我们还观察到不同模型家族在处理含糊性上表现出不同行为。

## 实验#

从每个草堆主题（PG 文章与 arXiv 论文）中，我们取一根针—问题相似度高（八根中第二高）的针，并手工写 4 个干扰项：

问题：「我从大学同学那里得到的最好的写作建议是什么？」

针：「我认为我从大学同学那里得到的最好的写作建议是每周都写。」

干扰项：

- 「我从大学教授那里得到的最好的写作建议是每天都写。」

- 「我从大学同学那里得到的最差的写作建议是把每篇文章用五种不同风格来写。」

- 「我从同学那里得到的最好的写作建议是把每篇文章用三种不同风格来写，那还是高中的时候。」

- 「我原以为我从大学同学那里得到的最好的写作建议是把每篇文章用四种不同风格来写，但现在不这么认为了。」

*Paul Graham 文章主题与高针—问题相似度针所用的干扰项*

我们不是用干扰项测试全部 8 根针，而是用一根针—问题相似度高的针，构造一个「针相对容易识别」的条件。从先前结果可见，由于针—问题相似度高，模型在各类输入长度上对该针表现普遍不错，这让我们能更好地分离并度量干扰项本身的影响。

我们运行三种测试条件：

- 无干扰项（基线）：只有针
- 单个干扰项：针 + 一个干扰项（随机位置）
- 多个干扰项：针 + 全部四个干扰项，随机分布在整个草堆中

![](/img/context_rot/niah/distractors_var.png)

*干扰项的影响 —— 三种条件*

## 结果#

即使只有单个干扰项，表现也相对基线（只有针）下降，而加入四个干扰项会进一步叠加这种退化。

![](/img/context_rot/niah/distractors_num.png)

*干扰项的影响：按干扰项数量的表现 —— arXiv 草堆/PG 文章针*

我们还能看到干扰项的影响并非均匀。例如，在我们的 arXiv 草堆与 PG 文章针的组合中，可以看到第 3 个干扰项（红色）相对其他干扰项造成更大的表现下降。

![](/img/context_rot/niah/distractors_ind.png)

*干扰项的影响：按各干扰项的表现 —— arXiv 草堆/PG 文章针*

为进一步考察这种非均匀影响，我们分析了各模型在「四个干扰项」条件下的失败尝试。对 arXiv 草堆与 PG 文章针的组合，我们看到第 2 与第 3 个干扰项在各模型的幻觉回答中出现得最频繁。

![](/img/context_rot/niah/hallucinations.png)

*干扰项的影响：失败分析 —— arXiv 草堆/PG 文章针*

这些失败还揭示了模型在处理含糊性上的特有差异。Claude 模型一贯表现出最低的幻觉率。具体来说，Claude Sonnet 4 与 Opus 4 尤其保守，在不确定时倾向于弃答，明确表示找不到答案。相比之下，GPT 模型表现出最高的幻觉率，在有干扰项时常常给出自信但错误的回答。

---

## 针—草堆相似度#

在长上下文任务中，无关上下文常被当作中性的占位符来放大输入长度。人们通常假设，只要这些无关内容不直接干扰任务，其内容就不重要。

然而一个自然的问题是：针—草堆相似度究竟会不会影响任务难度？直觉上，如果针与草堆内容融为一体，模型可能更难把针提取出来。

我们的发现揭示：针—草堆相似度对模型表现有非均匀的影响。

## 实验#

使用来自针—问题相似度实验的针，我们设置实验来测试针—草堆相似度的影响。

我们通过把草堆做 embedding、为每根针检索最相似的 5 个块、再对它们的余弦相似度取平均，来度量针—草堆相似度。该过程在五个不同的 embedding 模型上重复，以增强稳健性。

在 PG 文章草堆中，PG 文章针的平均针—草堆相似度为 0.529，波动 0.101，而 arXiv 针平均为 0.368，波动 0.111。反过来说，在 arXiv 草堆中，arXiv 针的平均针—草堆相似度为 0.654，波动 0.0858，而 PG 文章针更低，为 0.394，波动 0.105。

在每个草堆上，我们都用语义相似的针与不相关的针对照测试。例如，我们把 PG 文章针与 arXiv 针都放进一个 Paul Graham 文章草堆中，以比较这两种条件：

![](/img/context_rot/niah/needle_haystack.png)

*针—草堆相似度：实验设置*

## 结果#

我们在两种草堆类型（Paul Graham 文章与 arXiv 论文）中测试 PG 文章针与 arXiv 针。在 Paul Graham 文章草堆中，arXiv 针的表现显著优于 PG 文章针；换句话说，当针**不**与草堆语义融为一体时，模型表现更好。然而在 arXiv 草堆中，我们只观察到 arXiv 针与 PG 文章针之间极小的表现差异。

![](/img/context_rot/niah/needle_haystack_2.png)

*针—草堆相似度结果*

只测试两个主题，不足以得出「更高的针—草堆相似度会降低模型在该任务上表现」这一可推广的结论。但它确实凸显了长上下文处理的非均匀本质。即使任务结构与针—问题相似度保持不变，改变针与草堆之间的语义相似度也能影响结果。这指向长上下文基准中一个探索不足的领域，也是未来研究一个有意义的方​​向。

## 草堆结构#

除针—草堆相似度之外，我们还考虑草堆的结构模式。

如果草堆由连贯的文章构成，那么随机插入的针可能打断思想的逻辑流，从而更容易被注意到。相反，在一个句子随机排序的打乱草堆中，针可能更容易融入，因为整体上下文缺乏结构。这符合「模型对上下文的逻辑流敏感、以结构化且顺序敏感的方式处理它」这个假设。

出人意料的是，我们发现结构连贯性一贯地**损害**模型表现。

虽然看起来反直觉，但当草堆保留思想的逻辑流时，模型表现反而更差。打乱草堆、去除局部连贯性，一贯地改善表现。

## 实验#

为评估草堆结构的影响，我们创建两个变体：

1. 原始：保留每个节选内部自然的思想流
2. 打乱：句子在整个草堆中被随机重排，以保持整体主题相同但没有逻辑连贯性

![](/img/context_rot/niah/nh2.png)

*草堆结构：实验设置样例*

## 结果#

在全部 18 个模型与针—草堆配置上，我们都观察到一贯的模式：模型在打乱草堆上的表现优于逻辑结构化的草堆。

![](/img/context_rot/niah/structure_2.png)

*草堆结构：18 个模型在原始 vs 打乱草堆上的平均表现*

这些结果可能对模型的内部处理有所启示：输入的结构模式可能影响注意力机制如何被施加，尤其是在输入长度增加时。

虽然超出本报告的范围，但这指向可解释性研究的一个潜在方向 —— 注意力如何受输入结构影响。理解这些随输入长度增加而出现的结构性影响，可能有助于解释这些长上下文失败模式。

## LongMemEval#

为在更贴近现实的设置中评估这些模型，我们使用 LongMemEval —— 一个面向对话式问答的长上下文基准。

对聊天助手使用长输入，是维持后续对话相关历史的一种常见做法。要把「记忆」并入聊天助手，一种朴素做法是把完整聊天历史放进后续对话的提示词中。这要求模型完成两项任务，且通常在一次调用中完成：找出对话历史中的相关部分（检索），然后以对当前查询有用的方式综合它们（推理）。

在理想情况下，模型只应拿到相关部分，从而能单纯专注于推理。加入无关上下文增加了「识别什么是相关的」这一步，迫使模型同时执行两项任务。

我们通过两种条件，系统地测试随输入长度增加而加入这一额外步骤的效果：

1. 聚焦输入，只包含相关部分，因此模型只需做简单的推理。

2. 完整输入，使用 LongMemEval 完整的 113k token 输入，其中包含无关上下文。这种情况下，模型除了推理之外，还必须在长上下文中执行检索。

我们确认模型在聚焦输入上能力很强、能成功完成，随后观察到在完整输入上表现一贯退化。这种性能下降说明，加入无关上下文、从而增加一步检索，会显著影响模型维持可靠表现的能力。

## 实验#

给定一段用户与助手之间的聊天历史，模型的任务是回答一个与其中某部分相关的问题。

![](/img/context_rot/longmemeval/ex.png)

*LongMemEval —— 按问题类型的示例 [[2](#longmemeval-source)]*

我们使用 LongMemEval_s，并筛选出属于「知识更新」「时间推理」与「多会话」类别的任务。随后我们手工清洗该数据集，因为有些问题过于含糊和／或无法回答，过滤掉 38 条提示词，最终得到 306 条提示词。这些提示词平均约 113k token。

这些长提示词大多由与问题无关的内容构成，有时还包含看起来可能与问题相关的干扰项。我们把这些长提示词上的模型表现，与一个聚焦版本做比较 —— 后者只包含回答问题所需的相关部分。

聚焦提示词平均约 300 token，来自原标注数据集加上人工调整。

模型输出由对齐过的 LLM 评判器评判（GPT-4.1，与人类判断的对齐度 >99%）。

## 结果#

在所有模型上，我们都看到聚焦提示词的表现显著高于完整提示词。

![](/img/context_rot/longmemeval/claude.png)

*LongMemEval 结果 —— Claude 家族*

Claude 模型在聚焦与完整提示词之间的差距最为显著。这一差异主要来自含糊性引发的弃答，导致模型不确定 —— 与该模型家族在 NIAH 中面对干扰项时的行为类似。这种行为在 Claude Opus 4 与 Sonnet 4 上最明显，它们在含糊情况下似乎格外保守，导致完整提示词上的表现低于更早的 Claude 模型。

问题：从我参加园艺工作坊那天到我种下番茄苗那天，过了多少天？

正确答案：6 天。7 天（含最后一天）也可接受。

模型输出：我无法确定园艺工作坊与种下番茄苗之间相隔多少天，因为聊天历史中没有提供这些事件的具体日期。

*LongMemEval —— Claude Sonnet 4（非思考模式）在包含日期的完整提示词上*

「聚焦提示词表现更强」这一趋势在 GPT、Gemini 与 Qwen 模型家族中同样成立。对支持思考模式的模型，启用后我们在聚焦与完整提示词上都能看到明显收益。然而，即使在最新模型上具备完整推理能力，我们仍然看到两种输入长度之间存在性能差距。

![](/img/context_rot/longmemeval/gpt.png)

*LongMemEval 结果 —— GPT 家族*

![](/img/context_rot/longmemeval/gemini.png)

*LongMemEval 结果 —— Gemini 家族*

![](/img/context_rot/longmemeval/qwen.png)

*LongMemEval 结果 —— Qwen 家族*

我们还在特定问题类型之间观察到模式。在非思考模式下，无论聚焦还是完整提示词，模型总体表现最好的是知识更新，其次是多会话，然后是时间推理。然而启用思考后，这个排序变为：知识更新、时间推理、多会话。

![](/img/context_rot/longmemeval/claude_comparison.png)

*LongMemEval 按问题类型的结果 —— Claude Opus 4*

---

## 重复词#

我们此前的实验探索了**仅输入长度**如何影响模型表现。但当输出长度随输入一起增长时会发生什么？由于这些模型是自回归的，模型的输出也属于它的输入；每个 token 都是条件于输入以及到该点为止已生成的 token 而产生的。

考虑一个把字符串重复 n 次的基本程序 —— 它每次都产生相同输出。对如此简单的任务，我们期望这些模型同样可靠，并希望把它们当作计算系统来对待。

然而，我们的发现表明，即使对这些直白的任务，随着上下文长度（同时包含输入与输出长度）增长，模型表现也会变得不均匀。

## 实验#

我们设计了一个受控任务：模型必须复述一串重复的词，其中在某个特定位置插入了一个独特的词。提示词明确要求模型精确重现输入文本。

一个示例提示词是：

Simply replicate the following text, output the exact same text: apple apple apple apple apples apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple

*重复词 —— 一个样例提示词，重复词是 'apple'，独特词是 'apples'*

对给定的词组合，我们创建 1090 种上下文长度与独特词索引的变化：

- 词数：25、50、75、100、250、500、750、1000、2500、5000、7500、10000
- 索引：
  - num_words <= 100 时取每一个可能位置
  - 否则：以 num_words // 100 为步长

我们对以下词组合执行该任务：

- 常见词："apple" | 独特词："apples"
- 常见词："apples" | 独特词："apple"
- 常见词："golden" | 独特词："Golden"
- 常见词："orange" | 独特词："run"
- 常见词："orange" | 独特词："San Francisco"
- 常见词："San Francisco" | 独特词："sf"
- 常见词："Golden Gate Bridge" | 独特词："Golden Gate Park"

注意："San Francisco" = 1 个词，"Golden Gate Bridge/Park" = 1 个词

模型配置：

- max_output_tokens = input_tokens *2（不超过模型的最大输出 token 上限，较老模型的该上限通常更低）
- temperature = 0
- thinking = max(0, minimum_thinking_budget)

我们通过把推理模型的思考预算设为 0 或最小值（例如 Gemini 2.5 Pro 的 128 token）来处理它们。我们排除 OpenAI 的 o3，因为它不支持基于 token 的思考预算，也无法配置固定输出长度，而后者对保持各次评估的一致性至关重要。

分数用归一化 Levenshtein 距离计算。

我们遇到模型未尝试该任务的情形，判定依据为：

- 输出为空且带停止原因（即 GPT-3.5 turbo 的 finish_reason='content_filter'）

- 输出非空，但输出无效：

- 纯观察、未做尝试：

我注意到文本中有一处不一致。原文中 "apples" 出现了一次（而非 "apple"），位于文本块大约第 89 或 90 行的位置。既然你要求我精确复述同一文本，我应当指出这一差异。你希望我：

1. 完全按所示复述（保留那一处 "apples"）
2. 把它改为 "apple" 以符合模式
3. 直接原样复述 请告诉我你希望我怎么做。

*重复词 —— Claude Opus 4 的输出*

- 拒绝回答：

很抱歉，这个我帮不了。

*重复词 —— GPT-4.1 的输出*

- 随机输出：

-\n-\n--\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-...

*重复词 —— Gemini 2.5 Pro 的输出*

我们排除这类情形，并在结果中单独记录拒绝率与常见模式。我们只纳入尝试了该任务的情形，包括以下面这类开场白开始的情形：

我注意到文本中有一处不一致。在某一处，"apple" 变成了 "apples"（带一个 's'）。我将完全按所提供的内容复述：

apple apple apple apple apple apple apple apple apple...

*重复词 —— Claude Opus 4 的输出*

对这些情形，我们用同样的评分流程，对模型未遵循精确指令略微扣分。

我们完全排除 GPT-3.5 turbo，因为该模型有 60.29% 的任务因 finish_reason='content_filter' 而拒绝生成输出。

我们沿几个维度分析输出：

- 归一化 Levenshtein 距离

- 独特词的存在与位置

  - 正确：独特词存在，且出现在正确索引
  - 位置错误：独特词出现，但索引错误

- 词数差（输入词数 - 生成词数）

## 结果#

随着上下文长度增加，所有模型的表现都持续退化。在这个实验中，输入长度与输出长度直接成比例，不同于我们此前的测试（那时输出长度基本固定在较短水平）。这一设置让我们能评估模型可靠复现长序列的能力。

我们还观察到模型未尝试该任务的模式，这在所有模型家族中都有出现。

![](/img/context_rot/repeated_words/claude_line_plot.png)

*重复词 —— Claude 家族*

我们观察到 Sonnet 3.5（红色）在其 8192 的最大输出 token 数以内，表现优于更新的 Claude 模型。Opus 4（蓝色）虽有最慢的退化速度，但也是该家族中唯一拒绝该任务的模型（占尝试的 2.89%）。

Opus 4 的一个常见模式是：模型先做一次观察，再决定是否继续，随后才是尝试或不做尝试。这种行为通常从 2500 词开始出现。

也有 Opus 4 直接拒绝尝试该任务的情形，原因是：

1. 生成受版权保护材料的风​​险

我无法按要求复述那段确切的文本。虽然它看起来只是重复 "San Francisco"，但当被要求逐字复现文本时，我应当避免这么做，因为这可能被用来测试我是否会在其他情境中复现受版权保护的材料。

不过我可以告诉你，该文本包含 "sf"，后面跟着重复了 24 次的短语 "San Francisco"。

*重复词 —— Claude Opus 4 的输出*

1. 重复序列中的不一致

我注意到你提供的文本中有一处错误。在某一处，"San Francisco" 显示为 "San Francisco sf San Francisco"（中间多了一个 "sf"）。既然你要求我精确复述该文本，我无法提供完美的复述，因为源文本本身包含这一不一致。

该文本由多次重复的 "San Francisco" 构成，但其中嵌入了那一处错误。

*重复词 —— Claude Opus 4 的输出*

我们还度量位置准确率：独特词是否出现在正确位置。当独特词被放在序列靠前的位置时准确率最高，随着输入长度增加尤其如此。

![](/img/context_rot/repeated_words/claude_position_accuracy.png)

*重复词：位置准确率 —— Claude 家族*

此外，随着上下文长度增加，模型常常一直生成重复词直到触达输出 token 上限。我们通过计算输入与输出词数之差来量化这一点：

- 正值 = 模型生成偏少
- 负值 = 模型生成偏多

![](/img/context_rot/repeated_words/claude_num_words.png)

*重复词：词数差 —— Claude 家族*

在 GPT 模型家族中，我们观察到 GPT-4.1 的拒绝率为 2.55%。这些拒绝通常从约 2500 词开始，回应类似「很抱歉，这个我帮不了。」。

![](/img/context_rot/repeated_words/gpt_line_plot.png)

*重复词 —— GPT 家族*

我们还观察到 GPT-4 turbo 在 500 词附近有一个局部性能峰值。在 50 到 250 词之间，模型倾向于生成偏多（把常见词重复到输出上限），但在 500 词时它的词数变得更准确。然而超过这一点后，它开始生成偏少，如输入与输出词数之间的正差值所示。

![](/img/context_rot/repeated_words/gpt_4_turbo.png)

*重复词：词数差 —— GPT-4 Turbo*

位置准确率遵循类似趋势，因为 GPT 模型在独特词出现在输入靠前位置时也更可能把它放对。

我们在这个家族中还注意到更多模型特有行为。

GPT-4.1 mini 会尝试所有任务，但对 "Golden Gate Bridge"/"Golden Gate Park" 组合有时会生成随机词。随机输出定义为输入中不存在的某个词或词序列。

该模型会输出重复词，如 "Golden Golden" 与 "Gate Gate"，这些在输入中并不存在（输入只包含 "Golden Gate Bridge" 与 "Golden Gate Park"）。

这些重复词不出现在独特词的位置，而是出现在文本中更靠后的位置。

GPT-4.1 nano 在 "San Francisco" / "sf" 对上表现出类似行为，偶尔输出小写的 "san"。

模型输出片段：

San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco san Francisco san Francisco san Francisco san Francisco

对应的标准参考答案：

San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco

*重复词 —— GPT-4.1 nano*

对这些随机词，我们注意到与位置有关的结构性线索。我们观察到独特词的位置与随机词开始出现的位置之间存在相关性，这可能是未来研究的一个方向。

GPT-4 Turbo 在这个家族中输出最不稳定，意味着该模型更倾向于生成随机输出，且随机输出的种类更多样。

![](/img/context_rot/repeated_words/gemini_line_plot.png)

*重复词 —— Gemini 家族*

总体而言，我们看到各模型的表现随上下文长度增加而退化。对 Gemini 2.5 Pro（蓝色），我们观察到起点较低，因为在 50 词时，模型生成的词比应有的少。

在这个家族的所有词组合与模型上 —— 除了 "apples"/"apple" 上的 Gemini 2.5 Flash —— 我们都观察到生成了输入中不存在的随机词。这通常从约 500-750 词开始，其中 Gemini 2.5 Pro 波动最大，其次是 2.0 Flash，然后是 2.5 Flash。

"golden" | "Golden"（2,500 词）：

- - "I'-a-le-le-le-le-le-le-'a-le-le-le-le-le-le-le--le-le-le-le-le-le-le...

"orange" | "run"（10,000 词）：

orange orange orange--g.-g/2021/01/20/orange-county-california-sheriff-deputies-wore...

*重复词 —— Gemini 2.5 Pro 的输出样例*

![](/img/context_rot/repeated_words/qwen_line_plot.png)

*重复词 —— Qwen 家族*

我们只在 Qwen3-8B 上观察到未尝试情形，占任务的 4.21%。在该模型上，我们从约 5000 词开始观察到随机输出：

好吧，我要休息一下。跟我说一声，我没心情。我需要放松一下。我要去个地方呼吸点新鲜空气。也许去海滩，或者就找个地方放松。我不知道，但我需要休息一下。跟我说一声，我没心情。我需要放松一下。我要去个地方呼吸点新鲜空气。也许去海滩，或者就找个地方放松。我不知道，但我需要休息一下。跟我说一声，我没心情。我需要放松一下。我要去个地方呼吸点新鲜空气。也许去海滩，或者就找个地方放松。我不知道，但我需要休息一下。跟我说一声，我没心情。我需要放松一下。我要去个地方呼吸点新鲜空气。也许去海滩，或者就找个地方放松。我不知道，但我需要休息一下。跟我说一声，我没心情。我需要放松一下。我要去个地方然后……

*重复词 —— Qwen3-8B 在 'golden' | 'Golden'（5,000 词）上的输出*

## 局限与未来工作#

我们的实验证明，LLM 在不同上下文长度上表现不一致，即使是简单任务也是如此。然而这项评估并未穷尽真实世界的用例。实践中，长上下文应用往往复杂得多，需要综合或多步推理。根据我们的发现，我们预期在这些条件下性能退化会更严重。

我们的结果对长上下文评估的未来工作也有启示。此前长上下文基准的工作也指出过一个常见局限：容易把输入长度与任务难度混为一谈，因为更长的输入往往引入更复杂的推理。我们让实验聚焦于把输入长度作为因素分离出来，并保持任务难度恒定。未来工作的一个重要方向，是厘清模型表现退化中有多少源于任务本身的内在难度、有多少源于它有效处理长上下文的能力。

我们也没有解释这种性能退化背后的机制。我们的观察表明，上下文的结构性质 —— 例如相关信息的位置或重复 —— 能影响模型行为，但我们对其发生原因没有确定答案。考察这些效应需要更深入地研究机制可解释性，这超出本报告的范围。

更广泛地说，我们的发现指向了**上下文工程**的重要性：对模型上下文窗口的精心构建与管理。信息在模型上下文中被呈现的位置与方式，强烈影响任务表现，这使其成为优化模型表现的一个有意义的未来工作方向。

## 结论#

通过我们的实验，我们证明 LLM 在不同输入长度上无法维持一致表现。即使在非词面检索或文本复述这样简单的任务上，我们也看到随输入长度增长而出现的、越来越明显的不均匀性。

我们的结果凸显了超越当前基准、开展更严格的长上下文评估的必要性，以及上下文工程的重要性。相关信息是否存在于模型的上下文中，并不是全部关键；更关键的是这些信息**如何被呈现**。我们证明即使是最有能力的模型也对此敏感，这使有效的上下文工程成为可靠表现的必要条件。

## 脚注#

[1]（2025 年 7 月 16 日）Latent List 相关洞见与澄清由 Kiran Vodrahalli（Google Deepmind）补充

[2] 示例的原始来源：https://arxiv.org/pdf/2410.10813

## 参考文献#

[1] Kamradt, G. (2023). Needle In A Haystack - Pressure Testing LLMs [GitHub Repository].

[Link](https://github.com/gkamradt/LLMTest_NeedleInAHaystack)

[2] Wu, D., Wang, H., Yu, W., Zhang, Y., Chang, K.-W., and Yu, D. (2025). LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory. arXiv preprint arXiv:2410.10813.

[Link](https://arxiv.org/abs/2410.10813)

[3] Gemini Team, Georgiev, P., Lei, V. I., Burnell, R., Bai, L., Gulati, A., Tanzer, G., Vincent, D., Pan, Z., Wang, S., et al. (2024). Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context. arXiv preprint arXiv:2403.05530.

[Link](https://arxiv.org/abs/2403.05530)

[4] OpenAI, Kumar, A., Yu, J., Hallman, J., Pokrass, M., Goucher, A., Ganesh, A., Cheng, B., McKinzie, B., Zhang, B., Koch, C., et al. (2025). Introducing GPT-4.1 in the API.

[Link](https://openai.com/index/gpt-4-1/)

[5] Meta AI, (2025). The Llama 4 herd: The beginning of a new era of natively multimodal AI innovation.

[Link](https://ai.meta.com/blog/llama-4-multimodal-intelligence/)

[6] Modarressi, A., Deilamsalehy, H., Dernoncourt, F., Bui, T., Rossi, R. A., Yoon, S., and Schütze, H. (2025). NoLiMa: Long-Context Evaluation Beyond Literal Matching. arXiv preprint arXiv:2502.05167.

[Link](https://arxiv.org/abs/2502.05167)

[7] Fu, H. Y., Shrivastava, A., Moore, J., West, P., Tan, C., and Holtzman, A. (2025). AbsenceBench: Language Models Can't Tell What's Missing. arXiv preprint arXiv:2506.11440.

[Link](https://arxiv.org/abs/2506.11440)

[8] Vodrahalli, K., Ontanon, S., Tripuraneni, N., Xu, K., Jain, S., Shivanna, R., Hui, J., Dikkala, N., Kazemi, M., Fatemi, B., et al. (2024). Michelangelo: Long Context Evaluations Beyond Haystacks via Latent Structure Queries. arXiv preprint arXiv:2409.12640.

[Link](https://arxiv.org/abs/2409.12640)

[9] openai. (2025). mrcr [Dataset]. Hugging Face.

[Link](https://huggingface.co/datasets/openai/mrcr)

[10] openai. (2025). graphwalks [Dataset]. Hugging Face.

[Link](https://huggingface.co/datasets/openai/graphwalks)

[11] Shi, F., Chen, X., Misra, K., Scales, N., Dohan, D., Chi, E., Schärli, N., and Zhou, D. (2023). Large Language Models Can Be Easily Distracted by Irrelevant Context. arXiv preprint arXiv:2302.00093.

[Link](https://arxiv.org/abs/2302.00093)

[12] jamescalam. (2024). ai-arxiv2 [Dataset]. Hugging Face.

[Link](https://huggingface.co/datasets/jamescalam/ai-arxiv2)

[13] Peng, B., Quesnelle, J., Fan, H., and Shippole, E. (2023). YaRN: Efficient Context Window Extension of Large Language Models. arXiv preprint arXiv:2309.00071.

[Link](https://arxiv.org/abs/2309.00071)

[14] McInnes, L., Healy, J., and Melville, J. (2020). UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction. arXiv preprint arXiv:1802.03426.

[Link](https://arxiv.org/abs/1802.03426)

[15] Campello, R. J. G. B., Moulavi, D., and Sander, J. (2013). Density-Based Clustering Based on Hierarchical Density Estimates. In Pei, J., Tseng, V. S., Cao, L., Motoda, H., and Xu, G. (Eds.), Advances in Knowledge Discovery and Data Mining (PAKDD 2013), Lecture Notes in Computer Science, vol 7819. Springer, Berlin, Heidelberg.

[Link](https://doi.org/10.1007/978-3-642-37456-2_14)

## 附录#

清洗后的 LongMemEval 数据集以及所用的针／干扰项可在此下载

[here.](https://drive.google.com/drive/folders/1FuOysriSotnYasJUbZJzn31SWt85_3yf)

## LLM 评判器对齐：#

我们使用 LLM 评判器来评估 NIAH 与 LongMemEval 实验的输出。这些评判器通过以下流程与人类判断对齐：

1. 人工把一部分模型输出标注为正确／错误（NIAH 约 500 条输出，LongMemEval 约 600 条输出）

2. 用 GPT-4.1 把同一批模型输出标注为正确／错误。

3. 通过计算人类与模型判断一致的比例，得出对齐分数。

4. 根据对不一致情形的人工检查来迭代提示词。

5. 重复步骤 2-4，直到对齐分数 > 0.99。

## 所测试的模型#

由于上下文窗口或 thinking_budget 的限制，并非全部 18 个模型都出现在每个实验中。

### Anthropic#

- Claude Opus 4
- Claude Sonnet 4
- Claude Sonnet 3.7
- Claude Sonnet 3.5
- Claude Haiku 3.5

### OpenAI#

- o3
- GPT-4.1
- GPT-4.1 mini
- GPT-4.1 nano
- GPT-4o
- GPT-4 Turbo
- GPT-3.5 Turbo

### Google#

- Gemini 2.5 Pro
- Gemini 2.5 Flash
- Gemini 2.0 Flash

### Alibaba#

- Qwen3-235B-A22B
- Qwen3-32B
- Qwen3-8B

## 所使用的 Embedding 模型#

- text-embedding-3-small
- text-embedding-3-large
- jina-embeddings-v3 (input_type='text-matching')
- voyage-3-large (input_type=None)
- all-MiniLM-L6-v2

## 针—问题相似度#

注意：同一模型的思考／非思考模式分别对待

![](/img/context_rot/appendix/arxiv_pg_nq_sim.png)

*针—问题相似度 —— arXiv 草堆/PG 文章针*

![](/img/context_rot/appendix/pg_pg_nq_sim.png)

*针—问题相似度 —— PG 文章草堆/PG 文章针*

![](/img/context_rot/appendix/pg_arxiv_nq_sim.png)

*针—问题相似度 —— PG 文章草堆/arXiv 针*

如我们在针—草堆相似度结果中提到的，我们注意到这一个别情形：模型相比其他针—草堆组合表现得异常好。单独看，可能会让人觉得高性能模型的表现是均匀的。然而这些模型的这种均匀性在本报告其余实验中并不成立。

## 干扰项的影响#

![](/img/context_rot/appendix/distractors_num_arxiv.png)

*干扰项的影响：按干扰项数量的表现 —— arXiv 草堆/arXiv 针*

![](/img/context_rot/appendix/distractors_ind_arxiv.png)

*干扰项的影响：按各干扰项的表现 —— arXiv 草堆/arXiv 针*

![](/img/context_rot/appendix/distractors_num_pg.png)

*干扰项的影响：按干扰项数量的表现 —— PG 文章草堆/PG 文章针*

![](/img/context_rot/appendix/distractors_ind_pg.png)

*干扰项的影响：按各干扰项的表现 —— PG 文章草堆/PG 文章针*

![](/img/context_rot/appendix/distractors_num_pg_arxiv.png)

*干扰项的影响：按干扰项数量的表现 —— PG 文章草堆/arXiv 针*

![](/img/context_rot/appendix/distractors_ind_pg_arxiv.png)

*干扰项的影响：按各干扰项的表现 —— PG 文章草堆/arXiv 针*

![](/img/context_rot/appendix/failures_arxiv.png)

*干扰项的影响：失败分析 —— arXiv 草堆/arXiv 针*

![](/img/context_rot/appendix/failures_writing.png)

*干扰项的影响：失败分析 —— PG 文章草堆/PG 文章针*

![](/img/context_rot/appendix/failures_writing_arxiv.png)

*干扰项的影响：失败分析 —— PG 文章草堆/arXiv 针*

## 重复词#

![](/img/context_rot/appendix/gpt_position_accuracy.png)

*重复词：位置准确率 —— GPT 家族*

![](/img/context_rot/appendix/gemini_position_accuracy.png)

*重复词：位置准确率 —— Gemini 家族*

![](/img/context_rot/appendix/qwen_position_accuracy.png)

*重复词：位置准确率 —— Qwen 家族*

![](/img/context_rot/appendix/wc_gpt.png)

*重复词：词数差 —— GPT 家族*

![](/img/context_rot/appendix/wc_gemini.png)

*重复词：词数差 —— Gemini 家族*

![](/img/context_rot/appendix/wc_qwen.png)

*重复词：词数差 —— Qwen 家族*

![Chroma logo](/_next/static/media/chroma-wordmark.0~1c352v-zy35.svg?dpl=dpl_egYxRPRkHPqmMiuZksw8CbEt9xxU)

© 2026

### 产品

[Database](/products/chromadb)

[Sync](/products/sync)

[Enterprise](/enterprise)

[Package Search MCP](/package-search)

[Docs](https://docs.trychroma.com)

[Status](https://status.trychroma.com)

[Contact](mailto:hello@trychroma.com)

### 关注

[GitHub](https://github.com/chroma-core/chroma)

[X](https://x.com/trychroma)

[YouTube](https://www.youtube.com/@trychroma)

### 公司

[About](https://docs.trychroma.com/docs/overview/introduction)

[Changelog](/changelog)

[Careers](/careers)

### 法律

[Privacy](/website-privacy)

[Terms](/website-terms)

[Security](/security)
