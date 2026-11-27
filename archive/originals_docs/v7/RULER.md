# RULER.md — the one living file for judicial units & formulas

This is the single place where proposed units and formulas live. Every time we
evaluate a case, we come back here and either KEEP or CHANGE the unit/formula
that the case touches, with the reason logged. Nothing is settled; everything is
a hypothesis under revision.

Domain: **judicial**, all three categories — **criminal, civil, administrative**.
Sources this attempt: CourtListener. (Trellis is available; Courtroom5 is
connected but exposed no usable tools, so it was not used.)

---

## The honest status of these units (read first)

These units are scored by **judgment**, not by a reproducible rule, and on this
first attempt they were scored **knowing the outcome**. That means the 9/9
"fit" below is NOT evidence the units work — it can just be the coder agreeing
with himself. What IS real here is the machinery: a proposed ruler, a formula,
and a case-by-case loop where a real outcome can force a change. One case already
forced one (see Hartford, below). Validation comes later, from blind coding at
volume.

---

## Current units (v1)

A case is viewed as an **appeal**: a challenger asks a higher court to overturn
the decision below. The universal outcome is **WIN** (challenger gets relief /
reversal) or **LOSE** (affirmed / denied). Two proposed units drive it:

- **E — Error clarity** (0–1): how clearly the decision below got the dispositive
  point wrong. 0.1 = clearly correct below; 0.9 = obvious, dispositive error.
- **D — Deference** (0–1): how much the standard of review protects the decision
  below. 0.2 = pure legal question reviewed fresh (de novo); 0.8 = factual
  finding / agency discretion / abuse-of-discretion (hard to overturn).

(A third candidate, **P — procedural posture**, is held in reserve; several cases
turned on ripeness/finality and may need it. Not yet adopted.)

## Current formula (v1)

    Challenger-success  Ω = E − D
    Predict WIN if Ω > 0 ... BUT see the override below.

**v0 → v1 change forced by a case.** v0 was simply `WIN if E − D > 0` (deference
must be overcome by clearer error). The Hartford case broke it: the challenger
WON despite the highest deference (agency fact-finding, substantial-evidence
review) because the error was egregious (no evidence at all). So deference does
**not** simply subtract — a clear-enough error overrides it. v1 adds:

    OVERRIDE: if E ≥ 0.7, predict WIN regardless of D  (clear error dominates).

This is the **dominance axiom** showing up in real data: past a threshold, one
unit dictates the outcome and the others stop mattering. We did not assume that;
the Hartford case produced it.

---

## Per-case log — Attempt 1 (9 cases)

Outcome = challenger's result. E,D scored from the court's own reasoning.

### Criminal
| Case | E | D | Ω=E−D | v1 predict | actual | keep/change |
|---|---|---|---|---|---|---|
| Jeffrey Z. (sex-offender registration) | 0.2 | 0.4 | −0.2 | LOSE | LOSE | KEEP |
| Wilson v. Comm'r (habeas certification) | 0.8 | 0.7 | +0.1 | WIN | WIN | KEEP |
| Hilton v. Comm'r (ineffective assistance) | 0.2 | 0.8 | −0.6 | LOSE | LOSE | KEEP |

### Civil
| Case | E | D | Ω=E−D | v1 predict | actual | keep/change |
|---|---|---|---|---|---|---|
| New Capital v. KOSL (broker unlicensed) | 0.3 | 0.5 | −0.2 | LOSE | LOSE | KEEP |
| Cruz v. Spec Personnel (no duty of care) | 0.75 | 0.3 | +0.45 | WIN | WIN | KEEP |
| Amica Mutual v. Gilleran (duty to defend) | 0.3 | 0.4 | −0.1 | LOSE | LOSE | KEEP |

### Administrative
| Case | E | D | Ω=E−D | v1 predict | actual | keep/change |
|---|---|---|---|---|---|---|
| Greenwich Retail (tax penalty) | 0.25 | 0.5 | −0.25 | LOSE | LOSE | KEEP |
| CHRO v. Travelers (age-ad discrimination) | 0.3 | 0.6 | −0.3 | LOSE | LOSE | KEEP |
| Hartford v. CHRO (ancestry discrimination) | 0.7 | 0.8 | −0.1 | (E−D) says LOSE → **override → WIN** | WIN | **CHANGE (added override)** |

**What the loop did this attempt:** 8 cases KEPT the formula. 1 case (Hartford)
CHANGED it — forcing the dominance override. That single forced change is the
whole point: reality edited the ruler, not the other way around.

---

## Cross-category observation (a candidate finding, not a claim)

The same two units — error clarity and deference — appear to govern the outcome
in **all three categories**. Criminal, civil, administrative did not need
different rulers; they needed the same one. If that survives blind coding at
volume, it is exactly the kind of cross-domain unit the project is hunting: a
ruler that measures "did the tribunal below clearly get it wrong, against how
hard it is to overturn" — across the whole judicial system, not one corner of it.

---

## Standing routine (every attempt)

1. Pull **3 cases per category** (criminal, civil, administrative) from the
   connected sources.
2. For each case: score the current units, predict with the current formula,
   compare to the real outcome.
3. KEEP the unit/formula if it held; CHANGE it (and log why) if a case broke it.
4. Append the cases to the log here. This file is the running record.

## Next, to make it real (not just consistent)

- Score units **before** reading the outcome (blind), ideally by more than one
  coder, so a fit means something.
- Grow to dozens of cases per category; then test E and D for genuine
  independence and predictive power with the validation harness.
- Decide whether **P (procedural posture)** must be adopted — watch for cases
  that are lost purely on ripeness/finality despite a strong merits error.
