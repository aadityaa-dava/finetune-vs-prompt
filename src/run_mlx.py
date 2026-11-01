"""Run an MLX model over a split and save predictions with per-request latency.
Usage: python src/run_mlx.py --model <hf-id-or-path> --split val --name base_zeroshot [--limit 5]
"""
import argparse
import json
import time
from mlx_lm import load, generate
from prompts import build_messages, build_messages_fewshot


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--split", default="val")
    ap.add_argument("--name", required=True)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--fewshot", action="store_true")
    ap.add_argument("--adapter", default=None)
    ap.add_argument("--max_tokens", type=int, default=256)
    a = ap.parse_args()

    model, tok = load(a.model, adapter_path=a.adapter)
    rows = [json.loads(l) for l in open(f"data/processed/{a.split}.jsonl")]
    if a.limit:
        rows = rows[: a.limit]

    def run(text):
        prompt = tok.apply_chat_template((build_messages_fewshot if a.fewshot else build_messages)(text), add_generation_prompt=True, tokenize=False)
        t0 = time.perf_counter()
        out = generate(model, tok, prompt=prompt, max_tokens=a.max_tokens, verbose=False)  # greedy
        return out, time.perf_counter() - t0

    run("warm-up sentence.")  # first call includes compile/cache cost; exclude it from latency

    out_path = f"results/preds_{a.name}_{a.split}.jsonl"
    with open(out_path, "w") as f:
        for i, e in enumerate(rows):
            out, dt = run(e["text"])
            f.write(json.dumps({"text": e["text"], "raw_output": out, "latency_s": dt}) + "\n")
            if i < 3:
                print(f"--- {e['text']}\n{out}\n({dt:.2f}s)")
    import mlx.core as mx
    print("peak GPU memory (GB):", round(mx.get_peak_memory() / 1e9, 2))
    print("wrote", out_path, len(rows))


if __name__ == "__main__":
    main()
