# Data card

- **Source:** ade-benchmark-corpus/ade_corpus_v2, config Ade_corpus_v2_drug_ade_relation (Gurulingappa et al., 2012; MEDLINE case reports). Hub license tag: unknown.
- **Processing:** whitespace-normalized; rows grouped by unique sentence (6,821 rows -> 4,271 sentences); all drug/effect pairs per sentence merged into one gold record; exact duplicate pairs removed.
- **Splits (seed 42, by sentence, asserted leak-free):** train 3,416 / val 427 / test 428.
- **Multi-pair sentences:** train 1,079 / val 131 / test 140.
- **Test set policy:** the test split is used only for final evaluation. All tuning uses val.
- **Known issues:** incomplete labels (unlabeled drugs/effects), inconsistent span boundaries, some questionable drug-effect pairings. Not medical advice.
