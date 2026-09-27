# 翻译留痕：observability-basics

- doc_id：`observability-basics`
- 时间：2026-09-27T17:00:39+08:00
- 原文：`extracted/observability-basics.md`
- 译文：`translated/observability-basics.md`
- 原文 sha256：`9ef883819a0c1bc8fd102db80cd2ff65a1aa65082eb4c455434e129cc21435b4`
- 译文 sha256：`ec569ac8d6461456d074ae2559be7bfadd428c410d7b7ce84266b0b0e9a760d3`
- 术语约束条数：15

## 一、本文档涉及的术语清单

| 英文 | 译法 | handling | 出现次数 |
|---|---|---|---|
| `tracing` | 链路追踪 | `translate` | 28 |
| `observability` | 可观测性 | `translate` | 23 |
| `context` | 上下文 | `translate` | 13 |
| `span` | 跨度 | `translate` | 10 |
| `monitoring` | 监控 | `translate` | 8 |
| `api` | API | `acronym` | 2 |
| `llm` | LLM | `acronym` | 2 |
| `mcp` | MCP | `acronym` | 1 |
| `tool` | 工具 | `translate` | 1 |
| `security` | 安全 | `translate` | 1 |
| `best practices` | 最佳实践 | `translate` | 1 |
| `debugging` | 调试 | `translate` | 1 |
| `pipeline` | 流水线 | `translate` | 1 |
| `root cause` | 根因 | `translate` | 1 |
| `compliance` | 合规 | `translate` | 1 |

## 二、落盘校验结果

```json
{
  "non_empty": true,
  "code_blocks_total": 2,
  "code_blocks_in_translation": 2,
  "code_blocks_match": true,
  "code_blocks_byte_identical": true,
  "urls_orig": 20,
  "urls_trans": 20,
  "urls_all_present": true,
  "urls_counts_equal": true,
  "headings_orig": 30,
  "headings_trans": 30,
  "headings_match": true,
  "orig_chars": 11389,
  "trans_chars": 5805,
  "length_ratio": 0.5097,
  "length_ratio_ok": true
}
```

## 四、发出的 prompt 全文

```markdown
(未找到 prompt 导出文件)
```

## 五、AI 返回的译文全文

```markdown
![Cookie](/_astro/cookie-illustration.4Ddzj9Hm_ZT4qFS.svg)

我们用 cookie 来定制你的 Last9 体验。
 你的偏好是？

仅必要项

全部接受

[Last9](/)

[预约演示
 打开菜单](/schedule-demo/)

[Last9](/)

[预约演示
 关闭菜单](/schedule-demo/)

产品

[Discover](/discover/)

探索

[日志](/logs/)

[链路追踪](/traces/)

[指标](/metrics/)

[控制平面](/control-plane/)

[AI](/mcp/)

[RUM](/docs/discover-applications/)

[告警](/alerting/)

资源

[指南](/guides/)

[博客](/blog/)

[活动](/events/)

[更新日志](/changelog/)

更多

[客户](/customers/)

[文档](/docs/)

[定价](/pricing/)

[Last9](/)

Apr 23rd, 2025

## 链路追踪与 Span：你应该知道的观测性基础

了解链路追踪与 span 如何帮你看清分布式系统内部 —— 从而更快排查故障、构建更可靠的软件。

![Anjali Udasi](https://last9.ghost.io/content/images/2024/08/profile_pic.jpeg)

[Anjali Udasi](/blog/authors/anjali/)

![链路追踪与 Span：你应该知道的观测性基础](https://last9.ghost.io/content/images/2025/04/traces.webp)

#### 目录

https://discord.com/invite/Q3p2EEucx9/

https://www.linkedin.com/company/last9/

https://youtube.com/@last9/

https://x.com/last9io/

在现代软件架构中，应用不只是变得更大 —— 它们变得更分布式了。随着微服务、Serverless 函数与容器跨多个环境运行，理解系统内部正在发生什么，就像在暴风雨中追踪一滴雨。

这正是链路追踪与 span 的用武之地。这些可观测性工具不是流行语 —— 它们是你理解复杂分布式系统的秘密武器。我们来拆解一下链路追踪与 span 是什么、为什么重要，以及如何用它们更快排查故障、构建更可靠的系统。

# 理解链路追踪与 Span：核心概念

链路追踪（trace）记录一个请求穿越分布式系统的整个旅程。把一条 trace 想象成一个请求从头到尾的完整故事 —— 从用户点击按钮，到他们看到结果。

Span 是 trace 的构成单元。每个 span 代表这段旅程中的一个工作单元 —— 比如一次数据库查询、一次 API 调用，或一次函数执行。Span 之间相互嵌套，以表示操作之间的父子关系。

用简单的话说，它们的关系是：

- 一条 trace 包含多个 span
- 每个 span 代表一个操作
- Span 带有时间数据与元数据
- Span 可以嵌套，以表示操作之间如何相互关联

<!-- CODE_BLOCK_START id=c1 lang= -->
```
Trace
├── Span (API Gateway)
│   ├── Span (Auth Service)
│   └── Span (User Service)
│       └── Span (Database Query)
└── Span (Response Formatting)
```
<!-- CODE_BLOCK_END id=c1 -->

💡

如果你好奇链路追踪与 span 如何与

[指标、日志和事件配合，这篇文章把四者都拆解了一遍。](https://last9.io/blog/understanding-metrics-events-logs-traces-key-pillars-of-observability/)

## 链路追踪与 Span 对 DevOps 从业者的价值

你正在运行一个包含几十个微服务的复杂系统。突然，用户反馈结账流程很慢。没有链路追踪，你就得逐个检查每个服务，白白浪费时间。

有了链路追踪与 span，你可以：

1. 立刻定位瓶颈：准确看出是哪个服务或函数耗时过长
2. 跨服务边界调试：跟随请求在服务之间跳转的路径
3. 理解依赖关系：可视化你的服务如何连接与相互依赖
4. 改善性能：精确地识别并修复慢操作
5. 缩短平均恢复时间（MTTR）：出问题后更快找到根因

## 链路追踪与 Span 的技术实现

我们来深入链路追踪在分布式系统中运作的具体细节。

### Trace 上下文与传播

要让链路追踪跨服务边界生效，每个服务都需要知道自己在处理同一个请求的一部分。这通过上下文传播实现 —— 在服务之间传递 trace ID 与 span ID。

当一个请求首次进入你的系统时，它会被分配一个唯一的 trace ID。随着请求在服务之间流转，这个 ID 一直跟着它（通常作为 HTTP 头）。每个服务随后创建自己的 span，但把它们关联到同一条 trace 上。

### Span 的属性和事件

Span 不只是时间戳 —— 它们承载丰富的数据：

- 名称：这个 span 代表什么操作
- 时间：开始与结束时间
- 状态：成功、错误等
- 属性：自定义键值对（如 user_id 或 cart_size）
- 事件：span 内值得注意的发生
- 链接：与其他 span 的连接

### 采样策略

对所有请求都做链路追踪会产生海量数据。这就是为什么大多数系统采用采样 —— 只收集一定比例的 trace。聪明的采样策略包括：

- 头采样（head-based）：在请求开始时决定是否采样
- 尾采样（tail-based）：在请求完成后决定（更适合捕获错误）
- 优先级采样：总是追踪重要操作，但对例行操作采样

💡

如果你想理解可观测性、遥测与监控之间的区别，看看这篇有用的文章：

[可观测性 vs 遥测 vs 监控。](https://last9.io/blog/observability-vs-telemetry-vs-monitoring/)

## 链路追踪实施指南：工具与框架

准备好给你的系统加上链路追踪了吗？你需要这些：

### OpenTelemetry：行业标准

[OpenTelemetry 已成为实现链路追踪与 span 的首选框架。它提供：](https://opentelemetry.io/)

- 覆盖所有主流编程语言的库
- 厂商中立的 API 与 SDK
- 对流行框架的自动埋点
- 一套一致的收集与导出数据方式

### 链路追踪工具箱

有几款工具可以帮你收集、存储与可视化 trace：

| 工具 | 类型 | 最适用 |
| --- | --- | --- |
| Last9 | 一体化可观测性 | 高基数、高性价比的可观测性，定价可预测 |
| Jaeger | 开源链路追踪 | 自托管的链路追踪可视化 |
| Zipkin | 开源链路追踪 | 简单的分布式链路追踪 |
| Grafana Tempo | 链路追踪后端 | 与 Grafana 仪表盘集成 |
| OpenTelemetry Collector | 数据收集流水线 | 处理与路由遥测数据 |

如果你在找一款符合预算的可观测性方案，

[Last9 值得一看。它按摄取的事件量计费，让成本保持可预测。此外，我们的平台能在规模化下处理高基数数据，并与 OpenTelemetry 和 Prometheus 集成，把你的指标、日志与链路追踪汇聚到一处。](https://last9.io/)

### 在你的代码中实现链路追踪

下面是一个简化示例，展示如何在 Node.js 应用中使用 OpenTelemetry 创建 span：

<!-- CODE_BLOCK_START id=c2 lang= -->
```
// Initialize the OpenTelemetry SDK (once in your app)
const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
const { SimpleSpanProcessor } = require('@opentelemetry/sdk-trace-base');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-http');

const provider = new NodeTracerProvider();
const exporter = new OTLPTraceExporter({
  url: 'http://localhost:4318/v1/traces',
});
provider.addSpanProcessor(new SimpleSpanProcessor(exporter));
provider.register();

// Get a tracer
const { trace } = require('@opentelemetry/api');
const tracer = trace.getTracer('my-service');

// Create spans in your code
async function processOrder(orderId) {
  const span = tracer.startSpan('process-order');

  // Add attributes to the span
  span.setAttribute('order.id', orderId);
  span.setAttribute('customer.type', 'premium');

  try {
    // Do work...

    // Create a child span
    const dbSpan = tracer.startSpan('database-query', {
      parent: span,
    });

    try {
      // Run database query...
      dbSpan.end();
    } catch (error) {
      dbSpan.setStatus({ code: SpanStatusCode.ERROR });
      dbSpan.recordException(error);
      dbSpan.end();
      throw error;
    }

    span.end();
  } catch (error) {
    span.setStatus({ code: SpanStatusCode.ERROR });
    span.recordException(error);
    span.end();
    throw error;
  }
}
```
<!-- CODE_BLOCK_END id=c2 -->

💡

想知道 OpenTelemetry 与传统的 APM 工具相比如何？这篇文章拆解了关键区别：

[OpenTelemetry vs 传统 APM 工具。](https://last9.io/blog/opentelemetry-vs-traditional-apm-tools/)

## 进阶链路追踪技术

基础链路追踪就位之后，这些进阶技术可以把你的可观测性提升到下一个层次。

### 分布式上下文管理

在复杂系统中，你需要管理的上下文不止 trace ID。W3C Trace Context 规范为以下内容提供了标准：

- traceparent：包含 trace ID 与父 span ID
- tracestate：允许厂商添加自定义上下文数据

使用这些头能确保你的链路追踪在不同服务与厂商之间都能工作。

### 链路追踪、指标与日志之间的关联

可观测性真正的威力来自把不同信号连接起来：

- 示例 trace（exemplar）：把指标关联到产生它们的 trace
- 日志中的 trace ID：在日志消息里加上 trace ID 以便交叉引用
- 自定义属性：在所有遥测类型中使用一致的属性

### 错误处理与异常追踪

当异常发生时，span 可以提供关键的上下文：

- 把 span 标记为错误状态
- 连同堆栈跟踪一起记录异常
- 向 span 添加事件，展示错误的演进过程
- 创建 baggage 项，让错误上下文跨服务边界传递

💡

想更深入了解如何提前发现问题、提升系统可靠性，看看这篇关于主动监控的文章：

[主动监控。](https://last9.io/blog/proactive-monitoring/)

## 实战中的链路追踪模式与反模式

### 有效的链路追踪模式

有意义的 span 名称：使用一致的命名约定，如 service_name/operation
合适的粒度：为重要操作创建 span，而不是每次函数调用都创建
正确的上下文传播：确保 trace 上下文流经所有通信渠道
有用的属性：添加有助于排查问题的属性，如用户 ID 或功能开关
性能意识：留意过度创建 span 带来的开销

### 应当避免的链路追踪反模式

过度埋点：创建过多 span 会导致性能问题
上下文缺失：未能传播上下文会切断跨服务边界的 trace
命名不一致：使用不同的命名标准会让 trace 更难解读
数据过多：把大负载放进 span 会压垮你的链路追踪后端
忽视第三方服务：缺少外部调用的 span 会形成盲区

💡

探索可观测性如何在 LLM 的性能与可靠性中发挥关键作用：

[LLM 可观测性。](https://last9.io/blog/llm-observability/)

## 链路追踪与 Span 的业务价值：超越技术收益

链路追踪不只用于排查故障 —— 它也能提供业务洞见：

- 端到端追踪关键用户旅程
- 衡量关键业务操作的性能
- 基于 trace 数据设定 SLO（服务等级目标）
- 用真实用户的语言量化性能问题的代价
- 通过向 span 添加相关属性来构建业务上下文

当你能展示技术改进如何影响用户体验与业务指标时，你就弥合了 DevOps 与业务相关方之间的鸿沟。

## 结论

链路追踪与 span 让你拥有透视分布式系统的 X 光视力。它们揭示服务之间隐藏的连接、精确指出性能瓶颈，并大幅加快调试速度。

随着系统变得越来越复杂，这类可观测性不是奢侈品 —— 而是必需品。

💡

如果你想继续聊分布式链路追踪与可观测性，欢迎加入我们的

[Discord 社区，DevOps 从业者在那里分享经验与最佳实践！](https://discord.com/invite/W8gMppQC4b)

## 常见问题

### 链路追踪与日志有什么区别？

日志记录离散事件，而链路追踪展示跨服务操作之间的关系。日志告诉你发生了什么；链路追踪告诉你它是怎么发生的。

### 加上链路追踪会让我的应用变慢吗？

现代链路追踪库增加的开销很小 —— 配置得当的情况下性能影响通常低于 3%。借助采样，你还能进一步降低这一影响。

### 我需要改所有代码才能加上链路追踪吗？

不一定。很多框架提供自动埋点，只需极少的代码改动就能加上链路追踪。OpenTelemetry 为大多数语言中的流行框架提供自动埋点。

### 分布式链路追踪会产生多少数据？

这因流量、采样率和 span 细节而差异很大。繁忙系统要按每天数 GB 到数 TB 来规划。这就是为什么选对可观测性平台对成本控制很重要。

### 链路追踪对安全与合规有帮助吗？

有！链路追踪为请求在你的系统中流转留下了审计轨迹。配合合适的属性，你可以追踪哪些用户或服务在何时访问了什么数据。

### 链路追踪与 span 如何与其他可观测性信号配合？

链路追踪与指标、日志互为补充。指标在高层次上展示系统健康状况，日志提供详细事件，而链路追踪把这些点连起来，展示跨服务的请求流转。

主题

[可观测性](/blog/tag/observability/)

[监控](/blog/tag/monitoring/)

关于作者

![Anjali Udasi](https://last9.ghost.io/content/images/2024/08/profile_pic.jpeg)

[Anjali Udasi](/blog/authors/anjali/)

帮助让技术变得没那么令人生畏。我

#### 目录

https://discord.com/invite/Q3p2EEucx9/

https://www.linkedin.com/company/last9/

https://youtube.com/@last9/

https://x.com/last9io/

![Last9 键盘插图](/_astro/buttons.SzdkIwcl_Z28vC7U.webp)

## 免费开始观测。无厂商锁定。

[预约演示](/schedule-demo/)

[OPENTELEMETRY • PROMETHEUS](/docs/integrations/)

只需更新你的配置。几秒钟内就能在 Last9 上看到数据。

[DATADOG • NEW RELIC • 其他](/docs/integrations/)

我们都能支持。一键迁移你的仪表盘与告警。

[构建于开放标准之上](/docs/integrations/)

100+ 集成。原生支持 OTel，与你现有的技术栈兼容。

4.8/5

[G2 评价](https://www.g2.com/products/last9-last9/reviews)

![Gartner Cool Vendor 2025](/_astro/gartner-cool-vendor-badge.ClTJIiRB_sMwyD.webp)

Gartner Cool Vendor 2025

![High Performer](/_astro/high-performer-badge.BCroQ4N5_1fldwe.svg)

High Performer

![Best Usability](/_astro/best-usability-badge.mZNSvnQA_1fldwe.svg)

Best Usability

![Highest User Adoption](/_astro/highest-user-adoption-badge.DlXpV0dv_1fldwe.svg)

Highest User Adoption

```
