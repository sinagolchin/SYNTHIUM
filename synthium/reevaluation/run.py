"""Re-evaluate every case, stage by stage, with every restored formula and tool.

    python -m synthium.reevaluation STAGES_DIR --cases CASES.csv --out OUT_DIR

Writes ``reevaluation_results.json``, ``formulas_by_stage.csv`` and
``reevaluation_report.md`` to OUT_DIR. Keep OUT_DIR outside the public repository: it
holds case-level data.

UNTESTED and NOT BLIND.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
from typing import Dict, List

import numpy as np

from ..geometry.scores import NON_SCORE_Q_COLUMNS, parse_score, quality_columns
from ..phenomena.catalogue import RECORDS
from .analyses import compare_with_first_reading, quality_motion, run_checks, scorer_agreement
from .formulas import STAND_INS, all_for_stage
from .geometry_on_stages import run_geometry, run_quality_geometry
from .stages import STAGES, load_staged

# Why a record gets no check here (records that a check uses are filled in from the checks).
NOT_CHECKED = {
    "formula": "computed at every stage where its dimensions exist, but nothing in a court record shows "
               "the thing it names (meaning, perception, information, flux), so no check was possible",
    "unit": "a unit, not a claim; used where the stage scores need it",
    "tool": "a tool, not a claim",
    "axiom": "an axiom with no outcome it predicts in these records",
    "law": "a law whose parts these records do not hold",
    "profile": "a hand-set profile, not a claim about cases",
}
SPECIFIC = {
    "V2-DENSITY": "needs a location in space (x, y, z); court cases have none",
    "V2-PRESSURE": "needs depth z", "V2-FIELD": "needs distance", "V2-RANGE": "needs distance",
    "V2-ENTROPY-GRAD": "needs depth z",
    "V3-MEANING-NET": "needs a network of beings", "V3-BEAUTY": "no court observable",
    "V3-AWAKENING": "the fixed point (v 0, r 1, S 0): counted below, no outcome claim",
    "V3.1-CARE": "needs a care matrix between beings", "V3.4-CARE": "needs resource transfers between beings",
    "U-LIFEYEAR": "needs a death-compensation award with the victim's age and income; none of these cases is one",
    "U-DIGNITY": "needs bereavement and dependency awards; none here", "V-TWOPRICE": "needs death awards; none here",
    "V-THREE-OBJECTS": "needs death awards; none here", "U-GRIEF-DIMS": "needs death awards; none here",
    "V6.1-PRESSURE": "needs the twelve privacy units; these are not privacy cases",
    "V4.3-RUBRIC": "needs the privacy units", "M-S": "needs reversal counts by layer across many appeals",
    "M-W": "needs movement by destination across many appeals", "M-STACK": "needs errors on several layers",
    "M-FACT-INV": "needs appeals at several levels", "PHEN-CYCLE": "needs fear, love and obsession measured as phenomena of their own over time",
    "AXIOM-OPT": "an optimisation; its parts (H, interference) are checked in C03 and C13",
    "ENV": "needs channel reliability over years",
}


def _reading_order(cases_csv: str) -> Dict[str, int]:
    with open(cases_csv, newline="", encoding="utf-8") as fh:
        return {r["case_id"]: i for i, r in enumerate(csv.DictReader(fh))}


def _first_values(cases_csv: str) -> Dict[str, Dict[str, float]]:
    with open(cases_csv, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    cols = quality_columns(list(rows[0].keys()), None, NON_SCORE_Q_COLUMNS)
    out = {}
    for r in rows:
        d = {}
        for c in cols:
            v, _ = parse_score(r.get(c, ""))
            if v is not None and 0 <= v <= 1:
                d[c] = v
        out[r["case_id"]] = d
    return out


def _clean(o):
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.ndarray):
        return _clean(o.tolist())
    return o


def _f(x, nd=2):
    if x is None:
        return "n/a"
    try:
        if not np.isfinite(x):
            return "n/a"
    except TypeError:
        return str(x)
    return f"{x:.{nd}f}"


def record_status(checks: List[dict]) -> List[dict]:
    used = {}
    for ch in checks:
        for rid in ch["records"]:
            used.setdefault(rid, []).append(f"{ch['id']}: {ch['verdict']}")
    out = []
    for r in RECORDS:
        if r.id in used:
            status = "; ".join(used[r.id])
        elif r.id in SPECIFIC:
            status = "untestable here: " + SPECIFIC[r.id]
        elif r.id in ("GEOMETRY", "PHENOMENA", "V4-MANIFOLD", "V4-DISCOVERY", "V4-TENSOR", "V4-CALCULUS", "V4-NDIM"):
            status = "used: run on the stage points (see geometry section)"
        else:
            status = ("computed only: " if r.compute else "untestable here: ") + NOT_CHECKED.get(r.kind, "no check")
        out.append({"id": r.id, "kind": r.kind, "version": r.version, "statement": r.statement,
                    "this_run": status, "status": r.status})
    return out


def run(stages_dir: str, cases_csv: str, out_dir: str, seed: int = 0) -> dict:
    os.makedirs(out_dir, exist_ok=True)
    cases = load_staged(stages_dir)
    calib = load_staged(os.path.join(stages_dir, "calibration"))
    order = _reading_order(cases_csv)
    first = _first_values(cases_csv)

    checks = run_checks(cases, order)
    res = {
        "status": "UNTESTED; NOT BLIND (stage scores made after every ending was known)",
        "n_cases": len(cases),
        "stages_present": {st: sum(c.present(st) for c in cases) for st in STAGES},
        "stages_unknown": {st: sum(str((c.stages.get(st) or {}).get("present", "")).lower() == "unknown" for c in cases) for st in STAGES},
        "scorers": sorted({c.scorer for c in cases}),
        "stand_ins": STAND_INS,
        "checks": checks,
        "records": record_status(checks),
        "quality_motion": quality_motion(cases),
        "scorer_agreement": scorer_agreement(calib, cases) if calib else {"tested": False},
        "first_vs_stage": compare_with_first_reading(cases, first),
        "geometry": run_geometry(cases, seed=seed),
        "quality_geometry": run_quality_geometry(cases, seed=seed),
        "notes": {c.case_id: c.notes for c in cases if c.notes},
        "missing": {c.case_id: c.missing for c in cases if c.missing},
    }
    res = _clean(res)
    with open(os.path.join(out_dir, "reevaluation_results.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)

    # every formula at every stage of every case
    keys = sorted({k for c in cases for st in c.present_stages() for k in all_for_stage(c, st)})
    with open(os.path.join(out_dir, "formulas_by_stage.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["case_id", "stage"] + keys)
        for c in cases:
            for st in c.present_stages():
                vals = all_for_stage(c, st)
                w.writerow([c.case_id, st] + [_f(vals.get(k), 4) if k in vals else "" for k in keys])

    with open(os.path.join(out_dir, "reevaluation_report.md"), "w", encoding="utf-8") as fh:
        fh.write(report(res))
    return res


def report(res: dict) -> str:
    L = []
    a = L.append
    a("# Re-evaluation of every case, stage by stage\n")
    a("**UNTESTED and NOT BLIND.** The stage scores were made after every ending was known, by seven "
      "scorers working from the stored case notes. Scores are rankings from counted signs, with no real "
      "unit. A 'holds' below can be hindsight; a 'breaks' is harder to explain away. Nothing here is "
      "retired: every record stays under consideration.\n")
    a(f"Cases: {res['n_cases']}. Stage points present: " +
      ", ".join(f"{k} {v}" for k, v in res["stages_present"].items()) + ".")
    a("Stages marked unknown (notes lack them): " + ", ".join(f"{k} {v}" for k, v in res["stages_unknown"].items()) + ".\n")

    a("## 1. What each old formula predicts, against what happened\n")
    a("| check | records | tested as | n | result | verdict |")
    a("|---|---|---|---|---|---|")
    for ch in res["checks"]:
        r = ch["result"] or {}
        if "rho" in r:
            txt = f"rho {_f(r.get('rho'))}, p {_f(r.get('p'), 3)}"
            n = r.get("n")
        elif "share_not_falling" in r:
            txt = f"{_f(r.get('share_not_falling'))} of chosen steps did not fall (p {_f(r.get('p'), 3)}); imposed steps {_f(r.get('imposed_share_not_falling'))}"
            n = r.get("n")
        elif "n_steps" in r:
            txt = f"U fell {r['fell']}, rose {r['rose']} (p {_f(r.get('p'), 3)})"
            n = r["n_steps"]
        elif "inside" in r:
            txt = f"{r['inside']} of {r['n_points']} points inside the 'impossible' region"
            n = r["n_points"]
        elif "conserved" in r:
            txt = "conserved: " + (", ".join(r["conserved"]) or "none") + "; variation " + ", ".join(
                f"{k} {_f(v['variation'])}" for k, v in r["by_quantity"].items())
            n = r["n_cases"]
        elif "forms" in r:
            txt = "; ".join(f"{k} rho {_f(v.get('rho'))}" for k, v in r["forms"].items())
            n = max((v.get("n", 0) for v in r["forms"].values()), default=0)
        else:
            txt = ", ".join(f"{k} {_f(v) if isinstance(v, (int, float)) else v}" for k, v in r.items() if not isinstance(v, dict))
            n = r.get("n")
        a(f"| {ch['id']} | {', '.join(ch['records'])} | {ch['tested_as']} | {n} | {txt} | {ch['verdict']} |")
    a("")
    for ch in res["checks"]:
        if ch.get("note"):
            a(f"- {ch['id']}: {ch['note']}")
    a("\nStand-ins used where a formula needs a part the stage scores do not hold:\n")
    for k, v in res["stand_ins"].items():
        a(f"- {k}: {v}")

    g = res["geometry"]
    a("\n## 2. Geometry on stage points\n")
    a(f"{g['n_stage_points']} stage points (one per case per stage present). Dimensions used: the five early "
      "ones (v, R, r, C, S), the four Fear of Loss parts and standing H.\n")
    d = g["dimensions"]
    a(f"- Own dimension or made of others: tested {d['qualities_tested']}; own dimension: {', '.join(d['new_dimensions']) or 'none'}; "
      f"made of others: {', '.join(d['combinations']) or 'none'}.")
    for t in g["dimension_tests"]:
        if t.get("tested"):
            a(f"  - {t['column']}: best fit from {' + '.join(t['best_predictors'])}, adj. R^2 {_f(t['best_adj_r2'])} "
              f"(shuffled {_f(t['shuffled_best_mean'])}, p {_f(t['p'], 3)}) -> {t['verdict']}")
    if "pca" in g:
        p = g["pca"]
        pa = p["parallel_analysis"]
        a(f"- Directions beating shuffled data: **{pa['dimensions_beating_chance']}** of {len(pa['eigenvalues'])} "
          f"(effective dimensions {_f(pa['participation_ratio'])}, on {p['n_points']} complete points).")
        for i, tl in enumerate(p["top_loadings"]):
            a(f"  - direction {i + 1} ({_f(100 * p['explained'][i], 0)}% of spread): " +
              ", ".join(f"{k} ({v:+.2f})" for k, v in tl))
    if "curvature" in g:
        c = g["curvature"]
        a(f"- Folded? real {_f(c['observed'], 3)} vs shuffled {_f(c['shuffled_mean'], 3)} (sd {_f(c['shuffled_sd'], 3)}); "
          f"share of shuffles at least as folded {_f(c['p_at_least_as_folded'], 3)}.")
    pt = g["paths"]
    if pt.get("tested"):
        a(f"- Paths: on {pt['n_cases']} cases with 3+ scored stages, the real stage order is {_f(pt['mean_real_length'])} long "
          f"vs {_f(pt['mean_shuffled_length'])} for shuffled orders; real shorter in {_f(100 * pt['share_cases_real_shorter'], 0)}% "
          f"of cases (p {_f(pt['p'], 3)}). Median path / straight line {_f(pt['median_length_over_straight_line'])}.")
    for key, label in (("H_created_how", "Standing H from r, C, order(1-S)"),
                       ("H_created_how_with_resistance", "Standing H from C, order(1-S), R")):
        h = g[key]
        if h.get("tested"):
            a(f"- {label}: best form **{h['best_form']}** (rho {_f(h['best_rho'])}, margin {_f(h['margin'])}, "
              f"p {_f(h['p_best'], 3)}); " + ", ".join(f"{k} {_f(v['rho'])}" for k, v in h["forms"].items()))
    for key, label in (("balance_five", "Balance among v, R, r, C, S"), ("balance_fear", "Balance among fear parts and H")):
        b = g[key]
        if b.get("tested"):
            a(f"- {label}: least-spread share {_f(b['least_spread_share'], 3)} vs shuffled {_f(b['shuffled_mean'], 3)} "
              f"(p {_f(b['p_at_least_as_balanced'], 3)}); weights " + ", ".join(f"{k} {v:+.2f}" for k, v in b["weights"].items()))
    a("\nBuild-up (dot, line, area, volume ...):\n")
    a("| step | added | points | new share | volume | shuffled volume | effective dims |")
    a("|---|---|---|---|---|---|---|")
    for s in g["build_up"]:
        a(f"| {s['step']} | {s['added'] or '-'} | {s['n_points']} | {_f(s['new_share'])} | {_f(s['volume'])} | {_f(s['volume_shuffled'])} | {_f(s['effective_dims'])} |")

    qg = res["quality_geometry"]
    a("\n## 3. Qualities over stage points\n")
    if qg.get("tested"):
        a(f"Qualities on 15+ stage points: {len(qg['qualities'])}. Own dimension: {', '.join(qg['new_dimensions']) or 'none'}. "
          f"Made of others: {', '.join(qg['combinations']) or 'none'}.")
        for t in qg["results"]:
            if t.get("tested") and not t["verdict"].startswith("new"):
                a(f"  - {t['column']} from {' + '.join(t['best_predictors'])}: adj. R^2 {_f(t['best_adj_r2'])}, p {_f(t['p'], 3)}")
    else:
        a("Too few qualities on enough stage points.")
    a("\nWhich qualities move between stages (cases with the quality at 2+ stages):\n")
    a("| quality | cases | share that moved | mean range | mean by stage (act, filing, plea/answer, trial/hearing, sentence/remedy, appeal) |")
    a("|---|---|---|---|---|")
    qm = sorted(res["quality_motion"].items(), key=lambda kv: -kv[1]["cases_with_2plus_stages"])
    for k, v in qm[:25]:
        a(f"| {k} | {v['cases_with_2plus_stages']} | {_f(v['share_that_moved'])} | {_f(v['mean_range'])} | " +
          ", ".join(_f(v["mean_by_stage"].get(st)) for st in STAGES) + " |")

    a("\n## 4. First reading vs stage re-scoring\n")
    a("| quality | cases | rank agreement | mean gap |")
    a("|---|---|---|---|")
    for k, v in sorted(res["first_vs_stage"].items(), key=lambda kv: -kv[1]["n"]):
        a(f"| {k} | {v['n']} | {_f(v['rho'])} (p {_f(v['p'], 3)}) | {_f(v['mean_abs_diff'])} |")

    sa = res["scorer_agreement"]
    a("\n## 5. Do the scorers agree? (KIM-2019 scored by every scorer)\n")
    if sa.get("fields"):
        a(f"Scorers: {len(sa['scorers'])}. Median spread on the same case {_f(sa['median_sd_same_case'])} vs "
          f"across different cases {_f(sa['median_sd_across_cases'])}; noise share {_f(sa['noise_share'])} "
          "(0 = perfect agreement, 1 = scorers differ as much as cases do).\n")
        worst = sorted(sa["fields"].items(), key=lambda kv: -kv[1]["sd_same_case"] / max(kv[1]["sd_across_cases"], 1e-9))[:8]
        for k, v in worst:
            a(f"- least agreed: {k}: {', '.join(_f(x) for x in v['values'])}")
    else:
        a("No calibration files.")

    a("\n## 6. Every record in the index, and what this run did with it\n")
    a("| id | kind | this run |")
    a("|---|---|---|")
    for r in res["records"]:
        a(f"| `{r['id']}` | {r['kind']} | {r['this_run']} |")

    a("\n## 7. Scorers' proposals and notes (INFERRED, to be debated)\n")
    for cid, n in sorted(res["notes"].items()):
        a(f"- {cid}: {n}")
    a("\n## 8. Stages the stored notes lack\n")
    for cid, m in sorted(res["missing"].items()):
        a(f"- {cid}: " + "; ".join(str(x) for x in m))
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Re-evaluate every case stage by stage (UNTESTED)")
    ap.add_argument("stages_dir")
    ap.add_argument("--cases", required=True)
    ap.add_argument("--out", default="reevaluation_out")
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args(argv)
    run(a.stages_dir, a.cases, a.out, a.seed)
    print(f"wrote {a.out}/reevaluation_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
