| Model (test, n=428) | JSON valid | Pair F1 | Precision / Recall | Exact match | Latency mean / p95 | Peak memory | Cost per 1,000 requests |
|---|---|---|---|---|---|---|---|
| Qwen2.5-3B, zero-shot (local) | 26.9% | 0.154 | 0.483 / 0.092 | 7.9% | 0.75s / 1.05s | 2.08 GB | $0 cash; ~$0.0009 electricity (assumed) |
| Qwen2.5-3B, 4-shot (local) | 91.1% | 0.581 | 0.662 / 0.518 | 42.5% | 1.41s / 1.93s | 2.33 GB | $0 cash; ~$0.0018 electricity (assumed) |
| gpt-oss-120b, 4-shot (Groq API) | 100.0% | 0.667 | 0.739 / 0.607 | 58.4% | 1.00s / 2.64s | n/a (hosted) | $0.112 (list price) |
| **Qwen2.5-3B + LoRA r8, short prompt (local)** | 99.8% | 0.733 | 0.747 / 0.720 | 66.8% | 1.03s / 1.76s | 2.15 GB | $0 cash; ~$0.0013 electricity (assumed) |
| Qwen2.5-3B + LoRA r8, 4-shot prompt (local) | 99.8% | 0.571 | 0.532 / 0.617 | 49.3% | 1.85s / 2.83s | 2.73 GB | $0 cash; ~$0.0023 electricity (assumed) |

Notes: single training seed. Local latency = M4 MacBook Pro, one request at a time. API latency includes network and shared free-tier queueing.
API cost = measured tokens x Groq list price ($0.15/M in, $0.6/M out); we paid $0 on the free tier. Electricity assumes 30 W and $0.15/kWh and ignores hardware cost.
Test-set F1 differences (paired bootstrap, 95% CI): LoRA vs gpt-oss-120b +0.066 [+0.025, +0.108]; LoRA vs 3B 4-shot +0.152 [+0.107, +0.198].
