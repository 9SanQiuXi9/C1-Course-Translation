#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
translate_queue.py —— 管线 ④ 翻译工作队列管理器

定位
    ⚠️ 本脚本【不调用任何大模型 API】（无密钥/额度）。翻译动作由人完成，
       脚本负责：排队 → 生成精准 prompt → 严格校验 → 落盘 → 留痕 → 进度。

为什么按【文档】为单位排队，而不是整篇丢给 AI
    一篇最多约 99,000 字符。一次性翻译会让 AI 悄悄跳过中间部分，
    而且返回值看起来是完整的（最危险）；一处错了无法定位，也无法逐篇验收。
    所以一篇一次调用，每篇独立验收。
    > 20000 字符的文档允许在【标题边界】折成 2-3 段，但每段带文档 ID 和段序号。
    ⚠️ 不按字数硬切。

术语一致性怎么保证
    ⚠️ 不靠「事后替换」，而靠「每篇 prompt 带上该篇真正用到的术语约束」。
       只列该文档命中的术语（通常十几条），不把 99 条全塞进去 —— 那会干扰模型。

用法
    python scripts/translate_queue.py status
    python scripts/translate_queue.py next                # 生成 1 个任务
    python scripts/translate_queue.py next --count 3      # 生成 3 个任务
    python scripts/translate_queue.py save <doc_id> <译文文件>
    python scripts/translate_queue.py selftest            # 校验器反例自测
"""

import datetime
import hashlib
import json
import os
import re
import sys

# ============================================================ 路径配置
# 换课程时只改这几行
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
# ⚠️ 目录布局改成了 data/ + work/ + output/，所以回退判据不能再只看 materials/：
#    必须认 data/materials 或 data 目录，否则会把 BASE_DIR 误退回 scripts/，
#    导致所有路径都拼到 scripts/ 下面（实测 init_glossary 报「找不到语料 scripts/work/extracted」）。
if not (os.path.isdir(os.path.join(BASE_DIR, "data"))
        or os.path.isdir(os.path.join(BASE_DIR, "materials"))):
    BASE_DIR = SCRIPT_DIR

EXTRACTED_DIRNAME = "extracted"
TRANSLATED_DIRNAME = "translated"
PROMPTS_DIRNAME = "prompts_to_send"

GLOSSARY_NAME = "glossary.json"

EXTRACTED_DIR = os.path.join(BASE_DIR, "work", "extracted")
TRANSLATED_DIR = os.path.join(BASE_DIR, "output", "translated")
PROMPTS_DIR = os.path.join(BASE_DIR, "output", "prompts_to_send")
GLOSSARY_PATH = os.path.join(BASE_DIR, "work", "glossary", "glossary.json")
MANIFEST_PATH = os.path.join(BASE_DIR, "work", "reports", "manifest.json")
PROGRESS_PATH = os.path.join(TRANSLATED_DIR, "_progress.json")


def configure(extracted_dir=None, translated_dir=None, prompts_dir=None,
              glossary=None, manifest=None):
    """
    按命令行参数重设路径全局变量（换源复用）。
    ⚠️ PROGRESS_PATH 派生自 TRANSLATED_DIR，改目录时必须跟着重算，
       否则进度文件会留在旧目录（表现为「译文换了位置但进度没跟上」）。
    """
    global EXTRACTED_DIR, TRANSLATED_DIR, PROMPTS_DIR, GLOSSARY_PATH
    global MANIFEST_PATH, PROGRESS_PATH
    if extracted_dir:
        EXTRACTED_DIR = os.path.abspath(extracted_dir)
    if translated_dir:
        TRANSLATED_DIR = os.path.abspath(translated_dir)
    if prompts_dir:
        PROMPTS_DIR = os.path.abspath(prompts_dir)
    if glossary:
        GLOSSARY_PATH = os.path.abspath(glossary)
    if manifest:
        MANIFEST_PATH = os.path.abspath(manifest)
    PROGRESS_PATH = os.path.join(TRANSLATED_DIR, "_progress.json")


PATH_FLAGS = {
    "--extracted-dir": ("extracted_dir", "抽取产出目录"),
    "--translated-dir": ("translated_dir", "中文译文目录"),
    "--prompts-dir": ("prompts_dir", "待译任务输出目录"),
    "--glossary": ("glossary", "术语表 JSON"),
    "--manifest": ("manifest", "上游账本"),
}


def apply_path_flags(argv):
    """从 argv 里取换源参数并调用 configure()。返回 (剩余参数, 错误码)。"""
    opts = {}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in PATH_FLAGS:
            if i + 1 >= len(argv):
                print(f"❌ {a} 后面要跟一个值")
                return argv, 64
            opts[PATH_FLAGS[a][0]] = argv[i + 1]
            i += 1
        i += 1
    if opts:
        configure(**opts)
    return argv, 0

# 超过这个字符数就在标题边界分段（不按字数硬切）
SPLIT_THRESHOLD = 20000
# 正文短于这个字符数 → 判为【空壳：无可译内容】，不投入翻译
# ⚠️ 阈值取 350：实测这批空壳都在 10~317 字符之间（# Notion / # Figma /
#    付费墙表单 / 反爬占位说明），而真实内容最短的是 622 字符。
#    这是启发式判据，报告里会带 reason 供人工复核。
EMPTY_SHELL_CHARS = 350
# 空壳的判定原因关键词（命中即写明具体成因）
SHELL_REASONS = [
    ("js_rendered", ("# Notion",), "原站为 Notion，内容由 JS 动态渲染，静态抓取只剩标题"),
    ("empty_source", ("# (untitled)",), "源文件为空（0 字节），从未取到内容"),
    ("js_rendered", ("# Figma",), "原站为 Figma 幻灯片，内容由 JS 动态渲染，静态抓取只剩标题"),
    ("paywalled", ("Enter access code",), "原站为 Ghost 私有模式，正文需订阅/访问码，只抓到表单"),
    ("blocked", ("requires a browser to access",), "原站（Medium）反爬拦截，只有占位说明"),
    ("login_page", ("# Log In",), "抓到的是登录页，不是正文"),
    ("spa_shell", ("课程官网",), "官网 SPA 正文在打包 JS 中，抽取未取到正文（extract.py 缺陷）"),
]
# 中文/英文字符比合理区间，超出则警告（可能漏译或过度扩写）
LENGTH_RATIO_MIN = 0.30
LENGTH_RATIO_MAX = 1.50

HANDLING_HINT = {
    "translate": "翻译为「{zh}」",
    "keep_en": "保留英文原形（不翻译）",
    "bilingual": "首次出现译为「{zh}（{en}）」，之后只用「{zh}」",
    "acronym": "保留英文缩写（首次出现给全称）",
}


# ============================================================ 基础工具
def reconfigure_stdout():
    """Windows GBK 控制台：打印中文前必须把 stdout 设成 UTF-8"""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def now_iso():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def strip_front_matter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end >= 0:
            return text[end + 4:]
    return text


def parse_front_matter(text):
    """极简 YAML 头解析（只取本项目用到的标量字段）"""
    meta = {}
    if not text.startswith("---"):
        return meta
    end = text.find("\n---", 3)
    if end < 0:
        return meta
    for line in text[3:end].split("\n"):
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$", line)
        if m:
            v = m.group(2).strip().strip('"')
            meta[m.group(1)] = v
    return meta


CODE_BLOCK_RE = re.compile(
    r"<!--\s*CODE_BLOCK_START\s+id=(\S+)\s+lang=(\S*)\s*-->(.*?)"
    r"<!--\s*CODE_BLOCK_END\s+id=\1\s*-->", re.S)
FENCE_RE = re.compile(r"^(`{3,})[^\n]*\n(.*?)^\1\s*$", re.S | re.M)


def extract_code_blocks(text):
    """
    提取代码块，返回 [(id, lang, 代码内容)]。
    优先取带 CODE_BLOCK_START/END 标记的块；没有标记时退回 ``` 围栏。
    ⚠️ 代码块内容必须逐字节原样保留，所以校验时要拿它做逐字节比对。
    """
    blocks = [(m.group(1), m.group(2), m.group(3)) for m in CODE_BLOCK_RE.finditer(text)]
    if blocks:
        return blocks
    return [("f%d" % i, "", m.group(2))
            for i, m in enumerate(FENCE_RE.finditer(text), 1)]


def strip_code_blocks(text):
    """去掉代码块（含内容），避免代码里的词被当成术语/URL/标题统计"""
    t = CODE_BLOCK_RE.sub(" ", text)
    t = FENCE_RE.sub(" ", t)
    return t


def _normalize_url(u):
    """
    归一化 URL 以便比对。
    ⚠️ 上游抽取器有缺陷：正文里混进了 \\x00 控制字符，把 URL 与其后的词粘成
       一个 token（实测 'https://academy.dair.ai/...\\x00Enroll'）。
       译文不可能复现这种提取噪声，所以比对前要把它清掉，否则会误报。
    ⚠️ 尾部标点也要统一去掉：原文可能是 Markdown 链接文字里带句号
       （如 [https://react.dev/errors/149.](/errors/149)），译文把句号放到
       链接外 —— 两边字面不同但 URL 是同一个。只对原文去标点会误判为"丢失"
       （实测踩到）。这里对两边做同样的归一化。
    """
    u = re.split(r"[\x00-\x1f\s]", u)[0]
    # 半角 + 全角标点都要去：中文译文会把句号写成「。」，不去掉就会误判为丢失
    return u.rstrip(".,;:!?)]}'\"。，、；：！？）】》」』”’…")


def find_urls(text):
    """
    提取正文 URL（先去掉 front matter 与代码块）。
    ⚠️ 必须去掉 front matter：里面 origin_url/source_file 等字段不是正文，
       译文按约定不含 front matter，算进去必然对不上（实测多算 1 个）。
    ⚠️ 必须排除中文标点：中文译文会把 URL 紧接在「。」「，」之后，
       而这些标点不属于 `[^\\s\\)\\]<>"']`，会被吞进 URL，
       导致「原文有、译文缺」的假丢失（实测 Cloudflare 那篇漏报 3 个 URL）。
    """
    body = strip_code_blocks(strip_front_matter(text))
    return [_normalize_url(u)
            for u in re.findall(
                r"https?://[^\s\)\]<>\"'\u3000-\u303f\uff00-\uffef\u2018\u2019\u201c\u201d\u2026]+",
                body)]


def find_headings(text):
    """提取正文标题行（同样排除 front matter 与代码块）"""
    body = strip_code_blocks(strip_front_matter(text))
    return re.findall(r"^#{1,6}\s+\S.*$", body, re.M)


def content_length(text):
    """正文长度（去 front matter / 代码块 / 空白）"""
    return len(re.sub(r"\s", "", strip_code_blocks(strip_front_matter(text))))


def term_pattern(term, case_sensitive=False):
    """
    词边界正则，避免 "agent" 命中 "reagent"。
    ⚠️ 含 CJK 的术语不加英文词边界（中文前后文不是 ASCII 字母，边界行为不一致）。
    """
    flags = 0 if case_sensitive else re.IGNORECASE
    has_cjk = any("\u4e00" <= ch <= "\u9fff" for ch in term)
    if has_cjk:
        return re.compile(re.escape(term), flags)
    return re.compile(r"(?<![A-Za-z])" + re.escape(term) + r"(?![A-Za-z])", flags)


# ============================================================ 术语命中扫描
def terms_in_doc(text, glossary):
    """
    找出该文档【真正用到】的术语。
    ⚠️ 只列命中的，不把整张表塞进 prompt —— 那会干扰模型。
    ⚠️ 跳过代码块内部：代码不译，代码里的 agent 不算术语出现。
    """
    body = strip_code_blocks(text)
    hits = []
    for t in glossary.get("terms", []):
        en = t.get("en", "")
        if not en:
            continue
        n = len(term_pattern(en, bool(t.get("case_sensitive"))).findall(body))
        if n:
            hits.append((n, t))
    hits.sort(key=lambda x: -x[0])
    return hits


# ============================================================ 分段（标题边界）
def _split_oversized(part, threshold):
    """
    兜底：某个标题段本身就超过阈值时，在【空行（段落边界）】再分。
    ⚠️ 仍不按字符硬切：以段落为最小单元；绝不切进代码块；
       也绝不让一段以标题行结尾（标题必须跟着它的内容）。
    """
    lines = part.split("\n")
    segs, cur, cur_len = [], [], 0
    in_code = False
    for ln in lines:
        if "CODE_BLOCK_START" in ln:
            in_code = True
        is_fence = ln.lstrip().startswith("```")
        if is_fence:
            in_code = not in_code
        blank = (not ln.strip())
        # 边界安全：不在代码块内、且当前段不以标题行收尾
        safe = (not in_code) and not (cur and re.match(r"^#{1,6}\s+\S", cur[-1] or ""))
        if cur and cur_len + len(ln) + 1 > threshold and blank and safe:
            segs.append("\n".join(cur))
            cur, cur_len = [], 0
            continue
        cur.append(ln)
        cur_len += len(ln) + 1
    if cur:
        segs.append("\n".join(cur))
    return [s for s in segs if s.strip()]


def split_by_headings(body, threshold=SPLIT_THRESHOLD):
    """
    > threshold 时在【标题边界】分段。
    ⚠️ 不按字数硬切：把「标题 + 其下内容」作为最小单元。
       若某个标题段本身就超阈值（如全篇只有一个大章节），
       再退回【段落边界】分，且绝不切进代码块、不让标题与内容分离。
    返回 [(seg_no, 文本)]；不需要分段时返回 [(1, 全文)]。
    """
    if len(body) <= threshold:
        return [(1, body)]

    parts = re.split(r"(?m)^(?=#{1,2}\s+\S)", body)
    parts = [p for p in parts if p.strip()]
    if not parts:
        parts = [body]

    segs, cur = [], ""
    for p in parts:
        if cur and len(cur) + len(p) > threshold:
            segs.append(cur)
            cur = p
        else:
            cur += p
    if cur:
        segs.append(cur)

    # 兜底：任何仍然超阈值的段，按段落边界再分
    final = []
    for s in segs:
        if len(s) > threshold:
            final.extend(_split_oversized(s, threshold))
        else:
            final.append(s)
    final = [s for s in final if s.strip()] or [body]
    return [(i, s) for i, s in enumerate(final, 1)]


# ============================================================ prompt 生成
def build_prompt(doc_id, meta, body, term_hits, seg_no=1, seg_total=1):
    """生成一份可直接复制的翻译 prompt"""
    L = []
    L.append(f"# 翻译任务：{doc_id}" + (f"（第 {seg_no}/{seg_total} 段）" if seg_total > 1 else ""))
    L.append("")
    L.append("## 一、文档元数据")
    L.append("")
    L.append(f"- doc_id：`{doc_id}`")
    L.append(f"- title：{meta.get('title') or '(无)'}")
    L.append(f"- origin_url：{meta.get('origin_url') or '(无)'}")
    L.append(f"- 本段字符数：{len(body):,}" + (f"（全文分 {seg_total} 段）" if seg_total > 1 else ""))
    L.append("")

    L.append("## 二、术语约束（本文档用到的，必须严格遵守）")
    L.append("")
    if term_hits:
        L.append("| 英文 | 处理方式 | 出现次数 |")
        L.append("|---|---|---|")
        for n, t in term_hits:
            hint = HANDLING_HINT.get(t.get("handling"), "").format(
                zh=t.get("zh", ""), en=t.get("en", ""))
            L.append(f"| `{t['en']}` | {hint} | {n} |")
        L.append("")
        L.append("⚠️ 上表是硬约束，**不得自行更换译法**。")
        L.append("⚠️ 未列出的词按常规翻译；专有名词（MCP、token、vibe coding 等）保留英文。")
    else:
        L.append("（本文档未命中术语表中的术语，按常规翻译即可。）")
    L.append("")

    L.append("## 三、翻译要求")
    L.append("")
    for r in [
        "严格按上表术语译法，不得自行更换",
        "专有名词保留英文（MCP、token、vibe coding 等）",
        "代码块内容**逐字节原样保留**，不翻译、不改变量名、不动缩进",
        "保留所有 Markdown 结构（标题层级、列表、表格、链接）",
        "URL 一个字都不能改",
        "保留 `<!-- CODE_BLOCK_START ... -->` 与 `<!-- CODE_BLOCK_END ... -->` 注释标记",
        "标题行数量与原文一致，不要新增或删除标题",
        "输出纯中文，不要中英对照",
        "⚠️ 只翻译给定内容，不要补充、摘要、扩展、评论",
    ]:
        L.append(f"- {r}")
    L.append("")

    L.append("## 四、待翻译原文")
    L.append("")
    # ⚠️ 用比正文内最长反引号串更长的围栏，否则正文里的 ``` 会提前闭合
    fence = "`" * (max([len(m.group(0)) for m in re.finditer(r"`+", body)] or [3]) + 1)
    fence = fence if len(fence) >= 4 else "````"
    L.append(fence + "markdown")
    L.append(body)
    L.append(fence)
    L.append("")

    L.append("## 五、输出要求")
    L.append("")
    L.append("直接给出译文，用 ``` 包裹便于复制。**不要**输出任何解释、前言或后记。")
    if seg_total > 1:
        L.append(f"⚠️ 这是第 {seg_no}/{seg_total} 段，只翻译本段内容。")
    L.append("")
    return "\n".join(L)


# ============================================================ 落盘校验
def run_checks(doc_id, orig_text, trans_text):
    """
    严格校验。返回 (ok, checks, errors)。
    ⚠️ 校验不通过就拒绝写入 —— 坏译文一旦落盘，后面所有统计都不可信。
    """
    checks = {}
    errors = []

    # a) 非空
    checks["non_empty"] = bool(trans_text.strip())
    if not checks["non_empty"]:
        errors.append("译文为空")

    # b) 代码块逐字节一致
    ob = extract_code_blocks(orig_text)
    tb = extract_code_blocks(trans_text)
    checks["code_blocks_total"] = len(ob)
    checks["code_blocks_in_translation"] = len(tb)
    checks["code_blocks_match"] = (len(ob) == len(tb))
    if not checks["code_blocks_match"]:
        errors.append(f"代码块数量不一致：原文 {len(ob)} 个，译文 {len(tb)} 个")
    else:
        diffs = [ob[i][0] for i in range(len(ob)) if ob[i][2] != tb[i][2]]
        checks["code_blocks_byte_identical"] = not diffs
        if diffs:
            errors.append(f"代码块内容被改动（逐字节比对不一致）：{diffs}")

    # c) URL：以【不得丢失】为硬门槛
    # ⚠️ 为什么不用"数量必须相等"当硬门槛：
    #    上游抽取有缺陷（正文混进 \x00，把 "A url Enroll" 这种伪链接切得与译文
    #    不一致），且同一 URL 可能同时出现在 front matter 与正文里。
    #    数量比对会被这些噪声卡死，让好译文无法落盘。
    #    真正要守的不变量是【原文正文里的每个 URL 都还在译文里】——那才是"漏译/丢链接"。
    ou, tu = find_urls(orig_text), find_urls(trans_text)
    checks["urls_orig"] = len(ou)
    checks["urls_trans"] = len(tu)
    missing = [u for u in ou if u not in set(tu)]
    extra = [u for u in tu if u not in set(ou)]
    checks["urls_all_present"] = (not missing)          # 硬门槛：一个都不能丢
    checks["urls_counts_equal"] = (len(ou) == len(tu))   # 仅记录
    if missing:
        errors.append(f"URL 丢失：原文有 {len(ou)} 个，译文缺 {missing[:3]}")
    if extra:
        checks.setdefault("urls_notes", []).append(
            f"译文多出 URL（未计入失败，需人工确认）：{extra[:3]}")

    # d) 标题行数量
    oh, th = find_headings(orig_text), find_headings(trans_text)
    checks["headings_orig"] = len(oh)
    checks["headings_trans"] = len(th)
    checks["headings_match"] = (len(oh) == len(th))
    if not checks["headings_match"]:
        errors.append(f"标题行数量不一致：原文 {len(oh)}，译文 {len(th)}")

    # e) 长度比（警告级，不阻断）
    ol, tl = content_length(orig_text), content_length(trans_text)
    ratio = (tl / ol) if ol else 0.0
    checks["orig_chars"] = ol
    checks["trans_chars"] = tl
    checks["length_ratio"] = round(ratio, 4)
    if ol and not (LENGTH_RATIO_MIN <= ratio <= LENGTH_RATIO_MAX):
        checks["length_ratio_ok"] = False
        errors.append(f"长度比异常：{ratio:.2f}（合理区间 "
                      f"{LENGTH_RATIO_MIN}~{LENGTH_RATIO_MAX}）"
                      f"，可能漏译或过度扩写")
    else:
        checks["length_ratio_ok"] = True

    # ⚠️ 不能用「所有布尔都为真」来判 ok：checks 里有仅记录用的布尔
    #    （如 urls_counts_equal），把它们当门槛会让好译文永远存不进去。
    #    这里显式列出【硬门槛】。
    HARD_GATES = ("non_empty", "code_blocks_match", "code_blocks_byte_identical",
                  "urls_all_present", "headings_match", "length_ratio_ok")
    ok = all(checks.get(k) is True for k in HARD_GATES)
    return ok, checks, errors


# ============================================================ 进度读写
def load_progress():
    if os.path.isfile(PROGRESS_PATH):
        try:
            with open(PROGRESS_PATH, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"total_docs": 0, "done": 0, "pending": 0, "docs": {}}


def save_progress(progress):
    os.makedirs(TRANSLATED_DIR, exist_ok=True)
    with open(PROGRESS_PATH, "w", encoding="utf-8", newline="\n") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)
        f.write("\n")


def load_manifest_no_content():
    """
    从 manifest 读取【明确判定为不可翻译】的条目。
    ⚠️ 队列必须尊重上游判定：manifest 里 translatable=false 且带失败根因的，
       是抽取环节已经证实不可恢复的（如 Type3 无 ToUnicode 抽出字母替换乱码）。
       只看字符数会漏掉它们 —— 实测 how-openai-uses-codex 有 7,526 字符，
       长度远超空壳阈值，但内容是乱码，靠字符数判不出来。
    返回 {doc_id: reason}
    """
    out = {}
    if not os.path.isfile(MANIFEST_PATH):
        return out
    try:
        with open(MANIFEST_PATH, encoding="utf-8") as f:
            man = json.load(f)
    except Exception:
        return out
    for it in man.get("items") or []:
        if it.get("translatable") is not False:
            continue
        if it.get("status") in ("not_applicable",):
            continue          # 中文原生文档：不是"不可恢复"，是"不需要译"
        did = it.get("id")
        lp = (it.get("local_path") or "")
        if not did or not lp:
            continue
        # 只认能对上 extracted/<id>.md 的条目
        out[did] = (it.get("failure_root_cause")
                    or f"manifest 判定 translatable=false（status={it.get('status')}）")
    return out


def classify_empty_shell(body, doc_id=None, manifest_map=None):
    """
    判断正文是否是【空壳：无可译内容】。
    返回 (is_shell, code, reason)；不是空壳则 (False, None, None)。

    ⚠️ 空壳不该投入翻译：硬译出来就是「# Notion」「# 未命名」这种无意义产出，
       白白消耗人工与额度。但也不能悄悄跳过 —— 必须在报告里标注成因，
       因为「无可译内容」和「还没翻」是两件完全不同的事。
    """
    text = strip_front_matter(body).strip()
    # ① 上游 manifest 已明确判定不可翻译 → 直接跳过并沿用它的根因
    if doc_id and manifest_map and doc_id in manifest_map:
        return True, "unrecoverable_upstream", manifest_map[doc_id]
    # ② 内容过短 → 空壳
    if len(text) > EMPTY_SHELL_CHARS:
        return False, None, None
    for code, keys, reason in SHELL_REASONS:
        if any(k in text for k in keys):
            return True, code, reason
    # 兜底：内容极短但没命中已知特征
    n_lines = len([l for l in text.split("\n") if l.strip()])
    return True, "too_short", (
        f"正文仅 {len(text)} 字符 / {n_lines} 个非空行，"
        f"远低于真实内容（最短的完整文档约 622 字符），判定为无可译内容")


def list_docs():
    """返回 {doc_id: 原文全文}"""
    docs = {}
    if not os.path.isdir(EXTRACTED_DIR):
        return docs
    for fn in sorted(os.listdir(EXTRACTED_DIR)):
        if fn.lower().endswith(".md"):
            with open(os.path.join(EXTRACTED_DIR, fn), "rb") as f:
                docs[os.path.splitext(fn)[0]] = f.read().decode("utf-8", "replace")
    return docs


def refresh_progress(docs, progress):
    """
    按磁盘实际情况刷新 total/done/pending/skipped_no_content。
    ⚠️ 空壳文档单独记为 skipped_no_content，既不算 done（没译）也不算 pending
       （不该译），并且带上 reason —— 「无可译内容」必须能在报告里看到成因。
    """
    progress["total_docs"] = len(docs)
    # ⚠️ 先清理失效条目：目录整理/重抽取后，某些 doc_id 可能已不存在，
    #    留着会让 status 去 docs[d] 取值时报 KeyError（实测踩到）。
    for stale in [d for d in progress["docs"] if d not in docs]:
        if progress["docs"][stale].get("status") == "done":
            continue          # 有译文的保留（可能是改名，便于人工核对）
        del progress["docs"][stale]
    for doc_id, raw in docs.items():
        entry = progress["docs"].get(doc_id, {})
        tpath = os.path.join(TRANSLATED_DIR, doc_id + ".md")
        is_shell, code, reason = classify_empty_shell(raw, doc_id, MANIFEST_NO_CONTENT)
        if os.path.isfile(tpath) and os.path.getsize(tpath) > 0:
            entry["status"] = "done"
            entry.pop("no_content_reason", None)
        elif is_shell:
            entry["status"] = "skipped_no_content"
            entry["no_content_code"] = code
            entry["no_content_reason"] = reason
        else:
            entry.setdefault("status", "pending")
        progress["docs"][doc_id] = entry
    vals = progress["docs"].values()
    progress["done"] = sum(1 for v in vals if v.get("status") == "done")
    progress["skipped_no_content"] = sum(
        1 for v in vals if v.get("status") == "skipped_no_content")
    progress["pending"] = progress["total_docs"] - progress["done"] \
        - progress["skipped_no_content"]
    return progress


def load_glossary():
    if not os.path.isfile(GLOSSARY_PATH):
        return {"terms": [], "frozen": False, "frozen_hash": None}
    with open(GLOSSARY_PATH, encoding="utf-8") as f:
        return json.load(f)


# manifest 里明确判定不可翻译的条目（模块级加载一次，manifest 在同一次运行中不变）
MANIFEST_NO_CONTENT = load_manifest_no_content()


# ============================================================ 命令：status
def cmd_status(argv):
    docs = list_docs()
    progress = refresh_progress(docs, load_progress())
    save_progress(progress)
    gloss = load_glossary()

    print("=" * 78)
    print("translate_queue.py status —— 翻译进度")
    print("=" * 78)
    print(f"  术语表：{len(gloss.get('terms', []))} 条"
          f"  frozen={gloss.get('frozen')}")
    print(f"  文档总数：{progress['total_docs']}   "
          f"已译：{progress['done']}   "
          f"无可译内容：{progress.get('skipped_no_content', 0)}   "
          f"待译：{progress['pending']}")
    pct = (progress['done'] / progress['total_docs'] * 100) if progress['total_docs'] else 0
    print(f"  完成度：{pct:.1f}%（分母为全部文档，含无可译内容的空壳）")

    shells = sorted(d for d, v in progress["docs"].items()
                    if v.get("status") == "skipped_no_content")
    if shells:
        print(f"\n  无可译内容（{len(shells)} 篇，已标注成因，不投入翻译）：")
        for d in shells:
            e = progress["docs"][d]
            print(f"    [{e.get('no_content_code')}] {d}")
            print(f"        {e.get('no_content_reason')}")

    pending = sorted(k for k, v in progress["docs"].items()
                     if v.get("status") == "pending")
    if pending:
        print(f"\n  待译（{len(pending)} 篇，按字符数从少到多，先易后难）：")
        sized = sorted(pending, key=lambda d: len(strip_front_matter(docs[d])))
        for d in sized[:15]:
            n = len(strip_front_matter(docs[d]))
            flag = "需要分段" if n > SPLIT_THRESHOLD else ""
            print(f"    {n:>8,} 字符  {d}  {flag}")
        if len(sized) > 15:
            print(f"    …… 另有 {len(sized) - 15} 篇")
    elif not shells:
        print("\n  ✅ 全部文档已翻译完成")
    else:
        print(f"\n  ✅ 待译队列已清空（剩 {len(shells)} 篇无可译内容，已在上面标注）")
    print("=" * 78)
    return 0


# ============================================================ 命令：next
def cmd_next(argv):
    count = 1
    for i, a in enumerate(argv):
        if a == "--count" and i + 1 < len(argv):
            count = int(argv[i + 1])

    docs = list_docs()
    if not docs:
        print(f"❌ 没有找到原文：{EXTRACTED_DIR}")
        return 1
    progress = refresh_progress(docs, load_progress())
    gloss = load_glossary()
    os.makedirs(PROMPTS_DIR, exist_ok=True)

    pending = [d for d in sorted(docs)
               if progress["docs"].get(d, {}).get("status") == "pending"]
    if not pending:
        print("✅ 没有待译文档了。")
        return 0

    # 先易后难：短文档优先，便于尽早发现流程问题
    pending.sort(key=lambda d: len(strip_front_matter(docs[d])))
    chosen = pending[:count]

    print("=" * 78)
    print(f"translate_queue.py next —— 生成 {len(chosen)} 个翻译任务")
    print("=" * 78)
    for doc_id in chosen:
        raw = docs[doc_id]
        meta = parse_front_matter(raw)
        body = strip_front_matter(raw)
        hits = terms_in_doc(raw, gloss)
        segs = split_by_headings(body)
        total = len(segs)
        for seg_no, seg in segs:
            suffix = f".seg{seg_no}" if total > 1 else ""
            fname = f"{doc_id}{suffix}.prompt.md"
            fpath = os.path.join(PROMPTS_DIR, fname)
            prompt = build_prompt(doc_id, meta, seg, hits, seg_no, total)
            with open(fpath, "w", encoding="utf-8", newline="\n") as f:
                f.write(prompt)
            rel = os.path.relpath(fpath, BASE_DIR).replace(os.sep, "/")
            print(f"  ✅ {doc_id}{suffix}")
            print(f"       术语约束 {len(hits)} 条 / 正文 {len(seg):,} 字符"
                  + (f" / 分段 {seg_no}-{total}" if total > 1 else ""))
            print(f"       → {rel}")
        progress["docs"].setdefault(doc_id, {})["prompt_exported_at"] = now_iso()
    save_progress(progress)

    print("\n  下一步：把上面的 .prompt.md 内容复制到 AI 对话，拿到译文存成文件，然后：")
    print(f"    python scripts/translate_queue.py save <doc_id> <译文文件>")
    print("=" * 78)
    return 0


# ============================================================ 命令：save
def cmd_save(argv):
    args = [a for a in argv if not a.startswith("--")]
    if len(args) < 2:
        print("用法：python scripts/translate_queue.py save <doc_id> <译文文件路径>")
        return 1
    doc_id, trans_path = args[0], args[1]

    docs = list_docs()
    if doc_id not in docs:
        print(f"❌ doc_id 不存在于 extracted/：{doc_id}")
        return 1
    if not os.path.isfile(trans_path):
        print(f"❌ 译文文件不存在：{trans_path}")
        return 1

    with open(trans_path, "rb") as f:
        trans_text = f.read().decode("utf-8", "replace")
    orig_text = docs[doc_id]

    # ⚠️ 译文常被 AI 用 ``` 包裹，落盘前剥掉最外层围栏，否则会污染 Markdown
    stripped = trans_text.strip()
    m = re.match(r"^(`{3,})[a-zA-Z]*\n(.*)\n\1$", stripped, re.S)
    if m:
        trans_text = m.group(2)

    ok, checks, errors = run_checks(doc_id, orig_text, trans_text)

    print("=" * 78)
    print(f"translate_queue.py save —— {doc_id}")
    print("=" * 78)
    print(f"  原文 {checks['orig_chars']:,} 字符 / 译文 {checks['trans_chars']:,} 字符"
          f"  长度比 {checks['length_ratio']}")
    for k in ("code_blocks_match", "code_blocks_byte_identical",
              "urls_all_present", "headings_match", "length_ratio_ok"):
        if k in checks:
            print(f"    {'✅' if checks[k] else '❌'} {k}")
    print(f"    代码块 原文{checks['code_blocks_total']} / 译文{checks['code_blocks_in_translation']}")
    print(f"    URL   原文{checks['urls_orig']} / 译文{checks['urls_trans']}")
    print(f"    标题  原文{checks['headings_orig']} / 译文{checks['headings_trans']}")

    if not ok:
        print("\n  ❌ 校验未通过，拒绝落盘（避免坏译文污染后续统计）：")
        for e in errors:
            print(f"     · {e}")
        # ⚠️ 若该文档【已有有效译文】，绝不能把状态改成 failed：
        #    磁盘上的好译文还在（refresh_progress 下次也会按文件判回 done），
        #    标 failed 会自相矛盾，还会掩盖"好译文仍在"这个事实。
        progress = refresh_progress(docs, load_progress())
        entry = progress["docs"].setdefault(doc_id, {})
        existing = os.path.join(TRANSLATED_DIR, doc_id + ".md")
        if os.path.isfile(existing) and os.path.getsize(existing) > 0:
            print(f"\n  ℹ️ 该文档已有有效译文，未被本次失败覆盖："
                  f"{os.path.relpath(existing, BASE_DIR)}")
        else:
            entry["status"] = "failed"
        entry.setdefault("failures", []).append({
            "at": now_iso(), "errors": errors, "source_file": trans_path,
        })
        save_progress(progress)
        print("=" * 78)
        return 1

    # ---- 落盘（幂等：覆盖而非追加）
    os.makedirs(TRANSLATED_DIR, exist_ok=True)
    out_path = os.path.join(TRANSLATED_DIR, doc_id + ".md")
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(trans_text if trans_text.endswith("\n") else trans_text + "\n")

    hits = terms_in_doc(orig_text, load_glossary())
    prompt_path = os.path.join(PROMPTS_DIR, f"{doc_id}.prompt.md")
    prompt_text = ""
    if os.path.isfile(prompt_path):
        with open(prompt_path, encoding="utf-8") as f:
            prompt_text = f.read()

    # ---- 文档级留痕（证据链的一部分）
    trail = [
        f"# 翻译留痕：{doc_id}",
        "",
        f"- doc_id：`{doc_id}`",
        f"- 时间：{now_iso()}",
        f"- 原文：`extracted/{doc_id}.md`",
        f"- 译文：`translated/{doc_id}.md`",
        f"- 原文 sha256：`{hashlib.sha256(orig_text.encode('utf-8')).hexdigest()}`",
        f"- 译文 sha256：`{hashlib.sha256(trans_text.encode('utf-8')).hexdigest()}`",
        f"- 术语约束条数：{len(hits)}",
        "",
        "## 一、本文档涉及的术语清单",
        "",
        "| 英文 | 译法 | handling | 出现次数 |",
        "|---|---|---|---|",
    ]
    for n, t in hits:
        trail.append(f"| `{t['en']}` | {t.get('zh','')} | `{t.get('handling')}` | {n} |")
    trail += ["", "## 二、落盘校验结果", "", "```json",
              json.dumps(checks, ensure_ascii=False, indent=2), "```", ""]
    if errors:
        trail += ["## 三、校验警告", ""]
        trail += [f"- {e}" for e in errors]
        trail.append("")
    trail += ["## 四、发出的 prompt 全文", "", "```markdown",
              prompt_text or "(未找到 prompt 导出文件)", "```", "",
              "## 五、AI 返回的译文全文", "", "```markdown", trans_text, "```", ""]
    trail_path = os.path.join(TRANSLATED_DIR, f"{doc_id}.PROMPT.md")
    with open(trail_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(trail))

    progress = refresh_progress(docs, load_progress())
    progress["docs"].setdefault(doc_id, {})
    progress["docs"][doc_id].update({
        "status": "done", "saved_at": now_iso(), "checks": checks,
        "trail": os.path.relpath(trail_path, BASE_DIR).replace(os.sep, "/"),
    })
    progress["docs"][doc_id].pop("last_failure", None)
    save_progress(progress)

    print(f"\n  ✅ 校验通过，已落盘：")
    print(f"     译文：{os.path.relpath(out_path, BASE_DIR)}")
    print(f"     留痕：{os.path.relpath(trail_path, BASE_DIR)}")
    print(f"  进度：{progress['done']}/{progress['total_docs']}")
    if errors:
        print(f"\n  ⚠️ 有 {len(errors)} 条警告（不阻断）：")
        for e in errors:
            print(f"     · {e}")
    print("=" * 78)
    return 0


# ============================================================ 反例自测
def cmd_selftest(argv):
    """
    ⚠️ 一个失效的校验器比没有校验更危险。这里用已知样本证明：
       ① 正常译文能通过
       ② 代码块被改动能检出
       ③ URL 丢失能检出
       ④ 标题被删能检出
       ⑤ 空译文能检出
    """
    print("=" * 78)
    print("translate_queue.py selftest —— 校验器反例自测")
    print("=" * 78)
    orig = "\n".join([
        "# Title",
        "",
        "The agent calls MCP tools.",
        "",
        "<!-- CODE_BLOCK_START id=c1 lang=python -->",
        "```python",
        "x = 1",
        "```",
        "<!-- CODE_BLOCK_END id=c1 -->",
        "",
        "## Section",
        "",
        "See https://example.com/docs for details.",
    ])
    good = "\n".join([
        "# 标题",
        "",
        "该智能体调用 MCP 工具。",
        "",
        "<!-- CODE_BLOCK_START id=c1 lang=python -->",
        "```python",
        "x = 1",
        "```",
        "<!-- CODE_BLOCK_END id=c1 -->",
        "",
        "## 小节",
        "",
        "详见 https://example.com/docs 。",
    ])
    failures = []

    ok, chk, err = run_checks("t", orig, good)
    print(f"\n  [1] 正常译文：ok={ok} ratio={chk['length_ratio']} 错误={err}")
    if not ok:
        failures.append(f"正常译文被误判失败：{err}")

    bad_code = good.replace("x = 1", "x = 2")
    ok2, chk2, err2 = run_checks("t", orig, bad_code)
    print(f"  [2] 改坏代码块：ok={ok2} 检出={err2}")
    if ok2 or not any("代码块" in e for e in err2):
        failures.append("代码块被改动没有被检出")

    bad_url = good.replace("https://example.com/docs", "https://example.com/other")
    ok3, chk3, err3 = run_checks("t", orig, bad_url)
    print(f"  [3] 改坏 URL：ok={ok3} 检出={err3}")
    if not any("URL 丢失" in e for e in err3):
        failures.append("URL 被改动/丢失没有被检出")

    bad_head = good.replace("## 小节\n", "")
    ok4, _, err4 = run_checks("t", orig, bad_head)
    print(f"  [4] 删掉标题：ok={ok4} 检出={err4}")
    if not any("标题" in e for e in err4):
        failures.append("标题被删没有被检出")

    ok5, _, err5 = run_checks("t", orig, "   ")
    print(f"  [5] 空译文：ok={ok5} 检出={err5}")
    if ok5 or not any("空" in e for e in err5):
        failures.append("空译文没有被检出")

    bad_short = "# 标题\n\n该智能体调用 MCP 工具。\n"
    ok6, chk6, err6 = run_checks("t", orig, bad_short)
    print(f"  [6] 严重漏译：ratio={chk6['length_ratio']} 检出={err6}")
    if not any("长度比" in e for e in err6):
        failures.append("严重漏译（长度比异常）没有被检出")

    print("\n" + "=" * 78)
    if failures:
        print("❌ 自测失败：")
        for f in failures:
            print(f"   · {f}")
        print("=" * 78)
        return 1
    print("✅ 自测全部通过（能检出代码块改动/URL 改动/标题丢失/空译文/严重漏译）")
    print("=" * 78)
    return 0


# ============================================================ 入口
def main(argv):
    reconfigure_stdout()
    if not argv:
        print(__doc__)
        print("换源参数（可放在子命令之后）：")
        for _f, (_k, _d) in PATH_FLAGS.items():
            print(f"  {_f} PATH   {_d}")
        return 0
    # ---- 换源：先抽出路径参数并重设全局，再处理子命令
    argv, _rc = apply_path_flags(argv)
    if _rc:
        return _rc
    cmd = argv[0]
    rest = argv[1:]
    if cmd == "status":
        return cmd_status(rest)
    if cmd == "next":
        return cmd_next(rest)
    if cmd == "save":
        return cmd_save(rest)
    if cmd == "selftest":
        return cmd_selftest(rest)
    print(f"未知命令：{cmd}\n")
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
