"""Small general-capability sanity set (40 items), base vs LoRA adapter. Not a benchmark: it only detects large regressions."""
import json
import re
import sys
from mlx_lm import load, generate

QA = [
 ("What is 17 + 26? Answer with just the number.", ["43"]), ("What is 9 * 8? Answer with just the number.", ["72"]),
 ("What is 144 / 12? Answer with just the number.", ["12"]), ("What is 100 - 37? Answer with just the number.", ["63"]),
 ("What is 15% of 200? Answer with just the number.", ["30"]), ("What is the square root of 81? Answer with just the number.", ["9"]),
 ("What is the capital of France? One word.", ["paris"]), ("What is the capital of Japan? One word.", ["tokyo"]),
 ("What is the capital of Canada? One word.", ["ottawa"]), ("What is the capital of Australia? One word.", ["canberra"]),
 ("What is the capital of Egypt? One word.", ["cairo"]), ("What is the capital of Brazil? One word.", ["brasilia", "brasília"]),
 ("What is the chemical symbol for gold? Answer with just the symbol.", ["au"]), ("What is the chemical symbol for sodium? Answer with just the symbol.", ["na"]),
 ("What is the chemical formula for water? Answer with just the formula.", ["h2o"]), ("What gas do plants absorb from the air for photosynthesis? One or two words.", ["carbon dioxide", "co2"]),
 ("Which planet is closest to the Sun? One word.", ["mercury"]), ("Which planet is known as the Red Planet? One word.", ["mars"]),
 ("How many days are in a leap year? Answer with just the number.", ["366"]), ("How many sides does a hexagon have? Answer with just the number.", ["6"]),
 ("Who wrote the play Romeo and Juliet? Answer with the full name.", ["shakespeare"]), ("What language is primarily spoken in Brazil? One word.", ["portuguese"]),
 ("What is the largest ocean on Earth? One or two words.", ["pacific"]), ("What is the boiling point of water in Celsius at sea level? Just the number.", ["100"]),
 ("Is a whale a fish or a mammal? One word.", ["mammal"]), ("Is the Earth round or flat? One word.", ["round"]),
 ("Answer yes or no: is 7 a prime number?", ["yes"]), ("Answer yes or no: is 9 a prime number?", ["no"]),
 ("What is the opposite of hot? One word.", ["cold"]), ("What is the past tense of the verb 'go'? One word.", ["went"]),
 ("What is the plural of 'mouse' (the animal)? One word.", ["mice"]), ("Spell the word 'cat' backwards. Just the word.", ["tac"]),
 ("What comes next in the sequence 2, 4, 6, 8? Just the number.", ["10"]), ("What month comes right after March? One word.", ["april"]),
 ("What day comes right after Tuesday? One word.", ["wednesday"]), ("How many minutes are in one hour? Just the number.", ["60"]),
 ("How many continents are there? Just the number.", ["7", "seven"]), ("What color do you get by mixing blue and yellow? One word.", ["green"]),
 ("Reply with exactly the word: OK", ["ok"]), ("Write the number 5 as a word, in lowercase. One word.", ["five"]),
]

def score(model_path, adapter):
    model, tok = load(model_path, adapter_path=adapter)
    ok, outs = 0, []
    for q, ans in QA:
        prompt = tok.apply_chat_template([{"role": "user", "content": q}], add_generation_prompt=True, tokenize=False)
        out = generate(model, tok, prompt=prompt, max_tokens=40, verbose=False).strip()
        hit = any(a in re.sub(r"[^a-z0-9ÿ\u00e0-\u00ff ]", "", out.lower()) for a in ans)
        ok += hit
        outs.append((q, out, hit))
    return ok, outs

M = "mlx-community/Qwen2.5-3B-Instruct-4bit"
res = {}
for label, ad in [("base", None), ("lora_r8", "adapters/lora_r8")]:
    ok, outs = score(M, ad)
    res[label] = (ok, outs)
    print(f"{label}: {ok}/{len(QA)}")
print("--- items where results differ (base -> lora):")
for (q, ob, hb), (_, ol, hl) in zip(res["base"][1], res["lora_r8"][1]):
    if hb != hl:
        print(f"Q: {q}\n   base: {ob[:80]!r} ({'ok' if hb else 'wrong'})\n   lora: {ol[:80]!r} ({'ok' if hl else 'wrong'})")
json.dump({k: {"correct": v[0], "n": len(QA), "outputs": v[1]} for k, v in res.items()}, open("results/forgetting_check.json", "w"), indent=1)
