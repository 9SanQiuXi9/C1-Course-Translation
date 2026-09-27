# C1 课程资料中文翻译

Stanford **CS146S: The Modern Software Developer** 课程资料的
**获取 → 抽取 → 术语 → 翻译 → 校验**全流程，以及可复现、可换源的完整管线。

> 换源跑另一批资料、以及各脚本的完整参数，见
> **[docs/材料翻译流水线SOP.md](docs/材料翻译流水线SOP.md)**。
> 本文档只给「这是什么、有什么、怎么用」。

---

## 0. 交付物索引

建议阅读顺序：**README → AI 日志 → 拿来说明 → AAR 复盘**。

| 交付物 | 位置 | 用途 |
|---|---|---|
| **README.md** | 仓库根目录（本文件） | 资料包说明：来源、覆盖范围、翻译流程、使用方法 |
| **AI 日志** | [AI日志.md](AI日志.md) → [docs/AI协作日志.md](docs/AI协作日志.md) | 用了什么工具、什么 prompt、踩了什么坑（11 个坑 + 10 条失误） |
| **拿来说明** | [拿来说明.md](拿来说明.md) → [docs/案例说明.md](docs/案例说明.md) | 3 个案例：关键决策/产出如何借助 AI 做出来（含原文·prompt·产出·对比） |
| **AAR 复盘** | [AAR复盘.md](AAR复盘.md) → [docs/AAR.md](docs/AAR.md) | 七维度复盘：目标范围 · 决策风险 · 工具使用 · 自行把关 · 提示词 · 交接标准 · 节奏分配 |
| 管线说明书 | [docs/材料翻译流水线SOP.md](docs/材料翻译流水线SOP.md) | 换源流程、各脚本完整参数、排错、改代码注意事项 |

**关键产物**

| 产物 | 位置 |
|---|---|
| 中文译文（41 篇，核心交付） | [`output/translated/`](output/translated/) |
| 英文原文（57 篇，便于对照） | [`work/extracted/`](work/extracted/) |
| 体检账本（脚本生成） | [`work/reports/manifest.json`](work/reports/manifest.json) |
| 术语表（机读 + 人工复查） | [`work/glossary/glossary.json`](work/glossary/glossary.json) · [`glossary.md`](work/glossary/glossary.md) |
| 质检数字（脚本生成） | [`work/quality/stats.json`](work/quality/stats.json) |
| 一键入口 | [`scripts/run_all.py`](scripts/run_all.py) |

> **关于目录布局**：本仓库分三层 —— `work/` 是工作层（可随时重跑生成）、
> `output/` 是交付层、根目录是导航层。根目录的 `AI日志.md` / `AAR复盘.md` /
> `拿来说明.md` 是**指路文件**（约 2–3 KB），正文在 `docs/` 下，**内容只有一份副本，不会漂移**。

> **关于 `docs/` 里的文件来源**：为便于区分，说明如下 ——
>
> | 文件 | 来源 |
> |---|---|
> | `docs/AI协作日志.md` · `docs/AAR.md` · `docs/案例说明.md` · `docs/材料翻译流水线SOP.md` · `docs/prompts/`（11 个模板） | **本项目产出** |
> | `docs/CHALLENGE.md` · `docs/challenge.json` · `docs/challenge.yaml` · `docs/rubric.json` | C1 挑战**下发时自带**的任务说明与评分标准，非本项目产出 |

---

## 1. 资料包说明

本包把 CS146S 的公开课程资料整理成一份**可离线阅读的中文材料**，并附上产生它的管线。

| 组成部分 | 内容 |
|---|---|
| **输入** | 课程官网页面、阅读材料、讲义、作业仓库、补充文档的本地快照 |
| **中间产物** | 统一 Markdown 英文原文、冻结术语表、术语槽位统计、质检报告 |
| **交付** | **41 篇中文译文**（`output/translated/`），逐篇带生成留痕 |
| **管线** | 10 个 Python 脚本，纯标准库，可一键重跑、可换源复用 |
| **账本** | `work/reports/manifest.json` —— 记录口径、逐文档可信度、抓取缺口分类，**本文所有数字都能在它里面查到** |

**它不是**：不是课程官方材料，不是逐句对照的双语版，也不是自动机翻产物。

---

## 2. 来源与覆盖范围

### 2.1 来源

资料来自 CS146S 公开渠道，按 `manifest.json` 的 `source_class` 分六类：

| 类别 | 含义 | 条数 |
|---|---|---|
| `reading` | 课程阅读材料（官网 Reading 区块的文章与 PDF） | 40 |
| `github` | GitHub 仓库（作业 / 指定阅读） | 5 |
| `official_site` | 课程官网（themodernsoftware.dev） | 1 |
| `lecture` | 讲义（官网 Lectures 区块：Google Slides / PDF） | 1 |
| `supplemental` | 非课程官方材料（本地附加文档 / 干扰项） | 1 |
| `video` | 视频（YouTube） | 0（未纳入翻译） |

此外 `data/fetched/` 内另有 **15 个域名、22 篇归档补充阅读**（含 a16z、cognition.ai、
graphite.dev、raw.githubusercontent.com、resolve.ai、semgrep.dev、vercel.com、
warp.dev、figma.com、mihaileric.com、reactjs.org 等）—— 这些不在课程官方目录内，
是抓取阶段一并归档的外部材料，也参与了抽取与翻译。

### 2.2 规模

本节所有数字都出自 [`work/reports/manifest.json`](work/reports/manifest.json)，
可逐项复核（见 2.3）。**不手写数字** —— 手写的数字会随重跑失效且无法追溯。

| 项 | 数值 | manifest 字段 |
|---|---|---|
| 课程原始资料 | 45 文件 / 28.7 MB（31 HTML + 3 PDF + 官网快照 + 1 中文原生文档） | — |
| 抓取归档 | 49 文件 / 12.9 MB（15 个域名目录，每份数据带 `.meta.json` 证据链） | — |
| 阅读文章本地归档 | 31 篇 HTML + 3 份 PDF | `summary.local_archived` |
| 阅读文章抽取成功 | 27 / 31 | `summary.reading_html_ok` |
| **可翻译正文（严格口径）** | **517,216 字符 / 76,324 英文词** | `summary.reading_translatable_chars` |
| 剥壳前全量（宽松口径） | 3,805,381 字符 / 464,510 英文词 | `summary.totals.chars_loose` |
| 抽取产出 | **57 篇** Markdown（`work/extracted/`） | `items[].text_path` |
| 术语表 | **99 条**（83 translate / 12 acronym / 3 keep_en / 1 bilingual），已冻结 | `work/glossary/glossary.json` |
| 术语槽位 | 3,976（在 41 篇译文范围内可核对） | `work/quality/stats.json` |

### 2.3 为什么这些数字可信

`manifest.json` 不只是「一个数字文件」，它记录了口径、交叉校验结果与不确定项。
以下三点是它真正的价值，也是本包可复核性的来源。

**① 两个口径同时保留，差异过大就交人工复核**

「可翻译正文 517,216 字符」是**严格口径**：剥掉导航、页脚、链接、图片行、代码块
之后剩下的正文。宽松口径（3,805,381 字符）是剥壳前的全量。

两个数字**都保留**，不取其一 —— 因为差异过大说明剥壳不干净、正文字数不可信。
manifest 会据此标出 `needs_review_ids` 交人工复核，而不是在两个数字里默默选一个。

**② 逐文档标记可信度，不确定就说不确定**

| 标记 | 篇数 | 含义 |
|---|---|---|
| `extract_warnings` | 33 | 抽取过程有告警（如剥离过激已回退） |
| `chars_reliable = false` | 6 | 字数**不可靠**，已如实标记 |
| `garbage_rate > 0.10` | 11 | 疑似乱码，已标记 |
| `failure_root_cause` | 5 | 写明失败根因 |

**③ 抓取缺口按 5 种原因分类，且严格区分「确认不存在」与「未核查」**

`summary.unavailable_total = 108` 条，全部进入 `known_gaps`：

| 原因 | 条数 | 语义 |
|---|---|---|
| `already_archived` | 29 | 此前已归档，本轮未重复请求 |
| `http_404` | 15 | 服务器明确返回「不存在」——**确定性结论** |
| `needs_account` | 20 | 需 Google 账号登录，无法自动抓取 |
| `not_attempted` | 41 | 本轮未发起请求（如 `--dry-run`）——**未核查** |
| `unreachable_automated` | 3 | YouTube 等无法自动获取 |

> ⚠️ 这五类**不可混淆**。`http_404` 是「确认不存在」，而 `not_attempted`
> 与 `network_error` 是「**未核查**」—— 后者绝不能被当成前者。
> 证书失败、网络抖动都不允许把已有结论降级。

### 2.4 怎么复核

```bash
# ① 重新生成账本（不改任何已有产出，约 1 秒）
python scripts/build_manifest.py

# ② 打印关键数字
python -c "import json;m=json.load(open('work/reports/manifest.json',encoding='utf-8'));print(m['summary']['reading_translatable_chars'],m['summary']['totals'])"

# ③ 看交叉校验范围与需人工复核的文件
python -c "import json;m=json.load(open('work/reports/manifest.json',encoding='utf-8'));print(m['cross_check']['scope']);print(m['cross_check']['needs_review_ids'])"

# ④ 看 108 条不可得资源的分类
python -c "import json;m=json.load(open('work/reports/manifest.json',encoding='utf-8'));print(m['summary']['unavailable'])"

# ⑤ 看某个文档的逐项证据（把 <doc_id> 换成 work/extracted/ 里的文件名）
#    注意用 .get()：并非每个 item 都有全部字段（如 failure_root_cause 仅 5 篇有）
python -c "import json;m=json.load(open('work/reports/manifest.json',encoding='utf-8'));i=[x for x in m['items'] if x['id']=='<doc_id>'][0];print({k:i.get(k) for k in ('chars','noise_ratio','garbage_rate','chars_reliable','failure_root_cause')})"
```

> 上面命令都是**单行**，在 PowerShell / cmd / bash 里都可直接粘贴执行。
> 需要换行时请自行拆分，不要用 `\` 续行（PowerShell 不支持）。

`manifest.json` 顶层结构：

| 字段 | 内容 |
|---|---|
| `summary` | 核心数字 + 按状态/来源分类计数 |
| `cross_check` | 严格 vs 宽松逐文件对比、`needs_review_ids`、口径说明 |
| `items[]` | **逐文档证据**：`chars` / `noise_ratio` / `garbage_rate` / `chars_reliable` / `failure_root_cause` / `text_path` |
| `known_gaps[]` | 108 条不可得资源及其根因 |
| `thresholds` | 判定阈值（`min_empty_chars=500`、`min_ok_chars=3000`、`suspect_noise_ratio=0.9`） |
| `status_values` | 14 种状态取值全集 |
| `paths` | 各输入输出路径，便于核对读的是哪份资料 |

### 2.5 翻译覆盖

```
抽取产出 57 篇
├── 已译            41 篇  (71.9%)
├── 待译             7 篇  (archive-* 补充阅读，非核心课程)
└── 无可译内容        9 篇  (见第 6 节「已知缺口」)
```

**范围说明**：翻译按「核心课程优先」推进，因此 `archive-*` 归档补充阅读中
还有 7 篇未译。它们已抽取完成、可直接进入翻译队列，不属于缺口。

---

## 3. 目录结构

```
C1-课程资料中文翻译/
├── data/                        输入（durable，改动少）
│   ├── materials/                 课程原始资料（只读，脚本绝不写入）  45 文件 / 28.7 MB
│   └── fetched/                   抓取归档，按域名分目录 + .meta.json  49 文件 / 12.9 MB
│
├── work/                        中间产物（regenerable，可随时重跑生成）
│   ├── reports/                   manifest.json ★ 全项目的账本：口径 + 逐文档可信度
│   │                                + 抓取缺口分类；另有 fetch_report / extract_report
│   ├── extracted/                 抽取后的 Markdown 英文原文          57 文件
│   ├── glossary/                  glossary.json（机读）· glossary.md（人工复查）
│   ├── slots/                     slot_report.json（术语槽位）
│   ├── quality/                   l1/l2/l3_report.json · stats.json（质检）
│   └── logs/                      run_all.py 每步完整输出留档
│
├── output/                      最终交付
│   ├── translated/                41 篇中文译文 + <doc_id>.PROMPT.md 留痕 + _progress.json
│   └── prompts_to_send/           每篇文档的待译任务 prompt（过程产物，已 gitignore）
│
├── docs/                        项目文档
│   ├── 材料翻译流水线SOP.md        ★ 管线完整说明书
│   ├── CHALLENGE.md · challenge.* · rubric.json
│   └── prompts/                   各环节的可复制 Prompt 模板（11 个，长期保留）
│
├── scripts/                     10 个管线脚本
└── README.md · .gitignore
```

**找文件的约定**：想知道「输入在哪」看 `data/`；「中间结果在哪」看 `work/`；
「要交付的东西在哪」看 `output/`。`work/` 全部可重新生成。

> ⚠️ 注意区分两个「prompt」目录：
> · `docs/prompts/` —— 各环节的**模板**（静态、长期保留，人写给人看的）
> · `output/prompts_to_send/` —— 每篇文档的**动态任务**（`translate_queue.py next` 生成，可随时重跑）

---

## 4. 翻译流程

### 4.1 管线

```
⓪ 体检       build_manifest.py     → work/reports/manifest.json
① 抓取       fetch.py              → data/fetched/ + work/reports/fetch_report.json
② 抽取       extract.py            → work/extracted/*.md + extract_report.json
③ 术语       init_glossary.py      → work/glossary/glossary.json + glossary.md
④ 槽位       check_slots.py        → work/slots/slot_report.json
⑤ 质检       check_quality.py      → work/quality/stats.json（L1 结构 / L2 术语 / L3 自测）
⑥ 翻译       translate_queue.py    → output/prompts_to_send/ + output/translated/
```

### 4.2 一键跑 ⓪~⑤

```bash
python scripts/run_all.py              # 全部自动层（⑥只 dry-run，不联网）
python scripts/run_all.py --list       # 只看计划
python scripts/run_all.py --help       # 全部选项
```

第 ① 步**默认只做 `--dry-run`**（不联网、只登记与规划）。要真实抓取加 `--with-fetch`。

### 4.3 翻译是人工循环

**脚本不调用任何大模型 API**（本项目按无密钥、无额度设计）。翻译动作由人完成，
脚本负责**排队 → 生成精准 prompt → 严格校验 → 落盘 → 留痕 → 进度**：

```bash
python scripts/translate_queue.py status            # 进度
python scripts/translate_queue.py next --count 3    # 生成 3 个待译 prompt
#   → output/prompts_to_send/
#   → 交给翻译者产出中文 Markdown
python scripts/translate_queue.py save <doc_id> <译文文件>
```

`save` 是**硬闸门**，四项校验任一不过就拒收：

| 校验 | 说明 |
|---|---|
| 代码块逐字节一致 | 代码不许被「顺便翻译」 |
| URL 全保留 | 链接不许被改写 |
| 标题行数一致 | 结构不许丢 |
| 长度比在合理区间 | 防整段漏译 / 注水 |

通过后写入 `output/translated/<doc_id>.md`，并保存 `<doc_id>.PROMPT.md` 留痕
（可复现当初给翻译者的术语约束），同时更新 `_progress.json`。

**为什么按文档排队而不是整篇丢给 AI**：一篇最多约 99,000 字符。一次性翻译会让
模型悄悄跳过中间部分，而返回值看起来是完整的（最危险）；一处错了无法定位，
也无法逐篇验收。> 20000 字符的文档允许在**标题边界**折成 2–3 段，不按字数硬切。

### 4.4 术语一致性怎么保证

不靠「事后替换」，而靠**每篇 prompt 带上该篇真正用到的术语约束** ——
只列该文档命中的术语（通常十几条），不把 99 条全塞进去（那会干扰模型）。

术语表与译文之间用 `frozen_hash` 绑定：术语表一旦改动，`check_slots.py` 会拒绝
沿用旧槽位统计，必须显式 `--accept-glossary-change` 重算 —— 否则「命中率」可以
靠改表来迁就译文，指标就失去意义。

### 4.5 验收

```bash
python scripts/check_quality.py all                   # L1 结构 + L2 术语 + L3 自测
python scripts/check_slots.py --verify                # 按文档核对术语命中率
```

**当前质检结果**（41 篇已译文档）：

| 层 | 结果 |
|---|---|
| L1 结构 | 标题行数 41/41 · 代码块数量 41/41 · 代码块逐字节 41/41 · 表格行数 41/41 · 链接数量 41/41 |
| L1 长度 | 中位长度比 0.5591（合理区间内） |
| L2 术语 | 槽位 3251/3976 = **81.77%**，其中确凿漂移仅 91 处（占 2.29%） |
| L3 自测 | 反例自测 **8/8** 通过 |

> L2 的 81.77% 里，未命中大部分是**段落配对偏移**（参考文献区逐条不对齐），
> 真正「全篇都没用指定译法」的漂移只有 91 处。报告把两者分开列出，不混为一谈。
>
> L2 另有 L4 语义层（人工标注 + Cohen's κ + Wilson 区间），代码完整但需人工填写
> 标注文件，**不在 `all` 内执行**。

### 4.6 自测

```bash
python scripts/check_slots.py --selftest        # 槽位/术语校验器反例自测
python scripts/check_quality.py l3              # 质检器反例自测
python scripts/translate_queue.py selftest      # 译落盘校验器反例自测
python scripts/test_fetch_logic.py              # 抓取重试与口径自测
```

> 这些都是**能真正失败**的反例自测（已实测注入 bug 会 exit≠0）。
> 失效的校验器比没有校验更危险 —— 它会给出虚假的信心。

---

## 5. 使用方法

### 5.1 只想读译文

直接看 `output/translated/*.md`（41 篇中文 Markdown），不需要跑任何脚本。

### 5.2 想核对某篇译得对不对

同名的 `<doc_id>.PROMPT.md` 里有当初生成的完整任务说明与术语约束；
英文原文在 `work/extracted/<doc_id>.md`。

### 5.3 想自己重跑整条管线

```bash
cd C1-课程资料中文翻译
python scripts/run_all.py              # 约 2 分钟（抽取步骤占绝大部分）
```

### 5.4 想换一份资料复用这套管线

```bash
python scripts/run_all.py --source-root /path/to/new-root --materials-dir /path/to/new-root/materials --course-dirname MYCOURSE --from-corpus-only --max-terms 120 --no-fetch
```

> 写成**单行**是刻意的：`\` 续行只有 bash 支持，PowerShell 与 cmd 会把每一行
> 当成独立命令执行（报 `'--source-root' is not recognized`）。
> 上面这条在 PowerShell / cmd / bash 里都能直接粘贴运行。
>
> ⚠️ `/path/to/new-root` 是**占位符**，需替换成你自己的目录后才能执行
> （直接跑会因目录不存在而失败）。`--from-corpus-only` 的使用条件与验收清单见 SOP 第 4 节。

`--source-root` 保证所有产出落到新目录，完全不碰本仓库的 `work/` `output/`。
`--from-corpus-only` 让术语表**从新语料重建**，而不是沿用本项目的术语表
（沿用会让旧领域的定稿术语变成大量零槽位噪声）。详见 SOP 第 4 节。

### 5.5 环境要求

- **Python 标准库即可，无第三方依赖**
- Windows 控制台 GBK：所有脚本已把 stdout 重配置为 UTF-8
- 若 HTTPS 全部验证失败（部分环境默认信任库为空），设置 CA bundle：

  ```bash
  set MF_CA_BUNDLE=C:\path\to\cacert.pem          # Windows cmd
  $env:MF_CA_BUNDLE="C:\path\to\cacert.pem"       # PowerShell
  export MF_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt   # Linux/macOS
  ```

  也支持标准变量 `SSL_CERT_FILE` / `REQUESTS_CA_BUNDLE`。

---

## 6. 已知缺口

### 6.1 无可译内容（9 篇）

| 文档 | 原因 |
|---|---|
| `how-openai-uses-codex` | PDF 用 Type3 矢量字形且字体缺失 `/ToUnicode` 映射，字符码到 Unicode 无映射关系，正文**客观不可恢复**（已按纪律不输出乱码） |
| `course-site-spa`<br>`archive-f.convertkit.com-ck.5-6f8d2461` | 官网 SPA，正文在打包 JS 中，抽取未取到正文（`extract.py` 缺陷） |
| `how-warp-uses-warp` | 原站为 Notion 页面，正文由客户端 JS 动态渲染，静态抓取只有应用外壳 |
| `archive-www.figma.com-Warp---Stanford--Copy--e1c08306` | Figma 幻灯片，内容由 JS 动态渲染，静态抓取只剩标题 |
| `good-context-good-code` | Ghost 私有模式，正文需付费/订阅/访问码，静态抓取只拿到订阅表单 |
| `peeking-under-the-hood-of-claude-code` | Medium 对自动化访问返回反爬拦截，正文从未取得 |
| `archive-app.kit.com-subscriptions-c7e965bf` | 抓到的是登录页，不是正文 |
| `lessons-from-ai-code-reviews` | 本地文件 0 字节：抓取阶段完全没拿到内容 |

这 9 篇已从翻译队列中排除并标注原因，不会被误当成「漏译」。

### 6.2 待译（7 篇）

`archive-*` 归档补充阅读，非核心课程内容：
`archive-a16z.com-martin-casado-819a7ad5`、
`archive-raw.githubusercontent.com-README-5285d5b3`、
`archive-resolve.ai-index-51fc7e81`、`archive-semgrep.dev-index-e5277db8`、
`archive-www.mihaileric.com-index-76879b6c`、`archive-www.warp.dev-index-8d73894f`、
`archive-www.warp.dev-university-345355c4`

### 6.3 其他限制

- **官网 SPA 抽取有损**：正文在打包 JS 中，需从 `children:"..."` 文本节点重建结构。
- **上游噪声**：部分页面抽取残留导航/页脚文本；术语统计已排除含 URL 的行
  （排除 1,445 行 / 8,752 行，占 16.5%）。
- **`archive-raw.githubusercontent.com-system_prompt_uafs-3e1f551e`** 有 5 行多余标题，
  是 PDF/HTML 抽取时重复 H1 被截断的产物。
- **L4 语义层未完成**：需人工填写 `work/quality/annotator_A/B.json`，当前为空白模板。
- **术语候选抽取未做句边界限制**：换源时 `--from-corpus-only` 产出的候选里会混入
  跨句碎片（如 `reservoir requires careful`），需人工筛选。

---

## 7. 免责与使用范围

- 原始资料版权归各自作者与机构所有。本包**仅供学习交流**，
  不得用于商业用途；如需引用请回到原始来源。
- 译文为**学习用参考译本**，非官方译文；技术表述以英文原文为准。
- 原文中出现的邮箱、姓名等联系信息，属于上游公开材料的原始内容，
  翻译时按「逐字保留」处理，未作改动。

---

## 8. 环境与维护

- **无第三方依赖**：10 个脚本全部只用 Python 标准库。
- **不手改 JSON**：`manifest.json` / `glossary.json` / `slot_report.json` / `stats.json`
  全部由脚本生成。手改会让口径漂移，也会破坏 `frozen_hash` 校验。
- **改术语表的正确姿势**：改 `scripts/init_glossary.py` 里的 `CURATED` 字典 →
  重跑 `init_glossary.py` → `check_slots.py --accept-glossary-change`。
- **代码修改注意事项**（8 条踩坑记录）见
  [docs/材料翻译流水线SOP.md](docs/材料翻译流水线SOP.md) 第 8 节。
