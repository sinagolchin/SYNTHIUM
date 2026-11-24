# v7.0 — The 12 units are gone. Dimensions now emerge from data.

## What was removed
Deleted from the active package: the 12 hand-coded units (`spec.py`), the
18-coefficient suppression formula (`formula.py`), the formula model
(`model.py`), the 12-unit axiom suite (`domains/judicial/axioms.py`), and the
unit-based currency solver (`currency.py`).

Why: those units were never validated. They were stipulated by earlier sessions,
required subjective 0–1 coding per case (the bottleneck), and made axiom-testing
circular — we'd have been testing axioms against a coding scheme that was itself
just a guess.

## The rule that replaces them
> A dimension is admissible only if it can be extracted from the record
> **reproducibly, with zero subjective coding**, and it must **earn its place**
> by predicting the independent outcome — never by doctrinal storytelling.

## The new substrate: citations
A case is now represented by **the set of precedents it cites** — a fact in the
record and in the API, needing no human judgment, available for every published
case. Dimensions are not declared; they emerge:

- A **hub precedent** (cited by many cases) is a candidate dimension: "does this
  case rely on precedent X?" — a reproducible 0/1 feature.
- Cases sharing citations form **emergent families** — discovered, not imposed.

A candidate becomes a real dimension only when its presence predicts the
independent outcome on held-out cases (`synthium.core.validation`). The emergent
layer finds candidates; the validation gate certifies them.

## First run (seed: 10 cases, `python -m synthium citation-space`)
- 185 distinct precedents; 3 hub precedents already shared across cases (e.g.
  one Indiana precedent shared by the two Indiana cases — a jurisdiction family
  appearing on its own).
- Cross-case overlap is thin (jaccard ≈ 0.03) — expected at n=10 spread across
  many jurisdictions, where most citations are local.

## What this changes about scaling
The reason to do this: **the coding bottleneck is gone.** Citations ingest with
zero hand-coding, so the same objective pull runs to thousands of cases. At that
scale the landmark Fourth Amendment precedents will surface as high-degree hubs
and jurisdiction/doctrine families will densify — and only then does outcome
validation have the numbers to certify any dimension. The blocker was never the
data; it was the hand-coding the old units forced. That is removed.

## Kept (sound, dimension-agnostic)
`core/values`, `core/validation`, `core/baseline`, the generic `core/axioms`
machinery (it tests whatever dimensions emerge), and the CourtListener labeler.
The boundary-equilibrium solver math is retained in git history and returns once
emergent dimensions exist to run it on.
