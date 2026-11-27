# Empirical Status

This document records the honest current state of Synthium's empirical claims.
It is updated as experiments accumulate.

## TL;DR

Synthium is a **ruler-building framework with no validated predictive claims
yet.** The single most important change since v4.3.1 is structural, not a new
result: the validation path now exists end to end. The v6.0 harness can take a
`PROPOSED` model to `VALIDATED` only by beating a pre-declared baseline on
held-out cases, and the CourtListener pipeline now supplies outcome labels read
from the court record rather than from the rubric under test. Nothing has been
run through that full path yet. That run is the next milestone.

## The de-leaking result (still stands)

After removing three data leaks from the v4.3 neural pipeline, the same
architecture achieves **52.7% ± 17.6%** test outcome accuracy across 5 seeds —
**below** the 72.7% always-predict-majority-class baseline. The headline 0.727
was leakage, not learning. Unit MAE stays ~0.13–0.14 across leaked and de-leaked
runs: the model still *imitates the rubric* about as well, but that imitation
does not translate into outcome prediction once the leaks are gone. This is the
gap between **rubric imitation** and **predictive validity**.

| Setup | Mean test accuracy | Std | Δ vs baseline |
|---|---|---|---|
| Original (3 leaks), seed 42 | 0.727 | — | +0.000 |
| De-leaked, 5 seeds | **0.527** | **0.176** | **−0.200 ± 0.176** |
| Majority-class baseline | 0.727 | — | 0.000 |

## What changed architecturally since v4.3.1

**v5.0 (honesty harness) — diagnosed and corrected.** Enforced scale types and
provenance at runtime, but gated *computation*: it refused arithmetic on
ungrounded values. That made proposing a model impossible, so it could never
reach the only thing that matters — a prediction test. Its provenance and audit
machinery are retained; its blocking behavior is not.

**v6.0 (predictive harness) — current.** Arithmetic always runs and logs
assumptions to provenance. Models are born `PROPOSED`. The lone refusal,
`assert_validated()`, raises unless the model has beaten a baseline and margin
that were frozen before the test outcomes were seen. Reality judges the model;
the model never judges itself.

**CourtListener independent labels — built.** `synthium_courtlistener.py` reads
suppression dispositions from the court record (cluster `disposition` field,
opinion text fallback) and emits `LabeledCase` records tagged
`outcome_origin="court_record"`. This is the keystone that earlier revisions of
this document listed as priority #2.

**Cyber/SRIA (LANL) — descoped.** Previously named here as the strongest
external-validation candidate. It has been removed from the project. CourtListener
outcome labels are now the validation path.

## What needs to happen next, in priority order

1. **Measure the extractor.** The CourtListener labeler is a first-pass read of
   the court record and its accuracy is unknown. Hand-code a sample of cases for
   suppression outcome, compare against the extractor, and report agreement.
   Until this is done, its labels are not yet ground truth.

2. **Run the full v6.0 path once.** Build the smallest honest predictor of
   court-derived outcome, freeze a majority-class baseline and a margin, split
   held-out, and run `validate()`. Report VALIDATED or FALSIFIED with numbers.
   A FALSIFIED verdict here is a real result, not a failure.

3. **Run the dimensional discovery engine on the judicial unit vectors.** Still
   unused. Determine empirically whether the 12-unit framing is overcomplete.

4. **Scale the labeled set.** 44 rubric-coded cases are too few. Target several
   hundred court-labeled cases via the CourtListener pipeline, then re-run the
   harness.

5. **Cross-domain unit recurrence.** Only meaningful once two independently
   developed subject cores each clear their own predictive test. No empirical
   force before then.

## Versioning note

- v4.3.0: neural pipeline (with leaks, as published)
- v4.3.1: de-leaked baseline established
- v5.0: honesty harness (computation-gated; diagnosed as misplaced)
- v5.x: CourtListener independent-label pipeline added
- v6.0: predictive harness (claim-gated); current architecture

Future revisions should add an entry per new experiment, with explicit
train/test/baseline numbers and the leakage audit performed before the run.
