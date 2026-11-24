"""Run the phenomenon tests on a case table and write a plain-language report.

    python -m synthium.phenomena CASES.csv --out results/
    python -m synthium.phenomena index --write      # regenerate docs/UNDER_CONSIDERATION.md
    python -m synthium.phenomena index --check      # exit 1 if the doc is out of date

Writes ``phenomena_report.md`` and ``phenomena_results.json``. Every number is UNTESTED.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from typing import List

import numpy as np

from synthium.geometry.dimensions import choose_order, estimate_dimensions
from synthium.geometry.scores import load_cases

from .catalogue import RECORDS, computable
from .structure import created_how, equilibrium, phenomena_from_profiles, profile_space

BANNER = (
    "**UNTESTED.** The case scores are rankings from counted signs with no real unit, and "
    "the old phenomenon profiles were set by hand. Nothing here has been checked on new "
    "cases. Every past formula listed is under consideration, not retired."
)


def _f(x, nd=2):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "n/a"
    return f"{x:.{nd}f}"


def run(path: str, out_dir: str, domain: str = "courts", seed: int = 0, n_perm: int = 100) -> dict:
    os.makedirs(out_dir, exist_ok=True)
    L: List[str] = ["# Synthium phenomena run", "", BANNER, ""]
    R: dict = {"source": os.path.basename(path), "domain": domain}

    # 1. The catalogue
    kinds = Counter(r.kind for r in RECORDS)
    R["catalogue"] = {"entries": len(RECORDS), "by_kind": dict(kinds), "computable": len(computable())}
    L += ["## 1. Every past formula, unit, axiom and tool", "",
          f"{len(RECORDS)} entries ({', '.join(f'{n} {k}s' for k, n in kinds.most_common())}), all "
          "under consideration. The full list is `docs/UNDER_CONSIDERATION.md`.", ""]

    # 2. The old phenomena on their own five dimensions
    phs = phenomena_from_profiles()
    pick = ["V1-MASS", "V2.2-BURN", "V3-E", "V3-M", "V3.4-E", "V3.4-M", "V3.4-COLLAPSE"]
    L += ["## 2. The old phenomena, run through the old formulas", "",
          "Each phenomenon below was placed by hand on five dimensions (v speed, R resistance, "
          "r resonance, C capacity, S entropy). The formulas are the originals, unchanged.", "",
          "| phenomenon | v | R | r | C | S | " + " | ".join(pick) + " |",
          "|---" * (6 + len(pick)) + "|"]
    R["profiles"] = {}
    for p in phs:
        vals = p.formulas()
        R["profiles"][p.name] = {"point": p.point, "formulas": vals}
        L.append("| " + " | ".join([p.name] + [_f(p.point[d]) for d in "vRrCS"] + [_f(vals[k]) for k in pick]) + " |")
    ps = profile_space()
    eq_p = equilibrium(ps, ps.columns, n_perm=n_perm, min_cases=5, seed=seed)
    R["profiles_equilibrium"] = eq_p
    L += ["", "Is there a balance among the five dimensions of the hand-set profiles?", ""]
    if eq_p["tested"]:
        w = ", ".join(f"{k} {v:+.2f}" for k, v in eq_p["weights"].items())
        L += [f"- Least-spread mix: {w}. It holds {_f(eq_p['least_spread_share'] * 100, 1)}% of the spread "
              f"(shuffled profiles: {_f(eq_p['shuffled_mean'] * 100, 1)}%, p = {_f(eq_p['p_at_least_as_balanced'], 3)}).",
              "- This describes how the profiles were set by hand, not the phenomena themselves.", ""]

    # 3. Real cases: base or derived, and created how
    cs = load_cases(path, domain=domain)
    R["n_cases"] = cs.n_cases
    ed = estimate_dimensions(cs, seed=seed, n_perm=n_perm)
    R["base_or_derived"] = ed
    L += ["## 3. On the real cases: which qualities are base dimensions, which are made from others", "",
          f"{cs.n_cases} cases, {len(cs.columns)} qualities, {ed['qualities_tested']} scored on enough cases to test.",
          f"- Base on these cases: {len(ed['new_dimensions'])}.",
          f"- Made from others: {len(ed['combinations'])}" + (f" ({', '.join(ed['combinations'])})." if ed['combinations'] else "."),
          ""]
    hows = []
    for r in ed["results"]:
        if r.get("tested") and r["column"] in ed["combinations"]:
            hows.append(created_how(cs, r["column"], r["best_predictors"], n_perm=n_perm, seed=seed))
    R["created_how"] = hows
    if hows:
        L += ["For each quality made from others: which operation builds it from its parts best "
              "(rank correlation; no constants fitted).", "",
              "| quality | parts | cases | sum | product | weakest | strongest | priority | best | margin | p |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
        for h in hows:
            if not h.get("tested"):
                continue
            f = h["forms"]
            L.append("| " + " | ".join([
                h["target"], " + ".join(h["parts"]), str(h["n_cases"]),
                *(_f(f[k]["rho"]) for k in ("sum", "product", "weakest part", "strongest part", "strict priority")),
                h["best_form"], _f(h["margin"]), _f(h["p_best"], 3)]) + " |")
        L += ["", "A margin under about 0.05 means the forms can't be told apart on these cases yet.", ""]

    # 4. Real cases: balance laws
    order = choose_order(cs, max_dims=6)
    eqs = []
    for k in range(3, len(order) + 1):
        eqs.append(equilibrium(cs, order[:k], n_perm=n_perm, seed=seed))
    R["equilibrium"] = eqs
    L += ["## 4. On the real cases: does any mix of qualities stay balanced?", "",
          "The best-covered qualities, added one at a time. A share well below the shuffled share "
          "would be a candidate balance law (Sina's building, axiom G9).", "",
          "| qualities | cases | least-spread share | shuffled | p | heaviest weights |",
          "|---|---|---|---|---|---|"]
    for e in eqs:
        if not e.get("tested"):
            L.append(f"| {len(e['columns'])} | - | - | - | - | {e['reason']} |")
            continue
        top = ", ".join(f"{k} {v:+.2f}" for k, v in list(e["weights"].items())[:3])
        L.append(f"| {len(e['columns'])} | {e['n_cases']} | {_f(e['least_spread_share'] * 100, 1)}% | "
                 f"{_f(e['shuffled_mean'] * 100, 1)}% | {_f(e['p_at_least_as_balanced'], 3)} | {top} |")
    L += ["", "## What these numbers do and don't mean", "",
          "- The old five dimensions (v, R, r, C, S) are not scored on the cases, so the old formulas "
          "can only run on the hand-set profiles. Bridging the two needs a rule for reading v, R, r, C "
          "and S from a case, which does not exist yet.",
          "- 'Made from others' and 'balanced' describe this sample. Both can change as cases are added.",
          "- No formula here has been checked on new cases."]

    with open(os.path.join(out_dir, "phenomena_report.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    with open(os.path.join(out_dir, "phenomena_results.json"), "w", encoding="utf-8") as fh:
        json.dump(R, fh, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    return R


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "index":
        from .index import in_sync, write
        if "--check" in argv:
            ok = in_sync()
            print("docs/UNDER_CONSIDERATION.md is " + ("up to date" if ok else "OUT OF DATE"))
            return 0 if ok else 1
        changed = write()
        print("docs/UNDER_CONSIDERATION.md " + ("updated" if changed else "already up to date"))
        return 0
    ap = argparse.ArgumentParser(description="Synthium phenomena on a case table (UNTESTED)")
    ap.add_argument("cases_csv")
    ap.add_argument("--out", default="phenomena_out")
    ap.add_argument("--domain", default="courts")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--n-perm", type=int, default=100)
    a = ap.parse_args(argv)
    run(a.cases_csv, a.out, a.domain, a.seed, a.n_perm)
    print(f"Wrote {a.out}/phenomena_report.md and phenomena_results.json (UNTESTED)")
    return 0
