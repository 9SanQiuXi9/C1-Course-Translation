# 翻译留痕：sast-vs-dast

- doc_id：`sast-vs-dast`
- 时间：2026-09-27T17:10:28+08:00
- 原文：`extracted/sast-vs-dast.md`
- 译文：`translated/sast-vs-dast.md`
- 原文 sha256：`bcea5fae6ba566537285b75bddfe2a2997820ecc948bfb32e85552644b1ab2dd`
- 译文 sha256：`a7cdc0778fee2dbbf5589ac690762f42ff6745771cc1ed58fde171e3487f964a`
- 术语约束条数：22

## 一、本文档涉及的术语清单

| 英文 | 译法 | handling | 出现次数 |
|---|---|---|---|
| `sast` | SAST | `acronym` | 63 |
| `dast` | DAST | `acronym` | 54 |
| `security` | 安全 | `translate` | 38 |
| `vulnerability` | 漏洞 | `translate` | 8 |
| `tool` | 工具 | `translate` | 6 |
| `ci/cd` | CI/CD | `acronym` | 6 |
| `api` | API | `acronym` | 5 |
| `deployment` | 部署 | `translate` | 5 |
| `observability` | 可观测性 | `translate` | 5 |
| `codebase` | 代码库 | `translate` | 4 |
| `injection` | 注入 | `translate` | 4 |
| `machine learning` | 机器学习 | `translate` | 4 |
| `pipeline` | 流水线 | `translate` | 4 |
| `server` | 服务器 | `translate` | 3 |
| `automation` | 自动化 | `translate` | 2 |
| `monitoring` | 监控 | `translate` | 2 |
| `exploit` | 漏洞利用 | `translate` | 2 |
| `best practices` | 最佳实践 | `translate` | 1 |
| `tracing` | 链路追踪 | `translate` | 1 |
| `repository` | 仓库 | `translate` | 1 |
| `refactor` | 重构 | `translate` | 1 |
| `eval` | 评估 | `translate` | 1 |

## 二、落盘校验结果

```json
{
  "non_empty": true,
  "code_blocks_total": 0,
  "code_blocks_in_translation": 0,
  "code_blocks_match": true,
  "code_blocks_byte_identical": true,
  "urls_orig": 10,
  "urls_trans": 10,
  "urls_all_present": true,
  "urls_counts_equal": true,
  "headings_orig": 29,
  "headings_trans": 29,
  "headings_match": true,
  "orig_chars": 19089,
  "trans_chars": 8617,
  "length_ratio": 0.4514,
  "length_ratio_ok": true
}
```

## 四、发出的 prompt 全文

```markdown
(未找到 prompt 导出文件)
```

## 五、AI 返回的译文全文

```markdown
## SAST vs. DAST vs. RASP：比较应用安全测试方法

[Learn December 18, 2024](https://www.splunk.com/en_us/blog/learn.html)

[Shanika Wickramasinghe](/en_us/blog/author/shanika-wickramasinghe.html)

全球信息安全支出预计到

[2025 年将达到 2120 亿美元。这比 2024 年增长 15%。Gartner 认为，](https://www.gartner.com/en/newsroom/press-releases/2024-08-28-gartner-forecasts-global-information-security-spending-to-grow-15-percent-in-2025)

[生成式 AI 的兴起与云的采用是这一快速增长的关键原因。该分析机构进一步预测，到 2027 年，GenAI 将参与所有](/en_us/blog/learn/generative-ai.html)

[网络攻击中的 17%。](/en_us/blog/learn/cybersecurity-attacks.html)

企业需要超越传统方法的先进安全策略来应对这些日益增长的威胁。这就是为什么企业主需要了解 SAST、DAST 与 RASP 这类安全方案，因为它们为应用提供多层防护。

（延伸阅读：

[应用安全详解与](/en_us/blog/learn/application-security-requirements.html)

[常见软件测试方法。）](/en_us/blog/learn/software-testing.html)

# 什么是 SAST？

静态应用安全测试（SAST）是一种

[白盒安全测试方法。SAST](https://en.wikipedia.org/wiki/White-box_testing)

[使用应用的静态源代码或二进制文件来识别漏洞。这意味着 SAST 工具在应用未运行时对其代码进行分析。](/en_us/blog/learn/static-code-analysis.html)

开发者用 SAST 检测各类安全风险，例如：

[跨站脚本（XSS）、不安全的反序列化、缓冲区溢出，以及](/en_us/blog/learn/cross-site-scripting-xss-attacks.html)

[代码中的其他 OWASP 漏洞。由于单靠 SAST 无法识别运行时特有的漏洞，开发者往往必须把 SAST 与其他测试方法结合，才能实现全面的安全。](/en_us/blog/learn/owasp-top-10.html)

SAST 是

[软件开发生命周期的重要组成部分，因为它能尽早发现漏洞。发现得越早，修复成本越低。由于 SAST 工具可以在开发阶段执行，开发者如今能在把产品推向市场之前写代码并测试它多达一千次（！！）。](/en_us/blog/learn/software-development-lifecycle-sdlc.html)

SAST 可以集成进

[CI/CD 流水线，这么做时就称为「Secure DevOps」或「](/en_us/blog/learn/ci-cd-devops-pipeline.html)

[DevSecOps」。SAST 通过自动化可以广泛扩展。能够实现覆盖 SAST 技术的自动化测试，使它成为快速应对代码级风险的高效方案。](/en_us/blog/learn/devsecops-concepts-principles.html)

## 什么是 DAST？

动态应用安全测试是一种

[黑盒测试方法。](https://en.wikipedia.org/wiki/Black-box_testing)

[DAST 中的「动态」一词表明，这种方法在应用运行时评估其安全性。与 SAST 不同，DAST 不需要访问应用的源代码。相反，它：](https://en.wikipedia.org/wiki/Dynamic_application_security_testing)

1. 模拟外部攻击者的行为。从外部测试应用，以
2. [识别只在运行时才出现的漏洞。](/en_us/blog/learn/vulnerability-types.html)

DAST 能够识别多种安全缺陷，例如拒绝服务（DoS）漏洞与不安全的服务器配置。通过模仿真实世界的攻击场景，DAST 工具评估应用如何响应这些模拟威胁。借助这种做法，开发者能发现静态测试方法（如 SAST）可能漏掉的弱点。

通常，开发者在软件开发生命周期的后期阶段执行 DAST，往往就在部署之前。通过在真实环境中测试应用，DAST 提供了运行时安全的清晰概览，并有助于打造性能更好、能抵御潜在攻击的应用。

## SAST 如何工作？

开发者使用

[SAST 工具施加预定义规则与其他检测方法 —— 例如模式匹配与数据流分析 —— 来识别编码错误与其他漏洞。他们把这些工具集成进自己的 IDE 或 CI/CD 流水线，在编码与测试阶段自动化扫描。](https://en.wikipedia.org/wiki/List_of_tools_for_static_code_analysis)

### 常见的 SAST 方法

以下是 SAST 中用到的一些方法。

![常见的静态应用安全测试方法](/content/dam/splunk-blogs/images/media_14bcb87a7461de3b7ba525cf6cf4c9c17338a9433/common-static-aplication-security-testing-methods.avif?width=750&format=avif&optimize=medium)

模式匹配会在代码库中扫描已知的不安全编码实践模式。例如使用弱加密算法或不安全的 API 调用。

数据流（Data flow）追踪数据如何在应用中流动。通过追踪不可信输入到达敏感操作的路径，它可以识别

[SQL 注入或缓冲区溢出这类漏洞。](/en_us/blog/learn/sql-injection.html)

控制流分析可以分析应用的控制结构。例如循环与条件分支，以揭示逻辑缺陷或竞态条件等潜在漏洞。

自定义规则创建。许多工具允许开发者创建自定义规则来落实编码最佳实践。以下是这些自定义规则的一些例子：

- 标记 SQL 查询中任何使用未净化输入的地方。
- 识别把用户提供的数据未经恰当转义就输出到浏览器的代码。
- 高亮标记脆弱或已废弃函数的使用，例如 JavaScript 中的 eval() 或 C 中的 strcpy()。
- 检测源代码中硬编码的 API key 与密码，并标记任何对用户提供数据缺少输入校验的地方。

依赖扫描。一些 SAST 工具会分析应用中使用的第三方库与框架，以识别依赖中的漏洞。

语义分析。通过解读代码的含义而不只是它的结构，SAST 工具能检测不安全的配置或 API 的误用。

机器学习模型：先进的 SAST 工具引入机器学习算法，通过分析大规模数据集中的模式来识别此前未知的漏洞。

### 使用 SAST 工具时的性能考量

SAST 工具往往需要

[大量 CPU 与内存资源。在分析大型代码库时，这可能是个大问题。对一百万行代码做一次完整扫描可能消耗数 GB 内存。](/en_us/blog/learn/cpu-vs-gpu.html)

SAST 扫描所需的时间会因代码库规模而有巨大差异，小型项目只需几分钟，企业级应用则可能长达数小时。这可能影响：

- 构建流水线的工期
- [开发者生产力](/en_us/blog/learn/dpe-developer-productivity-engineering.html)

考虑使用支持增量扫描的现代 SAST 工具，让你只分析变更过的代码，而不是整个代码库。

此外，通过规则选择与范围界定来做性能调优至关重要。配置不当的 SAST 工具会毫无必要地分析非关键代码路径，既浪费时间与资源，又带不来安全收益。

## DAST 如何工作？

DAST 工具模拟真实世界的攻击 —— 例如向输入字段发送各种形式的恶意数据，看应用如何处理它 —— 以识别应用行为与响应中的漏洞与弱点。

### DAST 的步骤

该过程通常包含以下步骤。

![动态应用安全测试步骤](/content/dam/splunk-blogs/images/media_1aece54bbf699307808799045108b90d64c19ee54/dynamic-application-security-testing-steps.avif?width=750&format=avif&optimize=medium)

第 1 步：扫描。扫描 Web 应用以发现入口点（如 URL、表单与 API）。这一步测绘出应用的结构，并识别

[潜在攻击面。](/en_us/blog/learn/attack-surfaces.html)

第 2 步：攻击模拟。通过向应用发送构造好的请求来模拟恶意活动。这些请求通过尝试利用入口点，来测试跨站脚本与跨站请求伪造等漏洞。

第 3 步：漏洞检测。分析应用的响应以识别安全弱点。它评估应用在攻击下是否表现如预期。例如，可以注入恶意数据以检测 SQL 注入缺陷。

第 4 步：报告。生成包含所检测到的漏洞与修复建议的报告。开发者可以利用报告中的结果修复所发现的问题。

现代 DAST 方案可以引入先进特性，例如 AI 驱动的分析与

[实时数据集成。它们自动创建测试集。用机器学习算法动态适应应用的结构，并最大限度减少误报。](/en_us/blog/learn/real-time-data.html)

### 使用 DAST 工具时的性能考量

使用 DAST 工具时有几个性能瓶颈需要留意。

- DAST 工具会主动与运行中的应用交互，暂时提高应用与 Web 服务器双方的 CPU 与内存占用。
- DAST 扫描期间产生的大量并发请求会消耗可观的网络带宽。
- DAST 扫描器常常通过生成唯一请求来绕过或使应用缓存失效，降低缓存机制的有效性。
- DAST 工具创建并管理多个测试会话，会提高应用服务器的内存占用。

为避免这类问题或尽可能减轻其影响，请遵循以下做法。

- 把 DAST 扫描安排在应用使用量最少的非高峰时段。
- 在与生产环境配置一致的分阶段或预发环境中执行扫描。
- 使用 DAST 工具中的限流功能来控制同时请求数。
- 在扫描期间提高应用服务器的线程池。
- 为 DAST 扫描器的 IP 配置独立的缓存策略。
- 实现超出性能阈值时自动暂停扫描。

## SAST vs. DAST：关键区别

下表总结了 SAST 与 DAST 的区别。

## SAST 与 DAST 的优缺点

### SAST 的优点

- 在软件开发生命周期的早期就识别安全漏洞。
- 分析代码库，包括基本函数与复杂分支。
- 直接作用于源代码，不要求应用运行。
- 提供实时反馈与全面洞见，例如漏洞的确切位置。
- 生成可导出的报告，可用仪表盘跟踪。
- 支持自动化，因此比人工代码审查更快、更高效。

### SAST 的缺点

- 常常产生大量误报。因此可能需要人工复查。
- 无法识别运行时或环境特有的漏洞，例如配置错误。
- 需要针对每种编程语言的专用工具，因此维护复杂。
- 在理解外部库、API 与 REST 端点方面比较吃力。

### DAST 的优点

- 识别只在应用执行期间才出现的漏洞。
- 从外部运作，无需访问源代码。这对测试第三方应用或已编译代码很有效。
- 模拟实际攻击场景，识别 SAST 漏掉的风险。
- 不依赖应用的编程语言。
- 评估整个应用与系统。包括内存消耗、资源使用以及第三方接口。

### DAST 的缺点

- 只关注应用的外层，可能漏掉更深层的漏洞。
- 在 SDLC 中应用得较晚，因此修复更昂贵、更耗时。
- 会漏掉某些 SAST 工具通过源代码分析能识别出的漏洞。举个例子，设想一个 Web 应用使用不安全的随机数生成器（例如 JavaScript 中的 Math.random()）来创建会话令牌。DAST 可能漏掉这个缺陷，因为它只测试运行时行为。（但 SAST 能检测到它。）
- 对大型项目需要定制基础设施，并需要多个应用实例并行运行，因此资源消耗大。

## 我该在什么时候用 SAST、什么时候用 DAST？

SAST 与 DAST 在保障 SDLC 安全上扮演互补的角色。理解各自何时使用，有助于获得全面的安全覆盖。

### 何时使用 SAST

在开发早期阶段。开发者用 SAST 在 SDLC 早期识别 SQL 注入与硬编码凭据这类漏洞。在部署前抓住这些问题，能降低修复成本与复杂度。

例如：一个 SAST 工具扫描 Python 代码，标记出源代码中嵌入了硬编码 API key 的漏洞。开发者重构代码，改用环境变量来安全地存储与获取这些 key。

用于代码审查。SAST 可集成进版本控制系统。让开发者在提交代码前先扫描。这确保只有安全的代码进入仓库。

示例：SAST 工具能检测出这样一个漏洞 —— 文件路径直接由用户输入拼接而成、未经校验，使应用暴露于路径穿越攻击。开发者通过净化输入、并使用安全的库函数处理文件路径来修复该问题。

在持续集成／持续部署流水线中。SAST 在 CI/CD 过程中运行自动扫描。它为开发者提供实时反馈。

### 何时使用 DAST

生产前测试。开发者在分阶段或 QA 环境中用 DAST 识别运行时漏洞（例如不安全的配置、认证缺陷、访问控制不足）。

示例：DAST 工具能检测出暴露敏感数据的数据库配置错误。然后开发者可以在部署前加固该配置。

用于部署后监控。DAST 工具持续扫描已部署的应用，找出环境变化或新兴威胁所导致的漏洞。这保证应用长期保持安全。

测试第三方集成。DAST 可以模仿外部攻击者的视角，识别第三方 API 或互联系统中的漏洞。

例如：一个 DAST 工具测试某个 Web 应用，发现在第三方支付 API 中存在漏洞 —— 信用卡信息通过未加密的 HTTP 连接传输。开发者通过强制所有 API 通信使用 HTTPS 来解决该问题。

## 哪个更有效：SAST 还是 DAST？

SAST 或 DAST 的有效性取决于：

- 所处的 SDLC 阶段
- 所应对的漏洞类型

SAST 在开发早期效果最好，主要用于识别源代码中的漏洞、降低成本并推广安全编码实践。相比之下，DAST 关注预发或已部署应用中的运行时漏洞。它提供关于配置错误与不安全集成等问题的洞见。

### 采用混合做法

与其在两者中选一个，不如把 SAST 与 DAST 结合起来，形成一套多层安全策略，同时应对静态代码与运行时环境中的漏洞。SAST 可以集成进开发早期阶段，在应用编译之前检测并修复代码级问题。一旦应用在测试环境中运行起来，DAST 就能识别运行时漏洞，并评估应用在攻击条件下的行为。

在 CI/CD 流水线中把 SAST 与 DAST 扫描都自动化，能提供持续反馈，并在不牺牲安全的前提下加速开发过程。

对敏捷或 DevOps 环境而言，加入 IAST 或 RASP 这类工具能进一步增强安全。通过把 SAST 与 DAST 的结果相互关联，组织可以实现更全面、

[更有效的漏洞管理。](/en_us/blog/learn/vulnerability-management.html)

### 用 RASP 作为 SAST 与 DAST 的替代方案

运行时应用自我保护（RASP）是一种高级安全方案，直接安装在

[应用所运行的服务器上。](/en_us/blog/learn/computer-servers.html)

RASP 把自身嵌入应用的运行时环境。这种集成让 RASP 能分析应用的逻辑与数据。在分析过程中，它能够：

1. 在异常行为发生时检测到它们。
2. 立即阻断恶意活动。

一个关键区别是：RASP 不只是对潜在问题发出告警 —— 它通过隔离并解决威胁来主动阻止攻击，而不依赖外部工具。

RASP 提供了 SAST 与 DAST 之外的一种动态选择。不像分析静态代码的 SAST、也不像模拟外部攻击的 DAST，RASP 实时运作。它在执行期间监控应用的行为，并通过终止会话或通知防御者来响应实时威胁。

RASP 在保护应用免受那些绕过网络防御、或在开发期间被漏掉的漏洞方面尤其有效。

然而，对 RASP 过度自信可能导致组织忽视安全编码实践。此外，RASP 可能影响应用性能，因为它直接运行在应用的运行时环境内。RASP 无法替代修复底层缺陷的必要性，但它能在修复进行期间提供持续保护。

正如

[一位 RASP 用户所评论的：](https://www.gartner.com/peer-community/post/talking-about-app-security-use-rast-tool-substitute-security-control-valuable-add-it-not-valuable-at)

「是否使用 RASP 工具，应当基于对应用具体需求与风险画像的全面评估。」

## 未来是 SAST、DAST 与 RASP 并举的 AppSec 测试

应用测试的未来在于把 SAST、DAST 与 RASP 结合起来，形成一套全面的安全策略。随着安全挑战加剧，把这些工具集成进 CI/CD 流水线并自动化其流程将变得不可或缺。

AI 与机器学习的进步会让测试更高效，因为它有助于减少误报并改善威胁检测。

### 金融与金融科技行业

在金融领域，AI 驱动的工具将改变漏洞被检测与缓解的方式。SAST 与 DAST 会继续在开发与预发阶段识别编码缺陷与运行时问题。

但你不会止步于此：RASP 会用 AI 走得更远，

[去监控实时交易。例如，RASP 可以检测出异常模式（例如攻击者试图实时利用某个漏洞），并阻断这些活动、同时通知安全团队。](/en_us/blog/learn/continuous-monitoring.html)

### IoT、边缘与联网设备

在 IoT 方面，这些工具的组合将在保护联网设备上发挥重要作用。具体如下：

- SAST 可以在开发期间确认固件没有漏洞。
- DAST 可以测试设备之间通信协议的安全性。
- 而 RASP 则监控已部署的设备，检测并阻止未授权访问尝试或新兴威胁导致的数据泄漏。

同样，使用多种方法有助于让 IoT 生态保持韧性。正如我们众多示例所展示的，SAST、DAST 与 RASP 合在一起，承诺了一个应用以更强、更主动的安全措施被构建与部署的未来。

## 有韧性的安全始于主动测试

把 SAST、DAST 与 RASP 结合起来，可以提供覆盖整个软件开发生命周期的健壮安全。

通过把这些方法集成进 CI/CD 流水线并利用 AI 的进步，组织能主动响应新兴威胁。这些方法共同提供了一套整体方案，让现代应用免受安全漏洞之害。

/en_us/blog/fragments/disclaimer-with-divider

Style

two-column

Title

Related Articles

Filter

Category

Blog Limit

3

Category

learn

Sort Category Shuffle Order

true

### 相关文章

![什么是授权？](https://www.splunk.com/content/dam/splunk-blogs/images/media_134f9a1eaa778415e17526c148554b4276eed0186/what-is-authorization.avif?width=300&format=avif&optimize=medium)

[Learn](/en_us/blog/learn.html)

阅读时间 6 分钟

### [什么是授权？](/en_us/blog/learn/authorization.html)

授权是在用户完成认证之后，决定该用户可以访问哪些操作、网站或应用的哪些部分的这一过程。

![强化学习导论](https://www.splunk.com/content/dam/splunk-blogs/images/media_121111357b189a731cd5a2ddf84369cef208cf003/introduction-to-reinforcement-learning.webp?width=300&format=webp&optimize=medium)

[Learn](/en_us/blog/learn.html)

阅读时间 4 分钟

### [强化学习导论](/en_us/blog/learn/reinforcement-learning.html)

强化学习是过去十年一些最著名的 AI 突破的核心。在这里了解它是如何工作的。

![数据可观测性：完整导论](https://www.splunk.com/content/dam/splunk-blogs/images/media_1dc11993783afa9f01679a410d89741f51f147679/data-observability-the-complete-introduction.avif?width=300&format=avif&optimize=medium)

[Learn](/en_us/blog/learn.html)

阅读时间 8 分钟

### [数据可观测性：完整导论](/en_us/blog/learn/data-observability.html)

在这里获取关于数据可观测性的完整内容：它是什么、五大支柱、收益与落地 —— 以及最棒的，你能用它做的全部事情。

/en_us/blog/fragments/about-splunk

```
