# Changelog

## 2026-11-24: every earlier version brought back, nothing retired

Sina's call: "Don't retire things because we did something wrong ... collectively all the
things that we have done needs to be always under consideration." Every part that 9.0.0
had set aside is back as live, importable code, and every formula, unit, axiom and tool is
listed in one place with its status: under consideration. Results stay UNTESTED.

- `docs/UNDER_CONSIDERATION.md`: the one index. 126 entries from V1 (Dec 2025) to now, each
  with its version, who proposed it where a source says so, what it claimed, why it was set aside at the time, any earlier test
  result, and where it lives now. Generated from `synthium/phenomena/catalogue.py`; a test
  keeps them in step. It includes the formulas Claude proposed, among them Fear of Loss =
  Connection x Possibility x Powerlessness from a Jan 2 2026 dialogue with Sina (text only),
  and Sina's Nov 26 convention that every being is a structure of balanced forces.
- `synthium/legacy/`: V1/Omega 1.5, V2, V3.4 (the combined script), V4, V4.3.1 (spec,
  rubric, dataset, governance, the 2,045-line monolith and the trained neural encoder
  weights), V5 honesty, V6 predictive and CourtListener labeler, V6.1 (the 12-unit
  formula), V8's atlas loader and July blind protocol, and SynthiumBot. Original code; the
  only changes are imports and data paths so they work inside one package, each marked
  `RESTORED 2026-11-24`. SynthiumBot's settings file held a live Telegram token, so it was
  left out and `config.py` reads `TELEGRAM_TOKEN` from the environment (a reconstruction).
- `synthium/phenomena/`: the phenomenon framework. Each old phenomenon (14 V2 profiles plus
  the V1 and V2 lexicon entries) sits on its own five dimensions and every old formula runs
  on it. On real case scores it asks: is a quality a base dimension or made from others; if
  made, by sum, product, weakest part, strongest part or strict priority; and does any mix
  of qualities stay balanced (Sina's building, axiom G9). `python -m synthium.phenomena
  CASES.csv --out DIR`.
- `archive/v2_2_to_v3_4_pdf/` and `_text/`: the original V2.2 to V3.4 PDFs and their text.
  `archive/originals_docs/`: the V4.3.1, V6, V6.1, V7 and V8 docs that 9.0.0 had dropped,
  unchanged (including `RETIRED.md` itself, as a record).
- `tests/test_legacy.py`, `tests/test_phenomena.py`, `tests/test_legacy_v8_blindprotocol.py`.
- New extras: `legacy`, `legacy-neural`, `legacy-bot`.
- The lineage table and "Set aside in 9.0.0, and why" below now say restored and under
  consideration instead of retired.
- Not copied: the SRIA RT files (judged "not Synthium" in 9.0.0; they look like Maysam's
  work). They stay on Drive.
- No change to the ruler, the ledgers, or any existing result.

## 2026-11-24: geometry and calculus brought back (`synthium/geometry/`)

Sina's call: the V4 maths (manifold geometry, tensor calculus, dimensional discovery)
should not have been retired with the word counts that fed it. It is back, fed with the
case quality scores. Every result it gives is marked UNTESTED.

- `archive/v4_original/`: the original V4 code, byte for byte from `Synthium.zip` on
  Drive, with `ARCHIVE_NOTE.md` on what it really did (constant metric, so its curvature
  was always zero; nested 1e-6 derivatives that return noise past the third order).
- `synthium/geometry/` (numpy only): cases as points, qualities as dimensions, the number
  of dimensions not fixed in advance. Dot to line to area to volume build-up; a test of
  whether a quality is a new dimension or a combination of others; PCA against shuffled
  data; Mahalanobis metric; paths along the cases and a curvature index against shuffled
  data; a metric that varies from place to place with real Christoffel symbols, Riemann
  tensor and scalar curvature (checked on a sphere); tensors of any rank; rates of change
  along reading order or filing date; case paths between stages; a loader for any
  domain's table and a shared-versus-own dimension comparison.
- `python -m synthium.geometry CASES.csv --out DIR` writes a plain-language report.
- `tests/test_geometry.py`: 29 tests on cases with known answers.
- No change to the ruler, the ledgers, or any existing result.

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
| V2 / "Omega" | Dec 2025 | keyword quantifier: counted words into five dimensions, printed "formulas" | set aside in V6.1; restored 2026-11-24 (`synthium/legacy/omega_v1_5`, `legacy/v2`), under consideration |
| V2.2 to V3.4 | Jan to Mar 2026 | PDF-only "discovery" corpus (field, units, vectors, ethics/empirical discovery); V3.4 also an 1,800-line combined script | set aside in V6.1; restored 2026-11-24 (`legacy/v3_4`, PDFs in `archive/v2_2_to_v3_4_pdf/`), under consideration |
| V4 | Apr 2026 | package: confidence, manifold geometry, tensor calculus, dimensional discovery, reality state | set aside in V6.1; restored 2026-11-24 (`legacy/v4`, extended in `synthium/geometry/`), under consideration |
| SynthiumBot | Apr 2026 | Telegram bot wrapping the V4 "Omega" engine | set aside with V4; restored 2026-11-24 (`legacy/synthiumbot`, token left out), under consideration |
| V4.3 / v4.3.1 | May 2026 | adds judicial spec, rubric, dataset, PyTorch encoder, governance; 2,045-line monolith | set aside in V6.1; restored 2026-11-24 (`legacy/v4_3_1`, with weights), under consideration |
| V5 | May 2026 | "honesty" single file: refused unlicensed arithmetic (froze the project) | idea kept; code restored 2026-11-24 (`legacy/v5`), under consideration |
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

### Set aside in 9.0.0, and why

Everything in this list was restored on 2026-11-24 as live code in `synthium/legacy/`
(see the top entry) and is under consideration. The reasons below are why each part was set
aside at the time; they are kept as the record, not as a final verdict.


- Omega keyword quantifier, V3.x PDF corpus, V4 geometry/tensor/dimensional-discovery
  modules, the v4.3.1 monolith, governance engine, V5/V6 single files: set aside in V6.1
  because they presented unvalidated numbers and pseudo-physics as measurement.
- Neural encoder and its trained weights (V4.3): its headline accuracy was a leakage
  artifact and it only imitated rubric labels. The project decided it could return only
  as an optional extra once a court-derived dataset exists. The empty `neural` and
  `discovery` extras in V8's pyproject were removed because no code used them.
- SynthiumBot: a chat front end for the V4 engine, set aside with it.
- 12-unit judicial formula and spec (V6.1): removed in V7; the units were never validated
  and made axiom tests circular.
- `synthium/data/atlas.py` and the 44-case suppression atlas CSV, `courtlistener_cases_v0.csv`:
  V8 kept them only as "legacy reference data"; nothing used them, and the atlas is coded
  in the 12 units removed in V7.
- July blind protocol's commit/reveal log code: superseded by the November protocol.
- `setup.py`, `requirements.txt`, `CONTENTS.md`, the V8 README: replaced by `pyproject.toml`
  and this folder's README.
- Docs of the set-aside era (`AXIOMS.md`, `CODING_RUBRIC_v1.md`, `EMPIRICAL_STATUS.md`,
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
