# 管线 ② 抽取 —— 主 Prompt（精简版）

> 复制下面代码块里的内容到新对话即可。
> AI 需要的**补充资料**（bug 清单、输出契约）在文末，按需一起贴。

---

## 主 Prompt

```
【任务】写 extract.py：把三种格式的课程资料统一抽成标准化 Markdown。

【仓库】<仓库根目录>\
【运行】在仓库根目录执行 python scripts/extract.py

【输入】
  materials/CS146S_offline/pages/*.html          27 个可用（4 个坏文件跳过）
  materials/CS146S_offline/pdfs/*.pdf            3 个
  materials/CS146S_offline/site/themodernsoftware.dev/
                                                 官网 SPA，正文在 assets/*.js 里
  archive/archive/<域名>/*                       抓取的 24 个文件（注意是两层 archive）
                                                 每个文件旁有同名 .meta.json
  跳过 .js 文件（是脚本，不是正文）

【环境限制】
  - 只用 Python 标准库。不要写 import bs4 / pypdf / fitz / requests。
  - Windows GBK 控制台，脚本开头必须：
      try: sys.stdout.reconfigure(encoding="utf-8")
      except Exception: pass

【架构】
  按扩展名分派到 html / pdf / spa / plain 四个函数。不要硬编码文件名，
  用目录扫描。下游 chunk.py 不应有任何格式解析逻辑。

【HTML 抽取】
  去整块 script/style/noscript/svg/head/nav/footer/aside，再按 class/id 关键词
  去导航/订阅/推荐等。若剥离后正文下降 >40%，把区块加回来并记 warning。
  标题归一化：文章标题 → 唯一一个 "# "，章节 → "## " / "### "。
  代码块 → Markdown 围栏，逐字节原样保留，前后加：
      <!-- CODE_BLOCK_START id=c1 lang=bash --> ... <!-- CODE_BLOCK_END id=c1 -->
  表格 → 管道表格；含 colspan/rowspan 的保留原始 HTML 并记 warning。
  图片 → ![alt](URL)；链接 → [锚文本](URL)，URL 不许改。

【PDF 抽取】⚠️ 已踩过 6 个坑，见附件 A，请务必先读
  目标：
    assessment.pdf            → 应抽出约 7,500 词，乱码率 <5%（可读）
    anthropic / codex 那两份  → 抽出的是乱码，应【如实判定不可恢复】，
                                不要用兜底或猜测去凑内容

【⭐ 质检指标：乱码率（必须实现）】
  词数不可靠。实测某份抽出 979 个"英文词"，看着像成功，实际全是乱码。
  用这个替代：

    def garbage_score(text):
        lines = [l for l in text.split("\n") if len(l.strip()) > 15]
        if not lines: return 1.0
        common = set("the of and to in is are that for with as on be this by it from or".split())
        bad = 0
        for l in lines:
            words = re.findall(r"[A-Za-z]{2,}", l)
            if len(words) < 3: continue
            if sum(1 for w in words if w.lower() in common) == 0 \
               and re.search(r"[bcdfghjklmnpqrstvwxz]{5,}", l.lower()):
                bad += 1
        return bad / max(1, len(lines))

    判定：<10% 可读 / 10-35% 部分可读 / >35% 乱码

【输出】
  按附件 B 的格式契约，产出 extracted/<id>.md + extract_report.json，
  并回填 manifest.json 的 items[]（只补 chars、english_words、garbage_rate、
  text_path、status 五个字段）。
  ⚠️ archive/ 里的文件，origin_url 从同名 .meta.json 读。

【纪律】
  - 抽取失败【不要】写占位文件，只在报告里记 status=failed 和根因
  - 不要为了看起来完整而猜测或补全内容
  - 幂等：重复运行结果完全相同

【控制台自检】打印每个文件的格式/状态/字符数/词数/乱码率，
  PDF 额外打印对象数/内容流数/CMap 数/判定类型，末尾给汇总。

请给出完整的 extract.py。
```

---

## 附件 A：PDF 的 6 个已踩坑（贴给 AI）

```
【PDF 抽取的 6 个坑，全部经实测确认，请勿重犯】

① 对象体取错捕获组
   正则 r"(?<![0-9])(\d+)\s+(\d+)\s+obj"，然后从 match.end() 找 endobj，
   两者之间才是对象体。
   ❌ 读 group(2) 拿到的是世代号 "0"，body 只剩 b"0"，
      于是所有流的统计归零 → 三份 PDF 全被判成 image_only。

② 没解压 /ObjStm 对象流
   必须找 /Type /ObjStm 的流 → 解压 → 按 /N 和 /First 切出被压缩对象。
   ❌ 不做这步，在原始字节里搜 /BaseFont、/ToUnicode、/CharProcs、HiddenHorzOCR
      全部是 0 次 → 误判成"没有字体 → 图片型"。
      **搜不到 ≠ 不存在。这是最危险的推理错误。**

③ /Length 不可信
   实测某对象声明 /Length 102，实际流长 8196 字节。按 /Length 硬切 → 解压失败。
   正确做法：定位 stream\r?\n 到 endstream，取完整块直接交给 zlib.decompress
   （zlib 在 EOS 处会自己停住、忽略尾部多余数据，给足余量是安全的）；
   失败则用 zlib.decompressobj().decompress(blob) 解可解前缀；再失败返回 None。

④ 不能把压缩字节当文本流
   判断"是不是内容流"时必须【先解压成功，再检查 BT 算子】。
   压缩数据以 x\xda (78 9a) 开头，里面可能恰好含 "BT" 字节 —— 那是巧合。

⑤ 多个字体的 CMap 不能全局合并
   必须按当前字体（/Fxx 或 /T3_x 经 Tf 切换）分别查各自的 CMap，
   用一个"最大 CMap"覆盖全部会串码。
   另外 TJ 数组里的数字是字距：< -100 当空格，小负数（-7、-30）是字距微调。
   cmap 为空时【不做 ASCII 猜测】，宁可返回空串。

⑥ 拒绝兜底扫描
   拿不到可靠 /Contents 引用时，不要"扫描所有含 BT 的流"——
   那会把 Type3 字形程序当正文，产出上万个解不开的字符码。
   宁可如实报"抽不出来"。

【PDF 类型判定（不要用图片数量判断）】
  在解压后的对象集合上统计：
    bt_operators        成功解压、含 BT、不含 endchar 的流数
    fonts_with_basefont /Type /Font 且带 /BaseFont 的对象数
    has_hidden_ocr      是否出现 HiddenHorzOCR
    has_type3           是否出现 /CharProcs
  判定顺序：bt==0→image_only；basefont>0→text；hidden_ocr→ocr_text_layer；
           type3→type3_vector；其他→unknown

【已知基准（用于验收你的解析器，不要靠输出判断文件好坏）】
  assessment.pdf   448 对象 / 16 内容流 / 17 CMap → 约 7,500 词，乱码率 <5%
  anthropic.pdf    4,214 对象 / 45 内容流 / 8 个 ObjStm 全部可解压 → 乱码率 >25%
  codex.pdf        5,625 对象 / 41 内容流 / 17 个 /CharProcs → 乱码率 >10%
  仓库里 scripts/pdf_extract_reference.py 是参考实现，可对照。
```

---

## 附件 B：输出格式契约（贴给 AI）

```
【extracted/<id>.md 的格式契约，下游依赖，不能改】

1. 开头是 YAML front matter（--- 包裹），字段：
   source_file, origin_url, title, extract_method(html/pdf/spa/text),
   extract_warnings(数组), src_sha256, chars, english_words, garbage_rate,
   code_blocks, tables, links, heading_levels_seen(html 才有)
   pdf 额外：pdf_type, bt_operators, fonts_total, fonts_with_basefont
2. 全文恰好一个 "# "（H1）= 文章标题
3. 章节标题为 "## " 和 "### "
4. 代码块被 <!-- CODE_BLOCK_START id=cN lang=xxx --> 与 ..._END 包裹
5. URL 保持原样

【extract_report.json】
每文件一条：file, format, status(ok/failed/suspect_low_quality/
  unrecoverable_encoding/skipped), chars, english_words, garbage_rate,
  code_blocks, tables, links, warnings, failure_reason
末尾汇总各类数量与总数。
```

---

## 出问题时怎么问（别只说"报错了"）

```
运行 extract.py 出问题了：

【我的操作】
python scripts/extract.py

【报错信息 / 异常结果】
（整段贴原文）

【我观察到的问题】
（例：三份 PDF 都被判成 image_only，内容流数全是 0）

【我认为可能的原因】
（例：对象体可能取错了捕获组，或 ObjStm 没解压）

请定位原因并修复。修复后对照附件 A 的已知基准验收。
```

| 症状 | 大概率原因 |
|---|---|
| 三份 PDF 全判 image_only | 对象体取错捕获组（坑 ①） |
| 搜不到 `/BaseFont`、`/ToUnicode` | 没解压 ObjStm（坑 ②） |
| Flate 流解压失败 | 按 `/Length` 切截断了（坑 ③） |
| 乱码 | 把压缩字节当文本流（坑 ④） |
| 大量解不开的字符码 | 兜底扫描（坑 ⑥） |
| 词数正常但内容是乱码 | 没实现乱码率（质检指标） |
| 控制台编码报错 | 没设 UTF-8 输出 |
