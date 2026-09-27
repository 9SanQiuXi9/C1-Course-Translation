# 管线 ⑦ 一键复跑：可复制 Prompt

> **使用方式**：在新对话中把「主 Prompt」整段复制给 AI。不需要前置上下文。
> **前置条件**：前面 6 个环节的脚本都已存在
> **产出**：`run_all.py`（单入口）+ `config.yaml`（换源配置）+ `README.md`（使用说明）

---

## 这一环为什么直接对应 20 分

评分维度里有一条明确要求「处理流程是否**可复跑、可复用**」，评分信号写的是：

> ✅ 有脚本或清晰步骤、**换源可复用**、质量抽检
> ❌ **纯手工一次性**、不可复跑

**判断标准很简单**：

> **明天给你另一门课的 31 个文件，你多久能出同样结果？**

- 要重做一整天 → 没有管线
- 改几行配置、跑一条命令 → 有管线

**本环节就是把"有管线"变成可验证的事实。**

---

## 主 Prompt（复制这里开始）

```
【项目背景，请先读完再动手】

我在做一个课程资料的翻译项目：把一批英文课程资料翻译成中文，做成别人能复用的资料包。

我已经分 6 个环节写好了脚本，现在要做最后一环：一键复跑入口 + 换源配置 + 使用说明。

【已有的脚本（都在 scripts/ 目录）】
  build_manifest.py   体检：扫描资料，产出 manifest.json 账本
  fetch.py            抓取：补抓缺口，产出 fetch_report.json
  extract.py          抽取：把 html/pdf/spa 统一抽成 extracted/*.md
  chunk.py            切块：按标题切成 chunks.jsonl
  check_slots.py      术语：产出 glossary.json 与 slot_report.json
  translate_queue.py  翻译：工作队列管理，产出 translated/*.md
  check_quality.py    校验：四层校验，产出 quality_report.json 与 stats.json

【我要的三个东西】
  1. config.yaml      换源配置：把「会变的东西」集中到这里
  2. run_all.py       一键复跑入口：按正确顺序调用所有脚本
  3. README.md        使用说明：环境依赖、安装、运行示例、目录结构

【我的环境限制】
  - 只能用 Python 标准库。装不了第三方库（所以没有 pyyaml，要自己写个极简的
    YAML 解析，或者改用 JSON 配置文件 —— 你选更可靠的方案并说明理由）。
  - Windows，控制台是 GBK 编码，打印必须用 UTF-8。
  - ⚠️ 翻译环节（translate_queue.py）需要人工在对话里操作，无法全自动。
    这一点要在 run_all.py 和 README 里如实说明，不要假装全自动。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【1. config.yaml / config.json —— 换源配置】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
目标：换一门课程时，只改这个配置文件，其它脚本一行都不用动。

需要集中配置的项：
  course:
    id: "C1"
    name: "CS146S: The Modern Software Developer"
    source_language: "en"
    target_language: "zh"
  paths:
    materials_dir: "materials/"           # 原始资料目录
    offline_dir: "materials/CS146S_offline/"
    pages_dir: "materials/CS146S_offline/pages/"
    pdfs_dir: "materials/CS146S_offline/pdfs/"
    site_dir: "materials/CS146S_offline/site/"
    archive_dir: "archive/"
    extracted_dir: "extracted/"
    translated_dir: "translated/"
    merged_dir: "merged/"
    logs_dir: "logs/"
  files:
    page_map: "materials/CS146S_offline/page_map.json"
    all_urls: "materials/CS146S_offline/all_urls.txt"
    manifest: "manifest.json"
    fetch_report: "fetch_report.json"
    chunks: "chunks.jsonl"
    glossary: "glossary.json"
    slot_report: "slot_report.json"
    stats: "stats.json"
  chunking:
    min_chars: 500
    max_chars: 8000
    target_min: 2000
    target_max: 4000
  fetch:
    user_agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    timeout_seconds: 15
    retry_times: 3
    retry_delays: [2, 5, 10]
    polite_delay_seconds: 1.5
  quality:
    min_slots_hit_rate: 0.95
    length_ratio_range: [0.5, 1.5]
    l4_sample_blocks: 12
    l4_paragraphs_per_block: 5
    random_seed: 20260717

⚠️ 所有脚本都要改成从这个配置文件读路径，而不是各自硬编码。
   如果某个脚本还没改，请在 run_all.py 里做兼容（但要提示"建议统一到配置"）。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【2. run_all.py —— 一键复跑入口】⚠️ 注意执行顺序
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
正确顺序（这个顺序有依赖关系，不能随意调整）：

  步骤 1  build_manifest.py    （第一遍，pre_fetch）→ manifest.json
  步骤 2  fetch.py             → archive/ + fetch_report.json
  步骤 3  build_manifest.py    （第二遍，post_fetch）→ 更新 manifest.json
  步骤 4  extract.py           → extracted/*.md + extract_report.json
  步骤 5  chunk.py             → chunks.jsonl
  步骤 6  check_slots.py       → slot_report.json（术语表需先人工定稿并冻结）
  步骤 7  translate_queue.py   ⚠️ 需要人工介入，见下
  步骤 8  check_quality.py all → quality_report.json + stats.json

⚠️ 注意步骤 1 和步骤 3 是【同一个脚本跑两次】。
   它自己会检查 fetch_report.json 是否存在，决定用 pre_fetch 还是 post_fetch 模式。
   这是刻意设计：让脚本能"先跑也能跑、后跑也正确"。

【关于步骤 7 的人工介入】
翻译环节无法全自动（需要在对话里逐块翻译）。所以：
  - run_all.py 跑到步骤 7 时，应【暂停】并打印清晰指引：
      "翻译环节需要人工操作：
        1. 运行 python translate_queue.py next 获取待译任务
        2. 把生成的 prompt 复制到对话里，获得译文
        3. 运行 python translate_queue.py save <chunk_id> <译文文件>
        4. 重复直到 python translate_queue.py status 显示全部完成
       完成后重新运行：python run_all.py --from 8"
  - 提供 --from N 参数：从第 N 步开始跑（跳过前面的）
  - 提供 --only N 参数：只跑第 N 步
  - 提供 --dry-run 参数：打印将执行什么，但不真正执行

【run_all.py 的行为要求】
  a) 每一步执行前后打印清晰的分隔标题和该步耗时
  b) 每步执行后检查退出码：
       退出码 0    → 继续下一步
       退出码非 0  → 【停止】，打印失败步骤名、退出码、以及建议的排查命令
     ⚠️ 不要忽略退出码继续往下跑。这是"静默失败"的来源。
  c) 全部完成后：
       - 打印总耗时
       - 汇总所有产出的文件路径
       - 读 stats.json，打印 headline 数字（块数、槽位数、κ 值等）
       - 【退出码 0】
  d) 中途失败时【退出码非 0】
  e) 把完整运行日志同时写到 logs/run_all_<时间戳>.log
  f) 幂等提示：如果检测到某些产物已存在，提示"将覆盖"或"将跳过"，
     并支持 --force 强制重跑

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【3. README.md —— 使用说明】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 这一项要写得让【陌生人】能独立跑起来。必须包含：

1. 项目简介
   - 这是什么（把某课程英文资料翻译成中文的可复跑管线）
   - 一句话说明产出物

2. 环境要求
   - Python 版本（请查一下用了哪些语法，给出准确的最低版本，如 3.8+）
   - ⚠️ 明确写"仅使用标准库，无需 pip install"
   - 操作系统（Windows / macOS / Linux 均可，但 Windows 需注意控制台编码）

3. 快速开始（这是最重要的部分，要给可复制的具体命令）
   ```bash
   # 第一步：体检，看看手上有多少可翻译内容
   python scripts/build_manifest.py

   # 第二步：抓取补缺
   python scripts/fetch.py

   # 第三步：一键跑完（除翻译外的全部环节）
   python scripts/run_all.py
   ```
   并说明每一步的预期输出和大概耗时。

4. 目录结构
   用树状图列出所有目录和关键文件，每个文件一句话说明

5. 换一门课怎么用（这是"可复用"的直接体现）
   - 说明只需修改 config.yaml 里的哪几项
   - 给一个具体的"换成另一门课"的示例
   - 说明新课程的资料需要满足什么格式约定

6. 翻译环节怎么操作（人工介入部分）
   - 逐步说明 translate_queue.py 的四个子命令
   - 给一个完整的示例流程

7. 产出物说明
   - manifest.json / fetch_report.json / chunk_report 等各个报告是什么、怎么看
   - stats.json 里的关键数字含义

8. 已知缺口与限制（⚠️ 必须诚实写）
   - 哪些资源拿不到、为什么（区分真 404 / 需账号 / 网络不可达）
   - 哪些环节无法自动化
   - 抽取质量的已知问题（如 OCR PDF 的部分字符丢失）

9. 质量证据
   - 引用 stats.json 的数字（并注明"由脚本生成，未手工修改"）

10. 致谢与来源
    - 原始课程名称、官网、讲师
    - 说明译文由 AI 辅助翻译，原文版权归原作者/课程方

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【约束】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- 只用 Python 标准库
- 关键步骤写中文注释
- 控制台打印用 UTF-8
- run_all.py 要能在中途失败后重跑（幂等）

请给出三个文件的完整内容：config 配置文件、run_all.py、README.md
```

---

## 交接 Prompt 模板（用于开新对话）

```
【此前进展】
7 个环节的脚本都已写好并跑通。

【关键数字，来自 stats.json】
（把 headline 里的数字贴上来）

【我现在要做的事】
写最终交付物：README.md 主体内容 + AI日志 + AAR + 拿来说明

【我的环境限制】
- Windows，控制台 GBK，打印需 UTF-8

（然后把本环节的 Prompt 全文贴上来）
```

---

## 常见调试 Prompt

```
运行 run_all.py 出问题了：

【我的操作】
python scripts/run_all.py

【报错信息 / 异常结果】
（整段贴原文）

【我观察到的问题】
（例：步骤 3 失败了，但脚本继续往下跑到步骤 5）

【我认为可能的原因】
（例：没有检查子进程的退出码）

请定位原因并修复。⚠️ 要求：任何一步失败都必须停止并返回非 0 退出码。
```

| 症状 | 大概率原因 | 该说什么 |
|---|---|---|
| 某步失败但继续往下跑 | 没检查退出码 | "请检查每步退出码，非 0 就停止" |
| 换课程后路径报错 | 脚本里还有硬编码路径 | "请把所有路径改成从 config 读" |
| 重复运行结果不同 | 没做幂等 | "请支持 --force 和跳过已存在产物" |
| 找不到 yaml 模块 | pyyaml 装不了 | "请改用 JSON 配置，或自己写极简解析" |
| 中文打印乱码 | 控制台 GBK | "请在脚本开头设 stdout 为 UTF-8" |

---

## 验收标准

| 项 | 标准 |
|---|---|
| 一键跑通 | `python run_all.py` 从零到产出 `stats.json`，退出码 0 |
| 换源测试 | **改 config 里的路径后能跑另一门课**（这是"可复用"的直接证据） |
| 失败停止 | 任一步失败即停止，退出码非 0 |
| 人工介入提示 | 翻译步骤有清晰指引，不假装全自动 |
| README 完备 | 含 Python 版本、无需安装依赖、可复制的命令、目录结构、换源说明、已知缺口 |
| 日志留档 | `logs/run_all_<时间戳>.log` 已生成 |

---

## ⚠️ 一个容易被忽略但很值钱的动作

**做一次真实的"换源测试"。**

找任意一个别的课程的几个 html 文件（或者**把你自己 31 篇里的 3 篇复制到新目录**），
改 `config.yaml` 里的路径，跑一遍。

**如果能在几分钟内产出结果** → 你的管线**真的可复用**，这是 20 分的直接证据。

**如果跑不通** → 说明有硬编码残留，现在发现比被评委发现好。

**把这次换源测试记录进 AAR**，它比任何"我觉得可以复用"的声明都有力。

---

## 三个交付物写完后

| 交付物 | 对应本环节的什么 |
|---|---|
| `README.md` | 本 Prompt 的第 3 项 |
| `AI日志.md` | 从 `logs/` 里的 Session 记录摘取 |
| `AAR.md` | 含"换源测试"结果、失败经验、改进方案 |
| `拿来说明.md` | 从各环节的交接记录里挑 3 个案例 |

**注意 README 里的所有数字都要来自 `stats.json` / `manifest.json`，
并在文中注明"由脚本生成，未手工修改"。**
