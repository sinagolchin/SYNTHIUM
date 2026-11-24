"""The restored geometry, run on stage points instead of whole cases.

Each (case, stage) is a point. A case is a path through its stages. Questions:

1. How many dimensions do the stage points need, and which scores are made of others?
2. Is the cloud of stage points folded (curved) beyond what shuffled clouds show?
3. Do cases move along smooth paths: is the real stage order shorter than shuffled orders?
4. How is standing (H) built from the five early dimensions: sum, product, weakest part ...?
5. Is any mix of the five dimensions balanced (forces summing to zero)?

UNTESTED and NOT BLIND.
"""

from __future__ import annotations

from typing import List

import numpy as np

from ..geometry import (
    build_up,
    curvature_index_vs_shuffled,
    estimate_dimensions,
    parallel_analysis,
    pca,
    standardise,
)
from ..geometry.scores import CaseScores
from ..phenomena.structure import created_how, equilibrium
from .stages import FEAR, FIVE, StagedCase, stage_points

CORE = list(FIVE) + list(FEAR) + ["H_enjoyment"]


def _with_order(cs: CaseScores) -> CaseScores:
    """Add 'order' = 1 - S, so every part points the same way for the monotone forms."""
    j = cs.columns.index("S")
    values = np.column_stack([cs.values, 1 - cs.values[:, j]])
    return CaseScores(cs.case_ids, cs.columns + ["order(1-S)"], values,
                      [t + [None] for t in cs.tags], cs.reading_order, cs.filed, cs.domain)


def path_order_test(cases: List[StagedCase], n_perm: int = 500, seed: int = 0) -> dict:
    """Real stage order vs shuffled stage order: total path length over the five dimensions."""
    rng = np.random.default_rng(seed)
    real, null_means, bends = [], [], []
    for c in cases:
        pts = [c.point(st) for st in c.present_stages()]
        pts = np.array([[p[k] for k in FIVE] for p in pts if p is not None])
        if len(pts) < 3:
            continue
        def length(P):
            return float(np.sum(np.linalg.norm(np.diff(P, axis=0), axis=1)))
        L = length(pts)
        chord = float(np.linalg.norm(pts[-1] - pts[0]))
        real.append(L)
        null_means.append(np.mean([length(pts[rng.permutation(len(pts))]) for _ in range(50)]))
        if chord > 0:
            bends.append(L / chord)
    if len(real) < 8:
        return {"tested": False, "n_cases": len(real)}
    real, null_means = np.array(real), np.array(null_means)
    diff = real - null_means
    # sign-flip permutation on the per-case differences
    obs = diff.mean()
    flips = np.array([(diff * rng.choice([-1, 1], len(diff))).mean() for _ in range(n_perm)])
    p = float((np.sum(np.abs(flips) >= abs(obs)) + 1) / (n_perm + 1))
    return {
        "tested": True,
        "n_cases": int(len(real)),
        "mean_real_length": float(real.mean()),
        "mean_shuffled_length": float(null_means.mean()),
        "share_cases_real_shorter": float(np.mean(diff < 0)),
        "p": p,
        "median_length_over_straight_line": float(np.median(bends)) if bends else float("nan"),
    }


def run_geometry(cases: List[StagedCase], seed: int = 0) -> dict:
    out: dict = {}
    cs = stage_points(cases, CORE)
    out["n_stage_points"] = cs.n_cases
    out["coverage"] = cs.coverage()

    est = estimate_dimensions(cs, n_perm=200, seed=seed)
    out["dimensions"] = {k: est[k] for k in ("qualities_tested", "new_dimensions", "combinations")}
    out["dimension_tests"] = est["results"]

    bu = build_up(cs, seed=seed)
    out["build_up"] = [
        {"step": s.name, "added": s.added, "n_points": s.n_cases, "new_share": s.new_share,
         "volume": s.volume, "volume_shuffled": s.volume_shuffled, "effective_dims": s.participation_ratio}
        for s in bu.steps
    ]

    rows = cs.complete_rows(CORE)
    if len(rows) >= 12:
        X = cs.select(CORE)[rows]
        Z = standardise(X)
        pr = pca(Z, CORE)
        pa = parallel_analysis(Z, seed=seed)
        out["pca"] = {
            "n_points": int(len(rows)),
            "explained": [float(x) for x in pr.explained[:5]],
            "top_loadings": [
                sorted(zip(CORE, [float(v) for v in pr.loadings[i]]), key=lambda t: -abs(t[1]))[:4]
                for i in range(3)
            ],
            "parallel_analysis": pa,
        }
        out["curvature"] = curvature_index_vs_shuffled(Z, k=6, n_perm=200, seed=seed)

    out["paths"] = path_order_test(cases, seed=seed)

    cso = _with_order(cs)
    out["H_created_how"] = created_how(cso, "H_enjoyment", ["r", "C", "order(1-S)"], seed=seed)
    out["H_created_how_with_resistance"] = created_how(cso, "H_enjoyment", ["C", "order(1-S)", "R"], seed=seed)
    out["balance_five"] = equilibrium(cs, list(FIVE), seed=seed)
    out["balance_fear"] = equilibrium(cs, list(FEAR) + ["H_enjoyment"], seed=seed)
    return out


def run_quality_geometry(cases: List[StagedCase], min_points: int = 15, seed: int = 0) -> dict:
    """The Q qualities as dimensions over stage points (only those on enough points)."""
    keys = sorted({k for c in cases for k in c.quality_keys()})
    cs = stage_points(cases, keys)
    cov = cs.coverage()
    keep = [k for k in keys if cov[k] >= min_points]
    if len(keep) < 3:
        return {"tested": False, "qualities_with_enough_points": keep}
    cs2 = stage_points(cases, keep)
    est = estimate_dimensions(cs2, min_cases=10, n_perm=100, seed=seed)
    return {"tested": True, "qualities": keep, "coverage": {k: cov[k] for k in keep},
            "new_dimensions": est["new_dimensions"], "combinations": est["combinations"],
            "results": est["results"]}
