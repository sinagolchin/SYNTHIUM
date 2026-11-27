# Changelog

## v6.1 — Consolidation

A clean package rebuilt from the project's serious core. The accumulated
multi-version sprawl was audited; the modern lineage was preserved and the rest
retired (see `RETIRED.md`).

Added:
- Layered package: `synthium.core` (values, baseline, validation),
  `synthium.data` (atlas, courtlistener), `synthium.domains.judicial`
  (spec, formula, model).
- `python -m synthium` CLI with eight commands.
- A 17-test suite, pure standard library.
- `synthium.domains.judicial.formula.Coefficient`: the 18 hand-chosen formula
  constants are now first-class objects with `grounded=False`. `suppression_pressure()`
  returns the list of coefficients it relied on alongside every score.
- `synthium.data.atlas`: leakage-aware loader. The three v4.3.1 leaks are
  designed out — cluster never enters features, outcome words redacted by
  default, cluster returned separately. `cluster_outcome_leakage()` surfaces the
  hazard table in code.
- `RETIRED.md`: what was dropped and why.

Changed:
- `Value.all_assumptions()` is now transitive: it gathers assumptions from the
  whole computation graph, so a derived value's audit trail is complete rather
  than truncated to its last operation (vs. v6.0).
- `validate_against_atlas()` runs the rubric-imitation experiment through the
  real harness but returns and prints an explicit caveat that it does not show
  predictive validity.
- Governance docs (`README`, `EMPIRICAL_STATUS`, `PROJECT_INSTRUCTIONS`) updated
  from the frozen v4.3.1 state to reflect v6.1; SRIA/LANL references removed.

Retired (see `RETIRED.md`):
- The "Omega" keyword-quantifier (`transducer.py`, `science.py`, `recorder.py`,
  `vectors`, `reality_field.py`, `main.py`) — scored text on keyword vibes and
  printed pseudo-physics "formulas". Exactly the ungrounded-numbers failure mode.
- The 2,045-line v4.3.1 monolith — split into focused modules; the parts worth
  keeping were carried into `core`/`data`/`domains`.
- The SRIA/LANL cyber workstream — descoped.
- The v3.x "discovery" PDF narrative — superseded by the propose-then-validate
  framing.

## v6.0 — Predictive harness

The gate moved from computation to claims. Arithmetic always runs; refusal lives
only in `assert_validated()`. A model is `PROPOSED` until it beats a pre-declared
baseline by a pre-declared margin on held-out cases.

## v5.0 — Honesty harness

Enforced scale-type discipline by gating computation. Diagnosed flaw: gating
computation means you can never even propose a model. v6.0 corrected the layer.

## v4.3.1 — De-leaked baseline

Leakage audit of the v4.3 neural pipeline. Three leaks found; de-leaked accuracy
was 0.527 ± 0.176, below the 0.727 majority-class baseline.

## v4.3.0 — Neural upgrade

Trainable judicial encoder, multi-objective loss, judicial spec v0.2, 44-case
atlas, CourtListener client. Outcome prediction had not yet been audited for
leakage when first published.
