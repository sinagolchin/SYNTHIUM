# Synthium — the whole story on one page (updated after 119 blind cases)

> **Note (Nov 13 2026):** this page dates from July 2026 and its case counts (119, 171) are historical. The current numbers, and which count is authoritative, are in the README under "Numbers at a glance".

**The goal:** build rulers — real measuring sticks — for things people judge
without math. Test domain: judicial decisions (criminal, civil, administrative).

**Chapter 1 — the fake success.** The first ruler (E = "how wrong was the lower
court", D = "how protected is its decision") fit 18/18 cases. It was a cheat we
caught ourselves: E was scored from opinions written AFTER the ruling, so it
correlated +0.99 with the answer. It measured the verdict, not the case. Retired.

**Chapter 2 — the honest restart.** New rule: every prediction is written down
BEFORE the outcome is read. 119 cases have gone through this locked register.

**Chapter 3 — three real discoveries (all readable before the ruling):**
1. **TYPE** — criminal / prisoner / child-protection appeals almost never get
   overturned; ordinary civil appeals do about 1 time in 3.
2. **POSTURE** — decisions made after a full trial are armored; decisions made
   "on paper" (case thrown out on a motion) are where reversals live.
3. **LAYER** — inside any case: fact-findings almost never flip; what flips is
   the legal/remedy scaffolding bolted on top (standing, statute readings,
   damages formulas).

**Chapter 4 — the ruler (v3.2) and its record.** Units T (type), P (posture),
L (layer). Core rule: *facts survive; separable legal overlays move; type sets
the appetite.* On committed-before-reveal notch predictions the ruler is
**16/19 (84%) vs the always-affirm baseline's 12/19 (63%)** — its entire edge
comes from correctly calling "the trial's facts will stand but that legal layer
will move," which the baseline cannot see at all.

**Still open / honest limits:** one jurisdiction (Connecticut) so far; one coder;
the newest two refinements (pure-law cases just affirm; remedy-as-estimate is
protected, remedy-as-calculation moves) were induced from the last batch and
still owe their exam on fresh cases; published opinions over-represent
interesting cases.

**Next:** test v3.2 on fresh batches, then a second jurisdiction, then a second
domain entirely — the real thesis is that this same method (propose units →
commit blind → let reality edit) can measure ANY qualitative concept.

## Cross-border (new): the fact/law seam is not just Connecticut
France (Cour de cassation) and Germany (Revision) both hardwire "facts bind,
only law moves" at their top courts — same seam the ruler found in CT. Confirms
the ruler measures a real, recurring court ARCHITECTURE (see CROSS_BORDER.md).
Caveat: strongest at law-only supreme courts (true by design); the quantified
test is intermediate fact-reviewing courts abroad. Connectors now in use:
CourtListener, Trellis, Legal Data Hunter (200+ jurisdictions); Descrybe,
Courtroom5 available next.

## Axiom candidates (new): Sina's three, formalized
Trajectory-toward-enjoyment (blocked: needs an enjoyment ruler first — circular
as written), non-interference (split: value-target vs testable claim that courts
price interference — consistent with all 130+ logged cases), preservation-floor
(false for individuals, strong as "law ranks life at the top; its exceptions map
a society's value hierarchy"). Set audit: A1/A3 conflict forces an exchange rate;
jointly they form objective+constraint+floor — a constrained optimization whose
violation surface IS the judicial data. See AXIOM_CANDIDATES.md.

## Audit 2026-07-10
Full audit run at Sina's request. Corrections: Stafford excluded (unverified),
A16 = 4/6 tie; abandoned A16 batch marked VOID; lifetime fact-seam claim corrected
(2 override-mediated fact reversals in A3; "armored except via override" is the law);
evidence grades declared (strong-blind vs deterministic-rule); audited lifetime
total = 171 committed cases. Details: docs/AUDIT_2026-07-10.md.
