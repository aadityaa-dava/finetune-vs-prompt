"""Test-set error analysis. POST-HOC: findings are descriptive; no model/prompt changes are made from them."""
import json
import sys
from collections import Counter, defaultdict
sys.path.insert(0, "src")
from evaluate import extract_json, to_pairs, norm

gold = {}
for l in open("data/processed/test.jsonl"):
    e = json.loads(l)
    gold[e["text"]] = {(norm(x["drug"]), norm(x["effect"])) for x in e["adverse_events"]}

MODELS = {"LoRA r8": "lora_r8_zeroshot", "gpt-oss-120b": "gptoss120b_fewshot", "3B 4-shot": "base_fewshot"}
LABELS = ["invalid JSON (sentences)", "FP: wording not in sentence", "FP: boundary mismatch", "FP: wrong pairing",
          "FP: extra/unlabeled pair", "FN: boundary mismatch", "FN: missed entirely"]


def ov(a, b):
    return bool(a) and bool(b) and (a == b or a in b or b in a)


def lm(p, g):  # lenient match: drug and effect each equal or one contains the other
    return ov(p[0], g[0]) and ov(p[1], g[1])


def f1(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    return 2 * p * r / (p + r) if p + r else 0.0


def analyze(name):
    preds = {}
    for l in open(f"results/preds_{name}_test.jsonl"):
        p = json.loads(l)
        preds[p["text"]] = p
    cats, ex, exact, parsed = Counter(), defaultdict(list), {}, {}
    seg = {"1 gold pair": [0, 0, 0], "2+ gold pairs": [0, 0, 0]}
    n_pred = n_gold = lp = lr = 0
    for text, G in gold.items():
        P = to_pairs(extract_json(preds[text]["raw_output"]))
        parsed[text] = P
        key = "1 gold pair" if len(G) == 1 else "2+ gold pairs"
        n_gold += len(G)
        if P is None:
            cats["invalid JSON (sentences)"] += 1
            seg[key][2] += len(G)
            exact[text] = False
            ex["invalid JSON (sentences)"].append((text, sorted(G), "RAW END: " + preds[text]["raw_output"][-80:]))
            continue
        tn = norm(text)
        n_pred += len(P)
        seg[key][0] += len(P & G); seg[key][1] += len(P - G); seg[key][2] += len(G - P)
        exact[text] = (P == G)
        lp += sum(any(lm(p, g) for g in G) for p in P)
        lr += sum(any(lm(p, g) for p in P) for g in G)
        gd, ge = {g[0] for g in G}, {g[1] for g in G}
        for p in P - G:
            if p[0] not in tn or p[1] not in tn:
                c = "FP: wording not in sentence"
            elif any(lm(p, g) for g in G):
                c = "FP: boundary mismatch"
            elif p[0] in gd and p[1] in ge:
                c = "FP: wrong pairing"
            else:
                c = "FP: extra/unlabeled pair"
            cats[c] += 1
            ex[c].append((text, sorted(G), sorted(P)))
        for g in G - P:
            c = "FN: boundary mismatch" if any(lm(p, g) for p in P) else "FN: missed entirely"
            cats[c] += 1
            ex[c].append((text, sorted(G), sorted(P)))
    lenp, lenr = lp / n_pred if n_pred else 0, lr / n_gold
    return dict(cats=cats, ex=ex, exact=exact, parsed=parsed, seg=seg,
                lenient=(lenp, lenr, 2 * lenp * lenr / (lenp + lenr) if lenp + lenr else 0))


R = {m: analyze(n) for m, n in MODELS.items()}
print(f"{'':32}" + "".join(f"{m:>14}" for m in MODELS))
for lab in LABELS:
    print(f"{lab:32}" + "".join(f"{R[m]['cats'][lab]:>14}" for m in MODELS))
print("\nlenient F1 (overlap match):    " + "".join(f"{R[m]['lenient'][2]:>14.3f}" for m in MODELS))
for s in ["1 gold pair", "2+ gold pairs"]:
    print(f"strict F1, {s:20}" + "".join(f"{f1(*R[m]['seg'][s]):>14.3f}" for m in MODELS))
print("sentences in segment:           ", {s: sum((len(G) == 1) == (s == '1 gold pair') for G in gold.values()) for s in R['LoRA r8']['seg']})

L, G120, B = R["LoRA r8"], R["gpt-oss-120b"], R["3B 4-shot"]
def h2h(a, b, an, bn):
    both = sum(a["exact"][t] and b["exact"][t] for t in gold)
    ao = sum(a["exact"][t] and not b["exact"][t] for t in gold)
    bo = sum(b["exact"][t] and not a["exact"][t] for t in gold)
    nei = len(gold) - both - ao - bo
    print(f"exact-match sentences: both {both} | only {an} {ao} | only {bn} {bo} | neither {nei}")
h2h(L, G120, "LoRA", "120B"); h2h(L, B, "LoRA", "3B 4-shot")

with open("results/error_examples.md", "w") as f:
    f.write("# Test-set error examples (post-hoc)\n\n## LoRA r8 by category\n")
    for lab in LABELS:
        f.write(f"\n### {lab} ({L['cats'][lab]})\n")
        for t, g, p in L["ex"][lab.replace(' (sentences)', ' (sentences)')][:6] if lab in L["ex"] else []:
            f.write(f"- TEXT: {t}\n  - GOLD: {g}\n  - PRED: {p}\n")
    for title, a, b, an, bn in [("LoRA right, 120B wrong", L, G120, "LoRA", "120B"), ("120B right, LoRA wrong", G120, L, "120B", "LoRA")]:
        f.write(f"\n## {title}\n")
        k = 0
        for t in gold:
            if a["exact"][t] and not b["exact"][t] and k < 8:
                f.write(f"- TEXT: {t}\n  - GOLD: {sorted(gold[t])}\n  - {bn}: {sorted(b['parsed'][t]) if b['parsed'][t] is not None else 'INVALID'}\n")
                k += 1
print("\nexamples written to results/error_examples.md")
print("--- one LoRA example per category:")
for lab in LABELS:
    if L["ex"].get(lab):
        t, g, p = L["ex"][lab][0]
        print(f"[{lab}] {t[:110]}\n   GOLD {g}\n   PRED {p}")
