# Synthium

**The idea (Sina's):** things people judge by feel, like fairness, harm and wrongdoing,
might be measurable. Synthium builds rulers for them and tests the rulers against
reality. The test domain is judicial decisions: judges decide enormous things with no
measuring stick, and courts publish millions of decisions.

**Where it stands:** a working ruler for appellate outcomes, with three units that are
all readable before the ruling:

- **T (type):** criminal, prisoner and child-protection appeals almost never overturn; civil about 1 in 3.
- **P (posture):** decided after a real trial is armored; decided on paper is fragile.
- **L (layer):** fact-findings almost never flip; the legal layer on top is what moves.

The committed-before-reveal record is 16/19 correct outcome notches against 12/19 for
the always-affirm baseline. The fact/law seam shows up in 11 legal systems on 5
continents. Depth is still one jurisdiction (Connecticut coefficients), one coder, and
the newest refinements still owe a prospective exam. See `docs/STATUS.md`.

**Campaign A (the owed blind test), finished Nov 12 2026:** 15/20 correct outcome
notches against 9/20 for always-affirm; on the 16 fully blind cases, 12/16 against 9/16.
Caveat recorded with it: the facts sections are written by the deciding court and can
leak its framing. Details in `data/campaign-a/PROGRESS.md`.

This folder is the one current version of Synthium: code, data and research notes.
Every earlier version (V2 to V8) was merged into it; `CHANGELOG.md` says what came from
where and what was dropped. The daily research runs work in this Google Drive folder and
save their results here, so it is always the latest copy.

## Layout

```
PROPOSALS.md               changes waiting for Sina's yes (nothing in it is applied)
synthium/                  the package (standard library only)
  core/                    values with assumption logs, baselines, the validation gate, axiom tests
  data/courtlistener.py    labels real court records with rubric-independent outcomes
  domains/judicial/        the T/P/L ruler, frozen fitted models (params/), citation space
  blind/                   the blind protocol (protocol.py) and Chinese tenor classifier
  paths.py                 where the data folder is (override with SYNTHIUM_DATA)
  cli.py                   the command line
data/
  VERIFIED_LEDGER.csv      the only authoritative case count
  T1_POINTS.csv            data for the pre-registered T1 review-barrier candidate
  campaign-a/              the Campaign A blind test: hash-chained blindlog.jsonl,
                           sealed/ full texts, PROGRESS.md (results and notes)
  MASTER_LEDGER.csv, FULL_CASE_LIST.md, EXCLUSIONS.csv
  registers/               every blind register (attempt 10 onward) and its analysis CSVs
  case_details/            case write-ups, incl. batch-2026-11/ (the 9-case November batch)
                           and campaign-a/ (one note per Campaign A case)
  citation_seed.json       10 real cases as citation vectors
  blind_log_2026-07/       the July blind protocol's log and sealed excerpt
  blind_dryrun_2026-11-10/ the November tool's dry run
docs/                      the living research documents (start with STATUS.md and RULER.md)
tests/                     59 tests
```

## Run it

```
cd Synthium                           # this folder, once downloaded
python -m pip install -e ".[dev]"    # optional; everything also runs in place
python -m pytest -q
python -m synthium ruler-eval
python -m synthium predict --category civil --posture trial --layer legal_overlay
python -m synthium predict --category criminal --posture trial --layer legal_overlay --level apex
python -m synthium blind status       # the blind protocol, see docs/BLIND_PROTOCOL.md
```

## Read next

- `docs/STATUS.md`: the whole story on one page
- `docs/RULER.md`: units, formula, and the full keep/change history
- `docs/PREDICTIONS_REGISTER.md`: every committed prediction
- `docs/CROSS_BORDER.md`: the fact/law seam across legal systems
- `docs/AXIOM_CANDIDATES.md`: Sina's axioms, formalized and audited, plus T1
- `docs/MATH_CANDIDATES.md`, `docs/VALUE_SKELETON.md`: the math candidates
- `docs/METHOD.md`, `docs/BLIND_PROTOCOL.md`: how cases are coded blind
- `docs/ARTICLE_a_ruler_for_judgment.md`: the July open research note
- `docs/ROADMAP.md`, `docs/AUDIT_2026-07-10.md`, `docs/CORRECTIONS_2026-07-13.md`,
  `docs/COUNT_RECONCILIATION.md`, `docs/ENVIRONMENT.md`
