"""Run the geometry on a case table and write a plain-language report.

    python -m synthium.geometry CASES.csv --out results/

Writes ``geometry_report.md`` and ``geometry_results.json``. Every number is UNTESTED.
"""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from typing import List

import numpy as np

from .calculus import rate_along
from .dimensions import build_up, estimate_dimensions, parallel_analysis, pca
from .manifold import (
    RiemannianManifold,
    curvature_index_vs_shuffled,
    learn_metric_from_data,
    pairwise_distances_missing,
)
from .metric_field import metric_field_from_cases
from .scores import load_cases, standardise
from .trajectory import paths_from_staged_cells, staged_cells

BANNER = (
    "**UNTESTED.** Every number below comes from scores that are rankings from counted "
    "signs, with no real unit yet. Nothing here has been checked on new cases. Read each "
    "number as a description of these cases, not a law."
)


def _f(x, nd=2):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "n/a"
    return f"{x:.{nd}f}"


def run(path: str, out_dir: str, domain: str = "courts", seed: int = 0) -> dict:
    cs = load_cases(path, domain=domain)
    os.makedirs(out_dir, exist_ok=True)
    L: List[str] = []
    R: dict = {"source": os.path.basename(path), "domain": domain}

    # 0. The points and their active dimensions
    present = ~np.isnan(cs.values)
    per_case = present.sum(axis=1)
    cov = cs.coverage()
    tag_counts = Counter(t for row in cs.tags for t in row if t)
    R["n_cases"] = cs.n_cases
    R["n_qualities"] = len(cs.columns)
    R["active_per_case"] = dict(zip(cs.case_ids, per_case.tolist()))
    L += [
        "# Synthium geometry, first run",
        "",
        BANNER,
        "",
        "## 0. The points",
        "",
        f"{cs.n_cases} cases (points) and {len(cs.columns)} qualities (possible dimensions). "
        f"{int(present.sum())} of {present.size} cells are scored "
        f"({100 * present.mean():.1f}%).",
        f"Each case is active on {int(per_case.min())} to {int(per_case.max())} qualities "
        f"(median {int(np.median(per_case))}).",
        "Tags on scored cells: "
        + ", ".join(f"{k} {v}" for k, v in tag_counts.most_common())
        + f", untagged {int(present.sum()) - sum(tag_counts.values())}.",
        "",
        "Most-scored qualities: "
        + ", ".join(f"{c} ({n})" for c, n in sorted(cov.items(), key=lambda kv: -kv[1])[:12]),
        "",
    ]

    # 1. Dot -> line -> area -> volume
    bu = build_up(cs, seed=seed)
    R["build_up"] = [s.__dict__ for s in bu.steps]
    L += [
        "## 1. Dot, line, area, volume",
        "",
        "Qualities are added one at a time. At each step only the cases scored on every "
        "quality so far can be placed, so the cloud thins as it gains dimensions.",
        "",
        "- **new share**: how much of the added quality is new, not already predictable "
        "(in a straight line) from the earlier ones. 1 = a fully new direction, 0 = nothing new.",
        "- **volume**: how much room the cloud fills, from 1 (every quality independent) to "
        "0 (flattened onto fewer dimensions). Next to it, the same for shuffled qualities.",
        "- **effective dims**: how many directions the spread really uses.",
        "",
        "| step | added quality | cases | new share | volume | shuffled volume | effective dims |",
        "|---|---|---|---|---|---|---|",
    ]
    for s in bu.steps:
        L.append(
            f"| {s.name} | {s.added or '-'} | {s.n_cases} | {_f(s.new_share)} | "
            f"{_f(s.volume)} | {_f(s.volume_shuffled)} | {_f(s.participation_ratio)} |"
        )
    L.append("")

    # 2. How many dimensions do the cases need?
    # The deepest step that still has at least 20 cases (12 at worst): fewer cases
    # than that cannot tell real directions from luck.
    deepest = None
    for floor in (20, 12):
        for st in bu.steps[1:]:
            if st.n_cases >= floor and st.k >= 3:
                deepest = st
        if deepest is not None:
            break
    if deepest is None and len(bu.steps) > 1:
        deepest = bu.steps[-1]
    L += ["## 2. How many dimensions the cases need", ""]
    if deepest is not None and deepest.k >= 2:
        cols = bu.order[: deepest.k]
        rows = cs.complete_rows(cols)
        X = cs.select(cols)[rows]
        pa = parallel_analysis(X, seed=seed)
        pr = pca(X, cols)
        R["block"] = {"columns": cols, "case_ids": deepest.case_ids}
        R["parallel_analysis"] = pa
        L += [
            f"Block used: the {deepest.k} qualities of the '{deepest.name}' step, on "
            f"{deepest.n_cases} cases that carry all of them.",
            "",
            f"Directions that beat shuffled data: **{pa['dimensions_beating_chance']}** of "
            f"{len(cols)}. Effective dimensions: {_f(pa['participation_ratio'])}.",
            "",
        ]
        for i in range(min(3, len(cols))):
            L.append(
                f"- Direction {i + 1} ({100 * pr.explained[i]:.0f}% of the spread; shuffled bar "
                f"{_f(pa['shuffled_bar'][i])} vs real {_f(pa['eigenvalues'][i])}): "
                + ", ".join(pr.top_qualities(i))
            )
        L.append("")
    ed = estimate_dimensions(cs, seed=seed, n_perm=100)
    R["new_dimension_test"] = ed
    L += [
        "**New dimension or a combination?** For each quality scored on at least 8 cases, the "
        "best straight-line fit from one or two other qualities, against the same search on "
        "shuffled scores.",
        "",
        f"- Tested: {ed['qualities_tested']} qualities.",
        f"- Count as their own dimension on these cases: {len(ed['new_dimensions'])}.",
        f"- Look like a combination of others: {len(ed['combinations'])}"
        + (": " + ", ".join(ed["combinations"]) if ed["combinations"] else "."),
        "",
        "| quality | best predictors | cases | adj. R^2 | shuffled | p | verdict |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in sorted(
        [r for r in ed["results"] if r.get("tested")], key=lambda r: -r["best_adj_r2"]
    ):
        L.append(
            f"| {r['column']} | {' + '.join(r['best_predictors'])} | {r['n_cases']} | "
            f"{_f(r['best_adj_r2'])} | {_f(r['shuffled_best_mean'])} | {_f(r['p'], 3)} | {r['verdict']} |"
        )
    L += [
        "",
        "A small number of cases per pair means a fit of 0.5 can still be luck; the shuffled "
        "column shows what luck alone reaches. With "
        f"{ed['qualities_tested']} qualities tested at p < 0.05, about "
        f"{max(1, round(0.05 * ed['qualities_tested']))} could pass by luck alone, so a "
        "'combination' verdict on 8 to 10 cases is a lead to re-check, not a result.",
        "",
    ]

    # 3. Distances and nearest cases
    Z = standardise(cs.values)
    D, shared = pairwise_distances_missing(Z, min_shared=4)
    pairs = []
    n = cs.n_cases
    for i in range(n):
        for j in range(i + 1, n):
            if np.isfinite(D[i, j]):
                pairs.append((D[i, j], shared[i, j], cs.case_ids[i], cs.case_ids[j]))
    pairs.sort()
    R["closest_pairs"] = pairs[:15]
    reachable = len(pairs)
    L += [
        "## 3. Distances between cases",
        "",
        "Distance = root mean square difference over the qualities both cases carry "
        "(each quality first put on the same footing). Pairs sharing fewer than 4 "
        f"qualities are left out: {reachable} of {n * (n - 1) // 2} pairs can be compared.",
        "",
        "Closest pairs:",
        "",
    ]
    for d, sh, a, b in pairs[:10]:
        L.append(f"- {a} and {b}: {_f(d)} over {sh} shared qualities")
    L.append("")
    if deepest is not None and deepest.k >= 2:
        cols = bu.order[: deepest.k]
        rows = cs.complete_rows(cols)
        Xb = standardise(cs.select(cols)[rows])
        g = learn_metric_from_data(Xb, "mahalanobis")
        M = RiemannianManifold(len(cols), g)
        Dm = M.pairwise(Xb)
        Di = RiemannianManifold(len(cols)).pairwise(Xb)
        iu = np.triu_indices(len(rows), 1)
        agree = float(np.corrcoef(Dm[iu], Di[iu])[0, 1]) if len(iu[0]) > 2 else float("nan")
        R["metric_agreement"] = agree
        L += [
            f"On the '{deepest.name}' block, distances with the learned metric (qualities that "
            f"move together count once) agree with plain distances at r = {_f(agree)}. "
            "Lower agreement means the qualities overlap enough for the metric to matter.",
            "",
        ]

    # 4. Curvature
    L += ["## 4. Is the cloud of cases curved?", ""]
    if deepest is not None and deepest.k >= 2 and deepest.n_cases >= 10:
        cols = bu.order[: deepest.k]
        rows = cs.complete_rows(cols)
        Xb = standardise(cs.select(cols)[rows])
        k = max(4, min(8, len(rows) // 6))
        ci = curvature_index_vs_shuffled(Xb, k=k, n_perm=200, seed=seed)
        R["curvature_index"] = ci
        L += [
            "Paths that hop from case to near case, compared with straight lines. Shuffled "
            "clouds give the baseline.",
            "",
            f"- Real cases: {_f(ci['observed'], 3)}; shuffled: {_f(ci['shuffled_mean'], 3)} "
            f"(sd {_f(ci['shuffled_sd'], 3)}); share of shuffles at least as folded: {_f(ci['p_at_least_as_folded'], 3)}.",
            "",
        ]
        pr = pca(cs.select(cols)[rows], cols)
        P2 = standardise(cs.select(cols)[rows]) @ pr.loadings[:2].T
        P2 = P2 / P2.std(axis=0)
        field = metric_field_from_cases(P2, bandwidth=1.0)
        curv = []
        for p in P2:
            try:
                curv.append(field.scalar_curvature(p))
            except np.linalg.LinAlgError:
                curv.append(float("nan"))
        curv = np.asarray(curv)
        order = np.argsort(curv)
        ids = [cs.case_ids[i] for i in rows]
        R["scalar_curvature_2d"] = dict(zip(ids, curv.tolist()))
        L += [
            "Curvature of a metric built from where the cases bunch, on the block's top two "
            "directions (rough with this few cases):",
            "",
            f"- median {_f(float(np.nanmedian(curv)))}, range {_f(float(np.nanmin(curv)))} to {_f(float(np.nanmax(curv)))}.",
            f"- Most negative (cases spread out around them): {', '.join(ids[i] for i in order[:3])}.",
            f"- Most positive (cases bunch around them): {', '.join(ids[i] for i in order[::-1][:3])}.",
            "",
        ]
    else:
        L += ["Not enough cases share enough qualities to test this yet.", ""]

    # 5. Rates of change along time
    L += [
        "## 5. Change along time",
        "",
        "Cases are separate events, not one moving body. A slope along **reading order** "
        "asks whether our scoring drifted while we read; along **filing date** it describes "
        "which cases were picked. Each slope is next to random orderings of the same scores.",
        "",
        "| quality | cases | slope per 10 cases read | p | slope per year filed | p |",
        "|---|---|---|---|---|---|",
    ]
    years = cs.filed_as_years()
    rates = {}
    for c in sorted(cov, key=lambda c: -cov[c])[:8]:
        y = cs.select([c])[:, 0]
        ro = rate_along(cs.reading_order, y, seed=seed)
        fy = rate_along(years, y, seed=seed)
        rates[c] = {"reading": ro.get("slope"), "p_reading": ro.get("p_slope"),
                    "filed": fy.get("slope"), "p_filed": fy.get("p_slope")}
        L.append(
            f"| {c} | {ro['n']} | {_f(10 * ro['slope'] if ro['slope'] == ro['slope'] else float('nan'), 3)} | "
            f"{_f(ro['p_slope'], 3)} | {_f(fy['slope'], 3)} | {_f(fy['p_slope'], 3)} |"
        )
    R["rates"] = rates
    L.append("")

    # 6. Cases as paths
    cells = staged_cells(path, cs.columns)
    paths = paths_from_staged_cells(cells)
    R["staged_cells"] = [c[:4] for c in cells]
    L += [
        "## 6. Cases as paths over time",
        "",
        f"Cells that record a before and after score: {len(cells)}, in {len(paths)} cases. "
        "Every other case is still a single point. To see trajectories, the reading routine "
        "would need to score qualities at each stage (filing, plea or trial, sentence).",
        "",
    ]
    for p in paths:
        for st in p.steps():
            L.append(f"- {p.case_id}: {st['from']} to {st['to']}, moved {st['moved']}")
    L += [
        "",
        "## What these numbers do and don't mean",
        "",
        "- They describe the shape of this sample of scores. They are not measurements in a "
        "unit, and none has been checked on new cases.",
        "- Missing scores are left missing. Every analysis says how many cases it used.",
        "- A quality called a 'new dimension' here may turn out to be a combination once more "
        "cases share it; the reverse is also possible.",
        "- Curvature here means the spread of cases changes from region to region. Whether "
        "that has a meaning for the qualities is the open question.",
    ]

    with open(os.path.join(out_dir, "geometry_report.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    with open(os.path.join(out_dir, "geometry_results.json"), "w", encoding="utf-8") as fh:
        json.dump(R, fh, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    return R


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Synthium geometry on a case table (UNTESTED)")
    ap.add_argument("cases_csv")
    ap.add_argument("--out", default="geometry_out")
    ap.add_argument("--domain", default="courts")
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args(argv)
    run(a.cases_csv, a.out, a.domain, a.seed)
    print(f"Wrote {a.out}/geometry_report.md and geometry_results.json (UNTESTED)")
    return 0
