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

---

## v1 → v2 unit change (forced by Brown)

**E is sharpened.** Old E = "how clearly the decision below got *the* point wrong."
The **Brown** case (criminal) broke that: the habeas court *did* make a clear
legal error (a witness's prior statement was admissible and it said otherwise),
yet the petitioner **LOST**, because that error was harmless — counsel's choice
not to use the statement was reasonable, so it changed nothing. So:

    v2:  E = error clarity ON THE OUTCOME-DETERMINATIVE issue.
         A clear but harmless / side-issue error scores LOW, because it
         is not the error that decides the case.

**Honest danger flagged.** This refinement can quietly become circular: if I
decide "harmless" *after* seeing who won, I'm letting the outcome define E, which
is exactly the trap. The only clean fix is to score E from the facts and the
contested issue **before** reading the result. Logged as the top priority for
blind coding.

---

## Per-case log — Attempt 2 (9 cases, CourtListener / Connecticut)

E scored on the dispositive issue (v2). Formula v1 unchanged: Ω = E − D;
WIN if Ω > 0; OVERRIDE: if E ≥ 0.7, WIN regardless of D.

### Criminal
| Case | E | D | Ω | predict | actual | keep/change |
|---|---|---|---|---|---|---|
| Brown v. Comm'r (clear error, but harmless) | 0.25 | 0.8 | −0.55 | LOSE | LOSE | **forced v2 E refinement** |
| Harvey (double jeopardy → conviction vacated) | 0.7 | 0.3 | +0.4 | WIN | WIN (partial) | KEEP |
| Gibbs (McCoy autonomy rejected) | 0.2 | 0.6 | −0.4 | LOSE | LOSE | KEEP |

### Civil
| Case | E | D | Ω | predict | actual | keep/change |
|---|---|---|---|---|---|---|
| SR Holdings v. Cannavo (appeals fail) | 0.3 | 0.6 | −0.3 | LOSE | LOSE | KEEP |
| Akinyele v. Huntington (res judicata reversed) | 0.75 | 0.25 | +0.5 | WIN | WIN | KEEP |
| C.W. v. E.W. (clearly-erroneous fact reversed) | 0.7 | 0.75 | −0.05 → **override → WIN** | WIN | WIN | KEEP (confirms override) |

### Administrative
| Case | E | D | Ω | predict | actual | keep/change |
|---|---|---|---|---|---|---|
| Baywing v. WPCA (no substantial evidence) | 0.7 | 0.8 | −0.1 → **override → WIN** | WIN | WIN | KEEP (confirms override) |
| Sargent v. Zoning Board (variance upheld) | 0.25 | 0.7 | −0.45 | LOSE | LOSE | KEEP |
| Ancona v. Eller (anti-SLAPP, unpreserved) | 0.2 | 0.5 | −0.3 | LOSE | LOSE | KEEP |

**What the loop did this attempt:** 9/9 fit; one case (Brown) sharpened the
definition of E; two cases (C.W., Baywing) again won despite high deference,
confirming the override. Across two attempts the override has now fired for three
high-deference wins (Hartford, C.W., Baywing) in all three categories.

## A warning the data is starting to give

The override (E ≥ 0.7 ⇒ WIN) is doing a lot of work, and under outcome-aware
coding it is at risk of becoming **unfalsifiable**: if I score every winner's E
at 0.7+, the rule can never be wrong. To actually test it I need the case that
would break it — a genuinely clear, dispositive error where the challenger
**LOSES** anyway. I have not seen one yet. Finding (or failing to find) that case
is the real next job, and it only means something under blind coding.

## Running tally (attempts 1–2): 18 cases, 6 categories-worth
- Units still in use: **E** (now v2, dispositive-issue) and **D**. Same two units
  govern criminal, civil, and administrative alike — holding so far.
- Formula: **Ω = E − D**, with the **E ≥ 0.7 override**. Unchanged this attempt.
- Confirmed weakness: scoring is single-coder and outcome-aware; the override
  needs a falsification case; **P (posture)** still not needed (Brown and Ancona
  were handled by the dispositive-issue version of E, not a separate unit).

---

# CORRECTIONS (post-evaluation) — the leak, demonstrated

Running the numbers on our own 18 cases:

| feature | what it is | correlation with win | separates wins/losses? |
|---|---|---|---|
| **E** (error clarity) | scored from the opinion, written AFTER the ruling | **+0.99** | perfectly, at 0.5 |
| **D** (deference) | standard of review, fixed BEFORE the ruling | **−0.07** | no |

**Conclusion (honest):** the 18/18 fit was carried entirely by E, and E is a
relabelling of the verdict, not a measurement of the case. r = +0.99 with perfect
separation is the signature of leakage. D — the only feature knowable before the
decision — predicts essentially nothing on its own. **The ruler has not been
shown to measure anything leak-free.** That is the corrected status.

Baseline honesty: on these 18, "always predict LOSE" scores 61%. And the sample
is reversal-biased — 39% wins here vs ~10–20% in real appellate courts — because
syllabus-rich, interesting cases were selected. A representative sample would make
the always-LOSE baseline ~85%, a bar nothing here has cleared.

The override (E ≥ 0.7 ⇒ WIN) is void as evidence: since E leaks, "confirming" it
three times confirmed nothing. Brown was a genuine near-falsifier (clear error,
challenger lost) and the only thing that saved the override was calling that error
"harmless" — a judgment made after seeing the result. That is the circularity.

## Corrected method (adopted going forward)

1. **Two ledgers, never mixed.**
   - LEAK-FREE inputs — knowable before the ruling: standard of review (D),
     who is appealing (criminal defendants lose ~85–90%), issue type, whether
     there was a dissent below. These are the only legal inputs to a prediction.
   - E is retired as an INPUT. It may be scored only **blind** (from the facts
     and the contested issue, before reading the holding) and only as a thing we
     are trying to predict — never as a predictor.
2. **Commit before reveal.** Score leak-free features, write the prediction to
   PREDICTIONS_REGISTER.md, THEN read the outcome. A prediction not written down
   before the reveal does not count.
3. **Beat the honest baseline.** A rule only earns the word "works" if it beats
   always-LOSE on a sample whose win-rate matches reality — not on a
   reversal-biased pick.
4. **Hunt the falsifier.** Actively look for a clear, dispositive error where the
   challenger LOSES anyway. Until that case is sought and not found, no override
   survives.

The two-attempt E/D log above is kept as an honest record of how a leaky feature
can fake a perfect fit — not as a result.

---

# RULER v3 — units and formula proposed from the 100-case blind register

The v1/v2 units (E = error clarity, D = deference) were judgment-scored and E
leaked. v3 replaces them with three units that are **categorical, objective, and
readable before the ruling** — each one earned by a pattern that held across the
blind register, not stipulated in advance.

## The v3 units

**T — Type risk** (what kind of case is it? read from the caption)
| category | T | basis (blind register) |
|---|---|---|
| criminal / habeas / child protection | 0.05 | ~0 reversals in 15+ cases |
| administrative | 0.15 | 1 of 6 |
| family | 0.30 | small n, ~1 in 3 |
| general civil | 0.35 | ~1 in 3 got some relief |

**P — Posture protection** (what did the trial court do? read from the record)
| posture below | P (protection of the outcome below) |
|---|---|
| full trial (jury or court), fact-findings made | 0.9 |
| default / settlement-enforcement / discretionary rulings | 0.7 |
| summary judgment / directed verdict | 0.4 |
| motion to dismiss / strike / sua sponte or finality defects | 0.3 |

**L — Layer of the challenged issue** (what is the appellant attacking?)
| layer | L (openness to being moved) |
|---|---|
| fact-findings, credibility | 0.1 |
| remedy / damages / fees | 0.5 |
| pure law riding on top (standing, statute reach, coverage, due process) | 0.9 |

L is the v3 successor to old E — but instead of judging "how wrong" the court
was (unknowable before the ruling), it records *which kind of question* is being
attacked, which IS knowable from the briefs/record. Old D survives inside P and
L: deference is high on facts, zero on law.

## The v3 formula (proposed)

    Movement potential   Φ = T_norm × L × (1 − P adjustment)
    Practical 3-notch rule:
      1. If the attacked issue is a FACT layer            -> predict CLEAN AFFIRM
      2. If the attacked issue is REMEDY only             -> predict MODIFIED-at-most
         (liability stands; money/relief may move)
      3. If the attacked issue is PURE LAW:
           - in criminal/habeas/child (T ≤ 0.05)          -> predict CLEAN AFFIRM anyway
           - in civil on a paper posture (P ≤ 0.4)        -> flag LIVE (reversal zone)
           - in civil after trial                          -> liability likely stands,
             but the legal overlay itself can flip (Bernblum, Gilman pattern)

In one sentence: **nothing moves unless a law-layer issue exists; type sets how
much appetite the court has; posture says how much of the case is fact-armored.**

## Keep/change log for this proposal
- KEEP: three-notch outcome scale (clean/modified/reversed) — earned by ~10
  partial outcomes the binary misscored.
- CHANGE: E (v2) retired entirely as an input → replaced by L (issue layer),
  which is codable pre-ruling. This resolves the leak that killed v1/v2.
- CHANGE: D generalized → split into P (posture) + the L=fact protection.
  Deference attaches to the fact layer, not to the case as a whole.
- KEEP: type signal from attempts 3–5, now unit T.

## Honest status (do not skip)
- The numeric values (0.05, 0.35, 0.9...) are **frequencies from the same 100
  cases** — in-sample. They are proposed, not validated. The formula must now be
  tested on FRESH blind cases it has never seen, committed before reveal.
- Single coder; posture/layer coding is objective in principle but should be
  double-coded.
- Φ as a multiplicative form is a stipulation; additive and lexicographic rivals
  should be run against it (the old axiom machinery applies: dominance = the
  fact-layer rule; absorption = T≈0 categories).
- Success criterion, stated in advance: on the next 30+ fresh blind cases, the
  3-notch rule must beat "always clean-affirm" (currently 70%) on overall
  accuracy AND correctly flag a majority of the modified/reversed cases.

---

# RULER v3.2 (current) — consolidated statement

**Outcome scale (3 notches):** CLEAN AFFIRM / MODIFIED / REVERSED.

**Units (all objective, all readable before the ruling):**
- **T — type:** criminal/habeas/child ≈ 0.05 · admin ≈ 0.15 · family/civil ≈ 0.3–0.35
- **P — posture:** full trial 0.9 · default/discretionary 0.7 · summary judgment 0.4 · dismissal/strike 0.3
- **L — layer under attack:** fact 0.1 · remedy-as-estimate 0.2 · remedy-as-calculation 0.6 · separable legal overlay 0.9 · purely-legal-case (no fact layer) = treat as base rate

**Decision rule v3.2:**
1. T ≤ 0.05 (criminal/habeas/child) → CLEAN AFFIRM.
2. Attack on FACT layer or remedy-as-ESTIMATE → CLEAN AFFIRM.
3. Fact layer exists AND a separable LEGAL overlay or remedy-CALCULATION is attacked → MODIFIED (facts stand, overlay moves). ← the star rule, 11/12 lifetime
4. PURELY legal case (no fact layer to protect) → CLEAN AFFIRM, tag high-variance.
5. Paper posture (P ≤ 0.4) → CLEAN AFFIRM, tag high-variance (no edge there yet).

**Keep/change history:** v1 E−D (leaked, retired) → v2 dispositive-issue E
(still leaked, retired) → v3 T/P/L from the 100-case register → v3.1 paper-zone
fix → v3.2 overlay-vs-pure-law and estimate-vs-calculation splits (on probation,
awaiting fresh-batch exam).

---

# v3.2 → v3.3 (from attempt 15, the prospective exam at CT Supreme)
- CHANGE R1: type-armor holds at INTERMEDIATE courts only. At apex/discretionary
  law-courts, layer dominates type (criminal moved 3/8 there). New form:
  R1 applies iff court_level = intermediate.
- ADD to L: 'discretionary ruling reviewed for abuse of discretion' ≈ protected
  (0.25) — Rodriguez. Third protection regime alongside fact and remedy-estimate.
- KEEP R3 (star rule): confirmed at apex level (AGW exact; Kovachich movement).
- KEEP the fact seam: 0 fact-layer reversals in 14 more cases; lifetime unbroken.
- Proposed unit set is now T (type) x P (posture) x L (layer) x **level** — the
  court-level interaction is the first CROSS-UNIT term the data has forced.
