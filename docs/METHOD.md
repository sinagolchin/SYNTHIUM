# The Synthium method (what actually worked)

1. **Propose units** — candidate measures for the qualitative thing.
2. **Leak audit** — a unit is admissible only if it can be read BEFORE the outcome
   exists. (Our first ruler failed this: "error clarity" was scored from opinions
   written after the ruling, r=+0.99 with the verdict. Retired.)
3. **Commit blind** — every prediction is written down before the outcome is read.
   No exceptions. A prediction not committed in advance does not count.
4. **Let reality edit** — each case either KEEPs or CHANGEs a unit/formula, logged.
   (Hartford forced the override; Brown sharpened E; Bernblum split fact from law;
   attempt 10 fixed the paper zone; attempt 11 split remedy into estimate/calculation.)
5. **Beat the honest baseline** — a rule "works" only if it beats the naive guess
   (always-affirm) on committed, representative cases.
6. **Audit every perfect score** — perfect fits are treated as symptoms (we caught
   two: the E leak, and the sign-inverted currency solve).

---

# MECHANICAL BLIND PROTOCOL v1 (built 2026-07-13; synthium/blindprotocol.py)

> Note (2026-11-11): v1's commands below are superseded by `python -m synthium blind` (docs/BLIND_PROTOCOL.md).
> Its tenor classifier lives on in `synthium/blind/classify.py`; its July log is in `data/blind_log_2026-07/`.

Enforcement is at FETCH level, not trust level:
1. SEARCH with outcome-neutral facts-language queries (no disposition verbs).
2. FETCH with include_full_text=false -> leading ~2KB. Chinese judgments are strictly
   linear (facts -> reasoning -> disposition at END), so the leading excerpt is
   machine-guaranteed disposition-free.
3. COMMIT via `python3 -m synthium.blindprotocol commit ...` — timestamped, excerpt
   SHA-256 hashed, sealed copy archived, TAINT DECLARATION recorded (what the search
   snippet showed).
4. FETCH full text; REVEAL via the tool — a lexicon classifier extracts the tenor
   (维持原判->CLEAN_AFFIRM, 撤销/发回->REVERSED, 改判->MODIFIED, else AMBIGUOUS ->
   manual review) and records hit/miss.

Guarantees & limits (stated): order is provable from the log + the fetch mechanism;
snippet taint is declared per-case, tainted rows grade 'disclosed'; Japanese judgments
(tenor-first) are OUT OF SCOPE for this protocol; classifier ambiguity blocks
auto-scoring. 4 classifier unit tests in tests/test_blindprotocol.py.
