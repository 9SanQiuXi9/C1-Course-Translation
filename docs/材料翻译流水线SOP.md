# 材料翻译流水线 SOP

> 本文档描述**当前仓库里真实存在**的脚本与参数。凡本文档写到的选项，都用
> `python scripts/<脚本> --help` 验证过。文档里出现的路径一律是**相对路径或占位符**，
> 不写某台机器的绝对路径 —— 那样既泄漏环境信息，换机器也必然失效。

---

## 1. 定位与两条铁律

**这是什么**：把一批英文课程资料（HTML / PDF / 网页归档）变成中文译文的半自动管线。

**铁律一：脚本不调用任何大模型 API。**
本项目按「无密钥、无额度」设计。翻译动作由人完成，脚本负责**排队 → 生成精准 prompt
→ 严格校验 → 落盘 → 留痕 → 进度**。`translate_queue.py save` 是硬闸门，四项校验
（代码块逐字节 / URL 全保留 / 标题数一致 / 长度比）任一不过就**拒收**。

**铁律二：所有数字必须来自脚本，不许手写。**
`manifest.json`、`glossary.json`、`slot_report.json`、`stats.json` 全部由脚本生成。
手改 JSON 会让口径漂移，也会破坏 `frozen_hash` 校验。

---

## 2. 目录布局

```
.
├── data/                        输入（只读为主）
│   ├── materials/               课程原始资料
│   │   └── <课程名>/            默认 CS146S_offline
│   │       ├── pages/           本地 HTML 页面
│   │       ├── pdfs/            PDF
│   │       ├── site/            站点快照
│   │       ├── all_urls.txt     URL 清单（每行一个 URL）
│   │       └── page_map.json    URL → 本地文件 映射
│   └── fetched/                 抓取归档（fetch.py 产出，含 .meta.json 证据链）
│
├── work/                        中间产物（可重新生成）
│   ├── extracted/               ★ 抽取出的英文原文 Markdown
│   ├── glossary/
│   │   ├── glossary.json        ★ 术语表（冻结，带 frozen_hash）
│   │   └── glossary.md          人工复查用
│   ├── reports/
│   │   ├── manifest.json        体检账本（总账，下游都读它）
│   │   ├── extract_report.json
│   │   ├── fetch_report.json
│   │   └── verify_report.json
│   ├── slots/slot_report.json   术语槽位统计
│   ├── quality/                 L1/L2/L3 质检报告 + stats.json
│   └── logs/                    run_all.py 每步完整输出留档（已 gitignore）
│
├── output/                      交付
│   ├── translated/              ★ 中文译文 Markdown（核心产物）
│   └── prompts_to_send/         待译任务 prompt（可重新生成，已 gitignore）
│
└── scripts/                     10 个脚本
```

★ = 关键产物。

---

## 3. 一键入口

`scripts/run_all.py` 串联全流程，**默认不在你不知情时联网**。

```bash
python scripts/run_all.py                # ①~⑥（⑥ 只 dry-run，不发请求）
python scripts/run_all.py --list         # 只看计划，不执行
python scripts/run_all.py --with-fetch   # ⑥ 做真实网络抓取
python scripts/run_all.py --no-fetch     # 完全跳过 ⑥
```

### 六步

| 编号 | 步骤 | 脚本 | 关键产物 |
|---|---|---|---|
| ① | 体检账本 | `build_manifest.py` | `work/reports/manifest.json` |
| ② | 抽取 | `extract.py` | `work/extracted/*.md` |
| ③ | 术语表 | `init_glossary.py --md` | `work/glossary/glossary.json` + `.md` |
| ④ | 槽位 | `check_slots.py` | `work/slots/slot_report.json` |
| ⑤ | 质检 | `check_quality.py all` | `work/quality/stats.json` |
| ⑥ | 下载 | `fetch.py --dry-run` | `data/fetched/` |

> ⚠️ **翻译不在 `run_all.py` 里**。因为翻译要人做，串进去会停在半截。
> 翻译是第 ⑤ 步之后的独立循环，见第 6 节。

### 找错用

```bash
python scripts/run_all.py --only quality        # 只跑一步
python scripts/run_all.py --skip slots          # 跳过一步
python scripts/run_all.py --from glossary       # 从③跑到尾
python scripts/run_all.py --continue-on-error   # 某步失败仍继续
python scripts/run_all.py --quiet               # 只输出汇总表
```

每步都做**产物存在性校验**，不只看退出码 —— 脚本可能「成功退出但没写出东西」。
控制台只打印每步输出尾部，完整输出在 `work/logs/<步骤>-<时间戳>.log`。

退出码：`0` 全部通过 · `1` 有步骤失败 · `64` 参数错误。

---

## 4. 换源（复用这套管线做另一批资料）

### 4.1 一条命令换源

关键在于把**所有产出都落到新目录**，完全不碰主仓库的 `work/` `output/`：

```bash
python scripts/run_all.py --source-root /path/to/new-root --materials-dir /path/to/new-root/materials --course-dirname MYCOURSE --from-corpus-only --max-terms 120 --no-fetch
```

> 命令写成**单行**是刻意的：`\` 续行只有 bash 支持，PowerShell 与 cmd 会把每行
> 当成独立命令（报 `'--source-root' is not recognized`）。本文件的命令都能直接粘贴运行。

- `--source-root ROOT` 之后，所有中间产物与交付都落到 `ROOT/work/` 与 `ROOT/output/`。
- `--from-corpus-only` 让 ③ 步**不带种子**、纯从新语料抽候选建表（见 4.3）。

### 4.2 新源需要准备什么

```
<materials>/<课程名>/
├── pages/*.html          页面（或 pdfs/、site/）
├── all_urls.txt          URL 清单
└── page_map.json         {"https://...": "pages/xxx.html"}
```

只要这三样齐备，`run_all.py` 就能跑通 ①~⑤，**不需要改任何源码**。

### 4.3 术语表：必须重建，不能沿用

这是换源最容易踩的坑。

```bash
# ❌ 沿用旧术语表：换到别的领域时，旧领域的定稿术语对新语料是
#    100% 的「零槽位噪声」。实测水培语料：99 条里 98 条零槽位。
python scripts/init_glossary.py --extracted-dir <新源>/work/extracted

# ✅ 从新语料重建
python scripts/init_glossary.py --extracted-dir <新源>/work/extracted --glossary <新源>/work/glossary/glossary.json --from-corpus-only --max-terms 120
```

同一份水培语料实测对比：

| 模式 | 术语条数 | 零槽位 | `frozen` |
|---|---|---|---|
| 默认（带种子） | 99 | **98** | `true` |
| `--from-corpus-only` | 40 | **0** | `false` |

**`--from-corpus-only` 产出的表是草稿，不是成品。**
- `frozen=false`，如实反映「还没被人复查过」。
- 候选里会混入**跨句碎片**（实测有 `reservoir requires careful`、
  `reservoir daily photosynthesis` 这类）。根因是候选排序里语料频次权重
  压过了术语性判断，且 n-gram 抽取不识别句边界。
- 所以要**人工过一遍** `--md` 产出的 `glossary.md`，定稿后再冻结。

### 4.4 换源验收清单

- [ ] ①~⑤ 全部通过，退出码 0
- [ ] 产物出现在 `--source-root` 指定目录下（不是主仓库）
- [ ] 主仓库 `work/extracted/` 篇数未变、无新源文件混入
- [ ] 术语表 `frozen=false`（草稿态）且零槽位为 0
- [ ] 人工复查 `glossary.md`，定稿术语后重新生成并冻结
- [ ] ④ 步若报「术语表被改过」，用 `--accept-glossary-change` 重算槽位

---

## 5. 参数速查

所有脚本都支持**环境变量回退**，命令行参数优先。

### `run_all.py`

| 选项 | 说明 |
|---|---|
| `--with-fetch` / `--no-fetch` | ⑥ 步真实抓取 / 完全跳过 |
| `--accept-glossary-change` | 术语表已改动时接受并重算槽位 |
| `--source-root ROOT` | 换源，产出落到 ROOT 下 |
| `--materials-dir DIR` | 资料根目录 |
| `--course-dirname NAME` | 课程子目录名 |
| `--urls PATH` / `--map PATH` | URL 清单 / 归档映射 |
| `--from-corpus-only` / `--max-terms N` | ③ 步从新语料重建术语表 |
| `--only` / `--skip` / `--from KEY` | 选步骤 |
| `--continue-on-error` / `--quiet` / `--list` | 行为 |

步骤 key：`manifest` `extract` `glossary` `slots` `quality` `fetch`

### `build_manifest.py`

```
--materials-dir DIR      资料根目录（默认自动定位 data/materials）
--course-dirname NAME    课程子目录名（默认 CS146S_offline）
--out PATH               账本输出（默认 work/reports/manifest.json）
--fetch-report PATH      抓取报告（默认与 --out 同目录）
--site-hostname NAME     站点快照目录名（默认 themodernsoftware.dev）
--supplemental-pdfname F 补充 PDF 文件名
```
环境变量：`MF_MATERIALS_DIR` `MF_COURSE_DIRNAME` `MF_OUT` `MF_FETCH_REPORT`

### `extract.py`

```
--materials-dir DIR    课程原始资料根目录
--course-dirname NAME  课程子目录名
--site-hostname NAME   站点快照目录名
--archive-dir DIR      抓取归档目录（默认 data/fetched）
--manifest PATH        上游账本
--out-dir DIR          抽取产出目录（默认 work/extracted）
--report PATH          抽取报告路径
```
环境变量：`MF_MATERIALS_DIR` `MF_COURSE_DIRNAME` `MF_ARCHIVE_DIR` `MF_MANIFEST`
`MF_EXTRACTED_DIR` `MF_EXTRACT_REPORT`

### `init_glossary.py`

```
--extracted-dir DIR   抽取产出目录
--glossary PATH       术语表 JSON 输出
--glossary-md PATH    术语表 Markdown 输出
--from-corpus-only    不带种子，纯从当前语料建表（别名 --no-seed）
--max-terms N         术语条数上限（默认 0 = 只用硬编码定稿术语）
--top N               候选池大小（默认 180）
--md                  同时写 Markdown
--report              只打印，不写文件
```
> ⚠️ `--from-corpus-only` 必须配合 `--max-terms N`，否则会产出空表（脚本会拒绝）。

### `check_slots.py`

```
--verify                    核对命中率（按文档）
--selftest                  校验器反例自测
--accept-glossary-change    接受术语表改动并重算槽位
--extracted-dir DIR         抽取产出目录
--translated-dir DIR        中文译文目录
--glossary PATH             术语表 JSON
--slot-report PATH          槽位报告输出
--verify-report PATH        命中率报告输出
```

### `check_quality.py`

```
check_quality.py all        跑全部自动层（l1+l2+l3）
check_quality.py l1         结构完整性
check_quality.py l2         术语一致性
check_quality.py l3         校验器反例自测
check_quality.py l4-sample  生成语义标注任务（需人工，不在 all 内）
check_quality.py l4-score   汇总人工标注
--src-dir DIR / --dst-dir DIR / --glossary PATH / --out-dir DIR
```

L1 硬门槛：标题行数 · 代码块数量 · 代码块逐字节 · 表格行数（0 容差）· 链接数量（±2%）
· 长度比 ∈ [0.30, 1.50]。正文行数与段首段尾**只作信息项**（汉语行数天然少于英语）。

### `translate_queue.py`

```
status                 进度
next [--count N]       生成 N 个待译任务
save <doc_id> <译文路径>  校验 + 落盘 + 留痕（硬闸门）
selftest               反例自测
--extracted-dir / --translated-dir / --prompts-dir / --glossary / --manifest
```

### `fetch.py`

```
--dry-run              不联网，只登记已归档 + 分类规划
--offline              不联网，待抓项记为 network_error
--retry-failed         只重试上一轮失败条目
--urls PATH            URL 清单（默认 <course>/all_urls.txt）
--map PATH             归档映射（默认 <course>/page_map.json）
--pages DIR            页面目录
--archive-dir DIR      归档落地目录（默认 data/fetched）
--manifest PATH        上游账本
--report PATH          抓取报告
--materials-dir DIR / --course-dirname NAME
```
环境变量：`MF_URLS` `MF_MAP` `MF_PAGES_DIR` `MF_ARCHIVE_DIR` `MF_MANIFEST`
`MF_FETCH_REPORT` `MF_MATERIALS_DIR` `MF_COURSE_DIRNAME`

---

## 6. 翻译循环（人工）

`run_all.py` 跑到 ⑤ 就结束，之后是按文档的翻译循环：

```bash
python scripts/translate_queue.py status            # 看还剩哪些
python scripts/translate_queue.py next --count 3    # 生成 3 个 prompt
#   → prompt 在 output/prompts_to_send/
#   → 交给翻译者（人或 LLM）产出中文 Markdown
python scripts/translate_queue.py save <doc_id> <译文路径>
```

`save` 会做四项校验，不过就拒收。通过后：写入 `output/translated/<doc_id>.md`、
保存 `.PROMPT.md` 留痕（可复现当初的术语约束）、更新 `_progress.json`。

**为什么按文档排队而不是整篇丢给 AI**：一篇最多约 99,000 字符。一次性翻译会让
模型悄悄跳过中间部分，而返回值看起来是完整的（最危险）；一处错了无法定位，也无法逐篇验收。
> 20000 字符的文档允许在**标题边界**折成 2–3 段，每段带文档 ID 和段序号。不按字数硬切。

完成后回到第 ⑤ 步重跑质检：

```bash
python scripts/check_quality.py all
```

---

## 7. 常见问题

### 全部 HTTPS 验证失败 / CA 相关

有些环境默认信任库是空的，必须显式指定 CA bundle：

```bash
# Windows cmd
set MF_CA_BUNDLE=C:\path\to\cacert.pem
# PowerShell
$env:MF_CA_BUNDLE="C:\path\to\cacert.pem"
# Linux/macOS
export MF_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
```

也支持标准变量 `SSL_CERT_FILE` / `REQUESTS_CA_BUNDLE`。
常见来源：certifi 包的 `cacert.pem`、msys2 的 `usr/ssl/certs/ca-bundle.crt`、系统信任库。

> ⚠️ 证书失败**绝不能记成 `network_error`** —— 那是「未核查」，与「确认不存在」是
> 两种不同结论。脚本已按此纪律实现。

### ④ 步报「术语表被改过」

术语表改动会改变 `frozen_hash`，`check_slots.py` 会拒绝沿用旧槽位（否则命中率
可以靠改表来迁就译文，指标失去意义）。确认是有意修改后：

```bash
python scripts/check_slots.py --accept-glossary-change
```

### 只有 `raw.githubusercontent.com` 可达

网络环境受限时的正常现象。`fetch.py` 会逐条登记失败原因与根因，区分
`http_404`（确认不存在）/ `blocked_403`（被拦截，不能判定不存在）/ `network_error`
（未核查）。三类不可得严格区分，重试有效也不会让结论降级。

### 抽取出乱码

PDF 若使用 Type3 矢量字形且缺 `/ToUnicode` 映射，抽出的文本是字母替换式乱码，
**客观不可恢复**。脚本会标 `status=type3_encoding_unrecoverable`、`translatable=false`，
并**不输出乱码**。判据用 `stopword_ratio`（正常英文 0.20–0.30，字母替换式乱码 ≈ 0.00），
不要用 `garbage_score`（会被短伪词骗过）。

---

## 8. 修改代码时的注意事项

这些都是踩过的坑，写在代码注释里，此处汇总。

1. **不要手改 JSON**。术语表改 `CURATED` 后重跑脚本。
2. **路径全局变量要用 `configure()` 重设**。下游函数直接读模块级常量，
   逐个改成传参风险更大。⚠️ 每个被改的名字都要写进 `global` 声明，漏一个就会出现
   「参数看着生效、产出还在老地方」。
3. **函数的默认参数不能绑定路径常量**。Python 默认参数在**定义时**求值一次，
   `configure()` 之后改全局也影响不到它。要用 `path=None` + 函数体内实时读取。
4. **写盘前先建父目录**。真实项目里目录早存在，只有换源到新目录才会暴露。
5. **不要用文件大小当「是否写出内容」的判据**。小规模换源会产出合法但很小的 JSON。
6. **自测必须走生产路径**。校验器的反例自测若用不同的容差参数，会变成假自测
   （曾出现「表格被合并」永远报未检出）。
7. **中英对齐不要靠字符相似度**。中英字符集不同，相似度天然接近 0，无法区分
   「段落错位」与「语言不同」。要用跨语言共享的键（URL / 标识符 / 数字 / 专名）。
8. **`--dry-run` 不能碰网络**，也**不能冒充 `network_error`**。

---

## 9. 术语表口径

- `handling` 四种：`translate`（译）· `keep_en`（保留英文）· `bilingual`（双语）· `acronym`（缩写）
- `source` 两种：`curated`（人工定稿）· `auto_candidate`（自动候选，待定稿）
- `frozen`：只有含人工定稿术语时才为 `true`
- `frozen_hash`：对 `glossary.json` 除 `frozen_hash` 自身外全部字段做 sha256
  （`json.dumps(..., sort_keys=True, ensure_ascii=False)`）
- `proper_names`：多词专名保护，校验时整段屏蔽，避免
  `Model Context Protocol` 里的 `model`/`context` 被当独立术语算成假 miss

**术语表规模**：80–100 条为宜。太短覆盖不住，太长人工复查不完。
默认 `--max-terms 0` 表示只保留人工定稿术语、不自动回填候选 —— 因为自动候选里
槽位最高的全是 `code` / `ai` / `data` 这类通用英文词（`code` 达 912 槽位），
它们不是术语，却会把槽位总数抬高数倍、稀释指标意义。
