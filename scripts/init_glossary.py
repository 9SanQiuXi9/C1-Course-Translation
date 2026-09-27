#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
init_glossary.py —— 管线 ③-a 术语表初始化（从语料自动抽候选术语）

作用
    扫描 extracted/*.md 的【正文】，自动抽取候选术语并按频次排序，
    输出初始 glossary.json。**绝不手工"种下"术语**：
    交付要求「所有数字来自脚本、可复跑」，手写的术语表无法复现。

两层价值（与 check_slots.py 配合）
    第一层：给人看的参考表 —— 规定每个术语只能怎么翻
    第二层：可自动校验的合同 —— 槽位数由扫描【原文】得出，翻完逐槽核对

用法
    python scripts/init_glossary.py                     # 抽取候选并写 glossary.json
    python scripts/init_glossary.py --top 180           # 候选数量（默认 180）
    python scripts/init_glossary.py --report            # 只打印候选，不写文件
"""

import collections
import hashlib
import json
import os
import re
import sys
import zlib  # noqa: F401  (仅占位，保持标准库自检)

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
GLOSSARY_NAME = "glossary.json"
GLOSSARY_MD_NAME = "glossary.md"

EXTRACTED_DIR = os.path.join(BASE_DIR, "work", "extracted")
GLOSSARY_PATH = os.path.join(BASE_DIR, "work", "glossary", "glossary.json")
GLOSSARY_MD_PATH = os.path.join(BASE_DIR, "work", "glossary", "glossary.md")


def configure(extracted_dir=None, glossary=None, glossary_md=None):
    """
    按命令行参数重设路径全局变量（换源复用）。
    ⚠️ 下游函数直接读这些模块级常量，所以必须在这里一次性重设。
    """
    global EXTRACTED_DIR, GLOSSARY_PATH, GLOSSARY_MD_PATH
    if extracted_dir:
        EXTRACTED_DIR = os.path.abspath(extracted_dir)
    if glossary:
        GLOSSARY_PATH = os.path.abspath(glossary)
        # md 报告默认跟着 glossary.json 走同一目录，避免两者错位
        if not glossary_md:
            GLOSSARY_MD_PATH = os.path.join(os.path.dirname(GLOSSARY_PATH),
                                            "glossary.md")
    if glossary_md:
        GLOSSARY_MD_PATH = os.path.abspath(glossary_md)


PATH_USAGE = """换源相关参数：
  --extracted-dir DIR   抽取产出目录（默认 work/extracted）
  --glossary PATH       术语表 JSON 输出路径（默认 work/glossary/glossary.json）
  --glossary-md PATH    术语表 Markdown 输出路径（默认与 JSON 同目录）

从新语料建表（换到别的领域时用）：
  --from-corpus-only    不带种子，纯从当前语料抽候选建表（别名 --no-seed）
                        ⚠️ 必须配合 --max-terms N；产出的表 frozen=false（草稿态）
  --max-terms N         术语条数上限（默认 0 = 只用硬编码定稿术语）
  --top N               候选池大小（默认 180）
"""

GLOSSARY_VERSION = 1
DEFAULT_TOP = 180

# 专有名词保护：这些是多词专名，不应被拆开算作独立术语槽位。
# ⚠️ 实测 The Model Context Protocol (MCP) 里的 model / context
#    会被当成独立术语，导致假 miss。声明在此，校验时整段屏蔽。
# ⚠️ 这是【本项目领域】的专名表。换到别的领域时用 --from-corpus-only
#    会把整张表置空 —— 旧领域的专名对新语料全是假阳性。
PROPER_NAMES = [
    "Model Context Protocol",
    "Context Protocol",
    "Pull Request",
    "Chain of Thought",
    "Vibe Coding",
    "Agentic Development Environment",
    "Site Reliability Engineering",
]
# 术语表规模上限：80~100 条为宜 —— 太短覆盖不住，太长人工根本复查不完。
# ⚠️ 默认 0 = 只保留人工定稿的 CURATED，【不自动回填】候选。
#    原因：自动候选里槽位最高的全是 code/ai/data 这类通用英文词（code 达 912 槽位），
#    它们不是术语却会把槽位总数抬高数倍，稀释指标意义；
#    而且删一条定稿术语后它会立刻回填空位，让"人工复查过的表"与产物不一致。
#    需要看候选清单时显式传 --max-terms N。
DEFAULT_MAX_TERMS = 0

# ============================================================ 非正文行判定
# 与 check_slots.py 保持完全一致：两边口径不同会导致槽位数对不上
LINKY_RE = re.compile(r"https?://|www\.|\.com/|\.ai/|\.dev/|\.ai\b|cdn-cgi|next/image|@")

STOPWORDS = set("""
a an the and or but if then else when while for with without within into onto from to of in on at by
as is are was were be been being do does did done have has had having will would shall should can could
may might must this that these those it its they them their there here you your yours we our ours i me my
he she his her him not no nor so than too very just also only such other another each both few more most
some any all every own same s t don now what which who whom whose how why where about above after again
against before below between during through under until up down out off over once because both d ll m o
re ve y ain aren couldn didn doesn hadn hasn haven isn ma mightn mustn needn shan shouldn wasn weren won
wouldn page site click read learn more new get start try free sign log home menu search next previous
""".split())

# 已知的"必须收录"术语（课程语境关键 + 易翻错）
SEED_TERMS = [
    "MCP", "agent", "agentic", "context", "context window", "context engineering",
    "prompt", "prompt engineering", "code review", "pull request", "repository",
    "commit", "refactor", "token", "hallucination", "inference", "fine-tuning",
    "embedding", "RAG", "guardrail", "observability", "debugging", "deployment",
    "pipeline", "subagent", "orchestration", "sandbox", "chain of thought",
    "reasoning", "benchmark", "latency", "throughput", "tool use", "tool calling",
    "scaffolding", "vibe coding", "workflow", "automation", "artifact", "template",
    "cache", "server", "client", "API", "tool", "model", "security", "evaluation",
    "prompt injection", "context rot", "spec", "AI-native", "on-call", "SRE",
    "DAST", "SAST", "LLM", "IDE", "PR", "CI/CD", "coding agent", "eval",
    "alignment", "transformer", "training", "dataset", "grounding", "retrieval",
    "vector database", "human-in-the-loop", "threat model", "vulnerability",
    "exploit", "static analysis", "compliance", "rollout", "canary", "incident",
    "postmortem", "SLA", "SLO", "uptime", "monitoring", "tracing", "span",
    "annotation", "machine learning", "deep learning", "neural network",
    "message passing", "agent loop", "code review agent",
]


# ============================================================ 正文提取与清洗
def reconfigure_stdout():
    """Windows GBK 控制台：打印中文/emoji 前必须把 stdout 设成 UTF-8"""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def strip_front_matter(text):
    """去掉 YAML front matter（--- 包裹的头部）"""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end >= 0:
            return text[end + 4:]
    return text


def strip_code_blocks(text):
    """
    去掉代码块。
    ⚠️ 代码与数据不译，代码里的 agent/MCP 不算槽位。
       抽取阶段用 <!-- CODE_BLOCK_START id=cN lang=xxx --> ... _END 包裹。
    """
    return re.sub(r"<!--\s*CODE_BLOCK_START.*?CODE_BLOCK_END\s*-->", " ", text,
                  flags=re.S)


def is_content_line(line):
    """
    判定是否【正文行】。
    ⚠️ 必须先排除导航/页脚/链接行/图片行再统计，否则槽位数虚高：
       实测 extracted/ 残留大量网页导航，英文词总数从真实约 76,000
       膨胀到 131,375（+72%）；槽位虚高会让"命中率"永远到不了 100%，
       指标直接失去意义。
    """
    s = line.strip()
    if not s:
        return False
    if s.startswith("!["):                       # 图片行
        return False
    if s.startswith("<!--"):                     # 抽取阶段插入的标记
        return False
    if LINKY_RE.search(s):                       # 含 URL / 邮箱 → 整行非正文
        return False
    if s.startswith("-") and s.count("](") >= 1:  # 列表项主要是链接
        return False
    return True


def content_text(text):
    """正文文本：去 front matter → 去代码块 → 只留正文行"""
    t = strip_code_blocks(strip_front_matter(text))
    return "\n".join(ln for ln in t.split("\n") if is_content_line(ln))


def load_corpus():
    """读 extracted/*.md，返回 {doc_id: 正文文本}"""
    docs = {}
    if not os.path.isdir(EXTRACTED_DIR):
        return docs
    for fn in sorted(os.listdir(EXTRACTED_DIR)):
        if not fn.lower().endswith(".md"):
            continue
        path = os.path.join(EXTRACTED_DIR, fn)
        with open(path, "rb") as f:
            raw = f.read().decode("utf-8", "replace")
        docs[os.path.splitext(fn)[0]] = content_text(raw)
    return docs


def count_english_words(text):
    return len(re.findall(r"[A-Za-z]{2,}", text))


# ============================================================ 候选术语抽取
def candidate_phrases(text, max_n=3):
    """
    抽取 1~3 词的候选名词短语。

    ⚠️ 实现方式：先切词元、再用滑动窗口拼 n-gram。
       【不要】用一个含嵌套量词的大正则去匹配所有 n-gram ——
       拼出来的模式（token 内部已有 * ，外面再套 \\s+ 重复）会让 re 在
       8 万词语料上回溯爆炸，实测跑 10 分钟不结束，且先报 multiple repeat。

    只保留：
      · 全大写缩写（MCP / API / SAST）
      · 含 - 或 / 的技术写法（AI-native / CI/CD / fine-tuning）
      · 出现次数 >= 2 的普通短语
    """
    token_re = re.compile(r"[A-Za-z][A-Za-z0-9]*(?:[\-\/\.\+][A-Za-z0-9]+)*")
    counter = collections.Counter()
    for line in text.split("\n"):
        tokens = token_re.findall(line)
        if not tokens:
            continue
        for n in range(1, max_n + 1):
            for i in range(len(tokens) - n + 1):
                parts = tokens[i:i + n]
                low = " ".join(parts).lower()
                if n == 1:
                    if low in STOPWORDS or len(low) < 2:
                        continue
                else:
                    pl = [p.lower() for p in parts]
                    if pl[0] in STOPWORDS or pl[-1] in STOPWORDS:
                        continue
                counter[low] += 1
    return counter


def rank_candidates(counter, top=DEFAULT_TOP):
    """按频次排序，优先保留缩写与技术术语"""
    def score(item):
        phrase, n = item
        bonus = 0
        if re.fullmatch(r"[a-z]{2,}", phrase) is None and phrase.upper() == phrase and len(phrase) >= 2:
            bonus += 2                       # 全大写缩写
        if "-" in phrase or "/" in phrase:
            bonus += 1
        if phrase in [s.lower() for s in SEED_TERMS]:
            bonus += 5                       # 种子术语优先
        if " " in phrase:
            bonus += 1                       # 多词短语更像术语
        return (n + bonus, phrase)

    ranked = sorted(counter.items(), key=score, reverse=True)
    return ranked[:top]


# ============================================================ 初始术语表
# 人工定稿的译法（这一步是人工的，允许）。键为小写英文，值为 (中文, handling, note)
CURATED = {
    "mcp": ("MCP", "acronym", "Model Context Protocol，课程核心概念；中文正文保留缩写，首次出现给全称"),
    "agent": ("智能体", "translate", "指 AI 智能体，非法律意义的「代理人」，也避免与「代理服务器」混淆"),
    "agentic": ("智能体式", "translate", "形容词，整体译「智能体式」。⚠️ 固定搭配 Agentic AI / agentic workflow / agentic system 一律译「智能体式 AI／智能体式工作流／智能体式系统」；不要用「智能体的 AI」这种别扭说法"),
    "context": ("上下文", "translate", "业内通行译法"),
    "context window": ("上下文窗口", "translate", "指模型单次可处理的 token 上限"),
    "context engineering": ("上下文工程", "translate", "与 prompt engineering 区分：前者管喂什么，后者管怎么说"),
    "prompt": ("提示词", "translate", "不译「提示」，避免与 UI 提示混淆"),
    "prompt engineering": ("提示词工程", "translate", "行业已通用"),
    "code review": ("代码审查", "translate", "不译「代码评审」，与 GitHub/GitLab 界面一致"),
    "pull request": ("拉取请求", "bilingual", "首次出现「拉取请求（Pull Request）」，之后用中文；PR 见 PR 条"),
    "repository": ("仓库", "translate", "代码仓库"),
    "commit": ("提交", "translate", "仅指版本控制义的「提交」（名词/动词）。⚠️ 三种例外不要套用：① 复合词 pre-commit、commit message 等工具名/固定名保留英文；② commit to doing sth 意为「投入/下决心做」，与版本控制无关；③ commit 出现在代码示例或 URL 中不译"),
    "refactor": ("重构", "translate", ""),
    "token": ("token", "keep_en", "计费/上下文计量单位，中文无通用对译，保留英文"),
    "hallucination": ("幻觉", "translate", "模型编造事实"),
    "inference": ("推理", "translate", "指模型前向计算；注意与 reasoning（推理能力）区分，见 reasoning 条"),
    "fine-tuning": ("微调", "translate", ""),
    "embedding": ("嵌入", "translate", "向量嵌入"),
    "rag": ("RAG", "acronym", "Retrieval-Augmented Generation，保留缩写"),
    "guardrail": ("护栏", "translate", "AI 安全护栏"),
    "observability": ("可观测性", "translate", ""),
    "debugging": ("调试", "translate", ""),
    "deployment": ("部署", "translate", ""),
    "pipeline": ("流水线", "translate", "不译「管道」"),
    "subagent": ("子智能体", "translate", "与 agent 保持同词根，避免「子代理」"),
    "orchestration": ("编排", "translate", "多智能体编排"),
    "sandbox": ("沙箱", "translate", ""),
    "chain of thought": ("思维链", "translate", "CoT，保留中文"),
    "reasoning": ("推理", "translate", "指模型的推理过程/推理环节。⚠️ 只有语境明确指「模型的推理能力」时才用「推理能力」，避免把通用的理性思考过程误译成「推理能力」"),
    "benchmark": ("基准测试", "translate", ""),
    "latency": ("延迟", "translate", ""),
    "tool use": ("工具调用", "translate", "不译「工具使用」"),
    "scaffolding": ("脚手架", "translate", "指围绕模型的工程支撑代码"),
    "vibe coding": ("vibe coding", "keep_en", "课程专有说法，中文无稳定对译，保留英文原形"),
    "workflow": ("工作流", "translate", ""),
    "automation": ("自动化", "translate", ""),
    "artifact": ("产物", "translate", "指流程产出的文件/交付物，不译「工件」"),
    "template": ("模板", "translate", ""),
    "server": ("服务器", "translate", ""),
    "client": ("客户端", "translate", ""),
    "api": ("API", "acronym", "Application Programming Interface，保留缩写"),
    "tool": ("工具", "translate", ""),
    "model": ("模型", "translate", ""),
    "security": ("安全", "translate", ""),
    "evaluation": ("评估", "translate", ""),
    "eval": ("评估", "translate", "evaluation 的简称，统一译为「评估」"),
    "prompt injection": ("提示词注入", "translate", "安全议题，不译「提示注入」"),
    "context rot": ("上下文腐化", "translate", "Chroma 研究提出的现象，指长上下文质量退化"),
    "spec": ("规格", "translate", "不译「规范」；specs-are-the-new-source-code 语境指规格文档"),
    "ai-native": ("AI 原生", "translate", "保留 AI 前缀，native 译「原生」"),
    "on-call": ("值班", "translate", "SRE 语境"),
    "sre": ("SRE", "acronym", "Site Reliability Engineering，保留缩写"),
    "dast": ("DAST", "acronym", "Dynamic Application Security Testing，保留缩写"),
    "sast": ("SAST", "acronym", "Static Application Security Testing，保留缩写"),
    "llm": ("LLM", "acronym", "Large Language Model，保留缩写"),
    "ide": ("IDE", "acronym", "Integrated Development Environment，保留缩写"),
    "pr": ("PR", "acronym", "Pull Request 的缩写，与 pull request 条并存"),
    "ci/cd": ("CI/CD", "acronym", "持续集成/持续交付，保留缩写"),
    "coding agent": ("编码智能体", "translate", "与 agent 同词根"),
    "alignment": ("对齐", "translate", "AI 对齐"),
    "transformer": ("Transformer", "keep_en", "架构名，业界普遍保留英文"),
    "training": ("训练", "translate", ""),
    "dataset": ("数据集", "translate", ""),
    "grounding": ("接地", "translate", "指用外部事实约束模型输出；也可译「事实锚定」"),
    "retrieval": ("检索", "translate", ""),
    "vector database": ("向量数据库", "translate", ""),
    "human-in-the-loop": ("人在回路", "translate", "行业通行译法"),
    "threat model": ("威胁模型", "translate", ""),
    "vulnerability": ("漏洞", "translate", ""),
    "exploit": ("漏洞利用", "translate", "名词指利用手段；⚠️ 动词义（利用某个漏洞）也用「漏洞利用」保持术语一致，不要写成「利用」"),
    "static analysis": ("静态分析", "translate", ""),
    "compliance": ("合规", "translate", ""),
    "rollout": ("灰度发布", "translate", "渐进式发布；语料仅 1 次，注意上下文"),
    "incident": ("故障事件", "translate", "SRE 语境，不译「事故」"),
    "postmortem": ("事后复盘", "translate", "SRE 语境"),
    "sla": ("SLA", "acronym", "Service Level Agreement，保留缩写；语料未出现"),
    "slo": ("SLO", "acronym", "Service Level Objective，保留缩写；语料未出现"),
    "monitoring": ("监控", "translate", ""),
    "tracing": ("链路追踪", "translate", "可观测性三支柱之一"),
    "span": ("跨度", "translate", "分布式追踪的最小单元；也可保留 span"),
    "annotation": ("标注", "translate", ""),
    "machine learning": ("机器学习", "translate", ""),
    "deep learning": ("深度学习", "translate", ""),
    "context rot": ("上下文腐化", "translate", "Chroma 研究提出的现象：长上下文质量退化"),
    "best practices": ("最佳实践", "translate", "多词短语，非通用词"),
    "technical debt": ("技术债", "translate", ""),
    "unit test": ("单元测试", "translate", ""),
    "test coverage": ("测试覆盖率", "translate", ""),
    "codebase": ("代码库", "translate", ""),
    "root cause": ("根因", "translate", "故障分析语境"),
    "incident response": ("故障响应", "translate", ""),
    "feature flag": ("功能开关", "translate", ""),
    "privacy": ("隐私", "translate", ""),
    "injection": ("注入", "translate", "安全语境"),
    "autonomy": ("自主性", "translate", ""),
    "non-deterministic": ("非确定性", "translate", "指模型输出不可复现"),
    "multimodal": ("多模态", "translate", ""),
    "zero-shot": ("零样本", "translate", ""),
    "few-shot": ("少样本", "translate", ""),
    "system prompt": ("系统提示词", "translate", "与 prompt 保持同词根"),
}


def build_glossary(docs, top=DEFAULT_TOP, max_terms=DEFAULT_MAX_TERMS,
                   curated=None, proper_names=None):
    """
    组装 glossary.json：
      · 优先收录 curated 里人工定稿的译法
      · 再从语料自动候选里补足到 max_terms（未定稿的标 keep_en，待人工确认）

    ⚠️ 自动候选里绝大多数是 code / ai / build / use 这类【通用英文词】，
       它们不是术语。所以默认只把候选补到 max_terms 上限，
       不靠启发式硬判「是不是术语」——那会引入噪声，宁可少收。

    ⚠️ curated / proper_names 做成参数（而不是直接读全局），是为了支持
       「不带种子、纯从新语料建表」的换源场景：
         · 换到完全不同的领域时，旧领域的定稿术语对新语料是 100% 的
           「零槽位噪声」（实测水培语料：99 条里 98 条零槽位）
         · 旧领域的专名表同样全是假阳性
       默认值仍是本项目的 CURATED，所以原有行为一字不变。
    """
    if curated is None:
        curated = CURATED
    if proper_names is None:
        proper_names = PROPER_NAMES

    counter = collections.Counter()
    for text in docs.values():
        counter.update(candidate_phrases(text))

    ranked = rank_candidates(counter, top=max(top, max_terms))

    terms = []
    seen = set()

    # ① 人工定稿的术语（按语料频次排序，高频在前）
    #    curated 为空时这一段整体跳过 —— 这就是「无种子模式」
    for en_lower, (zh, handling, note) in sorted(
            curated.items(), key=lambda kv: -counter.get(kv[0], 0)):
        occurrences = counter.get(en_lower, 0)
        terms.append({
            "en": en_lower,
            "zh": zh,
            "handling": handling,
            "case_sensitive": en_lower.upper() == en_lower and len(en_lower) <= 6,
            "note": note,
            "occurrences": occurrences,
            # ⚠️ 必须显式记录来源：有 40 条定稿术语的 note 是空字符串，
            #    靠「note 非空」判定定稿会把它们漏算，统计口径会自相矛盾
            #    （实测出现"头部写定稿 60 / 但总数 100"这种自打嘴巴的输出）。
            "source": "curated",
        })
        seen.add(en_lower)

    # ② 自动候选补足到上限
    # ⚠️ max_terms<=0 表示"只保留人工定稿，不自动回填"。
    #    这不是可有可无的开关：删掉一条定稿术语后，自动候选会立刻把
    #    空位填成通用词（实测填回 code，912 槽位），导致
    #    「人工复查通过的那份表」与最终产物不是同一份。
    # ⚠️ 无种子模式下若 max_terms<=0，会产出一张空表 —— 由调用方拒绝并提示。
    if max_terms > 0:
        for phrase, _n in ranked:
            if len(terms) >= max_terms:
                break
            if phrase in seen or phrase in STOPWORDS or len(phrase) < 2:
                continue
            terms.append({
                "en": phrase,
                "zh": phrase,
                "handling": "keep_en",
                "case_sensitive": False,
                "note": "自动候选，待人工定稿（当前按保留英文处理）",
                "occurrences": counter.get(phrase, 0),
                "source": "auto_candidate",
            })
            seen.add(phrase)

    # ⚠️ 冻结条件：只有含人工定稿术语时才冻结。
    #    纯自动候选的表是【草稿】，标 frozen=False 如实反映
    #    「这张表还没被人复查过」，避免下游把它当成已定稿口径。
    has_curated = any(t["source"] == "curated" for t in terms)
    gloss = {
        "version": GLOSSARY_VERSION,
        # CURATED 即「人工定稿」这一步的产物，所以直接冻结：
        # 冻结后任何改动都会改变 frozen_hash，check_slots.py 会拒绝沿用旧槽位。
        "frozen": has_curated,
        "frozen_hash": None,
        "policy": {
            "rules": [
                "同一术语在任何文件中必须使用同一译法",
                "术语表冻结后如需修改，必须重新全量校验",
                "保留英文的术语，中文正文中直接使用英文原形",
            ]
        },
        "terms": terms,
        # 专有名词保护：这些是多词专名，不应被拆开算作独立术语槽位。
        # ⚠️ 实测 The Model Context Protocol (MCP) 里的 model / context
        #    会被当成独立术语，导致假 miss。声明在此，校验时整段屏蔽。
        # ⚠️ 无种子模式下留空：旧领域的专名对新语料全是假阳性。
        "proper_names": list(proper_names),
    }
    gloss["frozen_hash"] = compute_frozen_hash(gloss)
    return gloss


def compute_frozen_hash(gloss):
    """
    计算冻结哈希。
    ⚠️ 必须【排除 frozen_hash 字段自身】再算，否则循环依赖：
       哈希取决于内容，而内容里又含哈希值。
    """
    payload = {k: v for k, v in gloss.items() if k != "frozen_hash"}
    blob = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def write_glossary_md(gloss, path=None):
    # ⚠️ 默认值不能用 GLOSSARY_MD_PATH —— 那样在 import 时就绑死了，
    #    configure() 之后改全局不影响它。这里实时读取。
    if path is None:
        path = GLOSSARY_MD_PATH
    """
    输出人工复查用的 glossary.md。
    设计要点：按【人工定稿状态】分区，把「需要人看」的排在最前面；
    未定稿条目在表格里明确标注，避免复查时误当成已定稿的规则。
    """
    terms = gloss["terms"]
    # ⚠️ 用显式 source 字段分区，不要用「note 是否为空」——
    #    40 条定稿术语的 note 本来就是空的，按 note 判会漏算，
    #    导致头部统计与总数自相矛盾。
    curated = [t for t in terms if t.get("source") == "curated"]
    auto = [t for t in terms if t.get("source") != "curated"]
    handling_zh = {
        "translate": "翻成中文",
        "keep_en": "保留英文",
        "bilingual": "首次双语",
        "acronym": "保留缩写",
    }

    L = []
    L.append("# 术语表（glossary）")
    L.append("")
    L.append(f"- 版本：`{gloss['version']}`　冻结："
             f"`{'是' if gloss['frozen'] else '否'}`")
    L.append(f"- 冻结哈希：`{gloss['frozen_hash']}`")
    L.append(f"- 条目：**{len(terms)}** 条"
             f"（人工定稿 {len(curated)} / 自动候选待定 {len(auto)}）")
    L.append("")
    L.append("> ⚠️ 本文件由 `scripts/init_glossary.py` 生成，**请勿手改**。")
    L.append("> 要改术语请改脚本里的 `CURATED` 字典后重跑，"
             "这样数字才可复现；手改会导致冻结哈希对不上、槽位校验拒绝沿用。")
    L.append("")
    L.append("## 定稿规则（policy）")
    L.append("")
    for r in gloss["policy"]["rules"]:
        L.append(f"1. {r}")
    L.append("")
    L.append("## handling 取值说明")
    L.append("")
    L.append("| handling | 含义 |")
    L.append("|---|---|")
    for k in ("translate", "keep_en", "bilingual", "acronym"):
        L.append(f"| `{k}` | {handling_zh[k]} |")
    L.append("")

    def table(rows, title, note_text):
        L.append(f"## {title}")
        L.append("")
        if note_text:
            L.append(note_text)
            L.append("")
        L.append("| # | 英文 | 中文 | handling | 大小写敏感 | 语料出现 | 备注 |")
        L.append("|---|---|---|---|---|---|---|")
        for i, t in enumerate(rows, 1):
            note = (t.get("note") or "").replace("|", "\\|")
            L.append(f"| {i} | `{t['en']}` | {t['zh']} | `{t['handling']}` | "
                     f"{'是' if t.get('case_sensitive') else '否'} | "
                     f"{t.get('occurrences', 0)} | {note} |")
        L.append("")

    table(sorted(curated, key=lambda t: -t.get("occurrences", 0)),
          f"一、人工定稿（{len(curated)} 条）—— 可直接执行",
          "这些是已定稿的硬规则，翻译时**必须**按表中译法，不得自由选择。")

    table(sorted(auto, key=lambda t: -t.get("occurrences", 0)),
          f"二、自动候选待人工定稿（{len(auto)} 条）",
          "以下由语料自动抽取，**尚未定稿**。多为通用英文词或低频词，"
          "请人工判断：确属术语的补上中文译法；明显是通用词的请**删除**。")

    zero = [t for t in terms if t.get("occurrences", 0) == 0]
    L.append(f"## 三、零槽位条目（{len(zero)} 条）—— 语料中未出现，请确认是否删除")
    L.append("")
    if zero:
        L.append("| # | 英文 | 中文 | handling | 备注 |")
        L.append("|---|---|---|---|---|")
        for i, t in enumerate(zero, 1):
            L.append(f"| {i} | `{t['en']}` | {t['zh']} | `{t['handling']}` | "
                     f"{(t.get('note') or '').replace('|', chr(92) + '|')} |")
    else:
        L.append("（无）")
    L.append("")
    L.append("---")
    L.append("")
    L.append("复查完成后：确认无误 → 保持 `frozen=true` 并重跑 "
             "`python scripts/init_glossary.py && python scripts/check_slots.py`；"
             "如需修改译法 → 改脚本 `CURATED` 后重跑全流程。")
    L.append("")

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L))
    return path


def main(argv):
    reconfigure_stdout()
    # ---- 换源相关参数（见 PATH_USAGE）
    if "-h" in argv or "--help" in argv:
        print("init_glossary.py —— 术语表初始化")
        print()
        print(PATH_USAGE)
        print("其它参数：--md（同时写 Markdown）--report --top N --max-terms N")
        return 0
    path_opts = {}
    for key, flag in (("extracted_dir", "--extracted-dir"),
                      ("glossary", "--glossary"),
                      ("glossary_md", "--glossary-md")):
        if flag in argv:
            i = argv.index(flag)
            if i + 1 >= len(argv):
                print(f"❌ {flag} 后面要跟一个值")
                return 64
            path_opts[key] = argv[i + 1]
    if path_opts:
        configure(**path_opts)

    do_report = "--report" in argv
    do_md = "--md" in argv
    # ⚠️ --from-corpus-only：不带种子，纯从当前语料建表。
    #    换到别的领域时必须用它 —— 否则旧领域的定稿术语会全部变成
    #    「零槽位噪声」（实测水培语料：99 条里 98 条零槽位）。
    from_corpus_only = ("--from-corpus-only" in argv
                        or "--no-seed" in argv)
    top = DEFAULT_TOP
    max_terms = DEFAULT_MAX_TERMS
    for i, a in enumerate(argv):
        if a == "--top" and i + 1 < len(argv):
            top = int(argv[i + 1])
        if a == "--max-terms" and i + 1 < len(argv):
            max_terms = int(argv[i + 1])

    if from_corpus_only and max_terms <= 0:
        print("❌ --from-corpus-only 必须配合 --max-terms N")
        print("   理由：无种子模式下 max-terms=0 会产出一张空表，没有意义。")
        print("   建议：--from-corpus-only --max-terms 120")
        return 64

    docs = load_corpus()
    if not docs:
        print(f"❌ 没有找到语料：{EXTRACTED_DIR}")
        return 1

    total_words = sum(count_english_words(t) for t in docs.values())
    print("=" * 78)
    print("init_glossary.py —— 术语表初始化（从语料自动抽候选）")
    print("=" * 78)
    print(f"  语料：{len(docs)} 个文档，清洗后正文 {total_words:,} 英文词")
    print(f"  （已排除 front matter、代码块、导航/链接/图片行）")

    # 无种子模式：curated 置空、专名表置空，全部从当前语料抽
    if from_corpus_only:
        gloss = build_glossary(docs, top=top, max_terms=max_terms,
                               curated={}, proper_names=[])
    else:
        gloss = build_glossary(docs, top=top, max_terms=max_terms)
    terms = gloss["terms"]
    by_handling = collections.Counter(t["handling"] for t in terms)

    if from_corpus_only:
        print(f"\n  ⚠️ 无种子模式（--from-corpus-only）：未使用任何硬编码定稿术语，")
        print(f"     全部 {len(terms)} 条均为从当前语料自动抽取的候选，")
        print(f"     frozen={gloss['frozen']}（草稿态，需人工定稿后再冻结）。")

    print(f"\n  术语条数：{len(terms)}")
    for h in ("translate", "keep_en", "bilingual", "acronym"):
        print(f"    {h:<10} {by_handling.get(h, 0):>4}")
    zero = [t["en"] for t in terms if t["occurrences"] == 0]
    print(f"  零槽位术语：{len(zero)} 条（术语表里有但原文没出现，需人工确认是否多余）")
    if zero:
        print(f"    {', '.join(zero[:20])}{' ...' if len(zero) > 20 else ''}")

    if do_report:
        print("\n  --report 模式：只打印，不写文件。")
        return 0

    os.makedirs(os.path.dirname(GLOSSARY_PATH), exist_ok=True)
    with open(GLOSSARY_PATH, "w", encoding="utf-8", newline="\n") as f:
        json.dump(gloss, f, ensure_ascii=False, indent=2)
        f.write("\n")
    md_path = write_glossary_md(gloss)
    print(f"\n  已写出：{GLOSSARY_PATH}")
    print(f"  已写出：{md_path}   ← 人工复查用")
    print(f"  冻结哈希：{gloss['frozen_hash'][:16]}…（frozen={gloss['frozen']}）")
    print("\n  下一步：人工复查 glossary.md；如需改译法，改脚本 CURATED 后重跑，"
          "再执行\n    python scripts/check_slots.py --accept-glossary-change")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
