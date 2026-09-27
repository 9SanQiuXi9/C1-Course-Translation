# 管线 ⑤ 质量校验：可复制 Prompt

> **前置条件**：翻译进行中或已完成；术语表已冻结
> **产出**：`check_quality.py` → `work/reports/quality_report.json` + `work/reports/stats.json`
> **粒度**：按【文档】校验（不做切块）

---

## 主 Prompt

```
【项目背景】

我在把 Stanford CS146S 课程资料从英文翻译成简体中文，项目已跑到【质量校验】环节。
需要写一个校验脚本，目的是【证明】翻译质量，而不只是"我抽看了几段"。
所以每一层校验都必须产出可核对的数字。

【仓库】<仓库根目录>\
【实际目录结构（请严格按这些路径读写）】
  data/materials/          课程原始资料（只读，脚本绝不写入）
  data/fetched/            抓取归档（按域名分目录 + .meta.json）
  work/extracted/          抽取后的英文 Markdown 原文，57 个 .md
                           每个带 YAML front matter（source_file, origin_url,
                           title, extract_method, chars, english_words,
                           garbage_rate, code_blocks, tables, links）
  work/glossary/glossary.json    已冻结的术语表
  work/slots/slot_report.json    术语槽位统计（按文档粒度）
  work/reports/                  manifest.json / fetch_report.json / extract_report.json
  output/translated/            中文译文（<doc_id>.md）+ 文档级留痕（<doc_id>.PROMPT.md）
  output/prompts_to_send/       待发送的翻译任务
  verify_report.json            仓库根目录，已有的【术语层】校验结果

【已有产出：verify_report.json】
这是术语校验的已有结果，请你【复用】而不是重造：
  totals: {docs: 24, slots: 931, hits: 884, hit_rate: 0.9495,
           docs_suspected_missing_translation: 0, docs_not_translated_yet: 33}
  per_doc: 24 条
  conflict_check: 有
  glossary_hash: 有
含义：24 篇已译文档的术语命中率 94.95%，还有 33 篇尚未翻译。

⚠️ 本脚本的 L2 层应该【直接读 verify_report.json】，
   但需要补充它能算但没算的部分（见下面 L2 一节）。

【环境】
  - 只用 Python 标准库（re, json, os, math, random, hashlib, collections）
  - Windows GBK 控制台，脚本开头必须：
      try: sys.stdout.reconfigure(encoding="utf-8")
      except Exception: pass

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【子命令】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  python scripts/check_quality.py all        跑全部自动层
  python scripts/check_quality.py l1         结构完整性
  python scripts/check_quality.py l2         术语一致性（复用 verify_report + 补充）
  python scripts/check_quality.py l3         校验器反例自测
  python scripts/check_quality.py l4-sample  生成语义标注任务（供人工标）
  python scripts/check_quality.py l4-score   汇总人工标注，算一致性统计

【输出】
  work/reports/quality_report.json    各层明细
  work/reports/stats.json             汇总数字（供 README 引用）
  output/prompts_to_annotate/         L4 的两份标注任务

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【L1 结构完整性】（本脚本的主要缺口，verify_report 没做）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
先确定比对范围，否则数字没意义：
  - 原文范围：work/extracted/*.md 中，以 extract_report.json 里 status="ok" 的文档为准
  - 译文范围：output/translated/*.md（排除 .PROMPT.md）
  - 输出三类：已完成 / 尚未翻译 / 多余（译文有但原文没有）

逐篇比对 7 项：
  1. Markdown 标题行数（^#{1,6}\s）
  2. 代码块数量（CODE_BLOCK_START 标记数）
  3. 代码块内容【逐字节一致】
     ⚠️ 比较前先归一化换行符（\r\n → \n）与行尾空白，避免误报
  4. 表格行数（以 | 开头的行）
  5. 链接数量（https?:// 出现次数）
  6. 正文非空行数
  7. 长度比 = 译文非空白字符数 / 原文非空白字符数
     （中译英通常 0.4-0.8 属正常；<0.3 判为疑似漏译）

统计口径：逐项给出「达标篇数 / 已比对篇数」，如 "code_blocks_ok": "24/24"
⚠️ 任何一项不达标，必须列出具体是哪几篇

输出：
{
  "scope": {"src_ok_docs": 57, "translated": 24, "not_translated_yet": 33,
            "extra_translations": []},
  "per_doc": [{"doc":"...","title_lines":{"src":8,"dst":8,"ok":true},
               "code_blocks":{"src":3,"dst":3,"ok":true,"bytes_identical":true},
               "table_lines":{...},"links":{...},
               "length_ratio":0.62,"status":"ok"}],
  "totals": {"title_lines_ok":"24/24","code_blocks_ok":"24/24",
             "tables_ok":"...","links_ok":"...","codelines_byte_identical":"24/24",
             "length_ratio_median":0.62,"length_ratio_outliers":[...]}
}
⚠️ 只对【已翻译】的文档做逐项比对；未翻译的单独列出，不算失败。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【L2 术语一致性】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
直接读 verify_report.json 的 totals 和 per_doc，不要重算。

但请【补充】它没有的三部分：

(a) 按 handling 分组统计
    读 work/glossary/glossary.json，把槽位按术语的 handling 分成三类：
      translate（必须译成中文）/ keep_en 与 acronym（保留英文）/ bilingual
    分别给命中率。
    ⚠️ 为什么重要：两类判据完全不同。translate 类要在译文里找中文译法；
       keep_en 类要检查英文是否仍在。混在一起会掩盖问题。

(b) 疑似漏译单独归类
    长度比 < 0.3 的文档 → 判为【疑似漏译】，其术语未命中不计入 hit_rate
    理由：整段漏译会让该文档所有槽位失效，混进术语命中率会让数字失去意义。
    verify_report 里 docs_suspected_missing_translation 为 0，请核对这个结论。

(c) 术语漂移明细
    verify_report 的 per_doc 只有汇总数。请结合 slot_report.json 与译文，
    列出具体的漂移案例（哪篇、哪个术语、译成了什么），供人工修正。
    ⚠️ 这是给你自己修错用的，不需要穷尽，给前 20 条即可。

■ 必须实现的 is_content_line() 过滤
  英文原文里残留大量网页导航与页脚（实测占 15.3% 的行）。若统计术语槽位时不排除：
    - 槽位数虚高
    - 命中率永远到不了 100%（译文不含导航）
  判定规则：
    def is_content_line(line):
        urls = len(re.findall(r"https?://", line))
        if urls == 0: return True
        if re.match(r"^\s*!\[", line): return False            # 纯图片
        if re.match(r"^\s*[-*]?\s*A?\s*https?://", line): return False  # 导航项
        if urls >= 2: return False
        if len(line.strip()) < 120: return False               # 短行+含链接
        return True
  ⚠️ 若 verify_report.json 已经做了这个过滤，请在报告里注明；若没做，
     请重新统计并说明差异。仓库里 check_slots.py 是槽位统计脚本，可参考它的做法。

■ 核对 glossary_hash
  开头核对 glossary.json 当前哈希 与 verify_report.json 里记录的 glossary_hash
  是否一致。不一致 → 报错退出，提示"术语表已改动，需重跑 check_slots.py"。
  ⚠️ 哈希计算要排除 frozen_hash 字段自身，否则循环依赖。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【L3 反例自测】⚠️ 必须有，否则 L1/L2 的数字不可信
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**一个失效的校验器比没有校验更危险** —— 它给出虚假的信心。
实际踩过的坑：术语检查逻辑因 bug 被静默禁用，脚本仍报告"全部通过"。

做法：在内存里构造"被破坏的"样本，断言校验器必须报警。至少覆盖：
  1. 代码块被翻译了        5. 术语用了错误译法
  2. 代码块被删除了        6. 整段漏译（长度比 < 0.3）
  3. URL 被改写            7. 表格行被合并
  4. 标题行被删            8. 译文为空

要求：
  - 每个反例期望"必须被检出"
  - 任何一项没检出 → all_pass=false，退出码非 0，明确指出哪项失效
  - ⚠️ 不要写永远通过的假自测。先自问"如果我故意写错，这段逻辑真会报错吗"

输出：{"cases_total":8,"cases_detected":8,"all_pass":true,
       "cases":[{"name":"代码块被翻译","detected":true}]}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【L4 语义质量】（脚本只做抽样与统计，判定由人工完成）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 脚本无法调用大模型，所以语义判定由我在对话里人工完成。
   脚本负责：分层抽样 → 生成标注任务 → 汇总两份标注 → 算统计量。

■ l4-sample：分层抽样
  不要随机抽。按风险分层，目标 10-12 个文档 × 每篇 5 个自然段 = 50-60 个判定点：
    层1：字符数最长的 3 篇各抽 1 段
    层2：代码块最多的 3 篇各抽 1 段
    层3：表格最多的 3 篇各抽 1 段
    层4：术语密度最高的 3 篇各抽 1 段
    层5：extract_method="pdf" 的文档抽 2 段（garbage_rate 高的优先，风险大）
  ⚠️ 只从【已翻译】的文档里抽。每段从文档中部取 5 个自然段，
     跳过代码块、表格、以及 is_content_line() 判为非正文的行。
  用固定随机种子（20260717）保证可复现。

  生成 output/prompts_to_annotate/annotator_A.md 和 _B.md，每份含：
    段落原文 + 对应译文 + 判定标准
  ⚠️ 关键：标注任务里【不要给术语表】！
     否则标注者只是在复述我的口径，等于自己批改自己，一致性会虚高。
  ⚠️ 两份任务内容相同，要求我在【不同对话里独立完成】。

■ l4-score：汇总统计
  读 annotator_A.json / annotator_B.json，每个判定点含：
    是否漏译 / 是否误译 / 是否术语漂移 / 是否机器感 / 总体 PASS|FAIL

  a) 观察一致率 Po = 两人总体判定相同的比例
  b) Cohen's κ：
       Pe = P(A=PASS)·P(B=PASS) + P(A=FAIL)·P(B=FAIL)
       κ = (Po - Pe) / (1 - Pe)
       Landis & Koch：<0 差 | 0-0.20 轻微 | 0.21-0.40 一般 | 0.41-0.60 中等
                      0.61-0.80 显著 | 0.81-1.00 几乎完全一致
  c) 每个缺陷维度的检出率 + 95% Wilson 置信区间：
       p̂ = k/n
       中心 = (p̂ + z²/(2n)) / (1 + z²/n)
       半宽 = z·sqrt(p̂(1-p̂)/n + z²/(4n²)) / (1 + z²/n)
       区间 = [中心-半宽, 中心+半宽]，z = 1.96
     ⚠️ 必须用 Wilson，不能用正态近似。
        因为报"检出 0 个漏译"时，正态近似给出零宽度区间（统计上荒谬）；
        Wilson 给出 [0, 0.065] 这类合理区间。
  d) 分歧清单：两人判定不同的判定点，供人工裁定

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【汇总 work/reports/stats.json（供 README 引用）】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{
  "generated_by": "check_quality.py",
  "pipeline_stage": "quality_check",
  "scope": {"src_ok_docs": N, "translated": N, "not_translated_yet": N},
  "l1_completeness": {"docs":"24/24","title_lines":"24/24","code_blocks":"24/24",
                      "tables":"...","links":"...","codelines_byte_identical":"24/24"},
  "l2_terminology": {"source":"verify_report.json",
                     "slots":"884/931","hit_rate":0.9495,
                     "by_handling":{"translate":{...},"keep_en":{...}}},
  "l3_selftest": {"cases":"8/8","all_pass":true},
  "l4_semantics": null,
  "headline": {"docs_verified":"24/24","term_slots":"884/931",
               "selftest_cases":"8/8","inter_annotator_kappa":null}
}
⚠️ 所有数字必须由脚本计算，不允许手填常量。
⚠️ L4 未完成时置 null 并在控制台提示"L4 待人工完成"。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【控制台输出要求】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 比对范围：已译 N 篇 / 未译 N 篇（列出未译的）
2. L1 逐项：达标篇数 / 已比对篇数；不达标的列出文档名
3. L2：命中率 + 按 handling 分组；疑似漏译单独列出；给前 20 条术语漂移明细
4. L3：反例自测结果，未检出的明确指出
5. L4：抽样规模；未完成则提示下一步
6. 最终 headline 数字

【约束】
  - 只用 Python 标准库
  - 路径写成文件顶部常量（换课程只改这几行）
  - 关键步骤写中文注释
  - 退出码：全部通过 0；L1/L2/L3 有失败项或自测未通过返回非 0
  - 幂等
  - ⚠️ 绝不写入 data/ 目录

请先给出设计方案（各函数职责 + 文件结构 + 如何复用 verify_report.json），
我确认后再给完整代码。
```

---

## 交接模板

```
【此前进展】
已完成：抽取 → 术语 → 翻译（24/57）→ 质量校验

【校验结果，来自 work/reports/stats.json】
- L1：已译文档 24/24，代码块逐字节一致 24/24
- L2：槽位 884/931（94.95%），按 handling 分组
- L3：反例 8/8 全部检出
- L4：N 个判定点，Cohen's κ = 0.xx
- 剩余 33 篇待翻译

【下一步】补完剩余翻译 → 重跑校验 → 写 README / AI 日志 / AAR / 拿来说明

【环境】只用标准库；Windows GBK，打印需 UTF-8
```

---

## 出问题时怎么问

```
运行 check_quality.py 出问题了：

【我的操作】
python scripts/check_quality.py l2

【报错信息 / 异常结果】
（整段贴原文）

【我观察到的问题】
（例：L2 报的命中率是 88%，但 verify_report.json 里是 94.95%）

【我认为可能的原因】
（例：可能是 is_content_line 过滤规则与 check_slots.py 不一致，
      导致分母（槽位总数）不同）
```

| 症状 | 大概率原因 |
|---|---|
| L2 命中率与 verify_report 不一致 | `is_content_line` 过滤规则不同 → 分母不同 |
| L1 报"多余译文" | 把 `.PROMPT.md` 留痕文件误当译文了 |
| 代码块校验误报不一致 | 比较前没做换行符归一化 |
| 疑似漏译列表里全是正常文档 | 长度比阈值太严（中译通常 0.4-0.8 正常） |
| 自测永远通过 | 自测是假的，要求构造必然失败的样本 |
| Wilson 区间宽度为 0 | 用了正态近似，应改用 Wilson |
| L4 抽样抽到未翻译的文档 | 抽样范围没限定在已翻译集合 |

---

## 验收标准

| 层 | 项 | 标准 |
|---|---|---|
| L1 | 比对范围 | 明确区分已译/未译，未译不算失败 |
| L1 | 代码块逐字节一致 | 100% |
| L2 | 是否复用 verify_report | **复用**，不重算 |
| L2 | 按 handling 分组 | 三类分开统计 |
| L2 | 疑似漏译 | 单独归类，不混进命中率 |
| L2 | 与 verify_report 的一致性 | 差异必须解释（过滤规则是否一致） |
| L3 | 反例自测 | 全部检出，**且能真正失败** |
| L4 | 标注独立性 | 标注任务**不含术语表** |
| L4 | Cohen's κ + Wilson | 已算，给区间解释 |
| 汇总 | `stats.json` | 无手填常量；README 将引用 |
| 安全 | `data/` 零写入 | 确认没有改动原始资料 |
