"""Group rows by unique sentence, build gold JSON, make leak-free train/val/test splits."""
import json
import random
import re
from collections import OrderedDict
from datasets import load_dataset

SEED = 42
OUT_DIR = "data/processed"


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())


def main():
    ds = load_dataset("ade-benchmark-corpus/ade_corpus_v2",
                      "Ade_corpus_v2_drug_ade_relation", split="train")

    # 1. Group rows by normalized sentence; collect unique (drug, effect) pairs per sentence
    groups = OrderedDict()
    for r in ds:
        text = norm(r["text"])
        pair = (norm(r["drug"]), norm(r["effect"]))
        groups.setdefault(text, [])
        if pair not in groups[text]:
            groups[text].append(pair)

    examples = []
    for text, pairs in groups.items():
        examples.append({
            "text": text,
            "adverse_events": [{"drug": d, "effect": e} for d, e in pairs],
        })
    print("unique sentences:", len(examples))

    # 2. Shuffle with a fixed seed, split 80/10/10 BY SENTENCE
    random.Random(SEED).shuffle(examples)
    n = len(examples)
    n_train, n_val = int(0.8 * n), int(0.1 * n)
    splits = {
        "train": examples[:n_train],
        "val": examples[n_train:n_train + n_val],
        "test": examples[n_train + n_val:],
    }

    # 3. Leak check: no sentence in more than one split
    sets = {k: {e["text"] for e in v} for k, v in splits.items()}
    assert not (sets["train"] & sets["val"]), "train/val leak"
    assert not (sets["train"] & sets["test"]), "train/test leak"
    assert not (sets["val"] & sets["test"]), "val/test leak"

    # 4. Write JSONL
    for name, rows in splits.items():
        with open(f"{OUT_DIR}/{name}.jsonl", "w") as f:
            for e in rows:
                f.write(json.dumps(e) + "\n")
        multi = sum(len(e["adverse_events"]) > 1 for e in rows)
        print(f"{name}: {len(rows)} sentences, {multi} with 2+ pairs")


if __name__ == "__main__":
    main()
