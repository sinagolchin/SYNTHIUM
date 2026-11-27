# Synthium

**A structural framework for constructing measurement rulers for abstract concepts.**

Synthium is research infrastructure for proposing, building, testing, and
revising rulers that attempt to measure qualitative phenomena — privacy,
exception strength, suppression pressure, correlation quality, semantic
coherence, and similar.

Synthium is **not** a discovered theory of reality. It is scaffolding inside
which testable hypotheses can be expressed in a common mathematical language and
validated (or falsified) against external data.

## Core principle

```
Synthium proposes rulers.
A ruler earns the right to be called "structural" only by predicting outcomes
it was never fit to — against a baseline and margin frozen in advance.
Architectural elegance earns nothing.
```

## Architecture

### Synthium Core (universal layer)

- Confidence system with decay and weakest-link aggregation
- State representation over an n-dimensional manifold; optional Riemannian metric
- Dimensional discovery engine (PCA, ICA, Isomap, LLE) with bootstrap stability
- Subject-core registry for proposed domain instantiations
- Governance engine with hysteresis and trajectory-aware risk scoring

### The validation harness (v6.0 — current)

`synthium_v6_0_predictive.py`. The framework's claim layer.

- Arithmetic always runs; operations a scale type doesn't support are recorded
  as `Assumption`s in provenance rather than refused.
- Models are born `PROPOSED`. `assert_validated()` is the only refusal: it
  raises unless the model has beaten a pre-declared `Baseline` by a pre-declared
  margin on held-out cases.
- A `Baseline` is a frozen rule; its score is produced on the test set, not
  carried forward. Reality judges the model; the model never judges itself.

v5.0 (`synthium_v5_0_honesty.py`) is the prior step: a honesty harness that
gated computation. That was diagnosed as the wrong layer to gate — it made
proposing a model impossible. Its provenance, scale-type, and `audit()`
machinery are retained; v6.0 supersedes its blocking behavior.

### Data layer — independent outcome labels

`synthium_courtlistener.py`. Reads suppression dispositions from the court
record (CourtListener REST v4) and emits `LabeledCase` records tagged
`outcome_origin="court_record"`. This is the target a proposed ruler must learn
to predict — deliberately independent of the rubric being tested. Conservative
extractor: ambiguous dispositions resolve to UNKNOWN, never a guess. Its own
accuracy is unmeasured and must be checked against hand-coding.

### Subject cores (domain instantiations)

Each is a **proposed** set of units, operators, and formulas for one domain.

- **Judicial Module v0.2** — Fourth Amendment suppression doctrine (12-unit
  extended state). Rubric-imitation today; below baseline on outcome prediction
  after de-leaking. See `EMPIRICAL_STATUS.md`.

Descoped: the cyber/SRIA (LANL) module has been removed from the project.

## Scientific status

A **prototype research framework**, not a validated instrument. All units are
proposed dimensions; all formulas are falsifiable hypotheses with hand-chosen
coefficients. Nothing has yet cleared the v6.0 predictive bar. See
`EMPIRICAL_STATUS.md`.

## Quick start

```bash
# v6.0 harness demo — shows a VALIDATED and a FALSIFIED verdict:
python synthium_v6_0_predictive.py

# Verify the outcome labeler offline (no token needed):
python synthium_courtlistener.py --self-test

# Pull and label real cases (needs a free CourtListener token):
export COURTLISTENER_TOKEN="..."
python synthium_courtlistener.py --build --max 50 --out cases.jsonl
```

## Vocabulary

Prefer **propose / construct / hypothesize** over **discover**; **ruler /
instrument / framework** over **theory / law**. A model is **PROPOSED**,
**VALIDATED**, or **FALSIFIED** — never "proven". The "Newton-scale rigor"
framing is a long-term aspiration, kept visibly separate from current state.

## Important limitations

- Sample sizes are small. The rubric-coded judicial atlas is 44 cases.
- Coefficients in symbolic formulas are hand-chosen, not learned or derived.
- The dimensional discovery engine has not verified any unit space's
  intrinsic dimensionality.
- The CourtListener extractor's accuracy has not been measured against
  hand-coded ground truth.

## Citation

Treat Synthium as a research framework in active development, not a validated
estimator.
