# 翻译留痕：archive-cognition.ai-index-5e05e503

- doc_id：`archive-cognition.ai-index-5e05e503`
- 时间：2026-09-27T16:31:41+08:00
- 原文：`extracted/archive-cognition.ai-index-5e05e503.md`
- 译文：`translated/archive-cognition.ai-index-5e05e503.md`
- 原文 sha256：`94acf5b735f57443e082b7b408759ef048d590479969bda10724e1d00a7fed1f`
- 译文 sha256：`2644448a44cf04f5c641c8e65c0bcfb37cdacf9835dff1ec4bc45ea0878f01ff`
- 术语约束条数：4

## 一、本文档涉及的术语清单

| 英文 | 译法 | handling | 出现次数 |
|---|---|---|---|
| `codebase` | 代码库 | `translate` | 2 |
| `model` | 模型 | `translate` | 1 |
| `pull request` | 拉取请求 | `bilingual` | 1 |
| `benchmark` | 基准测试 | `translate` | 1 |

## 二、落盘校验结果

```json
{
  "non_empty": true,
  "code_blocks_total": 0,
  "code_blocks_in_translation": 0,
  "code_blocks_match": true,
  "code_blocks_byte_identical": true,
  "urls_orig": 9,
  "urls_trans": 9,
  "urls_all_present": true,
  "urls_counts_equal": true,
  "headings_orig": 4,
  "headings_trans": 4,
  "headings_match": true,
  "orig_chars": 6156,
  "trans_chars": 4837,
  "length_ratio": 0.7857,
  "length_ratio_ok": true
}
```

## 四、发出的 prompt 全文

```markdown
# 翻译任务：archive-cognition.ai-index-5e05e503

## 一、文档元数据

- doc_id：`archive-cognition.ai-index-5e05e503`
- title：[Devin, the first autonomous software engineer.](https://devin.ai/)
- origin_url：https://cognition.ai/
- 本段字符数：6,794

## 二、术语约束（本文档用到的，必须严格遵守）

| 英文 | 处理方式 | 出现次数 |
|---|---|---|
| `codebase` | 翻译为「代码库」 | 2 |
| `model` | 翻译为「模型」 | 1 |
| `pull request` | 首次出现译为「拉取请求（pull request）」，之后只用「拉取请求」 | 1 |
| `benchmark` | 翻译为「基准测试」 | 1 |

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


/

01

Cognition operates

# [Devin, the first autonomous software engineer.](https://devin.ai/)

We believe the purpose of technology is to expand human capacity — not by replacing meaningful work but by working alongside people as an exponential collaborator, helping them think deeper and move faster. We build tools for software creation because software shapes nearly every aspect of modern life. Cognition helps engineers operate more like architects: strategizing, designing systems, and focusing on problem solving, while agents handle the repetitive engineering work.

Devin plans, writes, tests, and ships production code on its own, working inside your codebase and the tools your team already uses. Devin is deployed at some of the largest and most complex institutions in the world.

[Try Devin](https://www.devin.ai/)

[Download apps](https://devin.ai/download)

02

https://cognition.com/blog/mercedes-benz-cognition

https://www.goldmansachs.com/insights/talks-at-gs/russell-kaplan

https://devin.ai/customers/rvtech

https://cognition.com/blog/infosys-cognition

https://devin.ai/customers/itau

https://devin.ai/customers/nubank

03

### Introducing FrontierCode

FrontierCode is our benchmark to measure whether a model writes code that a maintainer would actually merge. Traditional benchmarks only check if code passes basic unit tests. FrontierCode asks a harder question: Would a human maintainer actually merge this pull request? To evaluate mergeability, FrontierCode combines custom rubrics, novel verifiers, and tests to check for correctness, test quality, scope discipline, style, and adherence to codebase standards.

##### FrontierCode 1.1 Main

[View leaderboard](/frontiercode)

| 1 | Opus 5.5medium | 54.6% |
| --- | --- | --- |
| 2 | Fable 5xhigh | 53.5% |
| 3 | Opus 5medium | 53.4% |
| 4 | GPT-6 Astramax | 53.3% |
| 5 | Fable 5.1medium | 50.9% |

04

### Join the team

We're defining the biggest shift in computing since the invention of software. Cognition is a team of interdisciplinary makers who love working on the hardest problems in AI. If you're interested in supporting the world's leading enterprises and technology companies, come build with us.

[Explore roles](/careers)

05. ArticlesArticles

/blog/1b-run-rate

![Cognition Crosses $1B in Annualized Revenue Run Rate](/_next/image?url=%2Fimages%2F1b-run-rate%2Fcover.jpg&w=1920&q=75&dpl=dpl_4iFKyV44ctVkgHLScGjvoenrBZep)

Cognition Crosses $1B in Annualized Revenue Run Rate

09.25.26

/blog/local-fusion

![Introducing Fusion in Devin Desktop & CLI](/_next/image?url=%2Fimages%2Ffusion-in-devin-cli%2Fcover.jpg&w=1920&q=75&dpl=dpl_4iFKyV44ctVkgHLScGjvoenrBZep)

Introducing Fusion in Devin Desktop & CLI

09.11.26

/blog/swe-2

![Introducing SWE-2: Pushing the Pareto Frontier](/_next/image?url=%2Fimages%2Fswe-2%2Fcover.jpg&w=1920&q=75&dpl=dpl_4iFKyV44ctVkgHLScGjvoenrBZep)

Introducing SWE-2: Pushing the Pareto Frontier

09.10.26

/blog/series-e

![Do it all with Devin: Announcing our Series E](/_next/image?url=%2Fimages%2Fseries-e%2Fcover.jpg&w=1920&q=75&dpl=dpl_4iFKyV44ctVkgHLScGjvoenrBZep)

Do it all with Devin: Announcing our Series E

09.08.26

/blog/interaction

![Welcoming The Interaction Company](/_next/image?url=%2Fimages%2Finteraction%2Fcog-poke-blog-image-v3.jpg&w=1920&q=75&dpl=dpl_4iFKyV44ctVkgHLScGjvoenrBZep)

Welcoming The Interaction Company

07.23.26

/blog/swe-1-7

![SWE-1.7: Frontier Intelligence at a Fraction of the Cost](/_next/image?url=%2Fimages%2Fswe-1-7%2Fswe-1-7-blog-cover.jpg&w=1920&q=75&dpl=dpl_4iFKyV44ctVkgHLScGjvoenrBZep)

SWE-1.7: Frontier Intelligence at a Fraction of the Cost

07.08.26

/blog/devin-fusion

![Devin Fusion](/_next/image?url=%2Fimages%2Fdevin-fusion%2Ffusion-blog-cover.jpg&w=1920&q=75&dpl=dpl_4iFKyV44ctVkgHLScGjvoenrBZep)

Devin Fusion: Frontier Performance at 60% Lower Cost

06.29.26

/blog/frontier-code

![Introducing FrontierCode](/_next/image?url=%2Fimages%2Ffrontier-code%2Fevals-blog-1.jpg&w=1920&q=75&dpl=dpl_4iFKyV44ctVkgHLScGjvoenrBZep)

Introducing FrontierCode

06.08.26

/blog/ai-productivity

![Estimating the Productivity of an Autonomous AI Software Engineer](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2mc9cv2v%2Fproduction%2F8527b7c1b2b03f309d7ba9189296ac76a1c7b650-1920x1080.jpg%3Fw%3D640%26h%3D360%26fit%3Dcrop&w=1920&q=75)

Estimating the Productivity of an Autonomous AI Software Engineer

06.04.26

/blog/ai-guarantee

![AI should earn its keep: Introducing the AI Productivity Guarantee](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2mc9cv2v%2Fproduction%2Fd378ef146ec6070438bfaeab4d9e47e8b886e55d-1920x1080.jpg%3Fw%3D640%26h%3D360%26fit%3Dcrop&w=1920&q=75)

AI should earn its keep: Introducing the AI Productivity Guarantee

06.04.26

/blog/introducing-devin-desktop

![Introducing Devin Desktop](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2mc9cv2v%2Fproduction%2F5841a7932386c05dc112f92fda8ff519b38d4f9a-1920x1080.jpg%3Fw%3D640%26h%3D360%26fit%3Dcrop&w=1920&q=75)

Introducing Devin Desktop

06.02.26

/blog/series-d

![More Devins in More Places](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2mc9cv2v%2Fproduction%2F58309361c06f31fa49f8c36e307963f21bd3f22b-1382x777.jpg%3Frect%3D1%2C0%2C1381%2C777%26w%3D640%26h%3D360%26fit%3Dcrop&w=1920&q=75)

More Devins in More Places

05.27.26

/blog/devin-in-windsurf

![Devin in Windsurf](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2mc9cv2v%2Fproduction%2F89fcacf48d33b51277268808596d123237018950-1920x1080.jpg%3Fw%3D640%26h%3D360%26fit%3Dcrop&w=1920&q=75)

Devin in Windsurf

04.15.26

/blog/swe-1-6-preview

![An Early Preview of SWE-1.6 and Research Update](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2mc9cv2v%2Fproduction%2F6ce843c49d6a38e1c0045e43891aca89fccd8981-1500x844.jpg%3Fw%3D640%26h%3D360%26fit%3Dcrop&w=1920&q=75)

An Early Preview of SWE-1.6 and Research Update

03.01.26

/blog/how-cognition-uses-devin-to-build-devin

![How Cognition Uses Devin to Build Devin](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2mc9cv2v%2Fproduction%2Fc1e05d959a8c25c8df5e86198a4213e4fd634b61-1500x844.jpg%3Fw%3D640%26h%3D360%26fit%3Dcrop&w=1920&q=75)

How Cognition Uses Devin to Build Devin

02.27.26

/blog/cognition-for-government

![Introducing Cognition for Government](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2mc9cv2v%2Fproduction%2F164f27869605d7c326a68e511efcf1a4077fc2b7-1920x1080.jpg%3Fw%3D640%26h%3D360%26fit%3Dcrop&w=1920&q=75)

Introducing Cognition for Government

02.25.26

/blog/introducing-devin-2-2

![Introducing Devin 2.2](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2mc9cv2v%2Fproduction%2F5638cfd0a8a65ad3074019b69c3aa05e112577b7-1920x1080.jpg%3Fw%3D640%26h%3D360%26fit%3Dcrop&w=1920&q=75)

Introducing Devin 2.2

02.24.26

````

## 五、输出要求

直接给出译文，用 ``` 包裹便于复制。**不要**输出任何解释、前言或后记。

```

## 五、AI 返回的译文全文

```markdown
/

01

Cognition operates

# [Devin，第一位自主软件工程师。](https://devin.ai/)

我们相信技术的目的是扩展人的能力 —— 不是取代有意义的工作，而是作为指数级的协作者与人并肩工作，帮助他们思考得更深、前进得更快。我们打造软件创造工具，因为软件塑造了现代生活几乎每一个方面。Cognition 帮助工程师更像架构师那样工作：制定策略、设计系统、专注于解决问题，而把重复性的工程工作交给智能体。

Devin 能自行规划、编写、测试并交付生产代码，它在你现有的代码库和团队已在使用的工具中工作。Devin 已部署在全球一些规模最大、最复杂的机构中。

[试用 Devin](https://www.devin.ai/)

[下载应用](https://devin.ai/download)

02

https://cognition.com/blog/mercedes-benz-cognition

https://www.goldmansachs.com/insights/talks-at-gs/russell-kaplan

https://devin.ai/customers/rvtech

https://cognition.com/blog/infosys-cognition

https://devin.ai/customers/itau

https://devin.ai/customers/nubank

03

### 隆重推出 FrontierCode

FrontierCode 是我们用来衡量一个模型写出的代码是否会被维护者真正合并的基准测试。传统基准测试只检查代码能否通过基本的单元测试。FrontierCode 提出了一个更难的问题：人类维护者真的会合并这个拉取请求吗？为了评估可合并性，FrontierCode 结合自定义评分标准、新颖的验证器与测试，来检查正确性、测试质量、改动范围控制、代码风格，以及对代码库规范的遵循程度。

##### FrontierCode 1.1 Main

[查看排行榜](/frontiercode)

| 1 | Opus 5.5medium | 54.6% |
| --- | --- | --- |
| 2 | Fable 5xhigh | 53.5% |
| 3 | Opus 5medium | 53.4% |
| 4 | GPT-6 Astramax | 53.3% |
| 5 | Fable 5.1medium | 50.9% |

04

### 加入团队

我们正在定义自软件发明以来计算领域最大的一次转变。Cognition 由一群跨领域的创造者组成，他们热爱攻克 AI 中最难的问题。如果你有兴趣支持全球领先的企业与科技公司，欢迎来和我们一起构建。

[查看职位](/careers)

05. ArticlesArticles

/blog/1b-run-rate

![Cognition 年化收入运行率突破 10 亿美元](/_next/image?url=%2Fimages%2F1b-run-rate%2Fcover.jpg&w=1920&q=75&dpl=dpl_4iFKyV44ctVkgHLScGjvoenrBZep)

Cognition 年化收入运行率突破 10 亿美元

09.25.26

/blog/local-fusion

![在 Devin Desktop 与 CLI 中推出 Fusion](/_next/image?url=%2Fimages%2Ffusion-in-devin-cli%2Fcover.jpg&w=1920&q=75&dpl=dpl_4iFKyV44ctVkgHLScGjvoenrBZep)

在 Devin Desktop 与 CLI 中推出 Fusion

09.11.26

/blog/swe-2

![隆重推出 SWE-2：推进帕累托前沿](/_next/image?url=%2Fimages%2Fswe-2%2Fcover.jpg&w=1920&q=75&dpl=dpl_4iFKyV44ctVkgHLScGjvoenrBZep)

隆重推出 SWE-2：推进帕累托前沿

09.10.26

/blog/series-e

![用 Devin 搞定一切：宣布我们的 E 轮融资](/_next/image?url=%2Fimages%2Fseries-e%2Fcover.jpg&w=1920&q=75&dpl=dpl_4iFKyV44ctVkgHLScGjvoenrBZep)

用 Devin 搞定一切：宣布我们的 E 轮融资

09.08.26

/blog/interaction

![欢迎 The Interaction Company](/_next/image?url=%2Fimages%2Finteraction%2Fcog-poke-blog-image-v3.jpg&w=1920&q=75&dpl=dpl_4iFKyV44ctVkgHLScGjvoenrBZep)

欢迎 The Interaction Company

07.23.26

/blog/swe-1-7

![SWE-1.7：以极低成本获得前沿智能](/_next/image?url=%2Fimages%2Fswe-1-7%2Fswe-1-7-blog-cover.jpg&w=1920&q=75&dpl=dpl_4iFKyV44ctVkgHLScGjvoenrBZep)

SWE-1.7：以极低成本获得前沿智能

07.08.26

/blog/devin-fusion

![Devin Fusion](/_next/image?url=%2Fimages%2Fdevin-fusion%2Ffusion-blog-cover.jpg&w=1920&q=75&dpl=dpl_4iFKyV44ctVkgHLScGjvoenrBZep)

Devin Fusion：成本降低 60% 的前沿性能

06.29.26

/blog/frontier-code

![隆重推出 FrontierCode](/_next/image?url=%2Fimages%2Ffrontier-code%2Fevals-blog-1.jpg&w=1920&q=75&dpl=dpl_4iFKyV44ctVkgHLScGjvoenrBZep)

隆重推出 FrontierCode

06.08.26

/blog/ai-productivity

![估算一位自主 AI 软件工程师的生产力](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2mc9cv2v%2Fproduction%2F8527b7c1b2b03f309d7ba9189296ac76a1c7b650-1920x1080.jpg%3Fw%3D640%26h%3D360%26fit%3Dcrop&w=1920&q=75)

估算一位自主 AI 软件工程师的生产力

06.04.26

/blog/ai-guarantee

![AI 应当证明自己的价值：推出 AI 生产力保证](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2mc9cv2v%2Fproduction%2Fd378ef146ec6070438bfaeab4d9e47e8b886e55d-1920x1080.jpg%3Fw%3D640%26h%3D360%26fit%3Dcrop&w=1920&q=75)

AI 应当证明自己的价值：推出 AI 生产力保证

06.04.26

/blog/introducing-devin-desktop

![隆重推出 Devin Desktop](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2mc9cv2v%2Fproduction%2F5841a7932386c05dc112f92fda8ff519b38d4f9a-1920x1080.jpg%3Fw%3D640%26h%3D360%26fit%3Dcrop&w=1920&q=75)

隆重推出 Devin Desktop

06.02.26

/blog/series-d

![更多 Devin，遍布更多场景](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2mc9cv2v%2Fproduction%2F58309361c06f31fa49f8c36e307963f21bd3f22b-1382x777.jpg%3Frect%3D1%2C0%2C1381%2C777%26w%3D640%26h%3D360%26fit%3Dcrop&w=1920&q=75)

更多 Devin，遍布更多场景

05.27.26

/blog/devin-in-windsurf

![Windsurf 中的 Devin](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2mc9cv2v%2Fproduction%2F89fcacf48d33b51277268808596d123237018950-1920x1080.jpg%3Fw%3D640%26h%3D360%26fit%3Dcrop&w=1920&q=75)

Windsurf 中的 Devin

04.15.26

/blog/swe-1-6-preview

![SWE-1.6 早期预览与研究进展](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2mc9cv2v%2Fproduction%2F6ce843c49d6a38e1c0045e43891aca89fccd8981-1500x844.jpg%3Fw%3D640%26h%3D360%26fit%3Dcrop&w=1920&q=75)

SWE-1.6 早期预览与研究进展

03.01.26

/blog/how-cognition-uses-devin-to-build-devin

![Cognition 如何用 Devin 构建 Devin](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2mc9cv2v%2Fproduction%2Fc1e05d959a8c25c8df5e86198a4213e4fd634b61-1500x844.jpg%3Fw%3D640%26h%3D360%26fit%3Dcrop&w=1920&q=75)

Cognition 如何用 Devin 构建 Devin

02.27.26

/blog/cognition-for-government

![隆重推出 Cognition for Government](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2mc9cv2v%2Fproduction%2F164f27869605d7c326a68e511efcf1a4077fc2b7-1920x1080.jpg%3Fw%3D640%26h%3D360%26fit%3Dcrop&w=1920&q=75)

隆重推出 Cognition for Government

02.25.26

/blog/introducing-devin-2-2

![隆重推出 Devin 2.2](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2mc9cv2v%2Fproduction%2F5638cfd0a8a65ad3074019b69c3aa05e112577b7-1920x1080.jpg%3Fw%3D640%26h%3D360%26fit%3Dcrop&w=1920&q=75)

隆重推出 Devin 2.2

02.24.26

```
