# Synthium Axioms — Canonical Record (v6.2)

This file is the single source of truth for Synthium's axioms. It exists because
the axiom set drifted silently across prior AI sessions (see the lineage in
`RETIRED.md`): a "precision confers fitness" axiom, an ethical Being/Freedom/
Trajectory triad, and an Agnosticism meta-axiom were each added and dropped
without record. **No axiom may be added, removed, or changed without an entry
here and a CHANGELOG note.**

Axioms come in two kinds. **Epistemic** axioms govern how Synthium may make
claims. **Generative** axioms have a mathematical form and constrain what units
and formulas are allowed — they can be violated by data. Every prior axiom in
the project's history was epistemic and informal (`mathematical_form = None`).
v6.2 adopts the first generative ones.

---

## Epistemic axioms (the referee — carried forward)

1. **Agnosticism** — every formula is a hypothesis, never a truth.
2. **Arithmetic never refuses** — computation always runs; only claims are gated.
3. **Proposed until proven** — a model earns standing only by a held-out test.
4. **Reality is the sole judge** — validation uses data the framework didn't author.
5. **Baseline frozen first** — the comparison is fixed before any outcome is seen.
6. **Stipulated until grounded** — hand-chosen coefficients stay flagged ungrounded.
7. **No leakage** — a feature may never contain the target.
8. **Units are constructed** — dimensions are instruments, not coordinates of reality.

These remain in force. They are implemented as architecture (`core.validation`,
`core.values`, the leakage-aware `data.atlas`), not as stated objects.

---

## Generative axioms (the friction surface — adopted v6.2)

Implemented in `synthium/core/axioms.py`; run with `python -m synthium axiom-test`.
Each has a `test()` that returns SATISFIED, VIOLATED, or an honest cannot-test.

| # | Axiom | Mathematical form | Generates | Status on atlas |
|---|---|---|---|---|
| G1 | Weak order | `a≥b or b≥a; a≥b & b≥c ⇒ a≥c` | ordinal scale | REQUIRES_PAIRWISE |
| G3 | Double cancellation | `(a1,b2)≥(a2,b1) & (a2,b3)≥(a3,b2) ⇒ (a1,b3)≥(a3,b1)` | additive interval scales + unit | **VIOLATED** (Priv×Excp) |
| G4 | Absorption (mult. zero) | `D=0 ⇒ outcome≠active` | product-of-powers algebra | INSUFFICIENT_DATA |
| G5 | Dominance | `D>t ⇒ outcome=forced` | weakest/strongest-link rule | SATISFIED (low cov.) |
| G8 | Independence of basis | `rank(D)=#dims` (pairwise \|r\| screen) | a genuine basis | SATISFIED (worst \|r\|=0.74) |
| G7 | Dimensional homogeneity | `[lhs]=[rhs]` per additive term | formula firewall | REQUIRES_COMMITMENT |
| G9 | Boundary equilibrium | `balance(case)=threshold` on close cases | **solves** for coefficients | REQUIRES_COMMITMENT |
| G10 | Invariance → conservation | `symmetry S ⇒ conserved Q` | a reason for the balance law | REQUIRES_COMMITMENT |

(Numbering follows the suggestion list; G2/G6 — solvability, lexicographic — are
not yet adopted but reserved.)

---

## First results (44-case atlas, structural-consistency mode)

A PASS here means the rubric's own coding is internally consistent with the
axiom — **not** predictive validity, because atlas outcomes share a source with
the features. The definitive run uses court-derived outcomes.

Three findings worth recording:

1. **Double cancellation is VIOLATED on Priv×Excp** — 4 violations across 28
   testable triples, all 9 grid cells filled. Even the rubric's own ordering does
   not support adding privacy and exception strength on a common interval scale.
   This is the project's first piece of generated friction: it points away from
   an additive rule and toward a multiplicative or limiting one. Caveat: n is
   small and the ordering is binary, so this is a signal to pursue, not a proof.

2. **The 12 units pass the independence screen** — worst pairwise correlation
   0.74, none above 0.9. No proposed unit is a near-duplicate of another. Weak
   support for treating them as a basis. (Pairwise only; full-rank collinearity
   needs the `discovery` extra.)

3. **Absorption is untestable on current data** — the atlas contains no case with
   Priv≈0 or Rem≈0. This is a concrete collection target: to test whether privacy
   is an absorbing factor, code cases with a genuinely absent privacy interest.

---

## Governance

- Changing this file requires a CHANGELOG entry naming the axiom and the reason.
- An axiom with `mathematical_form = None` is not an axiom here; it is a note.
- Adopting G9 (boundary equilibrium) is the next milestone: it converts the 18
  hand-tuned coefficients from stipulated to solved. It needs two commitments
  from the researcher — the conserved currency, and which cases are on the line.
