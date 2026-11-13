# Synthium — Public Findings Log

This log states what the project finds, as it finds it, in public, for debate.
Every entry is dated. Misses and null results are stated alongside hits.
Nothing here is a final claim. Challenge anything below — that is the point.

## 2026-11-12 — Campaign A complete: first blind test of A0

### What is being claimed

A0: a reviewing court may revise only what it is positioned to know at least
as well as the court below. In plain terms: a higher court can only change
what it can see as well as, or better than, the court that decided first.

### How it was tested

Twenty appellate cases. For each one, only the facts section of the lower
decision was read. The prediction was written down and sealed (hash-chained)
before the outcome was revealed. Only then was the prediction compared with
what the court actually ruled. The ruler reads three features before the
ruling: T (type of finding), P (posture), L (layer).

### Results

- Notch (the exact slice of the outcome the ruler predicts): 15 of 20 (75%).
- Always guessing "affirmed": 9 of 20 (45%).
- Blind-grade cases only: 12 of 16.
- Layer correct wherever coded: 16 of 16.
- Fact findings, challenged vs disturbed on review: credibility 10 challenged,
  0 disturbed; documentary 8 challenged, 1 disturbed; record-absence 3
  challenged, 3 disturbed.
- No falsifier of A0 found. No case yet shows a higher court revising a
  finding it was not positioned to know at least as well.

### Honest caveats

- The facts sections were written by the deciding court, and several carried
  directional wording ("nevertheless", "overlooked"). The facts scope still
  leaks the court's framing. This needs discussion before any public claim
  goes further than this log.
- A separate deterministic-rule evaluation of the ruler scores 16/19 against
  a 12/19 naive baseline. That is not the blind test above, and the two
  numbers should not be conflated.

### Open phase (same protocol, ongoing)

Three further cases coded blind since Campaign A closed: notch 2 of 3.

### What did not hold up

- The early v1/v2 E-D ruler leaked: E was scored from opinions written after
  the rulings. It was retired.
- A neural-network headline claim was retracted in the V4.3.1 audit.

### What is next

- Non-US cases: the same blind protocol applied to cases from the UK,
  the Netherlands, Canada, and the EU (Campaign B-Muse). No non-US cases
  coded yet; case sources are being connected.
- A thermodynamics-like rule (T1) is pre-registered and needs at least 30
  points per jurisdiction in at least 5 jurisdictions before it says anything.
- Whether to add a sociological domain beyond courts is undecided.

### What would change our mind

A genuine falsifier: a higher court revising a finding it was not positioned
to know at least as well as the court below, with the case cited and the
finding identified. Bring one and the claim falls or narrows.

### How to challenge

Open an issue on this repository, or reply to the announcement post. State
the case, the finding, and where the ruler goes wrong. Vague disagreement
does not move anything; a case does.
