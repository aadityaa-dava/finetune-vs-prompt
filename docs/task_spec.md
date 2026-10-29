# Task spec

**Task:** Extract drug / adverse-effect pairs from a medical sentence as JSON.
**Data:** ade-benchmark-corpus/ade_corpus_v2, config Ade_corpus_v2_drug_ade_relation
(6,821 rows -> 4,271 unique sentences). License tag on the Hub: unknown. Source: Gurulingappa et al., 2012.
This is a text-extraction exercise on public literature, not medical advice.

**Output schema:**
{"adverse_events": [{"drug": "<string>", "effect": "<string>"}]}

**Splits:** by unique sentence (never by row), 80/10/10, fixed seed, so no sentence appears in two splits.

**Metrics (fixed before running anything):**
1. JSON validity rate: output parses and matches the schema.
2. Pair-level micro F1 (PRIMARY): a predicted (drug, effect) pair counts as correct only if it
   matches a gold pair after lowercasing and whitespace normalization. Precision and recall reported too.
3. Sentence-level exact match: the set of predicted pairs equals the gold set.
Also reported for every model: mean latency per request, memory, and cost per 1,000 requests.

**Known limitation:** gold labels are incomplete and sometimes use odd spans, so a model can be
penalized for correct but unlabeled extractions. Analyzed in the error analysis.
