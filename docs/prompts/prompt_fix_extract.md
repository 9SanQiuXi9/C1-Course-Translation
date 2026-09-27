# extract.py 修复提示词（对照本仓库已有代码）

> 用途：修 `scripts/extract.py` 的几个实测确认的 bug。
> **不是重写，是定点修复。** 请先读现有代码，只改出问题的地方。

---

## 修复 Prompt（复制这里开始）

```
【任务】修复 scripts/extract.py 的几个 bug。请先读懂现有代码，只做定点修改，
不要重写整个文件，不要改动没问题的部分。

【仓库】<仓库根目录>\
【目标文件】scripts/extract.py
【参考实现】scripts/pdf_extract_reference.py（这份能跑对，可对照）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【已确认的 4 个 bug，按你上次排查的结论】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

■ bug 1：对象体取错捕获组
  现象：三份 PDF 全被判成 image_only，内容流数统计全是 0。
  根因：用 r"(\d+)\s+(\d+)\s+obj(.*?)endobj" 时误读了 group(2)。
       group(2) 是世代号（通常是 "0"），group(3) 才是对象体。
  修法：改为从 match.end() 开始找 endobj，取两者之间为对象体。
       或确保读的是 group(3)。
  参考：pdf_extract_reference.py 的 load_objects()

■ bug 2：/Length 不可信，把 Flate 流截断了
  现象：zlib.decompress 抛 "invalid literal/lengths set"。
       实测某对象声明 /Length 102，实际流长 8196 字节。
  修法：
    a) 不要按 /Length 切。定位 "stream\r?\n" 到 "endstream"，取完整块。
    b) 直接 zlib.decompress(blob) —— zlib 在 EOS 处会自己停住、
       忽略尾部多余数据，所以给足余量是安全的。
    c) 失败则 zlib.decompressobj().decompress(blob) 解可解前缀。
    d) 再失败返回 None，不要硬塞。
  参考：pdf_extract_reference.py 的 extract_stream_bytes()

■ bug 3：对象流解压失败时误判成"文件损坏"
  现象：判定 anthropic 的 8 个 ObjStm 中 4 个坏掉、约 176 个对象永久丢失。
  实测：这 8 个流【全部能干净解压，0 个失败】，203 个对象全部可取出。
       之前的失败是 bug 2 造成的（按 /Length 切而截断），不是文件坏。
  修法：先修 bug 2，然后重新统计。预期结果：
         anthropic.pdf → 对象 4,214 个 / 内容流 45 个 / ObjStm 8 个全部成功
       如果仍是 0 页 / 0 流，才继续排查，但不要先下"文件损坏"的结论。
  ⚠️ 搜不到 ≠ 不存在。在压缩数据里搜明文是无效操作。

■ bug 4：先查 BT 再解压，把压缩字节当成了文本流
  现象：内容流以 x\xda… 开头，是【仍被压缩】的字节，却被当成文本。
       压缩数据里恰好含 "BT" 字节，所以误判成"这是内容流"。
  修法：判断顺序必须是【先成功解压，再检查 BT 算子】。
       解压失败的流直接丢弃，不得进入文本抽取。
  参考：pdf_extract_reference.py 的 collect_content_streams()

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【必须新增：乱码率质检指标】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
词数不可靠。实测某份抽出 979 个"英文词"，看着像成功，实际全是乱码。
请实现并在控制台打印：

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
  把它写进 extract_report.json 和每个 .md 的 front matter。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【验收：用已知基准，不要靠输出自我判断】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
修完后请跑一遍，并对照下表：

  ai-assisted-code-review-assessment.pdf
      对象 448 / 内容流 16 / CMap 17
      → 约 7,500 英文词，乱码率 <5%          ✅ 应判为可读

  how-anthropic-uses-claude-code.pdf
      对象 4,214 / 内容流 45 / ObjStm 8 个全部成功
      → 抽出的是乱码，乱码率 >25%            ❌ 应如实判为不可恢复

  how-openai-uses-codex.pdf
      对象 5,625 / 内容流 41 / 17 个 /CharProcs
      → 乱码率 >10%                          ❌ 应如实判为不可恢复

⚠️ 后两份的目标【不是】抽出干净文本，而是【如实判定不可恢复】。
   不要用兜底扫描或字符猜测去凑内容。已发生过一次：兜底扫描产出
   上万个解不开的字符码，全是垃圾。

⚠️ 达不到上表数字 → 说明还有 bug，不是文件坏了。
   顺序反了会把解析 bug 误判成文件损坏，从而丢掉可翻译材料。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【顺带要做的两件事】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 回填 manifest.json 的 items[]：只补这 5 个字段，不要手改其他内容
     chars、english_words、garbage_rate、text_path、status
   把目前错误的 PDF 判定改为：
     assessment  → text（translatable=true）
     anthropic   → type3_encoding_unrecoverable（translatable=false）
     codex       → type3_encoding_unrecoverable（translatable=false）
   ⚠️ 数字必须由脚本产出，不手填。

2. 确认失败的抽取【没有写出占位文件】。
   若有空的或 TODO 的 .md，删掉，只保留报告里的 status=failed 记录。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【约束】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- 只用 Python 标准库，不要引入新依赖
- Windows GBK 控制台：脚本开头保留/加上
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
- 保持幂等：重复运行结果完全相同
- 只改 bug 相关的代码，不要重构无关部分

【完成后请报告】
  1. 改了哪几个函数、每处改了什么（一句话）
  2. 三份 PDF 修复后的实测数字（对象数/内容流数/词数/乱码率）
  3. 与验收基准的对比：达标 / 未达标
  4. manifest.json 回填了哪些条目

请先给出修改方案（改哪几处），我确认后再给出完整代码。
```

---

## 使用说明

**这份提示词和 `prompt_extract.md` 的区别：**

| | `prompt_extract.md` | 本文件 |
|---|---|---|
| 用在什么时候 | 从零写 `extract.py` | **已有 `extract.py`，修 bug** |
| 指令性质 | 描述要做什么 | **描述哪里错了、怎么改** |
| 是否重写 | 是 | **否，定点修改** |

**关键设计：我让它"先给修改方案，确认后再给代码"** —— 避免它又整份重写一遍（那正是你不想看到的）。

---

## 为什么这份必须单独存在

因为**上一轮的排查结论是"当前进度"**，而 `prompt_extract.md` 是"通用做法"。两者的用途不同：

- **通用做法**：换一门课、换一批资料时还要用
- **本次修复**：只针对现在这份 `extract.py` 的 4 个具体 bug

**如果把修复结论塞进 `prompt_extract.md`，那份通用提示词就会越来越长**——这正是你前面说"太长了"的原因。
