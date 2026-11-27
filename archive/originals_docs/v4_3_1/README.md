# Synthium

**A structural framework for constructing measurement rulers for abstract concepts.**

Synthium is research infrastructure for proposing, building, testing, and revising rulers that attempt to measure qualitative phenomena — privacy, exception strength, suppression pressure, correlation quality, semantic coherence, and similar.

Synthium is **not** a discovered theory of reality. It is a scaffolding inside which testable hypotheses can be expressed in a common mathematical language and validated (or falsified) against external data.

## Core principle

```
Synthium proposes rulers.
Rulers earn the right to be called "structural" only through predictive success
across independent domains and independent data — not through architectural elegance.
```

## Architecture

### Synthium Core (universal layer)

- **Confidence system** with decay and weakest-link aggregation
- **State representation** (`RealityState`) over an n-dimensional manifold
- **Riemannian geometry** with optional position-dependent metric, geodesic approximation, and local curvature proxy
- **Dimensional discovery engine** (PCA, ICA, Isomap, LLE) with bootstrap stability scoring
- **Subject-core registry** for tracking proposed domain instantiations
- **Impact geometry** (depth × breadth) as a candidate cross-domain pattern
- **SCK** (Semantic Coherence Kernel) as a runtime integrity regulator
- **Governance engine** with hysteresis, persistence-based escalation, and trajectory-aware risk scoring

### Subject Cores (domain instantiations)

Each subject core is a **proposed** set of units, operators, and formulas for a specific domain. Subject cores do not become Core. Core remains the universal ruler-building infrastructure; subject cores are hypotheses about a particular field.

Currently included:
- **Judicial Module v0.2** — Fourth Amendment suppression doctrine (12-unit extended state)
- **Cyber / SRIA Module v0.6.1** — host/network correlation with quality-gated evidence

Planned:
- Medical / physiology
- Sociology / population dynamics

### Optional Neural Layer

A small trainable encoder (PyTorch) that maps domain text into proposed units, operators, outcomes, and learned manifold embeddings. The current neural layer learns to imitate human-coded rubric labels; it has **not** yet been trained against outcomes independent of the rubric.

## Scientific status

This is a **prototype research framework**, not a validated instrument.

- All units are proposed measurement dimensions, not assumed coordinates.
- All formulas are falsifiable hypotheses with hand-tuned coefficients.
- Subject cores will be revised, versioned, and possibly abandoned as data accumulates.
- Cross-domain recurrence (tracked via the `universal_candidate` flag) is the only legitimate path from "proposed ruler" to "candidate structural claim".

See `EMPIRICAL_STATUS.md` for the current evidence picture, including the de-leaking results from v4.3.1.

## Quick start

```bash
# Original training run (preserved for reproduction).
PYTHONPATH=. python -m synthium.domains.judicial.train --epochs 180

# De-leaked training run (correct baseline). See EMPIRICAL_STATUS.md.
PYTHONPATH=. python -m synthium.domains.judicial.train_deleaked --epochs 180 --seeds 5
```

## Vocabulary

We prefer **propose / construct / hypothesize** over **discover**. We prefer **ruler / instrument / framework** over **theory / law / underlying structure**. The "Newton-scale rigor for qualitative phenomena" framing is a **long-term research aspiration** and is kept visibly separate from claims about current state.

## Important limitations

- Sample sizes are small. The judicial atlas is 44 cases.
- Atlas labels are rubric-derived; predicting them does not establish predictive validity for outcomes.
- Coefficients in symbolic formulas (e.g., `priv * (1 - 0.85 * bound)`) are hand-chosen, not learned or derived.
- The dimensional discovery engine has not been used to verify the intrinsic dimensionality of any proposed unit space.

## Citation

If you reference Synthium in academic or technical work, please treat it as a research framework in active development, not a validated estimator.
