# 管线 ⓪ 体检：可复制 Prompt

> **使用方式**：在新对话中，把下面「主 Prompt」整段复制给 AI。不需要任何前置上下文。
> **产出**：`build_manifest.py` → `manifest.json`（全项目账本）
> **建议**：每完成一个环节，都用「交接 Prompt 模板」把进展交接到下一个新对话

---

## 主 Prompt（复制这里开始）

```
【项目背景，请先读完再动手】

我在做一个课程资料的翻译项目：把一批英文课程资料（网页文章、PDF、课程官网）
翻译成中文，并做成别人能复用的资料包。

资料已经在本地，目录结构：
  materials/
    CS146S_offline/
      pages/     31 个 html 文章（其中 4 个是坏文件：空文件/付费墙/JS渲染/反爬）
      pdfs/      3 个 PDF
      site/      课程官网快照（SPA，正文在打包 JS 里）
      page_map.json   {原始URL: 本地html文件名} 映射
    Vibe_Coding_Playbook.pdf   一份中文原生文档（不要翻译）

我的环境限制（很重要，请务必遵守）：
  - 只能用 Python 标准库。pip 装不了任何第三方库。
  - 运行环境是 Windows，控制台是 GBK 编码，所以脚本里的打印必须处理 UTF-8，
    否则会报 UnicodeEncodeError。

我在做一条处理管线的第一环：体检（inventory）。
它的作用是建立一份「全项目账本」，回答：我手上到底有多少可翻译的内容？
哪些文件是坏的？坏在哪？

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【你的任务】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
写一个 build_manifest.py，扫描上述资料，产出 manifest.json。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【最核心的一条设计原则：只记「正文字数」，不记「文件大小」】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
文件大小会严重误导。实际数据：
  prompt-engineering-overview.html 有 2,005,200 字节，但正文只有约 57,000 字符——
  文件里 97% 是脚本和样式。
如果按文件大小记账，会高估工作量 6 倍以上。

所以必须实现两个抽取函数做交叉校验：
  extract_text(严格法)：先整块删除 <script> <style> <noscript> <svg> <head>，
                        再删所有标签，再解码 HTML 实体，压缩空白
  extract_text_loose(宽松法)：只删标签，不整块删 script/style
记录两者的字符数，并计算 noise_ratio = (宽松 - 严格) / 宽松

⚠️ 这个交叉校验是必须的：如果某个文件两者差异超过 90%，说明它脚本特别多，
   要在报告里标出来供人工复核。绝不可以在两个数字里默默选一个。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【items：每个文件一条记录】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
每条包含：
  id, source_class, title, origin_url, local_path,
  translatable (true/false/null), chars, english_words,
  chars_loose, english_words_loose, noise_ratio, file_bytes,
  status, failure_root_cause, retrieval_attempts

source_class 分这几类（用英文键名）：
  official_site / reading / lecture / video / github / supplemental

status 取值（不要自己发明新值）：
  ok                    正常可翻译
  empty                 0 字节空文件
  paywalled             付费墙
  js_rendered           内容靠 JS 动态渲染，静态抓取只有空壳
  blocked               被反爬拦截，只剩占位说明
  shell_only            正文极少，疑似空壳
  suspect               正文字数明显低于同类，疑似抽取不完整
  image_only            PDF 无文本层
  ocr_text_layer        PDF 是扫描件但带 OCR 隐藏文本层
  type3_vector          PDF 用 Type3 矢量字形
  font_encoding_broken  PDF 字体编码异常
  not_applicable        不需要翻译（如中文原生文档）
  failed                抽取抛异常

⚠️ failure_root_cause 必须写具体原因，不允许只写「抓不到」「失败」。
   要区分是：网络问题 / 需要登录 / 文件本身不存在 / 格式不支持。

translatable 的取值逻辑：
  true     可以翻译
  false    确认不需要翻译（如中文原生文档）
  null     不确定，需要人工确认 ← 允许并鼓励使用这个值

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【pdf 探测：这里最容易做错，请严格按下面做】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ 错误做法（我踩过这个坑）：
   用「有没有 /Subtype /Image」判断 PDF 是不是图片型。
   结果：有封面图的文档式 PDF 被误判成图片型。

❌ 另一个坑：
   直接在原始字节里用正则搜 /BaseFont、/ToUnicode、字体名。
   现代 PDF 会把对象压缩进 /ObjStm 对象流，
   此时在原始字节里搜任何字体信息都会搜到 0 次，
   于是误判成「没有字体 → 图片型」。
   ⚠️ 搜不到 ≠ 不存在。这是最危险的推理错误。

✅ 正确做法：
  第 1 步：实现 load_objects(raw) 解压对象流
    - 用正则找出所有未压缩对象：r"(\d+)\s+(\d+)\s+obj(.*?)endobj"
    - 找出所有 /Type /ObjStm 对象流：zlib 解压后，按 /N 和 /First 字段
      解析出「对象号 → 在解压数据中的偏移」，切分出每个被压缩对象
    - 合并两种来源，返回 {对象号: 对象体}（未压缩的优先）
  第 2 步：在【解压后的对象集合】上统计这些指标
    bt_operators         内容流里 \bBT\b 的出现次数（文本绘制算子）
    content_streams      含 BT 且不含 endchar 的流数量
    fonts_with_basefont  /Type /Font 且带 /BaseFont 的对象数量
    has_hidden_ocr       是否出现 HiddenHorzOCR（OCR 隐藏文本层标记）
    has_type3            是否出现 /CharProcs（Type3 矢量字形标记）
    embedded_images      /Subtype /Image 数量（仅记录，不参与类型判定）
  第 3 步：按此顺序判定类型
    bt_operators == 0        → image_only
    fonts_with_basefont > 0  → text
    has_hidden_ocr           → ocr_text_layer
    has_type3                → type3_vector
    其他                      → unknown_needs_review
  第 4 步：translatable 赋值
    text / ocr_text_layer / type3_vector → true
    image_only / unknown_needs_review    → null（需人工确认）
    ⚠️ 不要因为一个 PDF 不是干净的 text 就标成不可翻译。
       ocr_text_layer 和 type3_vector 其实是可以抽取文本的，只是质量有损。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【course 官网 SPA：正文在 JS 里】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
site/themodernsoftware.dev/index.html 是 Vite 空壳（body 里只有 <div id="root">）。
官网全部正文在 assets/index-CgRb4FxC.js 里，以 JSX 文本节点形式存在：
  children:"..."
用正则 r'children:"((?:[^"\\]|\\.){12,})"' 提取，统计字符数和英文词数。
在 notes 里说明：
  - 正文在打包 JS 中，index.html 是空壳
  - robots.txt 与 index.html 内容完全相同（SHA-256 一致），是抓取时误复制的假文件

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【known_gaps：不可得资源的分组登记】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
除了本地文件，还要登记「课程要求但拿不到」的资源。每条包含：
  what, count, source_class, status, failure_root_cause, urls, retrieval_attempts

⚠️ 三种「不可得」必须严格区分，绝对不能笼统写「抓不到」：
  http_404               真 404。服务器可达，文件确认不存在。这是有效信息。
  blocked_403            被拦截（如 Cloudflare 人机校验）。不能判定为不存在。
  network_error          网络不可达，拿不到状态码。属于「未核查」。
  needs_account          需要登录账号（如 Google Slides/Drive）
  unreachable_automated  自动抓取手段全部失败（如 YouTube 字幕）

需要登记的这些（这是已知情况，直接写进内置默认值）：
  - Google Slides 讲义 12 个：needs_account
  - Google Drive 文件 3 个：needs_account
  - YouTube 视频字幕 3 个：unreachable_automated
    （已实测：youtube.com 网络不可达；本地无 yt-dlp/youtube-dl/ffmpeg；
      youtubetotranscript.com 和 glasp.co 均返回 HTTP 403 被 Cloudflare 拦截）
    三个视频 URL：
      https://www.youtube.com/watch?v=7xTGNNLPyMI   （Deep Dive into LLMs）
      https://www.youtube.com/watch?v=T9aRN5JkmL8   （AI Prompt Engineering）
      https://www.youtube.com/watch?v=TswQeKftnaw   （Lessons from AI code reviews）
  - 官方作业仓库 week2–week8 共 7 个：http_404
    （github.com/mihail911/modern-software-dev-assignments 的 master 分支
      只公开 week1，且那个 week1 的 README 标注为 "fall 2026"，非本课程学年）
  - How FAANG Vibe Codes（X/Twitter 链接）1 个：not_cached

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【支持两遍运行（重要设计）】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
这个脚本要被运行两次：抓取环节【之前】一次，抓取【之后】再一次。

实现方式：检查同级目录下是否存在 fetch_report.json
  - 不存在（第一遍，pre_fetch）：
      用上面那些内置默认值填 known_gaps
      manifest["manifest_mode"] = "pre_fetch"
      manifest["fetch_status"] = "fetch_report.json 不存在，缺口数据来自内置默认值"
  - 存在（第二遍，post_fetch）：
      读它的 summary 字段存进 manifest["fetch_summary"]
      从它的 items 里，把所有 status 为 fetched_ok 的条目追加进 manifest["items"]，
        标注 status="fetched_pending_extract"，
        note="已抓取，正文字数待 extract.py 产出后回填"，
        translatable=true, chars=null
      用它的 items 按 status 分组，重新生成 known_gaps
      manifest["manifest_mode"] = "post_fetch"

⚠️ 无论哪种模式，脚本都必须能正常跑完。第一遍绝对不能因为没有
   fetch_report.json 而报错退出。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【summary：分阶段口径】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
summary 里必须区分这几类，不要混成一个含糊的覆盖率：
  local_archived      本地原有归档（阅读文章 + PDF + 官网）
  fetched_this_run    本次抓取补充的
  unavailable         不可得（按 status 细分）
  reading_html_total / reading_html_ok / reading_html_failed / reading_html_suspect
  reading_translatable_chars / reading_translatable_words
  status_by_class     每个 source_class 的状态分布
  manifest_mode

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【输出与控制台自检】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
manifest.json 写入脚本同级目录。开头三个元字段：
  "generated_by": "build_manifest.py"
  "manifest_mode": "pre_fetch" 或 "post_fetch"
  "note": "本文件由脚本生成，请勿手改。所有数字必须来自脚本，避免多文档口径漂移。"

控制台必须打印：
  1. 运行模式（pre_fetch / post_fetch）
  2. 阅读材料统计：总数 / 可翻译 / 失败 / 存疑，以及可翻译正文字数与词数
  3. 每个失败文件的明细：文件名 + 正文字数 + status + 失败根因
  4. 每个 PDF 的判定结果：文件名 + 判定类型 + 各项指标值
  5. 交叉校验结果：严格法 vs 宽松法的字符数与词数对比，以及差异百分比
  6. known_gaps 分组清单

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【约束】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- 只用 Python 标准库（re, json, os, zlib, hashlib, html）
- 把输入目录、输出路径写成文件顶部常量，方便换课程时只改这几行
- 关键步骤写中文注释
- 幂等：同一时点重复运行产出完全相同（不写入时间戳）
- 控制台打印用 UTF-8 编码

请直接给出完整的 build_manifest.py 代码。
```

---

## 交接 Prompt 模板（用于开新对话）

**每完成一个环节，用这个模板把进展交接到下一个新对话：**

```
【此前进展】
我已经完成：体检（build_manifest.py → manifest.json）

【关键数字，来自 manifest.json】
- 阅读文章：31 个 html，27 个可翻译，4 个失败
- 可翻译正文字数：517,216 字符 / 76,324 英文词
- PDF：3 个（1 个 text，2 个需确认）
- 官网 SPA：7,086 字符

【4 个失败文件的根因】
- lessons-from-ai-code-reviews：0 字节空文件
- how-warp-uses-warp：Notion 页面，JS 渲染
- good-context-good-code：付费墙
- peeking-under-the-hood-of-claude-code：Medium 反爬

【我现在要做的事】
（描述本环节目标）

【我的环境限制】
- 只能用 Python 标准库，装不了第三方库
- Windows，控制台 GBK，打印需 UTF-8

（然后把本环节的 Prompt 全文贴上来）
```

**为什么需要这个模板**：新对话没有记忆，所以交接时要给足上下文。但**把上一步的数字报清楚就够了**，不需要重述整个项目。

---

## ⚠️ 写作原则（这些提示词为什么能跨对话使用）

| 原则 | 具体做法 |
|---|---|
| **自带背景** | 开头就说明项目目标、目录结构、环境限制 |
| **明确输入输出** | 说清读什么文件、写到哪个路径 |
| **枚举而不是概括** | 列出具体的 status 取值，而不是说"合理分类" |
| **把踩过的坑写进去** | 比如"不要用有无图片判断 PDF 类型""搜不到≠不存在" |
| **给出判定顺序** | 用 1/2/3 列出规则，避免 AI 自由发挥 |
| **保留"不确定"选项** | 允许 `null`/`suspect`，而不是逼 AI 二选一 |
| **约束写死** | 明确"只用标准库""UTF-8 输出" |

---

## 验收标准

| 项 | 标准 |
|---|---|
| 阅读材料 | 31 个中 **27 个 translatable=true，4 个 false** |
| 可翻译正文字数 | 约 **517,000 字符**（±5%） |
| PDF 判定 | 3 个中**至少 1 个 text**；不允许出现 `image_only` 误判 |
| 官网 SPA | 约 **7,000 字符** |
| 交叉校验 | 报告里**同时**给出严格法与宽松法两个数字 |
| known_gaps | 明确区分 `http_404` / `blocked_403` / `network_error` / `needs_account` |
| 两遍运行 | 无 `fetch_report.json` 时能正常跑完，且 `manifest_mode="pre_fetch"` |
| 元字段 | 含 `generated_by` 与「请勿手改」提示 |
