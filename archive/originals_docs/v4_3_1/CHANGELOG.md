# Changelog

## v4.3.1 — De-leaked baseline

A leakage audit was performed on the v4.3 neural training pipeline. Three distinct data leaks were identified and a corrected training script was added. The honest test-set outcome accuracy after de-leaking is **0.527 ± 0.176** across five seeds, **below** the 0.727 majority-class baseline. See `EMPIRICAL_STATUS.md` for the full report.

Added:
- `synthium/domains/judicial/train_deleaked.py` — corrected training pipeline with outcome-stratified split, vocab built from train-only, multi-seed runs, Wilson 95% CIs, and explicit majority-class baseline comparison.
- `EMPIRICAL_STATUS.md` — honest current empirical state of the project, updated as experiments accumulate.
- `PROJECT_INSTRUCTIONS.md` — calibration note for Claude Project sessions.

Reframed:
- `README.md` — Synthium is now described as a **ruler-building structure for abstract concepts**, not a discovered theory. Existing technical content preserved; framing language updated throughout. The "Newton-scale rigor" framing is retained as a long-term research aspiration but kept visibly separate from current state claims.

Leaks fixed in the new training script (original pipeline preserved for reproduction):
1. Cluster name was being concatenated into the encoder's input text (`dataset.py` line 76).
2. Case summary text contained outcome-revealing phrases ("suppression denied", "affirmed", etc.) — now redacted by regex.
3. `supervised_contrastive_loss` was being called with cluster labels as the positive-pair signal, leaking near-deterministic outcome information into the embedding head — now zeroed via `LossWeights.metric = 0.0`.

## v4.3.0 — Neural upgrade

Added:
- `synthium.neural` package.
- Trainable `JudicialNeuralEncoder` (PyTorch).
- Multi-head outputs: units, operators, outcomes, manifold embeddings, uncertainty.
- Multi-objective loss with formula-consistency penalty.
- Judicial domain spec v0.2 with canonical 6-unit and extended 12-unit state vectors.
- 44-case judicial suppression atlas (`data/judicial_suppression_atlas_v0_2.csv`).
- Distance matrix, cluster centroids, and nearest-neighbor outputs.
- Lightweight CourtListener API client.
- CLI training script.

Known limitations at release (now better documented):
- Atlas labels are rubric-derived.
- Sample size is small (44 cases).
- Outcome prediction had not yet been audited for data leakage when first published.
