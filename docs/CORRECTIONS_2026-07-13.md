# CORRECTIONS — full audit, 2026-07-13
Nothing below is deleted from prior logs; corrections are appended, per project rule.

## C1 — HALLUCINATION, RETRACTED & REPLACED (Japan, Sup. Ct. 1973, case 62099)
CLAIMED (attempt 39, chat only, never logged): judgment voided because "the judge who
decided was not the judge who saw" — labeled 直接主義 and called A0's best confirmation.
FULL TEXT NOW READ. **The claimed ratio is false.** Actual holding: Judge Shiraishi
closed argument (Feb 1967), was TRANSFERRED (転補) on 10 Apr 1967; the judgment original
bearing his signature was created AFTER transfer (proven by the paper stock's Jan 1969
print marking). Rule: after transfer a judge "cannot perform acts as a judge of the
former court" -> procedure unlawful -> reversed. **This is an OFFICE/COMPETENCE rule —
supports A1 (right forum/office), NOT A0 (access).** The 直接主義 framing was supplied
from background knowledge, not the text. RETRACTED.
Seam note (verbatim, verified): the Supreme Court then decided the case itself "in
light of the facts lawfully determined by the appellate court" (原審が適法に確定した
事実関係) — facts preserved; movement entirely law/procedure-side. Seam held.
VERIFIED Japan finding that stands: in 3 separate judgments (68175, 61396, 50796),
verbatim: claims of 事実誤認 (factual error) "do not constitute grounds for final
appeal under CCP Art. 405" — a STATUTORY BAR on fact review at the apex. Strongest
form of the seam: jurisdictional, not deferential.

## C2 — PROTOCOL VIOLATION: China & Japan "blind commits" were not blind
Search snippets contained the dispositions (棄却/破棄/予以确认) before the "commits."
RELABELED as structural observations (grade=disclosed). The structural findings stand
on the courts' verbatim language; they are not prediction evidence. The foreign CSV now
carries a `grade` column: disclosed / uncertain_exposure / likely_blind_miss (the two
MISSES — Ackland, OLG Hamm — are the only commits PROVEN real, precisely because they
were wrong).

## C3 — FOREIGN NOTCH SCORE IS BASE RATE, NOT SKILL
All 11 foreign commitments were CLEAN_AFFIRM (a constant predictor). Notch 9/11 = the
base rate; carries zero information about the ruler. What the foreign register
legitimately shows: the SEAM held 11/11 (structural, verified in each system's own
doctrinal language). Stop citing foreign notch scores.

## C4 — COUNT CORRECTED: "263" -> 148 verifiable
Machine-readable unique rows after dedupe: **148**. The remainder (~100+, attempts 3-9
pre-CSV, attempt-23 exam 6, attempt-30 5) exist in prose logs only and are UNVERIFIABLE
this session. Citable number: **148**. The frozen v1 19-row record still reproduces
(ruler-eval: 16/19).

## C5 — DUPLICATE: Menard v. State (v1 attempt-10 = attempt-28)
Same case+notch, CONFLICTING codings (layer remedy_calculation vs fact; level
intermediate vs apex). v1 kept as canonical; attempt-28 copy EXCLUDED from all pooled
stats (data/EXCLUSIONS.csv). Coding conflict unresolved pending CourtListener re-auth.

## C6 — HEADLINE FINDING WEAKENED BY DEDUPE: level-invariance is NOT established
Attempt-29 claimed fact-channel level-invariance "0.14 -> 0.14 exactly." That exact
equality was partly an artifact of the Menard duplicate + smaller pool. Deduped and
current (148 rows): intermediate fact-side 3/21 = 0.14; apex fact-side 2/9 = 0.22.
No exact invariance; tiny n; even the direction is unstable. **The stacking-law vs
level-invariance fork is FULLY OPEN.** What remains robust: fact-side << law-side at
BOTH levels (0.14/0.22 vs 0.34/0.51), and W = 3/58 = 0.052 (when a case moves, ~95%
of the time it is the law that moved — now incl. Rose as a fact-disturbance).

## C7 — PRE-REGISTERED CLEAN TEST STILL OWED (attempt 30)
The documentary/credibility facts-only prospective coding test was promised and never
run. It remains THE outstanding test of A0's sharpest claim (circularity control).
Requires CourtListener re-auth (staged facts-then-holding reading); LDH full-text
fetches cannot credibly stage. NEXT ACTION once reconnected.

## Standing rule going forward
No "blind" label unless the disposition was demonstrably absent from everything read
pre-commit. No ratio decidendi cited without the full text in-session. Counts cite
machine rows only.

## C8 — Wang blind commit VOIDED (attempt 40 -> 42)
Reveal inconclusive: the retrieved full text terminates before the 判决主文, so the
classifier returns AMBIGUOUS (protocol correctly blocks auto-scoring). Independently, the
full text revealed a prosecutorial 抗诉 (appeal to OVERTURN) — meaning my commit-stage
taint declaration MIS-CODED the posture as defendant-only (sentence-can't-worsen). Commit
VOIDED on two independent grounds. Lesson: the taint declaration must positively identify
抗诉/appellant identity from the excerpt, or grade 'posture-uncertain'. Protocol updated
mentally; first true scored blind still owed. This is the protocol working — it refused
to let me score a prediction built on an incomplete reading.

## C9 — CN blind register BLOCKED by source structure (attempt 42), honest stop
The mechanical protocol needs raw judgments whose retrieved text CONTAINS the 判决主文
(so the reveal classifier can read the tenor) but whose leading 2KB EXCLUDES it (so the
commit is blind). Available CN sources fail this from both ends:
  - CAIL2018 (raw 2nd-instance judgments): records TRUNCATE before the 判决主文 (Wang) ->
    reveal impossible.
  - SPP/SupremeCourt 典型案例/指导性案例: curated digests; "outcome" is a summary
    (裁判要点), not a parseable disposition, and the excerpt often already states it ->
    commit not blind.
Therefore: NO scored CN blind case is achievable on current connectors. The protocol is
sound; the DATA SOURCE is the blocker. This is logged as a limitation, not worked around.
The genuine path (ROADMAP #1/#2) needs CourtListener reconnected (US syllabi stage
cleanly) OR a raw-judgment CN source (e.g. full 裁判文书网 texts) not currently available.
Standing decision: do not manufacture CN blind cases from digests; wait for a source that
structurally permits blinding.
