"""Score a predictions file against gold. Usage:
python src/evaluate.py --gold data/processed/val.jsonl --pred results/preds_X.jsonl --name X
Pred file format: one JSON per line: {"text": ..., "raw_output": "...", "latency_s": float}
"""
import argparse
import json
import re


def norm(s):
    return re.sub(r"\s+", " ", str(s).strip().lower())


def extract_json(raw):
    """Parse model output. Strips ```json fences; otherwise requires the output to be valid JSON as-is
    (we do NOT hunt for JSON inside chatty text, so format-following is measured)."""
    s = raw.strip()
    m = re.match(r"^```(?:json)?\s*(.*?)\s*```$", s, re.DOTALL)
    if m:
        s = m.group(1)
    try:
        return json.loads(s)
    except Exception:
        return None


def to_pairs(obj):
    """Return set of (drug, effect) if obj matches the schema, else None."""
    if not isinstance(obj, dict) or not isinstance(obj.get("adverse_events"), list):
        return None
    pairs = set()
    for item in obj["adverse_events"]:
        if not isinstance(item, dict) or not isinstance(item.get("drug"), str) or not isinstance(item.get("effect"), str):
            return None
        pairs.add((norm(item["drug"]), norm(item["effect"])))
    return pairs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", required=True)
    ap.add_argument("--pred", required=True)
    ap.add_argument("--name", required=True)
    a = ap.parse_args()

    gold = {}
    for line in open(a.gold):
        e = json.loads(line)
        gold[e["text"]] = {(norm(x["drug"]), norm(x["effect"])) for x in e["adverse_events"]}

    preds = {}
    for line in open(a.pred):
        p = json.loads(line)
        preds[p["text"]] = p

    n = len(gold)
    valid = tp = fp = fn = exact = 0
    lat = []
    missing = [t for t in gold if t not in preds]
    assert not missing, f"{len(missing)} gold sentences missing from predictions"

    for text, g in gold.items():
        p = preds[text]
        if p.get("latency_s") is not None:
            lat.append(p["latency_s"])
        pairs = to_pairs(extract_json(p["raw_output"]))
        if pairs is None:
            fn += len(g)  # invalid output: all gold pairs missed, no predictions counted
            continue
        valid += 1
        tp += len(pairs & g)
        fp += len(pairs - g)
        fn += len(g - pairs)
        exact += pairs == g

    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    res = {
        "name": a.name, "n": n,
        "json_valid_rate": round(valid / n, 4),
        "pair_precision": round(prec, 4), "pair_recall": round(rec, 4), "pair_f1": round(f1, 4),
        "sentence_exact_match": round(exact / n, 4),
        "mean_latency_s": round(sum(lat) / len(lat), 4) if lat else None,
    }
    print(json.dumps(res, indent=2))
    with open(f"results/metrics_{a.name}.json", "w") as f:
        json.dump(res, f, indent=2)


if __name__ == "__main__":
    main()
