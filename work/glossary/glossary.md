# 术语表（glossary）

- 版本：`1`　冻结：`是`
- 冻结哈希：`e5950ef8921edd8cade8bfaebda6b9b3e7203a7482d5cfb8a8004da0dc012dcd`
- 条目：**99** 条（人工定稿 99 / 自动候选待定 0）

> ⚠️ 本文件由 `scripts/init_glossary.py` 生成，**请勿手改**。
> 要改术语请改脚本里的 `CURATED` 字典后重跑，这样数字才可复现；手改会导致冻结哈希对不上、槽位校验拒绝沿用。

## 定稿规则（policy）

1. 同一术语在任何文件中必须使用同一译法
1. 术语表冻结后如需修改，必须重新全量校验
1. 保留英文的术语，中文正文中直接使用英文原形

## handling 取值说明

| handling | 含义 |
|---|---|
| `translate` | 翻成中文 |
| `keep_en` | 保留英文 |
| `bilingual` | 首次双语 |
| `acronym` | 保留缩写 |

## 一、人工定稿（99 条）—— 可直接执行

这些是已定稿的硬规则，翻译时**必须**按表中译法，不得自由选择。

| # | 英文 | 中文 | handling | 大小写敏感 | 语料出现 | 备注 |
|---|---|---|---|---|---|---|
| 1 | `agent` | 智能体 | `translate` | 否 | 319 | 指 AI 智能体，非法律意义的「代理人」，也避免与「代理服务器」混淆 |
| 2 | `mcp` | MCP | `acronym` | 否 | 317 | Model Context Protocol，课程核心概念；中文正文保留缩写，首次出现给全称 |
| 3 | `tool` | 工具 | `translate` | 否 | 274 |  |
| 4 | `context` | 上下文 | `translate` | 否 | 270 | 业内通行译法 |
| 5 | `model` | 模型 | `translate` | 否 | 224 |  |
| 6 | `prompt` | 提示词 | `translate` | 否 | 192 | 不译「提示」，避免与 UI 提示混淆 |
| 7 | `security` | 安全 | `translate` | 否 | 169 |  |
| 8 | `server` | 服务器 | `translate` | 否 | 124 |  |
| 9 | `code review` | 代码审查 | `translate` | 否 | 112 | 不译「代码评审」，与 GitHub/GitLab 界面一致 |
| 10 | `api` | API | `acronym` | 否 | 84 | Application Programming Interface，保留缩写 |
| 11 | `sast` | SAST | `acronym` | 否 | 71 | Static Application Security Testing，保留缩写 |
| 12 | `agentic` | 智能体式 | `translate` | 否 | 68 | 形容词，整体译「智能体式」。⚠️ 固定搭配 Agentic AI / agentic workflow / agentic system 一律译「智能体式 AI／智能体式工作流／智能体式系统」；不要用「智能体的 AI」这种别扭说法 |
| 13 | `sre` | SRE | `acronym` | 否 | 59 | Site Reliability Engineering，保留缩写 |
| 14 | `codebase` | 代码库 | `translate` | 否 | 55 |  |
| 15 | `evaluation` | 评估 | `translate` | 否 | 54 |  |
| 16 | `injection` | 注入 | `translate` | 否 | 54 | 安全语境 |
| 17 | `workflow` | 工作流 | `translate` | 否 | 53 |  |
| 18 | `automation` | 自动化 | `translate` | 否 | 53 |  |
| 19 | `dast` | DAST | `acronym` | 否 | 52 | Dynamic Application Security Testing，保留缩写 |
| 20 | `reasoning` | 推理 | `translate` | 否 | 47 | 指模型的推理过程/推理环节。⚠️ 只有语境明确指「模型的推理能力」时才用「推理能力」，避免把通用的理性思考过程误译成「推理能力」 |
| 21 | `pull request` | 拉取请求 | `bilingual` | 否 | 46 | 首次出现「拉取请求（Pull Request）」，之后用中文；PR 见 PR 条 |
| 22 | `llm` | LLM | `acronym` | 否 | 44 | Large Language Model，保留缩写 |
| 23 | `best practices` | 最佳实践 | `translate` | 否 | 43 | 多词短语，非通用词 |
| 24 | `vulnerability` | 漏洞 | `translate` | 否 | 42 |  |
| 25 | `client` | 客户端 | `translate` | 否 | 41 |  |
| 26 | `deployment` | 部署 | `translate` | 否 | 33 |  |
| 27 | `incident` | 故障事件 | `translate` | 否 | 33 | SRE 语境，不译「事故」 |
| 28 | `pr` | PR | `acronym` | 否 | 32 | Pull Request 的缩写，与 pull request 条并存 |
| 29 | `training` | 训练 | `translate` | 否 | 32 |  |
| 30 | `orchestration` | 编排 | `translate` | 否 | 31 | 多智能体编排 |
| 31 | `monitoring` | 监控 | `translate` | 否 | 31 |  |
| 32 | `observability` | 可观测性 | `translate` | 否 | 30 |  |
| 33 | `debugging` | 调试 | `translate` | 否 | 30 |  |
| 34 | `prompt injection` | 提示词注入 | `translate` | 否 | 30 | 安全议题，不译「提示注入」 |
| 35 | `tracing` | 链路追踪 | `translate` | 否 | 30 | 可观测性三支柱之一 |
| 36 | `on-call` | 值班 | `translate` | 否 | 29 | SRE 语境 |
| 37 | `token` | token | `keep_en` | 否 | 28 | 计费/上下文计量单位，中文无通用对译，保留英文 |
| 38 | `repository` | 仓库 | `translate` | 否 | 27 | 代码仓库 |
| 39 | `dataset` | 数据集 | `translate` | 否 | 26 |  |
| 40 | `ide` | IDE | `acronym` | 否 | 25 | Integrated Development Environment，保留缩写 |
| 41 | `context window` | 上下文窗口 | `translate` | 否 | 21 | 指模型单次可处理的 token 上限 |
| 42 | `spec` | 规格 | `translate` | 否 | 21 | 不译「规范」；specs-are-the-new-source-code 语境指规格文档 |
| 43 | `span` | 跨度 | `translate` | 否 | 21 | 分布式追踪的最小单元；也可保留 span |
| 44 | `prompt engineering` | 提示词工程 | `translate` | 否 | 20 | 行业已通用 |
| 45 | `machine learning` | 机器学习 | `translate` | 否 | 18 |  |
| 46 | `privacy` | 隐私 | `translate` | 否 | 16 |  |
| 47 | `ci/cd` | CI/CD | `acronym` | 否 | 15 | 持续集成/持续交付，保留缩写 |
| 48 | `exploit` | 漏洞利用 | `translate` | 否 | 15 | 名词指利用手段；⚠️ 动词义（利用某个漏洞）也用「漏洞利用」保持术语一致，不要写成「利用」 |
| 49 | `pipeline` | 流水线 | `translate` | 否 | 14 | 不译「管道」 |
| 50 | `retrieval` | 检索 | `translate` | 否 | 14 |  |
| 51 | `root cause` | 根因 | `translate` | 否 | 13 | 故障分析语境 |
| 52 | `compliance` | 合规 | `translate` | 否 | 12 |  |
| 53 | `commit` | 提交 | `translate` | 否 | 11 | 仅指版本控制义的「提交」（名词/动词）。⚠️ 三种例外不要套用：① 复合词 pre-commit、commit message 等工具名/固定名保留英文；② commit to doing sth 意为「投入/下决心做」，与版本控制无关；③ commit 出现在代码示例或 URL 中不译 |
| 54 | `embedding` | 嵌入 | `translate` | 否 | 10 | 向量嵌入 |
| 55 | `latency` | 延迟 | `translate` | 否 | 9 |  |
| 56 | `alignment` | 对齐 | `translate` | 否 | 9 | AI 对齐 |
| 57 | `static analysis` | 静态分析 | `translate` | 否 | 9 |  |
| 58 | `inference` | 推理 | `translate` | 否 | 8 | 指模型前向计算；注意与 reasoning（推理能力）区分，见 reasoning 条 |
| 59 | `ai-native` | AI 原生 | `translate` | 否 | 8 | 保留 AI 前缀，native 译「原生」 |
| 60 | `incident response` | 故障响应 | `translate` | 否 | 8 |  |
| 61 | `context engineering` | 上下文工程 | `translate` | 否 | 7 | 与 prompt engineering 区分：前者管喂什么，后者管怎么说 |
| 62 | `refactor` | 重构 | `translate` | 否 | 7 |  |
| 63 | `artifact` | 产物 | `translate` | 否 | 7 | 指流程产出的文件/交付物，不译「工件」 |
| 64 | `benchmark` | 基准测试 | `translate` | 否 | 6 |  |
| 65 | `template` | 模板 | `translate` | 否 | 5 |  |
| 66 | `coding agent` | 编码智能体 | `translate` | 否 | 5 | 与 agent 同词根 |
| 67 | `zero-shot` | 零样本 | `translate` | 否 | 5 |  |
| 68 | `tool use` | 工具调用 | `translate` | 否 | 4 | 不译「工具使用」 |
| 69 | `test coverage` | 测试覆盖率 | `translate` | 否 | 4 |  |
| 70 | `system prompt` | 系统提示词 | `translate` | 否 | 4 | 与 prompt 保持同词根 |
| 71 | `hallucination` | 幻觉 | `translate` | 否 | 3 | 模型编造事实 |
| 72 | `fine-tuning` | 微调 | `translate` | 否 | 3 |  |
| 73 | `rag` | RAG | `acronym` | 否 | 3 | Retrieval-Augmented Generation，保留缩写 |
| 74 | `subagent` | 子智能体 | `translate` | 否 | 3 | 与 agent 保持同词根，避免「子代理」 |
| 75 | `chain of thought` | 思维链 | `translate` | 否 | 3 | CoT，保留中文 |
| 76 | `context rot` | 上下文腐化 | `translate` | 否 | 3 | Chroma 研究提出的现象：长上下文质量退化 |
| 77 | `non-deterministic` | 非确定性 | `translate` | 否 | 3 | 指模型输出不可复现 |
| 78 | `multimodal` | 多模态 | `translate` | 否 | 3 |  |
| 79 | `sandbox` | 沙箱 | `translate` | 否 | 2 |  |
| 80 | `vibe coding` | vibe coding | `keep_en` | 否 | 2 | 课程专有说法，中文无稳定对译，保留英文原形 |
| 81 | `vector database` | 向量数据库 | `translate` | 否 | 2 |  |
| 82 | `human-in-the-loop` | 人在回路 | `translate` | 否 | 2 | 行业通行译法 |
| 83 | `postmortem` | 事后复盘 | `translate` | 否 | 2 | SRE 语境 |
| 84 | `annotation` | 标注 | `translate` | 否 | 2 |  |
| 85 | `unit test` | 单元测试 | `translate` | 否 | 2 |  |
| 86 | `guardrail` | 护栏 | `translate` | 否 | 1 | AI 安全护栏 |
| 87 | `scaffolding` | 脚手架 | `translate` | 否 | 1 | 指围绕模型的工程支撑代码 |
| 88 | `eval` | 评估 | `translate` | 否 | 1 | evaluation 的简称，统一译为「评估」 |
| 89 | `transformer` | Transformer | `keep_en` | 否 | 1 | 架构名，业界普遍保留英文 |
| 90 | `grounding` | 接地 | `translate` | 否 | 1 | 指用外部事实约束模型输出；也可译「事实锚定」 |
| 91 | `threat model` | 威胁模型 | `translate` | 否 | 1 |  |
| 92 | `rollout` | 灰度发布 | `translate` | 否 | 1 | 渐进式发布；语料仅 1 次，注意上下文 |
| 93 | `sla` | SLA | `acronym` | 否 | 1 | Service Level Agreement，保留缩写；语料未出现 |
| 94 | `slo` | SLO | `acronym` | 否 | 1 | Service Level Objective，保留缩写；语料未出现 |
| 95 | `deep learning` | 深度学习 | `translate` | 否 | 1 |  |
| 96 | `technical debt` | 技术债 | `translate` | 否 | 1 |  |
| 97 | `feature flag` | 功能开关 | `translate` | 否 | 1 |  |
| 98 | `autonomy` | 自主性 | `translate` | 否 | 1 |  |
| 99 | `few-shot` | 少样本 | `translate` | 否 | 1 |  |

## 二、自动候选待人工定稿（0 条）

以下由语料自动抽取，**尚未定稿**。多为通用英文词或低频词，请人工判断：确属术语的补上中文译法；明显是通用词的请**删除**。

| # | 英文 | 中文 | handling | 大小写敏感 | 语料出现 | 备注 |
|---|---|---|---|---|---|---|

## 三、零槽位条目（0 条）—— 语料中未出现，请确认是否删除

（无）

---

复查完成后：确认无误 → 保持 `frozen=true` 并重跑 `python scripts/init_glossary.py && python scripts/check_slots.py`；如需修改译法 → 改脚本 `CURATED` 后重跑全流程。
