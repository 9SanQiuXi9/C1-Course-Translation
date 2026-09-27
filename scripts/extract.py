#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract.py —— 管线 ② 抽取（extraction）

作用
    把三种不同格式的原始资料（HTML 网页 / PDF / 官网 SPA 的打包 JS）
    统一抽成【同一套格式约定】的 Markdown（extracted/<id>.md + YAML front matter），
    这样下游 chunk.py 完全不需要知道来源格式 —— 格式差异全部在这一层消化。

架构
    EXTRACTORS = {".html": extract_html, ".pdf": extract_pdf, ".js": extract_spa,
                  ".md": extract_markdown, ".txt": extract_text, ".prompt": extract_text}
    所有抽取器返回同一套结构（见 make_result），front matter 由统一函数生成。

两条硬性纪律（来自环节规格）
    A. 抽取失败时【绝不写占位文件】—— 那会被下游切块当成真实内容，制造「已处理」的假象。
       只在 extract_report.json 里记 status=failed 和原因。
    B. 绝不为「看起来完整」而猜测或补全缺失的字符/段落。宁可标 warning。

PDF 环节的三个致命坑（都已在下面处理）
    1. 用「有没有 /Subtype /Image」判断图片型 → 有封面图的正常文档会被误判
    2. 直接在原始字节里搜 /BaseFont → 对象压在 /ObjStm 里时搜到 0 次，
       于是误判成「无字体 → 图片型」。搜不到 ≠ 不存在。
    3. 把多个字体的 CMap 全局合并 → 不同字体子集键冲突，整篇串码

环境限制
    只用 Python 标准库（re/json/os/sys/zlib/hashlib/html/urllib + HTMLParser）。
    Windows 控制台 GBK，打印统一走 UTF-8。
    本机 OpenSSL 信任库为空，本环节不联网，无需处理。

用法
    python extract.py
"""

import hashlib
import html as htmllib
import json
import os
import re
import sys
import zlib
from html.parser import HTMLParser

# ============================================================ 路径配置
# 换课程时只需要改这几行
# ⚠️ 脚本放在 scripts/ 子目录里，而 manifest.json / materials/ / extracted/ 都在
#    仓库根目录，所以 BASE_DIR 必须取【脚本所在目录的上一级】。
#    取 dirname(__file__) 会指到 scripts/，导致读不到 manifest、抽取计划为 0。
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
# ⚠️ 目录布局改成了 data/ + work/ + output/，回退判据不能再只看 materials/：
#    必须认 data/ 或 materials/，否则会把 BASE_DIR 误退回 scripts/，
#    导致所有路径都拼到 scripts/ 下面。
if not (os.path.isdir(os.path.join(BASE_DIR, "data"))
        or os.path.isdir(os.path.join(BASE_DIR, "materials"))):
    # 兜底：脚本被直接放在仓库根时，退回脚本自身目录
    BASE_DIR = SCRIPT_DIR

MATERIALS_DIRNAME = "materials"
COURSE_DIRNAME = os.environ.get("MF_COURSE_DIRNAME", "CS146S_offline")
SITE_HOSTNAME = os.environ.get("MF_SITE_HOSTNAME", "themodernsoftware.dev")
ARCHIVE_DIRNAME = "archive"
EXTRACTED_DIRNAME = "extracted"

MANIFEST_NAME = "manifest.json"
EXTRACT_REPORT_NAME = "extract_report.json"

# 目录布局：data/ 输入 · work/ 中间产物 · output/ 最终交付
DATA_DIR = os.path.join(BASE_DIR, "data")
WORK_DIR = os.path.join(BASE_DIR, "work")
REPORTS_DIR = os.path.join(WORK_DIR, "reports")

MATERIALS_DIR = os.path.join(DATA_DIR, MATERIALS_DIRNAME)
COURSE_DIR = os.path.join(MATERIALS_DIR, COURSE_DIRNAME)
PAGES_DIR = os.path.join(COURSE_DIR, "pages")
PDFS_DIR = os.path.join(COURSE_DIR, "pdfs")
SITE_DIR = os.path.join(COURSE_DIR, "site", SITE_HOSTNAME)
ARCHIVE_DIR = os.path.join(DATA_DIR, "fetched")            # 抓取归档（原 archive/）
EXTRACTED_DIR = os.path.join(WORK_DIR, "extracted")        # 抽取后的 Markdown

MANIFEST_PATH = os.path.join(REPORTS_DIR, MANIFEST_NAME)             # 上游账本
EXTRACT_REPORT_PATH = os.path.join(REPORTS_DIR, EXTRACT_REPORT_NAME)  # 抽取报告


def configure(materials_dir=None, course_dirname=None, site_hostname=None,
              archive_dir=None, manifest=None, out_dir=None, report=None):
    """
    按命令行参数/环境变量重设本模块的路径全局变量。

    ⚠️ 用「重设全局」的原因同 build_manifest.py：下游几十处直接读这些
       模块级常量，逐个改成传参风险远大于收益。
    ⚠️ 每个被改的名字都要写进 global 声明 —— 漏一个就会让下游读到旧值，
       而这类 bug 表现为「参数看着生效了，产出却还在老地方」，很难查。
    """
    global COURSE_DIRNAME, SITE_HOSTNAME, MATERIALS_DIR, COURSE_DIR
    global PAGES_DIR, PDFS_DIR, SITE_DIR, ARCHIVE_DIR, EXTRACTED_DIR
    global MANIFEST_PATH, EXTRACT_REPORT_PATH

    if course_dirname:
        COURSE_DIRNAME = course_dirname
    if site_hostname:
        SITE_HOSTNAME = site_hostname

    # 换源时先确定资料根目录：显式给了就用它，否则沿用默认
    MATERIALS_DIR = (os.path.abspath(materials_dir) if materials_dir
                     else os.path.join(DATA_DIR, MATERIALS_DIRNAME))
    COURSE_DIR = os.path.join(MATERIALS_DIR, COURSE_DIRNAME)
    PAGES_DIR = os.path.join(COURSE_DIR, "pages")
    PDFS_DIR = os.path.join(COURSE_DIR, "pdfs")
    SITE_DIR = os.path.join(COURSE_DIR, "site", SITE_HOSTNAME)

    if archive_dir:
        ARCHIVE_DIR = os.path.abspath(archive_dir)
    if out_dir:
        EXTRACTED_DIR = os.path.abspath(out_dir)
    if report:
        EXTRACT_REPORT_PATH = os.path.abspath(report)
    if manifest:
        MANIFEST_PATH = os.path.abspath(manifest)


def parse_args(argv):
    """极简参数解析（不引 argparse，保持与其它脚本一致的风格）。"""
    opts = {"materials_dir": os.environ.get("MF_MATERIALS_DIR"),
            "course_dirname": os.environ.get("MF_COURSE_DIRNAME"),
            "site_hostname": os.environ.get("MF_SITE_HOSTNAME"),
            "archive_dir": os.environ.get("MF_ARCHIVE_DIR"),
            "manifest": os.environ.get("MF_MANIFEST"),
            "out_dir": os.environ.get("MF_EXTRACTED_DIR"),
            "report": os.environ.get("MF_EXTRACT_REPORT"),
            "help": False}
    flags = {
        "--materials-dir": "materials_dir",
        "--course-dirname": "course_dirname",
        "--site-hostname": "site_hostname",
        "--archive-dir": "archive_dir",
        "--manifest": "manifest",
        "--out-dir": "out_dir",
        "--report": "report",
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


USAGE = """extract.py —— 管线 ② 抽取（HTML / PDF / SPA → 统一 Markdown）

用法：
  python scripts/extract.py [选项]

选项：
  --materials-dir DIR    课程原始资料根目录（默认 data/materials）
  --course-dirname NAME  课程子目录名（默认 CS146S_offline）
  --site-hostname NAME   站点快照目录名（默认 themodernsoftware.dev）
  --archive-dir DIR      抓取归档目录（默认 data/fetched）
  --manifest PATH        上游账本路径（默认 work/reports/manifest.json）
  --out-dir DIR          抽取产出目录（默认 work/extracted）
  --report PATH          抽取报告路径（默认 work/reports/extract_report.json）
  -h, --help             显示本帮助

也可用环境变量：MF_MATERIALS_DIR / MF_COURSE_DIRNAME / MF_ARCHIVE_DIR /
MF_MANIFEST / MF_EXTRACTED_DIR / MF_EXTRACT_REPORT
"""

# 正文长度阈值：与下游一致
MIN_OK_CHARS = 500

# 剥离过激的兜底阈值：删掉某区块导致正文字数下降超过这个比例 → 把区块加回来
AGGRESSIVE_STRIP_RATIO = 0.40

# 非正文区块关键词（忽略大小写，按 class/id/role 匹配）
DENY_KEYWORDS = [
    "nav", "navbar", "menu", "sidebar", "footer", "header", "breadcrumb",
    "cookie", "subscribe", "newsletter", "social", "share", "related",
    "recommend", "comment", "author-bio", "byline", "advertisement", "ad-",
    "promo", "banner", "toc", "table-of-contents",
]

# 这些标签视为「整块非正文」，直接丢弃
DROP_TAGS = {"script", "style", "noscript", "svg", "head", "nav", "footer", "aside"}

# 代码块语言推断
LANG_HINTS = [
    "language-", "lang-", "highlight-source-", "brush:", "prettyprint",
]


# ============================================================ 通用工具
def reconfigure_stdout_utf8():
    """Windows 控制台 GBK，打印中文/emoji 会 UnicodeEncodeError"""
    for name in ("stdout", "stderr"):
        stream = getattr(sys, name, None)
        if stream is None:
            continue
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def log(msg=""):
    print(msg)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(262144), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text(path):
    with open(path, "rb") as f:
        raw = f.read()
    return raw.decode("utf-8", "replace")


def count_english_words(text):
    return len(re.findall(r"[A-Za-z]{2,}", text))


def norm_inline(s):
    """行内空白压缩（不动换行）"""
    return re.sub(r"[ \t\u00a0]+", " ", s).strip()


def strip_ws_lines(text):
    """去掉行尾空格、压缩连续空行（最多一个空行）"""
    lines = [ln.rstrip() for ln in text.split("\n")]
    out, blank = [], 0
    for ln in lines:
        if not ln.strip():
            blank += 1
            if blank > 1:
                continue
        else:
            blank = 0
        out.append(ln)
    return "\n".join(out).strip() + "\n"


def yaml_escape(value):
    """把值安全地写进 YAML 双引号标量"""
    if value is None:
        return '""'
    s = str(value)
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    s = s.replace("\n", " ").replace("\r", " ")
    return '"' + s + '"'


def yaml_scalar(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return '""'
    if isinstance(value, (int, float)):
        return str(value)
    return yaml_escape(value)


# ============================================================ 统一结果结构
def make_result(fmt):
    """
    所有抽取器都返回这个结构，保证下游格式一致。
    ⚠️ 这是「格式差异只在这一层消化」的关键：上层不需要知道来源是 html 还是 pdf。
    """
    return {
        "format": fmt,
        "title": None,
        "body": "",            # Markdown 正文（不含 front matter）
        "warnings": [],
        "code_blocks": 0,
        "tables": 0,
        "links": 0,
        "heading_levels_seen": None,   # 仅 html
        "extra": {},                   # PDF 自检指标等
    }


# ============================================================ A. HTML 抽取
# 链接占位符：\x00A\x00<href>\x00<锚文本>
# ⚠️ 用 \x00 是因为它绝不会出现在正常正文里。
#    （原实现只埋占位符、从未还原，导致 7,467 个 \x00 漏进产出、
#      2,489 个链接全部退化成 "A <url> 文本" 这种畸形文本。）
ANCHOR_RE = re.compile(r"\x00A\x00([^\x00]*)\x00(.*?)(?=\x00A\x00|$)", re.S)
# 兜底：清掉任何残留的控制字符（代码块不经过这里，不受影响）
CTRL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def _render_anchors(parser, text):
    """
    把链接占位符还原成 Markdown 链接 [锚文本](url)。
    · 无锚文本 → 直接给裸 URL（有些站点的链接是图标）
    · 锚文本与 href 字面相同 → 不再重复输出 [url](url)
    · 整段只有链接 → 单独占一行，避免与相邻文本粘连
    ⚠️ 按【实际产出的链接】计数，不在开标签处计数 ——
       否则未闭合的 <a> 也会被算进去。
    """
    if "\x00A\x00" not in text:
        return text
    only_link = bool(re.fullmatch(r"(?:\x00A\x00[^\x00]*\x00.*?)+", text.strip(), re.S))
    named, bare = [], []
    for m in ANCHOR_RE.finditer(text):
        href, label = m.group(1).strip(), m.group(2).strip()
        if label and label != href:
            named.append((label, href))
        elif href:
            bare.append(href)
    parser.links += len(named) + len(bare)
    parts = [f"[{lbl}]({url})" for lbl, url in named] + bare
    rendered = " ".join(parts)
    if not rendered:
        return text          # 全空锚点：交给兜底清理
    if only_link:
        return "\n" + rendered + "\n"
    return rendered


class BodyParser(HTMLParser):
    """
    把 (已剥壳的) HTML 正文转成 Markdown。
    只处理「正文」语义：标题、段落、列表、代码、表格、图片、链接。
    """
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []              # 输出 Markdown 行
        self.buf = []              # 当前文本缓冲
        self.skip_depth = 0        # >0 表示在要丢弃的区块里
        self.skip_stack = []
        self.pre_depth = 0
        self.pre_buf = []
        self.pre_lang = None
        self.list_stack = []       # [{'type':'ul'|'ol','counter':int}]
        self.code_blocks = 0
        self.tables = 0
        self.links = 0
        self.headings = {f"h{i}": 0 for i in range(1, 7)}
        self.headings_seen = []    # [(level, text)]
        self.images = 0
        self.figcaption_open = False
        self.in_table = False
        self.table_buf = []
        self.table_depth = 0
        self.table_complex = False
        self.title_candidates = []  # [(level, text)]

    # ---------- 输出辅助
    def _flush_text(self, is_inline=False):
        if not self.buf:
            return
        text = norm_inline(htmllib.unescape("".join(self.buf)))
        self.buf = []
        if not text:
            return
        # 先剥离格式 token，再渲染：这样文本比较（列表项/表格单元）
        # 不会被 \x00 污染
        text = _render_anchors(self, text)
        text = norm_inline(text)
        if not text:
            return
        if is_inline and self.out and self.out[-1] != "":
            self.out[-1] = self.out[-1] + " " + text
            return
        if self.figcaption_open:
            self.out.append(f"*{text}*")
            self.out.append("")
            return
        if self.list_stack:
            depth = len(self.list_stack) - 1
            indent = "  " * depth
            top = self.list_stack[-1]
            if top["type"] == "ol":
                top["counter"] += 1
                self.out.append(f"{indent}{top['counter']}. {text}")
            else:
                self.out.append(f"{indent}- {text}")
            return
        self.out.append(text)
        self.out.append("")

    def _append_anchor(self, href):
        """
        把 <a> 作为独立的缓冲条目推入。
        ⚠️ 必须与相邻文本【分开】，否则文本会粘进链接锚文本（实测出现
           "…折扣 A https://url 立即报名" 这种畸形输出）。
        """
        self.buf.append(f"\x00A\x00{href}\x00")

    def _emit_blank(self):
        if self.out and self.out[-1] != "":
            self.out.append("")

    # ---------- 标签处理
    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        cls_id = " ".join([a.get("class", ""), a.get("id", ""), a.get("role", "")]).lower()

        if tag in DROP_TAGS:
            self.skip_depth += 1
            self.skip_stack.append(tag)
            return
        if self.skip_depth:
            # 嵌套的同名标签也要计数，保证闭合配对
            if tag in DROP_TAGS:
                self.skip_depth += 1
            return

        if tag == "pre":
            self._flush_text()
            self.pre_depth += 1
            self.pre_buf = []
            self.pre_lang = guess_language(a.get("class", ""))
            return
        if self.pre_depth:
            if tag == "code" and not self.pre_lang:
                self.pre_lang = guess_language(a.get("class", ""))
            return

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._flush_text()
            self.buf = []
            self._pending_heading = int(tag[1])
            return
        if tag == "p" or tag == "div" or tag == "section" or tag == "article":
            self._flush_text()
            return
        if tag in ("ul", "ol"):
            self._flush_text()
            self.list_stack.append({"type": "ol" if tag == "ol" else "ul", "counter": 0})
            return
        if tag == "li":
            self._flush_text()
            return
        if tag == "br":
            self.buf.append("\n")
            return
        if tag == "figcaption":
            self._flush_text()
            self.figcaption_open = True
            return
        if tag == "img":
            self._flush_text()
            src = a.get("src", "")
            alt = norm_inline(a.get("alt", ""))
            if src:
                self.out.append(f"![{alt}]({src})")
                self.out.append("")
                self.images += 1
            return
        if tag == "a":
            href = a.get("href", "")
            if href:
                # ⚠️ 锚点必须单独入缓冲，不能与相邻文本混在一起，
                #    否则"折扣 A <url> 立即报名"这种粘连会污染输出
                self._flush_text(is_inline=True)
                self._append_anchor(href)
            return
        if tag == "table":
            self._flush_text()
            self.in_table = True
            self.table_depth = 1
            self.table_buf = []
            self.table_complex = False
            return
        if tag == "tr":
            if self.in_table:
                self.table_buf.append(["__ROW__"])
            return
        if tag in ("td", "th"):
            if self.in_table:
                if "colspan" in a or "rowspan" in a:
                    self.table_complex = True
                self.table_buf.append(["__CELL__", tag == "th"])
            return
        if tag == "hr":
            self._flush_text()
            self.out.append("---")
            self.out.append("")

    def handle_endtag(self, tag):
        if tag in DROP_TAGS:
            if self.skip_stack and self.skip_stack[-1] == tag:
                self.skip_stack.pop()
                self.skip_depth = max(0, self.skip_depth - 1)
            elif self.skip_depth:
                self.skip_depth -= 1
            return
        if self.skip_depth:
            return

        if tag == "pre":
            if self.pre_depth:
                self.pre_depth -= 1
            if self.pre_depth == 0:
                self._emit_code_block()
            return
        if self.pre_depth:
            return

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            lvl = getattr(self, "_pending_heading", int(tag[1]))
            text = norm_inline(htmllib.unescape("".join(self.buf)))
            self.buf = []
            self._pending_heading = None
            # ⚠️ 标题也必须过一遍锚点渲染：标题里嵌链接很常见
            #    （如 <h4><a href="/x">Title</a></h4>）。
            #    这里曾经直接输出 text，占位符没被还原，产出
            #    "## Ahttps://…" 这种畸形标题（实测 6 篇文档、101 处）。
            text = norm_inline(_render_anchors(self, text))
            if text:
                self.headings[f"h{int(tag[1])}"] += 1
                self.headings_seen.append((int(tag[1]), text))
                self.title_candidates.append((int(tag[1]), text))
                self.out.append("")
                self.out.append("#" * lvl + " " + text)
                self.out.append("")
            return
        if tag in ("p", "div", "section", "article"):
            self._flush_text()
            self._emit_blank()
            return
        if tag in ("ul", "ol"):
            self._flush_text()
            if self.list_stack:
                self.list_stack.pop()
            self._emit_blank()
            return
        if tag == "li":
            self._flush_text()
            return
        if tag == "figcaption":
            self._flush_text()
            self.figcaption_open = False
            return
        if tag == "table":
            self._flush_table()
            return
        if tag == "tr":
            if self.in_table and self.table_buf and self.table_buf[-1] != ["__ROW__"]:
                pass
            return
        if tag in ("td", "th"):
            if self.in_table and self.table_buf:
                cell = norm_inline(htmllib.unescape("".join(self.buf)))
                self.buf = []
                # 表格单元同样要过锚点渲染（单元格里带链接很常见）
                cell = norm_inline(_render_anchors(self, cell))
                self.table_buf.append(cell)
            return

    def handle_data(self, data):
        if self.skip_depth:
            return
        if self.pre_depth:
            self.pre_buf.append(data)
            return
        if self.in_table:
            self.buf.append(data)
            return
        self.buf.append(data)

    def handle_entityref(self, name):
        self.handle_data(htmllib.unescape("&" + name + ";"))

    def handle_charref(self, name):
        self.handle_data(htmllib.unescape("&#" + name + ";"))

    # ---------- 代码块 / 表格
    def _emit_code_block(self):
        raw = "".join(self.pre_buf)
        self.pre_buf = []
        # ⚠️ 代码内容逐字节原样保留：只去掉整体首尾各一个换行，不做其它调整
        code = raw
        if code.startswith("\r\n"):
            code = code[2:]
        elif code.startswith("\n"):
            code = code[1:]
        if code.endswith("\r\n"):
            code = code[:-2]
        elif code.endswith("\n"):
            code = code[:-1]
        self.code_blocks += 1
        cid = f"c{self.code_blocks}"
        lang = self.pre_lang or ""
        self.out.append(f"<!-- CODE_BLOCK_START id={cid} lang={lang} -->")
        self.out.append("```" + lang)
        self.out.append(code)
        self.out.append("```")
        self.out.append(f"<!-- CODE_BLOCK_END id={cid} -->")
        self.out.append("")

    def _flush_table(self):
        self._flush_text()
        rows, cur = [], None
        for item in self.table_buf:
            if item == ["__ROW__"]:
                cur = []
                rows.append(cur)
            elif isinstance(item, list) and item and item[0] == "__CELL__":
                if cur is not None:
                    cur.append("")
            elif isinstance(item, str) and cur is not None and cur:
                if cur[-1]:
                    cur[-1] += " " + item
                else:
                    cur[-1] = item
        rows = [r for r in rows if r and any(c.strip() for c in r)]
        if not rows:
            self.in_table = False
            self.table_buf = []
            return
        self.tables += 1
        if self.table_complex:
            # Markdown 表达不了 colspan/rowspan → 保留原始 <table> 并记 warning
            self.warnings_table_complex = True
            self.out.append("<!-- COMPLEX_TABLE_KEPT_AS_HTML -->")
            self.out.append("<table>")
            for r in rows:
                self.out.append("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>")
            self.out.append("</table>")
        else:
            width = max(len(r) for r in rows)
            rows = [r + [""] * (width - len(r)) for r in rows]
            self.out.append("| " + " | ".join(rows[0]) + " |")
            self.out.append("| " + " | ".join(["---"] * width) + " |")
            for r in rows[1:]:
                self.out.append("| " + " | ".join(r) + " |")
        self.out.append("")
        self.in_table = False
        self.table_buf = []

    # ---------- 收尾
    def result_body(self):
        self._flush_text()
        text = "\n".join(self.out)
        return strip_ws_lines(text)


def guess_language(class_attr):
    """从 class 推断代码语言"""
    low = (class_attr or "").lower()
    for hint in LANG_HINTS:
        m = re.search(re.escape(hint) + r"([a-z0-9+#]+)", low)
        if m:
            return m.group(1)
    return None


def _has_deny_keyword(attrs_str):
    """
    判断 class/id/role 是否命中非正文关键词。
    ⚠️ 必须按「token 边界」匹配，不能用裸子串：
       "header" 里含 "ad"，"breadcrumb" 含 "ad"，裸子串会把正文区块全删掉。
    """
    low = (attrs_str or "").lower()
    for kw in DENY_KEYWORDS:
        if kw == "ad-":
            if re.search(r"(^|[\s\"'_-])ad[-_]", low):
                return True
            continue
        if re.search(r"(^|[\s\"'_-])" + re.escape(kw) + r"($|[\s\"'_-])", low):
            return True
    return False


def strip_denied_blocks(html):
    """
    按 class/id 关键词剥掉导航/页脚/侧栏等整块非正文区域。
    返回 (剥离后的 html, 命中的区块数)。
    只在「开始标签 → 同名结束标签」之间成对地删，保证不破坏结构。
    """
    out = []
    i = 0
    n = len(html)
    removed = 0
    tag_re = re.compile(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)((?:[^>\"']|\"[^\"]*\"|'[^']*')*)>", re.S)
    skip_tag = None
    depth = 0
    while i < n:
        m = tag_re.search(html, i)
        if not m:
            if skip_tag is None:
                out.append(html[i:])
            break
        if skip_tag is None:
            out.append(html[i:m.start()])
        closing, tag, attrs = m.group(1), m.group(2).lower(), m.group(3)
        self_closing = attrs.rstrip().endswith("/") or tag in (
            "br", "img", "hr", "meta", "link", "input", "source", "area", "base", "col")

        if skip_tag is not None:
            if tag == skip_tag and not self_closing:
                if closing:
                    depth -= 1
                    if depth <= 0:
                        skip_tag = None
                        depth = 0
                else:
                    depth += 1
            i = m.end()
            continue

        if not closing and not self_closing and _has_deny_keyword(attrs):
            skip_tag = tag
            depth = 1
            removed += 1
            i = m.end()
            continue

        out.append(m.group(0))
        i = m.end()
    return "".join(out), removed


def remove_drop_tag_blocks(html):
    """整块删除 script/style/noscript/svg/head/nav/footer/aside"""
    for _ in range(3):   # 处理嵌套
        new = re.sub(
            r"(?is)<(script|style|noscript|svg|head|nav|footer|aside)\b[^>]*>.*?</\1\s*>",
            " ", html)
        if new == html:
            break
        html = new
    return html


def html_visible_text(html):
    """粗略取可见文本，用于「剥过头」兜底比较"""
    s = re.sub(r"(?s)<!--.*?-->", " ", html)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = htmllib.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def extract_html(text, src_path):
    """
    HTML → Markdown。
    步骤：剥壳 → 关键词剥离（带 40% 兜底）→ 结构化转 Markdown → 标题归一化。
    """
    res = make_result("html")
    html = text

    # 1. 整块剥壳
    shelled = remove_drop_tag_blocks(html)

    # 2. 关键词剥离 + 兜底
    denoised, n_blocks = strip_denied_blocks(shelled)
    base_len = len(html_visible_text(shelled))
    denoised_len = len(html_visible_text(denoised))
    if base_len > 0 and (base_len - denoised_len) / base_len > AGGRESSIVE_STRIP_RATIO:
        # ⚠️ 剥过头了：把区块加回来，并如实记一条警告
        res["warnings"].append(
            f"AGGRESSIVE_STRIP_REVERTED：按关键词剥离 {n_blocks} 个区块后正文下降 "
            f"{(base_len - denoised_len) / base_len * 100:.1f}%（>{AGGRESSIVE_STRIP_RATIO*100:.0f}%），"
            f"已全部加回，避免剥掉正文。该页结构特殊，建议人工抽查。")
        denoised = shelled
    elif n_blocks:
        res["warnings"].append(
            f"STRIPPED_BLOCKS：按 class/id 关键词剥离了 {n_blocks} 个非正文区块"
            f"（正文下降 {(base_len - denoised_len) / max(1, base_len) * 100:.1f}%）")

    # 3. 转 Markdown
    parser = BodyParser()
    try:
        parser.feed(denoised)
        parser.close()
    except Exception as exc:
        res["warnings"].append(f"HTML_PARSE_ERROR：{type(exc).__name__}: {exc}（已尽力输出已解析部分）")

    body = parser.result_body()
    if getattr(parser, "warnings_table_complex", False):
        res["warnings"].append(
            "COMPLEX_TABLE_KEPT_AS_HTML：表格含 colspan/rowspan，Markdown 无法表达，"
            "已保留原始 <table> HTML")

    res["code_blocks"] = parser.code_blocks
    res["tables"] = parser.tables
    res["links"] = parser.links
    res["heading_levels_seen"] = {k: v for k, v in parser.headings.items() if v}

    # 4. 标题归一化：确保全文恰好一个 H1
    title, body = normalize_headings(body, parser.title_candidates,
                                     page_title=extract_page_title(text))

    # 5. 兜底清理控制字符
    # ⚠️ 正常路径下 _render_anchors 已经还原了所有链接占位符，
    #    这里只兜住异常路径（占位符残缺、<a> 未闭合等），保证产出里
    #    绝不留 \x00。代码块内容不走这里（代码要求逐字节保留）。
    if CTRL_RE.search(body):
        n_left = len(CTRL_RE.findall(body))
        body = CTRL_RE.sub("", body)
        res["warnings"].append(
            f"CTRL_CHARS_STRIPPED：清掉了 {n_left} 个残留控制字符"
            f"（链接占位符未能完全还原，可能是 <a> 未闭合或结构异常）。")

    # 标题同样要清干净：它会写进 front matter，带 \x00 会让文件被判定为二进制
    if title:
        title = CTRL_RE.sub("", title).strip() or None

    res["title"] = title
    res["body"] = body
    return res


def extract_page_title(html):
    """
    取 <title> 文本。
    ⚠️ 有些站点的 <title> 里直接塞了链接标记（如
       "\\x00A\\x00https://devin.ai/\\x00Devin, the first autonomous…"），
       不处理就会把 \\x00 带进 front matter 的 title 字段（实测 7 篇中招）。
       这里把锚点还原成链接文本，再清掉残留控制字符。
    """
    m = re.search(r"(?is)<title[^>]*>(.*?)</title>", html)
    if not m:
        return None
    t = htmllib.unescape(m.group(1))
    if "\x00A\x00" in t:
        # 只保留锚文本：标题里不需要 URL
        labels = [x.group(2).strip() for x in ANCHOR_RE.finditer(t)]
        labels = [x for x in labels if x]
        t = " ".join(labels) if labels else ANCHOR_RE.sub(" ", t)
    t = CTRL_RE.sub("", t)
    return norm_inline(t) or None


def normalize_headings(body, candidates, page_title=None):
    """
    标题层级归一化，保证全文恰好一个 "# "（H1），章节落在 ## / ###。
    文章标题判定（按规格）：
      1) 优先 <h1>
      2) 若 <h1> 不存在，或它与 <title>/站名高度重合，则取第一个 <h2>
    其余标题按相对层级降级。
    """
    lines = body.split("\n")
    heading_idx = [(i, len(m.group(1)), m.group(2))
                   for i, ln in enumerate(lines)
                   for m in [re.match(r"^(#{1,6})\s+(.*)$", ln)] if m]
    if not heading_idx:
        # 没有任何标题：用 <title> 或文件名兜底，正文不变
        return (page_title or None), body

    title_idx, title_level, title_text = None, None, None

    h1s = [h for h in heading_idx if h[1] == 1]
    if h1s:
        cand = h1s[0]
        # 与 <title> 高度重合 → 说明这个 h1 其实只是站名/页面名，落到 h2
        if page_title and _too_similar(cand[2], page_title):
            h2s = [h for h in heading_idx if h[1] == 2]
            if h2s:
                cand = h2s[0]
        title_idx, title_level, title_text = cand
    else:
        h2s = [h for h in heading_idx if h[1] == 2]
        if h2s:
            title_idx, title_level, title_text = h2s[0]
        else:
            title_idx, title_level, title_text = heading_idx[0]

    # 相对层级降级：文章标题 → H1；其余标题至少从 H2 起
    out = []
    section_level = 2
    seen_title = False
    for i, ln in enumerate(lines):
        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if not m:
            out.append(ln)
            continue
        level = len(m.group(1))
        if i == title_idx and not seen_title:
            out.append("# " + m.group(2))
            out.append("")
            seen_title = True
            continue
        # 原始层级比标题层级深多少 → 映射到 2..6
        rel = level - (title_level or 1)
        new_level = 2 + max(0, rel)
        if level <= (title_level or 1):
            new_level = section_level
        new_level = min(new_level, 6)
        out.append("#" * new_level + " " + m.group(2))
        out.append("")
    return title_text, strip_ws_lines("\n".join(out))


def _too_similar(a, b):
    """判断两个标题是否高度重合（用于识别「h1 只是站名」的情况）"""
    if not a or not b:
        return False
    na = re.sub(r"[^a-z0-9]+", "", a.lower())
    nb = re.sub(r"[^a-z0-9]+", "", b.lower())
    if not na or not nb:
        return False
    if na == nb:
        return True
    shorter, longer = (na, nb) if len(na) <= len(nb) else (nb, na)
    return len(shorter) >= 6 and shorter in longer


def extract_markdown(text, src_path):
    """archive 里的 .md：本身已是 Markdown，只做标题归一化与清理"""
    res = make_result("md")
    body = text
    res["code_blocks"] = len(re.findall(r"^```", body, re.M)) // 2
    res["links"] = len(re.findall(r"\[[^\]]*\]\([^)]+\)", body))
    res["tables"] = len(re.findall(r"^\|.*\|$", body, re.M))
    title, body = normalize_headings(body, [], page_title=None)
    res["title"] = title
    res["body"] = strip_ws_lines(body)
    return res


def extract_text(text, src_path):
    """archive 里的 .prompt / .txt：纯文本，包成围栏代码块或原样段落"""
    res = make_result("txt")
    title = None
    m = re.search(r"^#\s+(.+)$", text, re.M)
    if m:
        title = m.group(1).strip()
    body = text
    if not m:
        # 没有标题：用首行（截断）当标题，其余作为正文
        first = next((ln.strip() for ln in text.split("\n") if ln.strip()), None)
        title = (first[:80] if first else None)
    res["title"] = title
    res["body"] = strip_ws_lines(body)
    res["links"] = len(re.findall(r"https?://\S+", body))
    return res


def extract_spa(text, src_path):
    """
    官网 SPA：index.html 是 Vite 空壳，正文全在打包 JS 的 JSX 文本节点里。
    正则提取 children:"..." 后，尽力按顺序重建结构（周次标题 / FAQ 问答）。
    """
    res = make_result("spa")
    parts = re.findall(r'children:"((?:[^"\\]|\\.){12,})"', text)
    cleaned = []
    for p in parts:
        try:
            cleaned.append(json.loads('"' + p + '"'))
        except Exception:
            cleaned.append(p.replace('\\"', '"').replace("\\n", " "))
    res["warnings"].append(
        f"SPA_FLAT_TEXT：正文来自打包 JS 的 {len(parts)} 个 JSX 文本节点，"
        f"原始信息是扁平文本片段，没有结构信息；下面的周次/FAQ 结构是按顺序尽力重建的，"
        f"拿不准的地方未强行编造。")
    body, n_head = rebuild_spa_structure(cleaned)
    res["code_blocks"] = 0
    res["links"] = len(re.findall(r"https?://\S+", body))
    res["tables"] = 0
    res["title"] = "CS146S: The Modern Software Developer — 课程官网（Overview / Syllabus / FAQ）"
    return res


def rebuild_spa_structure(parts):
    """按顺序尽力重建：识别 Week N 周次标题、FAQ 问答对"""
    lines = ["# CS146S: The Modern Software Developer — 课程官网", ""]
    n_head = 0
    for raw in parts:
        s = norm_inline(raw)
        if not s:
            continue
        if re.match(r"^(week\s*\d+|week\s*\d+\s*:)", s, re.I):
            lines.append("")
            lines.append("## " + s)
            lines.append("")
            n_head += 1
            continue
        if re.match(r"^(faq|frequently asked questions)$", s, re.I):
            lines.append("")
            lines.append("## " + s)
            lines.append("")
            n_head += 1
            continue
        if s.endswith("?") and len(s) < 200:
            lines.append("")
            lines.append("### " + s)
            lines.append("")
            n_head += 1
            continue
        lines.append(s)
        lines.append("")
    return strip_ws_lines("\n".join(lines)), n_head


# ============================================================ B. PDF 抽取
# ⚠️ 本环节最容易做错的三件事，下面逐一规避：
#    1. 用「有没有 /Subtype /Image」判断图片型 → 有封面图的正常文档会被误判
#    2. 直接在原始字节里搜 /BaseFont → 对象压在 /ObjStm 里时搜到 0 次，
#       于是误判成「无字体 → 图片型」。搜不到 ≠ 不存在。
#    3. 把多个字体的 CMap 全局合并 → 不同子集键冲突，整篇串码

STREAM_RE = re.compile(rb"stream\r?\n")
# 只匹配对象头（不捕获对象体），对象体靠 find(endobj) 定位
OBJ_RE_HEAD = re.compile(rb"(?<![0-9])(\d+)\s+(\d+)\s+obj\b")
NUM_OBJ_RE = re.compile(rb"(\d+)\s+\d+\s+R")


def _refs(body):
    return [int(m.group(1)) for m in NUM_OBJ_RE.finditer(body)]


def decompress_flate(data):
    r"""
    解压 Flate 流。**失败返回 None**，绝不把压缩字节原样吐回去。

    ⚠️ 返回原字节是个隐蔽的坏味道：调用方无法区分「解压成功」和「解压失败」，
       于是【仍被压缩】的字节会一路流到文本抽取，而压缩数据里恰好含 "BT"
       字节，就被误判成「这是内容流」—— 这是 bug 4 的成因。
       所以失败必须返回 None，让调用方明确丢弃。

    ⚠️ /Length 不可信（实测声明 102 字节、按 endstream 实际可解出 8196 字节）。
       调用方应传「stream 到 endstream 的完整块」；zlib 在 EOS 处会自己停住
       并忽略尾部多余数据，所以给足余量是安全的。
    """
    if not data:
        return None
    # 优先严格解压（完整块，无尾部污染时最快最可靠）
    for candidate in (data, data.rstrip(b"\r\n")):
        try:
            return zlib.decompress(candidate)
        except zlib.error:
            pass
        except Exception:
            pass
    # 兜底：解可解前缀（应对尾部被污染）
    try:
        out = zlib.decompressobj().decompress(data)
        if out:
            return out
    except Exception:
        pass
    return None


def decode_stream(raw_stream, body):
    """按 /Filter 解压流；解压失败返回 None（不得把压缩字节当数据用）"""
    if b"FlateDecode" in body:
        return decompress_flate(raw_stream)
    return raw_stream


def slice_stream_payload(raw, body, body_start, body_end, sm):
    r"""
    切出流的载荷字节，返回 (payload, 依据)。

    ⚠️ 完全【不看 /Length】。实测它的值在本项目 PDF 里普遍偏小
       （声明 102、实际能解出 8196），按它硬切会截断 Flate 流，
       zlib 报 invalid distance/literal 错误，把正常文件误判成「损坏」。
       可靠边界只有 endstream（保留关键字，不会出现在压缩数据里）。
    """
    start = body_start + sm.end()
    payload = raw[start:body_end]
    end = payload.find(b"endstream")
    if end >= 0:
        return payload[:end], "endstream"
    return payload, "rest_of_object"


def load_objects(raw, with_streams=False):
    r"""
    把 PDF 还原成 {对象号: {"body":bytes, "stream_raw":bytes, "stream":bytes}}。

    两种来源合并（未压缩的优先）：
      ① 未压缩对象：(\d+) (\d+) obj ... endobj
      ② /Type /ObjStm 对象流：zlib 解压后，按 /N 与 /First 解析出
         「对象号 → 在解压数据中的偏移」，切分出每个被压缩对象

    ⚠️ 这一步不做，后面全是错的：现代 PDF 把字体、ToUnicode 全压进对象流，
       不先解压就在原始字节里搜 /BaseFont 会搜到 0 次。
    """
    objs = {}
    # ⚠️ 对象边界用「正则只匹配对象头，再从 m.end() 找到 endobj」，
    #    不用 (.*?)endobj 非贪婪捕获：
    #    ① 非贪婪会撞上压缩数据/交叉引用表里的 "endobj" 字节，把对象截成半截
    #       （实测对象 2 的 body 只剩 b'0'，导致 BT/字体统计全归零）；
    #    ② 正则捕获组易错：group(2) 是世代号，group(3) 才是对象体。
    #    用 find 定位 endobj 两个坑都避开，也就不需要 blank_stream_bodies 那套补丁了。
    for m in OBJ_RE_HEAD.finditer(raw):
        onum = int(m.group(1))
        bstart = m.end()
        bend = raw.find(b"endobj", bstart)
        if bend < 0:
            bend = min(bstart + 300000, len(raw))
        body = raw[bstart:bend]
        sm = STREAM_RE.search(body)
        entry = {"body": body, "stream_raw": None, "stream": None,
                 "stream_len_source": None}
        if sm:
            data, src = slice_stream_payload(raw, body, bstart, bend, sm)
            entry["stream_raw"] = data
            entry["stream_len_source"] = src
            if with_streams:
                entry["stream"] = decode_stream(data, body)
        objs.setdefault(onum, entry)

    # ② 对象流
    for onum, entry in list(objs.items()):
        body = entry["body"]
        if b"/ObjStm" not in body:
            continue
        sm = STREAM_RE.search(body)
        if not sm:
            continue
        data = entry["stream_raw"]
        if data is None:
            continue          # 拿不到完整块（无 endstream）→ 不当对象流处理
        dec = decompress_flate(data)
        if dec is None:       # 解压失败 → 丢弃，绝不把压缩字节当解压结果
            continue
        mn, mf = re.search(rb"/N\s+(\d+)", body), re.search(rb"/First\s+(\d+)", body)
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
        for i, (cnum, off) in enumerate(pairs):
            start = first + off
            end = (first + pairs[i + 1][1]) if i + 1 < len(pairs) else len(dec)
            if cnum not in objs:          # 未压缩对象优先
                cbody = dec[start:end]
                cs = STREAM_RE.search(cbody)
                centry = {"body": cbody, "stream_raw": None, "stream": None,
                          "stream_len_source": None}
                if cs:
                    cdata = cbody[cs.end():]
                    ces = cdata.find(b"endstream")
                    if ces >= 0:
                        cdata = cdata[:ces]
                    centry["stream_raw"] = cdata
                    centry["stream_len_source"] = "endstream" if ces >= 0 else "rest_of_object"
                    if with_streams:
                        centry["stream"] = decode_stream(cdata, cbody)
                objs[cnum] = centry
    return objs


# ---------- ToUnicode CMap ----------
def parse_cmap(data):
    """
    解析 ToUnicode CMap 的 beginbfchar / beginbfrange 块 → {字符码: unicode 串}
    ⚠️ 每个字体必须用【它自己】的 CMap；全局合并会因多个子集键冲突而串码。
    """
    mapping = {}

    def to_unicode(hexstr):
        try:
            b = bytes.fromhex(hexstr)
        except ValueError:
            return ""
        try:
            return b.decode("utf-16-be")
        except UnicodeDecodeError:
            return b.decode("latin-1", "replace")

    for blk in re.findall(rb"beginbfchar(.*?)endbfchar", data, re.S):
        for src, dst in re.findall(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", blk):
            mapping[int(src, 16)] = to_unicode(dst.decode())

    for blk in re.findall(rb"beginbfrange(.*?)endbfrange", data, re.S):
        # <lo> <hi> <dstStart>
        for lo, hi, dst in re.findall(
                rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", blk):
            lo_i, hi_i = int(lo, 16), int(hi, 16)
            if hi_i - lo_i > 65535:
                continue
            base = to_unicode(dst.decode())
            for k in range(lo_i, hi_i + 1):
                if base:
                    mapping[k] = base if k == lo_i else base[:-1] + chr(ord(base[-1]) + (k - lo_i))
        # <lo> <hi> [ <d1> <d2> ... ]
        for lo, hi, arr in re.findall(
                rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*\[(.*?)\]", blk, re.S):
            vals = re.findall(rb"<([0-9A-Fa-f]+)>", arr)
            for i, v in enumerate(vals):
                code = int(lo, 16) + i
                if code <= int(hi, 16):
                    mapping[code] = to_unicode(v.decode())
    return mapping


def build_fonts(objs):
    """
    构建 {字体资源名: 字体信息}。
    ⚠️ 同时收集 /Type /Font 且带 /BaseFont 的字体（用于类型判定），
       以及每个字体自己的 CMap / Type3 字形名映射。
    """
    fonts = {}
    fonts_with_basefont = 0
    font_obj_has_basefont = set()

    for onum, entry in objs.items():
        body = entry["body"]
        if not re.search(rb"/Type\s*/Font", body):
            continue
        if b"/BaseFont" in body:
            fonts_with_basefont += 1
            font_obj_has_basefont.add(onum)

    # 资源名 → 字体对象号
    # ⚠️ 不要写 rb"/Font\s*<<(.*?)>>"：非贪婪的 >> 会在字体字典【内部】的
    #    第一个 >> 处就停下，导致只收到极少数字体（实测 assessment 18/53、
    #    anthropic 7/284、codex 2/279），于是大量文本因为"查不到字体"解不出来。
    #    字体字典里本就内嵌 << /Type/Font ... >>，所以按引用扫全对象最稳。
    name_to_obj = {}
    for entry in objs.values():
        for fname, fnum in re.findall(
                rb"/([A-Za-z0-9_.\-+]+)\s+(\d+)\s+\d+\s+R", entry["body"]):
            name_to_obj.setdefault(fname.decode("latin-1"), int(fnum))

    # 所有字体的 CMap（按对象号）—— 不受"资源名有没有被扫到"影响
    obj_to_cmap = {}
    for onum, entry in objs.items():
        tm = re.search(rb"/ToUnicode\s+(\d+)\s+\d+\s+R", entry["body"])
        if not tm:
            continue
        tentry = objs.get(int(tm.group(1)))
        if not tentry:
            continue
        stream = tentry.get("stream")
        if stream is None:
            stream = get_stream(tentry["body"])
        if stream and b"beginbf" in stream:
            obj_to_cmap[onum] = parse_cmap(stream)

    for name, fnum in name_to_obj.items():
        entry = objs.get(fnum)
        if not entry:
            continue
        body = entry["body"]
        info = {"obj": fnum, "has_basefont": fnum in font_obj_has_basefont,
                "cmap": obj_to_cmap.get(fnum, {}),
                "code_to_name": {}, "is_type3": b"/CharProcs" in body}
        # 是否双字节字符码：Type0 复合字体通常是 Identity-H（2 字节）
        info["two_byte"] = bool(re.search(rb"/Subtype\s*/Type0", body))
        # Type3 的 /Encoding /Differences：字符码 → 字形名
        dm = re.search(rb"/Differences\s*\[(.*?)\]", body, re.S)
        if dm:
            cur = None
            for tok in re.findall(rb"(\d+)|/([A-Za-z0-9_.\-+]+)", dm.group(1)):
                if tok[0]:
                    cur = int(tok[0])
                elif tok[1] and cur is not None:
                    info["code_to_name"][cur] = tok[1].decode("latin-1")
                    cur += 1
        # Type3 字形名集合（/CharProcs << /C0 n 0 R ... >>）
        cp = re.search(rb"/CharProcs\s*<<(.*?)>>", body, re.S)
        if cp:
            info["glyph_names"] = [g.decode("latin-1") for g in
                                   re.findall(rb"/([A-Za-z0-9_.\-+]+)\s+\d+\s+\d+\s+R", cp.group(1))]
        fonts[name] = info

    return fonts, fonts_with_basefont


# ---------- 内容流 token 扫描 ----------
TOKEN_RE = re.compile(
    rb"\[(?:\\.|[^\]\\])*\]"          # [ ... ]  数组（TJ）
    rb"|\((?:\\.|[^)\\])*\)"          # ( ... )  字面串
    rb"|<[0-9A-Fa-f\s]*>"             # < ... >  十六进制串
    rb"|/[^\s/\[\]()<>{}]+"           # /Name
    rb"|-?\d+\.?\d*"                  # 数字
    rb"|[A-Za-z'\"*]+",               # 算子
    re.S)


def unescape_pdf_string(raw):
    """处理 PDF 字面串里的转义与八进制"""
    out = bytearray()
    i = 0
    while i < len(raw):
        c = raw[i]
        if c == 0x5C and i + 1 < len(raw):      # backslash
            nxt = raw[i + 1]
            simple = {0x6E: 10, 0x72: 13, 0x74: 9, 0x62: 8, 0x66: 12,
                      0x28: 0x28, 0x29: 0x29, 0x5C: 0x5C}
            if nxt in simple:
                out.append(simple[nxt]); i += 2; continue
            if 0x30 <= nxt <= 0x37:             # 最多三位八进制
                j = i + 1
                digits = ""
                while j < len(raw) and len(digits) < 3 and 0x30 <= raw[j] <= 0x37:
                    digits += chr(raw[j]); j += 1
                out.append(int(digits, 8) & 0xFF); i = j; continue
            if nxt in (10, 13):                 # 续行
                i += 2; continue
            out.append(nxt); i += 2; continue
        out.append(c); i += 1
    return bytes(out)


def font_obj_number(body):
    """字体对象体里的 /FontDescriptor 引用号（用于排除字体流）"""
    m = re.search(rb"/FontDescriptor\s+(\d+)\s+\d+\s+R", body)
    return int(m.group(1)) if m else None


def garbage_score(text):
    r"""
    乱码率（0.0~1.0）：估计文本里有多大比例是「不可读的乱码」。

    ⚠️ 为什么必须有这个指标：词数会骗人。参考实现曾从 anthropic 抽出
       979 个「英文词」，看着像成功，实际因为字体 CMap 只建了 3/25 个，
       输出全是 "Ak tm ctece  Amttz e tAem em" 这种乱码。
       只靠词数验收，会把不可恢复的文件误判成可翻译。

    判据：一行若同时满足
      · 至少有 3 个英文词
      · 一个常见英文停用词都没有
      · 含 5 个以上连续辅音（英文里几乎不可能出现）
    才算乱码行。
    ⚠️ 该判据偏保守：正常散文里出现 5 连辅音的专有名词/技术词
       （如 "workflows"、"ANTHROP\C"）可能被计入，因此乱码率偏高时
       应结合正文抽样人工确认，不要只看这一个数字。
    判定：<10% 可读 / 10-35% 部分可读 / >35% 乱码
    """
    lines = [l for l in text.split("\n") if len(l.strip()) > 15]
    if not lines:
        return 1.0
    common = set("the of and to in is are that for with as on be this by it from or".split())
    bad = 0
    for l in lines:
        words = re.findall(r"[A-Za-z]{2,}", l)
        if len(words) < 3:
            continue
        if sum(1 for w in words if w.lower() in common) == 0 \
           and re.search(r"[bcdfghjklmnpqrstvwxz]{5,}", l.lower()):
            bad += 1
    return bad / max(1, len(lines))


def stopword_ratio(text):
    """
    常见英文停用词在正文词数中的占比。
    正常英文散文约 0.20~0.30；字母替换式乱码接近 0。

    ⚠️ 为什么需要这个独立指标：garbage_score 会被这种乱码骗过去。
       实测 how-openai-uses-codex.pdf 抽出的文本全是
       "eIOne sOnwdCgsOos2 / MwxeIegxeAn Cgxrgo" 这类字母替换乱码，
       但 garbage_score 只有 0.1594（判为"部分可读"），因为它是靠
       「5 连辅音」判据的，而乱码里的伪词都很短、不含长辅音串。
       真正靠得住的信号是停用词占比：这篇实测 0/682 = 0.0%。
    """
    lines = [l for l in text.split("\n") if len(l.strip()) > 15]
    common = set("the of and to in is are that for with as on be this by it from or "
                 "we you they this not but its our your their his her will can may".split())
    words = [w.lower() for l in lines for w in re.findall(r"[A-Za-z]{2,}", l)]
    if not words:
        return 0.0
    return sum(1 for w in words if w in common) / len(words)


def is_recoverable_text(text, min_stopword_ratio=0.05):
    """
    判断抽出的文本是否【真的可读】。
    返回 (recoverable, stopword_ratio)。
    阈值 0.05 取得很保守（正常散文 0.20+、乱码 0.00），
    宁可漏判也不误伤合法译文。
    """
    r = stopword_ratio(text)
    return r >= min_stopword_ratio, round(r, 4)


def garbage_verdict(rate):
    """乱码率 → 可读性判定文案"""
    if rate < 0.10:
        return "可读"
    if rate <= 0.35:
        return "部分可读"
    return "乱码"


def decode_with_font(font, codes):
    """
    按【当前字体】把字符码序列解成文本。
    优先级：ToUnicode CMap → Type3 字形名(/Differences) → 简单字体的 ASCII 兜底

    ⚠️ Type3 且无任何映射时【不做 ASCII 猜测】：
       它的字符码是字形索引（0,1,2...），套 ASCII 只会产出
       "rZO$Z'j_UNVOMN{" 这种乱码 —— 那是在编内容，违反纪律 B。
       正确处理是留空 + 报 undecoded，让报告如实说「客观不可恢复」。
    """
    cmap = font.get("cmap") if font else None
    c2n = font.get("code_to_name") if font else None
    is_type3 = bool(font and font.get("is_type3"))
    out = []
    missing = 0
    for code in codes:
        ch = None
        if cmap and code in cmap:
            ch = cmap[code]
        if ch is None and c2n and code in c2n:
            # Type3：字符码 → 字形名(/C0 /C12) → 再按字形名编号查 CMap
            glyph = c2n[code]
            if cmap:
                gm = re.fullmatch(r"C(\d+)", glyph)
                if gm and int(gm.group(1)) in cmap:
                    ch = cmap[int(gm.group(1))]
        if ch is None and not is_type3 and font is not None:
            # 只在【确认是简单字体】时做 ASCII 兜底。
            # ⚠️ font is None 表示连字体资源都没解析出来，此时字节编码未知，
            #    再套 ASCII 就是猜 —— 会产出 "rZO$Z'j_UNVOMN{" 这类乱码。
            if 32 <= code < 127:
                ch = chr(code)
            elif code > 255 and 32 <= (code & 0xFF) < 127:
                ch = chr(code & 0xFF)
        if ch is None:
            if code in (9, 10, 13):
                ch = " "
            else:
                missing += 1
                ch = ""
        out.append(ch)
    return "".join(out), missing


def codes_from_string(s, font):
    """把一个 PDF 文本串切成字符码：多字节字体按 2 字节大端，否则按单字节"""
    if s.startswith(b"<") and s.endswith(b">"):
        hexs = re.sub(rb"[^0-9A-Fa-f]", b"", s[1:-1])
        if len(hexs) % 2:
            hexs += b"0"
        try:
            raw = bytes.fromhex(hexs.decode("ascii"))
        except ValueError:
            raw = b""
        if font and font.get("two_byte"):
            return [int.from_bytes(raw[i:i + 2], "big") for i in range(0, len(raw) - 1, 2)]
        return list(raw)
    raw = unescape_pdf_string(s[1:-1])
    if font and font.get("two_byte"):
        return [int.from_bytes(raw[i:i + 2], "big") for i in range(0, len(raw) - 1, 2)]
    return list(raw)


def extract_stream_text(stream, fonts):
    """
    扫描一条内容流，抽文本。
    处理三个关键点：
      · /F1 12 Tf 切换【当前字体】—— 必须按当前字体查它自己的 CMap
      · TJ 数组里的数字是字距调整：大负数(< -100) 代表空格，小负数是微调
      · Td/TD/T*/Tm 作为换行/换段信号
    """
    tokens = TOKEN_RE.findall(stream)
    cur_font = None
    lines = []
    buf = []
    total_missing = 0

    def flush_line():
        nonlocal buf
        text = "".join(buf).strip()
        if text:
            lines.append(text)
        buf = []

    for i, tok in enumerate(tokens):
        if tok == b"Tf":
            # 往前的 /Name 就是字体资源名
            for j in range(i - 1, max(-1, i - 6), -1):
                if tokens[j].startswith(b"/"):
                    cur_font = fonts.get(tokens[j][1:].decode("latin-1"))
                    break
            continue
        if tok in (b"Td", b"TD", b"T*", b"ET", b"BT"):
            flush_line()
            continue
        if tok in (b"Tj", b"'", b'"'):
            s = tokens[i - 1] if i > 0 else b""
            if s[:1] in (b"(", b"<"):
                txt, miss = decode_with_font(cur_font, codes_from_string(s, cur_font))
                buf.append(txt)
                total_missing += miss
            continue
        if tok == b"TJ":
            arr = tokens[i - 1] if i > 0 else b""
            if arr.startswith(b"["):
                for part in re.findall(rb"\((?:\\.|[^)\\])*\)|<[0-9A-Fa-f\s]*>|-?\d+\.?\d*", arr, re.S):
                    if part[:1] in (b"(", b"<"):
                        txt, miss = decode_with_font(cur_font, codes_from_string(part, cur_font))
                        buf.append(txt)
                        total_missing += miss
                    else:
                        try:
                            adj = float(part)
                        except ValueError:
                            continue
                        # ⚠️ 不处理这个，单词会全黏在一起（thecodereviewprocess）
                        if adj < -100:
                            buf.append(" ")
            continue
    flush_line()
    return lines, total_missing


def get_stream(obj_body):
    """
    从一个【对象体】里取解压后的流；失败返回 None。
    ⚠️ 从 body 里重新定位 stream…endstream，不用预切的 stream_raw ——
       stream_raw 是我自己按第一个 stream 关键字切的，对多流对象会漏，
       导致内容流数被严重低估（实测 assessment 只认出 1 个，实际 16 个）。
    """
    sm = re.search(rb"stream\r?\n", obj_body)
    if not sm:
        return None
    end = obj_body.find(b"endstream", sm.end())
    blob = obj_body[sm.end():end] if end >= 0 else obj_body[sm.end():]
    return decompress_flate(blob)


def collect_content_streams(objs):
    r"""
    收集【可信】的内容流，返回 [(对象号, 解压后的字节)]。

    ⚠️ 判断顺序至关重要：**先解压成功，再检查 BT 算子**。
       反过来（先查 BT 再解压）会让【仍被压缩】的字节混进来 ——
       压缩数据里恰好含 "BT" 字节是巧合，不是内容流的证据。
       实测 AI 论文的 obj 134/170 以 x\xda 开头（仍压缩），
       却被判成「含 BT 的内容流」，于是抽出上万个解不开的字符码。

    ⚠️ 解压失败的流直接丢弃，不做「扫描所有流」的兜底 ——
       那会把 Type3 字体的字形程序流当正文，产出满屏乱码。
    """
    streams = []
    for num, entry in objs.items():
        body = entry["body"]
        data = get_stream(body)
        if data is None:                    # 解压失败 → 丢弃，绝不当文本用
            continue
        if b"BT" not in data:
            continue
        if b"endchar" in data:              # Type3 字形程序，不是内容流
            continue
        streams.append((num, data))
    return streams


def is_readable_line(line):
    """可读行：英文字母占比 > 60% 且含 >= 4 个英文词"""
    if not line:
        return False
    letters = sum(1 for c in line if c.isalpha())
    if len(line) == 0 or letters / len(line) <= 0.60:
        return False
    return len(re.findall(r"[A-Za-z]{2,}", line)) >= 4


def children_of(body):
    """取对象体里 /Kids 的引用号列表"""
    m = re.search(rb"/Kids\s*\[(.*?)\]", body, re.S)
    return _refs(m.group(1)) if m else []


def page_refs_in_order(objs):
    r"""
    按【文档顺序】返回页面对象号列表。
    优先走页面树：/Type /Catalog → /Pages(根) → 递归 /Kids；
    页面树缺失或成环时，退化为「按对象号排序的 /Type /Page」。
    ⚠️ 直接用 /Type /Page 的对象号排序，在多数字典顺序写的 PDF 里恰好对，
       但那只是巧合；真正可靠的顺序只有页面树能给。
    """
    roots = [n for n, e in objs.items() if b"/Type" in e["body"]
             and re.search(rb"/Type\s*/Pages", e["body"])]
    # 有 /Parent 的不是根
    roots = [n for n in roots if b"/Parent" not in objs[n]["body"]]
    if not roots:
        roots = sorted(n for n, e in objs.items()
                       if re.search(rb"/Type\s*/Pages", e["body"]))
    order, visited = [], set()

    def walk(n):
        if n in visited or len(order) > 20000:
            return
        visited.add(n)
        e = objs.get(n)
        if not e:
            return
        body = e["body"]
        kids = children_of(body)
        if kids:
            for k in kids:
                walk(k)
        elif re.search(rb"/Type\s*/Page[^s]", body):
            order.append(n)

    for r in roots:
        walk(r)
    if order:
        return order, "page_tree"
    # 兜底
    return sorted(n for n, e in objs.items()
                  if re.search(rb"/Type\s*/Page[^s]", e["body"])), "object_number_fallback"


def extract_pdf(text, src_path):
    """
    PDF → Markdown。
    先按规格判定类型（在解压后的对象集合上统计），再按页抽文本。
    """
    res = make_result("pdf")
    # ⚠️ 绝对不要对 PDF 原始字节做 \r\n → \n 规范化！
    #    Flate 压缩数据里出现 0x0D(\r) 是很常见的，替换会把流改坏，
    #    zlib 报 "invalid distance too far back" / "incorrect data check"，
    #    于是【把好文件当成坏文件】—— 实测 assessment 的内容流因此
    #    从 16 个掉到 1 个。STREAM_RE 已经是 rb"stream\r?\n"，本就兼容 \r\n。
    raw = open(src_path, "rb").read()

    objs = load_objects(raw, with_streams=True)

    # ---- 第 2 步：在解压后的对象集合上统计指标
    bt_operators = 0
    content_stream_count = 0
    for entry in objs.values():
        body = entry["body"]
        hits = len(re.findall(rb"\bBT\b", body))
        if entry.get("stream"):
            hits += len(re.findall(rb"\bBT\b", entry["stream"]))
        bt_operators += hits
        if entry.get("stream") and re.search(rb"\bBT\b", entry["stream"]) \
                and b"endchar" not in entry["stream"]:
            content_stream_count += 1

    blob = b"\n".join(e["body"] for e in objs.values())
    for e in objs.values():
        if e.get("stream"):
            blob += b"\n" + e["stream"]
    has_hidden_ocr = b"HiddenHorzOCR" in blob
    has_type3 = b"/CharProcs" in blob
    embedded_images = len(re.findall(rb"/Subtype\s*/Image", blob))
    fonts, fonts_with_basefont = build_fonts(objs)
    fonts_total = sum(1 for e in objs.values() if re.search(rb"/Type\s*/Font", e["body"]))

    # ---- 第 3 步：按固定顺序判定类型
    if bt_operators == 0:
        pdf_type = "image_only"
    elif fonts_with_basefont > 0:
        pdf_type = "text"
    elif has_hidden_ocr:
        pdf_type = "ocr_text_layer"
    elif has_type3:
        pdf_type = "type3_vector"
    else:
        pdf_type = "unknown_needs_review"

    res["extra"].update({
        "pdf_type": pdf_type,
        "bt_operators": bt_operators,
        "content_streams": content_stream_count,
        "fonts_total": fonts_total,
        "fonts_with_basefont": fonts_with_basefont,
        "embedded_images": embedded_images,
        "has_hidden_ocr": has_hidden_ocr,
        "has_type3": has_type3,
    })

    if pdf_type == "image_only":
        res["warnings"].append(
            "IMAGE_ONLY：解压后的对象集合中没有任何文本绘制算子（BT 出现 0 次），"
            "页面正文是内嵌图片，无文本层。不写占位文件，需 OCR 后再来。")
        res["extra"]["readable_line_ratio"] = 0.0
        return res

    # ---- 按【页面树顺序】取内容流
    # ⚠️ 只认「页面对象 → /Contents 引用」这条可靠路径。
    #    曾用「按对象号扫描所有含 BT 的流」兜底，结果把 Type3 字体的
    #    字形程序流当成了正文，抽出 21,203 个解不开的字符码和满屏乱码
    #    （".hMyv^+aEt|" 这种）。那是把「搜错地方」当成了「搜到」。
    #    拿不到可靠的内容流引用时，正确答案是承认抽不出来，而不是猜。
    page_order, order_src = page_refs_in_order(objs)
    page_contents = []
    for pnum in page_order:
        body = objs[pnum]["body"]
        cm = re.search(rb"/Contents\s*(\[[^\]]*\]|\d+\s+\d+\s+R)", body, re.S)
        refs = _refs(cm.group(1)) if cm else []
        if refs:
            page_contents.append(refs)

    # ---- 收集可信内容流（先解压成功，再查 BT）
    content_streams = collect_content_streams(objs)
    trusted_ids = {num for num, _ in content_streams}
    stream_by_id = dict(content_streams)

    all_lines = []
    total_missing = 0
    # 优先按页面树的 /Contents 引用取，保证页序正确
    used = set()
    for refs in page_contents:
        for r in refs:
            if r in stream_by_id and r not in used:
                used.add(r)
                ls, miss = extract_stream_text(stream_by_id[r], fonts)
                all_lines.extend(ls)
                total_missing += miss
    # 内容流存在但页面树没引用到（页树不完整）→ 按对象号补齐，仍是可信流
    for num, data in sorted(stream_by_id.items()):
        if num in used:
            continue
        ls, miss = extract_stream_text(data, fonts)
        all_lines.extend(ls)
        total_missing += miss
        if not page_contents:
            break     # 没有页面树时不补齐，避免顺序错乱与噪声放大

    skipped_non_content = sum(
        1 for num, e in objs.items()
        if e.get("stream_raw") and num not in trusted_ids)

    res["extra"]["content_streams_trusted"] = len(content_streams)
    res["extra"]["pages_with_contents"] = len(page_contents)
    res["extra"]["page_order_source"] = order_src
    res["extra"]["skipped_non_content_streams"] = skipped_non_content
    if not page_contents:
        res["warnings"].append(
            "NO_PAGE_TREE：无法从对象集合还原页面树（/Type /Page 数为 0），"
            "页面树的 /Contents 引用不可用；已改用【先解压成功再查 BT】的可信流集合，"
            "页序可能与原文档略有出入。")

    if not page_contents and not content_streams:
        res["warnings"].append(
            "NO_CONTENT_STREAM：没有任何流能同时满足「解压成功」与「含 BT 算子」，"
            "本文件正文不可恢复。已拒绝用「扫描压缩字节」的方式凑内容。")

    # ---- Type3 且无 ToUnicode：字符【客观不可恢复】，必须说清而不是输出乱码
    type3_fonts = [f for f in fonts.values() if f.get("is_type3")]
    type3_no_cmap = [f for f in type3_fonts if not f.get("cmap")]
    res["extra"]["type3_fonts"] = len(type3_fonts)
    res["extra"]["type3_fonts_without_tounicode"] = len(type3_no_cmap)
    res["extra"]["page_order_source"] = order_src
    res["extra"]["skipped_non_content_streams"] = skipped_non_content

    if type3_no_cmap:
        res["warnings"].append(
            f"TYPE3_ENCODING_INCOMPLETE：该 PDF 有 {len(type3_no_cmap)} 个 Type3 字体"
            f"既没有 /ToUnicode、也没有可用的 /Encoding /Differences，"
            f"字形名是 /C0 /C1 这类匿名编号，**没有到 Unicode 的映射关系**，"
            f"因此这些字符客观不可恢复。已按纪律留空，绝不猜测补全。"
            f"（这类 PDF 需要 OCR 或原始文本才能翻译）")

    readable = sum(1 for ln in all_lines if is_readable_line(ln))
    ratio = (readable / len(all_lines)) if all_lines else 0.0
    res["extra"]["readable_lines"] = readable
    res["extra"]["total_lines"] = len(all_lines)
    res["extra"]["readable_line_ratio"] = round(ratio, 4)
    res["extra"]["undecoded_codes"] = total_missing

    # ---- 独立可读性判据：停用词占比
    # ⚠️ 不能只信 garbage_score。实测 codex 那份抽出的全是字母替换乱码
    #    （"eIOne sOnwdCgsOos2"），garbage_score 只有 0.1594（判"部分可读"），
    #    因为它靠「5 连辅音」判据，而乱码的伪词都短、没有长辅音串。
    #    停用词占比是可靠信号：正常散文 0.20+，乱码 0.00（实测 0/682）。
    sample = "\n".join(all_lines)
    recoverable, sw_ratio = is_recoverable_text(sample)
    res["extra"]["stopword_ratio"] = sw_ratio
    if not recoverable and len(sample) > 200:
        res["extra"]["unrecoverable_garbled_text"] = True
        res["warnings"].append(
            f"GARBLED_TEXT_UNRECOVERABLE：抽出的文本里常见英文停用词占比仅 "
            f"{sw_ratio*100:.1f}%（正常英文散文约 20-30%），判定为字母替换式乱码，"
            f"正文【不可恢复】。根因：Type3 矢量字形缺少可控的 /ToUnicode 映射，"
            f"字符码被错误地套用了 ASCII。已按纪律不输出乱码。")

    # Type3 无 ToUnicode 且几乎全不可解 → 如实判定「不可恢复」，不冒充成功
    if type3_no_cmap and ratio < 0.50:
        res["extra"]["unrecoverable_type3"] = True
        res["warnings"].append(
            "TYPE3_UNRECOVERABLE：判定为 type3_vector 且字体缺失 Unicode 映射，"
            "抽出的文本不可读（可读行比例 "
            f"{ratio*100:.1f}%）。本文件的正文【不可恢复】，"
            "不应进入翻译环节；需 OCR 或改用带文本层的原始版本。")

    # 文本层存在但【没有可用字体映射】时，硬抽只会产出乱码：
    # ⚠️ 这正是 anthropic 那份的实际情况 —— /Font 资源字典与页面树所在的对象流
    #    已损坏，字体 CMap 全部拿不到，21,203 个字符码解不开。
    #    此时如实标记不可恢复，而不是把乱码当作抽取成功交给下游。
    undecodable_ratio = (total_missing / max(1, total_missing + sum(len(l) for l in all_lines)))
    if (not res["extra"].get("unrecoverable_type3")
            and not page_contents):
        res["extra"]["unrecoverable_no_page_tree"] = True
        res["extra"]["fonts_without_cmap"] = sum(1 for f in fonts.values() if not f.get("cmap"))
    elif (not res["extra"].get("unrecoverable_type3")
            and ratio < 0.05 and undecodable_ratio > 0.80):
        res["extra"]["fonts_without_cmap"] = sum(1 for f in fonts.values() if not f.get("cmap"))
        res["extra"]["unrecoverable_no_font_mapping"] = True
        res["warnings"].append(
            f"UNRECOVERABLE_NO_FONT_MAPPING：该 PDF 有文本绘制算子（BT={bt_operators}），"
            f"但可用字体仅有 {len(fonts)} 个、且没有任何 /ToUnicode 映射，"
            f"{total_missing:,} 个字符码无法解码（可读行比例 {ratio*100:.1f}%）。"
            f"根因是被压缩的对象流（/ObjStm）损坏，"
            f"字体资源字典与页面树未能还原。**正文不可恢复**，"
            f"已按纪律不输出乱码、不写占位文件。需原始版本或 OCR。")

    if total_missing:
        res["warnings"].append(
            f"UNDECODED_CODES：有 {total_missing} 个字符码在对应字体的 CMap 里找不到映射，"
            f"已按纪律留空，未做任何猜测补全。"
            f"（Type3/字体子集未提供完整 ToUnicode 时会发生）")

    body_md = "\n\n".join(all_lines)
    title = None
    for ln in all_lines[:40]:
        if is_readable_line(ln) and 3 <= len(ln) <= 120:
            title = ln
            break
    if not title:
        title = os.path.splitext(os.path.basename(src_path))[0]
        res["warnings"].append("TITLE_FALLBACK：未能从正文中识别出可靠标题，已用文件名兜底。")
    res["title"] = title
    res["body"] = strip_ws_lines(f"# {title}\n\n{body_md}") if body_md else ""
    res["links"] = len(re.findall(r"https?://\S+", body_md))
    return res


# ============================================================ 分派表
# ⚠️ 格式差异只在这一层消化；下游 chunk.py 不应出现任何格式解析逻辑
EXTRACTORS = {
    ".html": extract_html,
    ".htm": extract_html,
    ".pdf": extract_pdf,
    ".js": extract_spa,
    ".md": extract_markdown,
    ".markdown": extract_markdown,
    ".txt": extract_text,
    ".prompt": extract_text,
}


def extractor_for(path):
    return EXTRACTORS.get(os.path.splitext(path)[1].lower())


# ============================================================ 归档目录布局探测
def resolve_archive_root(archive_dir, legacy_dirname="archive"):
    """
    定位抓取归档的实际数据根。
    现在归档固定在 data/fetched/，但保留对两种历史布局的兼容：
      · 曾经 archive/archive/<域名>/（整体移动目录时多套了一层）
      · 也曾叫 archive/
    """
    root = archive_dir
    if not os.path.isdir(root):
        return root
    for _ in range(3):
        subs = [d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))]
        has_files = any(os.path.isfile(os.path.join(root, f)) for f in os.listdir(root))
        # 没有文件、且唯一子目录还叫 fetched/archive 时，再下一层
        if not has_files and len(subs) == 1 and subs[0] in (legacy_dirname, "fetched"):
            root = os.path.join(root, subs[0])
            continue
        break
    return root


def load_sidecar_meta(data_path):
    """读同名 .meta.json（archive 文件的 origin_url 来源）"""
    mp = data_path + ".meta.json"
    if not os.path.isfile(mp):
        return {}
    try:
        with open(mp, encoding="utf-8", errors="replace") as f:
            return json.load(f)
    except Exception:
        return {}


# ============================================================ 工作计划
def build_plan(manifest):
    """
    选取要处理的条目（不硬编码文件名）：
      · translatable=true  → 正常处理
      · translatable=null  → 也要处理：旧体检把两份 text 型 PDF 误判成
                             font_encoding_broken 并给了 null，跳过它们就
                             永远无法纠正判定、也无法回填。
      · translatable=false → 跳过（确认不需要翻译 / 已判定不可恢复）
    """
    plan = []

    if manifest and manifest.get("items"):
        for it in manifest["items"]:
            if it.get("translatable") is False and it.get("status") == "not_applicable":
                continue      # 确认不需要翻译（如中文原生文档）
            # ⚠️ 不要用「上一次的 status」做跳过条件：
            #    首次运行会把不可恢复的 PDF 标成 type3_encoding_unrecoverable，
            #    若据此跳过，第二次运行条目数就少一条（55→54），报告不再幂等。
            #    判定必须每次都重新产出，结果自然稳定。
            lp = (it.get("local_path") or "").replace("/", os.sep)
            path = os.path.join(BASE_DIR, lp) if not os.path.isabs(lp) else lp
            if os.path.isdir(path):
                # 官网 SPA：正文在打包 JS 里
                js = os.path.join(path, "assets", "index-CgRb4FxC.js")
                if os.path.isfile(js):
                    plan.append({"id": it["id"], "path": js, "kind": "manifest",
                                 "origin_url": it.get("origin_url"),
                                 "title_hint": it.get("title")})
                else:
                    plan.append({"id": it["id"], "path": path, "kind": "manifest",
                                 "origin_url": it.get("origin_url"),
                                 "title_hint": it.get("title"), "error":
                                 f"目录里找不到正文 JS（{js}）"})
                continue
            if os.path.isfile(path):
                plan.append({"id": it["id"], "path": path, "kind": "manifest",
                             "origin_url": it.get("origin_url"),
                             "title_hint": it.get("title")})
    else:
        for d in (PAGES_DIR, PDFS_DIR):
            if not os.path.isdir(d):
                continue
            for fn in sorted(os.listdir(d)):
                p = os.path.join(d, fn)
                if os.path.isfile(p) and extractor_for(p):
                    plan.append({"id": os.path.splitext(fn)[0], "path": p,
                                 "kind": "manifest", "origin_url": None,
                                 "title_hint": None})

    # ---- archive/ 里抓回来的文件（不在 manifest 里，但磁盘上确实有内容）
    archive_root = resolve_archive_root(ARCHIVE_DIR, ARCHIVE_DIRNAME)
    if os.path.isdir(archive_root):
        # 已被 manifest 覆盖的文件（按 sha256）→ 不重复登记
        known_sha = {}
        for it in (manifest or {}).get("items", []):
            lp = (it.get("local_path") or "").replace("/", os.sep)
            p = os.path.join(BASE_DIR, lp) if lp else None
            if p and os.path.isfile(p):
                try:
                    known_sha[sha256_file(p)] = it["id"]
                except OSError:
                    pass
        for dirpath, _dirs, files in os.walk(archive_root):
            for fn in sorted(files):
                if fn.endswith(".meta.json") or fn.startswith("."):
                    continue
                p = os.path.join(dirpath, fn)
                if not extractor_for(p):
                    continue
                domain = os.path.basename(dirpath)
                digest = sha256_file(p)
                dup_of = known_sha.get(digest)
                if dup_of:
                    # 与 materials/ 里的原件字节相同 → 跳过，如实记录，不算丢失
                    plan.append({"id": f"archive-{domain}-{os.path.splitext(fn)[0]}",
                                 "path": p, "kind": "archive-dup", "origin_url": None,
                                 "title_hint": None, "dup_of": dup_of,
                                 "error": f"与 manifest 条目 {dup_of} 的源文件 sha256 完全相同，"
                                          f"已跳过以免重复产出（内容不丢）"})
                    continue
                meta = load_sidecar_meta(p)
                plan.append({"id": f"archive-{domain}-{os.path.splitext(fn)[0]}",
                             "path": p, "kind": "archive",
                             "origin_url": meta.get("origin_url"),
                             "title_hint": None})
    return plan


# ============================================================ 写出
def front_matter(res, src_path, origin_url, src_sha):
    """按格式契约生成 YAML front matter"""
    lines = ["---"]
    lines.append(f"source_file: {yaml_scalar(os.path.relpath(src_path, BASE_DIR).replace(os.sep, '/'))}")
    lines.append(f"origin_url: {yaml_scalar(origin_url)}")
    lines.append(f"title: {yaml_scalar(res.get('title'))}")
    lines.append(f"extract_method: {yaml_scalar(res.get('format'))}")
    warns = res.get("warnings") or []
    if warns:
        lines.append("extract_warnings:")
        for w in warns:
            lines.append(f"  - {yaml_escape(w)}")
    else:
        lines.append("extract_warnings: []")
    lines.append(f"src_sha256: {yaml_scalar(src_sha)}")
    lines.append(f"chars: {int(res.get('chars') or 0)}")
    lines.append(f"code_blocks: {int(res.get('code_blocks') or 0)}")
    lines.append(f"tables: {int(res.get('tables') or 0)}")
    lines.append(f"links: {int(res.get('links') or 0)}")
    lines.append(f"garbage_rate: {res.get('garbage_rate', 1.0)}")
    if res.get("heading_levels_seen"):
        lines.append("heading_levels_seen:")
        # 固定顺序，保证幂等
        for k in ("h1", "h2", "h3", "h4", "h5", "h6"):
            if k in res["heading_levels_seen"]:
                lines.append(f"  {k}: {res['heading_levels_seen'][k]}")
    extra = res.get("extra") or {}
    if res.get("format") == "pdf":
        lines.append(f"pdf_type: {yaml_scalar(extra.get('pdf_type'))}")
        lines.append(f"bt_operators: {int(extra.get('bt_operators') or 0)}")
        lines.append(f"fonts_total: {int(extra.get('fonts_total') or 0)}")
        lines.append(f"fonts_with_basefont: {int(extra.get('fonts_with_basefont') or 0)}")
        lines.append(f"readable_line_ratio: {extra.get('readable_line_ratio', 0)}")
    lines.append("---")
    return "\n".join(lines)


def count_h1(body):
    return len(re.findall(r"^#\s+\S", body, re.M))


def ensure_single_h1(res):
    """
    保证全文恰好一个 H1（格式契约硬要求）。
    没有标题层级的文件（.md/.txt）补一个；有多个 H1 的降级多余的。
    """
    body = res.get("body") or ""
    title = res.get("title")
    h1s = count_h1(body)
    if h1s == 0:
        if title:
            res["body"] = strip_ws_lines(f"# {title}\n\n{body}")
            res["warnings"].append("H1_ADDED：原内容没有标题，已用识别出的标题补一个 H1。")
        else:
            res["body"] = strip_ws_lines(f"# (untitled)\n\n{body}")
            res["warnings"].append("H1_ADDED：没有标题且未能识别，已用占位标题保证契约。")
    elif h1s > 1:
        out, seen = [], False
        for ln in body.split("\n"):
            if re.match(r"^#\s+\S", ln):
                if seen:
                    ln = "##" + ln[1:]
                else:
                    seen = True
            out.append(ln)
        res["body"] = "\n".join(out)
        res["warnings"].append(f"H1_DEMOTED：原有 {h1s} 个 H1，已把多余的降级为 ##，保证全文恰好一个 H1。")
    return res


def write_markdown(out_path, res, src_path, origin_url, src_sha):
    res = ensure_single_h1(res)
    body = res.get("body") or ""
    res["chars"] = len(body.strip())
    res["garbage_rate"] = round(garbage_score(body), 4)
    fm = front_matter(res, src_path, origin_url, src_sha)
    content = strip_ws_lines(fm + "\n\n" + body)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    return res["chars"]


def process_one(job):
    """抽取单个文件，返回报告条目（失败也不写占位文件）"""
    src = job["path"]
    fmt = os.path.splitext(src)[1].lstrip(".").lower()
    entry = {
        "id": job["id"], "file": os.path.relpath(src, BASE_DIR).replace(os.sep, "/"),
        "format": fmt, "status": "failed", "chars": 0, "code_blocks": 0,
        "tables": 0, "links": 0, "headings_h1": 0, "headings_h2": 0, "headings_h3": 0,
        "warnings": [], "failure_reason": None, "text_path": None,
        "kind": job.get("kind"),
    }
    if job.get("error"):
        entry["failure_reason"] = job["error"]
        return entry, None
    fn = extractor_for(src)
    if fn is None:
        entry["failure_reason"] = f"没有对应 {fmt} 的抽取器（EXTRACTORS 里未注册）"
        return entry, None
    try:
        res = fn(read_text(src) if fmt in ("html", "htm", "js", "md", "markdown",
                                          "txt", "prompt") else "", src)
    except Exception as exc:
        # 纪律 A：失败绝不写占位文件
        entry["failure_reason"] = f"抽取抛异常：{type(exc).__name__}: {exc}"
        return entry, None
    return None, res


def main(argv=None):
    opts = parse_args(argv if argv is not None else sys.argv[1:])
    if opts["help"]:
        print(USAGE)
        return 0
    configure(materials_dir=opts["materials_dir"],
              course_dirname=opts["course_dirname"],
              site_hostname=opts["site_hostname"],
              archive_dir=opts["archive_dir"],
              manifest=opts["manifest"],
              out_dir=opts["out_dir"],
              report=opts["report"])
    reconfigure_stdout_utf8()
    log("=" * 78)
    log("extract.py —— 管线 ② 抽取（HTML / PDF / SPA → 统一 Markdown）")
    log(f"仓库根目录: {BASE_DIR}")
    log(f"资料目录　: {MATERIALS_DIR}")
    log(f"归档目录　: {ARCHIVE_DIR}")
    log(f"产出目录　: {EXTRACTED_DIR}")
    log("=" * 78)

    os.makedirs(EXTRACTED_DIR, exist_ok=True)

    manifest = None
    if os.path.isfile(MANIFEST_PATH):
        with open(MANIFEST_PATH, encoding="utf-8", errors="replace") as f:
            manifest = json.load(f)
        log(f"读取 manifest.json：{len(manifest.get('items') or [])} 条 items")
    else:
        log("⚠️  未找到 manifest.json，退化为扫描目录")

    archive_root = resolve_archive_root(ARCHIVE_DIR, ARCHIVE_DIRNAME)
    log(f"archive 数据根：{os.path.relpath(archive_root, BASE_DIR)}")

    plan = build_plan(manifest)
    log(f"\n抽取计划：{len(plan)} 个文件")
    dup = [j for j in plan if j.get("kind") == "archive-dup"]
    if dup:
        log(f"  其中 {len(dup)} 个是 archive 与 materials 的字节重复副本 → 跳过（内容不丢）")

    items = []
    by_id = {}
    for j in plan:
        err, res = process_one(j)
        if err is not None:
            items.append(err)
            log(f"  ✗ {j['id'][:58]:<60} FAILED  {(err['failure_reason'] or '')[:50]}")
            continue
        src_sha = sha256_file(j["path"])
        out_path = os.path.join(EXTRACTED_DIR, j["id"] + ".md")
        try:
            chars = write_markdown(out_path, res, j["path"], j.get("origin_url"), src_sha)
        except Exception as exc:
            items.append({
                "id": j["id"], "file": os.path.relpath(j["path"], BASE_DIR).replace(os.sep, "/"),
                "format": res.get("format"), "status": "failed", "chars": 0,
                "code_blocks": 0, "tables": 0, "links": 0,
                "headings_h1": 0, "headings_h2": 0, "headings_h3": 0,
                "warnings": res.get("warnings") or [],
                "failure_reason": f"写文件失败：{type(exc).__name__}: {exc}",
                "text_path": None, "kind": j.get("kind"),
            })
            continue

        body = res.get("body") or ""
        extra = res.get("extra") or {}
        # 乱码率质检：词数会骗人，必须用乱码率判断「是否真的抽到了可读文本」
        garbage_rate = round(garbage_score(body), 4)
        res["garbage_rate"] = garbage_rate
        status = "ok"
        if garbage_rate > 0.35:
            status = "suspect_low_quality"
        if res.get("format") == "pdf":
            ratio = extra.get("readable_line_ratio") or 0.0
            if extra.get("pdf_type") == "image_only":
                status = "failed"
            elif (extra.get("unrecoverable_type3")
                  or extra.get("unrecoverable_no_font_mapping")
                  or extra.get("unrecoverable_no_page_tree")
                  or extra.get("unrecoverable_garbled_text")):
                status = "suspect_low_quality"
            # ⚠️ 只用乱码率与可读行比例联合判定，不能只看 readable_line_ratio：
            #    实测 assessment 的可读行比例只有 0.4186（学术论文行短、含大量
            #    作者/邮箱/机构短行），但它是 7,015 词的真论文、乱码率仅 3.1%。
            #    只看比例会把它误判成不可恢复，从而丢掉一份可翻译材料。
            elif (extra.get("pdf_type") == "text" and ratio < 0.50
                  and garbage_rate > 0.10):
                status = "suspect_low_quality"
        entry = {
            "id": j["id"],
            "file": os.path.relpath(j["path"], BASE_DIR).replace(os.sep, "/"),
            "format": res.get("format"),
            "status": status,
            "chars": chars,
            "english_words": len(re.findall(r"[A-Za-z]{2,}", body)),
            "garbage_rate": garbage_rate,
            "garbage_verdict": garbage_verdict(garbage_rate),
            "code_blocks": res.get("code_blocks") or 0,
            "tables": res.get("tables") or 0,
            "links": res.get("links") or 0,
            "headings_h1": count_h1(body),
            "headings_h2": len(re.findall(r"^##\s+\S", body, re.M)),
            "headings_h3": len(re.findall(r"^###\s+\S", body, re.M)),
            "warnings": res.get("warnings") or [],
            "failure_reason": None,
            "text_path": os.path.relpath(out_path, BASE_DIR).replace(os.sep, "/"),
            "kind": j.get("kind"),
        }
        if res.get("format") == "pdf":
            entry.update({
                "pdf_type": extra.get("pdf_type"),
                "bt_operators": extra.get("bt_operators"),
                "content_streams": extra.get("content_streams"),
                "fonts_total": extra.get("fonts_total"),
                "fonts_with_basefont": extra.get("fonts_with_basefont"),
                "readable_lines": extra.get("readable_lines"),
                "total_lines": extra.get("total_lines"),
                "readable_line_ratio": extra.get("readable_line_ratio"),
                "undecoded_codes": extra.get("undecoded_codes"),
            })
        items.append(entry)
        by_id[j["id"]] = entry
        flag = "⚠️" if status != "ok" else "✅"
        log(f"  {flag} {j['id'][:58]:<60} {status:<20} {chars:>7,} 字符")

    # ---- 汇总
    ok = [i for i in items if i["status"] == "ok"]
    failed = [i for i in items if i["status"] == "failed"]
    suspect = [i for i in items if i["status"] == "suspect_low_quality"]
    all_warnings = []
    for i in items:
        for w in i.get("warnings") or []:
            all_warnings.append({"id": i["id"], "warning": w})

    report = {
        "generated_by": "extract.py",
        "note": "本文件由脚本生成，请勿手改。抽取失败的文件不会产出占位文件。",
        "inputs": {
            "manifest": os.path.relpath(MANIFEST_PATH, BASE_DIR).replace(os.sep, "/"),
            "archive_root": os.path.relpath(archive_root, BASE_DIR).replace(os.sep, "/"),
            "materials": os.path.relpath(MATERIALS_DIR, BASE_DIR).replace(os.sep, "/"),
        },
        "summary": {
            "total_files": len(items),
            "ok": len(ok),
            "failed": len(failed),
            "suspect": len(suspect),
            "total_chars": sum(i["chars"] for i in items),
            "total_code_blocks": sum(i["code_blocks"] for i in items),
            "total_tables": sum(i["tables"] for i in items),
            "total_links": sum(i["links"] for i in items),
            "total_warnings": len(all_warnings),
            "placeholders_written": 0,   # 纪律 A：恒为 0，可被下游核验
            "garbage": {
                "readable": sum(1 for i in items if (i.get("garbage_rate") or 1) < 0.10),
                "partial": sum(1 for i in items
                               if 0.10 <= (i.get("garbage_rate") or 1) <= 0.35),
                "garbage": sum(1 for i in items if (i.get("garbage_rate") or 1) > 0.35),
            },
        },
        "items": items,
        "warnings": all_warnings,
    }

    # ---- 回填 manifest
    backfilled = backfill_manifest(manifest, by_id)
    report["manifest_backfill"] = backfilled

    os.makedirs(os.path.dirname(EXTRACT_REPORT_PATH), exist_ok=True)
    with open(EXTRACT_REPORT_PATH, "w", encoding="utf-8", newline="\n") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # ============================================================ 控制台自检
    s = report["summary"]
    log("\n" + "=" * 78)
    log("【1】抽取汇总")
    log("=" * 78)
    for k in ("total_files", "ok", "failed", "suspect", "total_chars",
              "total_code_blocks", "total_tables", "total_links", "total_warnings"):
        log(f"    {k:<22} {s[k]:,}" if isinstance(s[k], int) else f"    {k:<22} {s[k]}")

    log("\n【2】PDF 判定与可读行比例")
    for i in items:
        if i.get("pdf_type"):
            log(f"    {i['id'][:40]:<42} {i['pdf_type']:<20} "
                f"BT={i.get('bt_operators'):<4} 流={i.get('content_streams'):<3} "
                f"可信流={i.get('content_streams_trusted')} "
                f"字体={i.get('fonts_total'):<3} BaseFont={i.get('fonts_with_basefont'):<3} "
                f"可读行={i.get('readable_lines')}/{i.get('total_lines')} "
                f"({(i.get('readable_line_ratio') or 0)*100:.1f}%)")

    # 2b. 乱码率质检 —— 词数会骗人，这一节才是「是否真的抽到可读文本」的证据
    log("\n【2b】乱码率质检（<10% 可读 / 10-35% 部分可读 / >35% 乱码）")
    log(f"    {'文件':<46}{'词数':>8}{'乱码率':>9}  判定")
    for i in items:
        if i["status"] == "failed":
            continue
        gr = i.get("garbage_rate")
        log(f"    {i['id'][:44]:<46}{i.get('english_words') or 0:>8,}"
            f"{(gr if gr is not None else 1.0)*100:>8.1f}%  {i.get('garbage_verdict')}")
    g = s["garbage"]
    log(f"    小结：可读 {g['readable']} / 部分可读 {g['partial']} / 乱码 {g['garbage']}")

    log("\n【3】H1 契约核对（每个文件必须恰好 1 个 H1）")
    bad_h1 = [i for i in items if i["status"] != "failed" and i["headings_h1"] != 1]
    log(f"    违反契约的文件数：{len(bad_h1)}")
    for i in bad_h1:
        log(f"      {i['id']}: H1={i['headings_h1']}")

    log("\n【4】失败与可疑清单")
    if not failed and not suspect:
        log("    无")
    for i in failed:
        log(f"    ✗ [{i['format']}] {i['id']}")
        log(f"        原因: {i['failure_reason']}")
    for i in suspect:
        log(f"    ⚠️ [{i['format']}] {i['id']}  可读行比例 "
            f"{(i.get('readable_line_ratio') or 0)*100:.1f}%")

    log("\n【5】剥过头兜底（HTML 剥离超过 40% 被回退的文件）")
    reverted = [i for i in items if any("AGGRESSIVE_STRIP_REVERTED" in w for w in i.get("warnings") or [])]
    if reverted:
        for i in reverted:
            log(f"    {i['id']}")
    else:
        log("    无（没有页面触发兜底）")

    log("\n【6】warning 清单")
    if not all_warnings:
        log("    无")
    kinds = {}
    for w in all_warnings:
        key = (w["warning"].split("：")[0])[:40]
        kinds[key] = kinds.get(key, 0) + 1
    for k, v in sorted(kinds.items(), key=lambda x: -x[1]):
        log(f"    {v:>3} × {k}")

    log("\n" + "=" * 78)
    log(f"已写出：{EXTRACT_REPORT_PATH}")
    log(f"Markdown 产出目录：{EXTRACTED_DIR}")
    log("=" * 78)
    return 0


def backfill_manifest(manifest, by_id):
    """把抽取结果回填进 manifest.json 的 items[]"""
    if not manifest:
        return {"updated": 0, "skipped": "manifest.json 不存在"}
    changed = 0
    pdf_fixed = []
    for it in manifest.get("items") or []:
        e = by_id.get(it.get("id"))
        if not e or e["status"] == "failed":
            continue
        # 约定的 5 个回填字段
        it["chars"] = e["chars"]
        it["english_words"] = e.get("english_words")
        it["garbage_rate"] = e.get("garbage_rate")
        it["text_path"] = e["text_path"]
        it["status"] = "extracted"

        # ---- PDF 判定修正：旧体检把两份 text 型误判成 font_encoding_broken
        if e.get("format") == "pdf":
            it["pdf_type"] = e.get("pdf_type")
            if e.get("pdf_type") == "text" and e.get("status") == "ok":
                it["status"] = "extracted"
                it["translatable"] = True
                it["failure_root_cause"] = None
                pdf_fixed.append(f"{it['id']} → text（translatable=true）")
            else:
                # Type3 无 Unicode 映射 / 抽出即乱码 → 客观不可恢复，如实标不可翻译
                it["status"] = "type3_encoding_unrecoverable"
                it["translatable"] = False
                it["failure_root_cause"] = (
                    "Type3 矢量字形且字体缺失 /ToUnicode 映射（字形名是 /C0 /C1 这类匿名编号），"
                    "字符码到 Unicode 没有映射关系，抽出的文本是字母替换式乱码，正文客观不可恢复。"
                    f"已按纪律不输出乱码；实测乱码率 {e.get('garbage_rate')}、"
                    f"停用词占比 {(e.get('extra') or {}).get('stopword_ratio')}。"
                    f"需 OCR 或带文本层的原始版本。")
                pdf_fixed.append(
                    f"{it['id']} → type3_encoding_unrecoverable（translatable=false，"
                    f"乱码率 {e.get('garbage_rate')}）")
        if e.get("warnings"):
            it["extract_warnings"] = e["warnings"]
        changed += 1
    os.makedirs(os.path.dirname(MANIFEST_PATH), exist_ok=True)
    with open(MANIFEST_PATH, "w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return {"updated": changed,
            "file": os.path.relpath(MANIFEST_PATH, BASE_DIR).replace(os.sep, "/"),
            "pdf_judgement_fixed": pdf_fixed}


if __name__ == "__main__":
    sys.exit(main())
