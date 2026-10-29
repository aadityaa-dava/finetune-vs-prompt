"""Run a Gemini model over a split with the SAME few-shot prompt as the other models.
Paced to a requests-per-minute limit; resumes if the output file already exists.
Usage: PYTHONPATH=src python src/run_gemini.py --model gemini-2.5-flash --split val --name gemini25flash_fewshot [--limit 3] [--rpm 5]
"""
import argparse
import json
import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import SYSTEM, build_messages_fewshot


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--split", default="val")
    ap.add_argument("--name", required=True)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--rpm", type=float, default=5.0)
    a = ap.parse_args()

    load_dotenv(".env")
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"], http_options=types.HttpOptions(timeout=60000))
    rows = [json.loads(l) for l in open(f"data/processed/{a.split}.jsonl")]
    if a.limit:
        rows = rows[: a.limit]

    out_path = f"results/preds_{a.name}_{a.split}.jsonl"
    done = set()
    if os.path.exists(out_path):
        done = {json.loads(l)["text"] for l in open(out_path)}
    print(f"{len(done)} already done, {len(rows) - len(done)} to go")

    cfg = types.GenerateContentConfig(
        system_instruction=SYSTEM, temperature=0, max_output_tokens=1024,
    )
    min_gap = 60.0 / a.rpm
    last = 0.0
    with open(out_path, "a") as f:
        for i, e in enumerate(rows):
            if e["text"] in done:
                continue
            msgs = build_messages_fewshot(e["text"])[1:]  # system prompt goes in config instead
            contents = [
                types.Content(role="user" if m["role"] == "user" else "model",
                              parts=[types.Part(text=m["content"])])
                for m in msgs
            ]
            wait = min_gap - (time.time() - last)
            if wait > 0:
                time.sleep(wait)
            for attempt in range(6):
                last = time.time()
                t0 = time.perf_counter()
                try:
                    r = client.models.generate_content(model=a.model, contents=contents, config=cfg)
                    dt = time.perf_counter() - t0
                    break
                except Exception as ex:
                    print("error:", type(ex).__name__, str(ex)[:300])
                    if "404" in str(ex) or "NOT_FOUND" in str(ex) or "INVALID_ARGUMENT" in str(ex):
                        print("fatal config error; not retrying")
                        return
                    time.sleep(30 * (attempt + 1) if ("429" in str(ex) or "RESOURCE_EXHAUSTED" in str(ex)) else 10)
            else:
                print("giving up; re-run the same command to resume")
                return
            u = r.usage_metadata
            rec = {
                "text": e["text"], "raw_output": r.text or "", "latency_s": dt,
                "input_tokens": getattr(u, "prompt_token_count", None),
                "output_tokens": getattr(u, "candidates_token_count", None),
                "thinking_tokens": getattr(u, "thoughts_token_count", None),
            }
            f.write(json.dumps(rec) + "\n")
            f.flush()
            if i < 3:
                print(f"--- {e['text']}\n{rec['raw_output']}\n({dt:.2f}s, in={rec['input_tokens']}, out={rec['output_tokens']})")
    print("done:", out_path)


if __name__ == "__main__":
    main()
