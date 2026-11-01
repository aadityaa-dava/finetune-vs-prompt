"""Convert train/val splits into MLX-LM chat format. Test is NOT touched here."""
import json
import os
from prompts import build_messages

os.makedirs("data/mlx", exist_ok=True)
for src, dst in [("train", "train"), ("val", "valid")]:
    n = 0
    with open(f"data/processed/{src}.jsonl") as f_in, open(f"data/mlx/{dst}.jsonl", "w") as f_out:
        for line in f_in:
            e = json.loads(line)
            msgs = build_messages(e["text"]) + [
                {"role": "assistant", "content": json.dumps({"adverse_events": e["adverse_events"]})}
            ]
            f_out.write(json.dumps({"messages": msgs}) + "\n")
            n += 1
    print(dst, n)
