# Demo video script (about 2.5 minutes, screen recording; keep keys and tokens off screen)

1. **Hook (0:00 to 0:15).** "Does fine-tuning a small model beat prompting a model 40 times its size? I measured it on one task and wrote down where it failed."
2. **Task (0:15 to 0:35).** Show one sentence and its JSON: "Pemphigus vulgaris precipitated by glibenclamide therapy." Say the metric (pair F1, strict parsing) was fixed before any run.
3. **Setup (0:35 to 1:00).** Show docs/eval_protocol.md and the `protocol-frozen` tag: test set untouched until the protocol was committed; leak-free split by sentence.
4. **Results (1:00 to 1:40).** Show the README results table. Say: fine-tuned 3B 0.733 vs 120B prompted 0.667 (CI [0.025, 0.108]) vs same 3B prompted 0.581. Then the honest part: latency is a tie, API cost is about $0.11 per 1,000 requests, license is non-commercial.
5. **Failures (1:40 to 2:10).** Show error_examples.md: boundary mismatches and noisy labels (lenient F1 0.899); overfitting (0.914 train vs 0.733 test); prompt sensitivity (0.571 with the wrong prompt); the 2e-4 learning rate that was worse.
6. **Live demo (2:10 to 2:30).** Terminal: start `mlx_lm.server`, run `python src/client_demo.py`, show the JSON coming back in about 0.6 s.
7. **Close.** "Fine-tune for volume, consistency and independence from an API; just prompt when you are low-volume or data-poor."
