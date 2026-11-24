"""How many dimensions the cases really span (restored from V4, with a chance baseline).

V4 counted a dimension as real when it explained more than 1% of the variance. With
few cases, random noise passes that bar easily. Here a dimension counts only when it
beats what the same qualities give after shuffling (parallel analysis).

:func:`build_up` follows Sina's picture: a dot, extended into a line, the line into an
area, the area into a volume. Each case is a point; qualities are added one at a time;
each step reports what the new dimension adds that the earlier ones did not already
hold.

UNTESTED: these are shapes of rankings with no real unit yet.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Sequence

import numpy as np

from .scores import CaseScores, standardise

STEP_NAMES = {0: "dot", 1: "line", 2: "area", 3: "volume"}


def step_name(k: int) -> str:
    return STEP_NAMES.get(k, f"{k}-volume")


def correlation_eigenvalues(X: np.ndarray) -> np.ndarray:
    """Eigenvalues of the correlation matrix of complete rows, largest first."""
    Z = standardise(np.asarray(X, float))
    n = Z.shape[0]
    C = Z.T @ Z / max(n, 1)
    return np.sort(np.linalg.eigvalsh(C))[::-1]


def participation_ratio(eigs: np.ndarray) -> float:
    """Effective number of dimensions: (sum l)^2 / sum l^2. Equal spread on d axes gives d."""
    eigs = np.clip(np.asarray(eigs, float), 0, None)
    s2 = float(np.sum(eigs**2))
    return float(np.sum(eigs) ** 2 / s2) if s2 > 0 else 0.0


@dataclass
class PCAResult:
    eigenvalues: np.ndarray
    explained: np.ndarray
    loadings: np.ndarray  # rows = components, columns = qualities
    columns: List[str]
    n_cases: int

    def top_qualities(self, component: int, k: int = 3) -> List[str]:
        idx = np.argsort(np.abs(self.loadings[component]))[::-1][:k]
        return [f"{self.columns[i]} ({self.loadings[component, i]:+.2f})" for i in idx]


def pca(X: np.ndarray, columns: Sequence[str]) -> PCAResult:
    Z = standardise(np.asarray(X, float))
    n = Z.shape[0]
    C = Z.T @ Z / max(n, 1)
    vals, vecs = np.linalg.eigh(C)
    order = np.argsort(vals)[::-1]
    vals, vecs = vals[order], vecs[:, order]
    total = vals.sum() if vals.sum() > 0 else 1.0
    return PCAResult(vals, vals / total, vecs.T, list(columns), n)


def parallel_analysis(X: np.ndarray, n_perm: int = 200, seed: int = 0, q: float = 95) -> dict:
    """Count components whose eigenvalue beats the q-th percentile of shuffled data."""
    rng = np.random.default_rng(seed)
    X = np.asarray(X, float)
    real = correlation_eigenvalues(X)
    null = np.array(
        [
            correlation_eigenvalues(np.column_stack([rng.permutation(c) for c in X.T]))
            for _ in range(n_perm)
        ]
    )
    bar = np.percentile(null, q, axis=0)
    beats = real > bar
    n_real = int(np.argmin(beats)) if not beats.all() else len(beats)
    return {
        "eigenvalues": real.tolist(),
        "shuffled_bar": bar.tolist(),
        "dimensions_beating_chance": n_real,
        "participation_ratio": participation_ratio(real),
    }


def _new_share(Z: np.ndarray) -> float:
    """Share of the last column's spread not explained by the earlier columns."""
    y = Z[:, -1]
    if Z.shape[1] == 1 or np.var(y) == 0:
        return 1.0
    A = np.column_stack([np.ones(len(y)), Z[:, :-1]])
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ coef
    return float(np.var(resid) / np.var(y))


def _volume(Z: np.ndarray) -> float:
    """det(correlation): 1 when the qualities are independent, 0 when the cloud is flat."""
    n = Z.shape[0]
    C = Z.T @ Z / max(n, 1)
    return float(max(np.linalg.det(C), 0.0))


@dataclass
class BuildStep:
    k: int
    name: str
    added: Optional[str]
    n_cases: int
    case_ids: List[str]
    new_share: Optional[float]
    volume: Optional[float]
    volume_shuffled: Optional[float]
    participation_ratio: Optional[float]
    spread_added: Optional[float]


@dataclass
class BuildUp:
    steps: List[BuildStep] = field(default_factory=list)

    @property
    def order(self) -> List[str]:
        return [s.added for s in self.steps if s.added]


def choose_order(cs: CaseScores, max_dims: int = 10, min_cases: int = 8) -> List[str]:
    """Greedy order: start from the most-scored quality; then add whichever quality keeps
    the most cases that carry every quality chosen so far (ties: most-scored first)."""
    cov = cs.coverage()
    chosen: List[str] = []
    while len(chosen) < max_dims:
        best, best_n = None, -1
        for c in sorted(cs.columns, key=lambda c: -cov[c]):
            if c in chosen:
                continue
            n = len(cs.complete_rows(chosen + [c]))
            if n > best_n:
                best, best_n = c, n
        if best is None or best_n < min_cases:
            break
        chosen.append(best)
    return chosen


def build_up(
    cs: CaseScores,
    order: Optional[Sequence[str]] = None,
    min_cases: int = 8,
    n_perm: int = 100,
    seed: int = 0,
) -> BuildUp:
    """Dot -> line -> area -> volume: add one quality at a time and report each step."""
    rng = np.random.default_rng(seed)
    order = list(order) if order is not None else choose_order(cs, min_cases=min_cases)
    out = BuildUp()
    out.steps.append(
        BuildStep(0, "dot", None, cs.n_cases, list(cs.case_ids), None, None, None, None, None)
    )
    for k in range(1, len(order) + 1):
        cols = order[:k]
        rows = cs.complete_rows(cols)
        if len(rows) < min_cases:
            break
        X = cs.select(cols)[rows]
        Z = standardise(X)
        vol = _volume(Z) if k > 1 else None
        vol_null = None
        if k > 1:
            vols = []
            for _ in range(n_perm):
                Zs = np.column_stack([rng.permutation(c) for c in Z.T])
                vols.append(_volume(Zs))
            vol_null = float(np.mean(vols))
        out.steps.append(
            BuildStep(
                k=k,
                name=step_name(k),
                added=cols[-1],
                n_cases=int(len(rows)),
                case_ids=[cs.case_ids[i] for i in rows],
                new_share=_new_share(Z) if len(rows) > k + 1 else None,
                volume=vol,
                volume_shuffled=vol_null,
                participation_ratio=participation_ratio(correlation_eigenvalues(X)),
                spread_added=float(np.std(X[:, -1])),
            )
        )
    return out


def is_new_dimension(
    cs: CaseScores,
    column: str,
    max_predictors: int = 2,
    min_cases: int = 8,
    n_perm: int = 200,
    seed: int = 0,
) -> dict:
    """Is ``column`` a dimension of its own, or a combination of other qualities?

    For every pair (or single, with ``max_predictors=1``) of other qualities scored on at
    least ``min_cases`` of the same cases, fit ``column`` from them in a straight line
    and keep the best fit (R^2). Searching many pairs finds a good fit by luck, so the
    same search is repeated with ``column`` shuffled; ``p`` is the share of shuffled
    searches that fit at least as well. A high best R^2 with a small ``p`` says the
    quality is (mostly) a combination of the predictors named; otherwise it counts as a
    new dimension on the cases we have.
    """
    from itertools import combinations

    rng = np.random.default_rng(seed)
    j = cs.columns.index(column)
    others = [c for c in cs.columns if c != column]
    candidates = []
    for size in range(1, max_predictors + 1):
        for combo in combinations(others, size):
            rows = cs.complete_rows([column, *combo])
            if len(rows) >= max(min_cases, size + 3):
                candidates.append((combo, rows))

    def r2(y, X):
        A = np.column_stack([np.ones(len(y)), X])
        coef, *_ = np.linalg.lstsq(A, y, rcond=None)
        res = y - A @ coef
        v = np.var(y)
        return 0.0 if v == 0 else 1.0 - np.var(res) / v

    def best(shuffle: bool):
        top, top_combo, top_n = -1.0, None, 0
        for combo, rows in candidates:
            y = cs.values[rows, j]
            if shuffle:
                y = rng.permutation(y)
            X = cs.select(list(combo))[rows]
            # Adjusted R^2 so bigger predictor sets do not win by size alone.
            n, k = len(y), len(combo)
            val = r2(y, X)
            adj = 1 - (1 - val) * (n - 1) / max(n - k - 1, 1)
            if adj > top:
                top, top_combo, top_n = adj, combo, n
        return top, top_combo, top_n

    if not candidates:
        return {"column": column, "tested": False, "reason": "too few shared cases"}
    obs, combo, n = best(False)
    null = np.array([best(True)[0] for _ in range(n_perm)])
    p = float((np.sum(null >= obs) + 1) / (n_perm + 1))
    return {
        "column": column,
        "tested": True,
        "best_adj_r2": float(obs),
        "best_predictors": list(combo),
        "n_cases": int(n),
        "pairs_searched": len(candidates),
        "shuffled_best_mean": float(null.mean()),
        "p": p,
        "verdict": "combination of others" if (p < 0.05 and obs >= 0.5) else "new dimension (on these cases)",
    }


def estimate_dimensions(cs: CaseScores, min_cases: int = 8, **kw) -> dict:
    """How many real dimensions do the cases need? Runs :func:`is_new_dimension` on every
    quality scored on at least ``min_cases`` cases."""
    cov = cs.coverage()
    results = [
        is_new_dimension(cs, c, min_cases=min_cases, **kw)
        for c in cs.columns
        if cov[c] >= min_cases
    ]
    tested = [r for r in results if r.get("tested")]
    new = [r["column"] for r in tested if r["verdict"].startswith("new")]
    combos = [r["column"] for r in tested if not r["verdict"].startswith("new")]
    return {
        "domain": cs.domain,
        "qualities_tested": len(tested),
        "new_dimensions": new,
        "combinations": combos,
        "untested": [c for c in cs.columns if cov[c] < min_cases or c not in {r["column"] for r in tested}],
        "results": results,
    }


def compare_domains(a: CaseScores, b: CaseScores, min_cases: int = 8) -> dict:
    """Shared versus domain-specific dimensions between two domains' case tables.

    Qualities are matched by name after dropping the ``Qnn_`` prefix (so a markets table
    that also scores ``opportunistic`` lines up with ``Q23_opportunistic``)."""
    import re as _re

    def bare(c):
        return _re.sub(r"^Q\d+[a-z]?_", "", c)

    ea, eb = estimate_dimensions(a, min_cases), estimate_dimensions(b, min_cases)
    na = {bare(c) for c in ea["new_dimensions"]}
    nb = {bare(c) for c in eb["new_dimensions"]}
    sa = {bare(c) for c in a.columns}
    sb = {bare(c) for c in b.columns}
    return {
        "domains": [a.domain, b.domain],
        "scored_in_both": sorted(sa & sb),
        "new_dimension_in_both": sorted(na & nb),
        f"only_{a.domain}": sorted(na - sb),
        f"only_{b.domain}": sorted(nb - sa),
    }
