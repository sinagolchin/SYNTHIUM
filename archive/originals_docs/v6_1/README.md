# Synthium

**A framework for constructing and *testing* measurement rulers for abstract concepts.**

Synthium is research infrastructure for proposing, building, and validating
rulers that attempt to measure qualitative phenomena — privacy, exception
strength, suppression pressure, and similar. It is **not** a discovered theory of
reality. It is scaffolding in which testable hypotheses can be expressed in a
common language and then validated — or falsified — against independent data.

```
Synthium proposes rulers.
Rulers earn the right to be called "structural" only through predictive success
on independent data — never through architectural elegance.
```

This is a clean consolidation (v6.1) of the project's serious core. The
sprawling multi-version history — the "Omega" keyword-quantifier, the 2,045-line
v4.3.1 monolith, the descoped SRIA/LANL workstream, and the v3.x "discovery"
narrative — has been retired. See `RETIRED.md` for what was dropped and why.

## The one rule the whole package is built around

> **Arithmetic always runs. Claims are refused until a held-out test passes.**

- `synthium.core.values` — arithmetic that *always* succeeds and logs any
  assumption it had to make (e.g. multiplying two ordinals). The gate is never
  here.
- `synthium.core.validation` — the single refusal point. A model is born
  `PROPOSED`. The only path to `VALIDATED` is beating a pre-declared baseline by
  a pre-declared margin on held-out cases. `assert_validated()` raises otherwise.

This is the v6.0 correction to v5.0: v5.0 gated *computation* and so could never
even propose a model; v6.0 moves the gate to *claims*.

## Layout

```
synthium/
  core/
    values.py       ScaleType, Provenance, Value — arithmetic + assumption log
    baseline.py     Baseline as a frozen RULE (not a number), majority/keyword floors
    validation.py   Status, Verdict, PredictiveModel, ValidationProtocol, validate, metrics
  data/
    atlas.py        the 44-case rubric-coded atlas, loaded leakage-aware
    courtlistener.py rubric-INDEPENDENT outcome labeling from real court records
  domains/judicial/
    spec.py         12 units, 18 operators, formula hierarchy (all PROPOSED)
    formula.py      suppression-pressure formula with every coefficient exposed as ungrounded
    model.py        wraps the formula into a testable PredictiveModel
  cli.py            python -m synthium <command>
tests/              17 tests, pure stdlib
```

No third-party dependencies are required for the core, data, or judicial layers
— everything runs on the Python standard library.

## Quick start

```bash
python -m synthium harness-demo            # VALIDATED on real signal, FALSIFIED on noise
python -m synthium coefficients            # every hand-chosen constant, flagged ungrounded
python -m synthium atlas                    # atlas stats + the cluster->outcome leakage table
python -m synthium atlas-validate           # rubric-imitation smoke test (loudly caveated)
python -m synthium requirements             # what predictive validity would actually require
python -m synthium courtlistener-selftest   # offline extractor self-test (no token, no network)
python tests/test_synthium.py               # run the test suite
```

To pull real cases (needs a free CourtListener token):

```bash
export COURTLISTENER_TOKEN="..."
python -m synthium build-dataset --max 50 --out cases.jsonl
```

## Scientific status

A **prototype research framework, not a validated instrument.**

- All units are proposed measurement dimensions, not coordinates of reality.
- All formula coefficients are hand-chosen — none fit, derived, or measured.
  `python -m synthium coefficients` prints all 18.
- The judicial subject core is `PROPOSED`. It has **no demonstrated outcome-predictive validity** at the current data scale.
- Cross-domain unit recurrence is the only legitimate path from "proposed ruler"
  to "candidate structural claim", and it has no empirical force yet.

See `EMPIRICAL_STATUS.md` for the evidence picture and `PROJECT_INSTRUCTIONS.md`
for the calibration note.

## Vocabulary

Prefer **propose / construct / hypothesize** over **discover**; **ruler /
instrument / framework** over **theory / law / underlying structure**. The
"Newton-scale rigor for qualitative phenomena" framing is a long-term research
aspiration, kept visibly separate from any claim about current state.
