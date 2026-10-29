"""Run a Groq-hosted model over a split with the SAME few-shot prompt as the other models.
Paced; resumes if the output file exists.
Usage: PYTHONPATH=src python src/run_groq.py --model openai/gpt-oss-120b --split val --name gptoss120b_fewshot [--limit 5] [--rpm 10]
"""
import argparse
import json
import os
import time
from dotenv import load_dotenv
from groq import Groq
from prompts import build_messages_fewshot


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--split", default="val")
    ap.add_argument("--name", required=True)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--rpm", type=float, default=10.0)
    ap.add_argument("--effort", default="low")
    a = ap.parse_args()

    load_dotenv(".env")
    client = Groq(api_key=os.environ["GROQ_API_KEY"], timeout=60.0, max_retries=0)
    rows = [json.loads(l) for l in open(f"data/processed/{a.split}.jsonl")]
    if a.limit:
        rows = rows[: a.limit]

    out_path = f"results/preds_{a.name}_{a.split}.jsonl"
    done = set()
    if os.path.exists(out_path):
        done = {json.loads(l)["text"] for l in open(out_path)}
    print(f"{len(done)} already done, {len(rows) - len(done)} to go")

    min_gap = 60.0 / a.rpm
    last = 0.0
    with open(out_path, "a") as f:
        for i, e in enumerate(rows):
            if e["text"] in done:
                continue
            msgs = build_messages_fewshot(e["text"])
            wait = min_gap - (time.time() - last)
            if wait > 0:
                time.sleep(wait)
            for attempt in range(6):
                last = time.time()
                t0 = time.perf_counter()
                try:
                    r = client.chat.completions.create(
                        model=a.model, messages=msgs, temperature=0,
                        max_completion_tokens=1024,
                        extra_body={"reasoning_effort": a.effort},
                    )
                    dt = time.perf_counter() - t0
                    break
                except Exception as ex:
                    msg = str(ex)
                    print("error:", type(ex).__name__, msg[:300])
                    if "400" in msg or "404" in msg or "401" in msg:
                        print("fatal config error; not retrying")
                        return
                    if "tokens per day" in msg.lower() or "TPD" in msg:
                        print("daily token cap reached; re-run tomorrow to resume")
                        return
                    time.sleep(20 * (attempt + 1))
            else:
                print("giving up; re-run the same command to resume")
                return
            u = r.usage
            details = getattr(u, "completion_tokens_details", None)
            rec = {
                "text": e["text"], "raw_output": r.choices[0].message.content or "", "latency_s": dt,
                "input_tokens": getattr(u, "prompt_tokens", None),
                "output_tokens": getattr(u, "completion_tokens", None),
                "reasoning_tokens": getattr(details, "reasoning_tokens", None) if details else None,
            }
            f.write(json.dumps(rec) + "\n")
            f.flush()
            if i < 3:
                print(f"--- {e['text']}\n{rec['raw_output']}\n({dt:.2f}s, in={rec['input_tokens']}, out={rec['output_tokens']}, reasoning={rec['reasoning_tokens']})")
    print("done:", out_path)


if __name__ == "__main__":
    main()
