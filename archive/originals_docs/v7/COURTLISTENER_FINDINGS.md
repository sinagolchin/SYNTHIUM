# First Live CourtListener Pull — Findings (v6.2, dataset v0)

## What happened

Pulled real Fourth Amendment suppression opinions live from CourtListener and
read each disposition directly. Six were coded end-to-end into the package
schema (`data/courtlistener_cases_v0.csv`): outcome read from the court's
holding, the 12 units coded from the facts.

| Case | Court | Outcome (from disposition) | Posture |
|---|---|---|---|
| United States v. Smith | D.D.C. | DENIED | auto stop, open container plain view |
| State v. Times | Fla. | DENIED (final) | home + valid warrant, knock-and-announce; trial granted, **quashed** |
| United States v. Moore | D.D.C. | GRANTED | auto, search scope grossly exceeded |
| State v. Beasley | Del. | GRANTED | warrantless home/garage entry, no exigency |
| United States v. Hoover | 6th Cir. | DENIED | auto, plain-view gun |
| People v. Hayes | Cal. App. | DENIED | arrest warrant, attenuated evidence |

This is the first time the project has joined **court-derived outcomes** (a
target no rubric authored) to **rubric-coded features** for the same cases. The
pipeline works.

## The result that matters: the atlas finding is NOT robust

The headline v6.2 result was that double cancellation is **VIOLATED** on Priv×Excp
in the 44-case atlas — evidence against additive structure. Adding just these 6
court-derived cases **flipped it to SATISFIED** (0 violations, combined n=50).

A conclusion that reverses when you add six cases is not a conclusion. It is a
small-n artifact. The honest takeaway is the opposite of reassuring: **we cannot
yet tell whether privacy and exception strength combine additively, and the
earlier "falsified" claim was fragile.** This is the single strongest argument
for scaling the corpus before trusting any axiom verdict.

## Two more honest findings

1. **A coding-definition bug surfaced.** `dominance[op_exigency]` came back
   VIOLATED because Beasley fired the exigency operator yet was GRANTED. Reason:
   in Beasley exigency was *claimed and rejected*. So the operator is ambiguous
   between "exigency invoked" and "exigency upheld." That ambiguity must be
   resolved in the rubric before the operator means anything. Inter-rater
   reliability would have caught this; one coder did.

2. **Absorption is still untestable.** As with the atlas, no pulled case has
   Priv≈0 or Rem≈0. Cases with a genuinely absent privacy interest must be
   sought deliberately; they do not show up in a generic suppression search.

## The caveat that limits all of the above

The unit coding here was **single-coder and outcome-aware** — the same author read
the disposition and coded the units. That risks unconsciously coding features to
fit the known outcome, which would inflate any apparent structure. So even the
"predictive-mode" framing is compromised at n=6. Before these cases support any
claim, the coding must be redone **blind to the holding**, by **multiple coders**,
with reliability reported.

## Next steps, in order

1. **Scale the pull.** Hundreds of cases, balanced grant/deny, via the connector.
2. **Freeze a blind-coding rubric.** Code units from the facts section only,
   never the holding; resolve the exigency invoked-vs-upheld ambiguity first.
3. **Re-run the suite at n in the hundreds.** Only then does VIOLATED/SATISFIED
   on double cancellation mean something.
4. **Hunt zero-privacy cases** (abandonment, open fields, third-party exposure)
   to finally exercise absorption.
5. **Commit the boundary-equilibrium inputs** (the currency + the on-the-line
   cases) to convert the 18 coefficients from stipulated to solved.

## Reproducibility

CourtListener opinion IDs used: Smith 11341931, Times 11347766, Moore 11347119,
Beasley 11343851, Hoover 11347237, Hayes 11341887. Search: opinions, query
"motion to suppress evidence Fourth Amendment warrantless search", newest first.

---

# Update — dataset v1 (9 court cases, v1 blind rubric)

## Methodology fix
Froze `CODING_RUBRIC_v1.md`: code the 12 units from the FACTS section only, read
the holding afterward, never revise. Resolved the operator ambiguity — flags mean
**present-on-the-facts, not upheld** — and accordingly **retired the
exigency-dominance axiom** (mere invocation should not dominate). Honest limit:
appellate opinions state the result in paragraph one, so single-pass blindness is
only partial; full blinding needs a facts-only extract or a second coder.

## Added three zero/low-privacy cases (to exercise absorption)
- **State v. Olive** (Ohio) — driver disclaimed ownership of a locked safe; no
  standing; **DENIED**. A genuine Priv≈0.05 case.
- **United States v. Watkins** (10th Cir.) — observation through a 1-inch curtain
  gap from a public walkway; **DENIED**. Low privacy (≈0.20), not zero.
- **People v. Diaby** (N.Y.) — ghost gun discarded in flight; contested
  abandonment; **PROCEDURAL** (remanded for a hearing), excluded from binary tests.

## Result: absorption finally RUNS — but is barely exercised
`absorption[Priv]` came back **SATISFIED** (all near-zero-privacy cases avoid
GRANTED), but on only 2 cases at 22% coverage, one of them procedural. Olive is
the lone clean binary zero-case. So: consistent with the axiom, not yet a test.

A structural finding emerged in the hunt itself: **clean Priv≈0 grant/deny cases
are rare.** No-standing cases resolve uniformly (denied), and contested-
abandonment cases get remanded (Diaby). To actually test absorption you need
zero-privacy cases that vary in outcome — which the doctrine may simply not
produce, itself a fact about the structure.

## Small-n instability persists (the running theme)
At n=9, `independence_of_basis` flips to VIOLATED (4 collinear pairs) — but it is
SATISFIED at n=44 (worst |r|=0.74) and n=50. The n=9 violation is noise.
`double_cancellation` is INSUFFICIENT at n=8. Every verdict here remains
data-fragile; nothing is settled until the corpus is an order of magnitude larger
and coded blind by multiple coders.

---

# Update — boundary-equilibrium currency (Suppression Potential Phi)

## The commitment
Named the conserved currency: **Phi = +Priv +Rem -Excp -Scope - tau**, a signed
scalar whose zero level is the reasonableness boundary (Phi>0 -> granted,
Phi<0 -> denied). Signs fixed by doctrine (privacy/remedial proximity push toward
suppression; exception strength/scope fidelity toward admission) — a falsifiable
choice. Added one boundary case (Kopp, Md.) so four court-flagged-close cases
(Times, Hayes, Diaby, Kopp) pin Phi=0 and the weights are SOLVED, not fit.

## The result: a perfect sort that the machinery flags as HOLLOW
Solving Phi=0 across the 4 boundary cases and testing on the 6 clear cases:

- Phi sorts the clear cases **6/6 (100%)** vs a 67% majority baseline.
- BUT the solved weights are **doctrine sign-INCONSISTENT**: every weight came
  out with the wrong sign (Priv -0.25, Rem -6.96, Excp +1.33, Scope +6.88) —
  privacy *reducing* suppression, exception strength *increasing* it. Doctrinally
  impossible.

The 100% is an artifact. Four self-coded boundary cases give a 4-weights-plus-tau
system enough freedom to separate six points coded by the same outcome-aware
hand, regardless of sign. The built-in sign check caught it: **the falsification
machinery worked, and reported its own result hollow.** This is the v6.2
discipline (rubric imitation != validity) operating at the coefficient level.

The synthetic test (`test_currency_solver_recovers_known_structure`) confirms the
solver DOES recover correct, sign-consistent weights from clean data — so the
hollowness is in the data, not the code.

## What would make it real
1. **Overdetermine it.** Many more boundary cases than unknowns, so the weights
   are forced. Then sign-consistency becomes a genuine pass/fail, not free.
2. **Blind, multi-coder units.** So a high sort-rate reflects structure, not the
   coder's memory of the outcome.
3. **Then** the solved weights replace the 18 stipulated coefficients — and only
   if they come back sign-consistent AND sort held-out clear cases.

Run it: `python -m synthium currency`.
