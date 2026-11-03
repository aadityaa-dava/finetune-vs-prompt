"""Benchmark the local server on VAL (not test). Sequential full pass (scored) + 4-way concurrency throughput."""
import json
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, "src")
from prompts import build_messages

URL = "http://127.0.0.1:8080/v1/chat/completions"
MODEL = "fused_model/qwen25-3b-ade-r8"
rows = [json.loads(l) for l in open("data/processed/val.jsonl")]


def call(text):
    body = json.dumps({"model": MODEL, "messages": build_messages(text), "temperature": 0, "max_tokens": 256}).encode()
    req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json"})
    t0 = time.perf_counter()
    r = json.load(urllib.request.urlopen(req, timeout=120))
    return r["choices"][0]["message"]["content"], time.perf_counter() - t0


call("warm-up sentence.")
out, lat = [], []
t0 = time.perf_counter()
for e in rows:
    o, dt = call(e["text"])
    out.append({"text": e["text"], "raw_output": o, "latency_s": dt})
    lat.append(dt)
wall = time.perf_counter() - t0
lat.sort()
n = len(lat)
print(f"sequential: {n} req in {wall:.0f}s = {n / wall:.2f} req/s | p50 {lat[n // 2]:.2f}s | p95 {lat[int(n * 0.95)]:.2f}s | mean {sum(lat) / n:.2f}s")
with open("results/preds_served_r8_val.jsonl", "w") as f:
    for r in out:
        f.write(json.dumps(r) + "\n")

sub = [e["text"] for e in rows[:100]]
t0 = time.perf_counter()
with ThreadPoolExecutor(4) as ex:
    res = list(ex.map(call, sub))
wall = time.perf_counter() - t0
l2 = sorted(dt for _, dt in res)
print(f"4 concurrent: 100 req in {wall:.0f}s = {100 / wall:.2f} req/s | p50 {l2[50]:.2f}s | p95 {l2[95]:.2f}s")
