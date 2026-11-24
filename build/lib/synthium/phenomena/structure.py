"""A phenomenon as a structure with dimensions of its own (restored idea, 2026-11-24).

The early Synthium idea (V1 to V3, and Sina's July question "is privacy created by
addition, multiplication, or something else?") was that every phenomenon (grief,
privacy, an exception, any adjective) has its own dimensions, and that it is built from
them by some operation, the way speed is distance divided by time. Sina's building
analogy adds a second question: which combination of the parts stays balanced, the way
the forces on a standing building sum to zero.

This module asks those three questions of real case scores:

* :func:`base_or_derived`: is a quality a base dimension, or made from others?
  (wraps :func:`synthium.geometry.is_new_dimension`)
* :func:`created_how`: if it is made from others, by which operation: a sum, a
  product, its weakest part, its strongest part, or a strict priority (lexicographic)?
  No constants are fitted; each form uses the parts as they are.
* :func:`equilibrium`: is there a weighted sum of qualities that stays nearly the same
  across all cases (a balance law), compared with shuffled cases?

It also turns the old hand-set phenomenon profiles into points the geometry tools can
use (:func:`profile_space`) and runs every past formula on one phenomenon
(:class:`Phenomenon`).

UNTESTED. The case scores are rankings from counted signs with no real unit, and the
old profiles were set by hand.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import permutations
from typing import Dict, List, Optional, Sequence

import numpy as np

from synthium.geometry.dimensions import is_new_dimension
from synthium.geometry.scores import CaseScores, standardise

from .catalogue import DIMENSIONS_5D, evaluate, legacy_profiles

FORMS = ("sum", "product", "weakest part", "strongest part", "strict priority")


@dataclass
class Phenomenon:
    """One phenomenon placed on its own dimensions."""

    name: str
    point: Dict[str, float]
    source: str = "hand-set profile"
    notes: List[str] = field(default_factory=list)

    @property
    def dimensions(self) -> List[str]:
        return list(self.point)

    def formulas(self) -> Dict[str, float]:
        """Every past five-dimension formula, run on this phenomenon (needs v, R, r, C, S)."""
        missing = [d for d in DIMENSIONS_5D if d not in self.point]
        if missing:
            raise ValueError(f"{self.name} lacks dimensions {missing}")
        return evaluate(self.point)


def phenomena_from_profiles() -> List[Phenomenon]:
    return [Phenomenon(k, v) for k, v in sorted(legacy_profiles().items())]


def profile_space() -> CaseScores:
    """The old phenomenon profiles as points, so the geometry tools can be used on them."""
    profs = sorted(legacy_profiles().items())
    cols = list(DIMENSIONS_5D)
    vals = np.array([[p[c] for c in cols] for _, p in profs], dtype=float)
    return CaseScores(
        case_ids=[k for k, _ in profs],
        columns=cols,
        values=vals,
        tags=[[None] * len(cols) for _ in profs],
        reading_order=np.arange(len(profs)),
        filed=[None] * len(profs),
        domain="legacy phenomenon profiles",
    )


# ------------------------------------------------------------------ helpers


def _rank(x: np.ndarray) -> np.ndarray:
    order = np.argsort(x, kind="mergesort")
    ranks = np.empty(len(x), dtype=float)
    ranks[order] = np.arange(len(x), dtype=float)
    # average ties
    vals, inv, counts = np.unique(x, return_inverse=True, return_counts=True)
    sums = np.zeros(len(vals))
    np.add.at(sums, inv, ranks)
    return (sums / counts)[inv]


def spearman(a: np.ndarray, b: np.ndarray) -> float:
    ra, rb = _rank(np.asarray(a, float)), _rank(np.asarray(b, float))
    if np.std(ra) == 0 or np.std(rb) == 0:
        return 0.0
    return float(np.corrcoef(ra, rb)[0, 1])


def _to01(X: np.ndarray) -> np.ndarray:
    lo, hi = np.nanmin(X, axis=0), np.nanmax(X, axis=0)
    span = np.where(hi > lo, hi - lo, 1.0)
    return (X - lo) / span


def combine(parts: np.ndarray, form: str) -> np.ndarray:
    """Combine the columns of ``parts`` (cases x parts, each 0..1) by one operation."""
    P = np.asarray(parts, float)
    if form == "sum":
        return P.sum(axis=1)
    if form == "product":
        return np.prod(P + 1e-6, axis=1)
    if form == "weakest part":
        return P.min(axis=1)
    if form == "strongest part":
        return P.max(axis=1)
    if form == "strict priority":
        # first part decides; the next only breaks ties (scores are on a 0..1 grid)
        key = np.zeros(len(P))
        for j in range(P.shape[1]):
            key = key * 1000.0 + np.round(P[:, j] * 999)
        return key
    raise ValueError(form)


def _form_scores(y: np.ndarray, P: np.ndarray) -> Dict[str, dict]:
    out = {}
    for form in FORMS:
        if form == "strict priority":
            best, best_order = -1.0, None
            for order in permutations(range(P.shape[1])):
                rho = spearman(combine(P[:, order], form), y)
                if rho > best:
                    best, best_order = rho, order
            out[form] = {"rho": best, "order": list(best_order)}
        else:
            out[form] = {"rho": spearman(combine(P, form), y)}
    return out


# ------------------------------------------------------------------ the three questions


def base_or_derived(cs: CaseScores, column: str, **kw) -> dict:
    """Is ``column`` a base dimension or made from other qualities? (Sina: "created how?")"""
    r = is_new_dimension(cs, column, **kw)
    if r.get("tested"):
        r["kind"] = "derived" if r["verdict"].startswith("combination") else "base (on these cases)"
    return r


def created_how(
    cs: CaseScores,
    target: str,
    parts: Sequence[str],
    n_perm: int = 200,
    min_cases: int = 8,
    seed: int = 0,
) -> dict:
    """Which operation builds ``target`` from ``parts`` best: sum, product, weakest part,
    strongest part or strict priority?

    Each part is rescaled to 0..1 over the cases that carry them all; no weights are
    fitted. The fit of each form is the rank correlation (Spearman) with the target. The
    whole search (every form, every priority order) is repeated with the target shuffled;
    ``p_best`` is the share of shuffled searches whose best form fits at least as well.
    The forms often fit almost equally well on few cases, so ``margin`` (best minus
    second best) matters as much as the winner.
    """
    parts = list(parts)
    if not parts or target in parts:
        raise ValueError("need parts that differ from the target")
    rows = cs.complete_rows([target, *parts])
    if len(rows) < min_cases:
        return {"target": target, "parts": parts, "tested": False,
                "reason": f"only {len(rows)} cases carry all of them"}
    y = cs.select([target])[rows, 0]
    P = _to01(cs.select(parts)[rows])
    obs = _form_scores(y, P)
    ranked = sorted(FORMS, key=lambda f: obs[f]["rho"], reverse=True)
    best = ranked[0]
    rng = np.random.default_rng(seed)
    null_best = np.empty(n_perm)
    for i in range(n_perm):
        ys = rng.permutation(y)
        null_best[i] = max(v["rho"] for v in _form_scores(ys, P).values())
    p = float((np.sum(null_best >= obs[best]["rho"]) + 1) / (n_perm + 1))
    if len(parts) > 1 and "order" in obs["strict priority"]:
        obs["strict priority"]["order"] = [parts[k] for k in obs["strict priority"]["order"]]
    return {
        "target": target,
        "parts": parts,
        "tested": True,
        "n_cases": int(len(rows)),
        "forms": obs,
        "best_form": best,
        "best_rho": obs[best]["rho"],
        "margin": obs[best]["rho"] - obs[ranked[1]]["rho"],
        "shuffled_best_mean": float(null_best.mean()),
        "p_best": p,
    }


def equilibrium(
    cs: CaseScores,
    columns: Sequence[str],
    n_perm: int = 200,
    min_cases: int = 8,
    seed: int = 0,
) -> dict:
    """Is there a weighted sum of these qualities that hardly changes from case to case?

    This is Sina's building question (forces sum to zero) and axiom G9 in data form. On
    the cases that carry every column, the qualities are put on one scale (z-scores) and
    the direction with the least spread is found (the smallest principal component).
    Its share of the total spread is compared with the same search on cases whose
    qualities were shuffled one by one. A share well below the shuffled ones says the
    weights describe a balance these cases keep; ``p`` is the share of shuffled sets at
    least as balanced.
    """
    columns = list(columns)
    rows = cs.complete_rows(columns)
    if len(rows) < max(min_cases, len(columns) + 2):
        return {"columns": columns, "tested": False,
                "reason": f"only {len(rows)} cases carry all {len(columns)} qualities"}
    X = standardise(cs.select(columns)[rows])
    keep = np.std(X, axis=0) > 0
    X, cols = X[:, keep], [c for c, k in zip(columns, keep) if k]
    if X.shape[1] < 2:
        return {"columns": columns, "tested": False, "reason": "fewer than two qualities vary"}

    def least(Z):
        Z = Z - Z.mean(axis=0)
        eig, vec = np.linalg.eigh(Z.T @ Z / max(len(Z) - 1, 1))
        return float(eig[0] / max(eig.sum(), 1e-12)), vec[:, 0]

    share, w = least(X)
    rng = np.random.default_rng(seed)
    null = np.array([least(np.column_stack([rng.permutation(c) for c in X.T]))[0] for _ in range(n_perm)])
    p = float((np.sum(null <= share) + 1) / (n_perm + 1))
    w = w / np.max(np.abs(w))
    order = np.argsort(-np.abs(w))
    return {
        "columns": cols,
        "tested": True,
        "n_cases": int(len(rows)),
        "least_spread_share": share,
        "even_share": 1.0 / X.shape[1],
        "shuffled_mean": float(null.mean()),
        "p_at_least_as_balanced": p,
        "weights": {cols[i]: float(w[i]) for i in order},
    }
