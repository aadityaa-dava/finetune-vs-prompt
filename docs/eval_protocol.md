# Final evaluation protocol (frozen before any test-set run)

**Test set:** data/processed/test.jsonl (428 sentences). Used for the first time after this commit.

**Models and settings (each scored exactly once on test):**
1. Qwen2.5-3B-Instruct-4bit, zero-shot, short prompt (local, M4)
2. Qwen2.5-3B-Instruct-4bit, 4-shot prompt (same 4 train examples as val runs)
3. openai/gpt-oss-120b via Groq free tier, 4-shot, temperature 0, reasoning_effort=low
4. **Primary result:** Qwen2.5-3B + LoRA, rank 8, lr 1e-4, final adapter (step 1,700, adapters/lora_r8), short zero-shot prompt
5. Secondary: the same adapter with the 4-shot prompt (it was trained on the short prompt, so this checks sensitivity to prompt format)

**Fixed choices (not revisited after seeing test results):**
- Final adapter = last step, chosen before the checkpoint comparison, not the best-looking checkpoint.
- Rank 8 over rank 16 (no detectable difference on val; smaller wins ties).
- Greedy decoding, max_tokens 256 for local models. Same strict JSON parser and metric as val.

**Reporting:** pair F1 (primary), precision, recall, JSON validity, sentence exact match, mean and p95 latency, memory,
and a paired bootstrap 95% interval (2,000 resamples) for each comparison with the LoRA model.

**Not included:** Gemini (free tier allows 20 requests/day per model, so a full run was infeasible; documented as a finding).

**Rules:** no re-runs to improve a number. A re-run is allowed only after a crash, and is logged in the README. All
runs are single-seed. Test-set error analysis is labeled as such; any prompt or model change prompted by it would be reported as post-hoc.
