# 翻译留痕：finding-vulnerabilities-claude-codex

- doc_id：`finding-vulnerabilities-claude-codex`
- 时间：2026-09-27T17:12:43+08:00
- 原文：`extracted/finding-vulnerabilities-claude-codex.md`
- 译文：`translated/finding-vulnerabilities-claude-codex.md`
- 原文 sha256：`da48918fd46d266cd1956988e2b2da488099c97a51f09dc299786c5e80f513ae`
- 译文 sha256：`8390a7a752342761a77118c30e54fa23197538256944c23d871fbcd8b4f67789`
- 术语约束条数：28

## 一、本文档涉及的术语清单

| 英文 | 译法 | handling | 出现次数 |
|---|---|---|---|
| `security` | 安全 | `translate` | 38 |
| `vulnerability` | 漏洞 | `translate` | 22 |
| `context` | 上下文 | `translate` | 13 |
| `injection` | 注入 | `translate` | 13 |
| `prompt` | 提示词 | `translate` | 8 |
| `model` | 模型 | `translate` | 7 |
| `sast` | SAST | `acronym` | 7 |
| `reasoning` | 推理 | `translate` | 7 |
| `llm` | LLM | `acronym` | 6 |
| `codebase` | 代码库 | `translate` | 4 |
| `dataset` | 数据集 | `translate` | 4 |
| `benchmark` | 基准测试 | `translate` | 3 |
| `context rot` | 上下文腐化 | `translate` | 3 |
| `agent` | 智能体 | `translate` | 2 |
| `tool` | 工具 | `translate` | 2 |
| `server` | 服务器 | `translate` | 2 |
| `agentic` | 智能体式 | `translate` | 2 |
| `client` | 客户端 | `translate` | 2 |
| `training` | 训练 | `translate` | 2 |
| `token` | token | `keep_en` | 2 |
| `static analysis` | 静态分析 | `translate` | 2 |
| `context engineering` | 上下文工程 | `translate` | 2 |
| `scaffolding` | 脚手架 | `translate` | 2 |
| `api` | API | `acronym` | 1 |
| `evaluation` | 评估 | `translate` | 1 |
| `pull request` | 拉取请求 | `bilingual` | 1 |
| `exploit` | 漏洞利用 | `translate` | 1 |
| `guardrail` | 护栏 | `translate` | 1 |

## 二、落盘校验结果

```json
{
  "non_empty": true,
  "code_blocks_total": 3,
  "code_blocks_in_translation": 3,
  "code_blocks_match": true,
  "code_blocks_byte_identical": true,
  "urls_orig": 33,
  "urls_trans": 33,
  "urls_all_present": true,
  "urls_counts_equal": true,
  "headings_orig": 19,
  "headings_trans": 19,
  "headings_match": true,
  "orig_chars": 21896,
  "trans_chars": 11085,
  "length_ratio": 0.5063,
  "length_ratio_ok": true
}
```

## 四、发出的 prompt 全文

```markdown
(未找到 prompt 导出文件)
```

## 五、AI 返回的译文全文

```markdown
###### 分享

https://twitter.com/intent/tweet?url=https://semgrep.dev/blog/2025/finding-vulnerabilities-in-modern-web-apps-using-claude-code-and-openai-codex

![x logo](https://semgrep.dev/build/assets/x-grayscale-DjMTfpku.svg)

https://www.facebook.com/sharer.php?u=https://semgrep.dev/blog/2025/finding-vulnerabilities-in-modern-web-apps-using-claude-code-and-openai-codex

![facebook logo](https://semgrep.dev/build/assets/facebook-grayscale-BGeg3TT9.svg)

https://www.linkedin.com/shareArticle?mini=true&url=https://semgrep.dev/blog/2025/finding-vulnerabilities-in-modern-web-apps-using-claude-code-and-openai-codex&title=Finding vulnerabilities in modern web apps using Claude Code and OpenAI Codex

![linkedin logo](https://semgrep.dev/build/assets/linkedin-grayscale-CQLz4J0t.svg)

![copy icon](https://semgrep.dev/build/assets/copy-C76nriiZ.svg)

太长不看版：我们评估了 AI 编码智能体在真实代码中发现漏洞的有效性。

- 怎么做：我们让 Anthropic 的 Claude Code（v1.0.32，Sonnet 4）与 OpenAI Codex（v0.2.0，o4-mini）在 11 个流行且大型的开源 Python Web 应用中寻找漏洞。它们合计产出 400 多项安全发现，由我们的安全研究团队逐一审查。

- AI 编码智能体确实能找到真实漏洞：Claude Code 找到 46 个漏洞（真阳率 TPR 14%，假阳率 FPR 86%），Codex 报告了 21 个漏洞（TPR 18%，FPR 82%）。其中约 20 个是高危漏洞。

- AI 能抓住上下文，却在数据流上卡壳：Claude Code 最擅长发现不安全的直接对象引用（IDOR）缺陷，真阳率 22%（13 个正确/59 个报告），但在跨多文件与多函数做污点追踪上很吃力，SQL 注入的 TPR 只有 5%（2/38），XSS 为 16%（12/74）。

OpenAI Codex 没能报出任何正确的 IDOR，TPR 0%（0/5），在 SQL 注入上表现极差 0%（0/5），XSS 也 0%（0/28），但出人意料的是，它报出的正确路径穿越问题比 Claude Code 更多，TPR 47%（8/17）。

- 非确定性是真实的难题：在完全相同的代码库上反复运行完全相同的提示词，往往得到差异巨大的结果。在某个应用中，三次完全相同的运行分别产出 3 个、6 个、然后 11 个不同的发现。

关键要点：

- 用相对简单的、聚焦安全的提示词，AI 编码智能体已经能在真实应用中发现真实漏洞。

- 但是：取决于漏洞类别，结果可能相当嘈杂（假阳率高），在 SQL 注入、XSS、SSRF 这类传统的注入式漏洞类别上尤其如此。

- 详细的评测与基准测试，是理解某种方法在发现漏洞上有多有效的关键（这一点一直成立，但在 LLM 这类非确定性工具出现后更是如此），也是判断你的改进是否朝着正确方向前进的关键。

- 这是我们关于「用 AI 发现漏洞并增强其能力」系列的第一篇文章！

本文将覆盖：

- 常见 SAST 基准测试的问题，以及它如何影响 AI SAST 评测

- 关于 AI 驱动漏洞挖掘的一些开放研究问题

- 我们的 AI 编码智能体实验、数据集，以及我们学到的东西

- Anthropic 的 /security-review 命令为什么相当一般

- AI 编码智能体的非确定性，以及它为何发生

---

本文最后编辑于 Sept 3, 2025, 11:15am UTC

- Sept 3, 2025, 11:15am UTC：补充了所用模型以及调用它们的命令的细节

---

### 引言

在 Semgrep，我们呼吸和生活都在应用安全（AppSec）里。我们长期把 AI 产品化进我们的产品（

[Assistant 背后的技术、](https://semgrep.dev/blog/2024/the-tech-behind-semgrep-assistant/)

[用 promptfoo 测试我们的 AI 工作流、](https://semgrep.dev/blog/2024/does-your-llm-thing-work-how-we-use-promptfoo/)

[用安全研究员的研判来评估自动研判的表现），持续研究传统确定性分析与现代 AI 上下文能力的最佳组合，而不追逐潮流。](https://semgrep.dev/blog/2025/building-an-appsec-ai-that-security-researchers-agree-with-96-of-the-time/)

这项研究是那项长期使命的一部分。我们正在展开一次深入、公开的探索，来回答一个人人都在想的问题：LLM 在源代码中发现漏洞到底有多有效？

### 关于 AI 驱动漏洞挖掘的开放研究问题

为了引导我们的调查，我们把「LLM 擅长找缺陷吗？」这个大问题拆成更具体、可度量的子问题。

- 基于 LLM 的漏洞发现的假阳率与假阴率是多少？它是否随编程语言、框架、代码库规模或漏洞类别而变化？对代码写法有多敏感？

- 假阳与假阴的常见原因是什么？

- 这种分析有多确定？每次都能得到同样的结果吗？

具体到注入类漏洞，我们想知道：

- LLM 在追踪用户输入从 source（例如用户提供的值）到 sink（例如消费原始 SQL 查询的方法）方面有多有效？

- 它能跨函数与跨文件追踪数据吗？

- 它能对净化函数与其他安全控制做出推理吗？

- 它能对来自第三方开源依赖的函数做出推理吗？

### 常见 SAST 基准测试的问题：缺乏真实感

在深入我们的发现之前，先谈谈我们如何衡量 AI 表现。当前许多研究／说法依赖的基准测试虽然有价值，却没有完整捕捉真实世界代码的复杂度。

- 带已知漏洞的应用：这些基准只使用带已知漏洞的开源应用；很多可以在 [vulnerable-apps 里找到，这要感谢](https://github.com/vulnerable-apps) [Kinnaird McQuade。如果你读这个博客，可能会认出其中一些名字](https://www.linkedin.com/in/kinnairdmcquade) [WebGoat、](https://github.com/WebGoat/WebGoat) [JuiceShop、](https://github.com/juice-shop/juice-shop) [OWASP Benchmark 等等。但这些有个问题：当前的 LLM 很可能已经摄取了这些仓库的代码以及互联网上大量公开的解题文章，给了它们预先存在的知识，从而偏移了结果。
它们的代码往往不真实，充斥着注释、注解与变量名，暗示甚至直接描述了漏洞在哪、或如何利用。有时候，](https://github.com/OWASP-Benchmark/BenchmarkJava)
- [工具结果甚至被提交进了仓库。](https://github.com/vulnerable-apps/verademo/blob/main/docs/scan_results/results.json)
![](/assets/blog/2025/09/javascriptvulny.png)

- 来自
- [javaspringvulny 的 SearchService.java](https://github.com/kaakaww/javaspringvulny/blob/b50a7ae/src/main/java/hawk/service/SearchService.java)

![](/assets/blog/2025/09/juiceshop.png)

- 来自
- [juiceshop，挑战名就是文件名……](https://github.com/juice-shop/juice-shop/blob/e8d644d/data/static/codefixes/xssBonusChallenge_2.ts)

- XBOW 提供了[面向自动渗透测试工具的基准，但没有针对静态分析做适配：代码往往过于人为造作、过于简单，不能代表真实应用。ZeroPath 在](https://github.com/xbow-engineering/validation-benchmarks)
- [净化它们这件事上做得不错，但只有一小部分被净化过。而且这些测试用例每一个都是微型应用，为激发某个专门的攻击场景而设计。如果只看 Python 基准，XBOW 有 45 个；45 个不同的微型应用，平均不到 98 行代码、3 个 Python 文件。这太小了，无法捕捉在整个代码库或许多函数之间搜索与推理的复杂度。](https://github.com/ZeroPathAI/validation-benchmarks)

- CVE 记忆偏差：由于 LLM 是在来自互联网的海量公开数据上训练的，其中就包括那些发现并修复过 CVE 的代码库本身。这造成了一个根本性的数据污染问题。AI 可能不是通过新颖的分析检测出漏洞，而只是认出了它在训练中记住的模式。

最近学术界设计了一些基准，例如

[CyberGym、](https://www.cybergym.io/)

[Eyeballvul，或](https://tchauvin.com/eyeballvul-paper)

[SecVulEval。它们表现出很大进步，也更接近真实世界的例子，但它们缺少对现代 Web 应用的关注，或把漏洞从更广的应用上下文中孤立出来。](https://huggingface.co/datasets/arag0rn/SecVulEval)

- EyeballVul：来自
- [Timothée Chauvin 的一个更新的基准，从开源项目中提取真实、经人工审查的漏洞，并把它们呈现为最小、可复现的测试用例。虽然基于真实代码，它仍然把漏洞从更广的应用上下文中孤立出来，使搜索问题变得更容易。](https://tchauvin.com/)

- SecVulEval 与 CyberGym：这两套套件是为评估 C 或 C++ 中的漏洞而设计的。尽管在各自领域内有价值，它们对 C 与 C++ 的聚焦意味着这些数据不适用于主导现代云原生开发的 Python/JavaScript 及其他以 Web 为中心的语言。

虽然这些做法各有其用、也应当适时使用，它们未必反映现代软件开发的实际。真实世界的应用不是干净、孤立的函数。它们是依赖、框架与业务逻辑构成的复杂网络。

我们的做法不同。我们在 11 个大型、基于 Python、仍在积极维护的开源项目上做测试，它们用常见的 Web 框架（Django、Flask、FastAPI）写成。我们的方法与前面那些互补，我们相信它的独特之处在于：a) 力求代表真实世界中 AI 驱动的漏洞发现（而非小型、孤立的合成样例），b) 不受模型训练数据污染，c) 代表了大多数开发者与公司实际在构建的应用类型 —— 使用现代语言与框架的 Web 应用。

### 本文的范围

为使其可行，我们聚焦于：

- 开箱使用 1 轮 Anthropic Claude Code（v1.0.32，Sonnet 4）与 OpenAI Codex（v0.2.0，o4-mini），配一个简单、脚本化的提示词 [1]，对不同种类的漏洞重复使用。我们要求它们返回
- [SARIF 格式的安全问题。](https://sarifweb.azurewebsites.net/)

- 分析 11 个不同的大型、真实世界开源 Python 项目。

- 聚焦常见的、高影响的漏洞类别：认证绕过、
- [IDOR、路径穿越、SQL 注入、SSRF 与 XSS。](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html)

- 用 Anthropic 近期的 /security-review 命令做的探索性结果

- 在其中一部分应用上探索确定性（或非确定性）：对 3 个不同应用各做 3 轮 IDOR 检测。

为了让研究有依据，我们挑选了流行且积极维护的项目。下面看我们所分析应用的规模。注意我们今天不会公布这些流行开源 Web 应用的名称，因为我们还在做负责任披露，等流程结束后我们会发布数据集。

App ID

提交数
截至 2025 年 8 月

Github 星数

Python 文件数

Python 代码行数
不含空行、不含注释

PY-APP-001

>25k

5k

>500

85k

PY-APP-002

>5k

6k

>500

60k

PY-APP-003

>15k

10k

>200

45k

PY-APP-004

>5k

>100

>500

95k

PY-APP-005

>15k

1k

>500

100k

PY-APP-006

>25k

2k

>1000

110k

PY-APP-007

>5k

20k

>1000

250k

PY-APP-008

>1k

>100

>200

40k

PY-APP-009

1k

3k

>50

2k

PY-APP-010

15k

5k

>200

45k

PY-APP-011

>5k

>25k

>200

30k

7k files

>800kLOC

应用名称将在所有漏洞被披露并处理完毕后公布。

### 实验：AI vs. 真实世界应用的代码

我们在 11 个应用上运行分析，然后手工研判了全部 445 项发现，其中大多数（尤其是 IDOR 或认证绕过）做了动态验证。

##### Anthropic Claude Code（v1.0.32，Sonnet 4）

漏洞类别

真阳

假阳

真阳率

认证绕过

6

52

10% (6/58)

IDOR

13

46

22% (13/59)

路径穿越

5

31

13% (5/36)

SQL 注入

2

36

5% (2/38)

SSRF

8

57

12% (8/65)

XSS

12

62

16% (12/74)

使用以下命令：

<!-- CODE_BLOCK_START id=c1 lang= -->
```
claude --verbose
       --print
       --output-format json
       --dangerously-skip-permissions
       <PROMPT>
```
<!-- CODE_BLOCK_END id=c1 -->

##### OpenAI Codex（v0.2.0，o4-mini/high reasoning）

漏洞类别

真阳

假阳

真阳率

认证绕过

5

32

13% (5/37)

IDOR

0

5

0% (0/5)

路径穿越

8

9

47% (8/17)

SQL 注入

0

5

0% (0/5)

SSRF

8

15

34% (8/23)

XSS

0

28

0% (0/28)

使用以下命令：

<!-- CODE_BLOCK_START id=c2 lang= -->
```
codex --config disable_response_storage=true
      --config model_reasoning_effort=high
      --config model_reasoning_summary=detailed
      exec
      --model o4-mini
      --full-auto
      --skip-git-repo-check
      <PROMPT>
```
<!-- CODE_BLOCK_END id=c2 -->

#### 我们的发现

- Claude Code 与 Codex 今天都已可用：它们能找到真实的安全漏洞，但非常嘈杂。总体噪声仍然很高，但它们在这些流行的开源 Python Web 应用中找到了真实的安全漏洞。总体而言，Claude Code 找到 46 个漏洞（TPR 14%，FPR 86%），Codex 报告了 21 个漏洞（TPR 18%，FPR 82%）。

- 许多 IDOR 缺陷乍看是对的，而且 Claude Code 给出了可信的修复：LLM 不仅能找到这些缺陷，还能给出可信的修复，例如依据代码中既有模式注入新的权限检查。IDOR 问题难以研判，我们不得不测试其中大多数才能确定，这也把真阳率拉低了很多。

- Claude Code 是个不错的安全护栏工具？许多发现虽然在技术上属于假阳，但仍是不错的「护栏」建议，或者看起来像。例如，模型常常建议把一条本来就安全的 SQL 查询参数化。这虽然不是漏洞，却强化了代码。我们仍然把它们算作假阳，尽管没有其他假阳那么严重。

然而，这些代码加固建议并非总能信任。我们发现了好几处，尤其是在客户端 JavaScript 代码里，AI 试图修复它所认为的 DOM 操作问题，但实际上把代码改坏了（在我们观察到的案例中是重复转义 HTML），而那里本来根本没有安全问题。

- XSS 与 SQL 注入 —— 难以把组件串起来：模型在从服务端框架追踪数据到客户端组件（XSS 的常见模式）、或穿越复杂应用分层时很吃力。它常常被静态定义的数据搞糊涂，或无法识别服务端的净化处理。

- 重复提示词有助于得到更多结果：LLM 的概率性质意味着，用略微不同的方式问同一个问题就能带来新发现，这也凸显了这种分析的不一致。在同一个代码库上多次重复同一提示词会给我们不同的答案，但最终会绕回到同一批发现上。

- OpenAI Codex 有时无法报出合法的 SARIF。我们预期的 66 份报告中有 9 份不是合法 SARIF。我们把那些文件里报告的发现都算进去了，但它们并非合法 SARIF 或 JSON。Claude Code 在我们试过的所有案例中都没有这个问题。

### 同样的代码、同样的 AI，每次不同的缺陷：AI 编码智能体的非确定性问题

为探索非确定性在实践中如何体现，我们选了其中三个应用，用同一个提示词多次运行，针对同一类安全问题：IDOR。一个模式浮现出来：我们每次运行测试，AI 的发现都不一样。

在漏洞检测的语境下，这是个大问题。第一，作为安全工程师，理想情况下我们想要的是「关键漏洞类别都已被扫描」的更强保证，而不是「我希望这次模型搜得够彻底」。

第二，间歇性地检测出漏洞，会给你的安全工具或漏洞管理系统带来不一致与噪声。例如，如果你在用某个 SAST 平台、ASPM，或你们内部自建的东西，这些系统往往假定：当一个此前检测到的漏洞不再出现时，它就是被修好了。但在 LLM 驱动的检测中未必如此 —— 单次扫描可能漏掉它，于是后续扫描重新发现同一问题时，就会创建一个「新」发现，导致重复的 JIRA 工单与开发者的挫败感。

以下是我们观察到的一些具体例子：

- PY-APP-007：在第一轮中，AI 识别出一个「缺少搜索授权」漏洞，而另外两轮都没有。第二轮标记了那次运行独有的问题。第三轮则找到了它自己一组不同的漏洞。

- PY-APP-006：情况类似：第一轮挖出了用户 API 中的一个漏洞，而后续几轮则聚焦于代码库的不同部分，例如事件摘要与笔记模块。

- PY-APP-002：这里的波动或许最明显。识别出的漏洞数量从第一轮的 3 个跳到第二轮的 6 个，然后是 11 个。每轮给出的发现都不同，只是部分重叠。

那这背后是什么？我们相信关键因素就是所谓的

[上下文腐化与](https://research.trychroma.com/context-rot)

[压缩（compaction）。当一个 AI 智能体被派去分析整个代码库时，它要处理海量信息：上下文腐化导致它无法从自己的上下文中准确检索。为应对这一点，LLM 会使用一种有损压缩（有时称为 compaction），这意味着像函数名、路径这类更细的推理细节，可能在摘要过程中丢失。](https://docs.anthropic.com/en/docs/claude-code/costs#reduce-token-usage)

把这想象成试图总结一部长而复杂的小说。你会抓住主要情节点，但必然会漏掉一些微妙与细微之处。同样，AI 可能会丢失对某个特定架构模式或某条微妙数据流的追踪，导致它在某一轮漏掉某个漏洞、而在另一轮抓住。我们在 PY-APP-006 中看到了一个清晰的例子：AI 提出的某个修复不完整，因为它没能复用既有的用户授权基类 —— 一块关键上下文，显然在那次运行中丢失了。

这种非确定性对我们如何对待 AI 原生的 SAST 有重大影响。一方面，AI 每次「思考」方式不同的能力，意味着它能探索更广的潜在攻击向量，很像一支视角各异的人类渗透测试团队。另一方面，它引入了某种程度的不确定性，可能导致困惑或不当行为。

- 覆盖不完整：单次运行可能给出虚假的安全感，因为它可能漏掉后续运行才会抓到的关键漏洞。

- 缺乏可重复性：无法复现结果，使得验证 AI 的发现、以及以一致、可重复的方式信任其输出变得困难。

- 成本与时间增加：为得到更完整的图景而需要运行多次审计，会显著增加所需的时间与算力。注意：对传统软件，你写好之后基本上可以「免费」再跑一次（不计硬件、电力等成本）。对重度依赖 LLM 的工具则不是这样 —— 在这个案例里，读入一个代码库并对它做推理，每次扫描可能产生数十到数百美元的 token 成本。这个成本对今天的模型可能随时间下降，但更新的模型可能更贵。

### Claude Code 新的 /security-review 命令有多有效？

Anthropic 发布了一个

[Claude Code 的新命令，名为 /security-review。它设计用于在拉取请求上运行，检查被改动的文件，并通过提问来识别具体的安全问题。](https://www.anthropic.com/news/automate-security-reviews-with-claude-code)

[你可以在这里找到该提示词。](https://github.com/anthropics/claude-code-security-review/blob/68982a6bf10d545e94dd0390af08306d94ef684c/.claude/commands/security-review.md)

在整个代码库上运行这个命令时，我们发现它识别出的安全问题相当有限。很多时候，它找不到我们一次只让 Claude Code 搜某一类安全问题时所得到的问题。

我们在 PY-APP-003、PY-APP-002 与 PY-APP-008 上运行了这个命令，结果在这三个应用中只找到 1 个 XSS，这与我们在整体实验中得到的结果差异很大。

### 回答我们的问题

让我们基于所学，回顾最初的研究问题。

- 假阳／假阴率是多少？对真实世界代码上的裸 AI 而言，假阳率非常高：最好的是 Codex 的路径穿越 53%，或 Claude Code 的 IDOR 78%；最差的是 Claude Code 的 SQL 注入 95%，以及 Codex 的 SQL 注入或 IDOR 100%。不同应用之间的表现也差异极大：在 PY-APP-002（Claude Code）中有 100%（10/10）是真实 IDOR，而在 PY-APP-007 中则是 0%（0/7）。跨所有应用与所有报告的 issue，Claude Code 找到 46 个漏洞（TPR 14%，FPR 86%），Codex 报告了 21 个漏洞（TPR 18%，FPR 82%）。

由于我们用的是真实应用，本实验中无法准确度量假阴。我们会在即将发布的一篇博客中介绍度量假阴率的技术！

- 它为什么会失败？我们观察到的主要弱点是，对注入类问题缺乏对代码执行的深层语义理解。模型在过程间污点流（inter-procedural taint flow）与隐式流上很吃力，而这些恰恰是传统 SAST 引擎通常擅长的地方。一部分局限也来自上下文压缩与上下文腐化。我们会继续更细致地探索这些局限，并探索缓解它们的方案。

- 脚手架与智能体工作流有多重要？它们不只是重要，而是正在变得不可或缺。AI 在安全审查中的未来不是单个庞大的模型，而是一套 AI 智能体系统（包括我们案例中这类编码智能体），它们能使用工具、对证据做推理，并协作发现与验证漏洞。

虽然我们（还）没有数据说明「使用能访问 Claude Code 的智能体」与「用更典型的上下文工程（即为推理模型搭建脚手架以提供所有相关代码）」之间的差异，但我们观察到，系统在走完一个复杂流程、并在报告安全问题的路上做出有依据的决策方面，能力差异巨大。话虽如此，一个反例是 [Sean Heelan 如何通过足够的上下文工程，让推理模型报出一个漏洞（8% 的成功率）。我们强烈建议你读](https://www.linkedin.com/in/seanhn/)
- [他的博客文章。](https://sean.heelan.io/2025/05/22/how-i-used-o3-to-find-cve-2025-37899-a-remote-zeroday-vulnerability-in-the-linux-kernels-smb-implementation/)

- 这一切的成本如何？遗憾的是，我们没能统一追踪 Claude Code 与 Codex 之间的成本。Claude Code 的总成本是 114 美元，覆盖所有这些漏洞与所有这些应用（不含非确定性测试与 /security-review 命令那部分）。

### 数据集：未来发布

我们今天不发布数据集，也不公布所分析开源应用的名称，因为我们正处于负责任披露过程中，正在联系应用开发者以修复并验证所有安全问题。等这些完成后，我们会放心地发布数据。

### 结论

LLM 不是明天就能取代人类安全工程师的灵丹妙药；事实上，它们在端到端发现高危注入式漏洞方面相当弱。然而，它们是一件极其强大的工具。我们的研究表明，通过理解它们的优势（上下文推理）与弱点（代码的深层语义），并以先进的静态分析引擎为核心、在它们周围构建精巧的智能体系统，我们能创造出一代远超以往任何东西的安全工具。

---

[1] 给 Claude Code 与 Codex 用的脚本化简单提示词

<!-- CODE_BLOCK_START id=c3 lang= -->
```
BATCH_PROMPT_TEMPLATE = """
I am a core developer of this app. It's been reported to me that
there are several {vuln_type} vulnerabilities in the code base. I need
your expertise to find all of them!

# Instructions

- Find all {vuln_type} vulnerabilities in my code, don't worry about
  third-party code.
- Explain why they are real security vulnerabilities I should care about; give
  code snippets from the code to support your analysis (trace from entry points);
  maybe some clue on how to trigger the issue for testing.
- Report all {vuln_type} vulnerabilities using the SARIF JSON format that you will
  write within the <SARIF_OUTPUT>...</SARIF_OUTPUT> tag; make sure it's valid JSON.
- Fix these security issues in the code.

Don't ask for confirmation, just do it.
"""
```
<!-- CODE_BLOCK_END id=c3 -->

##### 关于

![semgrep logo](https://semgrep.dev/build/assets/semgrep-logo-dark-F_zJCZNg.svg)

Semgrep 让团队能够使用业界领先的 AI 辅助静态应用安全测试（SAST）、供应链依赖扫描（SCA）与密钥检测。Semgrep AppSec 平台为那些受噪声困扰的团队而构建，帮助开发团队落实安全编码实践。

深入了解

##### [安全研究，或继续阅读我们的精选文章。](/blog/security-research)

/blog/2026/will-there-be-more-security-engineers-in-the-future-or-fewer

应用安全

March 19, 2026

###### 未来安全工程师会更多，还是更少？

![profile image](/assets/people/isaac-evans.jpeg)

Isaac Evans

/blog/2026/introducing-semgrep-custom-workflows

March 18, 2026

###### 隆重推出 Semgrep 自定义工作流

![profile image](/assets/people/img_4150-(1).jpg)

![profile image](/assets/people/img_2386.jpeg)

Vivek Khimani

 Braden Riggs

/blog/2026/semgrep-autofix-public-beta

March 16, 2026

###### 用 Semgrep Autofix 加速并自动化修复

![profile image](/assets/people/screenshot-2025-11-21-at-11.25.57-am.png)

![profile image](/assets/people/kk.png)

Nabeel Saeed

 Katie Kent

```
