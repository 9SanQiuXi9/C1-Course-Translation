# 管线 ④ 术语表与槽位校验：可复制 Prompt

> **前置条件**：抽取已完成（`extracted/*.md` 已生成）。**本流程不做切块。**
> **产出**：`glossary.json`（冻结的术语表）+ `slot_report.json`（槽位统计）
> **粒度**：术语槽位按【文档】统计，不按块统计

---

## 主 Prompt

```
【项目背景】

我在把一批英文课程资料翻译成中文，做成别人能复用的资料包。
现在要做术语表与槽位校验。项目流程是：抽取 → 术语 → 翻译 → 校验
（不做切块，所以术语槽位按【文档】粒度统计，不按块。）

【仓库】<仓库根目录>\
【输入】
  extracted/*.md        抽取后的英文原文，每个文件带 YAML front matter
                        （含 source_file、origin_url、title、chars、code_blocks 等）
  extract_report.json   抽取报告
【环境】
  - 只用 Python 标准库（re, json, os, collections, hashlib）
  - Windows GBK 控制台，脚本开头必须：
      try: sys.stdout.reconfigure(encoding="utf-8")
      except Exception: pass

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【为什么需要术语表】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
语料约 76,000 英文词，同术语反复出现。实测高频词：
  MCP 383 次、agent 291 次、context 266 次、prompt 225 次、
  code review 100 次、pull request 59 次、token 39 次
若每次自由选择译法（agent 时而"代理"时而"智能体"），读者会以为它们是不同概念。

【两层价值】
  第一层：给人看的参考表（规定每个术语只能怎么翻）
  第二层：可自动校验的合同 —— 扫描【原文】穷举每个术语的所有出现位置，
          得到"槽位数"；翻完后逐槽核对，输出"命中数 / 总槽位数"。

  ⚠️ 必须扫描【原文】，不能扫描译文。
     若某段整段漏译，扫译文时那段没有该术语、不计入槽位，漏译就永远查不出来。
     扫原文则槽位固定，漏了立刻暴露。

  ⚠️ 必须先排除【导航、页脚、链接行、图片行】再统计！
     实测：extracted/ 里的 Markdown 残留了大量网页导航与页脚，导致英文词总数
     从真实的约 76,000 膨胀到 131,375（多出 72%）。若不排除，槽位数会虚高，
     而且后续"命中率"会因译文不含导航而永远达不到 100%，让这个指标失去意义。

     判定"非正文行"的规则：
       - 行内 URL 或图片语法占比过高（如以 "A https://" 开头、或整行是 ![...](...)）
       - 以 - 开头且整行主要是链接
       - 空白行
     建议实现一个 is_content_line(line) 函数，并打印"排除行数 / 总行数"供核对。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【任务 1：术语表 glossary.json】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
结构：
{
  "version": 1,
  "frozen": true,
  "frozen_hash": "<术语表内容的 sha256>",
  "policy": {
    "rules": [
      "同一术语在任何文件中必须使用同一译法",
      "术语表冻结后如需修改，必须重新全量校验",
      "保留英文的术语，中文正文中直接使用英文原形"
    ]
  },
  "terms": [
    {
      "en": "agent",
      "zh": "智能体",
      "handling": "translate",
      "case_sensitive": false,
      "note": "指 AI 智能体，非法律意义的代理人",
      "occurrences": 0
    }
  ]
}

⚠️ handling 只能是这四种，不要自由发挥：
  "translate"  翻成中文
  "keep_en"    保留英文（专有名词、缩写、行业已通用）
  "bilingual"  首次出现双语「中文（英文）」，之后只用中文
  "acronym"    保留英文缩写，首次出现给全称

⚠️ 重要：不要手工编辑 glossary.json 来"种下"初始术语。
   请写一个 init_glossary.py（或在 check_slots.py 里加 --init 子命令），
   从语料里自动抽取候选术语并按词频排序，输出初始 glossary.json。
   理由：交付要求"所有数字来自脚本、可复跑"。手工初始化的术语表无法复现。

   自动抽取候选术语的建议做法：
     - 扫描正文，找出高频的英文名词短语（2-3 个词的组合）
     - 优先保留首字母缩写与技术术语（正则：^[A-Z]{2,}$ 或含 - / 大小写混合）
     - 按出现频次排序，取前 150-200 个作为候选
     - 人工再从中定稿出至少 60 条（这一步是人工的，允许）

提取【至少 60 条】。起步清单（核实并补充）：
  MCP, agent, agentic, context, context window, context engineering,
  prompt, prompt engineering, code review, pull request, repository, commit,
  refactor, token, hallucination, inference, fine-tuning, embedding, RAG,
  guardrail, observability, debugging, deployment, pipeline, subagent,
  orchestration, sandbox, chain of thought, reasoning, benchmark, latency,
  throughput, tool use, tool calling, scaffolding, vibe coding, workflow,
  automation, artifact, template, cache, server, client, API

课程语境里易翻错的，请重点考虑：
  tool use（工具调用）、MCP server、context rot（上下文腐化）、
  prompt injection（提示词注入）、spec（规格）、scaffolding（脚手架）、
  vibe coding（保留英文）、AI-native（AI 原生）、on-call（值班）、
  SRE, DAST, SAST, LLM, IDE, PR, CI/CD

有争议的术语在 note 里写明取舍理由，例如：
  - "agent" → 「智能体」（避免与"代理服务器"混淆）
  - "context" → 「上下文」（业内通行）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【任务 2：槽位校验 check_slots.py】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
扫描【原文】extracted/*.md，为每条术语穷举槽位，按【文档】归类。

输出 slot_report.json：
{
  "generated_by": "check_slots.py",
  "glossary_version": 1,
  "glossary_hash": "...",
  "totals": {
    "terms": 60,
    "slots_total": 1500,
    "slots_by_handling": {"translate": 1200, "keep_en": 300, ...}
  },
  "per_term": [
    {
      "en": "agent", "zh": "智能体", "handling": "translate",
      "slots_total": 291,
      "slots_per_doc": {"mcp-introduction": 14, "devin-coding-agents-101": 31, ...},
      "slots_in_title": 0
    }
  ],
  "per_doc": [
    {"doc": "mcp-introduction", "slots": 42}
  ]
}

匹配规则（请仔细实现）：
  - 词边界匹配，避免 "agent" 命中 "reagent"：
      r"(?<![A-Za-z])" + re.escape(term) + r"(?![A-Za-z])"
  - 默认忽略大小写；case_sensitive 为 true 时严格匹配
  - 多词术语（如 "code review"）允许词间空白变化（\s+）
  - ⚠️ 跳过代码块内部（CODE_BLOCK_START 到 CODE_BLOCK_END 之间）：
       代码与数据不译，代码里的 agent 不算槽位
  - ⚠️ 跳过 front matter（YAML 头）

运行方式：
  python scripts/check_slots.py            统计槽位
  python scripts/check_slots.py --selftest 反例自测
  python scripts/check_slots.py --verify   翻译完成后核对命中率

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【冻结机制】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
定稿后冻结：算术语表内容的 sha256 存入 frozen_hash，frozen 设 true。

⚠️ 哈希必须【排除 frozen_hash 字段自身】再计算，否则会陷入循环依赖
   （哈希值取决于内容，而内容里又含哈希值）。
   做法：把除 frozen_hash 外的整个对象用 json.dumps(sort_keys=True) 序列化后取 sha256。

之后每次校验先核对 glossary_hash 是否与 slot_report.json 记录的一致，
不一致就报错退出并提示"术语表被改过，需重跑槽位统计"。

**理由**：若术语表可随时改，"100% 命中率"就没意义了（可以改表迁就译文）。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【⚠️ 校验器必须自带反例自测】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**一个失效的校验器比没有校验更危险**，它给出虚假的信心。
实际踩过的坑：术语检查逻辑因 bug 被静默禁用，脚本仍报告"全部通过"。

--selftest 必须：
  1. 构造已知小样本（含正确译法、错误译法、代码块内干扰项）
  2. 跑校验
  3. 断言：能【检出】错误译法、【忽略】代码块内干扰项
  4. 断言失败即退出码非 0 并打印明确错误
  ⚠️ 这个自测必须能真正失败。不要写永远通过的假自测。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【--verify：翻译后核对命中率】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
读 translated/*.md（译文），对每条术语的每个槽位核对是否用了指定译法。
按【文档】汇总，输出：
{ "doc": "mcp-introduction", "slots": 42, "hits": 40,
  "misses": [{"term":"agent","found":"代理","should":"智能体"}] }

⚠️ 注意区分两种未命中：
  - 译文该文档长度 < 原文 30%  → 判为【疑似漏译】，单独归类
  - 否则                        → 判为【译法不一致】
  不区分的话，整段漏译会污染术语命中率，让数字失去意义。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【控制台自检】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 术语条数，四种 handling 各多少条
2. 槽位总数
3. 槽位最多的 10 个术语
4. 零槽位术语清单（术语表里有但原文没出现 → 可能多余，需人工确认）
5. 反例自测结果（--selftest）
6. 冻结哈希

【约束】
  - 输入输出路径写成文件顶部常量（换课程只改这几行）
  - 关键步骤写中文注释
  - 幂等；退出码：成功 0，失败非 0

请给出 glossary.json 初始内容 + check_slots.py 完整代码。
```

---

## 交接模板

```
【此前进展】
已完成：体检 → 抓取 → 抽取 → 术语表与槽位校验（未做切块）

【槽位统计，来自 slot_report.json】
- 术语 N 条（translate N / keep_en N / bilingual N / acronym N）
- 槽位总数 N，覆盖 N 个文档
- 反例自测：通过
- 冻结哈希：xxxxx

【下一步】按术语表把 extracted/*.md 逐文档翻译成中文

【环境】只用标准库；Windows GBK，打印需 UTF-8
```

---

## 验收标准

| 项 | 标准 |
|---|---|
| 术语条数 | **≥ 60 条** |
| handling 覆盖 | 四种处理方式都用到（不应全是 translate） |
| 槽位总数 | 与语料规模匹配（约 76,000 词，槽位应在数千量级） |
| 零槽位术语 | 已列出并说明 |
| 代码块内术语 | **未被计入槽位** |
| 冻结哈希 | 已生成 |
| 反例自测 | 通过，**且能真正失败** |

---

## ⚠️ 一个必须理解的取舍

**"保留英文"的术语，译文里也保留英文。** 不要试图给所有术语都找中文译法。

| 术语 | 建议 | 理由 |
|---|---|---|
| `MCP` | 保留英文 | 协议名，无通行中文译名 |
| `token` | 保留英文 | 「词元」「令牌」都有歧义 |
| `vibe coding` | 保留英文 | 课程名 + 该运动的专有名称 |
| `prompt` | 翻「提示词」 | 已有通行译法 |
| `agent` | 翻「智能体」 | 已有较通行译法 |

**这就是 `handling` 要有四种取值、而不是简单英中对照的原因。**
