# -*- coding: utf-8 -*-
"""
确定性测试：用假 urlopen 验证
  ① 重试机制真的能救回「首次失败」的抓取
  ② 粘性结论：上一轮拿到 404 的 URL，本轮超时不会被降级成 network_error
不联网，全部可控。
"""
import importlib.util, io, json, os, sys, urllib.error

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
os.environ["PYTHONIOENCODING"] = "utf-8"

spec = importlib.util.spec_from_file_location(
    "fetchmod",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "fetch.py"))
fm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fm)


class FakeResp:
    def __init__(self, body=b"hello", status=200, ctype="text/plain"):
        self._body = body
        self.status = status
        self.headers = {"Content-Type": ctype, "Date": "Wed, 01 Jan 2026 00:00:00 GMT"}

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def make_urlopen(script):
    """script: 依次弹出的动作，'timeout' | ('http', code) | ('ok', body)"""
    calls = {"n": 0}

    def fake_urlopen(req, **kwargs):
        i = calls["n"]
        calls["n"] += 1
        action = script[i] if i < len(script) else script[-1]
        if action == "timeout":
            raise urllib.error.URLError("timed out")
        if isinstance(action, tuple) and action[0] == "http":
            raise urllib.error.HTTPError(req.full_url, action[1], "err", {}, io.BytesIO(b""))
        return FakeResp(body=action[1] if isinstance(action, tuple) else b"hello")
    return fake_urlopen, calls


fm.time.sleep = lambda s: None      # 跳过等待，测试要快
print("sleep 已打桩，测试不会真的等\n")

# ---------- 场景 1：首次超时 → 重试成功 ----------
print("【场景 1】首次超时、第二次成功 → 应记为 fetched_ok 且 retried_to_success=2")
fake, calls = make_urlopen(["timeout", ("ok", b"payload-1")])
fm.urllib.request.urlopen = fake
f = fm.Fetcher(None)
r = f.fetch("https://raw.githubusercontent.com/o/r/master/a.md")
print("  status            :", r["status"])
print("  retried_to_success:", r.get("retried_to_success"))
print("  retry_successes   :", f.retry_successes)
print("  HTTP 请求次数      :", calls["n"], "（应为 2）")
assert r["status"] == "fetched_ok" and r.get("retried_to_success") == 2 and calls["n"] == 2
print("  ✅ 通过\n")

# ---------- 场景 2：两次超时后拿到 404 → 404 是结论，应记账为 http_404 ----------
print("【场景 2】两次超时后得到 404 → 应记为 http_404（不是 network_error）")
fake, calls = make_urlopen(["timeout", "timeout", ("http", 404)])
fm.urllib.request.urlopen = fake
f = fm.Fetcher(None)
r = f.fetch("https://raw.githubusercontent.com/o/r/master/missing.md")
print("  status     :", r["status"], "| http_status:", r["http_status"])
print("  根因       :", r["failure_root_cause"][:60], "…")
assert r["status"] == "http_404" and r["http_status"] == 404
print("  ✅ 通过\n")

# ---------- 场景 3：全程超时 → network_error（未核查），且与 404 明确区分 ----------
print("【场景 3】4 次全部超时 → 应记为 network_error，根因写明「未核查」")
fake, calls = make_urlopen(["timeout"])
fm.urllib.request.urlopen = fake
f = fm.Fetcher(None)
r = f.fetch("https://www.anthropic.com/claude-code")
print("  status    :", r["status"], "| http_status:", r["http_status"])
print("  根因      :", r["failure_root_cause"][:80], "…")
print("  尝试次数  :", calls["n"], "（应为 4 = 首次 + 3 次重试）")
assert r["status"] == "network_error" and r["http_status"] is None and calls["n"] == 4
print("  ✅ 通过\n")

# ---------- 场景 4：粘性结论 —— 上一轮 404，本轮超时 → 不得降级 ----------
print("【场景 4】粘性结论：上一轮已确认 404，本轮网络超时 → 结论必须保持 http_404")
URL404 = "https://raw.githubusercontent.com/o/r/master/week3/assignment.md"
prev_report = {"items": [{
    "origin_url": "https://github.com/o/r/blob/master/week3/assignment.md",
    "final_url": URL404, "status": "http_404", "http_status": 404,
    "failure_root_cause": "HTTP 404：服务器可达且明确返回「不存在」。这是有效信息",
    "observed_at": "2026-01-01T00:00:00",
}]}
cache = {URL404: {"status": "http_404", "http_status": 404,
                  "failure_root_cause": prev_report["items"][0]["failure_root_cause"],
                  "observed_at": "2026-01-01T00:00:00"}}
fake, calls = make_urlopen(["timeout"])
fm.urllib.request.urlopen = fake
f = fm.Fetcher(None, definitive_cache=cache)
r = f.fetch(URL404)
print("  status                    :", r["status"], "| http_status:", r["http_status"])
print("  cached_from_previous_run  :", r.get("cached_from_previous_run"))
print("  本轮实际请求次数           :", calls["n"], "（应为 0，确定性结论不重复问）")
assert r["status"] == "http_404" and calls["n"] == 0
print("  ✅ 通过\n")

# ---------- 场景 5：preserve_definitive 兜底 ----------
print("【场景 5】即使缓存未命中，preserve_definitive 也要把本轮超时回退成上一轮的 404")
items = [{"origin_url": "https://github.com/o/r/blob/master/week3/assignment.md",
          "final_url": URL404, "status": "network_error", "http_status": None,
          "attempts": [], "failure_root_cause": "网络不可达…"}]
out = fm.preserve_definitive(items, prev_report)
print("  status        :", out[0]["status"], "| http_status:", out[0]["http_status"])
print("  preserved_from:", out[0].get("preserved_from_previous_run"))
print("  attempts 追加 :", out[0]["attempts"][-1]["kind"])
assert out[0]["status"] == "http_404" and out[0]["http_status"] == 404
assert out[0]["attempts"][-1]["kind"] == "preserved_from_previous_run"
print("  ✅ 通过\n")

print("=" * 60)
print("全部 5 个场景通过：重试有效、404/403/network_error 三者严格区分、结论不降级")
