#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch.py —— 管线 ① 抓取与归档（补抓缺口 + 登记证据链）

⚠️ 本环节的核心认知
    绝大部分资料【已经归档在本地】（site/ 官网快照、pages/ 31 篇 html、pdfs/ 3 个 PDF）。
    本脚本的职责不是从零爬取，而是：
      A. 把「已归档」的事实登记成证据（不发网络请求）
      B. 只补抓真正缺失的缺口，并把每个候选路径的结局逐条留痕

⚠️ 最关键的口径要求：三种「不可得」必须严格区分，绝对不允许笼统写「抓不到」
    http_404      真 404。服务器可达，文件确认不存在。【这是有效信息，不是失败。】
    blocked_403   被拦截（Cloudflare 人机校验等）。【不能判定为不存在。】
    network_error 网络不可达，拿不到状态码。【属于「未核查」，不是「不存在」。】
    三者性质完全不同：404 是结论，403 是受阻，network_error 是没测到。
    混为一谈会让下游 README 的覆盖率数字整体不可信。

环境实测结论（已写进 fetch_report.environment_notes）
    1. 本机 Python 的 OpenSSL 默认 CA 库是【空的】（系统默认路径指向不存在的 msys2 cert.pem），
       所以「所有 HTTPS 都 CERTIFICATE_VERIFY_FAILED」——这看起来像网络全断，
       其实只是没有信任根。脚本会自动寻找可用的 CA bundle（见 CA_BUNDLE_CANDIDATES）。
       ⚠️ 这个坑非常危险：不修的话会把「证书信任问题」误记成 network_error，
          于是把「能抓的」写成「网络不可达」，凭空造出一堆假缺口。
    2. 网络确实不稳定：同一 URL 可能一次超时、下一次 0.9 秒成功。
       所以必须重试（2/5/10 秒），并且【抓到即落盘】，不要攒在内存里最后统一写。
    3. raw.githubusercontent.com 可用；github.com 的 HTML 与 api.github.com 不可达。
       所以 GitHub 只能靠「拼 raw 路径直抓文件」，不能列目录。

环境限制
    只用 Python 标准库（urllib / json / os / sys / time / hashlib / ssl / re）。
    Windows 控制台 GBK，打印统一走 UTF-8。

用法
    python fetch.py                  # 常规补抓
    python fetch.py --retry-failed   # 只重试上次 network_error / not_attempted 的条目
    python fetch.py --dry-run        # 不联网，只登记已归档 + 分类规划
    python fetch.py --offline        # 不联网，把所有待抓条目记为 network_error
"""

import datetime
import hashlib
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

# ============================================================ 路径与参数配置
# 换课程时只需要改这几行
BASE_DIR = os.path.dirname(os.path.abspath(__file__))     # = scripts/
REPO_ROOT = os.path.dirname(BASE_DIR)                     # 仓库根

# 目录布局：data/ 输入 · work/ 中间产物 · output/ 最终交付
DATA_DIR = os.path.join(REPO_ROOT, "data")
WORK_DIR = os.path.join(REPO_ROOT, "work")
REPORTS_DIR = os.path.join(WORK_DIR, "reports")

COURSE_DIRNAME = os.environ.get("MF_COURSE_DIRNAME", "CS146S_offline")  # 课程子目录名

USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

TIMEOUT_DEFAULT = 15         # 常规请求超时（秒）
TIMEOUT_ARXIV = 45           # arXiv PDF 较大，放宽到 45 秒
RETRY_DELAYS = [2, 5, 10]    # 每个 URL 最多重试 3 次，间隔 2 / 5 / 10 秒
DOMAIN_SLEEP = 1.5           # 同一域名两次请求之间 sleep 1.5 秒（礼貌抓取）

# GitHub 仓库目录链接（tree/...）没法列举，只能猜候选文件
TREE_CANDIDATE_FILES = ["README.md", "assignment.md", "writeup.md"]
BRANCH_CANDIDATES = ["master", "main"]   # 分支名不确定时：先 master 再 main

# CA bundle 候选路径 —— 修「默认信任库为空」这个致命坑。
# ⚠️ 可配置性：不同机器的 CA 位置不一样，所以
#     ① 优先读环境变量 SSL_CERT_FILE / MF_CA_BUNDLE（标准做法 + 自定义）
#     ② 再退回下面这份「常见位置」候选表（只放跨机器通用的相对/系统路径）
#     ③ 都没有时退回系统默认，并把这件事记进报告
#    绝不把某台机器的绝对安装路径写进代码：那既是隐私泄漏，
#    也让管线换一台机器就失效。
_env_ca = (os.environ.get("MF_CA_BUNDLE")
           or os.environ.get("SSL_CERT_FILE")
           or os.environ.get("REQUESTS_CA_BUNDLE"))
CA_BUNDLE_CANDIDATES = [
    _env_ca,
    # 与当前 Python 解释器同目录的 cacert.pem（certifi 常见落点）
    os.path.join(os.path.dirname(sys.executable), "cacert.pem"),
    # 虚拟环境里的 certifi
    os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages",
                 "certifi", "cacert.pem"),
    # 各平台系统信任库的标准位置
    "/etc/ssl/certs/ca-certificates.crt",
    "/etc/pki/tls/certs/ca-bundle.crt",
    "/etc/ssl/cert.pem",
    "/usr/local/etc/openssl/cert.pem",
]

# 明确不抓的域名 → 直接登记（省时间，也避免把「需要账号」误记成网络错误）
NO_FETCH_DOMAINS = {
    "docs.google.com": ("lecture", "needs_account",
                        "需 Google 账号登录，无法自动抓取"),
    "drive.google.com": ("lecture", "needs_account",
                         "需 Google 账号登录，无法自动抓取"),
    "youtube.com": ("video", "unreachable_automated",
                    "youtube.com 网络不可达；本地无 yt-dlp/youtube-dl/ffmpeg；"
                    "第三方字幕站 youtubetotranscript.com 与 glasp.co 均返回 HTTP 403，"
                    "被 Cloudflare 人机校验拦截。注意：403 属于被拦截，不能判定为内容不存在。"),
    "www.youtube.com": ("video", "unreachable_automated",
                        "youtube.com 网络不可达；本地无 yt-dlp/youtube-dl/ffmpeg；"
                        "第三方字幕站 youtubetotranscript.com 与 glasp.co 均返回 HTTP 403，"
                        "被 Cloudflare 人机校验拦截。注意：403 属于被拦截，不能判定为内容不存在。"),
    "youtu.be": ("video", "unreachable_automated",
                 "同上：视频站不可达，无法自动获取字幕。"),
}

# status 口径（和 build_manifest.py 的下游口径对齐）
STATUS_ALREADY = "already_archived"
STATUS_OK = "fetched_ok"
STATUS_404 = "http_404"
STATUS_403 = "blocked_403"
STATUS_NEEDS_ACCOUNT = "needs_account"
STATUS_UNREACHABLE = "unreachable_automated"
STATUS_NETERR = "network_error"
STATUS_NOT_ATTEMPTED = "not_attempted"

# summary 里必须出现的计数键（顺序即打印顺序）
SUMMARY_KEYS = [
    "total_urls", "already_archived", "fetched_ok", "http_404", "blocked_403",
    "needs_account", "unreachable_automated", "network_error", "not_attempted",
    "total_bytes_archived",
]

ENVIRONMENT_NOTES = [
    "raw.githubusercontent.com 可达；github.com HTML 与 api.github.com 不可达，"
    "因此 GitHub 只能用「拼 raw 路径直抓文件」的方式，无法列举目录",
    "网络不稳定，同 URL 可能时通时不通（实测同一 raw 地址一次 20s 超时、下一次 0.9s 成功），"
    "已实现重试（2/5/10 秒）并「抓到即落盘」",
    "本机 Python 的 OpenSSL 默认信任库为空（系统默认路径指向不存在的 msys2 cert.pem），"
    "会导致所有 HTTPS 报 CERTIFICATE_VERIFY_FAILED —— 这是证书信任问题，不是网络不可达。"
    "脚本已自动寻找可用 CA bundle，避免把它误记成 network_error",
    "arXiv PDF 超时放宽到 45 秒；同一域名两次请求之间 sleep 1.5 秒，礼貌抓取",
    "LinkedIn 返回 HTTP 451（因法律原因不可用）—— 既不是 404 也不是被反爬拦截，"
    "已在 items 中按 blocked_451 记录并保留原始状态码",
]


# ============================================================ 基础设施
def reconfigure_stdout_utf8():
    """Windows 控制台是 GBK，直接打印中文/emoji 会 UnicodeEncodeError"""
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


def resolve_materials_dir(base_dir, dirname, course_dirname):
    """定位 materials/：优先同级，否则向下搜一层（兼容被包在交付目录里的情况）"""
    default = os.path.join(base_dir, dirname)
    if os.path.isdir(os.path.join(default, course_dirname)):
        return default
    try:
        for entry in sorted(os.listdir(base_dir)):
            sub = os.path.join(base_dir, entry)
            if not os.path.isdir(sub):
                continue
            for cand in (os.path.join(sub, dirname), sub):
                if os.path.isdir(os.path.join(cand, course_dirname)):
                    return cand
    except OSError:
        pass
    return default


MATERIALS_DIR = resolve_materials_dir(DATA_DIR, "materials", COURSE_DIRNAME)
COURSE_DIR = os.path.join(MATERIALS_DIR, COURSE_DIRNAME)
ALL_URLS_PATH = os.path.join(COURSE_DIR, "all_urls.txt")
PAGE_MAP_PATH = os.path.join(COURSE_DIR, "page_map.json")
PAGES_DIR = os.path.join(COURSE_DIR, "pages")
MANIFEST_PATH = os.path.join(REPORTS_DIR, "manifest.json")          # 上游账本（只读）
ARCHIVE_DIR = os.path.join(DATA_DIR, "fetched")                     # 抓取归档
FETCH_REPORT_PATH = os.path.join(REPORTS_DIR, "fetch_report.json")  # 抓取证据链


def configure(materials_dir=None, course_dirname=None, urls=None, map_path=None,
              pages_dir=None, archive_dir=None, manifest=None, report=None):
    """
    按命令行参数/环境变量重设本模块的路径全局变量。

    ⚠️ 换源的关键就是这四个：--urls（URL 清单）/ --map（本地归档映射）/
       --pages（页面目录）/ --archive-dir（归档落地位置）。
       此前 URL 清单只从一个写死的 page_map.json 读，无法指向新清单。
    """
    global COURSE_DIRNAME, MATERIALS_DIR, COURSE_DIR
    global ALL_URLS_PATH, PAGE_MAP_PATH, PAGES_DIR
    global ARCHIVE_DIR, MANIFEST_PATH, FETCH_REPORT_PATH

    if course_dirname:
        COURSE_DIRNAME = course_dirname

    MATERIALS_DIR = (os.path.abspath(materials_dir) if materials_dir
                     else resolve_materials_dir(DATA_DIR, "materials",
                                                COURSE_DIRNAME))
    COURSE_DIR = os.path.join(MATERIALS_DIR, COURSE_DIRNAME)

    # 三个源输入：默认落在 COURSE_DIR 下，可各自独立覆盖
    ALL_URLS_PATH = (os.path.abspath(urls) if urls
                     else os.path.join(COURSE_DIR, "all_urls.txt"))
    PAGE_MAP_PATH = (os.path.abspath(map_path) if map_path
                     else os.path.join(COURSE_DIR, "page_map.json"))
    PAGES_DIR = (os.path.abspath(pages_dir) if pages_dir
                 else os.path.join(COURSE_DIR, "pages"))

    if archive_dir:
        ARCHIVE_DIR = os.path.abspath(archive_dir)
    if manifest:
        MANIFEST_PATH = os.path.abspath(manifest)
    if report:
        FETCH_REPORT_PATH = os.path.abspath(report)


def parse_args(argv):
    """
    参数解析：布尔开关用 `--flag`，取值选项用 `--key value`。
    ⚠️ 原来的实现是纯布尔式（`"--dry-run" in argv`），
       加取值选项后必须走下标推进，否则 `--urls X` 里的 X 会被当成未知开关。
    """
    opts = {"retry_failed": False, "dry_run": False, "offline": False,
            "help": False,
            "materials_dir": os.environ.get("MF_MATERIALS_DIR"),
            "course_dirname": os.environ.get("MF_COURSE_DIRNAME"),
            "urls": os.environ.get("MF_URLS"),
            "map_path": os.environ.get("MF_MAP"),
            "pages_dir": os.environ.get("MF_PAGES_DIR"),
            "archive_dir": os.environ.get("MF_ARCHIVE_DIR"),
            "manifest": os.environ.get("MF_MANIFEST"),
            "report": os.environ.get("MF_FETCH_REPORT")}
    value_flags = {
        "--materials-dir": "materials_dir",
        "--course-dirname": "course_dirname",
        "--urls": "urls",
        "--map": "map_path",
        "--pages": "pages_dir",
        "--archive-dir": "archive_dir",
        "--manifest": "manifest",
        "--report": "report",
    }
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("-h", "--help"):
            opts["help"] = True
        elif a == "--retry-failed":
            opts["retry_failed"] = True
        elif a == "--dry-run":
            opts["dry_run"] = True
        elif a == "--offline":
            opts["offline"] = True
        elif a in value_flags:
            if i + 1 >= len(argv):
                raise SystemExit(f"❌ {a} 后面要跟一个值")
            opts[value_flags[a]] = argv[i + 1]
            i += 1
        else:
            raise SystemExit(f"❌ 未知参数：{a}\n\n{USAGE}")
        i += 1
    return opts


USAGE = """fetch.py —— 管线 ① 抓取与归档（补抓缺口 + 登记证据链）

用法：
  python scripts/fetch.py [选项]

行为开关：
  --dry-run          不联网，只登记已归档 + 分类规划
  --offline          不联网，把所有待抓条目记为 network_error
  --retry-failed     只重试上一轮失败的条目

输入/输出（换源时用这些）：
  --urls PATH         URL 清单（默认 <course>/all_urls.txt，每行一个 URL）
  --map PATH          本地归档映射 JSON（默认 <course>/page_map.json）
  --pages DIR         页面目录（默认 <course>/pages）
  --archive-dir DIR   归档落地目录（默认 data/fetched）
  --manifest PATH     上游账本（默认 work/reports/manifest.json）
  --report PATH       抓取报告（默认 work/reports/fetch_report.json）
  --materials-dir DIR 资料根目录（默认自动定位 data/materials）
  --course-dirname N  课程子目录名（默认 CS146S_offline）
  -h, --help          显示本帮助

也可用环境变量：MF_URLS / MF_MAP / MF_PAGES_DIR / MF_ARCHIVE_DIR / MF_MANIFEST /
MF_FETCH_REPORT / MF_MATERIALS_DIR / MF_COURSE_DIRNAME
"""


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(262144), b""):
            h.update(chunk)
    return h.hexdigest()


def local_timestamp():
    """
    生成本地时区的 ISO-8601 时间戳（如 2026-01-01T12:00:00+08:00）。
    ⚠️ 不能用 time.strftime("%z")：Windows 上 %z 会输出中文时区名
       （实测得到 "2026-09-26T23:18:10中国标准时间"），根本不是合法 ISO-8601。
       datetime.astimezone().isoformat() 才跨平台可靠。
    """
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_meta(path, url, data, content_type, result=None, used_branch=None,
               origin_url=None, digest=None):
    """
    写 <文件名>.meta.json —— 每个归档文件的身份证。
    字段：origin_url / fetched_at / http_status / content_type / bytes / sha256 / used_branch
    外加若干溯源辅助字段（final_url、server_date、last_modified、path_in_url）。
    """
    result = result or {}
    headers = result.get("headers") or {}
    meta = {
        "origin_url": origin_url or url,
        "final_url": url,
        "fetched_at": local_timestamp(),
        "http_status": result.get("http_status", 200),
        "content_type": content_type or headers.get("Content-Type"),
        "bytes": len(data) if data is not None else None,
        "sha256": digest or sha256_bytes(data),
        "used_branch": used_branch,
        # 以下为溯源辅助，便于后续 extract.py 核对
        "archive_path": os.path.relpath(path, REPO_ROOT).replace("\\", "/"),
        "server": headers.get("Server"),
        "last_modified": headers.get("Last-Modified"),
        "server_date": headers.get("Date"),
        "url_path": urllib.parse.urlparse(url).path,
        "fetched_by": "fetch.py",
    }
    with open(path + ".meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    return meta


def meta_sidecar_is_valid(data_path, expect_sha=None):
    """检查 .meta.json 是否存在且与文件一致（幂等与自检都靠它）"""
    meta_path = data_path + ".meta.json"
    if not os.path.isfile(meta_path):
        return False, None
    try:
        with open(meta_path, encoding="utf-8", errors="replace") as f:
            meta = json.load(f)
    except Exception:
        return False, None
    try:
        actual = sha256_file(data_path)
    except OSError:
        return False, None
    if meta.get("sha256") != actual:
        return False, meta
    if expect_sha and expect_sha != actual:
        return False, meta
    return True, meta


def build_ssl_context():
    """
    构造 SSL 上下文。
    ⚠️ 有些环境的默认信任库是空的 → 必须显式找 CA bundle，
       否则所有 HTTPS 全部验证失败。
    ⚠️ 这直接影响口径正确性：证书问题绝不能被记成 network_error。
    可用 MF_CA_BUNDLE / SSL_CERT_FILE 环境变量指定（见 CA_BUNDLE_CANDIDATES）。
    """
    for ca in CA_BUNDLE_CANDIDATES:
        if ca and os.path.isfile(ca):
            try:
                ctx = ssl.create_default_context(cafile=ca)
                stats = ctx.cert_store_stats()
                if stats.get("x509_ca", 0) > 0:
                    return ctx, ca, stats
            except Exception:
                continue
    # 实在没有可用 CA bundle：退回系统默认（可能失败），但把这件事记进报告
    try:
        ctx = ssl.create_default_context()
        if ctx.cert_store_stats().get("x509_ca", 0) > 0:
            return ctx, None, ctx.cert_store_stats()
    except Exception:
        pass
    return None, None, {}


def domain_of(url):
    m = re.match(r"https?://([^/?#]+)", url or "")
    return m.group(1).lower() if m else ""


def sanitize_name(name, default="index"):
    name = urllib.parse.unquote(name or "")
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name).strip(" .")
    return name[:120] or default


# 已知扩展名白名单。
# ⚠️ 为什么要白名单而不是「取最后一个点之后」：
#    arXiv 路径 /pdf/2405.13565 的最后一段是 2405.13565，
#    按「最后一个点」切会把版本号 13565 当成扩展名，
#    产出 2405.13565-<hash>.13565 这种荒唐文件名。
#    只有认得出是扩展名，才敢把它当扩展名。
KNOWN_EXTENSIONS = {
    "html", "htm", "xhtml", "pdf", "md", "markdown", "txt", "json", "xml",
    "csv", "tsv", "js", "mjs", "css", "png", "jpg", "jpeg", "gif", "svg",
    "webp", "ico", "zip", "tar", "gz", "ipynb", "py", "ts", "tsx", "jsx",
    "yaml", "yml", "toml", "rst", "prompt", "sh", "ps1", "epub", "doc", "docx",
}


def local_name_for(url, content_type=None):
    """
    由 URL 生成归档文件名，形如 "<可读主干>-<短哈希>.<扩展名>"。
    规则：
      · 主干取路径最后一段，只做非法字符清洗，保留内部所有的点
      · 只有在【白名单】里认得出的才算扩展名；认不出就交给 Content-Type 兜底
      · 追加 URL 短哈希，保证同域名下的同名文件（如多处 README.md）不互相覆盖，且天然幂等
    """
    parsed = urllib.parse.urlparse(url)
    base = os.path.basename(parsed.path.rstrip("/")) or "index"
    safe = sanitize_name(base)

    ext = ""
    if "." in safe:
        head, _, tail = safe.rpartition(".")
        if tail.lower() in KNOWN_EXTENSIONS:
            safe, ext = head, tail.lower()
    if not ext:
        ext = extension_from_content_type(content_type) or ""
    tag = sha256_text(url)[:8]
    return f"{safe}-{tag}.{ext}" if ext else f"{safe}-{tag}"


def extension_from_content_type(content_type):
    """
    URL 路径里取不到可靠扩展名时，用 Content-Type 兜底。
    （arXiv 的 /pdf/2405.13565 这种路径拿不到扩展名，但响应头是 application/pdf）
    """
    if not content_type:
        return None
    ctype = content_type.split(";")[0].strip().lower()
    return {
        "application/pdf": "pdf",
        "text/html": "html",
        "application/xhtml+xml": "html",
        "text/plain": "txt",
        "text/markdown": "md",
        "application/json": "json",
        "application/xml": "xml",
        "text/xml": "xml",
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/svg+xml": "svg",
        "application/zip": "zip",
        "text/css": "css",
        "application/javascript": "js",
        "text/javascript": "js",
    }.get(ctype)


def classify_source_class(url, in_page_map):
    """按域名/路径判断 source_class"""
    d = domain_of(url)
    path = urllib.parse.urlparse(url).path.lower()
    if d in ("docs.google.com", "drive.google.com"):
        return "lecture"
    if "youtube.com" in d or d == "youtu.be":
        return "video"
    if "github" in d:
        return "github"
    if d in ("cdn.openai.com", "www-cdn.anthropic.com") or path.endswith(".pdf"):
        return "lecture"
    if d == "themodernsoftware.dev" or "warp.dev" in d:
        return "official_site"
    if in_page_map:
        return "reading"
    return "reading"


def is_garbage_url(url):
    """
    识别 all_urls.txt 里的垃圾行：
      ① XML 命名空间声明（http://www.w3.org/1998/Math/MathML 之类）—— 不是可抓资源
      ② 抓取时把内联 SVG 的转义标记混进了 URL 列表（超长、含 %3C、含空格）
    这些既不该发请求，也不该算「抓不到」，单独记为 not_attempted 并说明原因。
    """
    if len(url) > 500:
        return True, "疑似抓取时混入的内联 SVG/转义标记片段，不是合法资源 URL"
    if "%3c" in url.lower() or "<" in url or " " in url:
        return True, "URL 中含 HTML 转义标记或空格，不是可请求的合法 URL"
    d = domain_of(url)
    if d in ("www.w3.org", "www.w3.org".replace("www.", "")):
        return True, "XML 命名空间声明（如 1998/Math/MathML），是文档内命名空间而非可抓资源"
    return False, None


# ============================================================ HTTP 抓取（重试 + 抓到即落盘）
class Fetcher:
    """带重试、礼貌间隔、落盘、去重的抓取器"""

    def __init__(self, ssl_ctx, dry_run=False, offline=False, definitive_cache=None):
        self.ssl_ctx = ssl_ctx
        self.dry_run = dry_run
        self.offline = offline
        self.last_request_at = {}     # 域名 → 上次请求时间（礼貌间隔）
        self.memory_cache = {}        # 最终URL → 抓取结果（同一次运行内不重复请求）
        self.retry_successes = []     # 记录「重试后才成功」的 URL，证明重试机制有效
        self.cache_hits = 0           # 记录「复用确定性结论、未再请求」的次数
        self.request_count = 0
        # 已知的「确定性状态」缓存：最终URL → {status, http_status, cause, observed_at}
        # ⚠️ 存在的理由：网络抖动会让同一个 URL 这轮 404、下轮超时。
        #    若允许「超时」覆盖「已经拿到的 404」，报告里的 http_404 就变成了
        #    网络状况的随机函数 —— 这正是「三种不可得」口径最怕的污染。
        #    所以：确定性结论（拿到了状态码）具有粘性，绝不被不确定性（未核查）覆盖。
        self.definitive_cache = definitive_cache or {}

    def _polite_wait(self, domain):
        last = self.last_request_at.get(domain)
        if last is not None:
            elapsed = time.time() - last
            if elapsed < DOMAIN_SLEEP:
                time.sleep(DOMAIN_SLEEP - elapsed)

    def fetch(self, final_url, timeout=TIMEOUT_DEFAULT):
        """
        返回 dict：status/kind/http_status/body/content_type/attempts/retried_to_success
        status 语义严格区分 404 / 403 / 网络异常。
        """
        if final_url in self.memory_cache:
            cached = dict(self.memory_cache[final_url])
            cached["from_cache"] = True
            return cached

        attempts = []
        domain = domain_of(final_url)

        # 粘性检查：该 URL 之前已经拿到过确定性状态码 → 直接沿用，不再请求，
        # 避免「这轮超时」把上一轮的结论降级成 network_error。
        known = self.definitive_cache.get(final_url)
        if known:
            self.cache_hits += 1
            return {
                "status": known["status"], "kind": "cached_definitive",
                "http_status": known.get("http_status"), "body": None, "content_type": None,
                "attempts": [{"url": final_url,
                              "result": f"沿用上一轮已取得的确定性状态码 "
                                        f"{known.get('http_status')}（{known.get('observed_at')}），"
                                        f"本轮未重复请求",
                              "kind": "cached_definitive"}],
                "failure_root_cause": known.get("failure_root_cause"),
                "retried_to_success": None,
                "cached_from_previous_run": True,
                "observed_at": known.get("observed_at"),
            }

        if self.dry_run:
            # --dry-run 绝对不能碰网络：既不请求，也不冒充 network_error
            result = {"status": STATUS_NOT_ATTEMPTED, "kind": "not_attempted",
                      "http_status": None, "body": None, "content_type": None,
                      "failure_root_cause": "以 --dry-run 运行：本轮按设计未发起网络请求，"
                                            "该条目的真实可达性未核查",
                      "attempts": [{"url": final_url, "result": "--dry-run 未发起请求",
                                    "kind": "not_attempted"}]}
            self.memory_cache[final_url] = result
            return dict(result)

        if self.offline:
            result = {"status": STATUS_NETERR, "kind": "network_error", "http_status": None,
                      "body": None, "content_type": None,
                      "failure_root_cause": "以 --offline 运行：本轮未发起网络请求，"
                                            "无法取得状态码，属「未核查」，不能判定为不存在",
                      "attempts": [{"url": final_url, "result": "--offline 未发起请求",
                                    "kind": "network_error"}]}
            self.memory_cache[final_url] = result
            return dict(result)

        ok_on_attempt = None
        for i in range(len(RETRY_DELAYS) + 1):     # 首次 + 最多 3 次重试
            if i > 0:
                delay = RETRY_DELAYS[i - 1]
                attempts.append({"url": final_url,
                                 "result": f"第 {i} 次重试前等待 {delay}s", "kind": "retry_wait"})
                time.sleep(delay)
            self._polite_wait(domain)
            self.request_count += 1
            self.last_request_at[domain] = time.time()

            req = urllib.request.Request(final_url, headers={
                "User-Agent": USER_AGENT,
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
            })
            try:
                kwargs = {"timeout": timeout}
                if self.ssl_ctx is not None:
                    kwargs["context"] = self.ssl_ctx
                with urllib.request.urlopen(req, **kwargs) as resp:
                    body = resp.read()
                    ctype = resp.headers.get("Content-Type")
                    status = getattr(resp, "status", 200)
                    headers = {k: v for k, v in resp.headers.items()}
                attempts.append({"url": final_url, "result": f"HTTP {status}, {len(body)} 字节",
                                 "kind": "ok"})
                if i > 0:
                    ok_on_attempt = i + 1
                    self.retry_successes.append(final_url)
                result = {"status": STATUS_OK, "kind": "ok", "http_status": status,
                          "body": body, "content_type": ctype, "attempts": attempts,
                          "headers": headers,
                          "failure_root_cause": None,
                          "retried_to_success": ok_on_attempt,
                          "observed_at": local_timestamp()}
                self.memory_cache[final_url] = result
                return dict(result)

            except urllib.error.HTTPError as e:
                # 服务器可达，拿到了明确状态码
                code = e.code
                if code == 404:
                    kind, st = "http_404", STATUS_404
                    cause = ("HTTP 404：服务器可达且明确返回「不存在」。"
                             "这是有效信息（文件确认未公开），不是抓取失败")
                elif code == 403:
                    kind, st = "blocked_403", STATUS_403
                    cause = ("HTTP 403：请求被拦截（可能为 Cloudflare 人机校验）。"
                             "属于「被拦截」，不能据此判定内容不存在")
                elif code == 451:
                    kind, st = "blocked_451", "blocked_451"
                    cause = ("HTTP 451：因法律原因不可用（Unavailable For Legal Reasons）。"
                             "服务器可达但按法规拒绝提供，既不是 404 也不属于反爬拦截")
                else:
                    kind, st = f"http_{code}", f"blocked_{code}"
                    cause = (f"HTTP {code}：服务器返回了明确状态码，属「受阻」，"
                             f"不能判定为内容不存在")
                attempts.append({"url": final_url, "result": f"HTTP {code}", "kind": kind})
                result = {"status": st, "kind": kind, "http_status": code, "body": None,
                          "content_type": None, "attempts": attempts,
                          "failure_root_cause": cause, "retried_to_success": None,
                          "observed_at": local_timestamp()}
                # 确定性结论入缓存：同一轮内也不会再问第二次，且本轮后续沿用
                self.definitive_cache[final_url] = {
                    "status": st, "http_status": code, "failure_root_cause": cause,
                    "observed_at": result["observed_at"],
                }
                self.memory_cache[final_url] = result
                return dict(result)

            except Exception as e:
                # 网络层异常：拿不到状态码 → 未核查
                detail = f"{type(e).__name__}: {e}"
                attempts.append({"url": final_url, "result": detail, "kind": "network_error"})
                last_error = detail

        result = {"status": STATUS_NETERR, "kind": "network_error", "http_status": None,
                  "body": None, "content_type": None, "attempts": attempts,
                  "failure_root_cause": (
                      f"网络不可达，{len(RETRY_DELAYS) + 1} 次尝试均未取得 HTTP 状态码"
                      f"（最后一次：{last_error}）。属「未核查」，"
                      f"不能判定为文件不存在"),
                  "retried_to_success": None}
        self.memory_cache[final_url] = result
        return dict(result)

    def save_to_archive(self, url, data, content_type, result=None, used_branch=None,
                        origin_url=None):
        """
        抓到即落盘（不攒在内存里），并【立即】写出同名 .meta.json 元数据。
        返回 (绝对路径, 字节数, sha256)。
        ⚠️ 绝不写入 materials/ —— 那是只读的已归档原始资料。
        """
        domain = domain_of(url) or "unknown-domain"
        folder = os.path.join(ARCHIVE_DIR, sanitize_name(domain, "unknown-domain"))
        os.makedirs(folder, exist_ok=True)
        filename = local_name_for(url, content_type)
        path = os.path.join(folder, filename)
        with open(path, "wb") as f:
            f.write(data)          # ← 立即落盘
        digest = sha256_bytes(data)
        write_meta(path, url, data, content_type, result, used_branch, origin_url, digest)
        return path, len(data), digest


# ============================================================ 任务 A：登记已归档（不发请求）
def load_inputs():
    page_map = {}
    if os.path.isfile(PAGE_MAP_PATH):
        with open(PAGE_MAP_PATH, encoding="utf-8", errors="replace") as f:
            page_map = json.load(f)

    all_urls = []
    if os.path.isfile(ALL_URLS_PATH):
        with open(ALL_URLS_PATH, encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if line:
                    all_urls.append(line)

    manifest = None
    if os.path.isfile(MANIFEST_PATH):
        try:
            with open(MANIFEST_PATH, encoding="utf-8", errors="replace") as f:
                manifest = json.load(f)
        except Exception as exc:
            log(f"⚠️  manifest.json 解析失败（{type(exc).__name__}），跳过 known_gaps 参考")
    return page_map, all_urls, manifest


def build_archived_index(page_map):
    """
    建立「归一化 URL → 本地文件」索引，用于判断 all_urls.txt 里哪些已被归档。
    归一化：去掉 query / fragment / 末尾斜杠。
    """
    index = {}
    for url, local in page_map.items():
        index[normalize_url(url)] = local
    return index


def normalize_url(url):
    u = (url or "").strip()
    u = u.split("#")[0].split("?")[0]
    return u.rstrip("/")


def build_already_archived_items(page_map, all_urls):
    """
    任务 A：把 page_map 的每条映射登记为 already_archived；
    再用 all_urls.txt 比对，被 page_map 覆盖的同样标记已归档（且不重复抓取）。
    """
    items = []
    index = build_archived_index(page_map)
    seen_urls = set()

    # ① page_map 里的全部映射
    for url, local in page_map.items():
        items.append({
            "origin_url": url,
            "final_url": None,
            "domain": domain_of(url),
            "source_class": classify_source_class(url, True),
            "status": STATUS_ALREADY,
            "http_status": None,
            "local_path": f"materials/{COURSE_DIRNAME}/pages/{local}",
            "bytes": (os.path.getsize(os.path.join(COURSE_DIR, "pages", local))
                      if os.path.isfile(os.path.join(COURSE_DIR, "pages", local)) else None),
            "sha256": None,
            "content_type": "text/html",
            "used_branch": None,
            "attempts": [],
            "failure_root_cause": None,
            "note": "已归档：来自 page_map.json，本环节不重复抓取",
        })
        seen_urls.add(normalize_url(url))

    # ② all_urls.txt 里被 page_map 覆盖的，也登记为已归档
    for url in all_urls:
        key = normalize_url(url)
        if key in index and key not in seen_urls:
            items.append({
                "origin_url": url,
                "final_url": None,
                "domain": domain_of(url),
                "source_class": classify_source_class(url, True),
                "status": STATUS_ALREADY,
                "http_status": None,
                "local_path": f"materials/{COURSE_DIRNAME}/pages/{index[key]}",
                "bytes": None,
                "sha256": None,
                "content_type": "text/html",
                "used_branch": None,
                "attempts": [],
                "failure_root_cause": None,
                "note": "已归档：all_urls.txt 中的 URL 被 page_map.json 覆盖，不重复抓取",
            })
            seen_urls.add(key)

    return items, seen_urls


# ============================================================ 任务 B：域名分类与处理
def github_to_raw_candidates(url):
    """
    github.com 链接 → 待抓的 (raw_url, used_branch, 说明) 候选列表。
    转换规则：
      /blob/<branch>/<path> → https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>
      /tree/<branch>/<path> → 目录列举不出来，改为猜 <path>/{README.md,assignment.md,writeup.md}
    先去掉 ?query 与 #anchor。
    """
    clean = url.split("#")[0].split("?")[0].rstrip("/")
    m = re.match(r"https?://github\.com/([^/]+)/([^/]+)/(blob|tree)/([^/]+)/(.*)$", clean)
    if m:
        owner, repo, kind, branch, path = m.groups()
        if kind == "blob":
            raw = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
            return [(raw, branch, f"blob 链接直接转为 raw：{path}")]
        if kind == "tree":
            cands = []
            for fname in TREE_CANDIDATE_FILES:
                raw = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}/{fname}"
                cands.append((raw, branch, f"tree 目录无法列举，尝试候选文件 {fname}"))
            return cands
    # 仓库根链接（/owner/repo 或 /owner/repo/tree/<branch>）：试 master/main 下的 README
    m2 = re.match(r"https?://github\.com/([^/]+)/([^/]+)$", clean)
    if m2:
        owner, repo = m2.groups()
        cands = []
        for branch in BRANCH_CANDIDATES:
            raw = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/README.md"
            cands.append((raw, branch, f"仓库根链接无法列举目录，尝试 {branch} 分支的 README.md"))
        return cands
    m3 = re.match(r"https?://github\.com/([^/]+)/([^/]+)/tree/([^/]+)$", clean)
    if m3:
        owner, repo, branch = m3.groups()
        cands = []
        for fname in TREE_CANDIDATE_FILES:
            raw = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{fname}"
            cands.append((raw, branch, f"仓库根目录无法列举，尝试 {fname}"))
        return cands
    return []


def fetch_result_to_item(origin_url, final_url, result, source_class, used_branch,
                         local_path=None, byte_count=None, digest=None):
    return {
        "origin_url": origin_url,
        "final_url": final_url,
        "domain": domain_of(origin_url),
        "source_class": source_class,
        "status": result["status"],
        "http_status": result.get("http_status"),
        "local_path": local_path,
        "bytes": byte_count,
        "sha256": digest,
        "content_type": result.get("content_type"),
        "used_branch": used_branch,
        "attempts": result.get("attempts", []),
        "failure_root_cause": result.get("failure_root_cause"),
        "retried_to_success": result.get("retried_to_success"),
        # observed_at 是「结论粘性」的依据，必须落盘，否则下一轮无法判断这条结论是否确定
        "observed_at": result.get("observed_at"),
    }


def handle_github(fetcher, url):
    """
    B1：github.com → 转 raw 再抓。逐个候选路径明确记录 200/404/403/网络异常。
    ⚠️ 目录（tree）链接必须把每个候选文件的结局都留下，尤其是「全都 404」这个结论。
    """
    items = []
    cands = github_to_raw_candidates(url)
    if not cands:
        items.append({
            "origin_url": url, "final_url": None, "domain": domain_of(url),
            "source_class": "github", "status": STATUS_NOT_ATTEMPTED, "http_status": None,
            "local_path": None, "bytes": None, "sha256": None, "content_type": None,
            "used_branch": None, "attempts": [],
            "failure_root_cause": "github.com 链接形式无法转换为 raw 路径（非 blob/tree/仓库根），未尝试抓取",
        })
        return items

    any_ok = False
    all_causes = []
    for raw_url, branch, why in cands:
        result = fetcher.fetch(raw_url)
        local_path = byte_count = digest = None
        # 同 handle_plain：body 必须非空，否则粘性缓存路径会写 None 而崩
        if result["status"] == STATUS_OK and result.get("body") is not None:
            local_path, byte_count, digest = fetcher.save_to_archive(
                raw_url, result["body"], result.get("content_type"),
                result=result, used_branch=branch, origin_url=url)
            local_path = os.path.relpath(local_path, REPO_ROOT).replace("\\", "/")
            any_ok = True
        elif result.get("failure_root_cause"):
            all_causes.append(f"{os.path.basename(raw_url)} → {result['failure_root_cause']}")
        item = fetch_result_to_item(url, raw_url, result, "github", branch,
                                    local_path, byte_count, digest)
        item["note"] = why
        items.append(item)
        if any_ok:
            break     # 命中即停，避免继续猜其余候选

    if not any_ok:
        # 全部候选都失败：把「为什么」合成一句可复用的结论
        summary = "；".join(all_causes) if all_causes else "无候选路径"
        items[0]["candidate_summary"] = (
            f"该 GitHub 链接的全部 {len(cands)} 个候选路径均未取到内容：{summary}")
    return items


def handle_plain(fetcher, url, source_class, timeout=TIMEOUT_DEFAULT):
    """B2/B3/B4/B7：直接抓一次并记录"""
    result = fetcher.fetch(url, timeout=timeout)
    local_path = byte_count = digest = None
    # ⚠️ 必须同时要求 body 非空：粘性结论缓存会返回
    #    status=fetched_ok 但 body=None（沿用上轮状态码、本轮没下载内容），
    #    只看 status 会把 None 写进文件而崩（实测 --dry-run 触发）。
    if result["status"] == STATUS_OK and result.get("body") is not None:
        local_path, byte_count, digest = fetcher.save_to_archive(
            url, result["body"], result.get("content_type"), result=result)
        local_path = os.path.relpath(local_path, REPO_ROOT).replace("\\", "/")
    return [fetch_result_to_item(url, url, result, source_class, None,
                                 local_path, byte_count, digest)]


def preserve_definitive(new_items, prev_report_ref):
    """
    写回兜底：本轮若因超时拿不到状态码，而上一轮已取得确定性结论（有 http_status），
    则沿用上一轮的结论，只把本轮的超时如实追加进 attempts。
    ⚠️ 这是「三种不可得」口径的最后一道防线：
       绝不允许一次网络抖动把已经确认的 404 改写成 network_error。
    """
    if not prev_report_ref:
        return new_items
    prev_by_final, prev_by_origin = {}, {}
    for it in prev_report_ref.get("items") or []:
        if it.get("http_status") is not None:
            if it.get("final_url"):
                prev_by_final[it["final_url"]] = it
            if it.get("origin_url"):
                prev_by_origin[it["origin_url"]] = it
    for it in new_items:
        if it.get("http_status") is not None or it.get("status") == STATUS_OK:
            continue
        if it.get("status") != STATUS_NETERR:
            continue
        old = prev_by_final.get(it.get("final_url")) or prev_by_origin.get(it.get("origin_url"))
        if not old:
            continue
        it["attempts"] = list(it.get("attempts") or []) + [{
            "url": it.get("final_url") or it.get("origin_url"),
            "result": (f"本轮网络超时（未取得状态码），但上一轮已取得确定性状态码 "
                       f"{old.get('http_status')}，结论沿用上一轮，未被降级"),
            "kind": "preserved_from_previous_run",
        }]
        it["preserved_from_previous_run"] = {
            "status": old.get("status"),
            "http_status": old.get("http_status"),
            "observed_at": old.get("observed_at"),
        }
        it["status"] = old.get("status")
        it["http_status"] = old.get("http_status")
        it["failure_root_cause"] = old.get("failure_root_cause")
        # ⚠️ 关键：把 observed_at 一起写上，否则下一轮构建 definitive_cache 时
        #    这条「保住的结论」不成立，又会被下一轮的超时覆盖掉 —— 保护必须是传递的。
        it["observed_at"] = old.get("observed_at") or local_timestamp()
        it["conclusion_preserved"] = True
    return new_items


def handle_no_fetch(url, source_class, status, cause, note=None):
    """B5/B6：明确不抓，直接登记（省时间，且避免把「需账号」误记成网络错误）"""
    return [{
        "origin_url": url, "final_url": None, "domain": domain_of(url),
        "source_class": source_class, "status": status, "http_status": None,
        "local_path": None, "bytes": None, "sha256": None, "content_type": None,
        "used_branch": None,
        "attempts": [{"url": url, "result": "按设计不发起请求（该域名需账号/不可自动获取）",
                      "kind": status}],
        "failure_root_cause": cause,
        "note": note or "按域名策略直接登记，未发起网络请求",
    }]


# ============================================================ 主流程
def main(argv=None):
    opts = parse_args(argv if argv is not None else sys.argv[1:])
    if opts["help"]:
        print(USAGE)
        return 0
    configure(materials_dir=opts["materials_dir"],
              course_dirname=opts["course_dirname"],
              urls=opts["urls"], map_path=opts["map_path"],
              pages_dir=opts["pages_dir"], archive_dir=opts["archive_dir"],
              manifest=opts["manifest"], report=opts["report"])
    reconfigure_stdout_utf8()

    log("=" * 78)
    log("fetch.py —— 管线 ① 抓取与归档（补抓缺口 + 登记证据链）")
    log(f"资料目录: {MATERIALS_DIR}")
    log(f"归档目录: {ARCHIVE_DIR}")
    # 打印三个源输入，便于换源时核对「读的到底是哪份清单」
    log(f"URL 清单: {ALL_URLS_PATH}")
    log(f"归档映射: {PAGE_MAP_PATH}")
    log(f"抓取报告: {FETCH_REPORT_PATH}")
    log("=" * 78)

    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    # ---- 零覆盖检查：记录 materials/ 状态，收尾时比对
    materials_before = snapshot_tree(MATERIALS_DIR)

    ssl_ctx, ca_used, ca_stats = build_ssl_context()
    log(f"\n【环境自检】SSL 信任库：{ca_used or '系统默认'}"
        f"（CA 证书 {ca_stats.get('x509_ca', 0)} 张）")
    if not ca_used and ca_stats.get("x509_ca", 0) == 0:
        log("  ⚠️ 未找到可用 CA bundle，HTTPS 可能全部验证失败"
            "（会被记为 network_error，属未核查）")
        # ⚠️ 必须给出可操作的修法：不同机器 CA 位置不同，
        #    所以这才是「换机器」时最容易卡住的一步。
        log("     修法：设置环境变量指向可用的 CA bundle 文件，例如")
        log("       set MF_CA_BUNDLE=C:\\path\\to\\cacert.pem     (Windows cmd)")
        log("       $env:MF_CA_BUNDLE=\"C:\\path\\to\\cacert.pem\"  (PowerShell)")
        log("       export MF_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt  (Linux)")
        log("     也支持标准变量 SSL_CERT_FILE / REQUESTS_CA_BUNDLE。")
        log("     常见来源：certifi 包的 cacert.pem、msys2 的 "
            "usr/ssl/certs/ca-bundle.crt、系统信任库。")
    if opts["dry_run"] or opts["offline"]:
        log(f"  运行模式：{'--dry-run（不联网，只登记与规划）' if opts['dry_run'] else '--offline（不联网，待抓项记为 network_error）'}")

    page_map, all_urls, manifest = load_inputs()
    if manifest:
        log(f"  参考 manifest.json：mode={manifest.get('manifest_mode')}, "
            f"known_gaps={len(manifest.get('known_gaps') or [])} 组")
    log(f"  输入：all_urls.txt {len(all_urls)} 行 / page_map.json {len(page_map)} 条")

    # ---- 任务 A：登记已归档
    items, archived_keys = build_already_archived_items(page_map, all_urls)

    # ---- 读取上一轮 fetch_report（用于幂等跳过 + --retry-failed）
    prev_report = None
    if os.path.isfile(FETCH_REPORT_PATH):
        try:
            with open(FETCH_REPORT_PATH, encoding="utf-8", errors="replace") as f:
                prev_report = json.load(f)
        except Exception as exc:
            log(f"⚠️  上一轮 fetch_report.json 解析失败（{type(exc).__name__}），忽略")

    done_ok_keys, retry_keys = {}, None
    definitive_cache = {}
    if prev_report:
        for it in prev_report.get("items") or []:
            if it.get("status") == STATUS_OK and it.get("local_path"):
                p = os.path.join(BASE_DIR, it["local_path"].replace("/", os.sep))
                if os.path.isfile(p) and it.get("sha256") == sha256_file(p):
                    done_ok_keys[normalize_url(it["origin_url"])] = it
            # 收集「上一轮已经拿到状态码」的结论（含 404/403/451），供粘性判定使用
            key_url = it.get("final_url") or it.get("origin_url")
            if key_url and it.get("http_status") is not None:
                definitive_cache[key_url] = {
                    "status": it["status"],
                    "http_status": it.get("http_status"),
                    "failure_root_cause": it.get("failure_root_cause"),
                    "observed_at": it.get("observed_at") or "上一轮",
                }
        if opts["retry_failed"]:
            retry_keys = {normalize_url(it.get("origin_url"))
                          for it in (prev_report.get("items") or [])
                          if it.get("status") in (STATUS_NETERR, STATUS_NOT_ATTEMPTED)}
            log(f"  --retry-failed：上一轮 network_error / not_attempted 共 {len(retry_keys)} 条")
    if definitive_cache:
        log(f"  粘性结论缓存：{len(definitive_cache)} 条已取得状态码的 URL "
            f"本轮不再重问（避免网络抖动把 404 降级成 network_error）")


    # ---- 任务 B：按域名分类，逐类处理
    fetcher = Fetcher(ssl_ctx, dry_run=opts["dry_run"], offline=opts["offline"],
                      definitive_cache=definitive_cache)
    skipped_idempotent = 0
    planned = []

    for url in all_urls:
        key = normalize_url(url)
        if key in archived_keys:
            continue          # 任务 A 已登记，不重复抓取

        # 垃圾行（w3.org 命名空间、混入的 SVG 片段）
        garbage, why = is_garbage_url(url)
        if garbage:
            planned.append({"kind": "garbage", "url": url, "why": why})
            continue

        domain = domain_of(url)
        # B5/B6：明确不抓
        if domain in NO_FETCH_DOMAINS:
            sc, st, cause = NO_FETCH_DOMAINS[domain]
            items.extend(handle_no_fetch(url, sc, st, cause))
            continue

        # 幂等：已成功落盘且 sha256 一致 → 跳过不重复抓
        if key in done_ok_keys and not opts["retry_failed"]:
            prev = done_ok_keys[key]
            p = os.path.join(BASE_DIR, prev["local_path"].replace("/", os.sep))
            item = dict(prev)
            item["note"] = "幂等跳过：archive/ 中已有同名文件且 sha256 一致，本轮不重复抓取"
            # 顺手补齐缺失/失效的 .meta.json（让重复运行能自愈历史产物）
            valid, _meta = meta_sidecar_is_valid(p, prev.get("sha256"))
            if not valid and os.path.isfile(p):
                try:
                    with open(p, "rb") as f:
                        data = f.read()
                    write_meta(p, prev.get("final_url") or prev.get("origin_url"), data,
                               prev.get("content_type"), {"http_status": prev.get("http_status")},
                               prev.get("used_branch"), prev.get("origin_url"))
                    item["note"] += "；并补齐了缺失的 .meta.json"
                except OSError:
                    pass
            items.append(item)
            skipped_idempotent += 1
            continue

        # --retry-failed：只重试指定条目，其余原样保留
        if opts["retry_failed"] and key not in retry_keys:
            continue

        # B1：github.com
        if domain == "github.com" or domain.endswith(".github.com"):
            planned.append({"kind": "github", "url": url})
            continue
        # B2/B3/B4/B7
        planned.append({"kind": "plain", "url": url,
                        "timeout": TIMEOUT_ARXIV if "arxiv.org" in domain else TIMEOUT_DEFAULT})

    # 处理垃圾行登记
    for g in [p for p in planned if p["kind"] == "garbage"]:
        items.append({
            "origin_url": g["url"][:300], "final_url": None, "domain": domain_of(g["url"]),
            "source_class": "supplemental", "status": STATUS_NOT_ATTEMPTED, "http_status": None,
            "local_path": None, "bytes": None, "sha256": None, "content_type": None,
            "used_branch": None, "attempts": [],
            "failure_root_cause": g["why"],
            "note": "all_urls.txt 中的非资源行（命名空间声明/混入的标记片段），未发起请求",
        })

    # 抓取计划
    todo = [p for p in planned if p["kind"] in ("github", "plain")]
    log(f"\n【抓取计划】待抓 {len(todo)} 条"
        f"（github {sum(1 for p in todo if p['kind'] == 'github')} / "
        f"直接抓 {sum(1 for p in todo if p['kind'] == 'plain')}）")
    if opts["dry_run"]:
        log("  --dry-run：以下条目本轮不会真正请求：")
        for p in todo:
            log(f"    · {p['url'][:110]}")

    # 逐条抓取并【每条立即写报告】——网络不稳时中断也不丢证据
    for n, p in enumerate(todo, 1):
        log(f"  [{n}/{len(todo)}] {p['url'][:100]}")
        if p["kind"] == "github":
            new_items = handle_github(fetcher, p["url"])
        else:
            new_items = handle_plain(fetcher, p["url"],
                                     classify_source_class(p["url"], False),
                                     timeout=p.get("timeout", TIMEOUT_DEFAULT))
        # 兜底：本轮若因超时拿不到状态码，而上一轮已取得确定性结论，则沿用上一轮
        new_items = preserve_definitive(new_items, prev_report)
        for it in new_items:
            mark = {"fetched_ok": "✅", "http_404": "·404", "blocked_403": "⛔403",
                    "blocked_451": "⛔451", "network_error": "✗net"}.get(it["status"], it["status"])
            log(f"        {mark}  {it['status']:<16} {(it.get('final_url') or '')[:80]}")
        items.extend(new_items)
        write_report(items, manifest, fetcher, ssl_ctx, ca_used, opts, partial=True)

    # ---- 兜底：上一轮报告里未纳入本轮 items 的旧条目（如 --retry-failed 情形）保留下来
    if prev_report:
        known = {normalize_url(it.get("origin_url")) for it in items}
        for it in prev_report.get("items") or []:
            if normalize_url(it.get("origin_url")) not in known:
                carry = dict(it)
                carry["note"] = (carry.get("note", "") +
                                 "（保留自上一轮 fetch_report）").strip()
                items.append(carry)

    # ---- 写最终报告
    report = write_report(items, manifest, fetcher, ssl_ctx, ca_used, opts)

    # ============================================================ 控制台自检
    s = report["summary"]

    log("\n" + "=" * 78)
    log("【1】分类计数（summary）")
    log("=" * 78)
    for k in SUMMARY_KEYS:
        log(f"    {k:<24} {s.get(k)}")
    extra = {k: v for k, v in s.items() if k not in SUMMARY_KEYS}
    for k, v in extra.items():
        log(f"    {k:<24} {v}   （补充口径）")

    # 1b. 结论粘性核对：确定性结论有没有被网络抖动污染
    n_definitive = sum(1 for it in items if it.get("http_status") is not None)
    n_preserved = sum(1 for it in items if it.get("conclusion_preserved"))
    n_cached = sum(1 for it in items if it.get("cached_from_previous_run"))
    log(f"\n【1b】结论粘性核对（防止 network_error 覆盖已确认的状态码）")
    log(f"    已取得明确 HTTP 状态码的条目 : {n_definitive}")
    log(f"    其中沿用上一轮结论未降级     : {n_preserved + n_cached + fetcher.cache_hits}"
        f"（复用缓存 {n_cached + fetcher.cache_hits} + 超时后回退 {n_preserved}）")
    log(f"    network_error（拿不到状态码）: {s.get('network_error')}"
        f"  ← 这些是「未核查」，绝不等同于「不存在」")
    if n_preserved + n_cached + fetcher.cache_hits:
        log("    → 说明本轮确实发生了网络抖动，但已确认的 404/403/451 没有被改写成 network_error")

    # 2. 落盘核对
    log("\n【2】落盘核对：archive/ 实际文件数 vs summary.fetched_ok")
    archived_files, hash_ok, hash_bad = [], 0, []
    for root, _dirs, files in os.walk(ARCHIVE_DIR):
        for fn in files:
            if fn.endswith(".meta.json"):
                continue
            fp = os.path.join(root, fn)
            archived_files.append(fp)
            if os.path.isfile(fp + ".meta.json"):
                try:
                    meta = json.load(open(fp + ".meta.json", encoding="utf-8"))
                    if sha256_file(fp) == meta.get("sha256"):
                        hash_ok += 1
                    else:
                        hash_bad.append(os.path.relpath(fp, REPO_ROOT))
                except Exception:
                    hash_bad.append(os.path.relpath(fp, REPO_ROOT))
    log(f"    archive/ 实际落盘文件数 : {len(archived_files)}")
    log(f"    summary.fetched_ok      : {s.get('fetched_ok')}")
    log(f"    带 .meta.json 且 sha256 可复算一致 : {hash_ok}")
    if hash_bad:
        log(f"    ⚠️ sha256 不一致或缺少元数据 : {hash_bad}")
    match = "✅ 一致" if len(archived_files) == s.get("fetched_ok") else "⚠️ 不一致，需人工核对"
    log(f"    核对结果                : {match}")
    log(f"    （注：跨轮幂等跳过不会重复落盘，历史文件会累计在 archive/ 中）")

    # 3. 零覆盖检查
    log("\n【3】零覆盖检查：materials/ 是否被修改")
    materials_after = snapshot_tree(MATERIALS_DIR)
    changed = diff_snapshot(materials_before, materials_after)
    if changed:
        log(f"    ❌ 检测到 materials/ 发生变化（{len(changed)} 项）：")
        for c in changed[:20]:
            log(f"        {c}")
    else:
        log(f"    ✅ materials/ 下 {len(materials_after)} 个文件全部未被修改"
            f"（快照 sha256 前后一致）")

    # 4. 重试有效性
    log("\n【4】重试有效性")
    log(f"    本轮 HTTP 请求次数            : {fetcher.request_count}")
    log(f"    「重试后才成功」的 URL 数      : {len(fetcher.retry_successes)}")
    if fetcher.retry_successes:
        for u in fetcher.retry_successes[:10]:
            log(f"        · {u[:110]}")
        log("    → 证明重试机制确实把「本来会失败的抓取」救了回来")
    else:
        log("    → 本轮没有出现「首次失败、重试成功」的情况"
            "（不代表重试无用：它防的是间歇性超时）")

    # 5. 缺口清单
    log("\n【5】缺口清单：按 status 分组的所有非 fetched_ok 条目")
    grouped = {}
    for it in items:
        if it.get("status") == STATUS_OK:
            continue
        grouped.setdefault(it["status"], []).append(it)
    if not grouped:
        log("    无缺口")
    for st in sorted(grouped, key=lambda k: -len(grouped[k])):
        group = grouped[st]
        log(f"\n    [{st}] 共 {len(group)} 条")
        seen_cause = set()
        for it in group[:6]:
            cause = it.get("failure_root_cause") or "(未记录根因)"
            log(f"        · {it['origin_url'][:96]}")
            if cause not in seen_cause:
                log(f"            根因: {cause}")
                seen_cause.add(cause)
        if len(group) > 6:
            log(f"        …… 另有 {len(group) - 6} 条同类条目（详见 fetch_report.json）")

    log("\n" + "=" * 78)
    log(f"已写出：{FETCH_REPORT_PATH}")
    log(f"归档目录：{ARCHIVE_DIR}")
    log("=" * 78)
    return 0


# ============================================================ 报告写出与快照
def build_summary(items):
    summary = {
        "total_urls": len(items),
        STATUS_ALREADY: 0, STATUS_OK: 0, STATUS_404: 0, STATUS_403: 0,
        STATUS_NEEDS_ACCOUNT: 0, STATUS_UNREACHABLE: 0, STATUS_NETERR: 0,
        STATUS_NOT_ATTEMPTED: 0,
        "total_bytes_archived": 0,
    }
    for it in items:
        st = it.get("status")
        if st in summary and st not in ("total_urls", "total_bytes_archived"):
            summary[st] += 1
        elif st and st not in summary:
            summary[st] = summary.get(st, 0) + 1     # 兜住 blocked_451 等未枚举状态
        if st == STATUS_OK and it.get("bytes"):
            summary["total_bytes_archived"] += it["bytes"]
    return summary


def write_report(items, manifest, fetcher, ssl_ctx, ca_used, opts, partial=False):
    """写 fetch_report.json；partial=True 时是逐条增量落盘（防中断丢证据）"""
    summary = build_summary(items)
    report = {
        "generated_by": "fetch.py",
        "environment_notes": ENVIRONMENT_NOTES,
        "run_options": {
            "mode": ("retry_failed" if opts.get("retry_failed")
                     else "dry_run" if opts.get("dry_run")
                     else "offline" if opts.get("offline") else "normal"),
            "ssl_ca_bundle": ca_used,
            "timeout_default": TIMEOUT_DEFAULT,
            "timeout_arxiv": TIMEOUT_ARXIV,
            "retry_delays": RETRY_DELAYS,
            "domain_sleep": DOMAIN_SLEEP,
        },
        "inputs": {
            "all_urls": os.path.relpath(ALL_URLS_PATH, REPO_ROOT).replace("\\", "/"),
            "page_map": os.path.relpath(PAGE_MAP_PATH, REPO_ROOT).replace("\\", "/"),
            "manifest_mode": (manifest or {}).get("manifest_mode"),
            "manifest_known_gaps": len((manifest or {}).get("known_gaps") or []),
        },
        "summary": summary,
        "items": items,
    }
    if partial:
        report["partial"] = True      # 增量落盘标记；最终一次会覆盖为完整报告
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    atomic_write_text(FETCH_REPORT_PATH, payload)
    return report


def atomic_write_text(path, text, attempts=5):
    """
    原子写文本。
    ⚠️ Windows 上 os.replace 会因目标文件被占用（杀软扫描 / 其他进程正在读）而抛
       PermissionError: [WinError 5]，这不是逻辑错误而是共享冲突，必须重试。
       重试仍失败则退回「直接覆盖写」，宁可牺牲原子性也不能让整轮抓取白跑。
    """
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    for i in range(attempts):
        try:
            os.replace(tmp, path)
            return True
        except PermissionError:
            time.sleep(0.3 * (i + 1))
        except OSError:
            time.sleep(0.3 * (i + 1))
    try:
        os.remove(tmp)
    except OSError:
        pass
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return False


def snapshot_tree(root):
    """记录目录下所有文件的 sha256，用于零覆盖检查"""
    snap = {}
    if not os.path.isdir(root):
        return snap
    for dirpath, _dirs, files in os.walk(root):
        for fn in files:
            fp = os.path.join(dirpath, fn)
            try:
                snap[os.path.relpath(fp, root)] = (os.path.getsize(fp), sha256_file(fp))
            except OSError:
                snap[os.path.relpath(fp, root)] = (-1, "unreadable")
    return snap


def diff_snapshot(before, after):
    changed = []
    for k in sorted(set(before) | set(after)):
        if before.get(k) != after.get(k):
            changed.append(f"{k}: {before.get(k)} → {after.get(k)}")
    return changed


if __name__ == "__main__":
    sys.exit(main())
