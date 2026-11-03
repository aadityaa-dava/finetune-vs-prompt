"""Final test-set table. Assumptions are marked; everything else is read from results/."""
import json

ROWS = [
    ("Qwen2.5-3B, zero-shot (local)", "base_zeroshot", 2.08, "local"),
    ("Qwen2.5-3B, 4-shot (local)", "base_fewshot", 2.33, "local"),
    ("gpt-oss-120b, 4-shot (Groq API)", "gptoss120b_fewshot", None, "api"),
    ("**Qwen2.5-3B + LoRA r8, short prompt (local)**", "lora_r8_zeroshot", 2.15, "local"),
    ("Qwen2.5-3B + LoRA r8, 4-shot prompt (local)", "lora_r8_fewshot", 2.73, "local"),
]
PRICE_IN, PRICE_OUT = 0.15, 0.60   # USD per 1M tokens, Groq list price, checked 2026-11-03
WATTS, USD_PER_KWH = 30, 0.15      # ASSUMPTIONS (not measured): laptop power draw, electricity price

lines = ["| Model (test, n=428) | JSON valid | Pair F1 | Precision / Recall | Exact match | Latency mean / p95 | Peak memory | Cost per 1,000 requests |",
         "|---|---|---|---|---|---|---|---|"]
for label, name, mem, kind in ROWS:
    m = json.load(open(f"results/metrics_{name}_test.json"))
    preds = [json.loads(l) for l in open(f"results/preds_{name}_test.jsonl")]
    lat = sorted(p["latency_s"] for p in preds)
    n = len(lat)
    mean, p95 = sum(lat) / n, lat[int(n * 0.95)]
    if kind == "api":
        tin = sum(p["input_tokens"] for p in preds)
        tout = sum(p["output_tokens"] for p in preds)
        cost = f"${(tin * PRICE_IN + tout * PRICE_OUT) / 1e6 / n * 1000:.3f} (list price)"
        memtxt = "n/a (hosted)"
    else:
        kwh = WATTS * mean * 1000 / 3.6e6
        cost = f"$0 cash; ~${kwh * USD_PER_KWH:.4f} electricity (assumed)"
        memtxt = f"{mem:.2f} GB"
    lines.append(f"| {label} | {m['json_valid_rate']:.1%} | {m['pair_f1']:.3f} | {m['pair_precision']:.3f} / {m['pair_recall']:.3f} "
                 f"| {m['sentence_exact_match']:.1%} | {mean:.2f}s / {p95:.2f}s | {memtxt} | {cost} |")
lines += ["",
          "Notes: single training seed. Local latency = M4 MacBook Pro, one request at a time. API latency includes network and shared free-tier queueing.",
          f"API cost = measured tokens x Groq list price (${PRICE_IN}/M in, ${PRICE_OUT}/M out); we paid $0 on the free tier. Electricity assumes {WATTS} W and ${USD_PER_KWH}/kWh and ignores hardware cost.",
          "Test-set F1 differences (paired bootstrap, 95% CI): LoRA vs gpt-oss-120b +0.066 [+0.025, +0.108]; LoRA vs 3B 4-shot +0.152 [+0.107, +0.198]."]
open("results/final_table.md", "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
