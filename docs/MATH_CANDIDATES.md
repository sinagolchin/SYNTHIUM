# MATH CANDIDATES — what in the audited record is already equation-shaped
(pilot computed 2026-07-10 on the 36 machine-readable committed rows; see caveats)

## 1. The suppression ratio S — the universality constant candidate
S = P(reversal | fact-side layer attacked) / P(movement | law-side layer attacked)

- Machine-readable set: 0/7 vs 15/29 -> S ~ 0, rule-of-three upper bound ~0.22 (n tiny)
- Lifetime as-logged (incl. the 2 override reversals in A3): ~0.01 / ~0.35 -> **S ~ 0.03**

Facts move ~30x less than law when directly attacked. S is DIMENSIONLESS, so it can
be measured in any jurisdiction regardless of local base rates. **The universality
claim becomes: S is small (<0.1) everywhere.** China is the predicted stress case.
This is the single best "physics-shaped" object we have: a suppressed (forbidden-ish)
transition channel with a measurable branching ratio.

## 2. The movement law (pilot logistic fit)
logit P(move) = -0.58 + 1.57*Phi + 0.41*apex, where Phi = T x L x (1-P)

- Both signs POSITIVE as the theory demands (more Phi -> more movement; apex -> more).
- Apex odds multiplier e^0.41 ~ 1.5x (population-level attempt data suggests 2-2.5x;
  see caveat C1).
- In-sample accuracy 61% vs 58% always-affirm: the continuous form UNDERPERFORMS the
  categorical v3.3 rules. **Finding: our unit values are currently ORDINAL, not
  CARDINAL.** The categories are right; the numbers attached to them are not yet on a
  true scale. Path to cardinal: backfill attempts 13/14/16/17 into CSV rows (~70 total),
  then fit T, L, P values themselves instead of the hand-set composite.

## 3. Ordering laws (court level as a temperature-like parameter)
Falsifiable predictions that have held in every batch so far, foreign included:
- O1: at EVERY court level, movement ordering is fact < discretion < remedy-calc < law.
- O2: raising court level raises movement for every layer but NEVER inverts O1.
- O3: overrides (clearly-erroneous / no-substantial-evidence) are the only fact-channel,
  rate ~1%.
A single observed inversion kills the temperature picture. None seen in 171 cases.

## Not yet math (named honestly)
- Entropy candidate (precedent density -> rising constraint): substrate exists
  (citation_space.py), zero committed tests.
- Axiom pricing (A2: penalty scales with interference): regression not yet run.

## Caveats
- C1: the v1 CSV was built for notch tests and is MOVEMENT-ENRICHED (intermediate rate
  here 38% vs ~19-29% population). Rates above are not population rates; signs and
  ratios are the usable content.
- C2: in-sample fit, single coder, one-state coefficients. To graduate, the FITTED
  equation must predict the next blind batch before reveal, same as every ruler version.

---

## REFIT on 71 committed rows (backfill of attempts 13/14/16/17; 2026-07-10)

**The four-number ruler** (grouped logistic, logit P = -2.37 + 1.86*lawside + 0.39*apex):

| | intermediate | apex |
|---|---|---|
| fact-side layer attacked | **0.09** | **0.12** |
| law-side layer attacked | **0.37** | **0.47** |

Layer dominates level: lawside odds x6.4 vs apex odds x1.5. S_strict = 0/9 in machine
rows (UB weak at this n); lifetime as-logged ~0.03. Params frozen in
synthium/domains/judicial/fitted_params.json; predict_p() exposes them.

**Two honest surprises the refit forced:**
1. **O1's within-law sub-ordering is NOT stable.** Intermediate: pure_law 3/16 (19%)
   < legal_overlay 4/9 (44%) < remedy_calc 3/3. Apex: overlay 5/13 (38%) < pure_law
   10/19 (53%). The clean, level-invariant statement is only **fact-side << law-side**;
   the within-law ordering flips with level (or is small-n noise). O1 revised
   accordingly — the ordering law survives at the side grain, not the layer grain.
2. **The apex effect concentrates in the PURE-LAW channel** (19% -> 53%, ~2.8x) while
   legal_overlay stays roughly flat (44% -> 38%). Reading: apex courts select pure-law
   questions to answer, and answer them by moving. This is the T x L x level cross-term
   made visible numerically.

## PRE-REGISTERED EXAM for the fitted equation (attempt 18, next batch)
- Fresh apex batch, 3 per category. Posture/layer coded per CODING_RUBRIC; the
  equation's p comes from the frozen table above — no human adjustment permitted.
- Because all p < 0.5, a 0.5-threshold test is vacuous (predicts affirm everywhere).
  The equation therefore graduates on **calibration**: Brier score vs two baselines,
  (i) always-affirm p=0, (ii) constant base-rate p=0.38.
- Pass condition: Brier(model) < Brier(always-affirm) on the fresh batch.

---

## v2 REFIT — posture added as third feature (n=89 total, 86 with known posture)

logit P(move) = -2.17 + 2.56*lawside + 0.28*apex + **-2.34***(1 - P_posture)

- In-sample accuracy 0.60 -> **0.663**; Brier 0.223 -> **0.206**. Real, if modest,
  improvement from adding posture. Params frozen in fitted_params_v2.json;
  predict_p_v2() exposes them.

### An honest surprise: the posture coefficient's SIGN is backwards from the hand-set theory
The original Φ = T x L x (1-P) design assumed trial-posture findings are heavily
DEFERRED to (low movement) while dismissal-posture rulings are freely reviewed
(high movement) — trial P=0.9 was meant to SUPPRESS movement, dismissal P=0.3 to
ALLOW it. **The fitted coefficient says the opposite in this sample: trial-posture
cases moved MORE (Taylor, Vandercar, Garrison, Donald all reversed at trial
posture) and dismissal-posture cases moved LESS** (Yeager, Mitchell, McCarthy all
affirmed at dismissal posture).

Leading hypothesis, NOT yet confirmed: "dismissal" in our coding has been
absorbing two different things — (a) pure legal rulings freely reviewable (the
original theory) and (b) procedural GATEKEEPING dismissals (adequate-remedy-at-law,
standing, finality) that apex/intermediate courts affirm almost mechanically as a
docket-control device. If (b) dominates the dismissal bucket in this sample, the
sign flip is a mixture artifact, not a refutation of the underlying theory — it
would mean "dismissal" needs to split into two postures, not that trial findings
aren't armored. **This is flagged, not resolved.** Do not treat the sign as settled.

### Retroactive re-score of attempt 18 (DIAGNOSTIC ONLY — NOT a validation)
Applying the fitted v2 model to attempt 18's own 9 cases separates them cleanly by
posture: trial (Taylor, Vandercar) -> p=0.61, both REVERSED; dismissal (Yeager,
Mitchell, McCarthy) -> p=0.27, all three CLEAN_AFFIRM; discretionary (the
remaining four) -> p=0.49, 3 of 4 moved. This LOOKS like vindication, but it is
circular: those 9 cases are now part of the 89-row training set, so of course the
refit fits them. **This is a diagnostic that motivated the refit, not evidence the
refit works on new data.**

## PRE-REGISTERED EXAM v2 (attempt 20, next batch)
- Fresh batch, any level/region, layer+posture coded from facts before scoring.
- p from predict_p_v2(), frozen, no adjustment.
- Pass condition: Brier(v2 model) < Brier(v1 2-feature model) < Brier(always-affirm)
  on the SAME fresh batch — i.e., v2 must beat v1, not just beat the naive baseline
  v1 already beat once. This is a harder bar than attempt 18's, on purpose.

---

## 4. THE STACKING LAW (new candidate, from TLM v Bedasie, attempt 26)
Fact-armor is cumulative in the number of courts that have concurrently found the fact.

  P(fact reversal) = f(k), k = number of courts below that concurrently found it
  Prediction: f is steeply decreasing; f(2) << f(1).

Doctrinal basis (not our invention — the courts say it):
- Privy Council: concurrent-findings practice, Devi v Roy — Board declines to
  review facts found concurrently by two courts, absent miscarriage of justice.
- US: the "two-court rule" analogue in habeas/appellate deference.
This explains the ~1% lifetime fact-reversal rate MECHANISTICALLY: apex fact
challenges are usually doubly-armored.

Status: CONSISTENT with our data (intermediate fact 0/6, apex fact 0/4 — both at
the floor) but NOT YET SEPARABLE at our n. To test: collect fact-layer challenges
specifically, at both levels, until the floor breaks. This is a rare case where the
theory predicts a difference our current data cannot yet see — a clean, honest,
falsifiable target.

---

# ⚠ MAJOR CORRECTION (attempt 27): the suppression ratio S was WRONG

## The error
I reported **S ≈ 0.03 — "facts move 30x less than law."** That numerator was
P(fact reversal | **ALL CASES**) = 2/171 = 0.012.

**That is the wrong denominator.** It counts hundreds of cases in which *no fact
challenge was ever raised*. A fact-finding cannot be "reversed" in a case where
nobody attacked it — those cases are not trials of the seam, they are silent on it.
The scientifically meaningful quantity is conditional on the challenge actually
being made:

  **S = P(fact reversal | a fact challenge WAS raised) / P(movement | law-side attacked)**

## The corrected number
Attempt 27 deliberately sampled *fact challenges* (sufficiency, credibility,
clearly-erroneous) — the only sample that can estimate the numerator.

- P(fact reversal | fact challenged) = **1/14 = 0.071**  (5 new + 9 prior fact-layer rows)
- P(movement | law-side attacked)    = **26/61 = 0.426**
- **S = 0.17 → facts move about 6x less than law, NOT 30x.**

## What survives and what dies
- **DIES:** the "30x" / "~1% fact reversals" headline. It was an artifact of dividing
  by every case in the register rather than by the cases where the seam was tested.
- **SURVIVES:** the seam itself. A 6x suppression is still a large, structural,
  measurable asymmetry — and it is now measured with the *right* conditional, which
  makes it a far more defensible quantity than the inflated one.
- **STRENGTHENED:** the override channel is REAL and ACTIVE, not a ~1% curiosity.
  Attempt 27 found two clean fact reversals via *clearly erroneous* (Circulent v.
  Hatch & Bailey — payment findings unsupported by the exhibits; Johnson v. Vita
  Built — findings contradicted by undisputed record). The armor has a working door.

## Methodology flag (self-caught)
One of the three queries in attempt 27 contained the word **"reversed"** — i.e. it
sampled on the *outcome*. Cases from that query (Lastrina, Johnson, Downing) are
recorded but **EXCLUDED from all rate estimation**; they are used only as existence
proof that the override fires. Rates above come from the outcome-neutral queries only.

## Consequence for the ordering laws
O1 (fact < discretion < remedy-calc < law) still holds at the *side* grain, but the
gap is 6x, not 30x. Any future "universal constant" claim about S must quote the
conditional version and state its n. Current best estimate: **S ≈ 0.17, n=14 fact
challenges, one jurisdiction, wide error bars.**

---

# ATTEMPT 28: a coding error, a new channel, and a BETTER-FORMED invariant

## Correction #2 — "sufficiency of the evidence" is NOT a fact challenge
I had been coding sufficiency claims as fact-layer. They are **law-side**:
- **Sufficiency** = "accept every fact as the trier found it — do they *legally* add
  up to the elements?" Reviewed **de novo**. The facts are conceded, not attacked.
- **Clearly erroneous / manifest weight / credibility** = "the finding itself is
  wrong." Reviewed **deferentially**. This is the real fact channel.
Different standards of review -> opposite sides of the seam. My earlier fact-side
counts were contaminated with law-side cases.

**Proof it matters (State v. Whitaker, OH Supreme):** an aggravated-burglary
conviction was **vacated for insufficient evidence at the apex** — yet **no fact was
disturbed**. The court accepted the facts (the house was vacant) and held, as
*statutory interpretation*, that a vacant house is not an "occupied structure." A
total win for the appellant, entirely in the law layer. Under my old coding this
would have looked like fact-armor failing. It is the opposite: the seam holding.

## New channel #3 — PROCEDURAL INTEGRITY (State v. Weaver, OH Supreme)
Reversed because the **fact-finder was biased**. Not "the facts are wrong" but "the
process that produced them was corrupt." This is a third door through the armor,
distinct from the override standards:
  1. override standards (clearly erroneous / no substantial evidence) — the finding
     is unsupported by the record
  2. **procedural integrity — the finder was not impartial**
  3. (candidate) documentary contradiction — see Circulent/Johnson: paper beats the
     finder; credibility findings still stand (Downing).

## A BETTER-FORMED INVARIANT (replaces the troubled S)
S kept shifting as I fixed denominators (0.03 -> 0.17 -> ~0.34 with corrected
coding, n=7, wide bars). The instability is a symptom: **S was the wrong quantity.**
It depends on how often litigants *choose* to attack facts, which is a strategic
variable, not a property of the law.

The stable, dimensionless quantity is:

  **W = P(the thing that moved was a FACT-FINDING | the case moved at all)**

This asks: *when an appellate court does act, what does it act on?* It is
independent of appeal rates, of litigant strategy, and of local base rates.

**Attempt 28 is the cleanest measurement yet: 6 of 9 cases MOVED (67%, apex) and
ZERO fact-findings were disturbed. W = 0/6 in this batch.**

Register-wide (as-logged): ~35 movement events, 4 involving a disturbed fact-finding
(C.W. v. E.W., Baywing, Circulent, Johnson v. Vita Built) -> **W ≈ 0.10.**

**The law, restated: when a case moves, ~90% of the time it is the LAW that moved,
not the facts.** That is the seam, expressed as a quantity that cannot be gamed by
changing the denominator.

## Stacking law — first real test
True deferential-fact challenges only (corrected coding):
- INTERMEDIATE (k=1 court below): **1/4** disturbed (Circulent)
- APEX (k=2 courts below): **0/3** disturbed (Menard, Reserve Realty, Garrett)
Direction is CONSISTENT with f(2) < f(1). **n is far too small to claim it.** Needs
~30 fact challenges per level. Honest status: not yet evidence, just not yet refuted.

---

# FULL EVALUATION (attempt 29) — 151 committed rows, and a striking new invariant

## LAW 1 — W, the movement-destination law (now measured at scale)
  **W = P(fact-finding disturbed | the case moved) = 2/57 = 0.035**
  Register-wide incl. the 2 pre-machine attempt-3 reversals: **W ≈ 0.07**

  **When an appellate court moves a case, ~95% of the time it is the LAW that moved.**
  Measured over 57 movement events across 2 US states + 5 foreign systems.

## LAW 3 — ⭐ THE FACT CHANNEL IS LEVEL-INVARIANT (new, unexpected)
Movement rate, split by which side was attacked and how high the court is:

| | fact-side attacked | law-side attacked |
|---|---|---|
| **intermediate** | **0.14** (3/22) | 0.36 (16/44) |
| **apex** | **0.14** (2/14) | **0.51** (36/71) |

**The law-side rate RISES with court level (0.36 -> 0.51). The fact-side rate does
NOT MOVE AT ALL (0.14 -> 0.14).**

This is the sharpest structural result we have. Court level behaves like a
temperature-ish parameter — raise it and the system moves more — but **it only
excites the LAW channel. The fact channel does not respond to it.** The fact
channel appears *frozen out*: it has a floor that raising the court level cannot lift.

Why this matters more than the raw numbers: every prior finding said "facts move
less." This says something stronger and stranger — **facts move less AND their rate
is insensitive to the one parameter that governs everything else.** A conserved-ish
channel that doesn't couple to the system's driving variable is exactly the shape of
a genuine structural constraint rather than a mere tendency.

Honest caveats (real, not decorative):
- n on the fact side is small (22 and 14). 0.14 vs 0.14 could be coincidence; what
  is robust is the *direction*: law-side clearly rises with level, fact-side shows
  no rise. A larger fact-side sample could still break the exact equality.
- The fact-side bucket still contains some cases coded before the sufficiency
  correction. The strict deferential-fact subset is 0/6 disturbed (both levels).
- Prediction, now falsifiable: **collect 40+ deferential-fact challenges at each
  level; if the apex rate is materially BELOW the intermediate rate, the stacking
  law wins and level-invariance dies. If they stay equal, level-invariance holds and
  stacking is wrong.** These two candidate laws now make OPPOSITE predictions — a
  clean fork the data can settle.

## LAW 2 — stacking: still not evidence
Deferential-fact challenges: intermediate 0/2, apex 0/4 disturbed (strict coding);
broader fact-layer rows at intermediate 2/7. Direction inconclusive. **Note this now
CONFLICTS with LAW 3's level-invariance.** One of them is wrong. Good — that is what
a falsifiable pair looks like.

## MODEL EVALUATION — all 151 rows
| model | Brier |
|---|---|
| v2 (lawside + apex + posture) | **0.2018** |
| v1 (lawside + apex) | 0.2146 |
| always-affirm baseline | 0.3775 |

v2 < v1 < baseline confirmed at full scale. (In-sample for v1/v2 — they were fit on
subsets of these rows; the honest prospective results remain attempts 20 and 21,
where v2 beat v1 on genuinely held-out data.)

---

# UNITS OF MEASUREMENT — what is genuinely extractable (post-audit, computed 2026-07-13)

## U1 — The epistemic skeleton's natural unit: the DECIBAN (weight of evidence)
The factorization test (LR=0.04) found the gates act INDEPENDENTLY. Independent gates
multiply odds; the unique additive scale for multiplicative odds is the logarithm; the
classical unit of log-odds evidence is the ban/deciban (Turing & Good). Measured on the
deduped register (n=159, Fisher SEs):
  baseline (fact-side, intermediate) = -9.2 ± 2.2 db
  LAW-SIDE gate                      = +7.0 ± 2.3 db
  APEX gate                          = +2.2 ± 1.6 db
  DOC-vs-CRED gate (retrodictive)    = +25.0 ± 9.0 db  [Haldane-corrected; clean test owed]
  GATEKEEPING gate                   = -25.0 ± 9.0 db  [Haldane-corrected]
The seam, as a number: attacking law instead of fact buys ~+7 db; the strongest gates in
the system (~±25 db) are the access gate and the channel gate — an order of magnitude
larger than the court-level gate. Units portability across jurisdictions: UNTESTED.

## U2 — Dimensionless invariant candidate: W = 0.052, 95% CI [0.018, 0.141]
P(the moved thing was a fact | something moved). Register-wide; per-system values unmeasured.

## U3 — The STANDARD LIFE-YEAR (China, enacted): closed form extracted
Art. 15 (SPC Interpretation, 2022): death compensation = I_pc x L(age), where I_pc =
urban per-capita disposable income. Verified identical for all ages 18-100:
  **L(a) = clip(80 - a, 5, 20)**  [standard life-years]
Implied constants enacted by the statute: lifespan horizon 80; cap 20; floor 5; marginal
price of a year of age = -1 income-year/yr, ONLY on (60,75]. One unit: 1 SLY = 1
per-capita income-year. A QALY-like unit, in force, with a court behind it.

## U4 — Dimensional analysis distinguishes the value objects
UK bereavement: [currency x death^-1] (fixed sum divided among claimants).
German Hinterbliebenengeld: [currency x mourner^-1] (each survivor in full).
Same institution name, DIFFERENT DIMENSIONS -> different objects, provable by units alone.
Connecticut D_life: [currency x death^-1], owed to the estate, floor independent of earnings.

## U5 — Dignity ratio R = D/V (dimensionless, cross-system)
UK: D = 15,120 pounds (statutory); V = dependency (estimate 300k-1M) -> R ~ 0.015-0.05. ESTIMATE.

## What is NOT extractable yet (honest)
No conservation law. No entropy measure (substrate seed only). Level-invariance NOT
established post-dedupe. All logistic weights one-jurisdiction-dominated. The +-25 db
gates rest on 19 and 19 cases respectively, one retrodictive.
