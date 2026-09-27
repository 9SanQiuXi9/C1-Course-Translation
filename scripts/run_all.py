# -*- coding: utf-8 -*-
"""
run_all.py —— 管线一键入口

按固定顺序跑完整条管线，每步都做「产物存在性」校验，最后给出汇总表。

  ┌─ 步骤 ─────────────────────────────────────────────────────────┐
  │ ① 体检账本   build_manifest.py         -> work/reports/manifest.json
  │ ② 抽取       extract.py                -> work/extracted/*.md
  │ ③ 术语表     init_glossary.py --md     -> work/glossary/glossary.json + .md
  │ ④ 槽位       check_slots.py            -> work/slots/slot_report.json
  │ ⑤ 质检       check_quality.py all      -> work/quality/*.json
  │ ⑥ 下载       fetch.py                  -> data/fetched/        （默认 dry-run）
  └────────────────────────────────────────────────────────────────┘

设计取舍（都写在对应位置的中文注释里）：
  · 用 subprocess 调用另存脚本，而不是 import 调 main()
    理由：各脚本在 import 期就算好常量、也许还会改 stdout 编码，
    同进程混跑容易互相干扰；子进程隔离最干净，也与你手工逐条敲命令等价。
  · 第 ⑥ 步默认走 --dry-run（不联网）
    理由：一键入口不该有看不见的网络副作用。要真抓用 --with-fetch。
  · 每步都校验产物，而不是只看退出码
    理由：脚本可能"成功退出但没写出东西"（磁盘满、路径错、静默跳过）。

用法：
  python scripts/run_all.py                  跑 ①~⑤（含 ⑥ 的 dry-run）
  python scripts/run_all.py --with-fetch     含真实网络抓取
  python scripts/run_all.py --no-fetch       完全跳过第 ⑥ 步
  python scripts/run_all.py --list           只打印计划，不执行
  python scripts/run_all.py --only extract   只跑某一步（可多次指定）
  python scripts/run_all.py --from glossary  从某一步开始跑到末尾
  python scripts/run_all.py --skip slots     跳过某一步（可多次指定）
  python scripts/run_all.py --continue-on-error  某步失败也继续往下跑
  python scripts/run_all.py --accept-glossary-change
                                             术语表改过时，接受并重算槽位
"""
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import datetime
import os
import subprocess
import time

# ══════════════════════════════════════════════════════════════════
#  路径常量（换项目时只改这几处）
# ══════════════════════════════════════════════════════════════════
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
LOG_DIR = os.path.join(BASE_DIR, "work", "logs")     # 每步完整输出留档

# 产物路径（存在性校验用；与各脚本内的常量保持一致）
P_MANIFEST = os.path.join(BASE_DIR, "work", "reports", "manifest.json")
P_EXTRACTED = os.path.join(BASE_DIR, "work", "extracted")
P_GLOSSARY = os.path.join(BASE_DIR, "work", "glossary", "glossary.json")
P_GLOSSARY_MD = os.path.join(BASE_DIR, "work", "glossary", "glossary.md")
P_SLOTS = os.path.join(BASE_DIR, "work", "slots", "slot_report.json")
P_QUALITY = os.path.join(BASE_DIR, "work", "quality", "stats.json")


# ══════════════════════════════════════════════════════════════════
#  步骤定义
# ══════════════════════════════════════════════════════════════════
def _has_any_file(d):
    """目录里是否有文件（递归）。用于校验「抽取」这类产出多篇文档的步骤。"""
    if not os.path.isdir(d):
        return False, "目录不存在"
    n = 0
    for _root, _dirs, files in os.walk(d):
        n += len(files)
    if n == 0:
        return False, "目录为空"
    return True, f"{n} 个文件"


def _has_file(p, min_bytes=2):
    """
    单个文件是否存在且有实际内容。
    ⚠️ 阈值只用来排除「空文件 / 只剩一个换行」，不要用 KB 级阈值 ——
       小规模的换源（比如只有 1 篇文档）会产出合法但很小的 JSON，
       用 1 KB 卡它会把成功误判成失败（实测踩到）。
       内容是否完整要靠各脚本自己的校验，不靠文件大小。
    """
    if not os.path.isfile(p):
        return False, "文件不存在"
    n = os.path.getsize(p)
    if n < min_bytes:
        return False, f"文件仅 {n} 字节，疑似未写出内容"
    if n < 1024:
        return True, f"{n} 字节"
    return True, f"{n/1024:.1f} KB"


# key, 显示名, 脚本, 附加参数, 产物校验, 说明
def build_steps(with_fetch=False, no_fetch=False, accept_change=False,
                paths=None):
    """
    构造步骤表。
    paths: dict 可含 materials_dir / course_dirname / work_dir / out_dir /
           archive_dir —— 换源时把这些透传给每个脚本。
    ⚠️ 一律用「显式长参数」传递，不做隐式环境变量耦合：
       这样日志里能直接看到每一步到底读了哪些路径，便于核对。
    """
    p = paths or {}

    def add(*pairs):
        """把 paths 里的键映射成脚本参数，跳过空值。"""
        args = []
        for key, flag in pairs:
            v = p.get(key)
            if v:
                args += [flag, v]
        return args

    # 各步共用的「换源参数」
    src_args = add(("materials_dir", "--materials-dir"),
                   ("course_dirname", "--course-dirname"))
    extract_args = src_args + add(("archive_dir", "--archive-dir"),
                                  ("manifest", "--manifest"),
                                  ("extracted_dir", "--out-dir"),
                                  ("extract_report", "--report"))
    glossary_args = add(("extracted_dir", "--extracted-dir"),
                        ("glossary", "--glossary"),
                        ("glossary_max_terms", "--max-terms"))
    # ⚠️ --from-corpus-only 是「布尔开关」，没有取值，
    #    所以不能走 add() 那套「键→值」的映射，必须单独追加。
    if p.get("glossary_from_corpus"):
        glossary_args = glossary_args + ["--from-corpus-only"]
    slots_args = add(("extracted_dir", "--extracted-dir"),
                     ("translated_dir", "--translated-dir"),
                     ("glossary", "--glossary"),
                     ("slot_report", "--slot-report"))
    quality_args = add(("extracted_dir", "--src-dir"),
                       ("translated_dir", "--dst-dir"),
                       ("glossary", "--glossary"),
                       ("quality_dir", "--out-dir"))
    fetch_args = add(("urls", "--urls"), ("map", "--map"),
                     ("archive_dir", "--archive-dir"),
                     ("manifest", "--manifest"),
                     ("fetch_report", "--report"))

    fetch_note = "（默认 dry-run，不联网）"
    if with_fetch:
        fetch_note = "（真实网络抓取）"
    elif no_fetch:
        fetch_note = "（已跳过）"
    else:
        fetch_args = fetch_args + ["--dry-run"]

    steps = [
        {
            "key": "manifest", "no": "①", "name": "体检账本",
            "script": "build_manifest.py",
            "args": src_args + add(("manifest", "--out")),
            "artifacts": [(P_MANIFEST, _has_file)],
            "note": "统计正文字数、区分严格/宽松抽取口径",
        },
        {
            "key": "extract", "no": "②", "name": "抽取",
            "script": "extract.py", "args": extract_args,
            "artifacts": [(P_EXTRACTED, _has_any_file)],
            "note": "HTML / PDF / SPA → 统一 Markdown",
        },
        {
            "key": "glossary", "no": "③", "name": "术语表",
            "script": "init_glossary.py", "args": ["--md"] + glossary_args,
            "artifacts": [(P_GLOSSARY, _has_file), (P_GLOSSARY_MD, _has_file)],
            "note": ("从当前语料重建术语表（草稿态 frozen=false，需人工定稿）"
                     if p.get("glossary_from_corpus")
                     else "生成并冻结术语表（人工复查 glossary.md）"),
        },
        {
            "key": "slots", "no": "④", "name": "槽位",
            "script": "check_slots.py",
            "args": (["--accept-glossary-change"] if accept_change else [])
                    + slots_args,
            "artifacts": [(P_SLOTS, _has_file)],
            "note": "按文档统计术语槽位；术语表改过需 --accept-glossary-change",
        },
        {
            "key": "quality", "no": "⑤", "name": "质检",
            "script": "check_quality.py", "args": ["all"] + quality_args,
            "artifacts": [(P_QUALITY, _has_file)],
            "note": "L1 结构 / L2 术语 / L3 反例自测",
        },
        {
            "key": "fetch", "no": "⑥", "name": "下载",
            "script": "fetch.py", "args": fetch_args,
            "artifacts": [],       # 抓取是可选取证步骤，缺失不算失败
            "note": f"抓取归档到 data/fetched/{fetch_note}",
            "optional": no_fetch,
        },
    ]
    return steps



def resolve_paths(opt):
    """
    把 --source-root / --materials-dir 等选项解析成各脚本要用的绝对路径。

    ⚠️ 换源的核心约定：给了 --source-root ROOT 时，所有中间产物与交付
       都落到 ROOT 下（ROOT/work/... 与 ROOT/output/...），完全不碰主仓库的
       work/ 与 output/。这样换源验证不会污染正式产出。
    """
    root = opt.get("source_root")
    if not root:
        return {}
    root = os.path.abspath(root)
    return {
        "materials_dir": (os.path.abspath(opt["materials_dir"])
                          if opt.get("materials_dir") else None),
        "course_dirname": opt.get("course_dirname"),
        "extracted_dir": os.path.join(root, "work", "extracted"),
        "glossary": os.path.join(root, "work", "glossary", "glossary.json"),
        "slot_report": os.path.join(root, "work", "slots", "slot_report.json"),
        "quality_dir": os.path.join(root, "work", "quality"),
        "translated_dir": os.path.join(root, "output", "translated"),
        "archive_dir": os.path.join(root, "fetched"),
        "manifest": os.path.join(root, "work", "reports", "manifest.json"),
        "extract_report": os.path.join(root, "work", "reports", "extract_report.json"),
        "fetch_report": os.path.join(root, "work", "reports", "fetch_report.json"),
        "urls": opt.get("urls"),
        "map": opt.get("map"),
        # 术语表重建（与路径无关，但要一起透传给 ③ 步）
        "glossary_from_corpus": opt.get("from_corpus_only"),
        "glossary_max_terms": (str(opt["max_terms"])
                               if opt.get("max_terms") is not None else None),
    }


# ══════════════════════════════════════════════════════════════════
#  换源：产物校验路径跟着走
# ══════════════════════════════════════════════════════════════════
def retarget_artifacts(steps, paths):
    """
    换源时把每步的产物校验路径改到新位置。

    ⚠️ 必须做：否则脚本把产出写到新目录，而校验还去旧位置找，
       会误报「产物不存在」让整步失败 —— 而步骤其实是成功的。
    做法是「替换产物列表里等于默认路径的项」，不必给每步硬编码字段名。
    """
    if not paths:
        return
    mapping = {
        P_MANIFEST: paths.get("manifest"),
        P_EXTRACTED: paths.get("extracted_dir"),
        P_GLOSSARY: paths.get("glossary"),
        P_GLOSSARY_MD: (os.path.join(os.path.dirname(paths["glossary"]),
                                     "glossary.md")
                        if paths.get("glossary") else None),
        P_SLOTS: paths.get("slot_report"),
        P_QUALITY: (os.path.join(paths["quality_dir"], "stats.json")
                    if paths.get("quality_dir") else None),
    }
    for st in steps:
        st["artifacts"] = [(mapping.get(old) or old, fn)
                           for old, fn in st["artifacts"]]


# ══════════════════════════════════════════════════════════════════
#  单步执行
# ══════════════════════════════════════════════════════════════════
def run_step(step, log_dir, verbose=True):
    """
    跑一步。返回结果 dict：
      ok       该步是否通过（退出码 0 且产物齐备）
      rc       退出码
      artifact 产物校验明细
      seconds  耗时
      log      完整输出留档路径
    """
    script = os.path.join(SCRIPT_DIR, step["script"])
    if not os.path.isfile(script):
        return {"ok": False, "rc": None, "seconds": 0.0, "log": None,
                "artifact": [], "error": f"脚本不存在：{script}"}

    cmd = [sys.executable, script] + step["args"]
    if verbose:
        print("-" * 78)
        print(f"  {step['no']} {step['name']}　{step['script']} "
              f"{' '.join(step['args'])}")
        print(f"     {step['note']}")
        print("-" * 78)

    t0 = time.time()
    try:
        # 在仓库根目录执行，保证脚本内相对路径的解析基准一致
        proc = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True,
                              text=True, encoding="utf-8", errors="replace")
        out, rc = (proc.stdout or "") + (proc.stderr or ""), proc.returncode
    except Exception as e:
        out, rc = f"[run_all] 启动子进程失败：{type(e).__name__}: {e}", 99
    secs = time.time() - t0

    # 完整输出留档：控制台只给尾部，全量进日志
    os.makedirs(log_dir, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_path = os.path.join(log_dir, f"{step['key']}-{stamp}.log")
    with open(log_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"# {step['name']} ({step['script']})\n")
        f.write(f"# 命令: {' '.join(cmd)}\n")
        f.write(f"# 退出码: {rc}   耗时: {secs:.1f}s\n")
        f.write("#" + "-" * 76 + "\n")
        f.write(out)

    if verbose:
        # 只打印尾部，避免刷屏；完整内容在日志里
        lines = [ln for ln in out.rstrip().split("\n") if ln.strip()]
        tail = lines[-12:] if len(lines) > 12 else lines
        if len(lines) > 12:
            print(f"     ……（完整输出 {len(lines)} 行，见日志）")
        for ln in tail:
            print("     " + ln)

    # ---- 产物校验
    checks = []
    art_ok = True
    for path, fn in step["artifacts"]:
        ok, detail = fn(path)
        rel = os.path.relpath(path, BASE_DIR).replace(os.sep, "/")
        checks.append({"path": rel, "ok": ok, "detail": detail})
        if not ok:
            art_ok = False

    ok = (rc == 0) and art_ok
    if verbose:
        print()
        for c in checks:
            mark = "✅" if c["ok"] else "❌"
            print(f"     {mark} 产物 {c['path']}  {c['detail']}")
        state = "✅ 通过" if ok else "❌ 失败"
        print(f"     {state}　退出码 {rc}　耗时 {secs:.1f}s")
        print(f"     日志 {os.path.relpath(log_path, BASE_DIR).replace(os.sep, '/')}")
        print()

    return {"ok": ok, "rc": rc, "seconds": secs, "log": log_path,
            "artifact": checks, "error": None}


# ══════════════════════════════════════════════════════════════════
#  参数解析
# ══════════════════════════════════════════════════════════════════
USAGE = """run_all.py —— 管线一键入口

用法：
  python scripts/run_all.py [选项]

选项：
  --with-fetch                 第 ⑥ 步做真实网络抓取（默认只 dry-run）
  --no-fetch                   完全跳过第 ⑥ 步
  --accept-glossary-change     术语表已改动时，接受并重算槽位

换源（不在主仓库 work/ output/ 上落任何东西）：
  --source-root ROOT           换一份资料跑全流程，产出落到 ROOT 下
  --materials-dir DIR          课程原始资料根目录（默认 data/materials）
  --course-dirname NAME        课程子目录名（默认 CS146S_offline）
  --urls PATH                  URL 清单（默认 <course>/all_urls.txt）
  --map PATH                   本地归档映射（默认 <course>/page_map.json）

换源后重建术语表（换到别的领域时必须加）：
  --from-corpus-only           ③ 步不带种子，纯从新语料抽候选建表
                               产出的表 frozen=false（草稿态，需人工定稿）
  --max-terms N                术语条数上限（配合 --from-corpus-only 使用）
                               例：--from-corpus-only --max-terms 120
  --only  <key>                只跑指定步骤（可重复）
  --skip  <key>                跳过指定步骤（可重复）
  --from  <key>                从指定步骤开始跑到末尾
  --continue-on-error          某步失败仍继续（默认遇错即停）
  --quiet                      只输出汇总表
  --list                       只打印计划，不执行
  -h, --help                   显示本帮助

步骤 key：
  manifest ① 体检账本   extract ② 抽取      glossary ③ 术语表
  slots    ④ 槽位       quality ⑤ 质检      fetch    ⑥ 下载
"""

# 步骤顺序（--from 用到）
STEP_ORDER = ["manifest", "extract", "glossary", "slots", "quality", "fetch"]


def parse_args(argv):
    o = {"with_fetch": False, "no_fetch": False, "accept": False,
         "only": [], "skip": [], "from": None, "continue": False,
         "quiet": False, "list": False, "help": False,
         "source_root": None, "materials_dir": None,
         "course_dirname": None, "urls": None, "map": None,
         "from_corpus_only": False, "max_terms": None}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("-h", "--help"):
            o["help"] = True
        elif a == "--with-fetch":
            o["with_fetch"] = True
        elif a == "--no-fetch":
            o["no_fetch"] = True
        elif a == "--accept-glossary-change":
            o["accept"] = True
        elif a == "--continue-on-error":
            o["continue"] = True
        elif a == "--quiet":
            o["quiet"] = True
        elif a == "--list":
            o["list"] = True
        elif a == "--from-corpus-only":
            # 布尔开关：换源时从新语料重建术语表，不用旧种子
            o["from_corpus_only"] = True
        elif a == "--max-terms":
            if i + 1 >= len(argv):
                raise SystemExit(f"❌ {a} 后面要跟一个数字\n\n{USAGE}")
            try:
                o["max_terms"] = int(argv[i + 1])
            except ValueError:
                raise SystemExit(f"❌ --max-terms 需要一个整数，收到：{argv[i+1]!r}")
            i += 1
        elif a in ("--source-root", "--materials-dir", "--course-dirname",
                   "--urls", "--map"):
            if i + 1 >= len(argv):
                raise SystemExit(f"❌ {a} 后面要跟一个值\n\n{USAGE}")
            o[a.lstrip("-").replace("-", "_")] = argv[i + 1]
            i += 1
        elif a in ("--only", "--skip", "--from"):
            if i + 1 >= len(argv):
                raise SystemExit(f"❌ {a} 后面要跟一个步骤 key\n\n{USAGE}")
            val = argv[i + 1]
            if val not in STEP_ORDER:
                raise SystemExit(f"❌ 未知步骤 key：{val}\n"
                                 f"   可用：{', '.join(STEP_ORDER)}\n\n{USAGE}")
            if a == "--only":
                o["only"].append(val)
            elif a == "--skip":
                o["skip"].append(val)
            else:
                o["from"] = val
            i += 1
        else:
            raise SystemExit(f"❌ 未知参数：{a}\n\n{USAGE}")
        i += 1
    return o


def select_steps(steps, opt):
    """按 --only / --skip / --from 过滤步骤，返回 (保留的步骤, 被跳过的名字)。"""
    sel, dropped = [], []
    for st in steps:
        k = st["key"]
        if opt["only"] and k not in opt["only"]:
            dropped.append(f"{st['no']} {st['name']}")
            continue
        if k in opt["skip"]:
            dropped.append(f"{st['no']} {st['name']}")
            continue
        if opt["from"] and STEP_ORDER.index(k) < STEP_ORDER.index(opt["from"]):
            dropped.append(f"{st['no']} {st['name']}")
            continue
        if st.get("optional"):
            dropped.append(f"{st['no']} {st['name']}（--no-fetch）")
            continue
        sel.append(st)
    return sel, dropped


# ══════════════════════════════════════════════════════════════════
#  入口
# ══════════════════════════════════════════════════════════════════
def main(argv):
    try:
        opt = parse_args(argv)
    except SystemExit as e:
        print(e)
        return 64

    if opt["help"]:
        print(USAGE)
        return 0

    if opt["with_fetch"] and opt["no_fetch"]:
        print("❌ --with-fetch 与 --no-fetch 不能同时用")
        return 64

    paths = resolve_paths(opt)
    steps = build_steps(with_fetch=opt["with_fetch"], no_fetch=opt["no_fetch"],
                        accept_change=opt["accept"], paths=paths)
    retarget_artifacts(steps, paths)
    sel, dropped = select_steps(steps, opt)

    print("=" * 78)
    print("run_all.py —— 管线一键入口")
    print("=" * 78)
    print(f"  仓库根目录：{BASE_DIR}")
    print(f"  脚本目录　：{SCRIPT_DIR}")
    print(f"  Python　　：{sys.executable}")
    print(f"  执行计划　：{len(sel)} 步")
    for st in sel:
        print(f"    {st['no']} {st['name']:<6} {st['script']} "
              f"{' '.join(st['args'])}")
    if dropped:
        print(f"  已跳过　　：{', '.join(dropped)}")
    print()

    if opt["list"]:
        print("（--list：仅打印计划，未执行）")
        return 0
    if not sel:
        print("❌ 没有可执行的步骤（检查 --only / --skip / --from）")
        return 64

    # ---- 逐步执行
    results, t_all = [], time.time()
    for st in sel:
        r = run_step(st, LOG_DIR, verbose=not opt["quiet"])
        r["step"] = st
        results.append(r)
        if not r["ok"] and not opt["continue"]:
            print("=" * 78)
            print(f"❌ 第 {st['no']} 步「{st['name']}」失败，管线中止")
            print("=" * 78)
            if r["rc"]:
                print(f"   退出码 {r['rc']}")
            print(f"   完整输出：{os.path.relpath(r['log'], BASE_DIR)}")
            print("   如需跳过失败继续跑：加 --continue-on-error")
            _print_summary(results, time.time() - t_all)
            return 1

    total = time.time() - t_all
    _print_summary(results, total)

    bad = [r for r in results if not r["ok"]]
    if bad:
        print(f"❌ {len(bad)}/{len(results)} 步未通过")
        return 1
    print(f"✅ 全部 {len(results)} 步通过")
    print("   下一步：人工复查 work/glossary/glossary.md，"
          "并用 translate_queue.py 逐篇翻译")
    return 0


def _print_summary(results, total):
    print("=" * 78)
    print("汇总")
    print("=" * 78)
    print(f"  {'步骤':<16}{'结果':<8}{'退出码':<8}{'耗时':<10}产物")
    for r in results:
        st = r["step"]
        mark = "✅ 通过" if r["ok"] else "❌ 失败"
        rc = "-" if r["rc"] is None else str(r["rc"])
        arts = "，".join(f"{c['path']} {c['detail']}" for c in r["artifact"])
        print(f"  {st['no']+' '+st['name']:<16}{mark:<8}{rc:<8}"
              f"{r['seconds']:>6.1f}s   {arts or '（无）'}")
    print(f"\n  总耗时 {total:.1f}s　日志目录 "
          f"{os.path.relpath(LOG_DIR, BASE_DIR).replace(os.sep, '/')}")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
