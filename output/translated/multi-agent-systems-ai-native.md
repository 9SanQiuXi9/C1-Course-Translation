https://resolve.ai/resources/ebook/practical-guide-for-adopting-ai-agents

超越代码生成：采用 AI 智能体的 4 种工作流

获取这份实用指南

/

![Resolve.ai](/icons/header/logo_long_black.svg)

/contact-us

联系我们

/book-a-demo

立即试用

/book-a-demo

立即试用

![Resolve.ai logo](/icons/logo_no_black.svg)

#### 机器替人类值班

/contact-us

联系我们

##### 加入对话

https://www.linkedin.com/company/resolveai/

![LinkedIn](/icons/LI_green.svg)

https://x.com/resolveai/

![X/Twitter](/icons/X_green.svg)

https://www.youtube.com/@resolve-ai

![YouTube](/icons/YT_green.svg)

©Resolve.ai - 保留所有权利

[服务条款](/terms-of-service)

[隐私政策](/privacy-policy)

[返回博客](/blog)

Technology

# 多智能体系统在让软件工程师成为 AI 原生中的角色

03/20/2026

分享：

https://www.linkedin.com/shareArticle?url=&text=Check+out+this+article%3A+The+role+of+multi+agent+systems+in+making+software+engineers+AI-native&title=The+role+of+multi+agent+systems+in+making+software+engineers+AI-native&summary=Discover+why+most+AI+approaches+like+LLMs+or+individual+AI+agents+fail+in+complex+production+environ...&source=Resolve

https://twitter.com/intent/tweet?url=&text=Check+out+this+article%3A+The+role+of+multi+agent+systems+in+making+software+engineers+AI-native&title=The+role+of+multi+agent+systems+in+making+software+engineers+AI-native&summary=Discover+why+most+AI+approaches+like+LLMs+or+individual+AI+agents+fail+in+complex+production+environ...&source=Resolve

https://www.instagram.com/?url=&text=Check+out+this+article%3A+The+role+of+multi+agent+systems+in+making+software+engineers+AI-native&title=The+role+of+multi+agent+systems+in+making+software+engineers+AI-native&summary=Discover+why+most+AI+approaches+like+LLMs+or+individual+AI+agents+fail+in+complex+production+environ...&source=Resolve

![多智能体系统在让软件工程师成为 AI 原生中的角色](/_next/image?url=https%3A%2F%2Fmedia.website-prod.resolve.ai%2Fcover_company_8b78fef71d.jpg&w=3840&q=75)

生成式 AI 已经如此彻底地改变了

[软件开发，以至于你可以在几小时内搭起整套服务，但要弄清这些服务出了什么问题，仍然需要在割裂的多个工具之间做艰苦的排查。从代码生成到代码审查，编码智能体包办了构建这一侧。但](https://resolve.ai/glossary/what-is-the-future-of-software-engineering)

[生产环境调试呢？那还是手工的。看下面这个例子：](https://resolve.ai/glossary/what-is-debugging)

| 编码 | 生产 |
| --- | --- |
| 写一个服务时：你打开一个 AI 原生的开发环境，让 AI「创建一个处理重试与超时的支付服务」。AI 结合你代码库的上下文，生成带错误处理的实现 | 当同一个服务出现高延迟时：你先提出一个假设 → 查 Datadog 看指标 → 切到 Loki 看日志 → 交叉比对部署历史 → 关联时间戳 →…… 如此继续 |

问题不在于 AI 的能力，而在于我们如何架构 AI 系统。多数工程团队仍是在用 AI 驱动的工具把同样的工作流跑得更快，而没有重新构想软件开发与生产运维应当如何端到端地运转。

在 Resolve AI，我们一直在为工程师构建用于

[生产系统的多智能体系统。我们一直主张工程应当做到 AI 原生（即工程师主要与](https://resolve.ai/glossary/what-are-production-systems-in-software-engineering)

[自主智能体交互来处理生产系统），而软件工程领域大多数关于生成式 AI 的讨论仍集中在用编程助手和编码助手去写 AI 生成的代码。](https://resolve.ai/glossary/what-is-agentic-ai)

我们最近向

[斯坦福的研究生 AI 课程介绍了我们的做法，深入讲解了那些支撑 AI 原生工程工作流的 AI 智能体及其架构模式。](https://www.youtube.com/watch?v=z7RBPQL0rZ4)

#### 什么是 AI 原生工程？为什么它重要？

AI 原生工程指的是工程师主要与 AI 交互来编排自己的工作：无论是写代码还是处理生产系统。AI 原生与仅仅「使用 AI」有显著区别 —— 后者中工程师仍在与自己的系统与工具打交道，只是用 AI 来加速流程中的单个步骤。

下面用一个示例工作流来说明这个区别。

AI 辅助：你使用 AI 工具在复杂任务上工作得更快。工作流仍以人为中心：工程师 → 系统与工具 → 关联 → 行动。
工程师仍在与工具打交道，只是用 AI 更快地完成单个任务

AI 原生：AI 成为你处理生产工作的主要界面。工作流变成 AI 主导：工程师 → 自然语言请求 → AI 系统 → 响应/行动。
工程师设定目标，让 AI 智能体去处理运维工作

![Screenshot 2025-09-25 at 6.05.44 PM.png](/_next/image?url=https%3A%2F%2Fresolve-prod-strapi-bucket.s3.us-east-2.amazonaws.com%2FScreenshot_2025_09_25_at_6_05_44_PM_4cb3a87090.png&w=1920&q=75)

以故障响应为例。在 AI 辅助的工作流里，你仍然要自己提出假设、判断哪些证据重要，并手工在多个工具之间关联信号。AI 在数据检索与分析上帮忙，但调查中的重活还是你在干。

AI 原生的故障响应运作方式不同：AI 智能体会实时分诊调查优先级，并行生成相互竞争的假设，并基于跨系统证据通过连续迭代来修正结论。你不再问「你能分析这些日志吗？」，而是说「解决这个结账失败」，然后由智能体协调整场调查。

这不只是更快。它改变了哪些问题值得投入工程注意力。当 AI 智能体承担日志分析、指标关联与部署时间线重建后，工程师就能在更高的层次上工作，专注于架构决策与系统设计，而不是战术性的排查。

这一转变需要持续的 AI 智能体，而不只是 AI 工具。虽然 OpenAI 或 Anthropic 的模型能加速单个任务，但只有有状态的智能体才能保持调查上下文、跨多个工具协调，并自主执行覆盖整个故障事件生命周期的复杂任务。

#### 为什么多智能体系统对实现 AI 原生工程不可或缺？

现代生产系统呈现出学术界所说的「不可约化的相互依赖」：理解它们需要跨领域的专门知识，而这些知识无法被统一进单一连贯的模型。这正是多数构建者忽略的洞见：没有任何单一 AI 工具或一组 AI 模型，能在协调一场实时调查的同时，对所有这些领域都保持专家级知识。

举例来说：当关键故障期间 API 延迟飙升 10 倍，调查需要多个专门智能体同时进行实时分析：关联 50 多个微服务的调用链、分析慢数据库查询与连接池耗尽、检查近期部署与基础设施变更、扫描认证日志寻找安全异常、对照当前负载模式评估自动扩缩容函数，以及在 SLA 语境下分析支持工单以评估客户影响。这些职能每一项都需要领域专属的专业知识与上下文数据，而没有任何单一系统能有效维持。

在大规模场景下，随着系统复杂度上升，单个 AI 工具缺乏适应能力，无法应对上下文需求的指数级增长。这正是多智能体系统能通过把编排与单个领域专业化结合起来而实现扩展的地方。下这张矩阵为工程负责人提供了概览。找到与你当前状态相符的那一行，理解它的局限：

这个框架揭示了每个层级的技术局限：

| 方式 | 它是什么 | 这种方式在哪里失效 | 局限的成因 |
| --- | --- | --- | --- |
| LLM | 用 LLM（如 ChatGPT）完成解释、分析、写文档等单个任务 | 工程师仍承担大部分运维工作量 | 单次生成容易产生幻觉，且没有反馈回路或与现实系统的集成 |
| LLM + 工具 | AI 可以按指令调用函数，从监控系统取数据 | 关联的认知负担仍在人身上 | 上下文窗口有限，跨工具交互没有持久状态管理 |
| 单智能体 | AI 独立遵循调查工作流 | 顺序调查，卡在错误假设上且没有验证 | 无法管理多样的推理策略或并行的调查路径 |
| 多智能体 | 通过多智能体协作，专门的 AI 智能体协调并行调查，并把各自产出合并成统一诊断 | 需要在协调协议上投入 | 分布式智能需要正式的通信 schema 与冲突解决机制 |

这个演进揭示了一个根本性的架构事实：每个层级都撞上不同的可扩展性天花板。LLM 缺乏持久状态。工具增强的 LLM 无法在多次对话之间保持调查上下文。即使有精密的提示词工程，单智能体也会随着系统复杂度上升而成为决策瓶颈。只有多智能体系统能突破限制此前所有方式的顺序推理约束。它们让并行假设检验成为可能，而单智能体只能顺序调查，这使它们从根本上不适合生产故障事件对时效的要求。

#### 构建多智能体系统是个艰难的工程问题

没有任何现成的智能体框架（如 LangChain）能单独解决这个问题。构建生产就绪的多智能体系统，需要深厚的领域专长与 AI 工程能力这一罕见的组合。多数尝试之所以失败，是因为团队只在一个领域有专长、而非两者兼具。下面说明为什么需要这种双重专长：

- 领域专长决定架构：不理解生产现实，就无法架构智能体。只有在 DevOps 或 SRE 岗位上凌晨三点调试过生产环境的人，才知道日志模式与指标异常需要根本不同的调查策略。当支付失败激增时，你既需要数据库专长、也需要基础设施专长，才能确定根因。这类决策不是 AI 问题。它们是塑造你如何构建多智能体系统的生产决策。
- AI 专长让智能体协同工作：把问题分解完之后，你就撞上了计算机科学中最难的部分。智能体之间的上下文传递不是靠直觉。它要管理信息流的有向无环图，其中每个智能体的输出会喂给下一个智能体的输入。编排并行智能体需要正式的协调协议，以防止竞态条件与死锁。系统需要从交互以及短暂出现的失败模式中持续学习。在协调智能体时错一步，你的系统就会逐渐变差，而不是变好。
- 两者的交汇才催生突破性系统：没有 AI 架构的领域知识只是昂贵的咨询。没有领域知识的 AI 架构，产出的结果会去调查错误的东西。突破发生在你把两者结合起来时：既知道数据库连接池在负载下的行为（领域），又能构建出可以协调连接池健康检查、部署时间线分析与上游服务验证的智能体 —— 所有这些都并行运行而互不干扰（AI 系统）。

在

[Resolve AI，我们的团队包括在生产系统领域有二十多年经验的工程师、共同创造了](https://resolve.ai/product)

[OpenTelemetry（生态中最具影响力的开源可观测性项目之一）的创始人，以及深度人工智能专长的研究者 —— 他们是 Google DeepResearch 与 Gemini Agents 背后的头脑。这种组合让我们构建的系统不只是知道「支付失败是坏事」，还知道要去检查连接池指标并将其与上游服务退化做关联。同时还能管理复杂的智能体编排，防止循环调查，并在多条并行执行路径上保持连贯的叙事线索。](https://resolve.ai/glossary/what-is-opentelemetry)

#### 关于 Resolve AI

Resolve AI 是你全天候在线的

[AI SRE，帮你解决故障事件并运行生产环境。凭借 Resolve AI，Salesforce、](https://resolve.ai/glossary/what-is-ai-sre)

[Zscaler 与](https://resolve.ai/customers/zscaler)

[Coinbase 等客户把机器变成替人类值班的一方、让工程师只管写代码，从而提升了工程效率与系统可靠性。想进一步了解 AI 原生工程工作流，请访问 resolve.ai。](https://resolve.ai/customers/coinbase)

![AI SRE 选型指南](/_next/image?url=https%3A%2F%2Fmedia.website-prod.resolve.ai%2F2025_SRE_Buyers_Guide_v3_page_1_d82558c4da.jpg&w=384&q=75)

#### AI SRE 选型指南

了解如何在生产环境中评估并采用 AI SRE。

https://resolve.ai/resources/ebook/ai-sre-buyers-guide

下载

![](/icons/arrow-right.svg)

![Spiros Xanthos 的头像](/_next/image?url=https%3A%2F%2Fmedia.website-prod.resolve.ai%2Fspiros_5982fae7f6.png&w=3840&q=75)

Spiros Xanthos

创始人兼 CEO

Spiros 是 Resolve AI 的创始人兼 CEO。他喜欢向客户学习并动手构建。他曾协助创建 OpenTelemetry，并创办了 Log Insight（被 VMware 收购）与 Omnition（被 Splunk 收购），最近担任 Splunk 可观测性业务的高级副总裁兼总经理。

https://www.linkedin.com/in/spiros/

https://x.com/spirosx

![Gabor Angeli 的头像](/_next/image?url=https%3A%2F%2Fmedia.website-prod.resolve.ai%2FGabor_Angeli_6c414bda98.jpeg&w=3840&q=75)

Gabor Angeli

研究工程师

Gabor Angeli 拥有丰富的人工智能专长，近期任职于 Google DeepMind 与 Square。他参与的产品如 Gemini 与 Square Assistant 每天触达数百万用户。他加入 Resolve AI，是为了构建帮助工程师理解并驾驭生产系统的智能体式 AI 系统。

https://www.linkedin.com/in/gabor-angeli-468ab6a/

![Bharat Khandelwal 的头像](/_next/image?url=https%3A%2F%2Fmedia.website-prod.resolve.ai%2Fbharat_7c0eaf3af0.jpeg&w=3840&q=75)

Bharat Khandelwal

研究工程师

@ Resolve AI

Bharat 是 Resolve AI 的研究工程师，在那里构建让大型语言模型能够调试并运维生产软件基础设施的智能体系统。加入 Resolve 之前，他在 WorldQuant 主导机器学习项目，设计用于宏观经济预测的基于 Transformer 的架构，并将来自非结构化数据的 LLM 驱动情绪信号纳入其中。他还曾在 Moveworks 从事企业级 NLP 系统，并在 Tower Research Capital 开发用于高频交易的低延迟机器学习策略。Bharat 拥有斯坦福大学计算机科学硕士学位（人工智能方向），以及 IIT 孟买计算机科学荣誉学士学位。

https://www.linkedin.com/in/khandelwalbharat/

![content title icon](/icons/star.svg)

- Content

#### 面向生产的 AI 电子书

了解顶尖工程团队如何用 AI 运行生产环境。

https://resolve.ai/resources/ebook/ai-for-production-systems

下载

![](/icons/arrow-right.svg)

![Spiros Xanthos 的头像](/_next/image?url=https%3A%2F%2Fmedia.website-prod.resolve.ai%2Fspiros_5982fae7f6.png&w=3840&q=75)

Spiros Xanthos

创始人兼 CEO

Spiros 是 Resolve AI 的创始人兼 CEO。他喜欢向客户学习并动手构建。他曾协助创建 OpenTelemetry，并创办了 Log Insight（被 VMware 收购）与 Omnition（被 Splunk 收购），最近担任 Splunk 可观测性业务的高级副总裁兼总经理。

https://www.linkedin.com/in/spiros/

https://x.com/spirosx

![Gabor Angeli 的头像](/_next/image?url=https%3A%2F%2Fmedia.website-prod.resolve.ai%2FGabor_Angeli_6c414bda98.jpeg&w=3840&q=75)

Gabor Angeli

研究工程师

Gabor Angeli 拥有丰富的人工智能专长，近期任职于 Google DeepMind 与 Square。他参与的产品如 Gemini 与 Square Assistant 每天触达数百万用户。他加入 Resolve AI，是为了构建帮助工程师理解并驾驭生产系统的智能体式 AI 系统。

https://www.linkedin.com/in/gabor-angeli-468ab6a/

![Bharat Khandelwal 的头像](/_next/image?url=https%3A%2F%2Fmedia.website-prod.resolve.ai%2Fbharat_7c0eaf3af0.jpeg&w=3840&q=75)

Bharat Khandelwal

研究工程师

@ Resolve AI

Bharat 是 Resolve AI 的研究工程师，在那里构建让大型语言模型能够调试并运维生产软件基础设施的智能体系统。加入 Resolve 之前，他在 WorldQuant 主导机器学习项目，设计用于宏观经济预测的基于 Transformer 的架构，并将来自非结构化数据的 LLM 驱动情绪信号纳入其中。他还曾在 Moveworks 从事企业级 NLP 系统，并在 Tower Research Capital 开发用于高频交易的低延迟机器学习策略。Bharat 拥有斯坦福大学计算机科学硕士学位（人工智能方向），以及 IIT 孟买计算机科学荣誉学士学位。

https://www.linkedin.com/in/khandelwalbharat/

![lead-title-icon](/icons/misc/cross.svg)

#### 相关文章

/blog/webinar-finserv-fireside-chat-eng-execs

![炉边谈话：金融科技公司如何用 AI 优化生产环境成本](/_next/image?url=https%3A%2F%2Fmedia.website-prod.resolve.ai%2FScreenshot_2026_01_22_at_5_08_21_PM_d4fc734373.png&w=3840&q=75)

#### 炉边谈话：金融科技公司如何用 AI 优化生产环境成本

聆听来自 Affirm、MSCI、SoFi 等金融科技公司工程负责人的 AI 策略与方法。

/blog/how-to-evaluate-an-ai-sre

![如何评估一个生产就绪的 AI SRE](/_next/image?url=https%3A%2F%2Fmedia.website-prod.resolve.ai%2FEval_Criteria_Blog_Banner_2_d0d49bd3b4.jpg&w=3840&q=75)

Technology

#### 如何评估一个生产就绪的 AI SRE

了解如何评估一个 AI SRE，以确保它能在你独特的生产环境中运行。本指南阐释了五大智能体支柱、六个关键评估维度，以及区分「生产就绪的 AI SRE」与「实验品」的企业级就绪标准。

/blog/Beyond-the-Build-Accelerating-Engineering-Velocity-with-Agentic-AI

![Beyond the Build：用智能体式 AI 加速工程效率](/_next/image?url=https%3A%2F%2Fmedia.website-prod.resolve.ai%2FBTB_Blog_Header_984d9acd09.png&w=3840&q=75)

#### Beyond the Build：用智能体式 AI 加速工程效率

100 位软件工程高管与 Resolve AI 及其他杰出领导者齐聚一堂，讨论智能体式 AI 在软件工程中从编码到管理生产系统的加速演进。
