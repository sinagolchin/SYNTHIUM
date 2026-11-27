# Changelog

## v6.0 — Predictive harness

Reframes where the framework refuses. v5.0 gated *computation*; v6.0 gates
*claims*. Arithmetic now always runs and records any unsupported-scale
operation as an `Assumption` attached to the result's provenance, instead of
raising. Models are born `PROPOSED`. The only path to `VALIDATED` is passing a
held-out, out-of-sample prediction test against a baseline and margin frozen
before the test outcomes were seen. `assert_validated()` is the single refusal
point.

Added:
- `synthium_v6_0_predictive.py` — `Value` (computes unconditionally, logs
  assumptions), `Baseline` (a frozen rule whose score is produced on the test
  set, not carried forward), `PredictiveModel` with `PROPOSED/VALIDATED/FALSIFIED`
  status, `ValidationProtocol`, `validate()`, and `assert_validated()`. Demo
  shows both a VALIDATED and a FALSIFIED verdict on synthetic data.
- `load_labeled_cases()` adapter that consumes the CourtListener label stream.

## v5.x — CourtListener independent-label pipeline

Added the upstream piece `EMPIRICAL_STATUS.md` had flagged as priority #2: an
outcome target that exists in the court record, independent of any Synthium
rubric.

Added:
- `synthium_courtlistener.py` — CourtListener REST v4 client (token now
  required; cursor pagination), a transparent rule-based outcome extractor
  (suppression granted/denied/mixed), and `LabeledCase` records that carry the
  exact evidence phrase plus `outcome_origin="court_record"`. Conservative by
  design: ambiguous or conflicting dispositions resolve to UNKNOWN rather than a
  guess. Ships with an offline self-test (8/8 fixtures, including appellate
  reversal-flipping).

Note: the extractor's own accuracy is itself unmeasured and must be checked
against hand-coded cases before its labels are trusted as ground truth.

## v5.0 — Honesty harness (diagnosed, then corrected by v6.0)

Added a scaffolding that refused to operate without explicit grounding:
scale-typed values, provenance on every value, units that cannot be registered
without anchors/zero-point/failure-conditions, axioms as first-class objects,
and an `audit()` that surfaces every empty slot.

Diagnosed flaw: it gated *computation* rather than *claims*. Blocking arithmetic
on ungrounded inputs makes it impossible to even propose a model, which makes
discovery impossible. v6.0 corrects this. v5.0 is retained as the source of the
provenance/scale-type machinery and the audit discipline.

Added:
- `synthium_v5_0_honesty.py` — `ScaledValue`, `Unit`, `Axiom`, `AnchorCase`,
  `ReliabilityRecord`, `FalsificationCondition`, `SubjectCore`, `run_audit()`.

Descoped:
- Cyber/SRIA (LANL) workstream removed from the project. This had been the
  named external-validation candidate; its removal is why CourtListener
  outcome labels became the keystone validation path.

## v4.3.1 — De-leaked baseline

A leakage audit on the v4.3 neural pipeline found three data leaks (cluster
name in input text, outcome words in case summaries, cluster labels in the
contrastive loss). Honest de-leaked test accuracy is **0.527 ± 0.176** across
five seeds, **below** the 0.727 majority-class baseline. See `EMPIRICAL_STATUS.md`.

Added:
- `synthium/domains/judicial/train_deleaked.py` — corrected training pipeline.
- `EMPIRICAL_STATUS.md`, `PROJECT_INSTRUCTIONS.md`.

## v4.3.0 — Neural upgrade

Added the `synthium.neural` package, the trainable `JudicialNeuralEncoder`,
multi-objective loss, judicial spec v0.2, the 44-case atlas, and a lightweight
CourtListener client. Known limitations at release: rubric-derived labels, small
sample, and (then) un-audited leakage.
