# 翻译留痕：ai-assisted-code-review-assessment

- doc_id：`ai-assisted-code-review-assessment`
- 时间：2026-09-27T17:18:57+08:00
- 原文：`extracted/ai-assisted-code-review-assessment.md`
- 译文：`translated/ai-assisted-code-review-assessment.md`
- 原文 sha256：`4e2b55c5a729bdc5288388eb5b47f05ad95b994f9a78d15394d1a73ec28f0287`
- 译文 sha256：`0d556db35b18ecfaa467bd3896118a8b438227c0b7a1407491c85fb845e31692`
- 术语约束条数：28

## 一、本文档涉及的术语清单

| 英文 | 译法 | handling | 出现次数 |
|---|---|---|---|
| `code review` | 代码审查 | `translate` | 41 |
| `model` | 模型 | `translate` | 39 |
| `evaluation` | 评估 | `translate` | 23 |
| `best practices` | 最佳实践 | `translate` | 19 |
| `training` | 训练 | `translate` | 19 |
| `ide` | IDE | `acronym` | 14 |
| `deployment` | 部署 | `translate` | 13 |
| `dataset` | 数据集 | `translate` | 12 |
| `static analysis` | 静态分析 | `translate` | 7 |
| `codebase` | 代码库 | `translate` | 6 |
| `context` | 上下文 | `translate` | 5 |
| `latency` | 延迟 | `translate` | 5 |
| `tool` | 工具 | `translate` | 4 |
| `monitoring` | 监控 | `translate` | 4 |
| `workflow` | 工作流 | `translate` | 3 |
| `automation` | 自动化 | `translate` | 3 |
| `repository` | 仓库 | `translate` | 3 |
| `machine learning` | 机器学习 | `translate` | 3 |
| `pipeline` | 流水线 | `translate` | 3 |
| `inference` | 推理 | `translate` | 3 |
| `prompt` | 提示词 | `translate` | 2 |
| `llm` | LLM | `acronym` | 2 |
| `fine-tuning` | 微调 | `translate` | 2 |
| `context window` | 上下文窗口 | `translate` | 1 |
| `span` | 跨度 | `translate` | 1 |
| `eval` | 评估 | `translate` | 1 |
| `transformer` | Transformer | `keep_en` | 1 |
| `rollout` | 灰度发布 | `translate` | 1 |

## 二、落盘校验结果

```json
{
  "non_empty": true,
  "code_blocks_total": 0,
  "code_blocks_in_translation": 0,
  "code_blocks_match": true,
  "code_blocks_byte_identical": true,
  "urls_orig": 16,
  "urls_trans": 17,
  "urls_all_present": true,
  "urls_counts_equal": false,
  "urls_notes": [
    "译文多出 URL（未计入失败，需人工确认）：['https://go.dev/doc/comment#func`']"
  ],
  "headings_orig": 1,
  "headings_trans": 1,
  "headings_match": true,
  "orig_chars": 44509,
  "trans_chars": 21557,
  "length_ratio": 0.4843,
  "length_ratio_ok": true
}
```

## 四、发出的 prompt 全文

```markdown
(未找到 prompt 导出文件)
```

## 五、AI 返回的译文全文

```markdown
# 现代代码审查中 AI 辅助的编码实践评估

现代代码审查中 AI 辅助的编码实践评估

Manushree Vijayvergiya

manushree@google.com

Google

Zurich, Switzerland

Małgorzata Salawa

magorzata@google.com

Google

Zurich, Switzerland

Ivan Budiselić

ibudiselic@google.com

Google

Zurich, Switzerland

Dan Zheng

danielzheng@google.com

Google

Mountain View, USA

Pascal Lamblin

lamblinp@google.com

Google

Montreal, Canada

Marko Ivanković

markoi@google.com

Google

Zurich, Switzerland

Juanjo Carin

juanjocarin@google.com

Google

Sunnyvale, USA

Mateusz Lewko

mlewko@google.com

Google

Zurich, Switzerland

Jovan Andonov

jandonov@google.com

Google

Zurich, Switzerland

Goran Petrovićgoranpetrovic@google.comGoogle

Zurich, Switzerland

Daniel Tarlow

dtarlow@google.com

Google

Montreal, Canada

Petros Maniatis

maniatis@google.com

Google

Mountain View, USA

René Just

∗

rjust@cs.washington.edu

University of Washington

Seattle, USA

摘要

现代代码审查是一个过程：代码作者提交的增量代码贡献，在被提交进版本控制系统之前，会由一位或多位同行审查。现代代码审查的一个重要环节，是核实代码贡献是否遵循最佳实践。其中一些最佳实践可以自动核实，但另一些通常留给人来审查。本文报告了 AutoCommenter 的开发、部署与评估 —— 这是一个由大型语言模型支撑、能自动学习并强制执行编码最佳实践的系统。我们为四种编程语言（C++、Java、Python 与 Go）实现了 AutoCommenter，并在一个大型工业环境中评估了它的表现与采纳情况。我们的评估表明，一个用于学习并强制执行编码最佳实践的端到端系统是可行的，并且对开发者工作流有正面影响。此外，本文还报告了把这样一个系统部署给数万名开发者所面临的挑战，以及相应的经验教训。

CCS 概念•软件及其工程→软件验证与确认

∗ 工作完成于 Google。

允许为个人或课堂用途免费制作本作品全部或部分的数字或硬拷贝，前提是不得为营利或商业优势而制作或分发副本，且副本须带有本声明与首页的完整引用。本作品中第三方组件的版权必须予以尊重。其他用途请联系作者/所有者。

AIware '24, July 15–16, 2024, Porto de Galinhas, Brazil

©

2024 版权归作者/所有者持有。

ACM ISBN 979-8-4007-0685-1/24/07

https://doi.org/10.1145/3664646.3665664

关键词

人工智能、代码审查、编码最佳实践

ACM 引用格式：

Manushree Vijayvergiya, Małgorzata Salawa, Ivan Budiselić, Dan Zheng, Pascal Lamblin, Marko Ivanković, Juanjo Carin, Mateusz Lewko, Jovan Andonov, Goran Petrović, Daniel Tarlow, Petros Maniatis, and René Just. 2024. AI-Assisted Assessment of Coding Practices in Modern Code Review. In Proceedings of the 1st ACM International Conference on AI-Powered Software (AIware '24), July 15–16, 2024, Porto de Galinhas, Brazil. ACM, New York, NY, USA, 9 pages. https://doi.org/10.1145/3664646.3665664

1 引言

现代代码审查 [21,23] 多年来在开源与工业环境中自然成长起来。一套常见的同行评审准则已经形成 [5,20,21]，甚至编程语言也以「风格指南」的形式正式定义了它们 [1-4]：

• 格式：行长限制、空白与缩进的使用、圆括号与方括号的位置等；

• 命名：大小写、简洁性、描述性等；

• 文档：文件级、函数级及其他注释的预期位置与内容；

• 语言特性：在不同（代码）语境下使用特定语言特性；

• 代码惯例：使用代码惯例来提升代码的清晰性、模块化与可维护性。

开发者普遍对现代代码审查流程表示高度满意 [23,28]，但对不熟悉该代码库、特定语言特性或常见代码惯例的代码作者来说，这一体验可能颇具挑战。在审查过程中，资深开发者除了审查（并了解）代码贡献及其影响之外，还会就最佳实践对代码作者进行指导。

像 linter 这类静态分析工具 [15] 可以核实代码是否遵循某些最佳实践（例如格式规则），有些工具甚至能自动修复违规。然而，那些细微的、或带例外的准则难以被完整自动核实（例如命名约定，以及遗留代码中有正当理由的偏离），还有些准则根本无法用精确规则来捕捉（例如代码注释的清晰度与具体性），得依赖人的判断与开发者的集体知识。因此，通常期望由人类审查者来检查代码改动是否违反最佳实践。

代码审查流程最大的成本是所需的时间，尤其是资深开发者的时间。即使已有大量自动化、且流程尽可能轻量，一位开发者也很容易每天在这件事上投入数小时 [23]。

机器学习的最新进展 —— 尤其是大型语言模型（LLM）的能力 —— 表明 LLM 适合用于代码审查自动化（例如 [11,16,17,24-26]）。然而，围绕大规模部署端到端系统的软件工程挑战仍未被探索。同样，这类系统在整体效能与用户接受度上的外部评估也尚付阙如。

本文研究是否可能部分地自动化代码审查流程，具体来说是检测最佳实践违规，从而为代码作者提供及时反馈，让审查者能专注于整体功能。具体而言，本文报告我们在 Google 的工业环境中开发、部署与评估 AutoCommenter —— 一个自动化代码审查助手 —— 的经验，它目前每天被数万名开发者使用。

总之，本文的贡献是：

• 一个基于 LLM 的代码审查助手系统的通用架构（第 3 节）。

• 工具校准与部署给数万名开发者的描述（第 4 节）。

• 对该系统的评估（第 5 节）。

• 经验教训的总结与讨论（第 6 节）。

2 背景

AutoCommenter 是在 Google 的大型工业环境中开发的。Google 的现代代码审查实践与其他工业及开源项目类似 [23]。

2.1 代码审查流程

Google 的代码审查流程成熟、以变更为基础、并由工具辅助。Ivanković 等人 [12] 与 Petrović 等人 [18] 对该流程做了详细总结。对代码库的每一次变更都必须由至少一位其他开发者审查。每天有数万次代码库变更走这个审查流程，数万名开发者以代码作者与审查者两种身份参与其中。作者与审查者通过代码审查系统交换评论，一次审查会经历该变更所涉文件的多个快照。每条审查者评论都附着在特定文件快照中的特定行与列范围上。为解决一条评论，作者通常会在本地副本中修改该文件，并导出一个新快照用于下一轮代码审查。当作者与所有审查者都满意、且没有任何自动化分析阻止合并时，代码就被合并进代码库。

代码审查流程中最昂贵的部分，是代码作者与审查者「护送」一次变更所花的时间（从最初编码，到处理审查者评论、确保所有自动化分析通过，到最终把变更合并进代码库）。虽然该流程已通过自动化系统在审查前分析代码（尤其是无需人工干预的自动代码格式化）得到优化，代码审查每年仍耗费数千个开发者年。因此，即使只有个位数百分比的节省，也能转化为可观的业务影响。

2.2 最佳实践

**最佳实践**是指编程语言中某种被认为更优的具体用法，而**最佳实践文档**描述它应如何应用、带来什么好处。**最佳实践 URL** 指某份最佳实践文档或其中某个具体小节，**最佳实践违规**指某段代码未遵循某项最佳实践、但可以被改成遵循它。若上下文清楚，我们用**URL**与**违规**分别指代最佳实践 URL 与最佳实践违规。

Google 的中心代码仓库包含多种语言的代码，其中 C++、Java、Python 与 Go 各自都超过 1 亿行 [19]。这些语言大多还有额外的语言入门材料、核心库文档，以及「每周小贴士」式的通讯。虽然这些材料的强制力不如风格指南，但它们在代码审查中被频繁引用。有些语言的这类文档多达数百页。代码作者与审查者都被期望核实代码遵循所有最佳实践。

十多年前引入的一项名为「readability」的正式机制，确保最佳实践被一致地遵循。某种语言中专门的风格专家被称为「readability 导师」，他们引导经验不足的开发者达到该语言的熟练水平 [23]。readability 导师会用几句话说明某项最佳实践，并在评论末尾附上一条 URL 供变更作者参考。图 1 展示了 readability 导师所发评论的一个例子。

readability 流程有一些缺点。对作者来说，由于额外的审查轮次，它增加了开发时间。对 readability 导师来说，它可能变成一件单调且耗时的工作。它要求掌握数百条不断演进的最佳实践，包括识别并废弃过时规则，并把它们（连同相关链接）记录在代码审查系统中。此外，它还要求跟踪、有时要经过多轮迭代，确保所有违规都已被纠正。

3 方法

针对 2.1 与 2.2 节所述的挑战，我们开发了 AutoCommenter —— 一个自动检测最佳实践违规的代码分析工具。它的目标是为代码作者提供及时反馈，并减轻人工最佳实践审查的负担，从而让审查者专注于代码功能。

3.1 模型与任务定义

自动化最佳实践分析需要一个能表示源代码、精确指出违规位置、并识别所违反最佳实践的模型。我们以基于 T5 的传统 transformer 方法、使用 T5X [22] 来做文本到文本的转换。最佳实践分析是一个多任务大序列模型中的一项任务。除 T5 的标准预训练任务（span 去噪，即预测被遮蔽的 token）之外，用于训练该模型的其他任务还包括代码审查评论解决、下一次编辑预测、变量重命名与构建错误修复 [9]。训练语料超过 30 亿个样本，其中最佳实践分析数据集贡献约 80 万个样本。模型用此类模型标准的交叉熵损失训练，并以最大化序列准确率（对每个样本预测出确切的目标文本）为调优目标。

对最佳实践分析而言，模型的**输入**是一个任务提示词加上源代码，**目标**是一处源代码位置与一条最佳实践违规的 URL。任务提示词以固定文本的代码注释形式编写，使用该编程语言恰当的注释风格。它以自然语言描述任务，并置于源代码之前，而源代码是某一个文件的直接文本表示。如果输入超出模型上下文窗口，就会被截断。位置是源代码中的一个字节偏移量，URL 指向所违反的最佳实践。一种领域特定语言定义了目标格式，其中一种特殊情况是「空」目标 —— 即不存在任何违规。除目标之外，模型还会输出一个置信度分数，用于评分的排序与过滤，即开发者接受度。

图 1 展示了输入与目标的一个例子（Go 代码）：

/ / [ ∗
/ / Package addition provides Add
package addition
/ / Return a sum
func Add ( value1 , value2 int ) int {
return value1 + value2
}

目标

`INSERT 1 5 3 COMMENT https://go.dev/doc/comment#func`

输入的第一行是固定文本的任务提示词；其余是源代码。目标给出了位置（字节偏移 153 对应 `Add` 函数的起始处）以及一条 go.dev 的 URL，指向该函数注释所违反的 Go 语言风格指南的确切部分（在这个案例里，是「注释应以函数名开头」这一通常做法）。注意目标可能包含零个、一个或多个（拼接的）位置—URL 对，取决于源代码中有多少处违规。

3.2 模型训练

图 2 展示了模型训练流水线的架构，它由三部分组成。我们把数据集创建拆成两步（预处理与整理），因为第一步由于处理的数据量大得多而显著更昂贵。预处理步骤的输出与模型的输入/目标表示无关。这种分离提升了特性迭代速度，因为它让示例表示与其他示例层面的调整能快速迭代。预处理步骤使用一个容错调度系统，并周期性地提取相关代码评论，以确保新数据随时可用。

3.2.1 大规模预处理。训练样本由真实代码审查数据创建，但并非所有代码评论都适合用于模型训练。因此预处理步骤会识别出**相关代码评论** —— 即含有一条指向最佳实践文档的 URL 的人工撰写评论。对每条评论，预处理步骤随后收集相应源代码与相关元数据，包括该评论在源代码中的位置及其创建时间。该步骤的输出是一组相关代码评论，每条都带有为模型训练整理样本所需的所有数据。

3.2.2 数据集整理。数据集整理是一个单一的按需处理步骤，以 Beam 流水线实现。它依据 3.1 节所述的输入/目标格式，把每条相关代码评论转换成标准的 TensorFlow Example 数据结构。

3.2.3 训练与微调。整理后的样本直接用于模型训练与评估。我们使用 T5X 框架 [22]，训练 1000 步，并用 Tensorboard 监控训练。

3.3 模型选择

在历史数据上的两项内在评估，为我们的模型检查点选择、置信度阈值与解码策略提供了依据。第一，在验证与测试数据集上的评估给出按文件粒度的精确率与召回率估计。第二，在完整历史代码审查上的评估给出每次代码审查的评论总数估计，表明开发者与 AutoCommenter 交互的频率。

3.3.1 在验证与测试数据集上评估。我们对数据集做时间上的切分，以确保模型没有在验证与测试数据集里那些代码评论的未来代码审查快照上训练过。在我们的数据集中，85% 的文件正好有一条相关代码评论，11% 有两条，4% 有三条或更多。我们把一次预测定义为**正确**，当且仅当预测的代码位置与 URL 与期望值匹配（不计顺序）。

回顾一下，模型会为每条预测给出置信度分数，这引入了另一个参数：如果某条预测的置信度分数低于某个阈值 *t*，它可以被抑制。我们定义 *Precision_t* 为置信度分数大于 *t* 的正确预测数除以置信度分数大于 *t* 的全部预测数；*Recall_t* 的定义类似。这些定义让我们能估计作为 *t* 的函数，会有多少（不）正确结果被展示给用户。*Precision_t* 与 *Recall_t* 用于训练期间的模型检查点比较。

虽然这种评估避免了数据泄漏、让我们能自动评估模型表现，但它有一个局限：虽然可以合理假定给定代码审查快照上的人工评论是正确的，它们却并不穷尽。换句话说，某个代码审查快照中的代码可能依据多项最佳实践都有改进空间，但人类审查者并未为所有这些问题都留下（带 URL 的）评论。这可能出于几个原因：

• 缺少引用：审查者可能就某个问题做了评论，但没有附上 URL 作为引用。

• 有选择地评论：审查者可能只就该问题评论一次，期望作者在整个项目中都一并修复。

• 专长或关注点不同：审查者可能并不熟悉所有最佳实践，或者只是在某次代码审查的语境下选择不就某个问题评论（例如只关注被改动的代码）。

虽然我们数据集中大多数文件只有一条相关评论，但基于人工检查「不正确」预测的轶事证据表明，由于上述原因，通常可能存在多条最佳实践评论。鉴于我们的标准答案数据并不完整，我们的精确率与召回率度量是有噪声的。

因此，我们采用下面描述的一项互补评估，以提升对模型整体表现的信心。

1

https://beam.apache.org/Therefore, we employ a complementary evaluation, described next, to increase confidence in overall model performance.

3.3.2 在完整历史代码审查上评估。为准确估计线上环境中的潜在评论量，我们用某个特定的模型检查点与阈值，在一组历史代码审查上评估 AutoCommenter。预测出的评论不会追溯性地发布到代码审查系统中，而是记入数据库以供分析。这让我们能估计预期的发布频率 —— 在按文件与按代码审查两种粒度上。由于开发者是与 AutoCommenter 就受代码审查的整组代码改动进行交互，这一评估是投产前的重要一步。额外的好处是，这一步还允许我们进一步优化，并评估不同用户群、编程语言等的发布频率。

3.4 推理基础设施

AutoCommenter 的核心是一个中心化的最佳实践分析服务。该服务接受一个或多个待分析的源文件作为输入。对每个文件，它构造一次模型输入（3.1 节），把它编码成标准的 TensorFlow Example 数据结构，并查询模型。模型本身由一个模型服务提供，该服务使用 TensorFlow 的 Example 数据结构作为与领域无关的输入输出格式。最后，最佳实践分析服务执行一系列过滤步骤（第 4 节），抑制低质量预测，并返回其余预测。

3.5 IDE 与代码审查集成

开发者通过两种方式与 AutoCommenter 的分析服务交互 —— 直接通过 IDE 插件，或间接通过代码审查系统。代码审查系统被 Google 所有开发者使用，IDE 则被其中几乎所有人使用。

AutoCommenter 的评论在 IDE 中以蓝色波浪下划线标注的诊断形式出现，覆盖相关代码片段。把鼠标悬停在下划线代码上，会显示完整评论，其中包含对该最佳实践的简要概括，以及一个可点击的链接指向相关最佳实践文档。这些内嵌信息免去了开发者在遇到不熟悉的最佳实践时在 IDE 与浏览器之间切换的麻烦，从而理顺了工作流。由于 IDE 中的评论需要实时生成，我们力求做到亚秒级延迟。

在代码审查系统中，AutoCommenter 在每次更新后（即每个新的代码审查快照）运行，一旦检测到违规就自动发布评论。自动工具产出的评论在视觉上与人类评论相似，但背景色不同。图 3 展示了 AutoCommenter 在代码审查系统中生成并发布的一条示例评论。注意右侧的点赞与点踩按钮，作者与审查者若觉得某条评论特别有用或没用可以点击。还要注意左侧对审查者可见的「请修复」按钮。如果点击它，就会生成一条新评论，表明该审查者认为这条评论很重要、必须在该代码合并进代码库之前处理。这些反馈按钮在代码审查系统中是标准配置，出现在自动工具生成的所有评论上（例如 [7,13]），用于衡量接受度。IDE 也提供了类似的反馈机制。

4 部署

我们在 2022 年 7 月至 2023 年 10 月这段时间内，把 AutoCommenter 部署给了 Google 所有开发者：

• 至 2022 年 7 月 —— **团队内部试用（teamfooding）**：即本文作者。

• 2022 年 7 月 —— **早期采用者**：约 3000 名志愿者。

• 2023 年 7 月 —— **A/B 实验**：约一半的开发者。

• 2023 年 10 月起 —— **正式可用**：所有开发者。

注意，出于工业保密原因，我们无法披露代码审查、开发者、文件、评论的绝对数量，或代码审查时长的分布。我们在适当之处报告相对指标与相关趋势。

我们用迭代式精炼的方法持续评估并改进 AutoCommenter 的表现：

• 在历史数据上评估（3.3 节），以获得关于模型在该任务上表现如何的方向性洞见，并据此定义阈值、选择解码策略。

• 通过反馈按钮与 issue 报告，监控并分析用户交互与直接反馈。

• 基于其他评估步骤中观察到的模式，做有针对性的人工评估。

图 4 展示了随时间变化，开发者对所发布代码审查评论与 IDE 诊断的正负反馈之比。虚线表示开发者每月提供的反馈点击总数。如预期那样，这个计数在早期采用者阶段低得多。此外，这一阶段的波动更大，因为我们在积极精炼 AutoCommenter。

回顾代码审查系统里的三个反馈按钮（图 3），它们让开发者能对某条已发布评论表达正面或负面态度。我们把带点赞或「请修复」的评论视为正面，把带点踩的评论视为负面；我们定义**有用率（useful ratio）**为正面评论数占所有有反馈评论数的比例。

本节余下部分描述部署期间我们做出的具体观察与相应改进。

4.1 选择阈值与解码策略

4.1.1 阈值。在初始部署期间，我们想谨慎管理开发者对 AutoCommenter 的信任，因此从一个很高的置信度阈值 *t* = 0.98 开始。我们人工抽样了几百条结果，观察到约 80% 低于该阈值的预测其实仍是正确的 —— 也就是说，在 *t* = 0.98 时假阴率非常高。此外，我们观察到 Python 的预测呈现出显著不同的置信度分数分布，受到阈值化的影响不成比例地大。我们推测训练数据集的构成（不同 URL 的数量与 URL 频率）以及最佳实践文档的具体性是原因，但把更深入的调查留给未来工作。尝试部署按语言划分的阈值被证明无效 —— 每种语言一个阈值仍然无法充分体现模型正确预测数百条不同最佳实践的能力。这导致预测出的 URL 缺乏多样性，因为无论正确与否，模型倾向于对某些 URL 给出更高分数。这些观察引出了对 AutoCommenter 的第一项重大改动：基于验证数据集上的内在评估计算出**按 URL 划分的阈值**。

4.1.2 解码。在完整历史代码审查上使用按 URL 阈值加贪心解码的评估显示，AutoCommenter 在 6% 的已改动文件中检测到违规。然而，其中 80% 的评论会被发布在作者未修改的代码行上。开发者通常不会对未改动的代码采取行动。因此，AutoCommenter 会过滤掉针对未改动代码行生成的评论，把已改动文件中的评论比例降到 1.3%。为提升这一比例，我们试验了不同的解码策略：贪心（默认）、束搜索、top-k 与 top-p 采样。我们最终选定束搜索（生成 *n* = 4 个候选响应），它把发布频率提升到三倍，达到 3.9%。它还带来了显著更高的 URL 多样性：发布最频繁的 10 个 URL 占全部评论的 41%，而贪心搜索下这一比例为 80%。

在为部署选择解码策略时，延迟是另一个重要方面。虽然束搜索提升了发布频率与多样性，推理却明显变慢（中位延迟 2 秒）。考虑到这一延迟对 IDE 中的交互式使用而言无法接受，我们最终决定在代码审查系统中使用束搜索，在 IDE 中使用贪心搜索。

4.2 抑制过时最佳实践

在把 AutoCommenter 发布给约 3000 名自愿的早期采用者之后，我们注意到几天内用户提交了大量 issue。其中许多对应同一条 URL —— 该 URL 描述与 Python 导入相关的最佳实践。然而，某些类型名的规范来源在 Python 3.9 中已改变，该最佳实践也在 2022 年初发生了变化。由于我们的训练数据延伸到 2022 年之前，它包含了不少已不再适用的最佳实践评论。我们意识到这是一个反复出现的模式：随着语言演进、新库被引入，最佳实践也在演进。缓解该问题的一种方式是过滤掉这类数据（每当规则变化时）并重新训练模型。但这耗费时间与资源：它需要完整重新生成数据、重新训练模型、评估与发布。在此期间，「过时」的模型要么得关掉（造成系统停机），要么得抑制受影响的预测。否则，系统可能很快失去开发者的信任。我们选择用条件过滤（对源代码匹配正则表达式）来抑制特定的最佳实践预测，原因有二。第一，它可以动态部署并立即生效。第二，它允许对预测做细粒度的过滤。

4.3 对选定评论的独立评分

在数月早期使用之后，我们观察到有用率在约 54% 处趋于平缓。为理解原因、找出改进空间并为更广泛的部署做准备，我们在 2023 年 4 月开展了一项独立的人工评分研究，分析了约 370 条在早期采用者部署阶段收到开发者反馈的已发布评论。

为收集关于评论有用性的多元视角，我们招募了 15 位评分者 —— 来自合作团队的开发者。我们请他们对收到明确用户反馈的 AutoCommenter 评论进行评分。我们没有向评分者展示原始用户反馈，以避免其评估产生偏差。评分者依据所链接的最佳实践与周边代码来评估每条评论的有用性。我们要求他们聚焦于评论的正确性，但同时也要判断该评论作为作者对他们而言是否可操作（例如，一条技术上正确、但在具体场景下似乎不值得解决的评论，他们会去解决吗）。我们鼓励他们为每条评论提供自由形式的反馈。

评分者评估给出的有用率为 60%，略高于同一批评论上来自开发者反馈的 54%，但远低于我们为更广泛部署设定的 80% 目标。

这项研究最有趣的发现是，无用的评论存在清晰的模式。以下是一些例子：

**涉及多个主题或复杂主题**：例如，有一条 URL 指向某个小节，该小节描述了与 Python linter 交互的多条准则，包括它经常触发的场景以及抑制它的方法。作者可能难以理解所发布的评论究竟指的是哪条具体准则、以及如何解决它。类似地，C++ 中关于编写良好函数文档的指南是满满一页密集的文字。评分者经常指出，最佳实践（以及 AutoCommenter 的简要概括）与实际代码之间存在脱节，即使代码确实包含相关违规。

**高质量概括的重要性**：评分者常常发现，AutoCommenter 的概括（由抓取文档源生成、有时缺失）未能充分解释所引用准则与评论/代码之间的相关性。

**主观且可能引发争议的主题**：一个例子是避免在库代码中使用 flag。在库中使用 flag 可能造成问题，但有些库恰恰被设计成通过 flag 配置许多特性。此外，遗留代码可能不遵循该准则，审查者也不会强制执行它。模型没有学到这些细微之处，有时会在作者向既有库添加新 flag 时预测出违规。

**某些准则上的系统性模型错误**：一个有意思的例子是一条鼓励对 C++ vector 优先使用成员函数 `push_back` 而非 `emplace_back` 的准则 —— 当两个函数用相同参数能达到相同效果时。模型已学会预测这一点，但它也会在 `emplace_back` 更合适的情况下预测，以及当某个不相关的类型恰好有一个名为 `push_back` 的成员函数时预测。

**正确但低价值的评论**：代码注释中句子末尾缺一个句号，人类审查者往往是允许的。虽然技术上正确，但要求作者回到 IDE 去修这个问题，净价值可能是负的。

2

https://github.com/google/styleguide/blob/gh-pages/pyguide.md#22-importsImportance of high-quality summaries:Raters often found that AutoCommenter's summary, which was generated by scraping the document source and sometimes missing, failed to adequately explain the relevance of the cited guideline to the comment/code.

评分研究的洞见促成了对 AutoCommenter 的两项改动。第一，评分研究识别出 17 条不可操作的 URL，抑制它们使历史有用率在开发者反馈上从 54% 提升到 66%，在评分者反馈上从 60% 提升到 74%。我们进一步分析了与类似但未被评分的 URL 相关联的评论，又抑制了 5 条。第二，我们审查并人工更新了所有频繁发布的 URL 的概括。这些改动合起来，足以达到我们为下一阶段部署设定的 80% 有用率目标。

4.4 A/B 实验

2023 年 7 月，我们在一次 A/B 实验的框架下把 AutoCommenter 部署给约一半的开发者。我们把开发者随机分配到实验组（启用 AutoCommenter）与对照组（禁用 AutoCommenter）。我们依据开发者邮箱 SHA256 哈希的最后几位来做随机化，并核实两组在规模与构成上没有差异，包括任职时长、职级、编程语言与业务单元的分布。我们还确认实验开始前、实验中测量的任何变量在对照组与实验组之间都没有差异。实验期间的评论发布频率与预期一致（4.1 节）。

我们没有在以下任何一项上检测到统计上显著的变化：代码审查总时长、开发者在代码审查上实际投入的时间、作者与审查者之间的评论—回应迭代次数。但我们的确检测到编码速度有轻微提升。我们推测，前往文档的上下文切换减少带来了这一正面效果。更深入的调查留给未来工作。基于这些结果，我们得出结论：没有负面影响，并于 2023 年 10 月把 AutoCommenter 部署给所有开发者。

5 评估

基于 2023 年 3 月以来收集的有用率与用户反馈，我们得出结论：开发者总体对 AutoCommenter 产出的评论是满意的。我们通过分析用户反馈，持续精炼数据集准备、阈值、URL 抑制与概括，以确保 AutoCommenter 对开发者工作流带来高度的正面影响。

除开发者满意度之外，在向 Google 全体广泛发布数月之后，我们还评估了 AutoCommenter 表现的另外三个方面：

（1）评论解决：开发者有多经常修改代码来解决 AutoCommenter 发布的评论？

（2）AutoCommenter 与人类评论对比：AutoCommenter 的评论在多大程度上覆盖了人类审查者在评论中引用的最佳实践文档？

（3）AutoCommenter 与 linter 对比：AutoCommenter 的输出在多大程度上超出了传统静态分析工具的能力？

5.1 评论解决

开发者很少通过点击代码审查系统与 IDE 中的点赞/点踩按钮、以及代码审查系统中的「请修复」按钮（图 3）来为 AutoCommenter 的评论给出**明确反馈**：代码审查系统中约 10% 的自动评论、IDE 中 2% 的诊断收到了明确反馈，这与 Google 其他自动化分析的情况相当。与此同时，开发者会悬停查看约 50% 的 AutoCommenter IDE 诊断，而此前工作表明开发者常常在未给出明确反馈的情况下就解决了自动评论 [18]。为估计 AutoCommenter 评论的解决率，我们做了一次离线分析，估计被后续代码改动解决掉的评论比例。

为分析评论解决情况，我们提取了来自 AutoCommenter 的、带自动评论的文件在历史上的改动。对每一次改动，我们提取发布该评论时的初始快照，以及开发者最终合并进代码库的快照。每条评论覆盖一个特定的行范围。我们使用一种基于 AST 的自动化行映射方法 [18] 来对齐这两个快照，从而识别出模型在初始快照上预测过、但在合并快照上不再预测的评论。这样的快照对表明该评论可能已被解决，但也可能是不相关的代码改动导致某条评论不再被预测。

对 6000 对快照的自动分析显示，50% 的情况下该评论在其最初发布的行上已不存在于提交的快照中。我们人工检查了 40 对这样的快照的随机样本。我们发现，80% 的情况下，作者所做的一处改动直接解决了所发布评论描述的问题。因此，我们估计评论解决率约为 40%，显著高于有明确正面反馈的评论占全部评论的比例。

5.2 AutoCommenter 与人类评论对比

图 5 比较了 AutoCommenter 在生产中生成的自动评论、与训练数据中人类评论（按指向最佳实践文档的唯一 URL）的累计分布。横轴是当所有在自动评论中出现过的 URL 按频率排序时该 URL 的排名。例如，最频繁使用的 URL 排名为 1，它占所有自动评论的 9.9%。同一个 URL 出现在训练数据中人类创建评论的 4.3% 里。总体而言，AutoCommenter 为 330 个不同的 URL 生成过评论。AutoCommenter 所使用的 URL 集合覆盖了带最佳实践 URL 的历史人类评论的 68%。这是个好结果：它表明 AutoCommenter 并未聚焦于审查者极少引用的冷门最佳实践。另一方面，尽管使用了束搜索，URL 多样性仍然相对较低。排名前 85 的 URL 占了 AutoCommenter 创建评论的 90%。同一组 URL 覆盖了带最佳实践 URL 的人类评论的 35%。

5.3 AutoCommenter 与 linter 对比

为理解 AutoCommenter 在多大程度上提供了超越 linter（它们能高效、精确地检查某些最佳实践）的价值，我们抽样了预测最频繁的前 50 项违规 —— 即图 5 中排名前 50 的 URL。对每个抽样的 URL，我们查阅其最佳实践文档并判定：(1) 最佳实践类型（第 1 节）；(2) 是否存在能检测相应违规的 linter，或能否轻易构建一个。具体而言，三位各自拥有 10 年以上构建静态分析工具经验的作者阅读了这些文档，并独立地对 URL 分类。在最佳实践类型上没有分歧，但在约 15% 的 URL 上，对于「能否轻易构建 linter」存在分歧。三位作者通过多数表决与讨论解决了这些分歧。分歧源于最佳实践本身含糊，以及那些包含多条准则的情况。例如，检查代码文档是否存在相对直接，但对有正当理由的例外以及内容清晰度做推理则未必。图 6 展示了 50 个抽样 URL 的分布，按类型以及违规能否被 linter 检测来划分。对其中 33/50（66%）的最佳实践而言，违规检测超出了传统静态分析的范围。

6 经验教训

基于我们开发与部署 AutoCommenter 的经验，我们总结出几条关键教训：

• **补充传统分析**：AutoCommenter 由 LLM 支撑的方法，为人类审查者频繁引用的 68% 的最佳实践生成了评论。其中许多超出传统静态分析的范围。

• **内在评估 vs. 现实表现**：内在评估与现实表现可能显著背离：我们的内在评估 —— 使用真实世界人类评论构成的数据集、加上最先进的模型架构与训练流程 —— 显示模型很有前景，但我们的外部评估与系统改进对成功部署而言被证明是不可或缺的。

• **监控用户接受度至关重要**：即使只有少数负面用户体验，也会侵蚀对一个自动系统的信任。持续监控并分析真实世界反馈，对发现这类情况并找出补救办法至关重要。在 AutoCommenter 的案例中，一个简单的抑制机制就足以把用户接受度强力提升到 80% 以上，而无需在效能上做出重大牺牲。

7 相关工作

Johnson [15] 指出，在 linter 出现后的 50 年里，关于自动化静态分析产生了相当多的研究成果：Heckman 与 Williams [10] 近期的文献综述总结了开发人员如何与静态分析交互。Johnson 等人 [14] 探讨了开发者在使用静态分析时面临的挑战。他们的研究结果凸显了良好集成进既有开发者工作流的重要性，以及建立并维护对工具信任的重要性。Vassallo 等人 [27] 探讨了开发者如何在编码与代码审查等不同语境下与静态分析交互。他们同样发现，集成进既有工作流对开发者是否愿意使用这些工具起主要作用，且结果的高质量极为重要。Beller 等人 [6] 研究了大量开源项目中静态代码分析的使用情况。除其他发现之外，他们强调自动化分析如何被使用、以及应当如何被使用，会因编程语言而异。

相比之下，用机器学习做代码分析是一个相对较新、理解较少的领域。近期有不少公开论文（例如 Hong 等人 [11]、Li 等人 [16]、Li 等人 [17]、Thongtanunam 等人 [24]、Tufano 等人 [25]、以及 Tufano 等人 [26]）报告了模型评估并提出了自动化代码审查工具。虽然这些模型与审查评论生成任务与本文提出的模型非常相似，但评估大多聚焦于历史数据集。正如 3.3.1 节所讨论的，仅基于历史评论的内在评估有一定局限，有时无法预测现实表现。Frömmgen 等人 [9] 近期的一篇论文提出了一个线上系统的评估，但做的是相反的任务：从评论生成代码，而不是从代码生成评论。

8 结论

核实代码遵循最佳实践，是现代代码审查流程中的常见任务。虽然有些最佳实践可以用 linter 这类传统工具自动核实，但许多需要资深开发者的知识与判断，这需要时间与精力。

本文报告了我们开发、部署与评估 AutoCommenter —— 一个由 LLM 支撑的代码审查助手系统 —— 的经验。具体而言，它梳理了从任务与模型设计、到内在评估与系统校准、再到分阶段发布与终端用户评估的整个过程。

评估结果表明，开发一个能力远超传统工具、同时实现高度终端用户接受度的端到端系统是可行的。这些结果是为部署精密代码审查助手与自动化代码审查迈出的有前景的第一步。

我们的优先事项是通过把 AutoCommenter 设计成具有极高精确率，来确保良好的开发者体验。虽然召回率不是首要关注点，我们仍认识到它的重要性，并计划探索模型与系统架构上哪些改动能提升召回率。例如，我们在 2022 年使用的模型在当时是最先进的。然而它的上下文窗口只有 2048 个 token，仅够约 200 行代码。当前最先进的模型在训练时上下文窗口达数万 token、推理时超过 100 万 token。这一跃升为新增功能、以及显著改进既有功能打开了机会。

9 致谢

这项工作源于 Google Core Systems 与 Google DeepMind 各团队多年协作的成果。我们感谢所有团队成员与领导的支持与建议，包括 Alberto Elizondo、Alexander Frömmgen、Ballie Sandhu、Chandu Thekkath、Chris Gorgolewski、David Tattersall、Ilya Cherny、Jacob Austin、Katja Grünwedel、Kristóf Molnár、Lera Kharatyan、Luka Rimanic、Madhura Dudhgaonkar、Marc Brockschmidt、Marcus Revaj、Maxim Tabachnyk、Nina Chen、Niranjan Tulpule、Nitya Ramani、Paige Bailey、Pavel Sychev、Pierre-Antoine Manzagol、Quinn Madison、Roger Fleig、Satish Chandra、Savinee Dancs、Stoyan Nikolov、Subhodeep Moitra 与 Vaibhav Tulsyan。

参考文献

2024. Google Style Guides. https://google.github.io/styleguide/. Accessed: 2024-03-15.

2024. Linux kernel coding style. https://www.kernel.org/doc/html/v4.10/process/coding-style.html. Accessed: 2024-03-15.

2024. PEP 8 – Style Guide for Python Code. https://peps.python.org/pep-0008/.Accessed: 2024-03-15.

2024. Rust Style Guide. https://doc.rust-lang.org/nightly/style-guide/. Accessed: 2024-03-15.

Alberto Bacchelli and Christian Bird. 2013. Expectations, outcomes, and challenges of modern code review. In 2013 35th International Conference on Software Engineering (ICSE). 712–721. https://doi.org/10.1109/ICSE.2013.6606617

Moritz Beller, Radjino Bholanath, Shane McIntosh, and Andy Zaidman. 2016. Analyzing the state of static analysis: A large-scale evaluation in open source software. In 2016 IEEE 23rd International Conference on Software Analysis, Evolution, and Reengineering (SANER), Vol. 1. IEEE, 470–481.

Zimin Chen, Małgorzata Salawa, Manushree Vijayvergiya, Goran Petrović, Marko Ivanković, and René Just. 2023. MuRS: Mutant Ranking and Suppression using Identifier Templates. In Proceedings of the Symposium on the Foundations of Software Engineering (FSE). 1798–1808.

M. E. Fagan. 1976. Design and code inspections to reduce errors in program development. IBM Systems Journal 15, 3 (1976), 182–211. https://doi.org/10.1147/sj.153.0182

Alexander Frömmgen, Jacob Austin, Peter Choy, Nimesh Ghelani, Lera Kharatyan, Gabriela Surita, Elena Khrapko, Pascal Lamblin, Pierre-Antoine Manzagol, Marcus Revaj, Maxim Tabachnyk, Daniel Tarlow, Kevin Villela, Daniel Zheng, Satish Chandra, and Petros Maniatis. 2024. Resolving Code Review Comments with Machine Learning. In International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP).

Sarah Heckman and Laurie Williams. 2011. A systematic literature review of actionable alert identification techniques for automated static code analysis. Information and Software Technology 53, 4 (2011), 363–387. https://doi.org/10.1016/j.infsof.2010.12.007 Special section: Software Engineering track of the 24th Annual Symposium on Applied Computing.

Yang Hong, Chakkrit Tantithamthavorn, Patanamon Thongtanunam, and Aldeida Aleti. 2022. Commentfinder: a simpler, faster, more accurate code review comments recommendation. In Proceedings of the Joint Meeting of the European Software Engineering Conference and the Symposium on the Foundations of Software Engineering (ESEC/FSE). 507–519.

Marko Ivanković, Goran Petrović, René Just, and Gordon Fraser. 2019. Code Coverage at Google. In Proceedings of the Joint Meeting of the European Software Engineering Conference and the Symposium on the Foundations of Software Engineering (ESEC/FSE). 955–963.

Marko Ivanković, Goran Petrović, Yana Kulizhskaya, Mateusz Lewko, Luka Kalinovčić, René Just, and Gordon Fraser. 2024. Productive Coverage: Improving the Actionability of Code Coverage. In International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP).

Brittany Johnson, Yoonki Song, Emerson Murphy-Hill, and Robert Bowdidge. 2013. Why don't software developers use static analysis tools to find bugs?. In 2013 35th International Conference on Software Engineering (ICSE). IEEE, 672–681.

Stephen C Johnson. 1977. Lint, a C program checker. Bell Telephone Laboratories Murray Hill.

Lingwei Li, Li Yang, Huaxi Jiang, Jun Yan, Tiejian Luo, Zihan Hua, Geng Liang, and Chun Zuo. 2022. Auger: Automatically generating review comments with pre-training models. In Proceedings of the Joint Meeting of the European Software Engineering Conference and the Symposium on the Foundations of Software Engineering (ESEC/FSE). 1009–1021.

Zhiyu Li, Shuai Lu, Daya Guo, Nan Duan, Shailesh Jannu, Grant Jenks, Deep Majumder, Jared Green, Alexey Svyatkovskiy, Shengyu Fu, and Neel Sundaresan. 2022. Automating code review activities by large-scale pre-training. In Proceedings of the 30th ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering (ESEC/FSE 2022). Association for Computing Machinery, New York, NY, USA, 1035–1047. https://doi.org/10.1145/3540250.3549081

Goran Petrović, Marko Ivanković, Gordon Fraser, and René Just. 2023. Please fix this mutant: How do developers resolve mutants surfaced during code review?. In International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP). 150–161.

Rachel Potvin and Josh Levenberg. 2016. Why Google Stores Billions of Lines of Code in a Single Repository. Communications of the ACM (CACM) 59 (2016), 78–87. http://dl.acm.org/citation.cfm?id=2854146

Peter Rigby, Brendan Cleary, Frederic Painchaud, Margaret-Anne Storey, and Daniel German. 2012. Contemporary Peer Review in Action: Lessons from Open Source Development. IEEE Software 29, 6 (2012), 56–61. https://doi.org/10.1109/MS.2012.24

Peter C. Rigby and Christian Bird. 2013. Convergent contemporary software peer review practices. In Proceedings of the 2013 9th Joint Meeting on Foundations of Software Engineering (Saint Petersburg, Russia) (ESEC/FSE 2013). Association for Computing Machinery, New York, NY, USA, 202–212. https://doi.org/10.1145/2491411.2491444

Adam Roberts, Hyung Won Chung, Gaurav Mishra, Anselm Levskaya, James Bradbury, Daniel Andor, Sharan Narang, Brian Lester, Colin Gaffney, Afroz Mohiuddin, et al. 2023. Scaling up models and data with t5x and seqio. Journal of Machine Learning Research 24, 377 (2023), 1–8.

Caitlin Sadowski, Emma Söderberg, Luke Church, Michal Sipko, and Alberto Bacchelli. 2018. Modern Code Review: A Case Study at Google. In International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP). 181–190.

Patanamon Thongtanunam, Chanathip Pornprasit, and Chakkrit Tantithamthavorn. 2022. Autotransform: Automated code transformation to support modern code review process. In Proceedings of the International Conference on Software Engineering (ICSE). 237–248.

Rosalia Tufano, Ozren Dabić, Antonio Mastropaolo, Matteo Ciniselli, and Gabriele Bavota. 2024. Code Review Automation: Strengths and Weaknesses of the State of the Art. IEEE Transactions on Software Engineering (TSE) (2024).

Rosalia Tufano, Simone Masiero, Antonio Mastropaolo, Luca Pascarella, Denys Poshyvanyk, and Gabriele Bavota. 2022. Using pre-trained models to boost code review automation. In Proceedings of the International Conference on Software Engineering (ICSE). 2291–2302.

Carmine Vassallo, Sebastiano Panichella, Fabio Palomba, Sebastian Proksch, Harald C Gall, and Andy Zaidman. 2020. How developers engage with static analysis tools in different contexts. Empirical Software Engineering 25 (2020), 1419–1457.

T. Winters, T. Manshreck, and H. Wright. 2020. Software Engineering at Google: Lessons Learned from Programming Over Time. O'Reilly Media. https://books.google.ch/books?id=TyIrywEACAAJ

收稿 2024-04-05；录用 2024-05-04

训练与微调（按需）

Worker

Worker

Workers

源代码
仓库

评论
存储

Scheduler

相关
代码
评论

Worker

Worker

Workers

Examples
（按时间
切分）

Worker

Worker

TPU pods

Tensorboard

模型
检查点

输入/目标
格式

大规模预处理（周期性）

数据集整理（按需）

代码惯例

文档

格式

语言

命名

0

5

10

不同 URL 的数量

Linter

是 否/部分

```
