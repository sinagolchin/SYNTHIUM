# Running the CourtListener pull

The labeling pipeline (`synthium/data/courtlistener.py`) is verified offline
(`python -m synthium courtlistener-selftest` → ALL PASS). The live pull could
not be run from the build sandbox: its network blocks courtlistener.com (HTTP
403). Run it on your machine.

```bash
export COURTLISTENER_TOKEN="your_token"        # free, from courtlistener.com
python -m synthium build-dataset --max 200 --out cases.jsonl
```

This writes one JSON line per case: the court-derived outcome
(SUPPRESSION_GRANTED / SUPPRESSION_DENIED / …), the text, and the extractor's
confidence. **These labels are a first-pass read of the record — hand-check a
sample before trusting them as ground truth.**

## The bottleneck you must decide on next

CourtListener gives the *target* (outcome). The axiom suite also needs the
*features* — the 12 unit values — for those same cases. Today those exist only
for the 44 hand-coded atlas cases. So to test the axioms on court-derived
outcomes, each pulled case needs its units coded. Three options:

1. **Hand-code** a few dozen pulled cases against the rubric. Slow, highest quality,
   lets you measure inter-rater reliability.
2. **LLM-code** with a fixed, frozen rubric prompt, then hand-check a sample to
   measure the coder's reliability. Faster; reliability must be reported.
3. **Outcome-only first.** Validate a text→outcome model (no units) against the
   majority baseline to confirm there is *any* learnable signal, before investing
   in unit coding.

Whichever you choose, keep features and target strictly separate (no leakage),
and freeze the coding procedure before seeing outcomes. Option 3 is the cheapest
honest next step; option 1 on ~30 cases is what unlocks the real axiom test.
