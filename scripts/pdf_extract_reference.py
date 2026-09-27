#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pdf_extract_reference.py —— PDF 文本抽取【参考实现】

【它为什么存在】
项目里另有一份 extract.py 在做同样的事，但反复出问题，根因被误判成"文件损坏"。
本脚本用已验证可跑的路径实现，用来：
  1. 提供【已知答案】作为验收基准（见文末 REFERENCE 表）
  2. 供 extract.py 对照差异，定位 bug 在解析的哪一步

⚠️ 这不是最终交付的抽取器，是【对照基准】。
   最终应把本脚本验证过的做法合并进 extract.py。

【它踩过并被验证的关键点】
  1. 对象体必须取对捕获组：
     r"(\\d+)\\s+(\\d+)\\s+obj(.*?)endobj"  → group(3) 是对象体，group(2) 是世代号
     取错 group(2) 会得到一个 "0"，于是所有流的统计全部归零，
     三份 PDF 会被误判成 image_only。
  2. 必须先解压 /ObjStm 对象流，否则在原始字节里搜 /BaseFont、/ToUnicode
     全部是 0 次 —— 搜不到 ≠ 不存在。
  3. /Length 不可信！实测 obj 447 声明 102 字节，实际流长 8196 字节。
     按 /Length 硬切会把 Flate 流截断。应该：
       a) 优先用 /Length，但失败就扩大到 endstream
       b) zlib 在 EOS 处会自己停住并忽略尾部，所以给足余量是安全的
  4. 不能把「压缩字节里恰好含 BT」当成「这是文本流」。
     判断前必须先成功解压 —— 压缩流以 x\\xda (78 9a) 开头，那不是 PDF 文本算子。
  5. TJ 数组里的数字是字距调整：
     大负数（< -100）代表空格；小负数（如 -7）是字距微调，不能当空格。
  6. 多个字体的 CMap 【不能全局合并】，必须按当前字体分别查，否则串码。
  7. 拿不到可靠的 /Contents 引用时【拒绝兜底扫描】—— 兜底会把 Type3 字形程序
     当正文，产出大量乱码。宁可如实报"抽不出来"。

【用法】
  python pdf_extract_reference.py                 # 跑三份基准 PDF，打印与基准的对比
  python pdf_extract_reference.py <某个.pdf>      # 单跑一份
  python pdf_extract_reference.py --dump <pdf>    # 单跑并输出前若干行文本供人眼核对
"""

import json
import os
import re
import sys
import zlib

# ---------------------------------------------------------------- 路径
BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(BASE)
PDF_DIR = os.path.join(REPO, "data", "materials", "CS146S_offline", "pdfs")
OUT_DIR = os.path.join(REPO, "work", "extracted", "_pdf_reference")

# ---------------------------------------------------------------- 已确认基准
# 这些数字是参考实现实测得到的。extract.py 的产出应与之接近（允许 ±10%，
# 因为换行与空白处理策略可能略有差异）。
# ⚠️ 达不到不是"文件坏了"，是解析器有 bug。
REFERENCE = {
    "ai-assisted-code-review-assessment.pdf": {
        "english_words": 9631,
        "prose_lines": 278,
        "note": "pdfTeX 生成，20 个标准字体，17 个 ToUnicode 映射表",
    },
    "how-anthropic-uses-claude-code.pdf": {
        "english_words": 8250,
        "prose_lines": 756,
        "note": "扫描件 + OCR 隐藏文本层（字体名 HiddenHorzOCR）。"
                "8 个 ObjStm 全部可解压。部分字符因字形映射缺失而丢失。",
    },
    "how-openai-uses-codex.pdf": {
        "english_words": None,
        "prose_lines": None,
        "note": "Type3 矢量字形（17 个 /CharProcs）。需结合字体的 /Encoding "
                "/Differences 与 /ToUnicode，尚未验证出可靠结果。",
    },
}


# ================================================================ 对象加载
def load_objects(raw: bytes) -> dict:
    """
    返回 {对象号: 对象体}。
    包含未压缩对象，以及从 /ObjStm 对象流里解出的被压缩对象。

    ⚠️ 关键点 1：正则的 group(3) 才是对象体，group(2) 是世代号。
    ⚠️ 关键点 2：/ObjStm 必须解压，否则字体信息全部搜不到。
    """
    objs = {}

    # ---- 未压缩对象
    for m in re.finditer(rb"(?<![0-9])(\d+)\s+(\d+)\s+obj", raw):
        num = int(m.group(1))
        body_start = m.end()
        end = raw.find(b"endobj", body_start)
        objs[num] = raw[body_start:end if end > 0 else body_start + 300000]

    # ---- 从对象流解出被压缩对象
    for m in re.finditer(
        rb"<<(?:[^<>]|<[^<>]*>)*?/Type\s*/ObjStm(?:[^<>]|<[^<>]*>)*?>>", raw
    ):
        header = m.group(0)
        data = extract_stream_bytes(raw, m.end())
        if data is None:
            continue
        try:
            first = int(re.search(rb"/First\s+(\d+)", header).group(1))
            count = int(re.search(rb"/N\s+(\d+)", header).group(1))
        except Exception:
            continue
        pairs = re.findall(rb"(\d+)\s+(\d+)", data[:first])
        for i in range(min(count, len(pairs))):
            obj_num = int(pairs[i][0])
            off = int(pairs[i][1])
            nxt = (
                int(pairs[i + 1][1])
                if i + 1 < len(pairs)
                else len(data) - first
            )
            objs.setdefault(obj_num, data[first + off: first + nxt])

    return objs


def extract_stream_bytes(raw: bytes, search_from: int):
    """
    从 search_from 附近找到 stream 关键字，返回【解压后】的流数据。

    ⚠️ 关键点 3：/Length 不可信（实测声明 102 字节、实际 8196 字节）。
       所以策略是：先按 endstream 取完整块，再交给 zlib。
       zlib 在 EOS 处会自己停住并忽略尾部数据，所以给足余量是安全的。

    ⚠️ 关键点 4：解压失败时返回 None，绝不把压缩字节当文本用。
    """
    sm = re.search(rb"stream\r?\n", raw[search_from: search_from + 64])
    if not sm:
        return None
    start = search_from + sm.end()
    end = raw.find(b"endstream", start)
    if end < 0:
        return None

    blob = raw[start:end]

    # 按 endstream 取的完整块优先（不受 /Length 偏小影响）
    for candidate in (blob, blob.rstrip(b"\r\n")):
        try:
            return zlib.decompress(candidate)
        except zlib.error:
            pass

    # 兜底：用 decompressobj 解可解的前缀（应对尾部被污染的情况）
    try:
        d = zlib.decompressobj()
        out = d.decompress(blob)
        if out:
            return out
    except zlib.error:
        pass

    return None


def get_stream(obj_body: bytes):
    """从一个对象体里取解压后的流（对象体自身就含 stream）。"""
    sm = re.search(rb"stream\r?\n", obj_body)
    if not sm:
        return None
    start = sm.end()
    end = obj_body.find(b"endstream", start)
    if end < 0:
        return None
    blob = obj_body[start:end]
    for candidate in (blob, blob.rstrip(b"\r\n")):
        try:
            return zlib.decompress(candidate)
        except zlib.error:
            pass
    try:
        out = zlib.decompressobj().decompress(blob)
        return out or None
    except zlib.error:
        return None


# ================================================================ CMap 解析
def parse_cmap(cm: bytes) -> dict:
    """解析 ToUnicode CMap，返回 {字符码: Unicode 字符串}。"""
    mp = {}
    for blk in re.findall(rb"beginbfchar(.*?)endbfchar", cm, re.S):
        for src, dst in re.findall(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", blk):
            try:
                mp[int(src, 16)] = bytes.fromhex(dst.decode()).decode(
                    "utf-16-be", "replace"
                )
            except Exception:
                pass
    for blk in re.findall(rb"beginbfrange(.*?)endbfrange", cm, re.S):
        for lo, hi, dst in re.findall(
            rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", blk
        ):
            a, b, base = int(lo, 16), int(hi, 16), int(dst, 16)
            if b - a > 65535:
                continue
            for i in range(b - a + 1):
                try:
                    mp[a + i] = chr(base + i)
                except Exception:
                    pass
    return mp


# ================================================================ 字体表
FONT_RES_RE = re.compile(rb"/([A-Za-z0-9_]+)\s+(\d+)\s+\d+\s+R")


def build_font_maps(objs: dict) -> tuple:
    """
    返回 (资源名 -> 字体对象号, 字体对象号 -> CMap)。

    ⚠️ 关键点 6：CMap 按字体分别保存，不做全局合并。
    """
    res_to_font = {}
    for body in objs.values():
        for name, num in FONT_RES_RE.findall(body):
            res_to_font.setdefault(name.decode("latin-1"), int(num))

    font_to_cmap = {}
    for num, body in objs.items():
        tu = re.search(rb"/ToUnicode\s+(\d+)\s+\d+\s+R", body)
        if not tu:
            continue
        cm_stream = get_stream(objs.get(int(tu.group(1)), b""))
        if cm_stream and b"beginbf" in cm_stream:
            font_to_cmap[num] = parse_cmap(cm_stream)
    return res_to_font, font_to_cmap


# ================================================================ 文本抽取
TOKEN_RE = re.compile(
    rb"/([A-Za-z0-9_]+)\s+[\d.]+\s+Tf"      # 字体切换
    rb"|\(((?:[^()\\]|\\.)*)\)"              # 字面串
    rb"|<([0-9A-Fa-f\s]+)>"                  # 十六进制串
    rb"|\[|\]"
    rb"|-?\d+\.?\d*"
    rb"|\bTJ\b|\bTj\b|\bTd\b|\bTD\b|\bT\*\b|\bTm\b|\bET\b|\bBT\b"
)


def unescape_pdf_string(s: bytes) -> bytes:
    s = re.sub(rb"\\([()\\])", rb"\1", s)
    s = re.sub(rb"\\([nrtbf])",
               lambda m: {b"n": b"\n", b"r": b"\r", b"t": b"\t",
                          b"b": b"\b", b"f": b"\f"}[m.group(1)], s)
    s = re.sub(rb"\\([0-7]{1,3})",
               lambda m: bytes([int(m.group(1), 8) & 0xFF]), s)
    return s


def decode_with_font(data: bytes, cmap: dict, two_byte: bool) -> str:
    """
    用指定字体的 CMap 解码一串字节。

    ⚠️ 关键点 4 续：cmap 为空时【不做 ASCII 猜测】。
       猜测会产出乱码，让"抽取成功"变成假象。宁可返回空串。
    """
    if not cmap:
        return ""
    if two_byte:
        out = []
        for i in range(0, len(data) - 1, 2):
            code = int.from_bytes(data[i:i + 2], "big")
            ch = cmap.get(code)
            if ch is not None:
                out.append(ch)
        return "".join(out)
    out = []
    for b in data:
        ch = cmap.get(b)
        if ch is not None:
            out.append(ch)
    return "".join(out)


def extract_text_from_stream(stream: bytes, res_to_font: dict,
                             font_to_cmap: dict):
    """从一个已解压的内容流里抽文本，返回行列表。"""
    cur_font_obj = None
    cur_cmap = {}
    lines = []
    buf = []
    in_array = False

    for m in TOKEN_RE.finditer(stream):
        tok = m.group(0)

        if m.group(1) is not None:                      # /Fxx ... Tf
            name = m.group(1).decode("latin-1")
            cur_font_obj = res_to_font.get(name)
            cur_cmap = font_to_cmap.get(cur_font_obj, {})
            continue

        if tok == b"[":
            in_array = True
            continue
        if tok == b"]":
            in_array = False
            continue

        if m.group(2) is not None:                      # 字面串
            data = unescape_pdf_string(m.group(2))
            # Type3 / 单字节字体：逐字节查表；若表键值普遍 > 255，按两字节
            two_byte = bool(cur_cmap) and max(cur_cmap) > 255
            buf.append(decode_with_font(data, cur_cmap, two_byte))
            continue

        if m.group(3) is not None:                      # 十六进制串
            hx = re.sub(rb"\s", b"", m.group(3))
            if len(hx) % 2:
                hx += b"0"
            try:
                data = bytes.fromhex(hx.decode())
            except Exception:
                continue
            buf.append(decode_with_font(data, cur_cmap, True))
            continue

        if in_array and re.fullmatch(rb"-?\d+\.?\d*", tok):
            # ⚠️ 关键点 5：TJ 字距。大负数当空格，小负数是字距微调。
            try:
                if float(tok) < -100:
                    buf.append(" ")
            except ValueError:
                pass
            continue

        if tok in (b"Td", b"TD", b"T*", b"Tm", b"ET"):
            if buf:
                lines.append("".join(buf))
                buf = []

    if buf:
        lines.append("".join(buf))

    return [ln for ln in lines if ln.strip()]


# ================================================================ 主流程
def collect_content_streams(objs: dict):
    """
    收集可信的内容流。

    ⚠️ 关键点 7：只接受【能成功解压】且【含真实 BT 算子】的流。
       不做"扫描所有流"的兜底 —— 那会把 Type3 字形程序当正文。
       判断顺序很重要：先解压，再判断 BT。压缩字节里恰好含 'BT' 是巧合。
    """
    streams = []
    for num, body in objs.items():
        if b"stream" not in body:
            continue
        data = get_stream(body)
        if data is None:
            continue                       # 解压失败 → 丢弃，不当文本用
        if b"BT" not in data:
            continue
        if b"endchar" in data:             # Type3 字形程序，不是内容流
            continue
        streams.append((num, data))
    return streams


def probe(path: str) -> dict:
    raw = open(path, "rb").read()
    objs = load_objects(raw)
    res_to_font, font_to_cmap = build_font_maps(objs)
    streams = collect_content_streams(objs)

    text_lines = []
    for _num, data in streams:
        text_lines.extend(
            extract_text_from_stream(data, res_to_font, font_to_cmap)
        )

    text = "\n".join(text_lines)
    words = len(re.findall(r"[A-Za-z]{2,}", text))
    prose = [
        ln for ln in text_lines
        if len(re.findall(r"[A-Za-z]{2,}", ln)) >= 5
        and sum(c.isalpha() for c in ln) / max(1, len(ln)) > 0.5
    ]

    return {
        "file": os.path.basename(path),
        "bytes": len(raw),
        "objects": len(objs),
        "content_streams": len(streams),
        "cmaps": len(font_to_cmap),
        "chars": len(text),
        "english_words": words,
        "prose_lines": len(prose),
        "text": text,
        "_prose_sample": prose[:8],
    }


def main(argv) -> int:
    dump = "--dump" in argv
    argv = [a for a in argv if a != "--dump"]

    targets = []
    if len(argv) > 1 and argv[1].endswith(".pdf"):
        targets = [argv[1]]
    else:
        targets = [os.path.join(PDF_DIR, f) for f in sorted(REFERENCE)]
        targets = [t for t in targets if os.path.isfile(t)]

    os.makedirs(OUT_DIR, exist_ok=True)
    print("=" * 78)
    print("PDF 文本抽取 —— 参考实现（对照基准）")
    print("=" * 78)

    all_ok = True
    for path in targets:
        r = probe(path)
        ref = REFERENCE.get(r["file"], {})
        print(f"\n### {r['file']}")
        print(f"    字节 {r['bytes']:,}   对象 {r['objects']:,}   "
              f"内容流 {r['content_streams']}   CMap {r['cmaps']}")
        print(f"    抽出 {r['chars']:,} 字符 / {r['english_words']:,} 英文词 / "
              f"{r['prose_lines']} 行散文")

        exp_w = ref.get("english_words")
        if exp_w:
            lo, hi = exp_w * 0.9, exp_w * 1.1
            ok = lo <= r["english_words"] <= hi
            all_ok &= ok
            print(f"    基准 {exp_w:,} 词  →  {'✅ 达标' if ok else '❌ 未达标'}")
        else:
            print(f"    基准：无（{ref.get('note', '')}）")

        print(f"    说明：{ref.get('note', '')}")

        if r["_prose_sample"]:
            print("    散文抽样：")
            for ln in r["_prose_sample"]:
                print(f"      > {ln[:96]}")

        out_txt = os.path.join(OUT_DIR, r["file"].replace(".pdf", ".txt"))
        with open(out_txt, "w", encoding="utf-8") as f:
            f.write(r["text"])
        print(f"    → 已写出 {os.path.relpath(out_txt, REPO)}")

    print("\n" + "=" * 78)
    if all_ok:
        print("参考实现全部达标。extract.py 的产出若达不到这些数字，说明是解析器 bug。")
    else:
        print("⚠️ 有文件未达标 —— 参考实现本身需要继续排查（不是文件坏了）。")
    return 0


if __name__ == "__main__":
    # Windows 控制台编码兜底
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.exit(main(sys.argv))
