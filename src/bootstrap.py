"""Paired bootstrap on val sentences. Usage: python src/bootstrap.py PRED_A PRED_B [GOLD]
Reports pair-F1 for each file and the 95% interval of (B - A)."""
import json
import random
import sys
sys.path.insert(0, "src")
from evaluate import extract_json, to_pairs, norm


def per_sentence(gold_path, pred_path):
    gold = {}
    for l in open(gold_path):
        e = json.loads(l)
        gold[e["text"]] = {(norm(x["drug"]), norm(x["effect"])) for x in e["adverse_events"]}
    preds = {}
    for l in open(pred_path):
        p = json.loads(l)
        preds[p["text"]] = p
    rows = []
    for t, g in gold.items():
        pairs = to_pairs(extract_json(preds[t]["raw_output"]))
        rows.append((0, 0, len(g)) if pairs is None else (len(pairs & g), len(pairs - g), len(g - pairs)))
    return rows


def f1(rows, idx):
    tp = sum(rows[i][0] for i in idx)
    fp = sum(rows[i][1] for i in idx)
    fn = sum(rows[i][2] for i in idx)
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    return 2 * p * r / (p + r) if p + r else 0.0


a_path, b_path = sys.argv[1], sys.argv[2]
gold_path = sys.argv[3] if len(sys.argv) > 3 else "data/processed/val.jsonl"
A, B = per_sentence(gold_path, a_path), per_sentence(gold_path, b_path)
n = len(A)
rng = random.Random(0)
diffs = []
for _ in range(2000):
    idx = [rng.randrange(n) for _ in range(n)]
    diffs.append(f1(B, idx) - f1(A, idx))
diffs.sort()
full = list(range(n))
print(f"A F1 {f1(A, full):.3f} | B F1 {f1(B, full):.3f} | B-A {f1(B, full) - f1(A, full):+.3f} | 95% CI [{diffs[49]:+.3f}, {diffs[1949]:+.3f}]")
