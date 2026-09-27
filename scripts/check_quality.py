# -*- coding: utf-8 -*-
"""
check_quality.py —— 翻译项目质量校验

用可核对的数字证明译文质量，而不是抽看几段。分四层：

  L1 结构完整性   标题/代码块/表格/链接/正文行数/长度比，逐篇逐项给"达标篇数/已比对篇数"
  L2 术语一致性   按 handling 分支判定，统计槽位命中率；冻结哈希校验；区分漏译与译法不一致
  L3 反例自测     构造 8 个"被破坏的"样本，断言校验器必须报警（复用 L1/L2 的真实判定函数）
  L4 语义质量     分层抽样生成人工标注任务 -> 汇总两份标注 -> Cohen's κ + Wilson 置信区间

设计原则：
  · 只读输入，绝不修改原文/译文/术语表
  · 幂等：固定随机种子，重复运行结果完全相同
  · 所有数字由脚本计算得出，不允许任何手填常量
  · 一个失效的校验器比没有校验更危险 —— 所以 L3 自测必须能真的失败

用法：
  check_quality.py all        跑全部自动层（l1+l2+l3，并汇总 l4 若已标注）
  check_quality.py l1
  check_quality.py l2
  check_quality.py l3
  check_quality.py l4-sample
  check_quality.py l4-score
"""
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import collections
import difflib
import hashlib
import json
import math
import os
import random
import re

# ══════════════════════════════════════════════════════════════════
#  路径常量（换项目时只改这几处）
# ══════════════════════════════════════════════════════════════════
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SRC_DIR = os.path.join(BASE_DIR, "work", "extracted")        # 英文原文目录（*.md）
DST_DIR = os.path.join(BASE_DIR, "output", "translated")     # 中文译文目录（*.md）
GLOSSARY = os.path.join(BASE_DIR, "work", "glossary", "glossary.json")  # 术语表 JSON
OUT_DIR = os.path.join(BASE_DIR, "work", "quality")          # 报告输出目录


def configure(src_dir=None, dst_dir=None, glossary=None, out_dir=None):
    """
    按命令行参数重设路径全局变量（换源复用）。
    ⚠️ 下面这些名字被各层判定函数直接读取，必须在这里一次性重设。
    """
    global SRC_DIR, DST_DIR, GLOSSARY, OUT_DIR
    if src_dir:
        SRC_DIR = os.path.abspath(src_dir)
    if dst_dir:
        DST_DIR = os.path.abspath(dst_dir)
    if glossary:
        GLOSSARY = os.path.abspath(glossary)
    if out_dir:
        OUT_DIR = os.path.abspath(out_dir)


PATH_FLAGS = {
    "--src-dir": ("src_dir", "英文原文目录"),
    "--dst-dir": ("dst_dir", "中文译文目录"),
    "--glossary": ("glossary", "术语表 JSON"),
    "--out-dir": ("out_dir", "报告输出目录"),
}

# 排除的非译文文件（留痕文件、进度文件等）
EXCLUDE_SUFFIXES = (".PROMPT.md",)
EXCLUDE_PREFIXES = ("_",)

# ══════════════════════════════════════════════════════════════════
#  判定阈值与容差（严格/宽松的边界都集中在这里，便于复核）
# ══════════════════════════════════════════════════════════════════
# —— 计数容差：链接等条目在翻译时可能被合理合并/拆分，允许小幅偏差
MAX_REL_DIFF = 0.02          # 相对偏差上限 2%
MIN_ABS_SLACK = 1            # 同时允许的绝对条数容差

# ⚠️ 表格单独用严格容差（0 容差）。
#    理由：表格是结构化内容，行数变化就意味着结构被破坏 ——
#    「合并一行」正是要检出的缺陷。若沿用 ±1 行的通用容差，
#    合并 1 行会被判为达标（L3 反例自测实测抓到了这个漏洞）。
TABLES_MAX_REL_DIFF = 0.0
TABLES_MIN_ABS_SLACK = 0

# —— 长度比：英译中通常 0.4~0.8；低于 0.3 判疑似漏译
RATIO_MIN_OK = 0.30
RATIO_MAX_OK = 1.50

# —— 段首段尾比对：各取首/末段，低于此比例认为该段可能被跳译
HEAD_TAIL_RATIO_MIN = 0.25

# —— L4 抽样
SEED = 20260101              # 固定种子，保证可复现
PARAS_PER_DOC = 5
LAYER_DOCS = 2               # 前 4 层各取 2 篇 -> 8 篇
RISK_LAYER_DOCS = 3          # 层 5 取 3 篇 -> 共 11 篇 × 5 段 = 55 个判定点
                             # （目标区间 10–12 篇 / 50–60 点）
RISK_NAME_MARKER = "archive-"  # 层 5 判据：文件名含此前缀 = 网页抽取、风险较高

Z95 = 1.96                   # 95% 置信区间的 z 值

# —— L2 段落配对窗口
# ⚠️ 为什么不能只用严格索引配对：
#    英文长段落常被汉语拆成更短的段落，段落数不一致（实测 429 vs 419），
#    累积错位会让「原文段 i ↔ 译文段 i」彻底失配 ——
#    实测某篇段 53 的原文讲 orchestration agent，译文段 53 却在讲新闻列表。
#    这会把正常译文判成 47% 命中率（真实约 95%），属于假失败。
#    解法：在 i 附近 ±WINDOW 段内查找该术语的指定译法，
#          并把实际命中的段距记进报告，便于核查配对质量。
PARA_WINDOW = 3


# ══════════════════════════════════════════════════════════════════
#  通用文本工具
# ══════════════════════════════════════════════════════════════════
def strip_bom(text):
    """
    去 BOM。
    ⚠️ 必须做：文件开头的 U+FEFF 会让 `^#` 匹配不到标题，导致 h1 被静默漏计。
       本项目踩过这个坑（prompt-engineering-overview 少算 1 个标题）。
    """
    return text.lstrip("\ufeff")


def norm_newlines(text):
    """归一化换行符。代码块比对前必须做，否则 CRLF/LF 差异会被误报为内容改动。"""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def split_front_matter(text):
    """
    拆出 YAML front matter 与正文，自动判断两种格式：
      A) 以 --- 开头且能找到闭合 ---  -> 返回 (front, body)
      B) 纯 Markdown / 纯文本        -> 返回 ("", text)
    """
    text = norm_newlines(strip_bom(text))
    if not text.startswith("---"):
        return "", text
    # 找第二个 --- 行
    m = re.match(r"^---[ \t]*\n(.*?)\n---[ \t]*(?:\n|$)", text, re.S)
    if not m:
        return "", text
    return m.group(1), text[m.end():]


def strip_code_blocks(text):
    """
    去掉围栏代码块（含其所在的 ``` 行）。
    用于标题/链接/正文行数统计 —— 代码块内容不该计入这些指标。
    """
    return re.sub(r"^[ \t]*```[^\n]*\n.*?^[ \t]*```[ \t]*$", "", text,
                  flags=re.M | re.S)


def find_code_blocks(text):
    """
    提取围栏代码块内容（按 ``` 成对切分）。
    返回列表，每项是块内文本（不含围栏行）。
    """
    blocks = []
    lines = norm_newlines(text).split("\n")
    i = 0
    while i < len(lines):
        if re.match(r"^[ \t]*```", lines[i]):
            fence = lines[i]
            start = i + 1
            j = start
            while j < len(lines):
                if re.match(r"^[ \t]*```[ \t]*$", lines[j]):
                    break
                j += 1
            if j < len(lines):
                blocks.append("\n".join(lines[start:j]))
                i = j + 1
                continue
            else:
                # 围栏未闭合：如实记为一块，便于暴露抽取/翻译问题
                blocks.append("\n".join(lines[start:]))
                break
        i += 1
    return blocks


def norm_code_block(text):
    """
    代码块比对前的归一化：
      ① 统一换行符  ② 去掉每行行尾空白  ③ 去掉首尾空行
    ⚠️ 不去行内缩进 —— 缩进是代码语义的一部分，去掉就失去了"逐字节一致"的意义。
    """
    t = norm_newlines(text)
    t = "\n".join(line.rstrip() for line in t.split("\n"))
    t = t.strip("\n")
    return t


def code_blocks_identical(src_text, dst_text):
    """
    逐块比对代码块。返回 (块数是否相等, 内容是否逐字节一致, 首个不一致块号)。
    """
    sb = find_code_blocks(src_text)
    db = find_code_blocks(dst_text)
    if len(sb) != len(db):
        return False, False, None
    for idx, (a, b) in enumerate(zip(sb, db), 1):
        if norm_code_block(a) != norm_code_block(b):
            return True, False, idx
    return True, True, None


def find_headings(text):
    """提取正文标题行（排除 front matter 与代码块）。"""
    body = strip_code_blocks(split_front_matter(text)[1])
    return re.findall(r"^#{1,6}\s+\S.*$", body, re.M)


def find_urls(text):
    """
    提取正文 URL（排除 front matter 与代码块）。
    ⚠️ 排除字符类必须含中文标点：中文译文会把 URL 紧接在「。」「，」之后，
       不排除就会把标点吞进 URL，造成假丢失。
    """
    body = strip_code_blocks(split_front_matter(text)[1])
    pat = (r"https?://[^\s\)\]<>\"'\u3000-\u303f\uff00-\uffef"
           r"\u2018\u2019\u201c\u201d\u2026]+")
    return re.findall(pat, body)


def find_table_lines(text):
    """表格行：以 | 开头的行（排除 front matter 与代码块）。"""
    body = strip_code_blocks(split_front_matter(text)[1])
    return [ln for ln in body.split("\n") if ln.lstrip().startswith("|")]


def nonempty_lines(text):
    """正文非空行数（排除 front matter 与代码块）。"""
    body = strip_code_blocks(split_front_matter(text)[1])
    return [ln for ln in body.split("\n") if ln.strip()]


def nonspace_len(text):
    """非空白字符数 —— 长度比的分子/分母。"""
    body = strip_code_blocks(split_front_matter(text)[1])
    return len(re.sub(r"\s", "", body))


def is_content_line(line):
    """
    判定一行是否属于"正文"。
    网页抽取出来的原文常残留导航、页脚、链接列表，会污染术语槽位统计。
    规则（按顺序判定）：
      无链接            -> 正文
      纯图片            -> 非正文
      导航项(A?+URL)    -> 非正文
      >=2 个链接        -> 非正文
      短行(<120)且含链接 -> 非正文
      其余              -> 正文
    """
    urls = len(re.findall(r"https?://", line))
    if urls == 0:
        return True
    if re.match(r"^\s*!\[", line):
        return False
    if re.match(r"^\s*[-*]?\s*A?\s*https?://", line):
        return False
    if urls >= 2:
        return False
    if len(line.strip()) < 120:
        return False
    return True


def split_paragraphs(text):
    """
    按空行切段（先剥 front matter 与代码块），并丢掉纯非正文段。
    用于 L2 的段落配对。
    """
    body = strip_code_blocks(split_front_matter(text)[1])
    raw = re.split(r"\n\s*\n", body)
    out = []
    for p in raw:
        lines = [ln for ln in p.split("\n") if is_content_line(ln)]
        if not lines:
            continue
        p2 = "\n".join(lines).strip()
        if p2:
            out.append(p2)
    return out


def count_stats(text):
    """
    统计一行里「正文行数 / 排除行数」，供核对过滤是否生效。
    """
    body = strip_code_blocks(split_front_matter(text)[1])
    lines = [ln for ln in body.split("\n") if ln.strip()]
    kept = [ln for ln in lines if is_content_line(ln)]
    return len(kept), len(lines)


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=False)


def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def read_text(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


# ══════════════════════════════════════════════════════════════════
#  文档配对
# ══════════════════════════════════════════════════════════════════
def is_translation_file(name):
    """排除留痕文件（*.PROMPT.md）与内部文件（_ 开头）。"""
    if not name.lower().endswith(".md"):
        return False
    for suf in EXCLUDE_SUFFIXES:
        if name.endswith(suf):
            return False
    for pre in EXCLUDE_PREFIXES:
        if name.startswith(pre):
            return False
    return True


def pair_docs():
    """
    配对原文与译文。
    返回 dict：
      pairs        : [(doc_id, src_path, dst_path), ...]
      not_translated: [doc_id, ...]  原文有、译文无（不算失败，单独列出）
      extra        : [文件名, ...]   译文有、原文无
      src_docs     : 原文篇数
    """
    src = {}
    if os.path.isdir(SRC_DIR):
        for fn in sorted(os.listdir(SRC_DIR)):
            if fn.lower().endswith(".md"):
                src[os.path.splitext(fn)[0]] = os.path.join(SRC_DIR, fn)

    dst = {}
    if os.path.isdir(DST_DIR):
        for fn in sorted(os.listdir(DST_DIR)):
            if is_translation_file(fn):
                dst[os.path.splitext(fn)[0]] = os.path.join(DST_DIR, fn)

    pairs = [(d, src[d], dst[d]) for d in sorted(src) if d in dst]
    not_translated = [d for d in sorted(src) if d not in dst]
    extra = [d for d in sorted(dst) if d not in src]
    return {"pairs": pairs, "not_translated": not_translated,
            "extra": extra, "src_docs": len(src)}


# ══════════════════════════════════════════════════════════════════
#  L1 结构完整性
# ══════════════════════════════════════════════════════════════════
def within_tolerance(a, b, max_rel=MAX_REL_DIFF, min_slack=MIN_ABS_SLACK):
    """
    计数项容差判定：允许相对偏差 <= max_rel，或绝对差 <= min_slack。
    正反向都容 —— 翻译时把条目合并或拆分都算合理。
    ⚠️ 代码块与表格不适用默认容差：
       · 代码块必须严格相等（块数与内容）
       · 表格用 TABLES_* 的 0 容差，因为行数变化 = 结构被破坏
    """
    if a == b:
        return True
    if abs(a - b) <= min_slack:
        return True
    return abs(a - b) / max(1, a) <= max_rel


def head_tail_ratio(src_body, dst_body, tail=False):
    """
    段首/段尾各比对一次，避免"中间整段跳译"被整体长度比掩盖。
    取正文中第一个（或最后一个）有实质内容的段落，算其长度比。
    """
    sp = split_paragraphs(src_body)
    dp = split_paragraphs(dst_body)
    if not sp or not dp:
        return None
    s = sp[-1] if tail else sp[0]
    d = dp[-1] if tail else dp[0]
    sn = len(re.sub(r"\s", "", s))
    dn = len(re.sub(r"\s", "", d))
    if sn == 0:
        return None
    return round(dn / sn, 4)


def check_l1_doc(doc_id, src_text, dst_text):
    """逐篇比对 7 项。"""
    src_body = split_front_matter(src_text)[1]
    dst_body = split_front_matter(dst_text)[1]

    # a) 标题行数
    sh, dh = find_headings(src_text), find_headings(dst_text)
    title = {"src": len(sh), "dst": len(dh), "ok": len(sh) == len(dh)}

    # b/c) 代码块数量 + 内容逐字节一致
    cnt_ok, bytes_ok, first_bad = code_blocks_identical(src_text, dst_text)
    sb, db = find_code_blocks(src_text), find_code_blocks(dst_text)
    code = {"src": len(sb), "dst": len(db), "ok": cnt_ok,
            "bytes_identical": bytes_ok}
    if first_bad is not None:
        code["first_mismatch_block"] = first_bad

    # d) 表格行数（0 容差：行数变化 = 结构被破坏）
    st, dt = find_table_lines(src_text), find_table_lines(dst_text)
    table = {"src": len(st), "dst": len(dt),
             "ok": within_tolerance(len(st), len(dt),
                                    TABLES_MAX_REL_DIFF, TABLES_MIN_ABS_SLACK)}

    # e) 链接数量（允许小幅偏差：条目可能被合理合并/拆分）
    su, du = find_urls(src_text), find_urls(dst_text)
    links = {"src": len(su), "dst": len(du),
             "ok": within_tolerance(len(su), len(du))}

    # f) 正文非空行数 —— ⚠️ 只作信息，不作硬门槛
    #    理由：汉语段落承载同等信息所需行数本来就比英文少（实测 0.26~1.07）。
    #    硬卡行数会把「译文更紧凑」误判成漏译 —— 实测 6/41 篇被误报。
    #    真正能反映内容量的是长度比（下一项），行数只作为结构参考列出。
    sl, dl = len(nonempty_lines(src_text)), len(nonempty_lines(dst_text))
    line_ratio = round(dl / sl, 4) if sl else 0.0
    lines = {"src": sl, "dst": dl, "ratio": line_ratio, "ok": True,
             "informational": True}

    # g) 长度比
    sn, dn = nonspace_len(src_text), nonspace_len(dst_text)
    ratio = round(dn / sn, 4) if sn else 0.0
    ratio_ok = RATIO_MIN_OK <= ratio <= RATIO_MAX_OK

    # 段首/段尾（你的要求：各比对一次，防中间整段跳译）
    # ⚠️ 只作异常提示，不作硬门槛：段落是按空行对齐的，
    #    中英段落切分习惯不同会让首段/末段错位（实测出现 head=0.09、tail=1.29
    #    这种一极小一极大的组合，是错位而非漏译）。
    ht_head = head_tail_ratio(src_body, dst_body, tail=False)
    ht_tail = head_tail_ratio(src_body, dst_body, tail=True)
    ht_ok = True
    if ht_head is not None and ht_head < HEAD_TAIL_RATIO_MIN:
        ht_ok = False
    if ht_tail is not None and ht_tail < HEAD_TAIL_RATIO_MIN:
        ht_ok = False

    hard_ok = (title["ok"] and code["ok"] and code["bytes_identical"]
               and table["ok"] and links["ok"] and ratio_ok)

    return {
        "doc": doc_id,
        "title_lines": title,
        "code_blocks": code,
        "table_lines": table,
        "links": links,
        "body_lines": lines,
        "length_ratio": ratio,
        "length_ratio_ok": ratio_ok,
        "head_tail": {"head": ht_head, "tail": ht_tail, "ok": ht_ok,
                      "informational": True},
        "status": "ok" if hard_ok else "fail",
    }


def run_l1(verbose=True):
    p = pair_docs()
    per_doc = []
    for doc_id, sp, dp in p["pairs"]:
        per_doc.append(check_l1_doc(doc_id, read_text(sp), read_text(dp)))

    n = len(per_doc)

    def tally(key, pred=None):
        if pred is None:
            ok = sum(1 for r in per_doc if r[key]["ok"])
        else:
            ok = sum(1 for r in per_doc if pred(r))
        return f"{ok}/{n}", [r["doc"] for r in per_doc
                             if not (r[key]["ok"] if pred is None else pred(r))]

    title_s, title_bad = tally("title_lines")
    code_s, code_bad = tally("code_blocks")
    bytes_s, bytes_bad = tally("code_blocks",
                               lambda r: r["code_blocks"]["bytes_identical"])
    table_s, table_bad = tally("table_lines")
    links_s, links_bad = tally("links")
    lines_s, lines_bad = tally("body_lines")
    ratio_s, ratio_bad = tally("length_ratio", lambda r: r["length_ratio_ok"])
    ht_s, ht_bad = tally("head_tail")

    ratios = sorted(r["length_ratio"] for r in per_doc)
    median = ratios[len(ratios) // 2] if ratios else 0.0
    outliers = [{"doc": r["doc"], "length_ratio": r["length_ratio"]}
                for r in per_doc
                if r["length_ratio"] < RATIO_MIN_OK
                or r["length_ratio"] > RATIO_MAX_OK]
    line_ratio_outliers = [{"doc": r["doc"],
                            "body_lines_src": r["body_lines"]["src"],
                            "body_lines_dst": r["body_lines"]["dst"],
                            "body_lines_ratio": r["body_lines"]["ratio"]}
                           for r in per_doc
                           if r["body_lines"]["ratio"] < 0.35]

    report = {
        "layer": "L1 结构完整性",
        "scope": {
            "src_docs": p["src_docs"],
            "translated": n,
            "not_translated": p["not_translated"],
            "extra": p["extra"],
        },
        "thresholds": {
            "max_rel_diff": MAX_REL_DIFF,
            "min_abs_slack": MIN_ABS_SLACK,
            "tables_max_rel_diff": TABLES_MAX_REL_DIFF,
            "tables_min_abs_slack": TABLES_MIN_ABS_SLACK,
            "ratio_ok_range": [RATIO_MIN_OK, RATIO_MAX_OK],
            "head_tail_ratio_min": HEAD_TAIL_RATIO_MIN,
        },
        "per_doc": per_doc,
        "totals": {
            "title_lines_ok": title_s,
            "code_blocks_ok": code_s,
            "code_blocks_bytes_ok": bytes_s,
            "tables_ok": table_s,
            "links_ok": links_s,
            "body_lines_ok": lines_s,
            "length_ratio_ok": ratio_s,
            "head_tail_ok": ht_s,
            "length_ratio_median": median,
            "length_ratio_outliers": outliers,
            "body_lines_ratio_outliers": line_ratio_outliers,
        },
        "failures": {
            "title_lines": title_bad,
            "code_blocks": code_bad,
            "code_blocks_bytes": bytes_bad,
            "tables": table_bad,
            "links": links_bad,
            "length_ratio": ratio_bad,
        },
        "informational": {
            "body_lines_low_ratio": line_ratio_outliers,
            "head_tail_anomalies": ht_bad,
        },
    }
    write_json(os.path.join(OUT_DIR, "l1_report.json"), report)

    if verbose:
        print("=" * 78)
        print("L1 结构完整性")
        print("=" * 78)
        print(f"  范围：原文 {p['src_docs']} 篇 / 已译 {n} 篇 / 未译 {len(p['not_translated'])} 篇")
        if p["not_translated"]:
            print(f"    未译：{', '.join(p['not_translated'])}")
        if p["extra"]:
            print(f"    ⚠️ 多余译文（原文无对应）：{', '.join(p['extra'])}")
        t = report["totals"]
        rows = [
            ("标题行数", t["title_lines_ok"], report["failures"]["title_lines"]),
            ("代码块数量", t["code_blocks_ok"], report["failures"]["code_blocks"]),
            ("代码块逐字节", t["code_blocks_bytes_ok"], report["failures"]["code_blocks_bytes"]),
            ("表格行数", t["tables_ok"], report["failures"]["tables"]),
            ("链接数量", t["links_ok"], report["failures"]["links"]),
            ("长度比在区间", t["length_ratio_ok"], report["failures"]["length_ratio"]),
        ]
        for name, s, bad in rows:
            flag = "" if not bad else f"  ❌ {', '.join(bad)}"
            print(f"    {name:<14} {s}{flag}")
        print(f"    长度比中位数  {t['length_ratio_median']}")
        if outliers:
            print(f"    ⚠️ 长度比离群 {len(outliers)} 篇：")
            for o in outliers[:10]:
                print(f"       {o['doc']}  ratio={o['length_ratio']}")

        # 以下两项为信息项，不作硬门槛
        print("    —— 以下为信息项（不作门槛）——")
        print(f"    正文行数        {t['body_lines_ok']}（汉语行数天然少于英语）")
        blo = report["informational"]["body_lines_low_ratio"]
        if blo:
            print(f"      行数比 <0.35 的 {len(blo)} 篇（可能是段落更紧凑，也可能有压缩）：")
            for o in blo[:8]:
                print(f"        {o['doc']}  {o['body_lines_src']}→{o['body_lines_dst']}  "
                      f"({o['body_lines_ratio']})")
        ann = report["informational"]["head_tail_anomalies"]
        if ann:
            print(f"      段首/段尾异常 {len(ann)} 篇（多为段落错位，非漏译）：")
            for d in ann[:8]:
                print(f"        {d}")
        print(f"  已写出：{os.path.join(OUT_DIR, 'l1_report.json')}")
    return report


# ══════════════════════════════════════════════════════════════════
#  L2 术语一致性
# ══════════════════════════════════════════════════════════════════
def compute_frozen_hash(gloss):
    """
    术语表内容的哈希。
    ⚠️ 必须排除 frozen_hash 字段自身再算，否则循环依赖：
       哈希取决于内容，而内容里又含哈希值。
       算法与 init_glossary.py / check_slots.py 保持一致。
    """
    payload = {k: v for k, v in gloss.items() if k != "frozen_hash"}
    blob = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def verify_frozen(gloss):
    """
    冻结校验：术语表内容哈希必须与 frozen_hash 一致。
    返回 (是否一致, 当前哈希, 记录哈希)。
    理由：术语表可随时改，则"高命中率"无意义。
    """
    cur = compute_frozen_hash(gloss)
    rec = gloss.get("frozen_hash")
    return (cur == rec), cur, rec


def build_proper_name_re(names):
    """
    专名匹配正则：专名 + 其后若干可继续构成专名的词。
    ⚠️ 后面允许小写词：专名常带小写通用后缀，如 "Model Context Protocol servers"。
       只认首字母大写会让 model/context 被算成独立术语，产生假 miss。
    """
    if not names:
        return None
    alts = "|".join(re.escape(n) for n in sorted(set(names), key=len, reverse=True))
    return re.compile(r"(?<![A-Za-z])(?:" + alts + r")"
                      r"(?:\s+[A-Za-z][A-Za-z0-9\-]*){0,3}(?![A-Za-z])")


def mask_proper_names(text, pat):
    """把专名替换成等长空格（保持位置不变，避免影响其他术语的词边界判断）。"""
    if pat is None:
        return text
    return pat.sub(lambda m: " " * len(m.group(0)), text)


def term_regex(en, case_sensitive=False):
    """术语的匹配正则：用非字母边界防止子串误命中（如 agent 命中 agents 之外的词）。"""
    flags = 0 if case_sensitive else re.I
    return re.compile(r"(?<![A-Za-z])" + re.escape(en) + r"(?![A-Za-z])", flags)


def alt_zh_forms(term):
    """
    同一英文词在译文里可能有多种合理中文形式。
    ⚠️ 判据要宽松：只要该处出现指定译法即算命中。
       这里额外接受 note 中以「或」/「／」列出的等价形式，
       以及常见同义写法，避免把合法译文判成漂移。
    """
    forms = [term.get("zh", "")]
    note = term.get("note") or ""
    # 从 note 里抽取「A 或 B」这类等价形式
    for m in re.finditer(r"「([^」]{1,12})」", note):
        forms.append(m.group(1))
    seen, out = set(), []
    for f in forms:
        f = f.strip()
        if f and f not in seen:
            seen.add(f)
            out.append(f)
    return out


def judge_slot(term, dst_para, en_present):
    """
    按 handling 分支判定一个槽位是否命中。
    ⚠️ 四种 handling 的判据必须分开实现，不要混用。

    translate  术语必须译成中文 -> 译文里出现指定中文译法即命中
    keep_en    术语保留英文     -> 译文里该英文词仍在才命中；被译成中文算未命中
    acronym    同 keep_en
    bilingual  首次双语、之后中文 -> 只检查是否用了指定中文译法
    """
    handling = (term.get("handling") or "translate").lower()
    en = term.get("en", "")

    if handling in ("keep_en", "acronym"):
        # 判据：英文原形仍在译文里
        return bool(re.search(r"(?<![A-Za-z])" + re.escape(en) + r"(?![A-Za-z])",
                              dst_para, re.I if not term.get("case_sensitive") else 0))

    # translate / bilingual：中文译法出现即命中
    for form in alt_zh_forms(term):
        if form and form in dst_para:
            return True
    return False


def judge_slot_window(term, d_paras, idx, window=PARA_WINDOW):
    """
    在译文段 idx 附近 ±window 内判定槽位是否命中。
    返回 (是否命中, 命中的段距)。命中失败时段距为 None。

    ⚠️ 用窗口而非严格索引的原因见 PARA_WINDOW 常量处注释。
       段距可用于核查配对质量：若大量命中都在 |offset|>0，说明段落切分差异大。
    """
    n = len(d_paras)
    for off in range(0, window + 1):
        for cand in ({idx} if off == 0 else {idx - off, idx + off}):
            if 0 <= cand < n and judge_slot(term, d_paras[cand], True):
                return True, (cand - idx)
    return False, None


def doc_level_present(term, d_paras):
    """
    该术语是否在译文全文中以指定译法出现过（不看段落位置）。
    用于区分两类未命中：
      · doc_level_present=True  -> 译法在全篇存在，只是不在对应段落附近
                                   => 配对/切分不确定，不是术语漂移
      · doc_level_present=False -> 整篇都没用指定译法
                                   => 确凿的术语漂移（真问题）
    这是本项目最需要的一个区分：段落按空行配对，参考文献区
    逐条不对齐，会把正常译文判成大量假漂移。
    """
    for p in d_paras:
        if judge_slot(term, p, True):
            return True
    return False


def run_l2(verbose=True):
    # ---- 冻结校验
    if not os.path.isfile(GLOSSARY):
        print(f"❌ 没有找到术语表：{GLOSSARY}")
        return None
    gloss = read_json(GLOSSARY)
    frozen_ok, cur_hash, rec_hash = verify_frozen(gloss)
    if not frozen_ok:
        print("=" * 78)
        print("❌ 术语表已改动，请重跑校验")
        print("=" * 78)
        print(f"  记录哈希：{rec_hash}")
        print(f"  当前哈希：{cur_hash}")
        print("  理由：术语表可随时改，则『高命中率』无意义。")
        print("  处理：重跑 init_glossary.py 重建并冻结术语表，再重跑本校验。")
        return {"frozen_ok": False, "recorded_hash": rec_hash,
                "current_hash": cur_hash}

    terms = gloss.get("terms") or []
    proper_pat = build_proper_name_re(
        gloss.get("proper_names") or [])

    p = pair_docs()
    pairs = p["pairs"]

    # ---- 逐文档：段落配对 + 逐术语统计
    per_term = collections.OrderedDict()
    for t in terms:
        per_term[t["en"]] = {
            "en": t["en"], "zh": t.get("zh", ""),
            "handling": t.get("handling", "translate"),
            "slots": 0, "hits": 0, "misses": [],
        }
    per_doc = []
    by_handling = collections.OrderedDict()
    suspected_omissions = []
    alignment_misses = []      # 译法在全篇存在 -> 配对不确定
    solid_misses = []          # 全篇未用指定译法 -> 确凿漂移
    excluded_total = 0
    lines_total = 0

    for doc_id, sp, dp in pairs:
        src_text, dst_text = read_text(sp), read_text(dp)
        sn, dn = nonspace_len(src_text), nonspace_len(dst_text)
        ratio = round(dn / sn, 4) if sn else 0.0

        # 该文档长度比 < 0.3 -> 疑似漏译，其未命中不计入命中率
        # 理由：整段漏译会让该文档所有槽位失效，混进命中率会让数字失去意义。
        suspected = ratio < RATIO_MIN_OK
        if suspected:
            suspected_omissions.append({"doc": doc_id, "length_ratio": ratio})

        # 过滤非正文行（供核对过滤是否生效）
        kept, tot = count_stats(src_text)
        excluded_total += (tot - kept)
        lines_total += tot

        s_paras = split_paragraphs(src_text)
        d_paras = split_paragraphs(dst_text)
        n_pair = min(len(s_paras), len(d_paras))
        para_warn = None
        if len(s_paras) != len(d_paras):
            para_warn = {"src_paras": len(s_paras), "dst_paras": len(d_paras),
                         "paired": n_pair}

        doc_slots = doc_hits = 0
        offset_hist = collections.Counter()
        for idx in range(n_pair):
            s_line = mask_proper_names(s_paras[idx], proper_pat)
            for t in terms:
                en = t["en"]
                cs = bool(t.get("case_sensitive"))
                n_occ = len(term_regex(en, cs).findall(s_line))
                if not n_occ:
                    continue
                handling = t.get("handling", "translate")
                # 源段落里的出现次数 = 槽位数；命中按处计
                hit, off = judge_slot_window(t, d_paras, idx)
                doc_slots += n_occ
                per_term[en]["slots"] += n_occ
                if hit:
                    doc_hits += n_occ
                    per_term[en]["hits"] += n_occ
                    offset_hist[off] += 1
                elif not suspected:
                    # 只有非疑似漏译才记未命中
                    # 并区分：译法在全篇存在（配对不确定）vs 全篇都没有（确凿漂移）
                    present = doc_level_present(t, d_paras)
                    per_term[en]["misses"].append({
                        "doc": doc_id,
                        "para": idx + 1,
                        "kind": ("配对偏移（译法在全篇存在）" if present
                                 else "确凿漂移（全篇未用指定译法）"),
                        "doc_level_present": present,
                        "src_snippet": s_paras[idx][:160],
                        "dst_snippet": (d_paras[idx][:160] if idx < len(d_paras) else ""),
                    })
                    if present:
                        alignment_misses.append(1)
                    else:
                        solid_misses.append(1)
                # 疑似漏译文档整体踢出命中率统计（含分组统计）
                if not suspected:
                    bh = by_handling.setdefault(handling, {"slots": 0, "hits": 0})
                    bh["slots"] += n_occ
                    if hit:
                        bh["hits"] += n_occ
        per_doc.append({"doc": doc_id, "slots": doc_slots, "hits": doc_hits,
                        "length_ratio": ratio,
                        "suspected_omission": suspected,
                        "paragraph_warning": para_warn,
                        "match_offsets": dict(offset_hist)})

    # ---- 汇总（疑似漏译文档的槽位整体踢出）
    omit_docs = {o["doc"] for o in suspected_omissions}
    per_doc_kept = [d for d in per_doc if d["doc"] not in omit_docs]
    slots_total = sum(d["slots"] for d in per_doc_kept)
    hits_total = sum(d["hits"] for d in per_doc_kept)
    rate = round(hits_total / slots_total, 4) if slots_total else 0.0

    # 每个术语的保持口径（供报告用）
    for en, rec in per_term.items():
        rec["slots_kept"] = rec["slots"]
        rec["hits_kept"] = rec["hits"]
    for h, v in by_handling.items():
        v["hit_rate"] = round(v["hits"] / v["slots"], 4) if v["slots"] else 0.0

    # 前 20 条漂移明细（确凿漂移优先展示）
    drift = [{"en": en, "zh": rec["zh"], "handling": rec["handling"], **m}
             for en, rec in per_term.items() for m in rec["misses"]]
    drift.sort(key=lambda x: (x.get("doc_level_present", True),
                              x["doc"], x["para"]))
    drift = drift[:20]

    n_align, n_solid = len(alignment_misses), len(solid_misses)
    n_miss = n_align + n_solid
    report = {
        "layer": "L2 术语一致性",
        "glossary_hash": cur_hash,
        "frozen_ok": True,
        "docs_compared": len(per_doc_kept),
        "docs_compared_raw": len(per_doc),
        "para_window": PARA_WINDOW,
        "content_filter": {"excluded_lines": excluded_total,
                           "total_lines": lines_total},
        "slots_total": slots_total,
        "slots_hit": hits_total,
        "hit_rate": rate,
        # ⚠️ 未命中分两类，这是本层最关键的区分：
        #    段落按空行配对，参考文献区逐条不对齐，会把正常译文判成假漂移。
        #    · alignment_misses  译法在全篇存在 -> 只说明段落没对上，不是术语漂移
        #    · solid_misses      全篇未用指定译法 -> 确凿的术语不一致（真问题）
        "miss_taxonomy": {
            "total_misses": n_miss,
            "alignment_misses": n_align,
            "solid_misses": n_solid,
            "solid_miss_rate": round(n_solid / slots_total, 4) if slots_total else 0.0,
        },
        "by_handling": by_handling,
        "suspected_omissions": suspected_omissions,
        "per_term": [
            {"en": r["en"], "zh": r["zh"], "handling": r["handling"],
             "slots": r.get("slots_kept", r["slots"]),
             "hits": r.get("hits_kept", r["hits"]),
             "hit_rate": round(r.get("hits_kept", r["hits"]) /
                               max(1, r.get("slots_kept", r["slots"])), 4),
             "solid_misses": sum(1 for m in r["misses"]
                                 if not m.get("doc_level_present", True)),
             "misses": r["misses"][:5]}
            for r in per_term.values()
        ],
        "per_doc": per_doc,
        "drift_top20": drift,
    }
    write_json(os.path.join(OUT_DIR, "l2_report.json"), report)

    if verbose:
        print("=" * 78)
        print("L2 术语一致性")
        print("=" * 78)
        print(f"  术语表哈希：{cur_hash[:16]}…（冻结校验通过）")
        cf = report["content_filter"]
        print(f"  非正文行过滤：排除 {cf['excluded_lines']} 行 / 总计 {cf['total_lines']} 行"
              f"（{cf['excluded_lines']/max(1,cf['total_lines']):.1%}）")
        print(f"  已比对文档：{report['docs_compared']} 篇"
              f"（段落配对窗口 ±{PARA_WINDOW}）")
        print(f"  槽位总计：{slots_total}   命中：{hits_total}   命中率：{rate:.2%}")
        mt = report["miss_taxonomy"]
        print(f"  未命中 {mt['total_misses']} 处，分两类：")
        print(f"    · 配对偏移（译法在全篇存在，非术语问题）  {mt['alignment_misses']}")
        print(f"    · 确凿漂移（全篇未用指定译法，真问题）    {mt['solid_misses']}"
              f"   占槽位 {mt['solid_miss_rate']:.2%}")
        if by_handling:
            print("  按 handling 分组：")
            for h, v in by_handling.items():
                print(f"    {h:<10} {v['hits']:>5}/{v['slots']:<5}  {v['hit_rate']:.2%}")
        if suspected_omissions:
            print(f"  ⚠️ 疑似漏译（长度比 < {RATIO_MIN_OK}，其未命中不计入命中率）：")
            for o in suspected_omissions:
                print(f"    {o['doc']}  ratio={o['length_ratio']}")
        if drift:
            print(f"  术语漂移明细（前 {len(drift)} 条，确凿漂移优先）：")
            for m in drift:
                mark = "配对偏移" if m.get("doc_level_present", True) else "确凿漂移"
                print(f"    [{mark}][{m['handling']}] {m['en']} → 应为「{m['zh']}」  "
                      f"{m['doc']} 段{m['para']}")
        print(f"  已写出：{os.path.join(OUT_DIR, 'l2_report.json')}")
    return report


# ══════════════════════════════════════════════════════════════════
#  L3 反例自测
# ══════════════════════════════════════════════════════════════════
# ⚠️ 自测必须复用 L1/L2 的真实判定函数。
#    若为自测另写一套简化逻辑，自测通过不代表主流程通过 ——
#    这正是"失效的校验器"的典型来源。

GOOD_SRC = """---
title: test
---

# Hello World

This is a paragraph about the agent design.

```python
def add(a, b):
    return a + b
```

| col1 | col2 |
| --- | --- |
| a | b |

See https://example.com/doc for details.
"""

GOOD_DST = """# 你好，世界

这是一个关于智能体设计的段落。

```python
def add(a, b):
    return a + b
```

| col1 | col2 |
| --- | --- |
| a | b |

详见 https://example.com/doc 。
"""

BAD_GLOSS = {
    "frozen_hash": None,
    "terms": [
        {"en": "agent", "zh": "智能体", "handling": "translate",
         "case_sensitive": False, "note": ""},
    ],
    "proper_names": [],
}


def _l1_fails(src, dst):
    """
    跑【L1 的生产判定函数】，返回该样本是否被判为 fail。
    ⚠️ 自测必须走这条路径，不能在自测里另写一套简化逻辑 ——
       否则自测通过与主流程无关，等于假自测。
       本项目踩过：表格容差改了 L1 生产路径，但自测调的是
       within_tolerance 的默认容差，两边不是同一个判据，
       结果"表格被合并"始终报未检出。
    """
    r = check_l1_doc("__selftest__", src, dst)
    return r["status"] == "fail"


def _detect_code_translated():
    """① 代码块被翻译 —— 块数相同但内容被改。"""
    bad = GOOD_DST.replace("def add(a, b):", "def 相加(a, b):")
    return _l1_fails(GOOD_SRC, bad)


def _detect_code_deleted():
    """② 代码块被删除 —— 块数变少。"""
    bad = GOOD_DST.replace("""```python
def add(a, b):
    return a + b
```

""", "")
    return _l1_fails(GOOD_SRC, bad)


def _detect_url_rewritten():
    """③ URL 被改写（数量不变，但内容不同）。"""
    bad = GOOD_DST.replace("https://example.com/doc", "https://example.com/OTHER")
    su, du = find_urls(GOOD_SRC), find_urls(bad)
    # 数量容差允许，但 URL 集合必须一致 —— 这是 L1 links 之外的独立判据
    return not (within_tolerance(len(su), len(du)) and set(su) == set(du))


def _detect_heading_deleted():
    """④ 标题行被删 —— 走 L1 生产路径。"""
    bad = GOOD_DST.replace("# 你好，世界\n\n", "")
    return _l1_fails(GOOD_SRC, bad)


def _detect_term_drift():
    """⑤ 术语用了错误译法（agent 应译「智能体」，却译成「代理」）—— 走 L2 生产判定。"""
    t = BAD_GLOSS["terms"][0]
    bad_para = "这是一个关于代理设计的段落。"
    good_para = "这是一个关于智能体设计的段落。"
    return (not judge_slot(t, bad_para, True)) and judge_slot(t, good_para, True)


def _detect_omission():
    """⑥ 整段漏译 —— 长度比 < 0.3，走 L1 生产路径。"""
    long_src = "# Title\n\n" + ("This is a sentence about something. " * 40)
    short_dst = "# 标题\n\n短。"
    return _l1_fails(long_src, short_dst)


def _detect_table_merged():
    """⑦ 表格行被合并 —— 走 L1 生产路径（表格用 0 容差）。"""
    bad = GOOD_DST.replace("| a | b |\n", "")
    return _l1_fails(GOOD_SRC, bad)


def _detect_empty_translation():
    """⑧ 译文为空 —— 走 L1 生产路径。"""
    return _l1_fails(GOOD_SRC, "")


L3_CASES = [
    ("代码块被翻译", _detect_code_translated),
    ("代码块被删除", _detect_code_deleted),
    ("URL 被改写", _detect_url_rewritten),
    ("标题行被删", _detect_heading_deleted),
    ("术语用了错误译法", _detect_term_drift),
    ("整段漏译", _detect_omission),
    ("表格行被合并", _detect_table_merged),
    ("译文为空", _detect_empty_translation),
]


def run_l3(verbose=True):
    cases = []
    for name, fn in L3_CASES:
        try:
            detected = bool(fn())
            err = None
        except Exception as e:                      # 自测自身出错也算失败
            detected, err = False, f"{type(e).__name__}: {e}"
        item = {"name": name, "detected": detected}
        if err:
            item["error"] = err
        cases.append(item)

    detected_n = sum(1 for c in cases if c["detected"])
    all_pass = detected_n == len(cases)
    report = {
        "layer": "L3 校验器反例自测",
        "cases_total": len(cases),
        "cases_detected": detected_n,
        "all_pass": all_pass,
        "cases": cases,
    }
    write_json(os.path.join(OUT_DIR, "l3_report.json"), report)

    if verbose:
        print("=" * 78)
        print("L3 校验器反例自测")
        print("=" * 78)
        for c in cases:
            mark = "✅ 已检出" if c["detected"] else "❌ 未检出"
            extra = f"  ({c['error']})" if c.get("error") else ""
            print(f"    {mark}  {c['name']}{extra}")
        print(f"  合计：{detected_n}/{len(cases)}   all_pass={all_pass}")
        if not all_pass:
            print("  ❌ 自测未全通过 —— 校验器本身可能失效，其余层的数字不可信！")
        print(f"  已写出：{os.path.join(OUT_DIR, 'l3_report.json')}")
    return report


# ══════════════════════════════════════════════════════════════════
#  L4 语义质量（分层抽样 → 人工标注 → 汇总统计）
# ══════════════════════════════════════════════════════════════════
def pick_paragraphs(body, k=PARAS_PER_DOC):
    """
    从文档【中部】取 k 个自然段的位置索引与内容，跳过代码块、表格、非正文行。
    去首尾各 15%，避免开头结尾的导航/页脚干扰。
    返回 [(para_index, text), ...]，索引是原始 split_paragraphs 的下标。
    """
    paras = split_paragraphs(body)
    keep = [(i, p) for i, p in enumerate(paras)
            if not p.lstrip().startswith("|")
            and not p.lstrip().startswith("![")]
    if not keep:
        return []
    lo = int(len(keep) * 0.15)
    hi = max(lo + 1, len(keep) - lo)
    mid = keep[lo:hi] or keep
    if len(mid) <= k:
        return list(mid)
    rnd = random.Random(SEED)
    idxs = sorted(rnd.sample(range(len(mid)), k))
    return [mid[i] for i in idxs]


def cross_lingual_keys(text):
    """
    抽取跨语言共享的"键" —— 用于判断中英两段是否讲同一件事。
    ⚠️ 为什么需要：中英字符集不同，difflib 相似度天然接近 0，
       无法区分"段落错位"与"语言不同"。而 URL、代码标识符、数字、
       专名在两种语言里是【逐字保留】的，是最好的对齐锚点。
    """
    keys = set()
    for u in re.findall(r"https?://[^\s\)\]<>\"']+", text):
        keys.add(u.rstrip(".,;:!?。，；：！？"))
    for w in re.findall(r"[A-Za-z_][A-Za-z0-9_\-]{2,}", text):
        if w[0].isupper() or "_" in w or any(c.isdigit() for c in w):
            keys.add(w.lower())
    for n in re.findall(r"\d+", text):
        keys.add(n)
    return keys


def align_paragraphs_by_keys(src_paras, dst_paras):
    """
    按"英文侧键"把原文段落映射到译文段落。
    返回 [(src_idx, dst_idx, shared_key_count), ...]

    做法：对每个原文段落算「该段键的最后一个」在译文中的位置，
          用【两者的键数量之比】做等比例映射 ——
          因为键在翻译中是逐字保留的，两侧数量比应接近段落长度比。
    """
    src_keys = [cross_lingual_keys(p) for p in src_paras]
    dst_keys = [cross_lingual_keys(p) for p in dst_paras]
    cum_s, cum_d = [], []
    acc = 0
    for k in src_keys:
        acc += len(k)
        cum_s.append(acc)
    acc = 0
    for k in dst_keys:
        acc += len(k)
        cum_d.append(acc)
    total_s, total_d = cum_s[-1] if cum_s else 0, cum_d[-1] if cum_d else 0
    if total_s == 0 or total_d == 0:
        return []
    out = []
    for i, ks in enumerate(src_keys):
        if not ks:
            continue
        ratio = cum_s[i] / total_s
        j = min(range(len(dst_paras)), key=lambda x: abs(cum_d[x] / total_d - ratio))
        # 校验：译文段 j 必须与原文段 i 有共享键，否则认为映射不可靠
        shared = len(ks & dst_keys[j])
        out.append((i, j, shared))
    return out


def pick_paragraphs_by_section(src_body, dst_body, k=PARAS_PER_DOC):
    """
    用【章节锚点】对齐后取段 —— 比纯段落索引可靠得多。

    ⚠️ 为什么不能用段落索引配对：
       中英段落切分习惯不同，且网页抽取常留重复块（实测某文档原文把整张
       表格重复了两遍、译文只译一遍），索引会整体错位，产生"原文讲图像生成、
       译文讲图像编辑"这类不对应的标注点，污染人工标注。
       而标题结构是稳定的 —— 本项目的 L1 已证明标题数 41/41 完全一致。

    做法：把两边的标题作为锚点按序配对，只在【标题数与内容都对应】的
          章节内取样，并返回该章节的中点段落。
    返回 [(译文段, 原文段, 章节标题, 共享键数), ...]
    （共享键数 = 该段原文与译文共同拥有的 URL/标识符/数字/专名个数，
      它是"两段确实对应"的客观证据，取代了不可靠的字符相似度。）
    """
    def sections(text):
        """切出 [(标题级别, 标题文本, 章节正文), ...]"""
        body = split_front_matter(text)[1]
        lines = body.split("\n")
        out, cur = [], None
        for ln in lines:
            m = re.match(r"^(#{1,6})\s+(\S.*)$", ln)
            if m:
                if cur:
                    out.append(cur)
                cur = [len(m.group(1)), m.group(2).strip(), []]
            elif cur is not None:
                cur[2].append(ln)
        if cur:
            out.append(cur)
        return out

    ss, ds = sections(src_body), sections(dst_body)
    # 只保留前后都有对应标题的章节（数量取较小边）
    n = min(len(ss), len(ds))
    if n == 0:
        return []

    cand = []
    for i in range(n):
        lv_s, t_s, body_s = ss[i]
        lv_d, t_d, body_d = ds[i]
        # 标题级别必须一致，否则认为锚点不可信
        if lv_s != lv_d:
            continue
        sp = split_paragraphs("\n".join(body_s))
        dp = split_paragraphs("\n".join(body_d))
        sp = [p for p in sp if not p.lstrip().startswith(("|", "!["))]
        dp = [p for p in dp if not p.lstrip().startswith(("|", "!["))]
        # ⚠️ 丢掉过短段落：网页里的 CTA 广告文案（"Get started for free"）
        #    和导航残留段落长度很短，取到它们会让标注者拿到"原文是按钮、
        #    译文是别的按钮"这种无意义判定点。
        sp = [p for p in sp if len(p.strip()) >= 80]
        dp = [p for p in dp if len(p.strip()) >= 30]
        if not sp or not dp:
            continue
        # 用跨语言共享键做真正的对齐（URL/标识符/数字/专名在两种语言里逐字保留）
        pairs = align_paragraphs_by_keys(sp, dp)
        # 只取有共享键、且键数足够多的段落 —— 没有共享键就无法确认两段对应
        good = [(i, j, n) for i, j, n in pairs if n >= 2]
        if not good:
            continue
        # 取共享键最多的那个段落，它最可能是真正对应的一段
        good.sort(key=lambda x: -x[2])
        i, j, n = good[0]
        cand.append((sp[i], dp[j], t_s, n))

    if len(cand) <= k:
        return cand
    rnd = random.Random(SEED)
    return [cand[i] for i in sorted(rnd.sample(range(len(cand)), k))]


def para_similarity(src_para, dst_para):
    """
    用 SequenceMatcher 算中英段落的结构相似度，用于自检配对是否可信。
    ⚠️ 中英字符集不同，比值天然偏低，所以阈值只用来抓"完全错位"（接近 0）。
    """
    if not src_para or not dst_para:
        return 0.0
    return round(difflib.SequenceMatcher(
        None, src_para.lower(), dst_para.lower()).ratio(), 4)


def run_l4_sample(verbose=True):
    p = pair_docs()
    pairs = p["pairs"]
    if not pairs:
        print("❌ 没有已翻译的文档，无法抽样")
        return None

    # 预计算每篇的指标
    info = []
    gloss_terms = []
    if os.path.isfile(GLOSSARY):
        gloss_terms = (read_json(GLOSSARY).get("terms") or [])
    for doc_id, sp, dp in pairs:
        st = read_text(sp)
        info.append({
            "doc": doc_id, "src": sp, "dst": dp,
            "chars": nonspace_len(st),
            "code_blocks": len(find_code_blocks(st)),
            "tables": len(find_table_lines(st)),
            "terms": sum(len(term_regex(t["en"], bool(t.get("case_sensitive")))
                             .findall(st)) for t in gloss_terms),
        })

    picked, seen = [], set()

    def take(items, layer, n):
        got = []
        for it in items:
            if len(got) >= n:
                break
            if it["doc"] in seen:
                continue
            seen.add(it["doc"])
            got.append(it)
            picked.append({"doc": it["doc"], "layer": layer})
        return got

    take(sorted(info, key=lambda x: -x["chars"]), "层1 字符数最长", LAYER_DOCS)
    take(sorted(info, key=lambda x: -x["code_blocks"]), "层2 代码块最多", LAYER_DOCS)
    take(sorted(info, key=lambda x: -x["tables"]), "层3 表格最多", LAYER_DOCS)
    take(sorted(info, key=lambda x: -x["terms"]), "层4 术语密度最高", LAYER_DOCS)
    take(sorted([i for i in info if RISK_NAME_MARKER in i["doc"]],
                key=lambda x: -x["chars"]), "层5 质量可能受损", RISK_LAYER_DOCS)

    by_doc = {i["doc"]: i for i in info}
    items = []
    for pk in picked:
        it = by_doc[pk["doc"]]
        # ⚠️ 用【章节锚点】对齐取段，不用段落索引。
        #    段落索引对结构有差异的文档（重复块、段落切分不同）必然错位，
        #    会让标注者拿到不对应的原文/译文，污染语义评分。
        for n, (sp, dp, title, shared) in enumerate(
                pick_paragraphs_by_section(read_text(it["src"]),
                                           read_text(it["dst"])), 1):
            items.append({"doc": it["doc"], "para": n,
                          "section": title, "layer": pk["layer"],
                          "src": sp, "dst": dp,
                          "shared_keys": shared})

    # 配对自检：共享键过少说明该判定点的原文/译文可能不对应，需人工留意
    low_sim = [i for i in items if i["shared_keys"] < 3]

    sample = {
        "seed": SEED,
        "paras_per_doc": PARAS_PER_DOC,
        "docs_picked": picked,
        "sample_size": len(items),
        "alignment_selfcheck": {
            "min_shared_keys": 3,
            "low_shared_keys_count": len(low_sim),
            "low_shared_keys_items": [
                {"doc": i["doc"], "para": i["para"],
                 "shared_keys": i["shared_keys"]} for i in low_sim],
        },
        "items": items,
    }
    write_json(os.path.join(OUT_DIR, "l4_sample.json"), sample)

    # 生成两份标注任务（内容相同，各自独立完成）
    crit = """## 判定标准

对每个判定点，逐项判断（只依据你看到的两段文字，**不要参考术语表**）：

| 字段 | 含义 |
|---|---|
| `omission` | 译文是否**漏掉**原文的实质内容（整句/整段没译） |
| `mistranslation` | 译文是否**译错**了原文的意思（与漏译不同：译了但意思不对） |
| `term_drift` | 专业术语是否用了**不一致**的译法（同一概念前后译法不同） |
| `machine_tone` | 是否有明显**机翻腔**（生硬直译、语序不自然、用词不地道） |
| `overall` | 综合判断：`PASS` 或 `FAIL`。任一项为 `yes` 且影响理解 -> `FAIL` |

> ⚠️ 两份标注任务内容完全相同，但**必须由不同的人、或在不同时间独立完成**。
>    不要互相对照着填，否则一致性统计会虚高。
"""
    for who in ("A", "B"):
        lines = [f"# 语义标注任务 —— 标注者 {who}", "",
                 f"抽样种子：{SEED}　判定点：{len(items)} 个　"
                 f"文档：{len({i['doc'] for i in items})} 篇", "", crit, "---", ""]
        cur = None
        for i, it in enumerate(items, 1):
            if it["doc"] != cur:
                cur = it["doc"]
                lines += [f"## {cur}", ""]
            warn = ""
            if it["shared_keys"] < 3:
                # 共享键少说明对应关系不够确凿 —— 如实提示标注者，不要悄悄塞给他
                warn = (f"\n> ⚠️ 本判定点的原文/译文仅有 {it['shared_keys']} 个共享键"
                        f"（URL/标识符/数字/专名），对应关系不够确凿；"
                        f"若你认为两者不对应，请在 `overall` 填 `SKIP`。\n")
            lines += [f"### 判定点 {i}　（doc={it['doc']}　"
                      f"章节={it.get('section','')}　{it['layer']}）", warn,
                      "**原文**", "", "> " + it["src"].replace("\n", "\n> "), "",
                      "**译文**", "", "> " + (it["dst"] or "（缺译文）").replace("\n", "\n> "), "",
                      "判定：omission=____  mistranslation=____  term_drift=____  "
                      "machine_tone=____  overall=____", "", "---", ""]
        with open(os.path.join(OUT_DIR, f"annotator_{who}.md"), "w",
                  encoding="utf-8", newline="\n") as f:
            f.write("\n".join(lines))

        tpl = {"annotator": who, "seed": SEED,
               "items": [{"doc": it["doc"], "para": it["para"],
                          "omission": "", "mistranslation": "",
                          "term_drift": "", "machine_tone": "",
                          "overall": ""} for it in items]}
        write_json(os.path.join(OUT_DIR, f"annotator_{who}.json"), tpl)

    if verbose:
        print("=" * 78)
        print("L4 语义质量 —— 抽样")
        print("=" * 78)
        print(f"  抽样文档 {len({i['doc'] for i in items})} 篇　判定点 {len(items)} 个")
        print("  分层：")
        for pk in picked:
            print(f"    [{pk['layer']}] {pk['doc']}")
        sc = sample["alignment_selfcheck"]
        print(f"  配对自检：共享键 <{sc['min_shared_keys']} 的判定点 "
              f"{sc['low_shared_keys_count']} 个"
              + ("（✅ 无）" if not sc["low_shared_keys_count"]
                 else "（⚠️ 需人工留意，可能段落不对应）"))
        for x in sc["low_shared_keys_items"][:5]:
            print(f"    {x['doc']} 段{x['para']}  共享键={x['shared_keys']}")
        print("  已生成：")
        for fn in ("annotator_A.md", "annotator_B.md",
                   "annotator_A.json", "annotator_B.json"):
            print(f"    {os.path.join(OUT_DIR, fn)}")
        print("  下一步：人工填写 A/B 两份 JSON，再跑 `check_quality.py l4-score`")
    return sample


def wilson_ci(k, n, z=Z95):
    """
    二项比例的 95% Wilson 置信区间。
    ⚠️ 必须用 Wilson，不能用正态近似：
       报"检出 0 个漏译"时，正态近似给出零宽度区间（统计上荒谬）；
       Wilson 给出 [0, 0.065] 这类合理上界，意思是"很可能低于 6.5%"。
    """
    if n <= 0:
        return [0.0, 0.0]
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return [round(max(0.0, center - half), 4), round(min(1.0, center + half), 4)]


def kappa_interpret(k):
    """Landis & Koch 一致性解释区间。"""
    if k < 0:
        return "差 (κ < 0)"
    if k <= 0.20:
        return "轻微一致 (0–0.20)"
    if k <= 0.40:
        return "一般一致 (0.21–0.40)"
    if k <= 0.60:
        return "中等一致 (0.41–0.60)"
    if k <= 0.80:
        return "显著一致 (0.61–0.80)"
    return "几乎完全一致 (0.81–1.00)"


def run_l4_score(verbose=True):
    pa = os.path.join(OUT_DIR, "annotator_A.json")
    pb = os.path.join(OUT_DIR, "annotator_B.json")
    if not (os.path.isfile(pa) and os.path.isfile(pb)):
        print("ℹ️ L4 待人工完成：缺少 annotator_A.json / annotator_B.json")
        if verbose:
            print("   先跑 `check_quality.py l4-sample` 生成标注任务。")
        return None

    ja, jb = read_json(pa), read_json(pb)
    da = {(i["doc"], i["para"]): i for i in ja.get("items", [])}
    db = {(i["doc"], i["para"]): i for i in jb.get("items", [])}
    keys = sorted(set(da) & set(db))
    if not keys:
        print("❌ 两份标注没有可对齐的判定点（doc/para 对不上）")
        return None

    def norm(v):
        return str(v or "").strip().upper()

    VALID = {"PASS", "FAIL", "SKIP"}
    # ⚠️ 必须排除未填写与 SKIP 的判定点：
    #    两份空模板的 overall 都是空字符串，归一化后"相等"，
    #    会算出 Po=1.0、κ=0.0 这种毫无意义的"一致性"（实测踩到）。
    scored = [k for k in keys
              if norm(da[k].get("overall")) in VALID
              and norm(db[k].get("overall")) in VALID
              and norm(da[k].get("overall")) != "SKIP"
              and norm(db[k].get("overall")) != "SKIP"]
    n_a = sum(1 for k in keys if norm(da[k].get("overall")) in VALID)
    n_b = sum(1 for k in keys if norm(db[k].get("overall")) in VALID)
    if not scored:
        print("ℹ️ L4 待人工完成：两份标注的 overall 都还是空的")
        print(f"   已填写：A {n_a}/{len(keys)}　B {n_b}/{len(keys)}")
        print("   请填写 annotator_A.json / annotator_B.json 的 overall 字段"
              "（PASS / FAIL；不对应的判定点填 SKIP）")
        return None

    A = [norm(da[k].get("overall")) for k in scored]
    B = [norm(db[k].get("overall")) for k in scored]

    n = len(keys)
    po = sum(1 for a, b in zip(A, B) if a == b) / n
    pA = sum(1 for a in A if a == "PASS") / n
    pB = sum(1 for b in B if b == "PASS") / n
    pe = pA * pB + (1 - pA) * (1 - pB)
    kappa = (po - pe) / (1 - pe) if abs(1 - pe) > 1e-12 else 0.0

    # 四个缺陷维度：任一人标 yes 即算"检出"（召回导向），并给 Wilson 区间
    dims = ["omission", "mistranslation", "term_drift", "machine_tone"]
    defect_rates = collections.OrderedDict()
    for d in dims:
        k = sum(1 for key in scored
                if norm(da[key].get(d)) == "YES" or norm(db[key].get(d)) == "YES")
        defect_rates[d] = {"k": k, "n": n,
                           "rate": round(k / n, 4),
                           "wilson_95": wilson_ci(k, n)}

    disagreements = [{"doc": key[0], "para": key[1],
                      "A": A[i], "B": B[i]}
                     for i, key in enumerate(scored) if A[i] != B[i]]

    report = {
        "layer": "L4 语义质量",
        "sample_size": len(keys),
        "scored_size": n,
        "filled": {"A": n_a, "B": n_b, "excluded_unfilled_or_skip": len(keys) - n},
        "agreement": {
            "observed_agreement": round(po, 4),
            "expected_agreement": round(pe, 4),
            "cohen_kappa": round(kappa, 4),
            "interpretation": kappa_interpret(kappa),
        },
        "defect_rates": defect_rates,
        "disagreements": disagreements,
    }
    write_json(os.path.join(OUT_DIR, "l4_report.json"), report)

    if verbose:
        print("=" * 78)
        print("L4 语义质量 —— 汇总")
        print("=" * 78)
        print(f"  判定点：{n}")
        ag = report["agreement"]
        print(f"  观察一致率 Po = {ag['observed_agreement']}")
        print(f"  期望一致率 Pe = {ag['expected_agreement']}")
        print(f"  Cohen's κ    = {ag['cohen_kappa']}  （{ag['interpretation']}）")
        print("  缺陷维度检出率（95% Wilson 区间）：")
        for d, v in defect_rates.items():
            print(f"    {d:<16} {v['k']:>3}/{v['n']:<3} = {v['rate']:.4f}  "
                  f"[{v['wilson_95'][0]:.4f}, {v['wilson_95'][1]:.4f}]")
        if disagreements:
            print(f"  分歧 {len(disagreements)} 个（需人工裁定）：")
            for x in disagreements[:10]:
                print(f"    {x['doc']} 段{x['para']}: A={x['A']} B={x['B']}")
        print(f"  已写出：{os.path.join(OUT_DIR, 'l4_report.json')}")
    return report


# ══════════════════════════════════════════════════════════════════
#  汇总 stats.json
# ══════════════════════════════════════════════════════════════════
def write_stats(l1, l2, l3, l4):
    """合并四层结果。所有数字由脚本计算得出，无手填常量。"""
    scope = l1["scope"] if l1 else {}
    t = l1["totals"] if l1 else {}

    def f(layer, key):
        return layer.get(key) if layer else None

    stats = {
        "generated_by": "check_quality.py",
        "scope": {
            "src_docs": scope.get("src_docs"),
            "translated": scope.get("translated"),
            "not_translated": len(scope.get("not_translated") or []),
        },
        "l1_completeness": {
            "docs": f"{scope.get('translated')}/{scope.get('translated')}" if l1 else None,
            # ── 硬门槛项（任一不达标即失败）──
            "title_lines": t.get("title_lines_ok"),
            "code_blocks": t.get("code_blocks_ok"),
            "code_blocks_bytes": t.get("code_blocks_bytes_ok"),
            "tables": t.get("tables_ok"),
            "links": t.get("links_ok"),
            "length_ratio_median": t.get("length_ratio_median"),
            # ── 信息项（不作门槛）──
            #    body_lines：汉语行数天然少于英语
            #    head_tail ：段落按空行配对，中英切分习惯不同会错位
            "informational": {
                "body_lines": t.get("body_lines_ok"),
                "head_tail": t.get("head_tail_ok"),
                "note": ("行数与段首段尾仅作信息项：汉语行数天然少于英语，"
                         "段落切分差异会造成错位，均不适合做门槛"),
            },
        },
        "l2_terminology": {
            "slots": (f"{l2['slots_hit']}/{l2['slots_total']}"
                      if l2 and l2.get("frozen_ok") else None),
            "hit_rate": l2.get("hit_rate") if l2 and l2.get("frozen_ok") else None,
            "by_handling": (l2.get("by_handling")
                            if l2 and l2.get("frozen_ok") else None),
            "frozen_ok": bool(l2.get("frozen_ok")) if l2 else None,
        },
        "l3_selftest": {
            "cases": f"{l3['cases_detected']}/{l3['cases_total']}" if l3 else None,
            "all_pass": l3.get("all_pass") if l3 else None,
        },
        "headline": {
            "docs_verified": (f"{scope.get('translated')}/{scope.get('translated')}"
                              if l1 else None),
            "term_slots": (f"{l2['slots_hit']}/{l2['slots_total']}"
                           if l2 and l2.get("frozen_ok") else None),
            "selftest_cases": (f"{l3['cases_detected']}/{l3['cases_total']}"
                               if l3 else None),
        },
    }

    write_json(os.path.join(OUT_DIR, "stats.json"), stats)
    return stats


def exit_code(l1=None, l2=None, l3=None):
    """
    退出码：全部通过 0；L1/L2/L3 有失败项或自测未通过 -> 非 0。
    ⚠️ 单独跑某一层时也必须返回对应的非零码 ——
       曾经只在 all 分支里算退出码，导致 `check_quality.py l1` 明明报了
       "标题行数 0/1 ❌" 却返回 0，CI 会误判为通过（实测踩到）。
    """
    if l3 and not l3.get("all_pass"):
        return 3
    if l1 and any(v for v in l1["failures"].values()):
        return 1
    if l2 is not None and not l2.get("frozen_ok", True):
        return 2
    return 0


# ══════════════════════════════════════════════════════════════════
#  入口
# ══════════════════════════════════════════════════════════════════
USAGE = """check_quality.py —— 翻译项目质量校验

用法：
  check_quality.py all        跑全部自动层（l1+l2+l3）
  check_quality.py l1         结构完整性
  check_quality.py l2         术语一致性
  check_quality.py l3         校验器反例自测
  check_quality.py l4-sample  生成语义标注任务（L4，需人工，不在 all 内）
  check_quality.py l4-score   汇总人工标注，计算一致性统计（L4，不在 all 内）
"""


def main(argv):
    cmd = (argv[0] if argv else "all").lower()
    if cmd in ("-h", "--help", "help"):
        print(USAGE)
        return 0

    # ---- 换源：从 argv 取路径参数并重设全局（必须在建目录/读文件之前）
    _opts = {}
    for _i, _a in enumerate(argv):
        if _a in PATH_FLAGS and _i + 1 < len(argv):
            _opts[PATH_FLAGS[_a][0]] = argv[_i + 1]
    if _opts:
        configure(**_opts)

    os.makedirs(OUT_DIR, exist_ok=True)
    print(USAGE.split("\n\n")[0])
    print(f"  原文目录：{SRC_DIR}")
    print(f"  译文目录：{DST_DIR}")
    print(f"  术语表　：{GLOSSARY}")
    print(f"  报告目录：{OUT_DIR}")
    print()

    l1 = l2 = l3 = l4 = None

    if cmd == "l1":
        l1 = run_l1()
    elif cmd == "l2":
        l2 = run_l2()
    elif cmd == "l3":
        l3 = run_l3()
    elif cmd == "l4-sample":
        run_l4_sample()
    elif cmd == "l4-score":
        l4 = run_l4_score()
    elif cmd == "all":
        # 只跑自动层；L4 需人工标注，改为显式调用 `l4-sample` / `l4-score`
        l1 = run_l1()
        print()
        l2 = run_l2()
        print()
        l3 = run_l3()
    else:
        print(f"❌ 未知子命令：{cmd}\n")
        print(USAGE)
        return 64

    # 汇总（仅 all 或能取到已有报告时）
    if cmd == "all":
        stats = write_stats(l1, l2, l3, l4)
        print()
        print("=" * 78)
        print("最终 headline")
        print("=" * 78)
        h = stats["headline"]
        print(f"  已核对文档      {h['docs_verified']}")
        print(f"  术语槽位        {h['term_slots']}")
        print(f"  反例自测        {h['selftest_cases']}")
        code = exit_code(l1, l2, l3)
        print()
        if code == 0:
            print("✅ 自动层（L1/L2/L3）全部通过")
        else:
            print(f"❌ 存在失败项（退出码 {code}）—— 详见上面各层明细")
        print(f"  已写出：{os.path.join(OUT_DIR, 'stats.json')}")
        print("  ℹ️ L4 语义层需人工标注，未纳入本命令；"
              "如需执行：`l4-sample` -> 填 annotator_A/B.json -> `l4-score`")
        return code

    # ⚠️ 单层子命令也要返回对应退出码，不能一律 0
    return exit_code(l1, l2, l3)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
