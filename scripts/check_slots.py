#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_slots.py —— 管线 ⑤ 术语槽位校验

作用
    扫描【原文】extracted/*.md，为术语表里每条术语穷举出现位置（= 槽位），
    按【文档】粒度归类（本项目不做切块，所以按文档统计）。
    翻译完成后用 --verify 逐槽核对是否用了指定译法，输出命中率。

⚠️ 为什么必须扫描【原文】而不是译文
    若某段整段漏译，扫译文时那段没有该术语、不计入槽位，漏译就永远查不出来。
    扫原文则槽位固定，漏了立刻暴露。槽位数是「合同」，不是「结果」。

⚠️ 为什么要先排除导航/页脚/链接行/图片行
    实测 extracted/ 残留大量网页导航，英文词总数从真实约 76,000 膨胀到
    131,375（+72%）。不排除的话槽位虚高，而且"命中率"会因译文不含导航
    而永远达不到 100%，指标直接失去意义。

用法
    python scripts/check_slots.py            统计槽位，写 slot_report.json
    python scripts/check_slots.py --selftest 反例自测（必须能真的失败）
    python scripts/check_slots.py --verify   翻译完成后核对命中率
"""

import collections
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
GLOSSARY_NAME = "glossary.json"
SLOT_REPORT_NAME = "slot_report.json"

EXTRACTED_DIR = os.path.join(BASE_DIR, "work", "extracted")
TRANSLATED_DIR = os.path.join(BASE_DIR, "output", "translated")
GLOSSARY_PATH = os.path.join(BASE_DIR, "work", "glossary", "glossary.json")
SLOT_REPORT_PATH = os.path.join(BASE_DIR, "work", "slots", "slot_report.json")
# ⚠️ 必须与 manifest / extract_report / fetch_report 同处 work/reports/。
#    曾经直接写在仓库根，导致根目录散落生成物、.gitignore 也漏配。
VERIFY_REPORT_PATH = os.path.join(BASE_DIR, "work", "reports", "verify_report.json")


def configure(extracted_dir=None, translated_dir=None, glossary=None,
              slot_report=None, verify_report=None):
    """
    按命令行参数重设路径全局变量（换源复用）。
    ⚠️ 下游函数直接读这些模块级常量，必须在这里一次性重设。
    """
    global EXTRACTED_DIR, TRANSLATED_DIR, GLOSSARY_PATH
    global SLOT_REPORT_PATH, VERIFY_REPORT_PATH
    if extracted_dir:
        EXTRACTED_DIR = os.path.abspath(extracted_dir)
    if translated_dir:
        TRANSLATED_DIR = os.path.abspath(translated_dir)
    if glossary:
        GLOSSARY_PATH = os.path.abspath(glossary)
    if slot_report:
        SLOT_REPORT_PATH = os.path.abspath(slot_report)
    if verify_report:
        VERIFY_REPORT_PATH = os.path.abspath(verify_report)


PATH_FLAGS = {
    "--extracted-dir": ("extracted_dir", "抽取产出目录"),
    "--translated-dir": ("translated_dir", "中文译文目录"),
    "--glossary": ("glossary", "术语表 JSON"),
    "--slot-report": ("slot_report", "槽位报告输出路径"),
    "--verify-report": ("verify_report", "命中率报告输出路径"),
}

# 译文长度低于原文这个比例 → 判为【疑似漏译】而非【译法不一致】
MISSING_TRANSLATION_RATIO = 0.30

VALID_HANDLING = ("translate", "keep_en", "bilingual", "acronym")

# ============================================================ 专有名词保护
# ⚠️ 为什么需要：有些术语是「更长专有名词的一部分」，拆开算槽位会误报。
#    实测 The Model Context Protocol (MCP) 里的 model / context
#    被当成独立术语，导致 MCP TypeScript SDK 那份 README 出现 2 个假 miss
#    （译文里专名整体保留英文是对的，不该判错）。
#    这些专名不写死在代码里 —— 由术语表用 proper_names 字段声明。
DEFAULT_PROPER_NAMES = [
    "Model Context Protocol",
    "Context Protocol",
    "Pull Request",
    "Chain of Thought",
    "Vibe Coding",
]


def build_proper_name_re(names):
    """
    专名匹配正则：专名 + 其后若干可继续构成专名的词。

    ⚠️ 为什么后面还要跟一串小写词：
       专名常常带小写的通用后缀，如
         "Model Context Protocol servers"
         "Model Context Protocol Registry"
         "Pull Request review"
       若只认首字母大写的后续词，这类标题里的 context / model 会被算成
       「无法翻译的槽位」，产生假 miss。实测 MCP servers README 的
       `# Model Context Protocol servers` 就踩了这个坑。
    """
    if not names:
        return None
    alts = "|".join(re.escape(n) for n in sorted(set(names), key=len, reverse=True))
    return re.compile(
        r"(?<![A-Za-z])(?:" + alts + r")"
        r"(?:\s+[A-Za-z][A-Za-z0-9\-]*){0,3}(?![A-Za-z])")


def mask_proper_names(text, pat):
    """
    把专名替换成等长空格。
    ⚠️ 等长替换是为了不改变其它术语的行内位置与词边界判断。
    """
    if pat is None:
        return text
    return pat.sub(lambda m: " " * len(m.group(0)), text)

LINKY_RE = re.compile(r"https?://|www\.|\.com/|\.ai/|\.dev/|\.ai\b|cdn-cgi|next/image|@")


# ============================================================ 基础工具
def reconfigure_stdout():
    """Windows GBK 控制台：打印中文/emoji 前必须把 stdout 设成 UTF-8"""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def strip_front_matter(text):
    """去掉 YAML front matter"""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end >= 0:
            return text[end + 4:]
    return text


def strip_code_blocks(text):
    """
    去掉代码块【连同内容】，含三种形态：
      ① 抽取阶段插入的 <!-- CODE_BLOCK_START ... --> ... <!-- CODE_BLOCK_END ... -->
         ⚠️ 只删标记是不够的：标记之间的代码内容会残留下来，
            实测导致代码里的 agent 被计入槽位（agent 槽位 3→6）。
      ② Markdown 围栏 ```lang ... ```
    ⚠️ 代码与数据不译，代码里的 agent/MCP 不算槽位。
    """
    t = re.sub(r"<!--\s*CODE_BLOCK_START.*?CODE_BLOCK_END\s*-->", " ", text, flags=re.S)
    t = re.sub(r"^```.*?^```\s*$", " ", t, flags=re.S | re.M)
    return t


def is_content_line(line):
    """正文行判定（与 init_glossary.py 完全一致，口径不同会导致槽位数对不上）"""
    s = line.strip()
    if not s:
        return False
    if s.startswith("!["):
        return False
    if s.startswith("<!--"):
        return False
    if LINKY_RE.search(s):
        return False
    if s.startswith("-") and s.count("](") >= 1:
        return False
    return True


def content_lines(text):
    """返回正文行列表（已排除 front matter / 代码块 / 导航行）"""
    t = strip_code_blocks(strip_front_matter(text))
    return [ln for ln in t.split("\n") if is_content_line(ln)]


def count_english_words(text):
    return len(re.findall(r"[A-Za-z]{2,}", text))


# ============================================================ 术语匹配（唯一实现）
def term_pattern(term, case_sensitive=False, extra_space=True):
    r"""
    构造术语匹配正则。
    ⚠️ 词边界只在【英文】术语上使用：
       中文译法（智能体/代码审查）用 (?<![A-Za-z])...(?![A-Za-z]) 会失配 ——
       例如「不是智能体。」里 智能体 后面是「。」，但「智能体的」后面是中文，
       边界断言行为不一致，实测导致正确译文被误报为未命中。
       所以：术语含 CJK 字符时，不加英文词边界。
    ⚠️ 多词术语允许词间空白变化（"code   review" 也算命中）。
    """
    parts = term.split()
    body = r"\s+".join(re.escape(p) for p in parts) if extra_space else re.escape(term)
    flags = 0 if case_sensitive else re.IGNORECASE
    has_cjk = any("\u4e00" <= ch <= "\u9fff" for ch in term)
    if has_cjk:
        return re.compile(body, flags)
    return re.compile(r"(?<![A-Za-z])" + body + r"(?![A-Za-z])", flags)


def find_slots(lines, term, case_sensitive=False):
    """在正文行里穷举槽位，返回 (命中总数, {行号: 次数})"""
    pat = term_pattern(term, case_sensitive)
    total = 0
    per_line = {}
    for i, ln in enumerate(lines):
        n = len(pat.findall(ln))
        if n:
            per_line[i] = n
            total += n
    return total, per_line


# ============================================================ 术语表读取与冻结校验
def load_glossary(path=None):
    # ⚠️ 同上：默认值不可绑定全局常量，否则 configure() 后失效
    if path is None:
        path = GLOSSARY_PATH
    if not os.path.isfile(path):
        raise FileNotFoundError(f"术语表不存在：{path}（先跑 init_glossary.py）")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def compute_frozen_hash(gloss):
    """
    ⚠️ 必须排除 frozen_hash 字段自身再算，否则循环依赖：
       哈希取决于内容，而内容里又含哈希值。
    """
    payload = {k: v for k, v in gloss.items() if k != "frozen_hash"}
    blob = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def glossary_hash(gloss):
    """术语表当前内容的哈希（用于与 slot_report 记录比对）"""
    return compute_frozen_hash(gloss)


def validate_glossary(gloss):
    """校验术语表结构，返回错误列表"""
    errs = []
    if not isinstance(gloss.get("terms"), list) or not gloss["terms"]:
        errs.append("术语表没有 terms")
        return errs
    for t in gloss["terms"]:
        for k in ("en", "zh", "handling"):
            if k not in t:
                errs.append(f"术语缺字段 {k}: {t}")
        if t.get("handling") not in VALID_HANDLING:
            errs.append(f"handling 非法：{t.get('en')} → {t.get('handling')}"
                        f"（只允许 {VALID_HANDLING}）")
        if not t.get("en", "").strip():
            errs.append(f"空的 en：{t}")
    return errs


# ============================================================ 任务 1：槽位统计
def load_originals():
    docs = {}
    if not os.path.isdir(EXTRACTED_DIR):
        return docs
    for fn in sorted(os.listdir(EXTRACTED_DIR)):
        if not fn.lower().endswith(".md"):
            continue
        with open(os.path.join(EXTRACTED_DIR, fn), "rb") as f:
            raw = f.read().decode("utf-8", "replace")
        docs[os.path.splitext(fn)[0]] = {
            "path": os.path.join(EXTRACTED_DIR, fn),
            "text": raw,
            "lines": content_lines(raw),
        }
    return docs


def build_slot_report(gloss, docs):
    per_term = []
    per_doc = collections.Counter()
    total_lines = 0
    kept_lines = 0
    proper_pat = build_proper_name_re(
        gloss.get("proper_names") or DEFAULT_PROPER_NAMES)

    masked = {d: mask_proper_names("\n".join(v["lines"]), proper_pat)
              for d, v in docs.items()}

    for d in docs.values():
        total_lines += len(strip_code_blocks(strip_front_matter(d["text"])).split("\n"))
        kept_lines += len(d["lines"])

    for t in gloss["terms"]:
        en = t["en"]
        cs = bool(t.get("case_sensitive"))
        slots_per_doc = {}
        slots_total = 0
        for doc_id, d in docs.items():
            n, _ = find_slots(masked[doc_id].split("\n"), en, cs)
            if n:
                slots_per_doc[doc_id] = n
                slots_total += n
                per_doc[doc_id] += n
        per_term.append({
            "en": en,
            "zh": t.get("zh"),
            "handling": t.get("handling"),
            "slots_total": slots_total,
            "slots_per_doc": dict(sorted(slots_per_doc.items(), key=lambda kv: -kv[1])),
            "slots_in_title": 0,     # 标题已计入正文行；保留字段以备扩展
        })

    by_handling = collections.Counter()
    for t, term in zip(per_term, gloss["terms"]):
        by_handling[term.get("handling")] += t["slots_total"]

    report = {
        "generated_by": "check_slots.py",
        "glossary_version": gloss.get("version"),
        "glossary_hash": glossary_hash(gloss),
        "glossary_frozen": bool(gloss.get("frozen")),
        "corpus": {
            "docs": len(docs),
            "content_lines": kept_lines,
            "all_lines": total_lines,
            "excluded_lines": total_lines - kept_lines,
            "english_words_in_content": sum(count_english_words("\n".join(d["lines"]))
                                            for d in docs.values()),
        },
        "totals": {
            "terms": len(gloss["terms"]),
            "slots_total": sum(t["slots_total"] for t in per_term),
            "slots_by_handling": {h: by_handling.get(h, 0) for h in VALID_HANDLING},
        },
        "per_term": sorted(per_term, key=lambda t: -t["slots_total"]),
        "per_doc": [{"doc": k, "slots": v}
                    for k, v in sorted(per_doc.items(), key=lambda kv: -kv[1])],
    }
    return report


# ============================================================ 冻结校验
def check_frozen_consistency(report):
    """
    核对术语表哈希是否与上次 slot_report 记录的一致。
    不一致 → 术语表被改过，必须重跑槽位统计。
    """
    if not os.path.isfile(SLOT_REPORT_PATH):
        return True, None
    try:
        with open(SLOT_REPORT_PATH, encoding="utf-8") as f:
            old = json.load(f)
    except Exception:
        return True, None
    old_hash = old.get("glossary_hash")
    new_hash = report.get("glossary_hash")
    if old_hash and new_hash and old_hash != new_hash:
        return False, (f"术语表被改过（记录 {old_hash[:16]}… ≠ 当前 {new_hash[:16]}…），"
                       f"需重跑槽位统计")
    return True, None


# ============================================================ 任务 2：--verify 命中率
def load_translations():
    docs = {}
    if not os.path.isdir(TRANSLATED_DIR):
        return docs
    for fn in sorted(os.listdir(TRANSLATED_DIR)):
        if not fn.lower().endswith(".md"):
            continue
        with open(os.path.join(TRANSLATED_DIR, fn), "rb") as f:
            docs[os.path.splitext(fn)[0]] = f.read().decode("utf-8", "replace")
    return docs


def expected_tokens(term):
    """
    该术语在译文里"应当出现"的字符串集合。
    handling 决定期望形态：
      translate  → 中文译法
      keep_en    → 英文原形
      acronym    → 英文缩写
      bilingual  → 中文或「中文（英文）」都算命中
    """
    handling = term.get("handling")
    en, zh = term.get("en", ""), term.get("zh", "")
    if handling in ("keep_en", "acronym"):
        return [en]
    if handling == "bilingual":
        return [zh, f"{zh}（{en}）", f"{zh}({en})"]
    return [zh] if zh else [en]


def verify_doc(gloss, doc_id, orig, trans):
    """
    逐槽核对一个文档。
    ⚠️ 区分两种未命中：
       · 疑似整段漏译       → 单独归类
       · 其余               → 译法不一致
       不区分的话，整段漏译会污染术语命中率，让数字失去意义。

    漏译判据：正文词数比用【中文字符数 / 原文英文词数】衡量。
      · 中文比英文紧凑，归一化后正常译文约为原文英文词的 0.6~1.8 倍
      · 低于 30% ⇒ 大概率整段没翻（阈值保守，宁可漏判也不误伤正常译文）
    """
    orig_lines = content_lines(orig)
    trans_lines = content_lines(trans)
    orig_words = count_english_words(strip_front_matter(orig))
    trans_words = count_english_words(strip_front_matter(trans))
    trans_chars = len(re.sub(r"[A-Za-z0-9\s]", "", strip_front_matter(trans)))

    # 主判据：归一化后正文长度 / 原文英文词数
    char_ratio = (trans_chars / orig_words) if orig_words else 0.0
    # 参考判据：若译文仍以英文为主（未翻译），用英文词数比更直观
    word_ratio = (trans_words / orig_words) if orig_words else 0.0
    line_ratio = (len(trans_lines) / len(orig_lines)) if orig_lines else 0.0
    suspected_missing = char_ratio < MISSING_TRANSLATION_RATIO

    misses = []
    slots = hits = 0
    # ⚠️ 原文计数同样要屏蔽专名，否则与 build_slot_report 口径不一致，
    #    会出现「槽位数对不上」的假 miss（实测 MCP SDK README）。
    proper_pat = build_proper_name_re(
        gloss.get("proper_names") or DEFAULT_PROPER_NAMES)
    orig_masked = mask_proper_names("\n".join(orig_lines), proper_pat).split("\n")
    for t in gloss["terms"]:
        en = t["en"]
        n_orig, _ = find_slots(orig_masked, en, bool(t.get("case_sensitive")))
        if not n_orig:
            continue
        slots += n_orig
        expected = expected_tokens(t)
        n_hit = 0
        for tok in expected:
            if not tok:
                continue
            n_hit = max(n_hit, len(term_pattern(tok, False).findall(trans)))
        n_hit = min(n_hit, n_orig)
        hits += n_hit
        if n_hit < n_orig:
            found = []
            for wrong in guess_wrong_forms(t):
                if term_pattern(wrong, False).search(trans):
                    found.append(wrong)
            misses.append({
                "term": en,
                "slots": n_orig,
                "hits": n_hit,
                "found": found,
                "should": expected[0],
                "kind": "missing_translation" if suspected_missing else "inconsistent_term",
            })

    return {
        "doc": doc_id,
        "slots": slots,
        "hits": hits,
        "misses": misses,
        "suspected_missing_translation": suspected_missing,
        "line_ratio": round(line_ratio, 4),
        "word_ratio": round(word_ratio, 4),
        "char_ratio": round(char_ratio, 4),
    }


def guess_wrong_forms(term):
    """常见的错误译法（仅用于在 miss 里给出线索，不参与命中判定）"""
    en = term.get("en", "")
    zh = term.get("zh", "")
    table = {
        "agent": ["代理", "代理程序"],
        "agentic": ["代理的"],
        "context": ["语境", "环境"],
        "tool use": ["工具使用"],
        "code review": ["代码评审"],
        "pipeline": ["管道"],
        "artifact": ["工件"],
        "spec": ["规范"],
        "subagent": ["子代理"],
        "prompt": ["提示"],
        "incident": ["事故"],
        "context rot": ["上下文腐烂"],
        "grounding": ["接地"],
    }
    wrong = [w for w in table.get(en, []) if w and w != zh]
    return wrong


# ============================================================ ⚠️ 反例自测
SELFTEST_GLOSSARY = {
    "version": 1,
    "frozen": True,
    "frozen_hash": None,
    "policy": {"rules": []},
    "terms": [
        {"en": "agent", "zh": "智能体", "handling": "translate",
         "case_sensitive": False, "note": "", "occurrences": 0},
        {"en": "MCP", "zh": "MCP", "handling": "acronym",
         "case_sensitive": True, "note": "", "occurrences": 0},
        {"en": "reagent", "zh": "试剂", "handling": "translate",
         "case_sensitive": False, "note": "反例：不能被 agent 命中", "occurrences": 0},
    ],
}


def build_selftest_fixtures():
    """
    构造已知小样本：含正确译法、错误译法、代码块内干扰项。
    返回 (原文, 正确译文, 错误译文)
    """
    orig = "\n".join([
        "# Test doc",
        "",
        "The agent calls MCP tools.",
        "Every agent must be sandboxed before it runs.",
        "An agent can fail, so we log every agent decision.",
        "The team reviews each agent transcript weekly.",
        "",
        "<!-- CODE_BLOCK_START id=c1 lang=python -->",
        "```python",
        "agent = 'agent'   # 代码块内的 agent 不算槽位",
        "```",
        "<!-- CODE_BLOCK_END id=c1 -->",
        "",
        "A reagent is a chemical, not an agent.",
    ])
    good = "\n".join([
        "# 测试文档",
        "",
        "该智能体调用 MCP 工具。",
        "每个智能体运行前都必须放进沙箱。",
        "智能体会失败，所以我们记录每个智能体的决策。",
        "团队每周审查每个智能体的对话记录。",
        "",
        "<!-- CODE_BLOCK_START id=c1 lang=python -->",
        "```python",
        "agent = 'agent'",
        "```",
        "<!-- CODE_BLOCK_END id=c1 -->",
        "",
        "试剂是化学品，不是智能体。",
    ])
    bad = good.replace("该智能体调用", "该代理调用").replace(
        "每个智能体都必须", "每个代理都必须")
    return orig, good, bad


def run_selftest():
    """
    ⚠️ 一个失效的校验器比没有校验更危险 —— 它给出虚假的信心。
       实测踩过的坑：术语检查逻辑因 bug 被静默禁用，脚本仍报「全部通过」。
       所以这个自测【必须能真的失败】。
    """
    reconfigure_stdout()
    print("=" * 78)
    print("check_slots.py --selftest 反例自测")
    print("=" * 78)
    failures = []
    orig, good, bad = build_selftest_fixtures()
    gloss = dict(SELFTEST_GLOSSARY)

    # --- 断言 1：槽位统计正确。
    #     新样本正文 5 行里 agent 共 6 次（5 行各 1~2 次）；代码块内还有 2 次必须被忽略。
    lines = content_lines(orig)
    n_agent, _ = find_slots(lines, "agent", False)
    n_mcp, _ = find_slots(lines, "MCP", True)
    n_reagent, _ = find_slots(lines, "reagent", False)
    # 反证：不剥代码块时会数到几个（必须比正文多，用来证明"剥掉"确实起作用）
    raw_agent = len(term_pattern("agent").findall(strip_front_matter(orig)))
    print(f"\n  [1] 槽位统计：agent={n_agent}（保留代码块时会数到 {raw_agent}）"
          f" MCP={n_mcp} reagent={n_reagent}")
    if n_agent != 6:
        failures.append(f"agent 槽位应为 6，实际 {n_agent}"
                        f"（若为 8 说明代码块内容没被删掉；若为 5 说明词边界失效）")
    if raw_agent <= n_agent:
        failures.append(f"代码块剥离未生效：不剥代码块时也只有 {raw_agent} 个 agent")
    if n_mcp != 1:
        failures.append(f"MCP 槽位应为 1，实际 {n_mcp}")
    if n_reagent != 1:
        failures.append(f"reagent 槽位应为 1，实际 {n_reagent}")

    # --- 断言 2：词边界 —— "agent" 不得命中 "reagent"
    hit_in_reagent = term_pattern("agent").search("A reagent is a chemical")
    print(f"  [2] 词边界：agent 命中 'reagent' = {bool(hit_in_reagent)}（应为 False）")
    if hit_in_reagent:
        failures.append("词边界失效：'agent' 命中了 'reagent'")

    # --- 断言 3：代码块必须被跳过
    code_hits = [ln for ln in lines if "agent = 'agent'" in ln]
    print(f"  [3] 代码块跳过：残留代码行 = {len(code_hits)}（应为 0）")
    if code_hits:
        failures.append("代码块未被跳过，代码内的 agent 会被误计为槽位")

    # --- 断言 4：正确译文应判为通过（无 miss）
    r_good = verify_doc(gloss, "t", orig, good)
    print(f"  [4] 正确译文：slots={r_good['slots']} hits={r_good['hits']} "
          f"misses={len(r_good['misses'])}（misses 应为 0）")
    if r_good["misses"]:
        failures.append(f"正确译文被误报 {len(r_good['misses'])} 条 miss："
                        f"{[m['term'] for m in r_good['misses']]}")

    # --- 断言 5：错误译文必须被检出（这是自测的核心：能真的失败）
    r_bad = verify_doc(gloss, "t", orig, bad)
    hit_terms = [m["term"] for m in r_bad["misses"]]
    print(f"  [5] 错误译文：slots={r_bad['slots']} hits={r_bad['hits']} "
          f"检出的 miss 术语={hit_terms}（必须含 'agent'）")
    if "agent" not in hit_terms:
        failures.append("❌ 校验器失效：错误译文（把 agent 译成「代理」）没有被检出")
    else:
        m = [x for x in r_bad["misses"] if x["term"] == "agent"][0]
        print(f"        → agent: hits={m['hits']}/{m['slots']} "
              f"found={m['found']} should={m['should']}")
        if "代理" not in m["found"]:
            failures.append(f"miss 里没有给出错误译法线索，found={m['found']}")

    # --- 断言 6：疑似漏译要单独归类
    #     样本取"只翻了一句"的极短译文，长度比才会低于 30%
    # ⚠️ 样本必须真的"只剩一小段"，否则本来就不该判漏译：原文有 3 个正文行
    #    （开头句 / 代码块后空过 / 末行 reagent 句），所以译文只留 1 行才算漏译。
    short = "# 测试文档\n\n该智能体调用 MCP 工具。"
    r_short = verify_doc(gloss, "t", orig, short)
    print(f"  [6] 疑似漏译：line_ratio={r_short['line_ratio']} "
          f"char_ratio={r_short['char_ratio']} "
          f"suspected={r_short['suspected_missing_translation']}（应为 True）")
    if not r_short["suspected_missing_translation"]:
        failures.append("整段漏译没有被判为 suspected_missing_translation"
                        f"（line_ratio={r_short['line_ratio']}, "
                        f"char_ratio={r_short['char_ratio']}）")

    print("\n" + "=" * 78)
    if failures:
        print("❌ 自测失败：")
        for f in failures:
            print(f"   · {f}")
        print("=" * 78)
        return 1
    print("✅ 自测全部通过（能检出错误译法、能忽略代码块、能识别漏译）")
    print("=" * 78)
    return 0


# ============================================================ 主流程
def main(argv):
    reconfigure_stdout()
    if "--selftest" in argv:
        return run_selftest()
    # ---- 换源：从 argv 取路径参数并重设全局（必须在 load_glossary 之前）
    _opts = {}
    for _i, _a in enumerate(argv):
        if _a in PATH_FLAGS and _i + 1 < len(argv):
            _opts[PATH_FLAGS[_a][0]] = argv[_i + 1]
    if _opts:
        configure(**_opts)

    try:
        gloss = load_glossary()
    except FileNotFoundError as e:
        print(f"❌ {e}")
        return 1

    errs = validate_glossary(gloss)
    if errs:
        print("❌ 术语表校验失败：")
        for e in errs:
            print(f"   · {e}")
        return 1

    docs = load_originals()
    if not docs:
        print(f"❌ 没有找到原文：{EXTRACTED_DIR}")
        return 1

    if "--verify" in argv:
        return run_verify(gloss, docs)

    # ---------- 槽位统计
    report = build_slot_report(gloss, docs)

    # 冻结一致性检查
    # ⚠️ 术语表改过就必须重跑槽位统计，否则「命中率」可以靠改表来迁就译文，
    #    指标失去意义。--accept-glossary-change 是显式的「我知道表变了、
    #    接受并重算槽位」开关，不能默认放过。
    ok, msg = check_frozen_consistency(report)
    accept = "--accept-glossary-change" in argv
    if not ok and not accept:
        print(f"❌ {msg}")
        print("   如果确认术语表是有意修改的，请重跑："
              "python scripts/check_slots.py --accept-glossary-change")
        return 1
    if not ok and accept:
        print(f"⚠️  {msg}")
        print("   已按 --accept-glossary-change 接受改动并重算槽位；"
              "已翻译的内容需要重新校验。")

    os.makedirs(os.path.dirname(SLOT_REPORT_PATH), exist_ok=True)
    with open(SLOT_REPORT_PATH, "w", encoding="utf-8", newline="\n") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        f.write("\n")

    c = report["corpus"]
    t = report["totals"]
    print("=" * 78)
    print("check_slots.py —— 术语槽位统计（扫描【原文】）")
    print("=" * 78)

    print(f"\n【1】术语条数：{t['terms']}")
    for h in VALID_HANDLING:
        print(f"    {h:<10} {t['slots_by_handling'].get(h, 0):>6,} 槽位"
              f"   {sum(1 for x in gloss['terms'] if x.get('handling') == h):>4} 条")

    print(f"\n【2】槽位总数：{t['slots_total']:,}")
    print(f"    语料：{c['docs']} 个文档 / 正文英文词 {c['english_words_in_content']:,}")
    print(f"    行过滤：排除 {c['excluded_lines']:,} / {c['all_lines']:,} 行"
          f"（导航/链接/图片/空行/代码块）")

    print(f"\n【3】槽位最多的 10 个术语：")
    for x in report["per_term"][:10]:
        print(f"    {x['slots_total']:>6,}  {x['en']:<26} → {x['zh']}  [{x['handling']}]")

    zero = [x for x in report["per_term"] if x["slots_total"] == 0]
    print(f"\n【4】零槽位术语：{len(zero)} 条（术语表里有但原文没出现 → 可能多余，需人工确认）")
    for x in zero:
        print(f"    {x['en']:<26} → {x['zh']}  [{x['handling']}]")

    print(f"\n【6】冻结哈希：{report['glossary_hash'][:32]}…"
          f"（frozen={report['glossary_frozen']}）")
    if not report["glossary_frozen"]:
        print("    ⚠️ 术语表尚未冻结（frozen=false）。定稿后请设 frozen=true 并重跑本步。")

    print("\n" + "=" * 78)
    print(f"已写出：{SLOT_REPORT_PATH}")
    print("=" * 78)
    return 0


def run_verify(gloss, docs):
    trans = load_translations()
    if not trans:
        print(f"❌ 没有找到译文：{TRANSLATED_DIR}")
        return 1

    results = []
    tot_slots = tot_hits = 0
    n_missing = 0        # 有译文但疑似整段漏译
    n_not_translated = 0  # 尚未翻译（不算漏译，避免噪声）
    for doc_id, d in docs.items():
        if doc_id not in trans:
            # ⚠️ 「还没译」不等于「漏译」。分开计数，
            #    否则 52 篇未译文档会把「疑似漏译」这个指标淹掉。
            n_not_translated += 1
            continue
        r = verify_doc(gloss, doc_id, d["text"], trans[doc_id])
        if r["suspected_missing_translation"]:
            n_missing += 1
        tot_slots += r["slots"]
        tot_hits += r["hits"]
        results.append(r)

    rate = (tot_hits / tot_slots) if tot_slots else 0.0
    out = {
        "generated_by": "check_slots.py --verify",
        "glossary_hash": glossary_hash(gloss),
        "totals": {
            "docs": len(results),
            "slots": tot_slots,
            "hits": tot_hits,
            "hit_rate": round(rate, 4),
            "docs_suspected_missing_translation": n_missing,
            "docs_not_translated_yet": n_not_translated,
        },
        "per_doc": results,
        "conflict_check": {"passed": rate >= 0.98},
    }
    # 保险：报告目录可能尚未创建（全新检出时）
    os.makedirs(os.path.dirname(VERIFY_REPORT_PATH), exist_ok=True)
    with open(VERIFY_REPORT_PATH, "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print("=" * 78)
    print("check_slots.py --verify —— 术语命中率核对（按文档）")
    print("=" * 78)
    print(f"\n  已核对文档 {len(results)} 篇（另有 {n_not_translated} 篇尚未翻译）")
    print(f"  槽位 {tot_slots:,}   命中 {tot_hits:,}   命中率 {rate*100:.2f}%")
    print(f"  疑似整段漏译的文档：{n_missing} 个")
    bad = [r for r in results if r.get("misses")]
    if bad:
        print(f"\n  未命中明细（{len(bad)} 个文档）：")
        for r in bad[:15]:
            kinds = collections.Counter(m["kind"] for m in r["misses"])
            print(f"    {r['doc']:<44} slots={r['slots']:<5} hits={r['hits']:<5} "
                  f"{dict(kinds)}")
            for m in r["misses"][:3]:
                print(f"        · {m['term']}: {m['hits']}/{m['slots']} 槽位命中，"
                      f"出现错误译法 {m['found']}，应为「{m['should']}」"
                      f" [{m['kind']}]")
    else:
        print("\n  ✅ 所有文档术语命中率 100%")
    print("\n" + "=" * 78)
    print(f"已写出：{VERIFY_REPORT_PATH}")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
