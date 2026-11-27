# Empirical Status — v6.1

The honest current state of Synthium's empirical claims. Updated as experiments
accumulate.

## TL;DR

Synthium is a **ruler-building-and-testing framework with no validated
predictive claims.** The judicial subject core is `PROPOSED`. Nothing in the
package is `VALIDATED`, because no model has yet beaten a pre-declared baseline
on held-out, rubric-independent outcomes.

This is the correct and expected state, not a shortfall. A `PROPOSED` status is
what a hypothesis is supposed to have before it is tested.

## What the v4.3 neural experiment established (carried forward)

The earlier neural encoder reported 72.7% test outcome accuracy. A leakage audit
found that number was driven entirely by three data leaks:

1. The cluster label was concatenated into the encoder's input text. Clusters
   near-perfectly determine outcome, so this handed the model the answer.
2. ~14 of 44 case summaries contained outcome-revealing phrases ("suppression
   denied", "affirmed", etc.).
3. The supervised contrastive loss used cluster identity as its positive-pair
   signal, leaking the same near-deterministic information into the embedding.

With the leaks removed, the same architecture scored **0.527 ± 0.176** across
five seeds — **below** the 0.727 majority-class baseline. The headline number was
leakage, not learning.

**How v6.1 carries this lesson forward:** the leaks are designed out of the
package rather than patched. `synthium.data.atlas` never folds the cluster into
features, redacts outcome words from text by default, and returns the cluster as
a separate field so it cannot be used as a supervised signal by accident.
`python -m synthium atlas` prints the cluster→outcome leakage table so the
hazard stays visible in code, not just in prose.

## The atlas

44 rubric-coded case studies. Binary GRANTED/DENIED subset: **37 cases, 30 DENIED
(81%)**. This is a set of probes chosen for doctrinal coverage, **not** a
statistical sample, and its outcome column was coded alongside the units by the
same rubric.

## Rubric imitation vs. predictive validity

`python -m synthium atlas-validate` runs the formula against the atlas's own
outcome column and reports a verdict through the real harness (frozen baseline,
held-out split). On a given split it can score very high.

**That number means almost nothing.** The target came from the same rubric as
the features, so it measures internal consistency, not predictive power. The
command prints this caveat every time. A `VALIDATED` status there would NOT
license any claim about real court outcomes.

The honest predictive-validity test has not been run because its preconditions
do not yet exist. `python -m synthium requirements` lists them.

## The formula's coefficients

The suppression-pressure formula contains **18 hand-chosen constants** (0.85,
0.45, 0.82, …). Not one was fit, derived, or measured. They are exposed as
first-class `Coefficient` objects with `grounded=False`, and
`suppression_pressure()` returns the list of coefficients it relied on alongside
every score it produces. See `python -m synthium coefficients`.

## What needs to happen next, in priority order

1. **Join rubric-coded units to court-derived outcomes.** Build a dataset where
   each case has both. This is the single blocker for any real validation.
2. **Independent outcome labels at scale.** Use `synthium.data.courtlistener` to
   read GRANTED/DENIED straight from the court record; hand-check a sample to
   measure the extractor's own accuracy first.
3. **Scale the atlas.** 37 binary cases cannot distinguish signal from noise.
   Target hundreds, with court-derived labels.
4. **Inter-rater reliability on the unit coding.** Multiple coders (including
   multiple LLMs as cross-coders) on the same cases, before the units' predictive
   value is judged. A feature you cannot reproduce across coders cannot be
   trusted as a measurement.
5. **Estimate coefficients from data.** Replace hand-chosen constants with fit
   values carrying confidence intervals; flip each `grounded` flag as it is
   earned.
6. **Cross-domain unit recurrence.** Only once two independently-developed
   subject cores produce statistically similar unit clusters from independent
   data is there weak evidence for cross-domain structure.

## Versioning note

- v4.3.1 — de-leaked baseline established.
- v5.0 — honesty harness; gated computation (diagnosed flaw: gated the wrong layer).
- v6.0 — predictive harness; gate moved from computation to claims.
- v6.1 — consolidation into a tested package; legacy lineages retired (`RETIRED.md`);
  ungrounded coefficients exposed; atlas loader leakage-aware by construction.
