# Prompt 集：可复用的课程资料翻译管线

## 这是什么

把一门英文课程的公开资料批量翻译成中文，产出**可复跑、可复用**的管线。

**每个 Prompt 都自包含**——复制到全新对话里就能用，不需要前置上下文。

## 实际执行的流程（已跳过切块）

```
⓪ 体检    manifest.json                    扫描资料，建立账本
    ↓
① 抓取    archive/ + fetch_report.json     补抓缺口，登记不可得资源
    ↓
② 抽取    extracted/*.md                   三种格式统一成 Markdown
    ↓
③ 术语    glossary.json + slot_report.json  冻结术语表 + 槽位穷举（按文档粒度）
    ↓
④ 翻译    translated/*.md + 文档级留痕      逐文档翻译
    ↓
⑤ 校验    quality_report.json + stats.json  四层校验 + κ 统计
    ↓
⑥ 一键复跑 run_all.py + README
```

**⓪ 出现两次是刻意的**：第一次告诉抓取脚本"该抓什么"，第二次把抓取结果并进账本。
脚本自己检查 `fetch_report.json` 是否存在来决定模式。

**切块已跳过。** 原本用它把长文切成小块，现在改为：
- 翻译按【文档】为单位（长文档在标题边界折段）
- 术语槽位按【文档】统计
- 完整性按【文档 + 标题章节】校验

---

## 文件清单

| Prompt | 环节 | 状态 |
|---|---|---|
| [prompt_manifest.md](prompt_manifest.md) | ⓪ 体检 | ✅ 通用版 |
| [prompt_fetch.md](prompt_fetch.md) | ① 抓取 | ✅ 通用版 |
| [prompt_extract.md](prompt_extract.md) | ② 抽取 | ✅ 通用版 |
| [prompt_fix_extract.md](prompt_fix_extract.md) | ② 抽取 | 🔧 **本次修复**（对已有 extract.py 定点改 bug） |
| [prompt_glossary.md](prompt_glossary.md) | ③ 术语 | ✅ 已改为文档粒度 |
| [prompt_translate.md](prompt_translate.md) | ④ 翻译 | ✅ 已改为逐文档 |
| [prompt_validate.md](prompt_validate.md) | ⑤ 校验 | ✅ 已改为文档粒度 |
| [prompt_runall.md](prompt_runall.md) | ⑥ 一键复跑 | ⚠️ 待同步（仍写有切块） |
| ~~prompt_chunk.md~~ | ~~切块~~ | ⏭️ **已跳过，保留备查** |

---

## 通用版 vs 修复版

| | 通用版（如 `prompt_extract.md`） | 修复版（如 `prompt_fix_extract.md`） |
|---|---|---|
| 用途 | 从零写脚本 | **修已有脚本的 bug** |
| 会变吗 | 稳定，换课程可复用 | 修完就作废 |
| 写法 | 描述要做什么 | 描述哪里错了、怎么改 |

**为什么分开**：如果把"本次修复结论"塞进通用版，那份会越来越长、越来越像流水账。
**通用的保持精简，一次性的单独放。**

---

## 写作原则

| 原则 | 做法 |
|---|---|
| **自带背景** | 开头说明项目目标、目录结构、环境限制 |
| **明确输入输出** | 说清读什么、写到哪 |
| **枚举而非概括** | 给出具体取值，不说"合理分类" |
| **把踩过的坑写进去** | 如"不要用有无图片判断 PDF 类型""搜不到≠不存在" |
| **给出判定顺序** | 用 1/2/3 列规则，避免自由发挥 |
| **保留"不确定"选项** | 允许 `null` / `suspect`，不逼 AI 二选一 |
| **约束写死** | 明确"只用标准库""UTF-8 输出" |
| **要求自检** | 每个脚本都必须打印可核对的数字 |

---

## 三条铁律

1. **能用脚本算的，绝不用形容词** —— "术语统一性有据可查" → "1420/1500 槽位命中"
2. **数字只能有一个来源** —— 写进脚本，README 引用，**禁止手写**
3. **缺口如实登记，绝不填充** —— 抓不到就写清根因，不用占位文件充数

---

## 环境约束（所有 Prompt 已内置）

| 约束 | 原因 |
|---|---|
| 只用 Python 标准库 | 环境装不了第三方库 |
| Windows，控制台 GBK | 打印必须 `sys.stdout.reconfigure(encoding="utf-8")` |
| 只有 `raw.githubusercontent.com` 可达 | `github.com` HTML 和 `api.github.com` 不通 |
| 本机 OpenSSL 信任库为空 | HTTPS 会报 `CERTIFICATE_VERIFY_FAILED`，是证书问题不是网络不通 |
| 无法在脚本里调大模型 API | 翻译环节需人工在对话里操作 |

---

## 交付物对照

| 挑战要求 | 从哪来 |
|---|---|
| `README.md` | ⓪⑥ 的产出 + ⑤ 的 `stats.json` |
| `*AI日志*` | 各环节 Session 导出 + ④ 的文档级 `PROMPT.md` |
| `*AAR*` | 全程失败经验（各 Prompt 的"常见问题"表就是素材） |
| `*拿来说明*` | "AI 出错 → 我质疑 → 修正"的案例（已积累多个） |
