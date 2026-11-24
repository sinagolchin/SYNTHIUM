# Empirical Status — v4.3.1

This document records the honest current state of Synthium's empirical claims. It is updated as experiments accumulate.

## TL;DR

Synthium is a **ruler-building framework with no validated predictive claims yet.** The neural judicial encoder, as previously reported, achieved 72.7% test outcome accuracy. After removing three data leaks, the same architecture and training procedure achieves **52.7% ± 17.6%** test accuracy across 5 seeds — worse than the 72.7% always-predict-majority-class baseline.

This is a diagnostic finding, not a death blow. It tells us exactly where empirical work needs to start.

## What was tested (v4.3)

- A small PyTorch text encoder (`JudicialNeuralEncoder`) trained on the 44-case `judicial_suppression_atlas_v0_2.csv`.
- Multi-objective loss: unit MSE + operator BCE + outcome cross-entropy + supervised contrastive metric loss + heteroscedastic uncertainty + formula-consistency penalty.
- Reported test outcome accuracy: 0.727 on an 11-case held-out set.

## The three leaks identified in v4.3.1

### Leak 1: Cluster name concatenated into input text

In `synthium/domains/judicial/dataset.py` (line 76):

```python
text = " ".join([row.get("case_name", ""), row.get("cluster", ""), row.get("text", "")]).strip()
```

The cluster name (e.g., `good_faith`, `home_privacy`, `exception_dominance`) was being fed directly into the encoder as part of the input. Because clusters near-perfectly predict outcomes in the atlas, this hands the model the answer.

### Leak 2: Outcome words in case text

About 14 of 44 case summaries contain phrases that directly reveal the outcome: "suppression denied", "suppression granted", "affirmed", "reversed", "violated", etc. Any text encoder learns these trivially.

### Leak 3: Cluster labels in the contrastive loss

In `synthium/neural/losses.py`, `supervised_contrastive_loss` was being called with cluster identity as the positive-pair signal. This trains the manifold-embedding head to recover the cluster — which is itself near-deterministic for outcome.

## Cluster→outcome leakage in the atlas

The 44-case atlas has **31 distinct cluster labels.** Most clusters contain a single case. Several large clusters are perfectly outcome-deterministic:

| Cluster | Cases | Outcome |
|---|---|---|
| `good_faith` | 8 | DENIED (8/8) |
| `exception_dominance` | 4 | DENIED (4/4) |
| `home_privacy` | 2 | GRANTED (2/2) |
| `curtilage_boundary` | 2 | DENIED (2/2) |
| `warrant_structure` | 2 | mixed |

Knowing the cluster essentially tells you the outcome.

## The de-leaked experiment

The script `synthium/domains/judicial/train_deleaked.py` reproduces v4.3's pipeline with three changes:
1. Drops the cluster name from the input text.
2. Redacts outcome-revealing phrases via regex.
3. Sets the supervised contrastive loss weight to 0 (`LossWeights.metric = 0.0`).

Plus methodological improvements:
- Outcome-stratified train/test split.
- Vocabulary built from training set only (no test-text leakage).
- Five random seeds with mean ± standard deviation reporting.
- Wilson 95% confidence intervals on per-seed accuracy.
- Explicit majority-class baseline computed from the training set.

## Results (5 seeds, 180 epochs each)

| Setup | Mean test accuracy | Std | Δ vs baseline |
|---|---|---|---|
| **Original (with all 3 leaks), seed 42** | 0.727 | — | +0.000 |
| **De-leaked, 5 seeds** | **0.527** | **0.176** | **−0.200 ± 0.176** |
| Always-predict-majority-class baseline | 0.727 | — | 0.000 |

Per-seed details:

| Seed | Test acc | Baseline | Δ | Unit MAE |
|---|---|---|---|---|
| 42 | 0.455 | 0.727 | −0.273 | 0.142 |
| 43 | 0.273 | 0.727 | −0.455 | 0.160 |
| 44 | 0.727 | 0.727 | +0.000 | 0.115 |
| 45 | 0.727 | 0.727 | +0.000 | 0.160 |
| 46 | 0.455 | 0.727 | −0.273 | 0.133 |

Unit MAE remains roughly stable across leaked and de-leaked runs (~0.13–0.14), meaning the model still imitates the rubric's unit values about as well — but that imitation does not translate into outcome prediction once the leaks are gone.

## What this means

The 72.7% headline number was driven entirely by leakage, not by the model learning a meaningful mapping from text features to suppression outcomes. With the leaks removed, the framework has no demonstrated outcome-predictive validity at the current data scale.

The architectural integrity of Synthium — confidence propagation, manifold infrastructure, subject-core registry, multi-objective loss design — is not affected by this finding. What is affected is any claim that the **judicial unit space**, as currently defined and labeled, **predicts real-world outcomes**.

This is the gap between **rubric imitation** (which the model still does, with unit MAE ≈ 0.14) and **predictive validity** (which has not been demonstrated).

## What needs to happen next, in priority order

1. **Run the dimensional discovery engine on the judicial unit vectors.** It has been sitting unused. Determine empirically whether the 12-unit framing is overcomplete, undercomplete, or appropriate. If 12 units collapse to 3 principal components, the framing needs revision.

2. **Independent outcome labels.** The atlas labels (units, operators, cluster, outcome) all originate from human coding informed by the same rubric. Scrape suppression outcomes directly from court decisions via CourtListener and use those as the target, with no rubric-derived intermediates.

3. **Scale the atlas.** 44 cases is too few to distinguish signal from noise at any meaningful level. Target: 500–1,000 cases with outcomes from the actual court record, not rubric inference.

4. **Cyber/SRIA validation against LANL.** This is the strongest candidate for the first true predictive-validity claim, because LANL provides outcomes (true compromises) that exist entirely independent of any Synthium rubric. Define the prediction target precisely, run the correlation × quality model, compare against well-known baselines (raw correlation, frequency-only, simple heuristic).

5. **Cross-domain unit recurrence test.** The `universal_candidate` flag is the right idea but has no empirical force yet. When (and only when) two independently-developed subject cores produce statistically similar unit clusters from independent data, that's the first weak evidence for cross-domain structure.

## Versioning note

- v4.3.0: initial neural training pipeline (with leaks, as published)
- v4.3.1: de-leaked baseline established; this document added
- v4.4.x: subject-core architecture refactor (in progress, separate branch)

Future revisions of this document should add entries for each new empirical experiment, with explicit train/test/baseline numbers and the leakage audit that was performed before the run.
