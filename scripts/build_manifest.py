#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_manifest.py —— 管线 ⓪ 体检（inventory）

作用
    扫描本地课程资料，逐个判定「能不能翻译 / 正文到底多少字 / 坏在哪 / 为什么坏」，
    产出机器可核对的账本 manifest.json。

四条设计原则（都是踩过坑换来的）
    1. 只记「正文字数」，不记「文件大小」。
       文件大小会严重误导：prompt-engineering-overview.html 有 2,005,200 字节，
       但正文只有 57,799 字符（96% 是脚本/样式）。按字节记账会高估工作量 6 倍以上。
    2. 正文统计必须做交叉校验：严格法（整块删 script/style）vs 宽松法（只删标签）。
       两者差异过大说明「剥壳不干净」，此时两个数字都不可信，必须报出来给人看，
       绝不在两个数字里默默选一个。
    3. PDF 类型判定必须在【解压后的对象集合】上做。
       直接在原始字节里搜 /BaseFont —— 搜不到 ≠ 不存在（对象可能压在 /ObjStm 里）；
       用「有没有 /Subtype /Image」判断图片型 —— 会把带封面图的正常文档误判成图片型。
    4. 失败必须给「根因」，并严格区分性质：
       真 404（确认不存在）≠ 被拦截 403（不能判定不存在）≠ 网络不可达（未核查）。

两遍运行
    抓取环节之前跑一次 → pre_fetch（known_gaps 来自内置默认值）
    抓取环节之后跑一次 → post_fetch（读同目录 fetch_report.json，登记新抓到的文件）
    第一遍绝对不能因为没有 fetch_report.json 而报错退出。

环境限制
    只用 Python 标准库（re / json / os / sys / zlib / hashlib / html）。
    Windows 控制台是 GBK，所以打印统一走 UTF-8 重配置，避免 UnicodeEncodeError。

用法
    python build_manifest.py
"""

import hashlib
import html as htmllib
import json
import os
import re
import sys
import zlib

# ============================================================ 路径配置
# ⚠️ 换源有三条路，优先级从高到低：
#     ① 命令行参数     --materials-dir / --course-dirname / --out / --fetch-report
#     ② 环境变量       MF_MATERIALS_DIR / MF_COURSE_DIRNAME / MF_OUT
#     ③ 下面这些默认值
#    这样「换一份资料」不需要改源码，只替换 URL 清单与术语表即可。
BASE_DIR = os.path.dirname(os.path.abspath(__file__))     # = scripts/
REPO_ROOT = os.path.dirname(BASE_DIR)                     # 仓库根

# 目录布局：data/ 输入 · work/ 中间产物 · output/ 最终交付
DATA_DIR = os.path.join(REPO_ROOT, "data")
WORK_DIR = os.path.join(REPO_ROOT, "work")
REPORTS_DIR = os.path.join(WORK_DIR, "reports")

# 默认值（可被参数/环境变量覆盖）
DEFAULT_COURSE_DIRNAME = os.environ.get("MF_COURSE_DIRNAME", "CS146S_offline")
DEFAULT_SITE_HOSTNAME = "themodernsoftware.dev"
DEFAULT_SUPPLEMENTAL_PDFNAME = "Vibe_Coding_Playbook.pdf"

# 运行时生效值（由 configure() 重设）
COURSE_DIRNAME = DEFAULT_COURSE_DIRNAME
MATERIALS_DIRNAME = "materials"
SITE_HOSTNAME = DEFAULT_SITE_HOSTNAME
SUPPLEMENTAL_PDFNAME = DEFAULT_SUPPLEMENTAL_PDFNAME
MATERIALS_DIR = os.path.join(DATA_DIR, MATERIALS_DIRNAME)       # 课程原始资料（只读）
OUT_PATH = os.environ.get("MF_OUT") or os.path.join(REPORTS_DIR, "manifest.json")
FETCH_REPORT_PATH = os.path.join(REPORTS_DIR, "fetch_report.json")  # 抓取产出（可能不存在）


def resolve_materials_dir(base_dir, dirname, course_dirname):
    """
    兼容不同存放习惯地定位资料根目录：
      ① 优先 <base>/<dirname>（如 data/materials）
      ② 否则在 <base> 下（含一级子目录）搜索「含课程子目录」的目录
    返回找到的绝对路径；都找不到就返回默认值（后续打印警告并跳过，绝不抛异常）。
    """
    default = os.path.join(base_dir, dirname)
    if os.path.isdir(os.path.join(default, course_dirname)):
        return default

    candidates = []
    try:
        for entry in sorted(os.listdir(base_dir)):
            sub = os.path.join(base_dir, entry)
            if not os.path.isdir(sub):
                continue
            for cand in (os.path.join(sub, dirname), sub):
                if os.path.isdir(os.path.join(cand, course_dirname)):
                    candidates.append(cand)
    except OSError:
        pass
    return candidates[0] if candidates else default


MATERIALS_DIR = resolve_materials_dir(DATA_DIR, "materials", COURSE_DIRNAME)
COURSE_DIR = os.path.join(MATERIALS_DIR, COURSE_DIRNAME)
PAGES_DIR = os.path.join(COURSE_DIR, "pages")
PDFS_DIR = os.path.join(COURSE_DIR, "pdfs")
SITE_DIR = os.path.join(COURSE_DIR, "site", SITE_HOSTNAME)
PAGE_MAP_PATH = os.path.join(COURSE_DIR, "page_map.json")
SUPPLEMENTAL_PDF = os.path.join(MATERIALS_DIR, SUPPLEMENTAL_PDFNAME)


def configure(materials_dir=None, course_dirname=None, out=None,
              fetch_report=None, site_hostname=None, supplemental_pdfname=None):
    """
    按命令行参数/环境变量重设本模块的路径全局变量。

    ⚠️ 为什么用「重设全局」而不是把路径层层传参：
       下游 build_page_items / build_pdf_items / build_site_items 等
       全都直接读这些模块级常量。逐个改成传参要动几十处调用点，
       风险远大于收益。这里集中重设一次，语义与「改常量」等价。
    ⚠️ 每个 globals() 赋值都必须带 global 声明，且只在 DO 里重设一次；
       漏一个就会让下游仍读旧值（这类 bug 很隐蔽）。
    """
    global COURSE_DIRNAME, MATERIALS_DIR, COURSE_DIR, PAGES_DIR, PDFS_DIR
    global SITE_DIR, PAGE_MAP_PATH, SUPPLEMENTAL_PDF, OUT_PATH, FETCH_REPORT_PATH
    global SITE_HOSTNAME, SUPPLEMENTAL_PDFNAME

    if course_dirname:
        COURSE_DIRNAME = course_dirname
    if site_hostname:
        SITE_HOSTNAME = site_hostname
    if supplemental_pdfname:
        SUPPLEMENTAL_PDFNAME = supplemental_pdfname

    if materials_dir:
        # 显式给了就用它；否则沿用「自动定位」的兼容逻辑，行为不变
        MATERIALS_DIR = os.path.abspath(materials_dir)
    else:
        MATERIALS_DIR = resolve_materials_dir(DATA_DIR, MATERIALS_DIRNAME,
                                              COURSE_DIRNAME)

    COURSE_DIR = os.path.join(MATERIALS_DIR, COURSE_DIRNAME)
    PAGES_DIR = os.path.join(COURSE_DIR, "pages")
    PDFS_DIR = os.path.join(COURSE_DIR, "pdfs")
    SITE_DIR = os.path.join(COURSE_DIR, "site", SITE_HOSTNAME)
    PAGE_MAP_PATH = os.path.join(COURSE_DIR, "page_map.json")
    SUPPLEMENTAL_PDF = os.path.join(MATERIALS_DIR, SUPPLEMENTAL_PDFNAME)
    if out:
        OUT_PATH = os.path.abspath(out)
    if fetch_report:
        FETCH_REPORT_PATH = os.path.abspath(fetch_report)
    elif out:
        # 账本路径变了，fetch_report 默认跟着走同一目录，避免两者错位
        FETCH_REPORT_PATH = os.path.join(os.path.dirname(OUT_PATH),
                                         "fetch_report.json")


def parse_args(argv):
    """极简参数解析（不引 argparse，保持与其它脚本一致的风格）。"""
    opts = {"materials_dir": os.environ.get("MF_MATERIALS_DIR"),
            "course_dirname": os.environ.get("MF_COURSE_DIRNAME"),
            "out": os.environ.get("MF_OUT"),
            "fetch_report": os.environ.get("MF_FETCH_REPORT"),
            "site_hostname": None, "supplemental_pdfname": None,
            "help": False}
    flags = {
        "--materials-dir": "materials_dir",
        "--course-dirname": "course_dirname",
        "--out": "out",
        "--fetch-report": "fetch_report",
        "--site-hostname": "site_hostname",
        "--supplemental-pdfname": "supplemental_pdfname",
    }
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("-h", "--help"):
            opts["help"] = True
        elif a in flags:
            if i + 1 >= len(argv):
                raise SystemExit(f"❌ {a} 后面要跟一个值")
            opts[flags[a]] = argv[i + 1]
            i += 1
        else:
            raise SystemExit(f"❌ 未知参数：{a}\n\n{USAGE}")
        i += 1
    return opts


USAGE = """build_manifest.py —— 管线 ⓪ 资料体检（inventory）

用法：
  python scripts/build_manifest.py [选项]

选项：
  --materials-dir DIR      资料根目录（默认自动定位 data/materials）
  --course-dirname NAME    课程子目录名（默认 CS146S_offline）
  --out PATH               账本输出路径（默认 work/reports/manifest.json）
  --fetch-report PATH      抓取报告路径（默认与 --out 同目录）
  --site-hostname NAME     站点快照目录名（默认 themodernsoftware.dev）
  --supplemental-pdfname F 补充 PDF 文件名（默认 Vibe_Coding_Playbook.pdf）
  -h, --help               显示本帮助

也可用环境变量：MF_MATERIALS_DIR / MF_COURSE_DIRNAME / MF_OUT / MF_FETCH_REPORT
（命令行参数优先于环境变量）
"""

GENERATED_BY = "build_manifest.py"
MANIFEST_NOTE = "本文件由脚本生成，请勿手改。所有数字必须来自脚本，避免多文档口径漂移。"

# 正文长度阈值（阅读文章正常都在 3,000 字符以上，实测最小 3,047）
MIN_EMPTY_CHARS = 500     # 低于此 → shell_only（疑似空壳）
MIN_OK_CHARS = 3000       # 低于此 → suspect（疑似抽取不完整）
SUSPECT_NOISE_RATIO = 0.90  # 严格/宽松差异超过 90% → 必须人工复核

# ============================================================ 状态口径
# status 取值（不许自己发明新值）
STATUS_VALUES = [
    "ok", "empty", "paywalled", "js_rendered", "blocked", "shell_only", "suspect",
    "image_only", "ocr_text_layer", "type3_vector", "font_encoding_broken",
    "not_applicable", "failed",
    "fetched_pending_extract",   # post_fetch 模式新增：已抓到，字数待回填
]
# 这些 status 属于「不可得」，要按性质细分登记进 known_gaps
UNAVAILABLE_STATUSES = [
    "http_404", "blocked_403", "network_error", "needs_account",
    "unreachable_automated", "not_cached", "not_published", "parse_error",
]
SOURCE_CLASSES = ["official_site", "reading", "lecture", "video", "github", "supplemental"]

# ============================================================ 内置默认缺口（pre_fetch）
# 这些是已经实测确认过的「课程要求但拿不到」的资源，直接写死；post_fetch 时会用
# fetch_report.json 的实际结果重新生成。
DEFAULT_KNOWN_GAPS = [
    {
        "what": "Google Slides 讲义（Lectures）",
        "count": 12,
        "source_class": "lecture",
        "status": "needs_account",
        "failure_root_cause": "docs.google.com 需 Google 账号登录后才能读取，匿名抓取只能拿到登录页，非文件不存在",
        "urls": [],
        "retrieval_attempts": [
            {"channel": "web_fetch docs.google.com/presentation/...", "result": "重定向到登录页，无法匿名访问", "kind": "needs_account"},
        ],
    },
    {
        "what": "Google Drive 文件（练习答案 / 设计文档模板 / 幻灯片）",
        "count": 3,
        "source_class": "lecture",
        "status": "needs_account",
        "failure_root_cause": "drive.google.com 需 Google 账号登录，且未开放「知道链接的任何人」权限",
        "urls": [],
        "retrieval_attempts": [
            {"channel": "web_fetch drive.google.com/file/d/...", "result": "重定向到登录页，无法匿名访问", "kind": "needs_account"},
        ],
    },
    {
        "what": "YouTube 视频字幕（3 个视频）",
        "count": 3,
        "source_class": "video",
        "status": "unreachable_automated",
        "failure_root_cause": (
            "自动抓取手段全部失败，且失败性质不同，必须分开记录："
            "① youtube.com 网络不可达（network_error，属「未核查」，不能判定为不存在）；"
            "② 本地无 yt-dlp / youtube-dl / ffmpeg，无法下载字幕（tool_missing）；"
            "③ youtubetotranscript.com 与 glasp.co 均返回 HTTP 403 被 Cloudflare 人机校验拦截"
            "（blocked_403，属「被拦截」，同样不能判定为不存在）。"
            "结论是「自动抓取不可得」，不是「客观不可得」——人工开浏览器仍可拿到转录文本。"
        ),
        "urls": [
            "https://www.youtube.com/watch?v=7xTGNNLPyMI",
            "https://www.youtube.com/watch?v=T9aRN5JkmL8",
            "https://www.youtube.com/watch?v=TswQeKftnaw",
        ],
        "titles": [
            "Deep Dive into LLMs",
            "AI Prompt Engineering: A Deep Dive",
            "Lessons from millions of AI code reviews",
        ],
        "retrieval_attempts": [
            {"channel": "web_fetch https://www.youtube.com/watch?v=7xTGNNLPyMI", "result": "fetch failed（无 HTTP 状态码）", "kind": "network_error"},
            {"channel": "web_fetch https://m.youtube.com/...", "result": "fetch failed（无 HTTP 状态码）", "kind": "network_error"},
            {"channel": "web_fetch video.google.com/timedtext?lang=en&v=...", "result": "fetch failed（无 HTTP 状态码）", "kind": "network_error"},
            {"channel": "本地命令 yt-dlp / youtube-dl / ffmpeg", "result": "三者均未安装（命令不存在）", "kind": "tool_missing"},
            {"channel": "web_fetch youtubetotranscript.com/transcript?v=...", "result": "HTTP 403（Cloudflare 人机校验）", "kind": "blocked_403"},
            {"channel": "web_fetch glasp.co/youtube/<id>", "result": "HTTP 403（Cloudflare 人机校验）", "kind": "blocked_403"},
        ],
    },
    {
        "what": "官方作业仓库 week2–week8（Assignments）",
        "count": 7,
        "source_class": "github",
        "status": "http_404",
        "failure_root_cause": (
            "github.com/mihail911/modern-software-dev-assignments 的 master 分支只公开 week1；"
            "week2–week8 的 assignment 文件经 raw.githubusercontent.com 直连返回 HTTP 404，"
            "服务器可达且明确报「不存在」——这是有效信息（确认未公开），不是抓取失败。"
            "另注：唯一公开的 week1 README 标注为 “fall 2026”，非本课程学年，内容不可直接复用。"
        ),
        "urls": [
            "https://github.com/mihail911/modern-software-dev-assignments",
        ],
        "retrieval_attempts": [
            {"channel": "web_fetch raw.githubusercontent.com/.../master/week1/README.md", "result": "HTTP 200，但 README 标注 fall 2026", "kind": "ok"},
            {"channel": "web_fetch raw.githubusercontent.com/.../master/week{2..8}/README.md", "result": "HTTP 404（真 404，文件确认不存在）", "kind": "http_404"},
        ],
    },
    {
        "what": "How FAANG Vibe Codes（W3 阅读，X/Twitter 短帖）",
        "count": 1,
        "source_class": "reading",
        "status": "not_cached",
        "failure_root_cause": "该阅读项指向 x.com 短帖，本地缓存中不存在对应文件；x.com 需要登录且禁止匿名抓取，本项未核查",
        "urls": [],
        "retrieval_attempts": [
            {"channel": "本地缓存 page_map.json 检索", "result": "无对应条目（未缓存）", "kind": "not_cached"},
        ],
    },
]


# ============================================================ 工具函数
def reconfigure_stdout_utf8():
    """
    Windows 控制台默认 GBK，直接 print 中文/emoji 会抛 UnicodeEncodeError。
    把 stdout/stderr 重配置成 UTF-8；失败也不影响主流程（宁可少打印，不能崩）。
    """
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is None:
            continue
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def read_text(path):
    """按 UTF-8 读取文本，坏字节用 replace 兜底（避免个别坏文件中断整轮体检）"""
    with open(path, "rb") as f:
        raw = f.read()
    return raw.decode("utf-8", "replace")


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def count_english_words(text):
    """英文词数：连续 2 个以上拉丁字母算一个词（粗略但两法口径一致，可用于交叉校验）"""
    return len(re.findall(r"[A-Za-z]{2,}", text))


def normspace(text):
    return re.sub(r"\s+", " ", text).strip()


def rel_path(path):
    """
    输出统一用正斜杠相对路径，便于跨平台复用。
    ⚠️ 基准必须是【仓库根 REPO_ROOT】，不是脚本目录 ——
       否则会写出 "../data/materials/..." 这种路径，
       下游 extract.py 拼出来就找不到文件（实测抽取计划因此变成 0 个 manifest 条目）。
    """
    try:
        return os.path.relpath(path, REPO_ROOT).replace("\\", "/")
    except ValueError:
        return path.replace("\\", "/")


def strip_script_style(raw):
    """剥壳：整块删除 script / style / noscript / svg / head"""
    s = re.sub(r"(?s)<!--.*?-->", " ", raw)
    s = re.sub(r"(?is)<(script|style|noscript|svg|head)\b[^>]*>.*?</\1\s*>", " ", s)
    return s


# ============================================================ 正文抽取（两法交叉校验）
def extract_text(raw):
    """
    严格法：先整块删除 <script> <style> <noscript> <svg> <head>，再删所有标签，
            再解码 HTML 实体，最后压缩空白。
    这是「正文」的权威口径。
    """
    s = strip_script_style(raw)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = htmllib.unescape(s)
    return normspace(s)


def extract_text_loose(raw):
    """
    宽松法：只删标签，不整块删 script/style。
    目的不是「另一种正文」，而是暴露「剥壳剥掉了多少东西」：
    两者差距大 → 该文件脚本/样式占比高 → 严格法结果需要人工复核。
    """
    s = re.sub(r"(?s)<[^>]+>", " ", raw)
    s = htmllib.unescape(s)
    return normspace(s)


def extract_site_text(js_blob):
    """
    课程官网是 Vite SPA，index.html 里 body 只有 <div id="root">，
    全部正文以 JSX 文本节点 children:"..." 的形式内嵌在打包 JS 中。
    """
    parts = re.findall(r'children:"((?:[^"\\]|\\.){12,})"', js_blob)
    # 打包后的字符串是「转义再转义」的，需要逐层还原
    cleaned = []
    for p in parts:
        try:
            cleaned.append(json.loads('"' + p + '"'))
        except Exception:
            cleaned.append(p.replace('\\"', '"').replace("\\n", " "))
    return normspace(" ".join(cleaned)), len(parts)


def extract_title(raw):
    m = re.search(r"(?is)<title[^>]*>(.*?)</title>", raw)
    if not m:
        return None
    t = normspace(htmllib.unescape(m.group(1)))
    return t or None


# ============================================================ PDF 探测
def load_objects(raw):
    r"""
    把 PDF 还原成 {对象号: 对象体}，两种来源合并（未压缩的优先）：

      ① 未压缩对象：(\d+) (\d+) obj ... endobj
      ② /Type /ObjStm 对象流：zlib 解压后，
         头部是 N 对「对象号 偏移」，正文起点由 /First 给出，
         据此把每个被压缩对象切出来。

    ⚠️ 这一步是整个 PDF 判定里最关键的：
       现代 PDF 把字体、ToUnicode 等全压进 ObjStm，
       不先解压就在原始字节里搜 /BaseFont 会搜到 0 次，
       于是把正常文档误判成「无字体 → 图片型」。
       搜不到 ≠ 不存在。
    """
    # ① 未压缩对象
    objs = {}
    for m in re.finditer(rb"(\d+)\s+(\d+)\s+obj(.*?)endobj", raw, re.S):
        objs[int(m.group(1))] = m.group(3)

    # ② 对象流：解压后切分被压缩对象
    for m in re.finditer(rb"(\d+)\s+(\d+)\s+obj(.*?)endobj", raw, re.S):
        body = m.group(3)
        if b"/ObjStm" not in body:
            continue
        sm = re.search(rb"stream\r?\n", body)
        if not sm:
            continue
        data = re.sub(rb"\s*endstream\s*$", b"", body[sm.end():])
        try:
            dec = zlib.decompress(data)
        except Exception:
            # 对象流解不开（加密 / 非 Flate）→ 跳过，但绝不当成「里面没有对象」
            continue
        mn = re.search(rb"/N\s+(\d+)", body)
        mf = re.search(rb"/First\s+(\d+)", body)
        if not (mn and mf):
            continue
        n_objs, first = int(mn.group(1)), int(mf.group(1))
        header = dec[:first].split()
        pairs = []
        for i in range(0, min(len(header) - 1, 2 * n_objs), 2):
            try:
                pairs.append((int(header[i]), int(header[i + 1])))
            except ValueError:
                break
        for i, (onum, off) in enumerate(pairs):
            end = pairs[i + 1][1] if i + 1 < len(pairs) else len(dec) - first
            objs.setdefault(onum, dec[first + off:first + end])

    return objs


def probe_pdf(path):
    r"""
    在【解压后的对象集合】上统计指标，再按固定顺序判定类型。
    指标（全部只在解压后的对象体上统计）：
      bt_operators          内容流里 \\bBT\\b 出现次数（文本绘制算子）
      content_streams       含 BT 且不含 endchar 的流数量（真正的正文内容流）
      fonts_with_basefont   /Type /Font 且带 /BaseFont 的对象数量 → 有字体就能抽文本
      has_hidden_ocr        是否出现 HiddenHorzOCR（扫描件 OCR 隐藏文本层标记）
      has_type3             是否出现 /CharProcs（Type3 矢量字形标记）
      embedded_images       /Subtype /Image 数量（仅记录，不参与类型判定！）
    """
    with open(path, "rb") as f:
        raw = f.read()

    objs = load_objects(raw)
    blob = b"\n".join(objs.values())

    bt_operators = 0
    content_streams = 0
    for body in objs.values():
        hits = len(re.findall(rb"\bBT\b", body))
        bt_operators += hits
        # 含 BT 说明在画文本；含 endchar 的多是 Type3 字形定义流，不算正文
        if hits and b"endchar" not in body:
            content_streams += 1

    # 字体判定：以解压后的对象体为准，/BaseFont 与 /Type /Font 双条件
    fonts_with_basefont = 0
    for body in objs.values():
        if re.search(rb"/Type\s*/Font", body) and b"/BaseFont" in body:
            fonts_with_basefont += 1

    return {
        "objects_decoded": len(objs),
        "objstm_objects": len(re.findall(rb"/ObjStm", raw)),
        # 对照项：证明「原始字节里搜不到」不是「不存在」
        "basefont_raw_bytes": len(re.findall(rb"/BaseFont", raw)),
        "basefont_decompressed": len(re.findall(rb"/BaseFont", blob)),
        "to_unicode_decompressed": len(re.findall(rb"/ToUnicode", blob)),
        "bt_operators": bt_operators,
        "content_streams": content_streams,
        "fonts_with_basefont": fonts_with_basefont,
        "has_hidden_ocr": b"HiddenHorzOCR" in blob,
        "has_type3": b"/CharProcs" in blob,
        "embedded_images": len(re.findall(rb"/Subtype\s*/Image", blob)),
        "charprocs_objects": len(re.findall(rb"/CharProcs", blob)),
    }


def classify_pdf_type(probe):
    """
    严格按给定顺序判定；顺序不能改：
      1) bt_operators == 0        → image_only（没有文本绘制算子，只能是图片）
      2) fonts_with_basefont > 0  → text
      3) has_hidden_ocr           → ocr_text_layer
      4) has_type3                → type3_vector
      5) 其他                      → unknown_needs_review
    """
    if probe["bt_operators"] == 0:
        return "image_only"
    if probe["fonts_with_basefont"] > 0:
        return "text"
    if probe["has_hidden_ocr"]:
        return "ocr_text_layer"
    if probe["has_type3"]:
        return "type3_vector"
    return "unknown_needs_review"


# 内容标记 → 判定（顺序即优先级，先判更明确的失败类型）
def classify_broken_html(raw, size, chars):
    """
    返回 (status, failure_root_cause, translatable)
    只负责「明显坏掉」的文件；正常文件返回 (None, None, None) 交给字数阈值判定。
    """
    low = raw.lower()
    if size == 0:
        return ("empty", "本地文件 0 字节：抓取阶段完全没拿到内容（非解析失败，是无内容可取）", False)
    if "requires a browser to access" in raw or "blocks automated" in low:
        return ("blocked", "原站（Medium）对自动化访问返回反爬拦截，缓存内只剩一段占位说明，正文从未取得", False)
    if ("gh-private" in low or "gh-private-signup-form" in low
            or "gh-flow-content private" in low or "enter access code" in low):
        return ("paywalled", "原站（Ghost 私有模式）正文需付费/订阅/访问码才可见，静态抓取只拿到订阅表单", False)
    if "notion-html" in low or "data-notion-version" in low:
        return ("js_rendered", "原站为 Notion 页面，正文由客户端 JS 动态渲染，静态抓取只有应用外壳（含 JS 加载器与样式），无正文", False)
    return (None, None, None)


# ============================================================ 阅读文章（pages/*.html）
def build_page_items(page_map):
    url_by_file = {v: k for k, v in page_map.items()}
    items, checks = [], []

    if not os.path.isdir(PAGES_DIR):
        print(f"⚠️  目录不存在，跳过阅读文章：{PAGES_DIR}")
        return items, checks

    for fn in sorted(os.listdir(PAGES_DIR)):
        if not fn.lower().endswith(".html"):
            continue
        fp = os.path.join(PAGES_DIR, fn)
        item_id = os.path.splitext(fn)[0]
        size = os.path.getsize(fp)

        item = {
            "id": item_id,
            "source_class": "reading",
            "title": None,
            "origin_url": url_by_file.get(fn),
            "local_path": rel_path(fp),
            "translatable": None,
            "chars": 0,
            "english_words": 0,
            "chars_loose": 0,
            "english_words_loose": 0,
            "noise_ratio": 0.0,
            "file_bytes": size,
            "status": "ok",
            "failure_root_cause": None,
            "retrieval_attempts": [],
        }

        try:
            raw = read_text(fp)
            strict = extract_text(raw)
            loose = extract_text_loose(raw)
            chars, words = len(strict), count_english_words(strict)
            chars_loose, words_loose = len(loose), count_english_words(loose)
            noise = (chars_loose - chars) / chars_loose if chars_loose else 0.0

            item.update({
                "title": extract_title(raw),
                "chars": chars,
                "english_words": words,
                "chars_loose": chars_loose,
                "english_words_loose": words_loose,
                "noise_ratio": round(noise, 4),
                "chars_reliable": noise <= SUSPECT_NOISE_RATIO,
            })

            status, cause, translatable = classify_broken_html(raw, size, chars)
            if status is None:
                # 字数阈值判定（坏文件已在上一步识别）
                if chars < MIN_EMPTY_CHARS:
                    status, translatable = "shell_only", None
                    cause = (f"抽取到的正文仅 {chars} 字符（<{MIN_EMPTY_CHARS}），"
                             f"远低于同类文章，疑似静态空壳，无法确认是否真有正文")
                elif chars < MIN_OK_CHARS:
                    status, translatable = "suspect", None
                    cause = (f"正文 {chars} 字符，明显低于同类文章（其他篇均 >3,000），"
                             f"疑似抽取不完整，需人工打开原页核对")
                else:
                    status, translatable = "ok", True
                    cause = None
            item.update({"status": status, "translatable": translatable,
                         "failure_root_cause": cause})
        except Exception as exc:  # 抽取抛异常 → failed（根因写具体异常）
            item.update({
                "status": "failed",
                "translatable": None,
                "failure_root_cause": f"抽取过程抛出异常：{type(exc).__name__}: {exc}",
            })

        items.append(item)
        # 交叉校验明细：严格法与宽松法都要留痕，差异大的单独标出来
        checks.append({
            "id": item_id,
            "chars_strict": item["chars"],
            "words_strict": item["english_words"],
            "chars_loose": item["chars_loose"],
            "words_loose": item["english_words_loose"],
            "noise_ratio": item["noise_ratio"],
            "diff_pct": round(item["noise_ratio"] * 100, 1),
            "needs_review": item["noise_ratio"] > SUSPECT_NOISE_RATIO,
        })

    return items, checks


# ============================================================ PDF 条目
def build_pdf_items():
    items = []

    if os.path.isdir(PDFS_DIR):
        for fn in sorted(os.listdir(PDFS_DIR)):
            if not fn.lower().endswith(".pdf"):
                continue
            fp = os.path.join(PDFS_DIR, fn)
            item = {
                "id": os.path.splitext(fn)[0],
                "source_class": "reading",   # 官网把这些 PDF 挂在 Reading 区块
                "title": None,
                "origin_url": None,
                "local_path": rel_path(fp),
                "translatable": None,
                "chars": None,               # PDF 正文字数由 extract.py 环节产出后回填
                "english_words": None,
                "chars_loose": None,
                "english_words_loose": None,
                "noise_ratio": None,
                "file_bytes": os.path.getsize(fp),
                "status": "failed",
                "failure_root_cause": None,
                "retrieval_attempts": [],
            }
            try:
                probe = probe_pdf(fp)
                ptype = classify_pdf_type(probe)
                item["pdf_probe"] = probe
                item["pdf_type"] = ptype
                # text / ocr_text_layer / type3_vector 都能抽出文本（后两者质量有损）→ 可翻译
                item["translatable"] = ptype in ("text", "ocr_text_layer", "type3_vector")
                item["status"] = ptype if ptype != "text" else "ok"
                if ptype == "ok" or ptype == "text":
                    item["status"] = "ok"
                    item["failure_root_cause"] = None
                elif ptype == "image_only":
                    item["failure_root_cause"] = (
                        "解压后对象集合中没有任何文本绘制算子（BT 出现 0 次），"
                        "页面正文是内嵌图片，无文本层，需 OCR"
                    )
                elif ptype == "ocr_text_layer":
                    item["failure_root_cause"] = (
                        "内容流带 HiddenHorzOCR 标记：扫描件 + OCR 隐藏文本层，文本可抽但质量有损"
                    )
                elif ptype == "type3_vector":
                    item["failure_root_cause"] = (
                        "字体为 Type3 矢量字形（/CharProcs 存在，且无 /BaseFont）："
                        "文本可抽但字符映射需借助 ToUnicode，质量有损"
                    )
                else:
                    item["failure_root_cause"] = (
                        "有文本绘制算子，但既无 /BaseFont、也无 OCR 标记与 Type3 标记，"
                        "字体编码方式无法判定，需人工复核"
                    )
            except Exception as exc:
                item["status"] = "failed"
                item["failure_root_cause"] = f"PDF 解析抛出异常：{type(exc).__name__}: {exc}"
            items.append(item)

    return items


# ============================================================ 课程官网 SPA
def build_site_items():
    items, notes = [], []
    index_html = os.path.join(SITE_DIR, "index.html")
    robots_txt = os.path.join(SITE_DIR, "robots.txt")
    js_path = os.path.join(SITE_DIR, "assets", "index-CgRb4FxC.js")

    if not os.path.isfile(index_html):
        return items, notes

    item = {
        "id": "course-site-spa",
        "source_class": "official_site",
        "title": "CS146S 课程官网（Overview / Syllabus / FAQ / 讲师）",
        "origin_url": "https://themodernsoftware.dev/",
        "local_path": rel_path(SITE_DIR) + "/",
        "translatable": True,
        "chars": None,
        "english_words": None,
        "chars_loose": None,
        "english_words_loose": None,
        "noise_ratio": None,
        "file_bytes": os.path.getsize(index_html),
        "status": "ok",
        "failure_root_cause": None,
        "retrieval_attempts": [],
    }

    # 正文在打包 JS 里
    try:
        if os.path.isfile(js_path):
            site_text, node_count = extract_site_text(read_text(js_path))
            item["chars"] = len(site_text)
            item["english_words"] = count_english_words(site_text)
            item["content_source"] = rel_path(js_path)
            item["jsx_text_nodes"] = node_count
            item["chars_loose"] = item["chars"]
            item["english_words_loose"] = item["english_words"]
            item["noise_ratio"] = 0.0
            notes.append(f"官网正文不在 index.html，而在打包 JS {os.path.basename(js_path)} 中"
                         f"（{node_count} 个 JSX 文本节点 children:\"...\"）")
        else:
            item["status"] = "suspect"
            item["translatable"] = None
            item["failure_root_cause"] = f"打包 JS 不存在，无法提取官网正文：{rel_path(js_path)}"
            notes.append(f"⚠️ {rel_path(js_path)} 不存在")
    except Exception as exc:
        item["status"] = "failed"
        item["translatable"] = None
        item["failure_root_cause"] = f"官网 JS 正文抽取抛异常：{type(exc).__name__}: {exc}"

    notes.append("index.html 是 Vite 空壳：body 内只有一个 <div id=\"root\">，静态读取拿不到任何正文")

    # robots.txt 与 index.html 是否同为误复制的假文件
    if os.path.isfile(robots_txt):
        try:
            h_index, h_robots = sha256_of(index_html), sha256_of(robots_txt)
            item["robots_txt_sha256"] = h_robots
            item["index_html_sha256"] = h_index
            if h_index == h_robots:
                item["robots_txt_is_duplicate"] = True
                notes.append(f"robots.txt 与 index.html 内容完全相同（SHA-256 一致：{h_robots[:16]}…），"
                             f"是抓取时误复制的假文件，不是真的 robots.txt，不可作为抓取规则依据")
            else:
                item["robots_txt_is_duplicate"] = False
        except Exception:
            pass

    item["notes"] = notes
    items.append(item)
    return items, notes


# ============================================================ 附加文档（中文原生，不翻译）
def build_supplemental_items():
    items = []
    if not os.path.isfile(SUPPLEMENTAL_PDF):
        return items
    fp = SUPPLEMENTAL_PDF
    item = {
        "id": os.path.splitext(os.path.basename(fp))[0],
        "source_class": "supplemental",
        "title": "Elite 20: Vibe Coding（中文原生文档）",
        "origin_url": None,
        "local_path": rel_path(fp),
        "translatable": False,      # 确认不需要翻译
        "chars": None,
        "english_words": None,
        "chars_loose": None,
        "english_words_loose": None,
        "noise_ratio": None,
        "file_bytes": os.path.getsize(fp),
        "status": "not_applicable",
        "failure_root_cause": None,
        "retrieval_attempts": [],
    }
    try:
        probe = probe_pdf(fp)
        item["pdf_probe"] = probe
        item["pdf_type"] = classify_pdf_type(probe)
        item["notes"] = [
            "⚠️ 该文档本身是中文原生内容，不是英文材料，因此 translatable=false（不是「翻译失败」）",
            "不属于课程官方材料，官网 Syllabus 中不存在该文档",
        ]
    except Exception as exc:
        item["failure_root_cause"] = f"PDF 解析抛出异常：{type(exc).__name__}: {exc}"
    items.append(item)
    return items


# ============================================================ post_fetch：读 fetch_report.json
def load_fetch_report():
    """读取抓取报告；不存在或读不动都返回 None（第一遍绝不能因此报错退出）"""
    if not os.path.isfile(FETCH_REPORT_PATH):
        return None
    try:
        with open(FETCH_REPORT_PATH, encoding="utf-8", errors="replace") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            print(f"⚠️  {os.path.basename(FETCH_REPORT_PATH)} 顶层不是对象，忽略本次抓取结果")
            return None
        return data
    except Exception as exc:
        print(f"⚠️  {os.path.basename(FETCH_REPORT_PATH)} 解析失败（{type(exc).__name__}: {exc}），"
              f"本次按 pre_fetch 处理")
        return None


def build_fetched_items(report):
    """把 fetch_report 里 status=fetched_ok 的条目登记进 items（正文字数待 extract.py 回填）"""
    out = []
    for i, fi in enumerate(report.get("items") or []):
        if not isinstance(fi, dict):
            continue
        if fi.get("status") != "fetched_ok":
            continue
        local = fi.get("local_path") or fi.get("path") or fi.get("saved_path")
        fid = fi.get("id") or os.path.splitext(os.path.basename(local or ""))[0] or f"fetched-{i+1}"
        out.append({
            "id": fid,
            "source_class": fi.get("source_class") or "reading",
            "title": fi.get("title"),
            "origin_url": fi.get("origin_url") or fi.get("url"),
            "local_path": local,
            "translatable": True,
            "chars": None,                 # ← 待 extract.py 产出后回填
            "english_words": None,
            "chars_loose": None,
            "english_words_loose": None,
            "noise_ratio": None,
            "file_bytes": fi.get("file_bytes"),
            "status": "fetched_pending_extract",
            "failure_root_cause": None,
            "note": "已抓取，正文字数待 extract.py 产出后回填",
            "retrieval_attempts": fi.get("retrieval_attempts") or [],
        })
    return out


def build_known_gaps_from_report(report):
    """用 fetch_report 的实际结果按 status 分组，重新生成 known_gaps"""
    groups = {}
    for fi in report.get("items") or []:
        if not isinstance(fi, dict):
            continue
        status = fi.get("status")
        if status in (None, "fetched_ok"):
            continue          # 抓到了就不是缺口
        g = groups.setdefault(status, {"count": 0, "urls": [], "root_causes": [], "source_class": fi.get("source_class")})
        g["count"] += 1
        url = fi.get("origin_url") or fi.get("url")
        if url and url not in g["urls"]:
            g["urls"].append(url)
        cause = fi.get("failure_root_cause") or fi.get("reason")
        if cause and cause not in g["root_causes"]:
            g["root_causes"].append(cause)

    gaps = []
    for status, g in sorted(groups.items()):
        detail = "；".join(g["root_causes"]) if g["root_causes"] else (
            f"抓取阶段返回状态 {status}，未给出更细根因，需人工复核")
        gaps.append({
            "what": f"抓取未成功的资源（status={status}）",
            "count": g["count"],
            "source_class": g["source_class"] or "reading",
            "status": status,
            "failure_root_cause": detail,
            "urls": g["urls"],
            "retrieval_attempts": [{"channel": "fetch 环节", "result": f"status={status}", "kind": status}],
        })
    return gaps


# ============================================================ 统计
def make_summary(items, known_gaps, manifest_mode):
    reading_html = [it for it in items
                    if it.get("source_class") == "reading"
                    and str(it.get("local_path") or "").lower().endswith(".html")]
    reading_all = [it for it in items if it.get("source_class") == "reading"]

    def is_translatable(it):
        return it.get("translatable") is True and it.get("chars") is not None

    tr = [it for it in reading_all if is_translatable(it)]

    status_by_class = {}
    for cls in SOURCE_CLASSES:
        agg = {}
        for it in items:
            if it.get("source_class") == cls:
                agg[it["status"]] = agg.get(it["status"], 0) + 1
        status_by_class[cls] = agg

    unavailable = {}
    for g in known_gaps:
        unavailable[g["status"]] = unavailable.get(g["status"], 0) + g.get("count", 0)

    return {
        "manifest_mode": manifest_mode,
        # local_archived 只记「本地原有归档」，不含本次抓取补充的条目（那些归 fetched_this_run）
        "local_archived": {
            "reading_html": sum(1 for it in reading_html
                                if it["status"] != "fetched_pending_extract"),
            "pdf": sum(1 for it in items if str(it.get("local_path") or "").lower().endswith(".pdf")
                       and it.get("source_class") == "reading"
                       and it["status"] != "fetched_pending_extract"),
            "official_site": sum(1 for it in items if it.get("source_class") == "official_site"
                                 and it["status"] != "fetched_pending_extract"),
            "supplemental": sum(1 for it in items if it.get("source_class") == "supplemental"
                                and it["status"] != "fetched_pending_extract"),
        },
        "fetched_this_run": {
            "fetched_ok": sum(1 for it in items if it["status"] == "fetched_pending_extract"),
            "note": "本次抓取补充的条目（正文字数待 extract.py 回填）",
        },
        "unavailable": unavailable,
        "unavailable_total": sum(unavailable.values()),
        "reading_html_total": len(reading_html),
        "reading_html_ok": sum(1 for it in reading_html if it.get("translatable") is True),
        "reading_html_failed": sum(1 for it in reading_html if it.get("translatable") is False),
        "reading_html_suspect": sum(1 for it in reading_html if it.get("translatable") is None),
        "reading_translatable_chars": sum(it.get("chars") or 0 for it in tr),
        "reading_translatable_words": sum(it.get("english_words") or 0 for it in tr),
        "status_by_class": status_by_class,
        "totals": {
            "items": len(items),
            "chars_strict": sum(it.get("chars") or 0 for it in tr),
            "chars_loose": sum(it.get("chars_loose") or 0 for it in tr),
            "words_strict": sum(it.get("english_words") or 0 for it in tr),
            "words_loose": sum(it.get("english_words_loose") or 0 for it in tr),
        },
    }


# ============================================================ 控制台报告
def print_report(manifest):
    s = manifest["summary"]
    items = manifest["items"]

    print("=" * 78)
    print(f"管线 ⓪ 体检完成 → {OUT_PATH}")
    print("=" * 78)

    # 1. 运行模式
    print(f"\n【1】运行模式：{manifest['manifest_mode']}")
    print(f"    fetch_status：{manifest.get('fetch_status', '-')}")

    # 2. 阅读材料统计
    print(f"\n【2】阅读材料统计（pages/*.html）")
    print(f"    总数        : {s['reading_html_total']} 篇")
    print(f"    可翻译      : {s['reading_html_ok']} 篇")
    print(f"    失败        : {s['reading_html_failed']} 篇")
    print(f"    存疑        : {s['reading_html_suspect']} 篇")
    print(f"    可翻译正文字数: {s['reading_translatable_chars']:,} 字符（严格法）")
    print(f"    可翻译英文词数: {s['reading_translatable_words']:,} 词（严格法）")
    print(f"    注：PDF 正文字数不计入此处，待 extract.py 产出后回填")

    la = s["local_archived"]
    print(f"    口径拆分：本地原有归档 {s['reading_html_total'] - s['fetched_this_run']['fetched_ok']} 篇"
          f"（HTML 归档总数 {la['reading_html']}）+ 本次抓取补充 {s['fetched_this_run']['fetched_ok']} 个"
          f"（其中部分非 html）")
    print(f"    本地原有归档：PDF {la['pdf']} 个 / 官网 {la['official_site']} 个 / "
          f"附加文档 {la['supplemental']} 个")

    # 3. 失败/存疑明细
    print(f"\n【3】失败与存疑文件明细（文件名 | 正文字数 | status | 根因）")
    bad = [it for it in items
           if it.get("source_class") == "reading"
           and str(it.get("local_path") or "").lower().endswith(".html")
           and it.get("translatable") is not True]
    if not bad:
        print("    无")
    for it in bad:
        flag = "❌" if it["translatable"] is False else "⚠️ "
        print(f"    {flag} {it['id']}")
        print(f"        正文字数 : {it['chars']:,}（宽松法 {it['chars_loose']:,}）"
              f"  词数 {it['english_words']:,}  文件 {it['file_bytes']:,} 字节")
        print(f"        status   : {it['status']}")
        print(f"        根因     : {it['failure_root_cause']}")

    # 4. PDF 判定
    print(f"\n【4】PDF 探测结果（解压对象流后统计）")
    for it in items:
        probe = it.get("pdf_probe")
        if not probe:
            continue
        ptype = it.get("pdf_type", "?")
        print(f"    {os.path.basename(it['local_path'] or '')}")
        print(f"        判定类型        : {ptype}   → translatable={it['translatable']}"
              f"   status={it['status']}")
        print(f"        bt_operators    : {probe['bt_operators']}（文本绘制算子）")
        print(f"        content_streams : {probe['content_streams']}（含 BT 不含 endchar 的内容流）")
        print(f"        fonts_with_basefont: {probe['fonts_with_basefont']}（/Type /Font 且带 /BaseFont）")
        print(f"        has_hidden_ocr  : {probe['has_hidden_ocr']}")
        print(f"        has_type3       : {probe['has_type3']}（/CharProcs 出现 {probe['charprocs_objects']} 次）")
        print(f"        embedded_images : {probe['embedded_images']}（仅记录，不参与类型判定）")
        print(f"        对象解码        : {probe['objects_decoded']} 个"
              f"（ObjStm 对象流 {probe['objstm_objects']} 个）")
        print(f"        /BaseFont 对照  : 原始字节 {probe['basefont_raw_bytes']} 次"
              f" / 解压后 {probe['basefont_decompressed']} 次"
              f"  ← 搜不到≠不存在")
        if it.get("failure_root_cause"):
            print(f"        说明            : {it['failure_root_cause']}")

    # 5. 交叉校验
    cc = manifest["cross_check"]
    print(f"\n【5】交叉校验：严格法（整块删 script/style） vs 宽松法（只删标签）")
    print(f"    {'':14}{'字符数':>14}{'英文词数':>12}")
    print(f"    严格法        {cc['strict_chars']:>14,}{cc['strict_words']:>12,}")
    print(f"    宽松法        {cc['loose_chars']:>14,}{cc['loose_words']:>12,}")
    diff = cc["loose_chars"] - cc["strict_chars"]
    pct = diff / cc["loose_chars"] * 100 if cc["loose_chars"] else 0
    print(f"    差异          {diff:>14,}{cc['loose_words'] - cc['strict_words']:>12,}")
    print(f"    差异百分比    {pct:>13.1f}%   （宽松法比严格法多出的比例 = 被剥掉的脚本/样式占比）")
    print(f"    口径：只统计 translatable=true 的 {s['reading_html_ok']} 篇阅读文章；"
          f"两个数字都保留，不择一使用")

    noisy = [c for c in manifest["cross_check"]["per_file"] if c["needs_review"]]
    if noisy:
        print(f"\n    ⚠️ 差异 > {int(SUSPECT_NOISE_RATIO*100)}% 的文件（脚本/样式占比极高，"
              f"正文统计需人工复核，已标记 needs_review）：")
        for c in sorted(noisy, key=lambda x: -x["noise_ratio"]):
            print(f"       {c['id']:<44} 差异 {c['diff_pct']:>5.1f}%   "
                  f"严格 {c['chars_strict']:>7,} / 宽松 {c['chars_loose']:>9,}")

    # 6. known_gaps
    print(f"\n【6】known_gaps：课程要求但拿不到的资源（{len(manifest['known_gaps'])} 组，"
          f"合计 {s['unavailable_total']} 个）")
    for g in manifest["known_gaps"]:
        print(f"    [{g['status']}] {g['what']} —— {g['count']} 个（{g['source_class']}）")
        print(f"        根因: {g['failure_root_cause']}")
        for u in (g.get("urls") or [])[:3]:
            print(f"        URL : {u}")
        if len(g.get("urls") or []) > 3:
            print(f"        URL : …另有 {len(g['urls']) - 3} 个")

    # 附：各 source_class 状态分布
    print(f"\n【附】status_by_class（每个 source_class 的状态分布）")
    for cls, agg in s["status_by_class"].items():
        if agg:
            print(f"    {cls:<16} {agg}")


def build_cross_check(page_checks, ok_ids):
    """把交叉校验结果固化进 manifest：两个数字都留，谁都不许被默默丢掉"""
    per_file = sorted(page_checks, key=lambda c: -c["noise_ratio"])
    ok = [c for c in per_file if c["id"] in ok_ids]
    return {
        "strict_chars": sum(c["chars_strict"] for c in ok),
        "strict_words": sum(c["words_strict"] for c in ok),
        "loose_chars": sum(c["chars_loose"] for c in ok),
        "loose_words": sum(c["words_loose"] for c in ok),
        "scope": f"仅统计 translatable=true 的 {len(ok)} 篇阅读文章",
        "noise_ratio_threshold": SUSPECT_NOISE_RATIO,
        "per_file": per_file,
        "needs_review_ids": [c["id"] for c in ok if c["needs_review"]],
        "note": "严格法与宽松法两个数字都必须保留：差异过大说明剥壳不干净、正文统计不可信，"
                "此时该文件标 needs_review 交人工复核，而不是在两个数字里默默选一个。",
    }


# ============================================================ 主流程
def main(argv=None):
    opts = parse_args(argv if argv is not None else sys.argv[1:])
    if opts["help"]:
        print(USAGE)
        return 0
    configure(materials_dir=opts["materials_dir"],
              course_dirname=opts["course_dirname"],
              out=opts["out"],
              fetch_report=opts["fetch_report"],
              site_hostname=opts["site_hostname"],
              supplemental_pdfname=opts["supplemental_pdfname"])
    reconfigure_stdout_utf8()

    print("=" * 78)
    print(f"{GENERATED_BY} —— 课程资料体检（inventory）")
    print(f"资料根目录: {MATERIALS_DIR}")
    print("=" * 78)

    # ---- 第一遍 / 第二遍判定
    fetch_report = load_fetch_report()
    manifest_mode = "post_fetch" if fetch_report is not None else "pre_fetch"

    # ---- page_map.json
    page_map = {}
    if os.path.isfile(PAGE_MAP_PATH):
        try:
            with open(PAGE_MAP_PATH, encoding="utf-8", errors="replace") as f:
                page_map = json.load(f)
        except Exception as exc:
            print(f"⚠️  page_map.json 解析失败（{type(exc).__name__}），origin_url 将为空")

    # ---- 收集 items
    items = []
    page_items, page_checks = build_page_items(page_map)
    items.extend(page_items)
    items.extend(build_pdf_items())
    site_items, site_notes = build_site_items()
    items.extend(site_items)
    items.extend(build_supplemental_items())

    # ---- 第二遍：追加本次抓取补充的文件 + 用真实结果重建 known_gaps
    fetched_items = []
    if fetch_report is not None:
        fetched_items = build_fetched_items(fetch_report)
        items.extend(fetched_items)
        known_gaps = build_known_gaps_from_report(fetch_report)
        fetch_status = (f"fetch_report.json 已读取：本次抓到 {len(fetched_items)} 个新文件，"
                        f"缺口按报告实际结果重新生成")
    else:
        known_gaps = [dict(g) for g in DEFAULT_KNOWN_GAPS]
        fetch_status = "fetch_report.json 不存在，缺口数据来自内置默认值"

    # ---- 交叉校验（严格法 vs 宽松法）
    ok_ids = {it["id"] for it in page_items if it.get("translatable") is True}
    cross_check = build_cross_check(page_checks, ok_ids)

    # ---- summary
    summary = make_summary(items, known_gaps, manifest_mode)

    manifest = {
        # 开头三个元字段
        "generated_by": GENERATED_BY,
        "manifest_mode": manifest_mode,
        "note": MANIFEST_NOTE,

        "fetch_status": fetch_status,
        "paths": {
            "materials_dir": rel_path(MATERIALS_DIR),
            "course_dir": rel_path(COURSE_DIR),
            "pages_dir": rel_path(PAGES_DIR),
            "pdfs_dir": rel_path(PDFS_DIR),
            "site_dir": rel_path(SITE_DIR),
            "page_map": rel_path(PAGE_MAP_PATH),
            "supplemental_pdf": rel_path(SUPPLEMENTAL_PDF),
            "fetch_report": rel_path(FETCH_REPORT_PATH),
        },
        "source_classes": {
            "official_site": "课程官网（themodernsoftware.dev）",
            "reading": "课程阅读材料（官网 Reading 区块的文章与 PDF）",
            "lecture": "讲义（官网 Lectures 区块：Google Slides / PDF）",
            "video": "视频（YouTube）",
            "github": "GitHub 仓库（作业 / 指定阅读）",
            "supplemental": "非课程官方材料（本地附加文档 / 干扰项）",
        },
        "status_values": STATUS_VALUES,
        "thresholds": {
            "min_empty_chars": MIN_EMPTY_CHARS,
            "min_ok_chars": MIN_OK_CHARS,
            "suspect_noise_ratio": SUSPECT_NOISE_RATIO,
        },
        "items": items,
        "known_gaps": known_gaps,
        "cross_check": cross_check,
        "summary": summary,
    }
    if fetch_report is not None:
        manifest["fetch_summary"] = fetch_report.get("summary")
        manifest["fetch_items_ingested"] = len(fetched_items)

    # ---- 写盘
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # ---- 控制台自检
    print_report(manifest)

    print(f"\n{'=' * 78}")
    print(f"已写出：{OUT_PATH}")
    print(f"{'=' * 78}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
