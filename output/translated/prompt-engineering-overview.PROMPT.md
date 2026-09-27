# 翻译留痕：prompt-engineering-overview

- doc_id：`prompt-engineering-overview`
- 时间：2026-09-27T17:23:44+08:00
- 原文：`extracted/prompt-engineering-overview.md`
- 译文：`translated/prompt-engineering-overview.md`
- 原文 sha256：`110e3582ae74fb837db29fbcf7dadfa65a24ae14358b00cfa08afc9964db42a3`
- 译文 sha256：`82e9bf8755fd921797c357718631e8db4f0c28b858447e1bc28ad74b8ddb0ab6`
- 术语约束条数：37

## 一、本文档涉及的术语清单

| 英文 | 译法 | handling | 出现次数 |
|---|---|---|---|
| `security` | 安全 | `translate` | 84 |
| `prompt` | 提示词 | `translate` | 77 |
| `api` | API | `acronym` | 27 |
| `model` | 模型 | `translate` | 21 |
| `context` | 上下文 | `translate` | 18 |
| `prompt engineering` | 提示词工程 | `translate` | 18 |
| `observability` | 可观测性 | `translate` | 12 |
| `server` | 服务器 | `translate` | 10 |
| `automation` | 自动化 | `translate` | 9 |
| `monitoring` | 监控 | `translate` | 9 |
| `reasoning` | 推理 | `translate` | 8 |
| `artifact` | 产物 | `translate` | 8 |
| `best practices` | 最佳实践 | `translate` | 7 |
| `machine learning` | 机器学习 | `translate` | 7 |
| `compliance` | 合规 | `translate` | 7 |
| `deployment` | 部署 | `translate` | 6 |
| `sre` | SRE | `acronym` | 5 |
| `incident` | 故障事件 | `translate` | 5 |
| `agent` | 智能体 | `translate` | 4 |
| `agentic` | 智能体式 | `translate` | 4 |
| `workflow` | 工作流 | `translate` | 4 |
| `orchestration` | 编排 | `translate` | 4 |
| `latency` | 延迟 | `translate` | 4 |
| `zero-shot` | 零样本 | `translate` | 4 |
| `ide` | IDE | `acronym` | 3 |
| `chain of thought` | 思维链 | `translate` | 3 |
| `training` | 训练 | `translate` | 2 |
| `debugging` | 调试 | `translate` | 2 |
| `incident response` | 故障响应 | `translate` | 2 |
| `fine-tuning` | 微调 | `translate` | 2 |
| `deep learning` | 深度学习 | `translate` | 2 |
| `tool` | 工具 | `translate` | 1 |
| `tracing` | 链路追踪 | `translate` | 1 |
| `repository` | 仓库 | `translate` | 1 |
| `ci/cd` | CI/CD | `acronym` | 1 |
| `multimodal` | 多模态 | `translate` | 1 |
| `few-shot` | 少样本 | `translate` | 1 |

## 二、落盘校验结果

```json
{
  "non_empty": true,
  "code_blocks_total": 0,
  "code_blocks_in_translation": 0,
  "code_blocks_match": true,
  "code_blocks_byte_identical": true,
  "urls_orig": 764,
  "urls_trans": 758,
  "urls_all_present": true,
  "urls_counts_equal": false,
  "headings_orig": 35,
  "headings_trans": 35,
  "headings_match": true,
  "orig_chars": 86709,
  "trans_chars": 61837,
  "length_ratio": 0.7132,
  "length_ratio_ok": true
}
```

## 四、发出的 prompt 全文

```markdown
(未找到 prompt 导出文件)
```

## 五、AI 返回的译文全文

```markdown
# 提示词工程：总览与指南

最后更新：01/14/2026

大型语言模型（LLM）的兴起为人类与计算机的交互带来了令人兴奋的可能性。然而，要充分发挥这些强大 AI 模型的潜力，需要一项关键技能：提示词工程。这个新兴领域专注于精心设计有效的提示词，以释放

[LLM 的能力，让它们能理解意图、遵循指令并生成期望的输出。随着我们在各种应用中越来越多地与 AI 交互，提示词工程在确保准确、相关且安全的交互方面发挥着关键作用。](https://cloud.google.com/ai/llms)

免费开始使用

https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/generative

试用聊天提示词

https://console.cloud.google.com/?walkthrough_id=vertex-ai--chat&utm_source=cgc-site&utm_medium=et&utm_campaign=FY25-Q2-global-discover-qs&utm_content=what-is-prompt-engineering&utm_term=-

https://www.youtube.com/watch?v=RywP7cCYUWE

![prompt engineer](https://www.gstatic.com/bricks/image/MUr6Af94qU6gNwxBGhqRbRtFxnQEWtGi3kRcV9hPlNLT-YkIjpO1aD_HriuhwwzR0OilQTK8m497.png)

1:53

成为世界级提示词工程师的技巧

### 什么是提示词工程？

提示词工程是设计与优化提示词的艺术与科学，用以引导 AI 模型（尤其是 LLM）生成期望的回答。通过精心设计提示词，你为模型提供上下文、指令与示例，帮助它理解你的意图并以有意义的方式回应。可以把它想象成为 AI 提供一张路线图，把它引向你心中那个具体的输出。

要深入了解提示词设计的世界、探索它的应用，请看

[Google Cloud 上的《提示词设计导论》。](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/introduction-prompt-design)

准备好亲手试用 LLM 与提示词工程了吗？试用

[Vertex AI 免费试用版，体验这项技术的力量。](https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/)

### 什么是给 AI 的提示词？

在

[AI 的语境下，提示词就是你提供给模型的输入，用以引出特定的回答。它可以有多种形式，从简单的问题或关键词，到复杂的指令、代码片段，甚至创意写作样本。提示词的有效性直接影响 AI 输出的质量与相关性。](https://cloud.google.com/learn/what-is-artificial-intelligence)

### 提示词工程需要什么？

有几个关键要素有助于做好提示词工程。掌握它们，你就能与 AI 模型有效沟通、释放其全部潜力。

#### 提示词格式

提示词的结构与风格在引导 AI 回应上起着重要作用。不同模型可能对特定格式反应更好，例如：

提示词的格式在 AI 如何解读你的请求上起着重要作用。不同模型可能对特定格式反应更好，例如

[自然语言提问、直接命令，或带特定字段的结构化输入。理解模型的能力与偏好格式，是设计有效提示词的必要前提。](https://cloud.google.com/learn/what-is-natural-language-processing)

#### 上下文与示例

在提示词中提供上下文与相关示例，能帮助 AI 理解期望的任务，并生成更准确、更相关的输出。例如，如果你想要一个创意故事，在提示词里加几句描述期望的语气或主题，就能显著改善结果。

#### 微调与适配

用量身定制的提示词在特定任务或领域上微调 AI 模型，可以提升其表现。此外，根据用户反馈或模型输出调整提示词，也能随时间进一步改善模型的回答。

#### 多轮对话

为多轮对话设计提示词，让用户能与 AI 模型进行连续、具上下文感知的交互，从而提升整体用户体验。

### 提示词的类型

AI 中使用的提示词有各种类型，各服务于特定目的：

#### 直接提示词（零样本）

零样本提示是给模型一个直接的指令或问题，不附加任何上下文或示例。

一个例子是想法生成：提示模型生成创意想法或头脑风暴方案。另一个例子是摘要或翻译：要求模型总结或翻译某段内容。

#### 单样本、少样本与多样本提示词

这种方法是在给出实际提示词之前，先给模型一个或多个期望的输入—输出对示例。这能帮助模型更好地理解任务，并生成更准确的回答。

#### 思维链提示词

CoT 提示鼓励模型把复杂推理拆解成一系列中间步骤，从而得到更全面、结构更清晰的最终输出。

#### 零样本 CoT 提示词

把思维链提示与零样本提示结合起来，要求模型执行推理步骤，这往往能产出更好的输出。

### 提示词工程的用例与示例

以下是一些具体示例与用例，展示提示词工程如何帮助产出定制化、相关的输出。

#### 语言与文本生成

场景

说明

示例提示词

创意写作

设计提示词，指明体裁、语气、风格与情节要点，引导 AI 生成引人入胜的叙事。

"Write a short story about a young woman who discovers a magical portal in her attic."

摘要

把文本交给 AI，并要求它生成抓住关键信息的简洁摘要。

"Summarize the main points of the following news article on climate change."

翻译

指明源语言与目标语言，让 AI 在保留含义与上下文的前提下准确翻译。

"Translate the following text from English to Spanish: 'The quick brown fox jumps over the lazy dog.'"

对话

设计模拟对话的提示词，让 AI 生成模仿人类互动并保持上下文的回答。

"You are a friendly chatbot helping users troubleshoot their computer problems. Respond to the user's query: 'My computer won't turn on.'"

场景

说明

示例提示词

创意写作

设计提示词，指明体裁、语气、风格与情节要点，引导 AI 生成引人入胜的叙事。

"Write a short story about a young woman who discovers a magical portal in her attic."

摘要

把文本交给 AI，并要求它生成抓住关键信息的简洁摘要。

"Summarize the main points of the following news article on climate change."

翻译

指明源语言与目标语言，让 AI 在保留含义与上下文的前提下准确翻译。

"Translate the following text from English to Spanish: 'The quick brown fox jumps over the lazy dog.'"

对话

设计模拟对话的提示词，让 AI 生成模仿人类互动并保持上下文的回答。

"You are a friendly chatbot helping users troubleshoot their computer problems. Respond to the user's query: 'My computer won't turn on.'"

#### 问答

场景

说明

示例提示词

开放式问题

设计提示词，鼓励 AI 基于其知识库给出全面、有信息量的回答。

"Explain the concept of quantum computing and its potential impact on the future of technology."

具体问题

设计针对特定信息的提示词，让 AI 从所给上下文或内部知识库中检索出精确答案。

"What is the capital of France?" or "According to the provided text, what are the main causes of deforestation?"

选择题

给出带选项的提示词，促使 AI 基于对上下文的理解分析并选出最合适的答案。

"Who wrote the Harry Potter series? A) J.R.R. Tolkien, B) J.K. Rowling, C) Stephen King"

假设性问题

设计探索假设情境的提示词，让 AI 推理、推测并给出可能的结果或方案。

"What would happen if humans could travel at the speed of light?"

观点类问题

设计引出 AI 对特定主题看法的提示词，鼓励它为自己的立场给出推理与论证。

"Do you believe that artificial intelligence will eventually surpass human intelligence? Why or why not?"

场景

说明

示例提示词

开放式问题

设计提示词，鼓励 AI 基于其知识库给出全面、有信息量的回答。

"Explain the concept of quantum computing and its potential impact on the future of technology."

具体问题

设计针对特定信息的提示词，让 AI 从所给上下文或内部知识库中检索出精确答案。

"What is the capital of France?" or "According to the provided text, what are the main causes of deforestation?"

选择题

给出带选项的提示词，促使 AI 基于对上下文的理解分析并选出最合适的答案。

"Who wrote the Harry Potter series? A) J.R.R. Tolkien, B) J.K. Rowling, C) Stephen King"

假设性问题

设计探索假设情境的提示词，让 AI 推理、推测并给出可能的结果或方案。

"What would happen if humans could travel at the speed of light?"

观点类问题

设计引出 AI 对特定主题看法的提示词，鼓励它为自己的立场给出推理与论证。

"Do you believe that artificial intelligence will eventually surpass human intelligence? Why or why not?"

#### 代码生成

场景

说明

示例提示词

代码补全

给 AI 一段不完整的代码片段，提示它根据上下文与编程语言建议或补全剩余代码。

"Write a Python function to calculate the factorial of a given number."

代码翻译

指明源与目标编程语言，让 AI 在保留功能与语法的前提下翻译代码。

"Translate the following Python code to JavaScript: def greet(name): print('Hello,', name)"

代码优化

提示 AI 分析既有代码，并就效率、可读性或性能提出改进。

"Optimize the following Python code to reduce its execution time."

代码调试

把含错误的代码交给 AI，提示它定位问题并提出可能的解决方案。

"Debug the following Java code and explain why it is throwing a NullPointerException."

场景

说明

示例提示词

代码补全

给 AI 一段不完整的代码片段，提示它根据上下文与编程语言建议或补全剩余代码。

"Write a Python function to calculate the factorial of a given number."

代码翻译

指明源与目标编程语言，让 AI 在保留功能与语法的前提下翻译代码。

"Translate the following Python code to JavaScript: def greet(name): print('Hello,', name)"

代码优化

提示 AI 分析既有代码，并就效率、可读性或性能提出改进。

"Optimize the following Python code to reduce its execution time."

代码调试

把含错误的代码交给 AI，提示它定位问题并提出可能的解决方案。

"Debug the following Java code and explain why it is throwing a NullPointerException."

#### 图像生成

场景

说明

示例提示词

照片级写实图像

设计提示词，详细描述期望的图像，包括物体、场景、光照与风格，以生成逼真、高质量的图像。

"A photorealistic image of a sunset over the ocean with palm trees silhouetted against the sky."

艺术图像

设计提示词，指明艺术风格、技法与主题，引导 AI 创作模仿特定艺术流派或唤起特定情绪的图像。

"An impressionist painting of a bustling city street with people walking under umbrellas in the rain."

抽象图像

设计提示词，鼓励 AI 生成可供多种解读的图像，利用形状、色彩与纹理唤起感受或概念。

"An abstract image representing the concept of hope, using bright colors and flowing shapes."

图像编辑

把一张现有图像交给 AI 并指明期望的修改，让它按给定指令编辑并增强图像。

"Change the background of this photo to a starry night sky and add a full moon." or "Remove the person from this image and replace them with a cat."

场景

说明

示例提示词

照片级写实图像

设计提示词，详细描述期望的图像，包括物体、场景、光照与风格，以生成逼真、高质量的图像。

"A photorealistic image of a sunset over the ocean with palm trees silhouetted against the sky."

艺术图像

设计提示词，指明艺术风格、技法与主题，引导 AI 创作模仿特定艺术流派或唤起特定情绪的图像。

"An impressionist painting of a bustling city street with people walking under umbrellas in the rain."

抽象图像

设计提示词，鼓励 AI 生成可供多种解读的图像，利用形状、色彩与纹理唤起感受或概念。

"An abstract image representing the concept of hope, using bright colors and flowing shapes."

图像编辑

把一张现有图像交给 AI 并指明期望的修改，让它按给定指令编辑并增强图像。

"Change the background of this photo to a starry night sky and add a full moon." or "Remove the person from this image and replace them with a cat."

### 写出更好提示词的策略

开发有效提示词需要策略性的做法。考虑以下策略来提升你的提示词工程技能：

#### 1. 设定清晰的目标与目的：

策略

提示词示例

用动作动词指明期望的动作

"Write a bulleted list that summarizes the key findings of the attached research paper"

界定期望的输出长度与格式

"Compose a 500-word essay discussing the impact of climate change on coastal communities."

指明目标读者

"Write a product description for a new line of organic skincare products, targeting young adults concerned with sustainability."

策略

提示词示例

用动作动词指明期望的动作

"Write a bulleted list that summarizes the key findings of the attached research paper"

界定期望的输出长度与格式

"Compose a 500-word essay discussing the impact of climate change on coastal communities."

指明目标读者

"Write a product description for a new line of organic skincare products, targeting young adults concerned with sustainability."

#### 2. 提供上下文与背景信息：

策略

提示词示例

纳入相关事实与数据

"Given that global temperatures have risen by 1 degree Celsius since the pre-industrial era, discuss the potential consequences for sea level rise."

引用具体来源或文档

"Based on the attached financial report, analyze the company's profitability over the past five years."

界定关键术语与概念

"Explain the concept of quantum computing in simple terms, suitable for a non-technical audience."

策略

提示词示例

纳入相关事实与数据

"Given that global temperatures have risen by 1 degree Celsius since the pre-industrial era, discuss the potential consequences for sea level rise."

引用具体来源或文档

"Based on the attached financial report, analyze the company's profitability over the past five years."

界定关键术语与概念

"Explain the concept of quantum computing in simple terms, suitable for a non-technical audience."

#### 3. 使用少样本提示：

策略

提示词示例

提供几个期望的输入—输出对示例

Input: "Cat" Output: "A small furry mammal with whiskers." Input: "Dog" Output: "A domesticated canine known for its loyalty." Prompt: "Elephant"

展示期望的风格或语气

Example 1 (humorous): "The politician's speech was so dull, it could cure insomnia." Example 2 (formal): "The dignitary delivered an address that was both informative and engaging." Prompt: "Write a sentence describing the comedian's stand-up routine."

展示期望的细节程度

Example 1 (brief): "The movie was about a young boy who befriends an alien." Example 2 (detailed): "The science fiction film follows the story of Elliot, a lonely boy who discovers and forms a unique bond with an extraterrestrial stranded on Earth." Prompt: "Summarize the plot of the novel you just finished reading."

策略

提示词示例

提供几个期望的输入—输出对示例

Input: "Cat" Output: "A small furry mammal with whiskers." Input: "Dog" Output: "A domesticated canine known for its loyalty." Prompt: "Elephant"

展示期望的风格或语气

Example 1 (humorous): "The politician's speech was so dull, it could cure insomnia." Example 2 (formal): "The dignitary delivered an address that was both informative and engaging." Prompt: "Write a sentence describing the comedian's stand-up routine."

展示期望的细节程度

Example 1 (brief): "The movie was about a young boy who befriends an alien." Example 2 (detailed): "The science fiction film follows the story of Elliot, a lonely boy who discovers and forms a unique bond with an extraterrestrial stranded on Earth." Prompt: "Summarize the plot of the novel you just finished reading."

#### 4. 要具体：

策略

提示词示例

使用精确的语言，避免含糊

与其说："Write something about climate change," 不如说："Write a persuasive essay arguing for the implementation of stricter carbon emission regulations."

尽可能量化你的请求

与其说："Write a long poem," 不如说："Write a sonnet with 14 lines that explores themes of love and loss."

把复杂任务拆成更小的步骤

与其说："Create a marketing plan," 不如说："1. Identify the target audience. 2. Develop key marketing messages. 3. Choose appropriate marketing channels."

策略

提示词示例

使用精确的语言，避免含糊

与其说："Write something about climate change," 不如说："Write a persuasive essay arguing for the implementation of stricter carbon emission regulations."

尽可能量化你的请求

与其说："Write a long poem," 不如说："Write a sonnet with 14 lines that explores themes of love and loss."

把复杂任务拆成更小的步骤

与其说："Create a marketing plan," 不如说："1. Identify the target audience. 2. Develop key marketing messages. 3. Choose appropriate marketing channels."

#### 5. 迭代与试验：

策略

操作

尝试不同的措辞与关键词

用同义词或不同句式重写你的提示词。

调整细节与具体程度

增删信息以微调输出。

测试不同的提示词长度

既试更短的、也试更长的提示词，找到最佳平衡。

策略

操作

尝试不同的措辞与关键词

用同义词或不同句式重写你的提示词。

调整细节与具体程度

增删信息以微调输出。

测试不同的提示词长度

既试更短的、也试更长的提示词，找到最佳平衡。

#### 6. 善用思维链提示：

策略

提示词示例

鼓励逐步推理

"Solve this problem step-by-step: John has 5 apples, he eats 2. How many apples does he have left? Step 1: John starts with 5 apples. Step 2: He eats 2 apples, so we need to subtract 2 from 5. Step 3: 5 - 2 = 3. Answer: John has 3 apples left."

要求模型解释其推理过程

"Explain your thought process in determining the sentiment of this movie review: 'The acting was superb, but the plot was predictable.'"

引导模型走一遍合乎逻辑的思路序列

"To classify this email as spam or not spam, consider the following: 1. Is the sender known? 2. Does the subject line contain suspicious keywords? 3. Is the email offering something too good to be true?"

策略

提示词示例

鼓励逐步推理

"Solve this problem step-by-step: John has 5 apples, he eats 2. How many apples does he have left? Step 1: John starts with 5 apples. Step 2: He eats 2 apples, so we need to subtract 2 from 5. Step 3: 5 - 2 = 3. Answer: John has 3 apples left."

要求模型解释其推理过程

"Explain your thought process in determining the sentiment of this movie review: 'The acting was superb, but the plot was predictable.'"

引导模型走一遍合乎逻辑的思路序列

"To classify this email as spam or not spam, consider the following: 1. Is the sender known? 2. Does the subject line contain suspicious keywords? 3. Is the email offering something too good to be true?"

关于提示词工程最佳实践的更多指导，请看

[Google Cloud 上的《提示词工程五大最佳实践》。](https://cloud.google.com/blog/products/application-development/five-best-practices-for-prompt-engineering)

### 提示词工程的收益

有效的提示词工程带来诸多收益，增强 AI 模型的能力与可用性：

#### 改善模型表现

精心设计的提示词能带来更准确、更相关、更有信息量的 AI 输出，因为它们提供了清晰的指令与上下文。

#### 减少偏见与有害回应

通过仔细控制输入、引导 AI 的关注点，提示词工程有助于减轻偏见，并把生成不当或冒犯性内容的风险降到最低。

#### 增强控制力与可预测性

提示词工程让你能够影响 AI 的行为，确保得到与你期望结果一致、稳定可预测的回答。

#### 提升用户体验

清晰简洁的提示词让用户更容易与 AI 模型有效交互，从而带来更直观、更令人满意的体验。

用 Google Cloud 开启你的 AI 之旅

新客户可获得 300 美元免费额度，用于 Google Cloud。

开始使用

https://console.cloud.google.com/freetrial/?redirectPath=/vertex-ai/

与 Google Cloud 销售专家交流，更详细地讨论你的独特挑战。

联系我们

https://cloud.google.com/contact

相关的 Google Cloud 产品与服务

[查看全部 AI 产品与解决方案](https://cloud.google.com/products/ai)

- https://cloud.google.com/vertex-ai
![Vertex AI icon](https://www.gstatic.com/bricks/image/fde8cc04-719e-49de-a777-be49193b4178.svg)

- Vertex AI Platform

- 一个供数据科学家与工程师创建、训练、测试、监控、调优并部署 ML 与 AI 模型的统一平台。

- https://cloud.google.com/generative-ai-studio
![Vertex AI icon](https://www.gstatic.com/bricks/image/fde8cc04-719e-49de-a777-be49193b4178.svg)

- Vertex AI 上的生成式 AI

- 快速构建原型并测试生成式 AI 模型。试用示例提示词、设计你自己的提示词，并定制基础模型与 LLM。

- https://cloud.google.com/ai/apis
![Ex: BigQuery icon](https://www.gstatic.com/bricks/image/rc7m6af1wpQO_v5GlttqQ_nbbC4jLY0EEN4aVof8WsJLmVyWrtPTHYb5XSm4sJY_142oDc1IsIs.png)

- AI API

- 用 Google Cloud 的 AI 与机器学习 API，轻松把 AI 集成进你的应用。

- https://cloud.google.com/model-garden
- 解决方案

- Vertex AI 上的 Model Garden

- 在一处发现、定制并部署来自 Google 及其合作伙伴的各类模型，为你的 ML 项目快速起步。

##### 助你起步的额外学习资源

第一次接触 Google Cloud 或生成式 AI？新客户可获得

[300 美元免费额度，用于运行、测试并部署工作负载。](https://cloud.google.com/free/docs/free-cloud-features)

- [培训：免费的生成式 AI 基础课程](https://www.cloudskillsboost.google/paths/118)
- [文档：提示词设计导论](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/introduction-prompt-design)
- [文档：通用提示词设计策略](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/prompt-design-strategies)
- [文档：生成式 AI 提示词示例](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/prompt-samples)

##### 迈出下一步

用 300 美元免费额度与 20 多个永久免费产品，开始在 Google Cloud 上构建。

免费开始使用

https://console.cloud.google.com/freetrial/

###### 需要起步方面的帮助？

- [联系销售](https://cloud.google.com/contact/)

###### 与可信赖的伙伴合作

- [寻找合作伙伴](https://cloud.google.com/find-a-partner/)

###### 继续浏览

- [查看全部产品](https://cloud.google.com/products/)

menu

https://cloud.google.com/

![Google Cloud](https://www.gstatic.com/cgc/google-cloud-logo.svg)



searchsend

[文档](https://cloud.google.com/docs)

[支持](https://cloud.google.com/support-hub)

[控制台](https://console.cloud.google.com/)

[登录](https://accounts.google.com/AccountChooser?continue=https://cloud.google.com/discover/what-is-prompt-engineering&hl=en-US&prompt=select_account&service=cloudconsole)

免费开始

https://console.cloud.google.com/freetrial

免费开始

https://console.cloud.google.com/freetrial

联系我们

https://cloud.google.com/contact

close

- 加速你的数字化转型
- 无论你的企业处在数字化旅程的早期，还是已在转型路上走得很远，Google Cloud 都能帮你解决最棘手的挑战。
- https://cloud.google.com/transform
- 了解更多

- 核心收益
- https://cloud.google.com/why-google-cloud
- 为什么选择 Google Cloud

- 企业选择我们的主要原因。

- https://cloud.google.com/ai
- AI 与 ML

- 获得企业级就绪的 AI。

- https://cloud.google.com/multicloud
- 多云

- 在你需要的任何地方运行应用。

- https://cloud.google.com/infrastructure
- 全球基础设施

- 构建在与 Google 相同的基础设施之上。

- https://cloud.google.com/data-cloud
- Data Cloud

- 用统一的数据做出更明智的决策。

- https://cloud.google.com/solutions/modern-infrastructure
- 现代基础设施云

- 下一代云基础设施。

- https://cloud.google.com/security
- 安全

- 保护你的用户、数据与应用。

- https://workspace.google.com
- 生产力与协作

- 用 AI 驱动的应用连接你的团队。

- 报告与洞见
- https://cloud.google.com/executive-insights
- 高管洞见

- 精选的高管层观点。

- https://cloud.google.com/analyst-reports
- 分析师报告

- 看行业分析师如何评价我们。

- https://cloud.google.com/whitepapers
- 白皮书

- 浏览并下载热门白皮书。

- https://cloud.google.com/customers
- 客户案例

- 探索案例研究与视频。

close

- [行业解决方案](#)
- [应用现代化](#)
- [人工智能](#)
- [API 与应用](#)
- [数据分析](#)
- [数据库](#)
- [基础设施现代化](#)
- [生产力与协作](#)
- [安全](#)
- [初创企业与中小企业](#)

查看全部解决方案

https://cloud.google.com/solutions

- https://cloud.google.com/solutions#industry-solutions
![](https://www.gstatic.com/cloud/images/navigation/forward.svg)

- 行业解决方案

- 降低成本、提升运营敏捷性，并抓住新的市场机会。

- https://cloud.google.com/solutions/retail
![](https://www.gstatic.com/cloud/images/navigation/retail.svg)

- 零售

- 面向零售价值链的分析与协作工具。

- https://cloud.google.com/solutions/cpg
![](https://www.gstatic.com/cloud/images/navigation/cpg.svg)

- 消费品

- 面向消费品数字化转型与品牌增长的解决方案。

- https://cloud.google.com/solutions/financial-services
![](https://www.gstatic.com/cloud/images/navigation/finance.svg)

- 金融服务

- 面向金融服务的计算、数据管理与分析工具。

- https://cloud.google.com/solutions/healthcare-life-sciences
![](https://www.gstatic.com/cloud/images/navigation/hcls.svg)

- 医疗健康与生命科学

- 规模化推进研究，赋能医疗创新。

- https://cloud.google.com/solutions/media-entertainment
![](https://www.gstatic.com/cloud/images/navigation/media.svg)

- 媒体与娱乐

- 面向内容生产与分发运营的解决方案。

- https://cloud.google.com/solutions/telecommunications
![](https://www.gstatic.com/cloud/images/navigation/telecommunications.svg)

- 电信

- 用于部署 5G 并实现其商业化的混合与多云服务。

- https://cloud.google.com/solutions/games
![](https://www.gstatic.com/cloud/images/navigation/gaming.svg)

- 游戏

- 用 AI 驱动的解决方案更快地开发并扩展游戏。

- https://cloud.google.com/solutions/manufacturing
![](https://www.gstatic.com/cloud/images/navigation/manufacturing.svg)

- 制造业

- 用于优化制造价值链的迁移与 AI 工具。

- https://cloud.google.com/solutions/supply-chain-logistics
![](https://www.gstatic.com/cloud/images/navigation/supply-chain.svg)

- 供应链与物流

- 在供应链与物流运营中实现可持续、高效、有韧性的数据驱动运营。

- https://cloud.google.com/gov
![](https://www.gstatic.com/cloud/images/navigation/government.svg)

- 政府

- 面向政府机构的数据存储、AI 与分析解决方案。

- https://cloud.google.com/edu/higher-education
![](https://www.gstatic.com/cloud/images/navigation/icon-sprite.svg#education)

- 教育

- 用于提供更引人入胜的学习体验的教学工具。

- 没找到你要找的？
- https://cloud.google.com/solutions#industry-solutions
- 查看全部行业解决方案

- https://cloud.google.com/solutions/camp
![](https://www.gstatic.com/cloud/images/navigation/forward.svg)

- 应用现代化

- 评估、规划、实施并度量软件实践与能力，以现代化并简化你组织的业务应用组合。

- https://cloud.google.com/solutions/camp
- CAMP

- 用 DORA 提升软件交付能力的计划。

- https://cloud.google.com/solutions/modernize-traditional-applications
- 现代化传统应用

- 分析、归类并开始在传统工作负载上做云迁移。

- https://cloud.google.com/solutions/migrate-from-paas
- 从 PaaS 迁移：Cloud Foundry、Openshift

- 把现有容器迁移到 Google 托管容器服务的工具。

- https://cloud.google.com/solutions/mainframe-modernization
- 从大型机迁移

- 把大型机应用迁移上云的自动化工具与规范性指导。

- https://cloud.google.com/solutions/software-delivery
- 现代化软件交付

- 软件供应链最佳实践 —— 内环生产力、CI/CD 与 S3C。

- https://cloud.google.com/devops
- DevOps 最佳实践

- 在你组织中落地 DevOps 的流程与资源。

- https://cloud.google.com/sre
- SRE 原则

- 在你组织中采用 SRE 的工具与资源。

- https://cloud.google.com/solutions/platform-engineering
- 平台工程

- 用于构建、管理并扩展 IDP 的一整套托管服务与黄金路径。

- https://cloud.google.com/solutions/modernize-with-edge
- 在边缘运行应用

- 面向 Google 硬件无关边缘方案上本地化、低延迟应用的指导。

- https://cloud.google.com/solutions/architect-multicloud
- 为多云做架构设计

- 用一致的平台跨多个云管理工作负载。

- https://cloud.google.com/solutions/serverless
- 走向 Serverless

- 用于开发、部署并扩展应用的全托管环境。

- https://cloud.google.com/solutions/ai
![](https://www.gstatic.com/cloud/images/navigation/forward.svg)

- 人工智能

- 用 AI 与机器学习为你的业务增添智能与效率。

- https://cloud.google.com/solutions/customer-engagement-ai
- 搭载 Google AI 的客户互动套件

- 结合我们最先进对话式 AI 的端到端应用。

- https://cloud.google.com/document-ai
- Document AI

- 规模化自动化的文档处理与数据采集。

- https://cloud.google.com/solutions/retail-product-discovery
- 面向电商的 Vertex AI Search

- 为零售商提供 Google 级质量的搜索与商品推荐。

- https://cloud.google.com/ai/gemini
- 搭载 Gemini 的 Google Cloud

- 用于应用开发、编码等的 AI 助手。

- https://cloud.google.com/use-cases/generative-ai
- Google Cloud 上的生成式 AI

- 用生成式 AI 的力量变革内容创作与发现、研究、客户服务与开发者效率。

- https://cloud.google.com/solutions/apis-and-applications
![](https://www.gstatic.com/cloud/images/navigation/forward.svg)

- API 与应用

- 无需编码，用 API、应用与自动化加快创新节奏。

- https://cloud.google.com/solutions/new-channels-using-apis
- 用 API 开辟新业务渠道

- 吸引并赋能一个开发者与合作伙伴的生态。

- https://cloud.google.com/solutions/unlocking-legacy-applications
- 用 API 释放遗留应用的价值

- 用于扩展并现代化遗留应用的云服务。

- https://cloud.google.com/solutions/open-banking-apix
- 开放银行 APIx

- 简化并加速合规开放银行 API 的安全交付。

- https://cloud.google.com/solutions/data-analytics-and-ai
![](https://www.gstatic.com/cloud/images/navigation/forward.svg)

- 数据分析

- 用 Serverless、全托管的分析平台从任意规模的数据中即刻获得洞见，大幅简化分析工作。

- https://cloud.google.com/solutions/data-migration
- 数据迁移

- 用 AI 驱动的迁移服务迁移并现代化你的数据仓库与数据湖。

- https://cloud.google.com/solutions/data-lakehouse
- 数据湖仓

- 用高性能、开放的数据湖仓统一并治理你的多模态数据。

- https://cloud.google.com/solutions/stream-analytics
- 实时分析

- 从事件流的摄取、处理与分析中获得洞见。

- https://cloud.google.com/solutions/marketing-analytics
- 营销分析

- 用于收集、分析并激活客户数据的解决方案。

- https://cloud.google.com/datasets
- 数据集

- 来自 Google、公共与商业提供方的数据，用以充实你的分析与 AI 项目。

- https://cloud.google.com/solutions/business-intelligence
- 商业智能

- 用于现代化 BI 技术栈并打造丰富数据体验的解决方案。

- https://cloud.google.com/use-cases/ai-data-analytics
- 用于数据分析的 AI

- 用面向数据分析的 AI 编写 SQL、构建预测模型并可视化数据。

- https://cloud.google.com/solutions/geospatial
- 地理空间分析

- 一个规模化解决地理空间用例的综合平台。

- https://cloud.google.com/solutions/databases
![](https://www.gstatic.com/cloud/images/navigation/forward.svg)

- 数据库

- 用安全、可靠、高可用的全托管数据服务迁移并管理企业数据。

- https://cloud.google.com/solutions/database-migration
- 数据库迁移

- 用于简化数据库迁移生命周期的指南与工具。

- https://cloud.google.com/solutions/database-modernization
- 数据库现代化

- 通过升级现代化你的运营数据库基础设施。

- https://cloud.google.com/solutions/databases/games
- 面向游戏的数据库

- 用 Google Cloud 数据库构建全球化实时游戏。

- https://cloud.google.com/products/databases
- Google Cloud 数据库

- 用于迁移、管理并现代化数据的数据库服务。

- https://cloud.google.com/solutions/oracle
- 把 Oracle 工作负载迁移到 Google Cloud

- 对 Oracle 工作负载做重新托管、重新平台化、重写。

- https://cloud.google.com/solutions/open-source-databases
- 开源数据库

- 带企业级支持的托管开源数据库。

- https://cloud.google.com/sql-server
- Google Cloud 上的 SQL Server

- 在 Google Cloud 上运行 SQL Server 虚拟机的各种选项。

- https://cloud.google.com/products/gemini/databases
- 面向数据库的 Gemini

- 用 AI 大幅提升数据库开发与管理效率。

- https://cloud.google.com/solutions/infrastructure-modernization
![](https://www.gstatic.com/cloud/images/navigation/forward.svg)

- 基础设施现代化

- 用面向 SAP、VMware、Windows、Oracle 及其他工作负载的解决方案快速迁移。

- https://cloud.google.com/solutions/application-migration
- 应用迁移

- 用于迁移上云的发现与分析工具。

- https://cloud.google.com/solutions/sap
- Google Cloud 上的 SAP

- 运行 SAP 应用与 SAP HANA 的认证。

- https://cloud.google.com/solutions/hpc
- 高性能计算

- 支持任意工作负载的计算、存储与网络选项。

- https://cloud.google.com/windows
- Google Cloud 上的 Windows

- 用于运行 Windows 工作负载的工具与合作伙伴。

- https://cloud.google.com/solutions/data-center-migration
- 数据中心迁移

- 面向虚拟机、应用、数据库等的迁移解决方案。

- https://cloud.google.com/solutions/active-assist
- Active Assist

- 自动化的云资源优化与更强的安全性。

- https://cloud.google.com/solutions/virtual-desktops
- 虚拟桌面

- 面向桌面与应用的远程办公方案（VDI 与 DaaS）。

- https://cloud.google.com/solutions/cloud-migration-program
- 快速迁移与现代化计划

- 简化你上云路径的端到端迁移计划。

- https://cloud.google.com/solutions/backup-dr
- 备份与灾难恢复

- 确保满足你的业务连续性需求。

- https://cloud.google.com/solutions/redhat
- Google Cloud 上的 Red Hat

- Google 与 Red Hat 为传统本地与定制应用提供企业级平台。

- https://cloud.google.com/solutions/cross-cloud-network
- 跨云网络

- 简化混合与多云网络，并保护你的工作负载、数据与用户。

- https://cloud.google.com/solutions/observability
- 可观测性

- 用端到端的可见性监控、排查并改善应用性能。

- https://workspace.google.com/enterprise/
![](https://www.gstatic.com/cloud/images/navigation/forward.svg)

- 生产力与协作

- 用以人为本、为影响力而设计的解决方案改变团队的工作方式。

- https://workspace.google.com/solutions/enterprise/?enterprise-benefits_activeEl=connect
- Google Workspace

- 面向企业的协作与生产力工具。

- https://workspace.google.com/essentials/
- Google Workspace Essentials

- 面向团队的安全视频会议与现代协作。

- https://cloud.google.com/identity
- Cloud Identity

- 让 IT 管理员管理用户设备与应用的统一平台。

- https://chromeenterprise.google
- Chrome Enterprise

- 为企业打造的 ChromeOS、Chrome 浏览器与 Chrome 设备。

- https://cloud.google.com/solutions/security
![](https://www.gstatic.com/cloud/images/navigation/forward.svg)

- 安全

- 检测、调查并响应在线威胁，帮助保护你的业务。

- https://cloud.google.com/solutions/agentic-soc
- 智能体式 SOC

- 用 AI 智能体交付更好的安全成果。

- https://cloud.google.com/security/solutions/web-app-and-api-protection
- Web 应用与 API 防护

- 面向你 Web 应用与 API 的威胁与欺诈防护。

- https://cloud.google.com/security/solutions/security-and-resilience
- 安全与韧性框架

- 覆盖安全与韧性生命周期每个阶段的解决方案。

- https://cloud.google.com/solutions/risk-and-compliance-as-code
- 风险与合规即代码（RCaC）

- 用自动化现代化你的治理、风险与合规职能。

- https://cloud.google.com/security/solutions/software-supply-chain-security
- 软件供应链安全

- 用于改善端到端软件供应链安全的方案。

- https://cloud.google.com/security/solutions/security-foundation
- 安全基础

- 帮助达成强安全姿态的推荐产品。

- https://cloud.google.com/security/solutions/secops-cybershield
- Google Cloud Cybershield™

- 强化全国范围的网络防御。

- https://cloud.google.com/solutions#section-13
![](https://www.gstatic.com/cloud/images/navigation/forward.svg)

- 初创企业与中小企业

- 用量身定制的解决方案与计划加速初创企业与中小企业的成长。

- https://cloud.google.com/startup
- 初创企业计划

- 获得财务、商业与技术方面的支持，把你的初创企业带到下一个层次。

- https://cloud.google.com/solutions/smb
- 中小企业

- 探索面向网站托管、应用开发、AI 与分析的解决方案。

- https://cloud.google.com/saas
- 软件即服务

- 构建更好的 SaaS 产品、高效扩展并发展你的业务。

close

- [精选产品](#)
- [AI 与机器学习](#)
- [商业智能](#)
- [计算](#)
- [容器](#)
- [数据分析](#)
- [数据库](#)
- [开发者工具](#)
- [分布式云](#)
- [混合与多云](#)
- [行业专属](#)
- [集成服务](#)
- [管理工具](#)
- [地图与地理空间](#)
- [媒体服务](#)
- [迁移](#)
- [混合现实](#)
- [网络](#)
- [运维](#)
- [生产力与协作](#)
- [安全与身份](#)
- [Serverless](#)
- [存储](#)
- [Web3](#)

查看全部产品（100+）

https://cloud.google.com/products#featured-products

- 精选产品

- https://cloud.google.com/products/compute
![](https://www.gstatic.com/cloud/images/navigation/compute-engine.png)

- Compute Engine

- 运行在 Google 数据中心的虚拟机。

- https://cloud.google.com/storage
![](https://www.gstatic.com/cloud/images/navigation/cloud-storage.png)

- Cloud Storage

- 安全、持久且可扩展的对象存储。

- https://cloud.google.com/bigquery
![](https://www.gstatic.com/cloud/images/navigation/bigquery.png)

- BigQuery

- 面向分析与数据科学的自治数据到 AI 平台。

- https://cloud.google.com/run
![](https://www.gstatic.com/cloud/images/navigation/cloud-run.png)

- Cloud Run

- 用于运行容器化应用的全托管环境。

- https://cloud.google.com/kubernetes-engine
![](https://www.gstatic.com/cloud/images/navigation/kubernetes-engine.png)

- Google Kubernetes Engine

- 用于运行容器化应用的托管环境。

- https://cloud.google.com/vertex-ai
![](https://www.gstatic.com/cloud/images/navigation/vertex-ai.png)

- Vertex AI

- 面向 ML 模型与生成式 AI 的统一平台。

- https://cloud.google.com/looker
![](https://www.gstatic.com/cloud/images/navigation/looker.png)

- Looker

- 面向 BI、数据应用与嵌入式分析的平台。

- https://cloud.google.com/apigee
![](https://www.gstatic.com/cloud/images/navigation/apigee.png)

- Apigee API Management

- 在任何地方以可见性与管控力管理 API 的全生命周期。

- https://cloud.google.com/sql
![](https://www.gstatic.com/cloud/images/navigation/cloud-sql.png)

- Cloud SQL

- 面向 MySQL、PostgreSQL 与 SQL Server 的关系型数据库服务。

- https://cloud.google.com/gemini-enterprise
![](https://www.gstatic.com/images/branding/productlogos/gemini_2025/v1/web-24dp/logo_gemini_2025_color_2x_web_24dp.png)

- Gemini Enterprise

- 用于发现、创建、运行并治理 AI 智能体的安全平台。

- https://cloud.google.com/cdn
![](https://www.gstatic.com/cloud/images/navigation/networking.png)

- Cloud CDN

- 用于交付网页与视频的内容分发网络。

- 没找到你要找的？
- https://cloud.google.com/products#featured-products
- 查看全部产品（100+）

- https://cloud.google.com/products/ai
![](https://www.gstatic.com/cloud/images/navigation/forward.svg)

- AI 与机器学习

- https://cloud.google.com/vertex-ai
- Vertex AI Platform

- 面向 ML 模型与生成式 AI 的统一平台。

- https://cloud.google.com/generative-ai-studio
- Vertex AI Studio

- 在 Vertex AI 上构建、调优并部署基础模型。

- https://cloud.google.com/products/agent-builder
- Vertex AI Agent Builder

- 构建并部署生成式 AI 体验。

- https://cloud.google.com/products/conversational-agents
- Conversational Agents

- 用确定性与生成式 AI 两种能力构建对话式 AI。

- https://cloud.google.com/enterprise-search
- Vertex AI Search

- 为你的企业应用与体验构建 Google 级质量的搜索。

- https://cloud.google.com/speech-to-text
- Speech-to-Text

- 覆盖 125 种语言的语音识别与转写。

- https://cloud.google.com/text-to-speech
- Text-to-Speech

- 220 多种音色、40 多种语言的语音合成。

- https://cloud.google.com/translate
- Translation AI

- 语言检测、翻译与术语表支持。

- https://cloud.google.com/gemini-enterprise
- Gemini Enterprise

- 用于发现、创建、运行并治理 AI 智能体的安全平台。

- https://cloud.google.com/vision
- Vision AI

- 用于检测情绪、文字等的定制与预训练模型。

- https://cloud.google.com/solutions/contact-center-ai-platform
- 联络中心即服务

- 云原生的全渠道联络中心方案。

- 没找到你要找的？
- https://cloud.google.com/products?pds=CAE#ai-and-machine-learning
- 查看全部 AI 与机器学习产品

- 商业智能

- https://cloud.google.com/looker
- Looker

- 面向 BI、数据应用与嵌入式分析的平台。

- https://cloud.google.com/looker-studio
- Looker Studio

- 用于仪表盘、报表与分析的交互式数据套件。

- https://cloud.google.com/products/compute
![](https://www.gstatic.com/cloud/images/navigation/forward.svg)

- 计算

- https://cloud.google.com/products/compute
- Compute Engine

- 运行在 Google 数据中心的虚拟机。

- https://cloud.google.com/appengine
- App Engine

- 面向应用与后端的 Serverless 应用平台。

- https://cloud.google.com/gpu
- Cloud GPU

- 用于 ML、科学计算与三维可视化的 GPU。

- https://cloud.google.com/products/cloud-migration/virtual-machines
- 迁移到虚拟机

- 把服务器与虚拟机迁移到 Compute Engine。

- https://cloud.google.com/spot-vms
- Spot VM

- 用于批处理作业与容错工作负载的计算实例。

- https://cloud.google.com/batch
- Batch

- 用于调度批处理作业的全托管服务。

- https://cloud.google.com/compute/docs/nodes/sole-tenant-nodes
- 独占租户节点

- 为合规、许可与管理而设的专用硬件。

- https://cloud.google.com/bare-metal
- 裸金属

- 用于在 Google Cloud 上运行专门工作负载的基础设施。

- https://cloud.google.com/recommender/docs/whatis-activeassist
- Recommender

- 面向 Google Cloud 产品与服务的使用建议。

- https://cloud.google.com/vmware-engine
- VMware Engine

- 全托管的原生 VMware Cloud Foundation 软件栈。

- https://cloud.google.com/run
- Cloud Run

- 用于运行容器化应用的全托管环境。

- 没找到你要找的？
- https://cloud.google.com/products?pds=CAUSAQw#compute
- 查看全部计算产品

- https://cloud.google.com/containers
![](https://www.gstatic.com/cloud/images/navigation/forward.svg)

- 容器

- https://cloud.google.com/kubernetes-engine
- Google Kubernetes Engine

- 用于运行容器化应用的托管环境。

- https://cloud.google.com/run
- Cloud Run

- 用于运行容器化应用的全托管环境。

- https://cloud.google.com/build
- Cloud Build

- 用于在 Docker 容器中运行构建步骤的方案。

- https://cloud.google.com/artifact-registry/docs
- Artifact Registry

- 面向构建产物与依赖的包管理器。

- https://cloud.google.com/code
- Cloud Code

- 用于编写、运行并调试 Kubernetes 应用的 IDE 支持。

- https://cloud.google.com/deploy
- Cloud Deploy

- 到 GKE 与 Cloud Run 的全托管持续交付。

- https://cloud.google.com/products/cloud-migration/containers
- 迁移到容器

- 用于把虚拟机迁移成 GKE 上系统容器的组件。

- https://cloud.google.com/deep-learning-containers/docs
- Deep Learning Containers

- 含数据科学框架、库与工具的容器。

- https://knative.dev/docs/
- Knative

- 用于创建 Kubernetes 原生云端软件的组件。

- https://cloud.google.com/solutions/data-analytics-and-ai
![](https://www.gstatic.com/cloud/images/navigation/forward.svg)

- 数据分析

- https://cloud.google.com/bigquery
- BigQuery

- 面向分析与数据科学的自治数据到 AI 平台。

- https://cloud.google.com/looker
- Looker

- 面向 BI、数据应用与嵌入式分析的平台。

- https://cloud.google.com/products/dataflow
- Dataflow

- 面向流式与批处理的实时分析。

- https://cloud.google.com/pubsub
- Pub/Sub

- 用于事件摄取与投递的消息服务。

- https://cloud.google.com/dataproc
- Dataproc

- 用于运行 Apache Spark 与 Apache Hadoop 集群的托管服务。

- https://cloud.google.com/products/serverless-spark
- Google Cloud Serverless for Apache Spark

- 面向 Spark 工作负载的快速虚拟机启动与动态自动扩缩容。

- https://cloud.google.com/composer
- Cloud Composer

- 构建在 Apache Airflow 之上的工作流编排服务。

- https://cloud.google.com/biglake
- BigLake

- 用于构建 Apache Iceberg 数据湖仓的存储引擎。

- https://cloud.google.com/dataplex
- Dataplex Universal Catalog

- 面向所有 Google Cloud 服务的统一数据到 AI 治理底座。

- https://cloud.google.com/solutions/data-migration
- BigQuery Migration Services

- 免费使用、云原生且由 AI 驱动的数据迁移服务。

- https://cloud.google.com/products/managed-service-for-apache-kafka
- Managed Service for Apache Kafka

- 用于运行高可用 Apache Kafka 集群的托管 Kafka 服务。

- 没找到你要找的？
- https://cloud.google.com/products?pds=CAQ#data-analytics
- 查看全部数据分析产品
- [数据库](https://cloud.google.com/products/databases)
- [AlloyDB for PostgreSQL](https://cloud.google.com/alloydb)
- [Cloud SQL](https://cloud.google.com/sql)
- [Firestore](https://cloud.google.com/firestore)
- [Spanner](https://cloud.google.com/spanner)
- [Bigtable](https://cloud.google.com/bigtable)
- [Datastream](https://cloud.google.com/datastream)
- [Database Migration Service](https://cloud.google.com/database-migration)
- [Bare Metal Solution](https://cloud.google.com/bare-metal)
- [Memorystore](https://cloud.google.com/memorystore)
- [开发者工具](https://cloud.google.com/products/tools)
- [Artifact Registry](https://cloud.google.com/artifact-registry/docs)
- [Cloud Code](https://cloud.google.com/code)
- [Cloud Build](https://cloud.google.com/build)
- [Cloud Deploy](https://cloud.google.com/deploy)
- [Cloud Deployment Manager](https://cloud.google.com/deployment-manager/docs)
- [Cloud SDK](https://cloud.google.com/sdk)
- [Cloud Scheduler](https://cloud.google.com/scheduler/docs)
- [Cloud Source Repositories](https://cloud.google.com/source-repositories/docs)
- [Infrastructure Manager](https://cloud.google.com/infrastructure-manager/docs)
- [Cloud Workstations](https://cloud.google.com/workstations)
- [Gemini Code Assist](https://cloud.google.com/products/gemini/code-assist)
- [查看全部开发者工具](https://cloud.google.com/products?pds=CAI#developer-tools)
- [分布式云](https://cloud.google.com/distributed-cloud)
- [Google Distributed Cloud Connected](https://cloud.google.com/distributed-cloud-connected)
- [Google Distributed Cloud Air-gapped](https://cloud.google.com/distributed-cloud-air-gapped)
- 混合与多云
- [Google Kubernetes Engine](https://cloud.google.com/kubernetes-engine)
- [Apigee API Management](https://cloud.google.com/apigee)
- [迁移到容器](https://cloud.google.com/products/cloud-migration/containers)
- [Cloud Build](https://cloud.google.com/build)
- [可观测性](https://cloud.google.com/products/observability)
- [Cloud Service Mesh](https://cloud.google.com/products/service-mesh)
- [Google Distributed Cloud](https://cloud.google.com/distributed-cloud)
- 行业专属
- [Anti Money Laundering AI](https://cloud.google.com/anti-money-laundering-ai)
- [Cloud Healthcare API](https://cloud.google.com/healthcare-api)
- [Device Connect for Fitbit](https://cloud.google.com/device-connect)
- [Telecom Network Automation](https://cloud.google.com/telecom-network-automation)
- [Telecom Data Fabric](https://cloud.google.com/telecom-data-fabric)
- [Telecom Subscriber Insights](https://cloud.google.com/telecom-subscriber-insights)
- [Spectrum Access System (SAS)](https://cloud.google.com/products/spectrum-access-system)
- [集成服务](https://cloud.google.com/integration-services)
- [Application Integration](https://cloud.google.com/application-integration)
- [Workflows](https://cloud.google.com/workflows)
- [Apigee API Management](https://cloud.google.com/apigee)
- [Cloud Tasks](https://cloud.google.com/tasks/docs)
- [Cloud Scheduler](https://cloud.google.com/scheduler/docs)
- [Dataproc](https://cloud.google.com/dataproc)
- [Cloud Data Fusion](https://cloud.google.com/data-fusion)
- [Cloud Composer](https://cloud.google.com/composer)
- [Pub/Sub](https://cloud.google.com/pubsub)
- [Eventarc](https://cloud.google.com/eventarc/docs)
- [管理工具](https://cloud.google.com/products/management)
- [Cloud Shell](https://cloud.google.com/shell/docs)
- [Cloud console](https://cloud.google.com/cloud-console)
- [Cloud Endpoints](https://cloud.google.com/endpoints/docs)
- [Cloud IAM](https://cloud.google.com/security/products/iam)
- [Cloud APIs](https://cloud.google.com/apis)
- [Service Catalog](https://cloud.google.com/service-catalog/docs)
- [Cost Management](https://cloud.google.com/cost-management)
- [可观测性](https://cloud.google.com/products/observability)
- [Carbon Footprint](https://cloud.google.com/carbon-footprint)
- [Config Connector](https://cloud.google.com/config-connector/docs/overview)
- [Active Assist](https://cloud.google.com/solutions/active-assist)
- [查看全部管理工具](https://cloud.google.com/products?pds=CAY#managment-tools)
- [地图与地理空间](https://cloud.google.com/solutions/geospatial)
- [Earth Engine](https://cloud.google.com/earth-engine)
- [Google Maps Platform](https://mapsplatform.google.com)
- 媒体服务
- [Cloud CDN](https://cloud.google.com/cdn)
- [Live Stream API](https://cloud.google.com/livestream/docs)
- [OpenCue](https://www.opencue.io/docs/getting-started/)
- [Transcoder API](https://cloud.google.com/transcoder/docs)
- [Video Stitcher API](https://cloud.google.com/video-stitcher/docs)
- [迁移](https://cloud.google.com/products/cloud-migration)
- [Migration Center](https://cloud.google.com/migration-center/docs)
- [应用迁移](https://cloud.google.com/solutions/application-migration)
- [迁移到虚拟机](https://cloud.google.com/products/cloud-migration/virtual-machines)
- [Cloud Foundation Toolkit](https://cloud.google.com/docs/terraform/blueprints/terraform-blueprints)
- [Database Migration Service](https://cloud.google.com/database-migration)
- [迁移到容器](https://cloud.google.com/products/cloud-migration/containers)
- [BigQuery Migration Services](https://cloud.google.com/solutions/data-migration)
- [快速迁移与现代化计划](https://cloud.google.com/solutions/cloud-migration-program)
- [Transfer Appliance](https://cloud.google.com/transfer-appliance/docs/4.0/overview)
- [Storage Transfer Service](https://cloud.google.com/storage-transfer-service)
- [VMware Engine](https://cloud.google.com/vmware-engine)
- 混合现实
- [Immersive Stream for XR](https://cloud.google.com/immersive-stream/xr)
- [网络](https://cloud.google.com/products/networking)
- [Cloud Armor](https://cloud.google.com/security/products/armor)
- [Cloud CDN and Media CDN](https://cloud.google.com/cdn)
- [Cloud DNS](https://cloud.google.com/dns)
- [Cloud Load Balancing](https://cloud.google.com/load-balancing)
- [Cloud NAT](https://cloud.google.com/nat)
- [Cloud Connectivity](https://cloud.google.com/hybrid-connectivity)
- [Network Connectivity Center](https://cloud.google.com/network-connectivity-center)
- [Network Intelligence Center](https://cloud.google.com/network-intelligence-center)
- [Network Service Tiers](https://cloud.google.com/network-tiers)
- [Virtual Private Cloud](https://cloud.google.com/vpc)
- [Private Service Connect](https://cloud.google.com/private-service-connect)
- [查看全部网络产品](https://cloud.google.com/products?pds=CAUSAQ0#networking)

- 运维

- 为一个组织提供单一 VPC，并在项目内隔离。

- https://cloud.google.com/private-service-connect
- Private Service Connect

- 在你的 VPC 与服务之间的安全连接。

- 没找到你要找的？
- https://cloud.google.com/products?pds=CAUSAQ0#networking
- 查看全部网络产品

- https://cloud.google.com/products/operations
![](https://www.gstatic.com/cloud/images/navigation/forward.svg)

- 运维

- https://cloud.google.com/logging
- Cloud Logging

- Google Cloud 的审计、平台与应用日志管理。

- https://cloud.google.com/monitoring
- Cloud Monitoring

- 用丰富的指标掌握基础设施与应用健康度。

- https://cloud.google.com/error-reporting/docs/grouping-errors
- Error Reporting

- 应用错误的识别与分析。

- https://cloud.google.com/managed-prometheus
- Managed Service for Prometheus

- Google Cloud 上的全托管 Prometheus。

- https://cloud.google.com/trace/docs
- Cloud Trace

- 从应用收集延迟数据的链路追踪系统。

- https://cloud.google.com/profiler/docs
- Cloud Profiler

- 用于分析应用性能的 CPU 与堆分析器。

- https://cloud.google.com/docs/quotas
- Cloud Quotas

- 管理所有 Google Cloud 服务的配额。

- 生产力与协作

- https://about.appsheet.com/home/
- AppSheet

- 用于构建并扩展应用的无代码开发平台。

- https://cloud.google.com/gemini-enterprise
- Gemini Enterprise

- 用于发现、创建、运行并治理 AI 智能体的安全平台。

- https://workspace.google.com/solutions/enterprise/?enterprise-benefits_activeEl=connect/
- Google Workspace

- 面向个人与组织的协作与生产力工具。

- https://workspace.google.com/essentials/
- Google Workspace Essentials

- 面向团队的安全视频会议与现代协作。

- https://cloud.google.com/identity
- Cloud Identity

- 让 IT 管理员管理用户设备与应用的统一平台。

- https://chromeenterprise.google
- Chrome Enterprise

- 为企业打造的 ChromeOS、Chrome 浏览器与 Chrome 设备。

- https://cloud.google.com/products/security-and-identity
![](https://www.gstatic.com/cloud/images/navigation/forward.svg)

- 安全与身份

- https://cloud.google.com/security/products/iam
- Cloud IAM

- 面向 Google Cloud 资源的权限管理系统。

- https://cloud.google.com/security/products/sensitive-data-protection
- Sensitive Data Protection

- 发现、分类并保护你宝贵的数据资产。

- https://cloud.google.com/security/products/managed-defense
- Mandiant Managed Defense

- 7×24 有把握地发现并消除威胁。

- https://cloud.google.com/security/products/threat-intelligence
- Google Threat Intelligence

- 知道谁在针对你。

- https://cloud.google.com/security/products/security-command-center
- Security Command Center

- 用于防御针对你 Google Cloud 资产威胁的平台。

- https://cloud.google.com/security/products/security-key-management
- Cloud Key Management

- 在 Google Cloud 上管理加密密钥。

- https://cloud.google.com/security/consulting/mandiant-incident-response-services
- Mandiant Incident Response

- 把入侵的影响降到最低。

- https://docs.cloud.google.com/chrome-enterprise-premium/
- Chrome Enterprise Premium

- 用广泛的端点可见性获得安全的企业级浏览体验。

- https://cloud.google.com/security/products/assured-workloads
- Assured Workloads

- 面向敏感工作负载的合规与安全控制。

- https://cloud.google.com/security/products/security-operations
- Google Security Operations

- 检测、调查并响应网络威胁。

- https://cloud.google.com/security/consulting/mandiant-services
- Mandiant Consulting

- 在故障事件之前、之中与之后获得专家指导。

- 没找到你要找的？
- https://cloud.google.com/products?pds=CAg#security-and-identity
- 查看全部安全与身份产品

- https://cloud.google.com/serverless
![](https://www.gstatic.com/cloud/images/navigation/forward.svg)

- Serverless

- https://cloud.google.com/run
- Cloud Run

- 用于运行容器化应用的全托管环境。

- https://cloud.google.com/functions
- Cloud Functions

- 用于创建响应云事件的函数的平台。

- https://cloud.google.com/appengine
- App Engine

- 面向应用与后端的 Serverless 应用平台。

- https://cloud.google.com/workflows
- Workflows

- 面向 Serverless 产品与 API 服务的工作流编排。

- https://cloud.google.com/api-gateway/docs
- API Gateway

- 用全托管网关开发、部署、保护并管理 API。

- https://cloud.google.com/products/storage
![](https://www.gstatic.com/cloud/images/navigation/forward.svg)

- 存储

- https://cloud.google.com/storage
- Cloud Storage

- 安全、持久且可扩展的对象存储。

- https://cloud.google.com/products/block-storage
- Block Storage

- 面向 AI、分析、数据库与企业应用的高性能存储。

- https://cloud.google.com/filestore
- Filestore

- 高度可扩展且安全的文件存储。

- https://cloud.google.com/persistent-disk
- Persistent Disk

- 面向 Google Cloud 上虚拟机实例的块存储。

- https://firebase.google.com/products/storage
- Cloud Storage for Firebase

- 用于存储并分发用户生成内容的对象存储。

- https://cloud.google.com/products/local-ssd
- Local SSD

- 本地挂载、满足高性能需求的块存储。

- https://cloud.google.com/storage-transfer-service
- Storage Transfer Service

- 从在线与本地来源向 Cloud Storage 传输数据。

- https://cloud.google.com/products/managed-lustre
- Google Cloud Managed Lustre

- 高性能托管并行文件服务。

- https://cloud.google.com/netapp-volumes
- Google Cloud NetApp Volumes

- 面向 NFS、SMB 与多协议环境的文件存储服务。

- https://cloud.google.com/backup-disaster-recovery
- Backup and DR Service

- 用于集中式、应用一致性数据保护的服务。

- https://cloud.google.com/web3
![](https://www.gstatic.com/cloud/images/navigation/forward.svg)

- Web3

- https://cloud.google.com/blockchain-node-engine
- Blockchain Node Engine

- 用于区块链开发的全托管节点托管服务。

- https://cloud.google.com/products/blockchain-rpc
- Blockchain RPC

- 用于区块链开发的企业级 RPC。

close

- 用我们透明的定价方式省钱
- Google Cloud 的按量付费定价会根据月度用量自动节省，预付费资源还有折扣。今天就联系我们获取报价。
- https://cloud.google.com/contact/form?direct=true
- 获取报价

- 定价总览与工具
- https://cloud.google.com/pricing
- Google Cloud 定价

- 用多少付多少，无厂商锁定。

- https://cloud.google.com/products/calculator
- 定价计算器

- 计算你能节省的云成本。

- https://cloud.google.com/free
- Google Cloud 免费层

- 探索带每月免费额度的产品。

- https://cloud.google.com/architecture/framework/cost-optimization
- 成本优化框架

- 获取优化工作负载成本的最佳实践。

- https://cloud.google.com/cost-management
- 成本管理工具

- 用于监控并控制成本的工具。

- 各产品定价
- https://cloud.google.com/compute/all-pricing
- Compute Engine

- https://cloud.google.com/sql/pricing
- Cloud SQL

- https://cloud.google.com/kubernetes-engine/pricing
- Google Kubernetes Engine

- https://cloud.google.com/storage/pricing
- Cloud Storage

- https://cloud.google.com/bigquery/pricing
- BigQuery

- https://cloud.google.com/pricing/list
- 查看涵盖 100+ 产品的完整价目表

close

- 学习与构建
- https://cloud.google.com/free
- Google Cloud 免费计划

- 300 美元免费额度与 20 多个免费产品。

- https://cloud.google.com/solution-generator
- Solution Generator

- 获取 AI 生成的解决方案建议。

- https://cloud.google.com/docs/tutorials?doctype=quickstart
- 快速上手

- 获取教程与逐步指导。

- https://cloud.google.com/blog
- 博客

- 阅读我们最新的产品新闻与故事。

- https://cloud.google.com/learn
- 学习中心

- 用按角色划分的培训发展你的职业生涯。

- https://cloud.google.com/certification
- Google Cloud 认证

- 准备并报名认证考试。

- https://cloud.google.com/discover
- 云计算基础

- 进一步了解云计算基础。

- https://cloud.google.com/architecture
- 云架构中心

- 获取参考架构与最佳实践。

- 连接
- https://cloud.google.com/innovators/innovatorsplus
- Innovators

- 加入 Google Cloud 的开发者计划。

- https://cloud.google.com/developers
- 开发者中心

- 保持了解动态、保持连接。

- https://cloud.google.com/events
- 活动与网络研讨会

- 浏览即将举办与点播的活动。

- https://discuss.google.dev/c/google-cloud/14
- Google Cloud 社区

- 提问、找答案并建立联系。

- 咨询与合作伙伴
- https://cloud.google.com/consulting
- Google Cloud Consulting

- 与我们的专家一起做云项目。

- https://cloud.google.com/marketplace
- Google Cloud Marketplace

- 几次点击即可部署开箱即用的解决方案。

- https://cloud.google.com/partners
- 寻找合作伙伴

- 探索与合作伙伴合作的好处。

- https://partners.cloud.google.com
- Google Cloud 合作伙伴

- 了解生态与资源。

close

https://cloud.google.com/

![Google Cloud](https://www.gstatic.com/cgc/google-cloud-logo.svg)

- [总览](https://cloud.google.com/why-google-cloud)
  - arrow_forward

- [解决方案](https://cloud.google.com/solutions)
  - arrow_forward

- [产品](https://cloud.google.com/products)
  - arrow_forward

- [定价](https://cloud.google.com/pricing)
  - arrow_forward

- [资源](https://cloud.google.com/docs/get-started)
  - arrow_forward

- [文档](https://cloud.google.com/docs)
- [支持](https://cloud.google.com/support-hub)
- [控制台](https://console.cloud.google.com/)

- 加速你的数字化转型
- [了解更多](https://cloud.google.com/transform)
- 核心收益
- [为什么选择 Google Cloud](https://cloud.google.com/why-google-cloud)
- [AI 与 ML](https://cloud.google.com/ai)
- [多云](https://cloud.google.com/multicloud)
- [全球基础设施](https://cloud.google.com/infrastructure)
- [Data Cloud](https://cloud.google.com/data-cloud)
- [现代基础设施云](https://cloud.google.com/solutions/modern-infrastructure)
- [安全](https://cloud.google.com/security)
- [生产力与协作](https://workspace.google.com)
- 报告与洞见
- [高管洞见](https://cloud.google.com/executive-insights)
- [分析师报告](https://cloud.google.com/analyst-reports)
- [白皮书](https://cloud.google.com/whitepapers)
- [客户案例](https://cloud.google.com/customers)

- [行业解决方案](https://cloud.google.com/solutions#industry-solutions)
- [零售](https://cloud.google.com/solutions/retail)
- [消费品](https://cloud.google.com/solutions/cpg)
- [金融服务](https://cloud.google.com/solutions/financial-services)
- [医疗健康与生命科学](https://cloud.google.com/solutions/healthcare-life-sciences)
- [媒体与娱乐](https://cloud.google.com/solutions/media-entertainment)
- [电信](https://cloud.google.com/solutions/telecommunications)
- [游戏](https://cloud.google.com/solutions/games)
- [制造业](https://cloud.google.com/solutions/manufacturing)
- [供应链与物流](https://cloud.google.com/solutions/supply-chain-logistics)
- [政府](https://cloud.google.com/gov)
- [教育](https://cloud.google.com/edu/higher-education)
- [查看全部行业解决方案](https://cloud.google.com/solutions#industry-solutions)
- [查看全部解决方案](https://cloud.google.com/solutions)
- [应用现代化](https://cloud.google.com/solutions/camp)
- [CAMP](https://cloud.google.com/solutions/camp)
- [现代化传统应用](https://cloud.google.com/solutions/modernize-traditional-applications)
- [从 PaaS 迁移：Cloud Foundry、Openshift](https://cloud.google.com/solutions/migrate-from-paas)
- [从大型机迁移](https://cloud.google.com/solutions/mainframe-modernization)
- [现代化软件交付](https://cloud.google.com/solutions/software-delivery)
- [DevOps 最佳实践](https://cloud.google.com/devops)
- [SRE 原则](https://cloud.google.com/sre)
- [平台工程](https://cloud.google.com/solutions/platform-engineering)
- [在边缘运行应用](https://cloud.google.com/solutions/modernize-with-edge)
- [为多云做架构设计](https://cloud.google.com/solutions/architect-multicloud)
- [走向 Serverless](https://cloud.google.com/solutions/serverless)
- [人工智能](https://cloud.google.com/solutions/ai)
- [搭载 Google AI 的客户互动套件](https://cloud.google.com/solutions/customer-engagement-ai)
- [Document AI](https://cloud.google.com/document-ai)
- [面向电商的 Vertex AI Search](https://cloud.google.com/solutions/retail-product-discovery)
- [搭载 Gemini 的 Google Cloud](https://cloud.google.com/ai/gemini)
- [Google Cloud 上的生成式 AI](https://cloud.google.com/use-cases/generative-ai)
- [API 与应用](https://cloud.google.com/solutions/apis-and-applications)
- [用 API 开辟新业务渠道](https://cloud.google.com/solutions/new-channels-using-apis)
- [用 API 释放遗留应用的价值](https://cloud.google.com/solutions/unlocking-legacy-applications)
- [开放银行 APIx](https://cloud.google.com/solutions/open-banking-apix)
- [数据分析](https://cloud.google.com/solutions/data-analytics-and-ai)
- [数据迁移](https://cloud.google.com/solutions/data-migration)
- [数据湖仓](https://cloud.google.com/solutions/data-lakehouse)
- [实时分析](https://cloud.google.com/solutions/stream-analytics)
- [营销分析](https://cloud.google.com/solutions/marketing-analytics)
- [数据集](https://cloud.google.com/datasets)
- [商业智能](https://cloud.google.com/solutions/business-intelligence)
- [用于数据分析的 AI](https://cloud.google.com/use-cases/ai-data-analytics)
- [地理空间分析](https://cloud.google.com/solutions/geospatial)
- [数据库](https://cloud.google.com/solutions/databases)
- [数据库迁移](https://cloud.google.com/solutions/database-migration)
- [数据库现代化](https://cloud.google.com/solutions/database-modernization)
- [面向游戏的数据库](https://cloud.google.com/solutions/databases/games)
- [Google Cloud 数据库](https://cloud.google.com/products/databases)
- [把 Oracle 工作负载迁移到 Google Cloud](https://cloud.google.com/solutions/oracle)
- [开源数据库](https://cloud.google.com/solutions/open-source-databases)
- [Google Cloud 上的 SQL Server](https://cloud.google.com/sql-server)
- [面向数据库的 Gemini](https://cloud.google.com/products/gemini/databases)
- [基础设施现代化](https://cloud.google.com/solutions/infrastructure-modernization)
- [应用迁移](https://cloud.google.com/solutions/application-migration)
- [Google Cloud 上的 SAP](https://cloud.google.com/solutions/sap)
- [高性能计算](https://cloud.google.com/solutions/hpc)
- [Google Cloud 上的 Windows](https://cloud.google.com/windows)
- [数据中心迁移](https://cloud.google.com/solutions/data-center-migration)
- [Active Assist](https://cloud.google.com/solutions/active-assist)
- [虚拟桌面](https://cloud.google.com/solutions/virtual-desktops)
- [快速迁移与现代化计划](https://cloud.google.com/solutions/cloud-migration-program)
- [备份与灾难恢复](https://cloud.google.com/solutions/backup-dr)
- [Google Cloud 上的 Red Hat](https://cloud.google.com/solutions/redhat)
- [跨云网络](https://cloud.google.com/solutions/cross-cloud-network)
- [可观测性](https://cloud.google.com/solutions/observability)
- [生产力与协作](https://workspace.google.com/enterprise/)
- [Google Workspace](https://workspace.google.com/solutions/enterprise/?enterprise-benefits_activeEl=connect)
- [Google Workspace Essentials](https://workspace.google.com/essentials/)
- [Cloud Identity](https://cloud.google.com/identity)
- [Chrome Enterprise](https://chromeenterprise.google)
- [安全](https://cloud.google.com/solutions/security)
- [智能体式 SOC](https://cloud.google.com/solutions/agentic-soc)
- [Web 应用与 API 防护](https://cloud.google.com/security/solutions/web-app-and-api-protection)
- [安全与韧性框架](https://cloud.google.com/security/solutions/security-and-resilience)
- [风险与合规即代码（RCaC）](https://cloud.google.com/solutions/risk-and-compliance-as-code)
- [软件供应链安全](https://cloud.google.com/security/solutions/software-supply-chain-security)
- [安全基础](https://cloud.google.com/security/solutions/security-foundation)
- [Google Cloud Cybershield™](https://cloud.google.com/security/solutions/secops-cybershield)
- [初创企业与中小企业](https://cloud.google.com/solutions#section-13)
- [初创企业计划](https://cloud.google.com/startup)
- [中小企业](https://cloud.google.com/solutions/smb)
- [软件即服务](https://cloud.google.com/saas)

- 精选产品
- [Compute Engine](https://cloud.google.com/products/compute)
- [Cloud Storage](https://cloud.google.com/storage)
- [BigQuery](https://cloud.google.com/bigquery)
- [Cloud Run](https://cloud.google.com/run)
- [Google Kubernetes Engine](https://cloud.google.com/kubernetes-engine)
- [Vertex AI](https://cloud.google.com/vertex-ai)
- [Looker](https://cloud.google.com/looker)
- [Apigee API Management](https://cloud.google.com/apigee)
- [Cloud SQL](https://cloud.google.com/sql)
- [Gemini Enterprise](https://cloud.google.com/gemini-enterprise)
- [Cloud CDN](https://cloud.google.com/cdn)
- [查看全部产品（100+）](https://cloud.google.com/products#featured-products)
- [AI 与机器学习](https://cloud.google.com/products/ai)
- [Vertex AI Platform](https://cloud.google.com/vertex-ai)
- [Vertex AI Studio](https://cloud.google.com/generative-ai-studio)
- [Vertex AI Agent Builder](https://cloud.google.com/products/agent-builder)
- [Conversational Agents](https://cloud.google.com/products/conversational-agents)
- [Vertex AI Search](https://cloud.google.com/enterprise-search)
- [Speech-to-Text](https://cloud.google.com/speech-to-text)
- [Text-to-Speech](https://cloud.google.com/text-to-speech)
- [Translation AI](https://cloud.google.com/translate)
- [Gemini Enterprise](https://cloud.google.com/gemini-enterprise)
- [Vision AI](https://cloud.google.com/vision)
- [联络中心即服务](https://cloud.google.com/solutions/contact-center-ai-platform)
- [查看全部 AI 与机器学习产品](https://cloud.google.com/products?pds=CAE#ai-and-machine-learning)
- 商业智能
- [Looker](https://cloud.google.com/looker)
- [Looker Studio](https://cloud.google.com/looker-studio)
- [计算](https://cloud.google.com/products/compute)
- [Compute Engine](https://cloud.google.com/products/compute)
- [App Engine](https://cloud.google.com/appengine)
- [Cloud GPU](https://cloud.google.com/gpu)
- [迁移到虚拟机](https://cloud.google.com/products/cloud-migration/virtual-machines)
- [Spot VM](https://cloud.google.com/spot-vms)
- [Batch](https://cloud.google.com/batch)
- [独占租户节点](https://cloud.google.com/compute/docs/nodes/sole-tenant-nodes)
- [裸金属](https://cloud.google.com/bare-metal)
- [Recommender](https://cloud.google.com/recommender/docs/whatis-activeassist)
- [VMware Engine](https://cloud.google.com/vmware-engine)
- [Cloud Run](https://cloud.google.com/run)
- [查看全部计算产品](https://cloud.google.com/products?pds=CAUSAQw#compute)
- [容器](https://cloud.google.com/containers)
- [Google Kubernetes Engine](https://cloud.google.com/kubernetes-engine)
- [Cloud Run](https://cloud.google.com/run)
- [Cloud Build](https://cloud.google.com/build)
- [Artifact Registry](https://cloud.google.com/artifact-registry/docs)
- [Cloud Code](https://cloud.google.com/code)
- [Cloud Deploy](https://cloud.google.com/deploy)
- [迁移到容器](https://cloud.google.com/products/cloud-migration/containers)
- [Deep Learning Containers](https://cloud.google.com/deep-learning-containers/docs)
- [Knative](https://knative.dev/docs/)
- [数据分析](https://cloud.google.com/solutions/data-analytics-and-ai)
- [BigQuery](https://cloud.google.com/bigquery)
- [Looker](https://cloud.google.com/looker)
- [Dataflow](https://cloud.google.com/products/dataflow)
- [Pub/Sub](https://cloud.google.com/pubsub)
- [Dataproc](https://cloud.google.com/dataproc)
- [Google Cloud Serverless for Apache Spark](https://cloud.google.com/products/serverless-spark)
- [Cloud Composer](https://cloud.google.com/composer)
- [BigLake](https://cloud.google.com/biglake)
- [Dataplex Universal Catalog](https://cloud.google.com/dataplex)
- [BigQuery Migration Services](https://cloud.google.com/solutions/data-migration)
- [Managed Service for Apache Kafka](https://cloud.google.com/products/managed-service-for-apache-kafka)
- [查看全部数据分析产品](https://cloud.google.com/products?pds=CAQ#data-analytics)
- [数据库](https://cloud.google.com/products/databases)
- [AlloyDB for PostgreSQL](https://cloud.google.com/alloydb)
- [Cloud SQL](https://cloud.google.com/sql)
- [Firestore](https://cloud.google.com/firestore)
- [Spanner](https://cloud.google.com/spanner)
- [Bigtable](https://cloud.google.com/bigtable)
- [Datastream](https://cloud.google.com/datastream)
- [Database Migration Service](https://cloud.google.com/database-migration)
- [Bare Metal Solution](https://cloud.google.com/bare-metal)
- [Memorystore](https://cloud.google.com/memorystore)
- [开发者工具](https://cloud.google.com/products/tools)
- [Artifact Registry](https://cloud.google.com/artifact-registry/docs)
- [Cloud Code](https://cloud.google.com/code)
- [Cloud Build](https://cloud.google.com/build)
- [Cloud Deploy](https://cloud.google.com/deploy)
- [Cloud Deployment Manager](https://cloud.google.com/deployment-manager/docs)
- [Cloud SDK](https://cloud.google.com/sdk)
- [Cloud Scheduler](https://cloud.google.com/scheduler/docs)
- [Cloud Source Repositories](https://cloud.google.com/source-repositories/docs)
- [Infrastructure Manager](https://cloud.google.com/infrastructure-manager/docs)
- [Cloud Workstations](https://cloud.google.com/workstations)
- [Gemini Code Assist](https://cloud.google.com/products/gemini/code-assist)
- [查看全部开发者工具](https://cloud.google.com/products?pds=CAI#developer-tools)
- [分布式云](https://cloud.google.com/distributed-cloud)
- [Google Distributed Cloud Connected](https://cloud.google.com/distributed-cloud-connected)
- [Google Distributed Cloud Air-gapped](https://cloud.google.com/distributed-cloud-air-gapped)
- 混合与多云
- [Google Kubernetes Engine](https://cloud.google.com/kubernetes-engine)
- [Apigee API Management](https://cloud.google.com/apigee)
- [迁移到容器](https://cloud.google.com/products/cloud-migration/containers)
- [Cloud Build](https://cloud.google.com/build)
- [可观测性](https://cloud.google.com/products/observability)
- [Cloud Service Mesh](https://cloud.google.com/products/service-mesh)
- [Google Distributed Cloud](https://cloud.google.com/distributed-cloud)
- 行业专属
- [Anti Money Laundering AI](https://cloud.google.com/anti-money-laundering-ai)
- [Cloud Healthcare API](https://cloud.google.com/healthcare-api)
- [Device Connect for Fitbit](https://cloud.google.com/device-connect)
- [Telecom Network Automation](https://cloud.google.com/telecom-network-automation)
- [Telecom Data Fabric](https://cloud.google.com/telecom-data-fabric)
- [Telecom Subscriber Insights](https://cloud.google.com/telecom-subscriber-insights)
- [Spectrum Access System (SAS)](https://cloud.google.com/products/spectrum-access-system)
- [集成服务](https://cloud.google.com/integration-services)
- [Application Integration](https://cloud.google.com/application-integration)
- [Workflows](https://cloud.google.com/workflows)
- [Apigee API Management](https://cloud.google.com/apigee)
- [Cloud Tasks](https://cloud.google.com/tasks/docs)
- [Cloud Scheduler](https://cloud.google.com/scheduler/docs)
- [Dataproc](https://cloud.google.com/dataproc)
- [Cloud Data Fusion](https://cloud.google.com/data-fusion)
- [Cloud Composer](https://cloud.google.com/composer)
- [Pub/Sub](https://cloud.google.com/pubsub)
- [Eventarc](https://cloud.google.com/eventarc/docs)
- [管理工具](https://cloud.google.com/products/management)
- [Cloud Shell](https://cloud.google.com/shell/docs)
- [Cloud console](https://cloud.google.com/cloud-console)
- [Cloud Endpoints](https://cloud.google.com/endpoints/docs)
- [Cloud IAM](https://cloud.google.com/security/products/iam)
- [Cloud APIs](https://cloud.google.com/apis)
- [Service Catalog](https://cloud.google.com/service-catalog/docs)
- [Cost Management](https://cloud.google.com/cost-management)
- [可观测性](https://cloud.google.com/products/observability)
- [Carbon Footprint](https://cloud.google.com/carbon-footprint)
- [Config Connector](https://cloud.google.com/config-connector/docs/overview)
- [Active Assist](https://cloud.google.com/solutions/active-assist)
- [查看全部管理工具](https://cloud.google.com/products?pds=CAY#managment-tools)
- [地图与地理空间](https://cloud.google.com/solutions/geospatial)
- [Earth Engine](https://cloud.google.com/earth-engine)
- [Google Maps Platform](https://mapsplatform.google.com)
- 媒体服务
- [Cloud CDN](https://cloud.google.com/cdn)
- [Live Stream API](https://cloud.google.com/livestream/docs)
- [OpenCue](https://www.opencue.io/docs/getting-started/)
- [Transcoder API](https://cloud.google.com/transcoder/docs)
- [Video Stitcher API](https://cloud.google.com/video-stitcher/docs)
- [迁移](https://cloud.google.com/products/cloud-migration)
- [Migration Center](https://cloud.google.com/migration-center/docs)
- [应用迁移](https://cloud.google.com/solutions/application-migration)
- [迁移到虚拟机](https://cloud.google.com/products/cloud-migration/virtual-machines)
- [Cloud Foundation Toolkit](https://cloud.google.com/docs/terraform/blueprints/terraform-blueprints)
- [Database Migration Service](https://cloud.google.com/database-migration)
- [迁移到容器](https://cloud.google.com/products/cloud-migration/containers)
- [BigQuery Migration Services](https://cloud.google.com/solutions/data-migration)
- [快速迁移与现代化计划](https://cloud.google.com/solutions/cloud-migration-program)
- [Transfer Appliance](https://cloud.google.com/transfer-appliance/docs/4.0/overview)
- [Storage Transfer Service](https://cloud.google.com/storage-transfer-service)
- [VMware Engine](https://cloud.google.com/vmware-engine)
- 混合现实
- [Immersive Stream for XR](https://cloud.google.com/immersive-stream/xr)
- [网络](https://cloud.google.com/products/networking)
- [Cloud Armor](https://cloud.google.com/security/products/armor)
- [Cloud CDN and Media CDN](https://cloud.google.com/cdn)
- [Cloud DNS](https://cloud.google.com/dns)
- [Cloud Load Balancing](https://cloud.google.com/load-balancing)
- [Cloud NAT](https://cloud.google.com/nat)
- [Cloud Connectivity](https://cloud.google.com/hybrid-connectivity)
- [Network Connectivity Center](https://cloud.google.com/network-connectivity-center)
- [Network Intelligence Center](https://cloud.google.com/network-intelligence-center)
- [Network Service Tiers](https://cloud.google.com/network-tiers)
- [Virtual Private Cloud](https://cloud.google.com/vpc)
- [Private Service Connect](https://cloud.google.com/private-service-connect)
- [查看全部网络产品](https://cloud.google.com/products?pds=CAUSAQ0#networking)
- [运维](https://cloud.google.com/products/operations)
- [Cloud Logging](https://cloud.google.com/logging)
- [Cloud Monitoring](https://cloud.google.com/monitoring)
- [Error Reporting](https://cloud.google.com/error-reporting/docs/grouping-errors)
- [Managed Service for Prometheus](https://cloud.google.com/managed-prometheus)
- [Cloud Trace](https://cloud.google.com/trace/docs)
- [Cloud Profiler](https://cloud.google.com/profiler/docs)
- [Cloud Quotas](https://cloud.google.com/docs/quotas)
- 生产力与协作
- [AppSheet](https://about.appsheet.com/home/)
- [Gemini Enterprise](https://cloud.google.com/gemini-enterprise)
- [Google Workspace](https://workspace.google.com/solutions/enterprise/?enterprise-benefits_activeEl=connect/)
- [Google Workspace Essentials](https://workspace.google.com/essentials/)
- [Cloud Identity](https://cloud.google.com/identity)
- [Chrome Enterprise](https://chromeenterprise.google)
- [安全与身份](https://cloud.google.com/products/security-and-identity)
- [Cloud IAM](https://cloud.google.com/security/products/iam)
- [Sensitive Data Protection](https://cloud.google.com/security/products/sensitive-data-protection)
- [Mandiant Managed Defense](https://cloud.google.com/security/products/managed-defense)
- [Google Threat Intelligence](https://cloud.google.com/security/products/threat-intelligence)
- [Security Command Center](https://cloud.google.com/security/products/security-command-center)
- [Cloud Key Management](https://cloud.google.com/security/products/security-key-management)
- [Mandiant Incident Response](https://cloud.google.com/security/consulting/mandiant-incident-response-services)
- [Chrome Enterprise Premium](https://docs.cloud.google.com/chrome-enterprise-premium/)
- [Assured Workloads](https://cloud.google.com/security/products/assured-workloads)
- [Google Security Operations](https://cloud.google.com/security/products/security-operations)
- [Mandiant Consulting](https://cloud.google.com/security/consulting/mandiant-services)
- [查看全部安全与身份产品](https://cloud.google.com/products?pds=CAg#security-and-identity)
- [Serverless](https://cloud.google.com/serverless)
- [Cloud Run](https://cloud.google.com/run)
- [Cloud Functions](https://cloud.google.com/functions)
- [App Engine](https://cloud.google.com/appengine)
- [Workflows](https://cloud.google.com/workflows)
- [API Gateway](https://cloud.google.com/api-gateway/docs)
- [存储](https://cloud.google.com/products/storage)
- [Cloud Storage](https://cloud.google.com/storage)
- [Block Storage](https://cloud.google.com/products/block-storage)
- [Filestore](https://cloud.google.com/filestore)
- [Persistent Disk](https://cloud.google.com/persistent-disk)
- [Cloud Storage for Firebase](https://firebase.google.com/products/storage)
- [Local SSD](https://cloud.google.com/products/local-ssd)
- [Storage Transfer Service](https://cloud.google.com/storage-transfer-service)
- [Google Cloud Managed Lustre](https://cloud.google.com/products/managed-lustre)
- [Google Cloud NetApp Volumes](https://cloud.google.com/netapp-volumes)
- [Backup and DR Service](https://cloud.google.com/backup-disaster-recovery)
- [Web3](https://cloud.google.com/web3)
- [Blockchain Node Engine](https://cloud.google.com/blockchain-node-engine)
- [Blockchain RPC](https://cloud.google.com/products/blockchain-rpc)

- 用我们透明的定价方式省钱
- [获取报价](https://cloud.google.com/contact/form?direct=true)
- 定价总览与工具
- [Google Cloud 定价](https://cloud.google.com/pricing)
- [定价计算器](https://cloud.google.com/products/calculator)
- [Google Cloud 免费层](https://cloud.google.com/free)
- [成本优化框架](https://cloud.google.com/architecture/framework/cost-optimization)
- [成本管理工具](https://cloud.google.com/cost-management)
- 各产品定价
- [Compute Engine](https://cloud.google.com/compute/all-pricing)
- [Cloud SQL](https://cloud.google.com/sql/pricing)
- [Google Kubernetes Engine](https://cloud.google.com/kubernetes-engine/pricing)
- [Cloud Storage](https://cloud.google.com/storage/pricing)
- [BigQuery](https://cloud.google.com/bigquery/pricing)
- [查看涵盖 100+ 产品的完整价目表](https://cloud.google.com/pricing/list)

- 学习与构建
- [Google Cloud 免费计划](https://cloud.google.com/free)
- [Solution Generator](https://cloud.google.com/solution-generator)
- [快速上手](https://cloud.google.com/docs/tutorials?doctype=quickstart)
- [博客](https://cloud.google.com/blog)
- [学习中心](https://cloud.google.com/learn)
- [Google Cloud 认证](https://cloud.google.com/certification)
- [云计算基础](https://cloud.google.com/discover)
- [云架构中心](https://cloud.google.com/architecture)
- 连接
- [Innovators](https://cloud.google.com/innovators/innovatorsplus)
- [开发者中心](https://cloud.google.com/developers)
- [活动与网络研讨会](https://cloud.google.com/events)
- [Google Cloud 社区](https://discuss.google.dev/c/google-cloud/14)
- 咨询与合作伙伴
- [Google Cloud Consulting](https://cloud.google.com/consulting)
- [Google Cloud Marketplace](https://cloud.google.com/marketplace)
- [寻找合作伙伴](https://cloud.google.com/partners)
- [Google Cloud 合作伙伴](https://partners.cloud.google.com)

```
