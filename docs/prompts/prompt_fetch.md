# 管线 ① 抓取与归档：可复制 Prompt

> **使用方式**：在新对话中把「主 Prompt」整段复制给 AI。不需要前置上下文。
> **前置条件**：体检已完成（`manifest.json` 已存在）
> **产出**：`fetch.py` → `archive/`（补抓的原始文件）+ `fetch_report.json`（抓取证据链）

---

## 主 Prompt（复制这里开始）

```
【项目背景，请先读完再动手】

我在做一个课程资料的翻译项目：把一批英文课程资料翻译成中文，做成别人能复用的资料包。
现在要做的是管线的第一环：抓取与归档。

⚠️ 重要认知：大部分资料【已经归档在本地】了。这个脚本的任务是
   「补抓缺口」+「把抓取结果登记成证据链」，不是从零爬取。

【已归档的（不用再抓）】
  materials/CS146S_offline/site/     课程官网快照
  materials/CS146S_offline/pages/    31 个 html 阅读文章
  materials/CS146S_offline/pdfs/     3 个 PDF

【需要处理的输入文件】
  materials/CS146S_offline/all_urls.txt
    课程官网抓取时汇总的全部 URL（约 98 条），包含 Google Slides、
    Google Drive、YouTube、GitHub、arXiv 等各类链接
  materials/CS146S_offline/page_map.json
    {原始URL: 本地html文件名} 映射，用于登记哪些已经归档了
  manifest.json
    体检产出的账本。读它的 known_gaps 字段了解已知缺口。
    它的 manifest_mode 字段会告诉你现在是抓取前还是抓取后。

【我的环境限制（实测结果，必须严格遵守）】
  1. 只有 raw.githubusercontent.com 可达。
     github.com 的 HTML 页面和 api.github.com 都【不可达】（抛 fetch failed）。
     ⇒ 不要尝试用 GitHub API 列目录，也不要抓 github.com 网页。
     ⇒ 只能构造 raw 路径直接抓文件。
  2. 网络【不稳定】：同一个 URL 可能出现一次成功、一次超时。
     ⇒ 必须实现重试，并且【抓到即落盘】，不要攒在内存里最后统一写。
  3. 只能用 Python 标准库（urllib, json, os, time, hashlib, ssl, re）。
     装不了第三方库，不要写 import requests。
  4. 运行环境 Windows，控制台 GBK 编码，打印必须用 UTF-8。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【你的任务】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
写一个 fetch.py，完成补抓与登记。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【输出】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. archive/<域名>/<文件名>           补抓到的原始文件，按域名分目录
2. archive/<域名>/<文件名>.meta.json 每个文件的元数据
3. fetch_report.json                 抓取证据链
4. 控制台摘要

每个 .meta.json 含：
  origin_url, fetched_at, http_status, content_type, bytes, sha256, used_branch

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【任务 A：登记已归档资源（不发网络请求）】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
读 page_map.json，把每条「原始URL → 本地文件」映射登记进 fetch_report.json，
status="already_archived"。
再用 all_urls.txt 里的 URL 去比对，凡是被 page_map.json 覆盖的也标记为已归档。
⚠️ 这些不要重复抓取。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【任务 B：按域名分类，逐类处理】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
■ B1. github.com 链接 → 转成 raw 链接再抓
  转换规则（容易出错，请仔细）：
    https://github.com/<owner>/<repo>/blob/<branch>/<path>
      → https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>
    https://github.com/<owner>/<repo>/tree/<branch>/<path>
      这是目录链接，列举不出来，改为尝试这些候选文件：
        <path>/README.md、<path>/assignment.md、<path>/writeup.md
    去掉 URL 里的 ?query 和 #anchor 再转换
  ⚠️ 分支名不确定时：先试 master，再试 main，记录哪个成功（used_branch 字段）
  ⚠️ 对每个候选路径明确记录结果：
      200 → fetched_ok，落盘
      404 → http_404    【真 404】文件确认不存在，这是有效信息
      403 → blocked_403 【被拦截】无法判断是否存在
      网络异常 → network_error 【未核查】无法判断

■ B2. raw.githubusercontent.com 直接链接 → 直接抓

■ B3. arxiv.org → 尝试抓（PDF 较大，超时设长一些，如 45 秒）

■ B4. cdn.openai.com / www-cdn.anthropic.com → 尝试抓 PDF

■ B5. docs.google.com / drive.google.com → 【不抓】，直接记
    status="needs_account"
    failure_root_cause="需 Google 账号登录，无法自动抓取"

■ B6. youtube.com / youtu.be → 【不抓】，直接记
    status="unreachable_automated"
    failure_root_cause="youtube.com 网络不可达；本地无 yt-dlp/youtube-dl/ffmpeg；
      第三方字幕站 youtubetotranscript.com 与 glasp.co 均返回 HTTP 403，
      被 Cloudflare 人机校验拦截。注意：403 属于被拦截，不能判定为内容不存在。"

■ B7. 其他域名 → 尝试抓一次并记录

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【fetch_report.json 的结构】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{
  "generated_by": "fetch.py",
  "environment_notes": [
    "raw.githubusercontent.com 可达；github.com HTML 与 api.github.com 不可达",
    "网络不稳定，同 URL 可能时通时不通，已实现重试"
  ],
  "summary": {
    "total_urls": N, "already_archived": N, "fetched_ok": N,
    "http_404": N, "blocked_403": N, "needs_account": N,
    "unreachable_automated": N, "network_error": N, "not_attempted": N,
    "total_bytes_archived": N
  },
  "items": [
    {
      "origin_url": "...",
      "final_url": "...",           // 实际请求的 URL（github 转换后的）
      "domain": "...",
      "source_class": "github|lecture|video|reading|supplemental",
      "status": "already_archived|fetched_ok|http_404|blocked_403|needs_account|unreachable_automated|network_error|not_attempted",
      "http_status": 200,            // 拿不到状态码时为 null
      "local_path": "archive/...",
      "bytes": N, "sha256": "...", "content_type": "...",
      "used_branch": "master|main|null",
      "attempts": [ {"url":"...", "result":"...", "kind":"..."} ],
      "failure_root_cause": "..."
    }
  ]
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【⚠️ 本环节最重要的要求】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
三种「不可得」必须严格区分，绝对不允许笼统写「抓不到」：

  1. http_404   真 404。服务器可达，文件确认不存在。【这是有效信息。】
  2. blocked_403 被拦截（Cloudflare 等）。【不能判定为不存在。】
  3. network_error 网络不可达，拿不到状态码。【属于「未核查」，不是「不存在」。】

failure_root_cause 必须写清是哪一种。因为下游的 README 会引用这些结论，
口径不清楚会导致整份报告的覆盖率数字不可信。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【技术实现要求】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- 浏览器 User-Agent（否则很多站会拒绝）：
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
- 请求超时 15 秒（arxiv 用 45 秒）
- 同一域名两次请求之间 sleep 1.5 秒（礼貌抓取）
- 重试：每个 URL 最多 3 次，间隔 2 / 5 / 10 秒
- ⚠️ 抓到即落盘，不要先攒在内存
- ⚠️ 绝对不要覆盖 materials/ 下的任何文件，那是已归档的原始资料，只读
- 幂等：重复运行不重复抓取已成功落盘的（检查 archive/ 里已有同名且 sha256 一致则跳过）
- 支持命令行参数 --retry-failed：只重试 fetch_report.json 里
  status 为 network_error 或 not_attempted 的条目

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【控制台自检（必须打印）】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 分类计数：打印 summary 的每一项
2. 落盘核对：archive/ 下实际文件数 == summary.fetched_ok，
   且每个文件都能算出 sha256
3. 零覆盖检查：确认 materials/ 下没有任何文件被修改
4. 重试有效性：打印有多少 URL 是「重试后才成功」的（证明重试机制起了作用）
5. 缺口清单：按 status 分组列出所有非 fetched_ok 的 URL 及其根因

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【约束】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- 只用 Python 标准库
- 输入路径、输出路径写成文件顶部常量，方便换课程时只改这几行
- 关键步骤写中文注释
- 控制台打印用 UTF-8

请直接给出完整的 fetch.py 代码。
```

---

## 交接 Prompt 模板（用于开新对话）

```
【此前进展】
已完成：体检（manifest.json）+ 抓取（fetch_report.json）

【抓取结果，来自 fetch_report.json】
- all_urls.txt 共 98 条：31 条已归档、N 条抓取成功、N 条真 404、
  N 条需 Google 账号、3 条网络不可达
- 抓取成功的文件在 archive/ 下
- 已知限制：github.com HTML 与 api.github.com 不可达，只有 raw.githubusercontent.com 通

【我现在要做的事】
（描述本环节目标）

【我的环境限制】
- 只能用 Python 标准库
- Windows，控制台 GBK，打印需 UTF-8

（然后把本环节的 Prompt 全文贴上来）
```

---

## ⚠️ 关于「要不要抓学生 fork」的判断

实测发现：Fall 2025 的完整作业目录**只存在于一个学生 fork** 里，
官方仓库只公开 `week1`，而且那个 `week1` 的 README 标注为 "fall 2026"。

**技术上可以抓，但有两个问题：**
1. 来源未经证实，未必等同于官方原始内容
2. 课程作业属于课程方内容，打包分发需谨慎

**建议做法**：
- 抓，但在记录的 `note` 里写明「来源为学生 fork，官方仓库仅公开 week1，
  未经证实等同于官方原始内容」
- README 里如实说明来源，**不要宣称成官方材料**

**诚实标注来源，比装作是官方的更能得分。**

---

## 验收标准

| 项 | 标准 |
|---|---|
| 报告覆盖率 | 覆盖 `all_urls.txt` 的全部 URL，无遗漏 |
| 已归档登记 | 与 `page_map.json` 一致 |
| GitHub 抓取 | syllabus 指定的 4 个仓库至少成功 2 个 |
| 三类不可得 | **全部明确区分**，无「抓不到」这种笼统表述 |
| `materials/` | **零改动** |
| 幂等 | 重复运行不重复抓取已成功项 |
| 落盘完整性 | 每个文件都有 `.meta.json` 和 sha256 |

---

## 为什么这个记录本身就是交付物

挑战要求的第一条学习目标是「定位一手来源，批量抓取并归档」。
评分看的是**你知不知道哪些抓不到、为什么**。

| ❌ 无价值的记录 | ✅ 有价值的记录 |
|---|---|
| "抓取了课程资料" | "98 条 URL：31 条已归档、12 条抓取成功、7 条真 404、15 条需 Google 账号、3 条网络不可达" |
| "有几个下载失败了" | "`week2–8/assignment.md` 真 404（官方仅公开 week1）；Slides 12 条需账号；YouTube 实测 6 渠道全败" |

**右边那种记录证明你定位了来源、尝试了、并诚实归因。**
