---
license: other
license_name: qwen-research
license_link: LICENSE
base_model: Qwen/Qwen2.5-3B-Instruct
base_model_relation: adapter
library_name: mlx
pipeline_tag: text-generation
language: en
datasets:
- ade-benchmark-corpus/ade_corpus_v2
tags:
- lora
- mlx
- information-extraction
- json
- adverse-drug-events
---

# Qwen2.5-3B + LoRA (r8) for drug / adverse-effect extraction to JSON

Built with Qwen. This is a LoRA adapter in **MLX format** (not PEFT) for `Qwen2.5-3B-Instruct`. It was trained on the 4-bit conversion `mlx-community/Qwen2.5-3B-Instruct-4bit`, so load it on that model. It contains no Qwen base weights.

It is a portfolio / research project that compares fine-tuning against prompting. Full code, data splits, logs and error analysis: https://github.com/aadityaa-dava/finetune-vs-prompt

**Not for clinical or medical use.** It is a text-extraction exercise on public literature.

## Task
Given one sentence from a medical case report, return JSON with every (drug, adverse effect) pair:
`{"adverse_events": [{"drug": "<string>", "effect": "<string>"}]}`

## Data
`ade-benchmark-corpus/ade_corpus_v2`, config `Ade_corpus_v2_drug_ade_relation` (Gurulingappa et al., 2012, *Journal of Biomedical Informatics*). The dataset card declares **no license**, so check its terms before reuse. 6,821 rows were grouped into 4,271 unique sentences and split by sentence (seed 42): 3,416 train / 427 validation / 428 test, with no sentence in two splits. Gold labels are incomplete and use inconsistent span boundaries.

## Training
LoRA via `mlx_lm.lora` on a 4-bit base: rank 8, scale 20, dropout 0.05, last 16 layers, batch 4, 1,700 steps (about 2 epochs), constant learning rate 1e-4 (no decay), loss on answer tokens only, seed 42. Trained locally on an Apple M4 (16 GB), about 91 minutes. Rank 16 was not detectably better; learning rate 2e-4 was worse at equal steps (validation F1).

## Results (test set, n=428, scored once under a protocol frozen beforehand)
| Model | JSON valid | Pair F1 | Precision / Recall | Exact match |
|---|---|---|---|---|
| Qwen2.5-3B, zero-shot | 26.9% | 0.154 | 0.483 / 0.092 | 7.9% |
| Qwen2.5-3B, 4-shot | 91.1% | 0.581 | 0.662 / 0.518 | 42.5% |
| gpt-oss-120b, 4-shot (API) | 100% | 0.667 | 0.739 / 0.607 | 58.4% |
| **This adapter, short prompt** | 99.8% | **0.733** | 0.747 / 0.720 | 66.8% |

Strict match after lowercasing and whitespace normalization. Paired bootstrap, 95% CI: adapter vs gpt-oss-120b +0.066 [+0.025, +0.108]; vs the same model with 4-shot prompting +0.152 [+0.107, +0.198]. Single training seed.

## Limitations
- **Memorization:** F1 is 0.914 on training sentences vs 0.733 on test.
- **Prompt-sensitive:** it expects the exact system prompt below. With a 4-shot prompt instead, test F1 fell to 0.571.
- **Span boundaries** drive most errors for every model; a lenient overlap metric gives 0.899.
- **General ability:** on a 40-question sanity set it scored 35/40, the same as the base, but produced degenerate outputs (repetition, image links) on 4 short unrelated prompts that the base answered correctly.
- Repetition loops can truncate JSON on a few inputs.
- Single seed, one dataset, one split; no claim beyond this task.
- **License:** Qwen Research License, **non-commercial only**; see `LICENSE` and `NOTICE`.

## Usage (mlx-lm)
```python
from huggingface_hub import snapshot_download
from mlx_lm import load, generate

adapter = snapshot_download("aadityaa1/qwen25-3b-ade-lora-r8")
model, tok = load("mlx-community/Qwen2.5-3B-Instruct-4bit", adapter_path=adapter)
SYSTEM = 'You extract drug and adverse-effect pairs from a medical sentence. Respond with ONLY a JSON object of the form {"adverse_events": [{"drug": "<string>", "effect": "<string>"}]} Use exact wording from the sentence. If there are no pairs, return {"adverse_events": []}. Output no other text.'
msgs = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": "Pemphigus vulgaris precipitated by glibenclamide therapy."}]
prompt = tok.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False)
print(generate(model, tok, prompt=prompt, max_tokens=256))
```

## Citation
Gurulingappa, H., Rajput, A. M., Roberts, A., Fluck, J., Hofmann-Apitius, M., Toldo, L. (2012). Development of a benchmark corpus to support the automatic extraction of drug-related adverse effects from medical case reports. *Journal of Biomedical Informatics*.
