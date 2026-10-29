"""Prompt used identically for every model (base, large API, fine-tuned)."""

SYSTEM = (
    "You extract drug and adverse-effect pairs from a medical sentence. "
    "Respond with ONLY a JSON object of the form "
    '{"adverse_events": [{"drug": "<string>", "effect": "<string>"}]} '
    "Use exact wording from the sentence. If there are no pairs, return {\"adverse_events\": []}. "
    "Output no other text."
)


def build_messages(text):
    return [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": text},
    ]


FEWSHOT_IDS = [0, 1, 2, 3]  # indices into train.jsonl; fixed so every model sees the same shots


def build_messages_fewshot(text, train_path="data/processed/train.jsonl"):
    import json
    train = [json.loads(l) for l in open(train_path)]
    msgs = [{"role": "system", "content": SYSTEM}]
    for i in FEWSHOT_IDS:
        e = train[i]
        msgs.append({"role": "user", "content": e["text"]})
        msgs.append({"role": "assistant", "content": json.dumps({"adverse_events": e["adverse_events"]})})
    msgs.append({"role": "user", "content": text})
    return msgs
