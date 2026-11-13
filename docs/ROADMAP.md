# ROADMAP — closing the audited gaps (2026-07-13)
Ordered by leverage: each item names the gap it closes and the decision rule.

## 0. USER ACTION — reconnect CourtListener (free)
Unblocks: the owed clean test (C7), Menard resolution (C5), early-register rebuild (C4),
and all domestic volume below. Single biggest unblock; nothing else touches it.

## 1. BUILD: mechanical blinding — ✅ BUILT 2026-07-13 (synthium/blindprotocol.py, 4 tests; first live commit logged)
The deepest protocol weakness is that one agent reads whole documents, so "blind" has
depended on my honesty about reading order. Fix: a fetcher that PROGRAMMATICALLY
truncates the disposition before I ever see the text —
  - CN judgments: cut at 判决如下/裁定如下 (facts 经审理查明 + reasoning 本院认为 kept)
  - JP judgments: strip the leading 主文 block, keep 理由 up to the outcome paragraph
  - CourtListener syllabi: strip holding sentences by pattern
Commit coding from the truncated text; reveal the tail; log both halves. Converts
"deterministic-rule grade" into genuine machine-enforced blind for ALL future grabs,
and makes a true blind China/Japan register possible for the first time.

## 2. CAMPAIGN A — the owed clean test (A0's circularity control)
~20 fresh fact challenges, evidence-basis coded from the FACTS SECTION ONLY via the
blinding tool, committed, then revealed. Decision rule: if credibility findings start
falling at any material rate, A0's sharp form dies; if the doc/cred split holds, the
+25±9 db gate is promoted from retrodictive to prospective.

## 3. CAMPAIGN B — settle the stacking vs level-invariance fork
Post-dedupe the fork is fully open (int fact 3/21=0.14 vs apex 2/9=0.22). Target: 40+
deferential-fact challenges PER LEVEL, outcome-neutral queries only. Decision rule:
apex rate materially below intermediate -> stacking wins; equal -> invariance wins;
above -> both die and something new is needed.

## 4. CAMPAIGN C — unit portability (the frontier question)
Is +7.0±2.3 db (law-side gate) a constant of judicial systems or a Connecticut fact?
Step 1: Ohio-only fit (cheapest second point; ~40 rows exist, need ~30 more).
Step 2: one foreign system at volume (UK Privy Council or FR Cassation via LDH, ~60).
Decision rule: gate weights agree within ~2 db -> the deciban scale is portable and
the seam has a MAGNITUDE, not just a direction. Disagree -> weights are local, only
the sign is universal. Either answer is a major result.

## 5. CAMPAIGN D — W per system
W=3/58 is register-wide. Need ~20 movement events per system for per-system W.
Falls out of Campaigns B/C data mostly for free.

## 6. VALUE SKELETON — three mechanical jobs
a) Pricing-of-life index across ~20 jurisdictions (survival vs loss-to-survivors),
   statute-reading via LDH legislation namespace. Tests the lineage prediction
   (Lord Campbell descendants say NO).
b) Iran Book Four (diyat): corpus lacks it — use web_search for the IRANHRDC Book 4
   translation + the compensation-fund gender-parity provision. Live falsifier of
   "the dignity channel is policed toward equality."
c) Real V for R=D/V: UK dependency award data (Judicial College guidelines / reported
   awards) to replace the 300k-1M estimate.

## 7. HOUSEKEEPING
- Rebuild attempts 3-9 as machine rows when CourtListener returns (recover the ~103).
- Resolve Menard coding conflict.
- v4 model: fold the gatekeeping/merits flag into the fitted equation as a feature
  (currently a separate lookup) and give the ruler its first prospective exam since
  attempt 29 — the ruler itself has been idle for ten attempts.
- Reliability: re-code a random 20-row sample in a fresh session blind to prior codes
  (intra-rater check); optionally Sina codes 10 against RULER.md for a true
  inter-rater number.

## 8. E-LAYER event studies (added 2026-07-13)
Run one historical event-study to validate the method before trusting it live:
DNA post-conviction statutes (r up) or an evidence-rule amendment. Then track the
deepfake predictions P1-P4 (ENVIRONMENT.md) as they unfold.

## RESEARCH AIMS (Sina, 2026-11-12, in his words; "the list is more than that")
1. "We wanna see if everything can be math"
2. "if Everything has a mathematical explanation"
3. "to understand if Quality is for when we don't have quantity for a concept"
4. "test and see if something similar to thermodynamic rules can apply the same except with different parameters"
5. "if we can consider this world a game with the limitations that all beings play within these limitations which i call it rules of the game that without them there is no game"
6. "if the same path all other scientists took to explain natural phenomenon such as gravity, speed, acceleration and etc can be taken for abstract concepts"
7. "if Calculus can help us in more explanation"
8. "there are a lot of information on internet that we can gain access too"
9. AI agents, "a new species", can help humans figure these out faster.

### Main hypothesis (testable form of aims 1-3)
H-Q: A quality is a quantity for which no ruler exists yet. Prediction: once a ruler is
built for a qualitative concept, measurements on it are stable across coders and cases
and predict fresh cases better than a naive baseline. Falsified for a concept if no ruler
built for it beats the baseline after a pre-registered blind campaign. Aims 1-2 as worded
cannot fail ("not found yet" absorbs every miss); they are held as motivation, and H-Q is
what gets tested. First instance: appellate deference (Campaign A, 2026-11-12: notch
15/20 vs always-affirm 9/20, facts-section leak caveat).

### Map of aims to work
- Aim 4 -> T1 review barrier (AXIOM_CANDIDATES), pre-registered 2026-11-10.
- Aim 5 -> the universal "physics" layer; first candidate rule A0 (fact findings hold).
- Aim 6 -> path: observe, measure, find invariants, state law, predict. Status: invariants, one concept.
- Aim 7 -> needs a time-varying measured quantity (e.g. deference by year); not tracked yet.
- Aim 9 -> agents make errors too; blind protocol and verified ledger stay mandatory.
