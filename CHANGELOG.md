# Changelog

## 2026-11-12: research data added by the daily runs (package still 9.0.0)

No code changed; the 59 tests are the same. The daily research runs now work in the
Google Drive copy of this folder and add their results to it. Added since 9.0.0:

- `data/VERIFIED_LEDGER.csv`: 15 rows to 35 (34 confirmed, 1 partial); the 20 new rows are the
  Campaign A cases.
- `data/campaign-a/`: Campaign A, the owed blind test, complete at 20 of 20 cases:
  15/20 outcome notches vs 9/20 always-affirm (16 fully blind cases: 12/16 vs 9/16).
  Holds the hash-chained `blindlog.jsonl`, the sealed full texts and `PROGRESS.md`.
- `data/case_details/campaign-a/`: one note per Campaign A case.
- `data/T1_POINTS.csv`: data for the pre-registered T1 review-barrier candidate;
  83 points from 6 jurisdictions as of Nov 12.
- `docs/AXIOM_CANDIDATES.md`: updated by the runs (the Greene rival draft).
- `PROPOSALS.md` now sits at the top of the folder. P2 (directional party columns in
  `T1_POINTS.csv`) was added; P1 is summarized at the end of the 9.0.0 entry below.

## 9.0.0 (2026-11-11): one merged codebase

Every Synthium version from V2 (Dec 2025) to V8 (Jul 2026), plus the November 2026
work, merged into this single package. Nothing about the ruler's rules, its coefficients,
the case coding or the ledgers was changed; `python -m synthium ruler-eval` gives the same
16/19 vs 12/19 as V8, and all 576 combinations of the ruler's inputs give byte-identical
predictions and probabilities before and after the clean-up.

### Version lineage (what each one was)

| Version | Date | What it was | Fate |
|---|---|---|---|
| V2 / "Omega" | Dec 2025 | keyword quantifier: counted words into five dimensions, printed "formulas" | retired (V6.1) |
| V2.2 to V3.4 | Jan to Mar 2026 | PDF-only "discovery" corpus (field, units, vectors, ethics/empirical discovery); V3.4 also an 1,800-line combined script | retired (V6.1) |
| V4 | Apr 2026 | package: confidence, manifold geometry, tensor calculus, dimensional discovery, reality state | retired (V6.1) |
| SynthiumBot | Apr 2026 | Telegram bot wrapping the V4 "Omega" engine | retired with V4 |
| V4.3 / v4.3.1 | May 2026 | adds judicial spec, rubric, dataset, PyTorch encoder, governance; 2,045-line monolith | retired (V6.1) |
| V5 | May 2026 | "honesty" single file: refused unlicensed arithmetic (froze the project) | idea kept, code retired |
| V6 | Jun 24 2026 | predictive harness: propose then validate, plus the CourtListener labeler | became `core/` and `data/` |
| V6.1 | Jun 25 2026 | first clean package: core, data, cli, 12-unit judicial formula | core kept; 12 units removed in V7 |
| V7 | Jun 29 2026 | 12 units removed; generic axiom tests; citation space | kept |
| V8 | Jul 2026 | the T/P/L ruler, fitted probability models, July blind protocol | kept; base of this version |
| Nov 2026 | Nov 10 2026 | rebuilt blind protocol (22 tests), 9-case batch, verified ledger to 15 rows, T1 axiom | kept |

### Where each part of this package came from

- `synthium/core/` (values, baseline, validation, axioms): V8, unchanged in behavior. Stale
  version references in docstrings removed.
- `synthium/data/courtlistener.py`: V8. Now also reads `COURTLISTENER_API_TOKEN`.
- `synthium/domains/judicial/ruler.py`: V8 (identical to the top-level `ruler.py`). Clean-up:
  the fitted-model section loaded JSON with unclosed files, a module-level global, repeated
  imports and a second copy of the posture table; it now uses one cached loader and the
  ruler's own `P_PROTECTION`. Outputs verified identical.
- `synthium/domains/judicial/params/`: the three frozen fits from V8 (`fitted_params*.json`).
  `fitted_params_v3_dismissal.json` is a recorded result that no code reads yet.
- `synthium/domains/judicial/citation_space.py`: V7/V8, unchanged.
- `synthium/blind/protocol.py`: the November 10 rebuild (was `tools/blindprotocol.py`), now
  run as `python -m synthium blind ...`.
- `synthium/blind/classify.py`: the Chinese tenor classifier from the July 13 original blind
  protocol, recovered from the old project. Also accepts the full-width comma.
- `synthium/paths.py`, `cli.py` additions: new. One place decides where `data/` is
  (`SYNTHIUM_DATA` overrides it). The CLI gained `--level`, `--register`,
  `courtlistener-selftest` and `blind`, and the V8 docstring's commands that didn't exist
  are now real.

### Data and docs: which copy won

- Ledgers, case list, and most docs: the current files (Nov 10-11 2026), which were newest.
  `VERIFIED_LEDGER.csv` has 15 rows; the V8 copy had 6.
- `AXIOM_CANDIDATES.md`: the current merged file (July A0/A1/A2 sections plus T1).
- `CROSS_BORDER.md`, `MATH_CANDIDATES.md`, `STATUS.md`, `METHOD.md`: the July 16 V8 copies,
  because they contain everything in the current files plus sections the current files had
  lost (attempt 38, China; the deciban units section; the audit note; blind protocol v1).
- Blind registers: all 15 from the V8 package. `blind_register_foreign.csv` is the later
  copy, with a `grade` column and the attempt-38 row.
- `EXCLUSIONS.csv`, `case_details/`, the July blind log: from the V8 package. The November
  batch notes and the blind dry run: from the November work.
- `docs/BLIND_PROTOCOL.md` is the tool's README, with commands updated.
- `docs/ARTICLE_a_ruler_for_judgment.md`: the July 16 open research note, the last thing
  made in the old project.

### Known gaps in the recovered July copies

- The old project's `PREDICTIONS_REGISTER.md` was 89,600 bytes; the only copy anyone could
  read is the 85,217-byte one used here, so about 4 KB of the July register may be missing.
- A few July files could only be transcribed, with some characters normalized: the attempt-38
  section of `CROSS_BORDER.md`, the July classifier (both comma forms are now accepted), and
  the sealed CN excerpt in `data/blind_log_2026-07/` (its hash will not match the July log).

### Dropped, and why

- Omega keyword quantifier, V3.x PDF corpus, V4 geometry/tensor/dimensional-discovery
  modules, the v4.3.1 monolith, governance engine, V5/V6 single files: retired in V6.1
  because they presented unvalidated numbers and pseudo-physics as measurement.
- Neural encoder and its trained weights (V4.3): its headline accuracy was a leakage
  artifact and it only imitated rubric labels. The project decided it could return only
  as an optional extra once a court-derived dataset exists. The empty `neural` and
  `discovery` extras in V8's pyproject were removed because no code used them.
- SynthiumBot: a chat front end for the retired V4 engine.
- 12-unit judicial formula and spec (V6.1): removed in V7; the units were never validated
  and made axiom tests circular.
- `synthium/data/atlas.py` and the 44-case suppression atlas CSV, `courtlistener_cases_v0.csv`:
  V8 kept them only as "legacy reference data"; nothing used them, and the atlas is coded
  in the retired 12 units.
- July blind protocol's commit/reveal log code: superseded by the November protocol.
- `setup.py`, `requirements.txt`, `CONTENTS.md`, the V8 README: replaced by `pyproject.toml`
  and this folder's README.
- Retired-era docs (`AXIOMS.md`, `CODING_RUBRIC_v1.md`, `EMPIRICAL_STATUS.md`,
  `RETIRED.md`, `UNITS_REMOVED.md`, old changelogs, `PROJECT_INSTRUCTIONS.md`): the reasons
  that mattered are summarized above.
- Not Synthium: the SRIA RT files, the SRIA V3 paper, the SCK adaptive-CUSUM paper and three
  court opinion PDFs that were inside the iCloud export.

### Tests

59 tests (20 ruler and core tests and 4 classifier tests from V8, 22 from the rebuilt protocol, 13 new package and CLI tests): the ruler's rules and its eval
numbers, the fitted models, the core gate and value logs, the CourtListener extractor,
citation space, the blind protocol, the CN classifier, data files, and every CLI command.

### Found while merging (not changed; see ../PROPOSALS.md, P1)

Five register rows use values outside the ruler's vocabulary (`child`,
`procedural_integrity`, three blank postures), and the foreign register calls its court
level column `court_tier`, so the scorer reads its apex rows as intermediate.
