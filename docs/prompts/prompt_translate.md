# 管线 ⑤ 翻译：可复制 Prompt

> **前置条件**：`extracted/*.md`（抽取完成）+ `glossary.json`（术语表已冻结）。**不做切块。**
> **产出**：`translated/*.md`（中文译文）+ `translated/<文档>.PROMPT.md`（文档级留痕）
> **粒度**：按【文档】逐篇翻译，不按块

---

## 主 Prompt

```
【项目背景】

我在把一批英文课程资料翻译成中文，做成别人能复用的资料包。
现在要做翻译。项目流程：抽取 → 术语 → 翻译 → 校验（不做切块）。

【仓库】<仓库根目录>\
【输入】
  extracted/*.md     英文原文，带 YAML front matter
  glossary.json      已冻结的术语表（60+ 条，含四种 handling）
  slot_report.json   术语槽位统计（按文档粒度）
  extract_report.json

【环境】
  - 只用 Python 标准库
  - ⚠️ 我无法在脚本里调用大模型 API（没有密钥和额度）。
    翻译动作由【我本人】在对话里完成。你的任务是写【工作队列管理器】。
  - Windows GBK 控制台，脚本开头必须：
      try: sys.stdout.reconfigure(encoding="utf-8")
      except Exception: pass

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【为什么要逐文档、而不是整篇丢给 AI】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
一篇文档最多约 57,000 字符（约 19,000 英文词）。一次性翻译会：
  - 让 AI 悄悄跳过中间部分，且返回值看起来是完整的（最危险）
  - 一处错了无法定位
  - 无法逐篇验收
所以按【文档】为单位排队，一篇一次调用，每篇独立验收。

⚠️ 如果某篇特别长（>20,000 字符），允许在【标题边界】折成 2-3 段
   分别翻译，但每段必须带文档 ID 和段序号，便于拼回和定位。
   不要按字数硬切。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【你要写的脚本：translate_queue.py】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

■ 功能 1：导出待译任务
  命令：python scripts/translate_queue.py next
  作用：从 extracted/ 找出还没翻译的文档，生成完整翻译 prompt 到
        prompts_to_send/<doc_id>.prompt.md

  生成的 prompt 必须包含：
  a) 元数据：doc_id、title、origin_url、字符数
  b) 【该文档涉及的术语约束】——关键：
     扫描该文档，找出其中出现过的所有术语（对照 glossary.json），
     只列这些，并标明 handling：
       翻译为「XX」 / 保留英文 / 首次出现双语
     ⚠️ 不要把 60 条术语全塞进去，只给该文档真正用到的，避免干扰。
  c) 【翻译要求】：
     - 严格按术语表译法，不得自行更换
     - 专有名词保留英文（MCP、token、vibe coding 等）
     - 代码块内容逐字节原样保留，不翻译、不改变量名
     - 保留所有 Markdown 结构（标题层级、列表、表格、链接）
     - URL 一个字都不能改
     - 保留 CODE_BLOCK_START / CODE_BLOCK_END 注释标记
     - 输出纯中文，不要中英对照
     - ⚠️ 只翻译给定内容，不要补充、摘要、扩展
  d) 原文全文（不截断）
  e) 输出要求：直接给译文，用 ``` 包裹便于复制

  命令变体：
    next --count 3     一次生成 3 个任务
    status             打印进度（已译/待译/总数）

■ 功能 2：接收译文并落盘
  命令：python scripts/translate_queue.py save <doc_id> <译文文件路径>
  作用：校验 → 写入 translated/<doc_id>.md → 存留痕 → 更新 progress

  ⚠️ 落盘校验（不通过就拒绝写入并报错）：
    a) 文件非空
    b) doc_id 在 extracted/ 里存在
    c) 译文里 CODE_BLOCK_START 数量 == 原文（逐字节比对代码块内容）
    d) 译文里 URL 数量 == 原文
    e) 译文里 Markdown 标题行数量 == 原文
    f) 长度比在合理区间（中文/英文通常 0.5~1.5），超出要警告
       （可能漏译或过度扩写）

■ 功能 3：文档级留痕
  translated/<doc_id>.PROMPT.md 记录：
    - doc_id、时间
    - 【发出的 prompt 全文】
    - 【AI 返回的译文全文】
    - 该文档涉及的术语清单
    - 落盘校验各项结果
    - 若校验失败过，记失败原因和修正动作
  ⚠️ 这是交付物的一部分：把"叙述型日志"升级为"文档级证据链"。

■ 功能 4：进度与状态
  translated/_progress.json：
  {
    "total_docs": N, "done": N, "pending": N,
    "docs": {
      "<doc_id>": {"status":"done|pending|failed", "saved_at":"...", "checks":{...}}
    }
  }

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【术语一致性怎么保证】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 术语一致性【不应】靠"事后替换"保证，而应靠"每篇 prompt 带上该篇的术语约束"。

所以功能 1 里那一步「扫描该文档涉及的术语」很关键：
  - 读 glossary.json
  - 对每条术语在该文档里用词边界正则匹配：
      r"(?<![A-Za-z])" + re.escape(term) + r"(?![A-Za-z])"，忽略大小写
  - ⚠️ 跳过代码块内部（CODE_BLOCK_START 到 CODE_BLOCK_END 之间）
  - 只把命中的术语列进 prompt

这样每篇的 prompt 短而精准，不会因塞进 60 条术语而干扰模型。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【输出目录】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  prompts_to_send/<doc_id>.prompt.md     待发送的翻译 prompt
  translated/<doc_id>.md                 中文译文
  translated/<doc_id>.PROMPT.md          文档级留痕
  translated/_progress.json              进度

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【我的实际工作流程（请让脚本配合）】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 我运行 translate_queue.py next，得到一份 prompt
2. 我把它复制到 AI 对话里，拿到译文
3. 我把译文存成临时文件
4. 我运行 translate_queue.py save <doc_id> <临时文件>
5. 脚本校验并落盘，我继续下一篇

所以 next 的输出要【方便复制】，save 的校验要【严格】。

【约束】
  - 只用 Python 标准库
  - 路径写成文件顶部常量
  - 关键步骤写中文注释
  - 幂等：重复 save 同一篇应覆盖而非追加
  - 退出码：成功 0，校验失败非 0

请给出 translate_queue.py 完整代码。
```

---

## 交接模板

```
【此前进展】
已完成：体检 → 抓取 → 抽取 → 术语 → 翻译（未做切块）

【翻译结果】
- 文档总数 N，已译 N，待译 N
- 译文在 translated/ 下，文档级留痕在 translated/*.PROMPT.md

【术语表状态】
- N 条，冻结哈希 xxxxx
- 四种 handling：translate N / keep_en N / bilingual N / acronym N

【下一步】对译文做质量校验（完整性 / 术语槽位 / 反例自测 / 语义抽样）

【环境】只用标准库；Windows GBK，打印需 UTF-8
```

---

## 出问题时怎么问

```
运行 translate_queue.py 出问题了：

【我的操作】
python scripts/translate_queue.py save mcp-introduction translated/tmp.md

【报错信息 / 异常结果】
（整段贴原文）

【我观察到的问题】
（例：校验说代码块内容不一致，但我没动代码）

【我认为可能的原因】
（例：比较前没做换行符归一化）

请定位原因并修复。
```

| 症状 | 大概率原因 |
|---|---|
| 校验误报代码块不一致 | 没做换行符/行尾空白归一化 |
| prompt 里塞了全部 60 条术语 | 没做「该文档涉及术语」筛选 |
| 术语被算进代码块 | 扫描时没跳过 CODE_BLOCK 区间 |
| 中文长度比异常 | 漏译或过度扩写 |
| 长文档被 AI 跳译 | 该篇没按标题折段 |

---

## 验收标准

| 项 | 标准 |
|---|---|
| 已译文档数 | 与总数一致（无遗漏） |
| 代码块一致性 | **100% 逐字节一致** |
| URL 数量 | 与原文完全一致 |
| 标题行数量 | 与原文完全一致 |
| 文档级留痕 | 每篇都有 `.PROMPT.md` |
| 长度比 | 无超出 0.5~1.5 区间的文档（或已说明原因） |
