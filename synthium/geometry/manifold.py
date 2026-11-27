"""The quality space as a Riemannian manifold (restored from V4, completed).

V4 gave the space one constant metric. With a constant metric the space is flat, so
V4's curvature was always zero and every geodesic a straight line. That part is kept
here, unchanged in meaning, as :class:`RiemannianManifold`.

Two things are added so the geometry can show more than a flat space:

* :func:`data_geodesics`: shortest paths that stay close to where the cases actually
  are (a path that must hop from case to near case), instead of a straight line through
  empty space. When these paths are much longer than straight lines, the cloud of cases
  is folded or curved.
* :mod:`synthium.geometry.metric_field`: a metric that changes from place to place,
  with real Christoffel symbols and curvature.

UNTESTED: distances are between rankings with no real unit yet.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np


@dataclass
class GeodesicPath:
    points: np.ndarray
    length: float
    parameterization: np.ndarray


class RiemannianManifold:
    """A space with one constant metric ``g``: ds^2 = g_ij dx^i dx^j (V4 semantics)."""

    def __init__(self, dimension: int, metric: Optional[np.ndarray] = None):
        self.dim = dimension
        if metric is None:
            metric = np.eye(dimension)
        metric = np.asarray(metric, dtype=float)
        if metric.shape != (dimension, dimension):
            raise ValueError("metric must be dim x dim")
        if not np.allclose(metric, metric.T):
            raise ValueError("metric must be symmetric")
        if np.min(np.linalg.eigvalsh(metric)) <= 0:
            raise ValueError("metric must be positive definite")
        self.metric = metric
        self.metric_inv = np.linalg.inv(metric)

    def distance(self, p: np.ndarray, q: np.ndarray) -> float:
        d = np.asarray(q, float) - np.asarray(p, float)
        return float(np.sqrt(max(0.0, d @ self.metric @ d)))

    def inner_product(self, v: np.ndarray, w: np.ndarray) -> float:
        return float(np.asarray(v) @ self.metric @ np.asarray(w))

    def norm(self, v: np.ndarray) -> float:
        return float(np.sqrt(max(0.0, self.inner_product(v, v))))

    def geodesic(self, start, end, num_points: int = 100) -> GeodesicPath:
        """With a constant metric the shortest path is the straight line."""
        start, end = np.asarray(start, float), np.asarray(end, float)
        t = np.linspace(0.0, 1.0, num_points)
        pts = np.outer(1 - t, start) + np.outer(t, end)
        return GeodesicPath(pts, self.distance(start, end), t)

    def christoffel_symbols(self) -> np.ndarray:
        """Zero: a constant metric has no Christoffel symbols. See metric_field for more."""
        return np.zeros((self.dim,) * 3)

    def riemann_curvature(self) -> np.ndarray:
        return np.zeros((self.dim,) * 4)

    def scalar_curvature(self) -> float:
        return 0.0

    def pairwise(self, X: np.ndarray) -> np.ndarray:
        """All distances between the rows of ``X`` (no missing values allowed)."""
        X = np.asarray(X, float)
        diff = X[:, None, :] - X[None, :, :]
        sq = np.einsum("ijk,kl,ijl->ij", diff, self.metric, diff)
        return np.sqrt(np.maximum(sq, 0.0))


def learn_metric_from_data(
    data: np.ndarray, method: str = "mahalanobis", shrinkage: Optional[float] = None
) -> np.ndarray:
    """Learn a constant metric from complete rows of ``data``.

    ``'mahalanobis'`` (default here) uses the inverse covariance: two qualities that
    always move together count once, not twice, and a quality on a wide scale does not
    dominate. ``'covariance'`` is V4's original default and is kept for comparison; it
    does the opposite and stretches the directions where cases already differ most.
    ``'identity'`` is the plain straight-line distance.

    ``shrinkage`` (0..1) pulls the covariance toward its diagonal, which keeps the
    inverse stable when there are few cases per quality. When omitted it is set to
    ``min(1, n_features / n_samples)``.
    """
    data = np.asarray(data, float)
    if np.isnan(data).any():
        raise ValueError("learn_metric_from_data needs complete rows (no NaN)")
    n, d = data.shape
    if method == "identity":
        return np.eye(d)
    centred = data - data.mean(axis=0)
    cov = centred.T @ centred / max(n - 1, 1)
    if shrinkage is None:
        shrinkage = min(1.0, d / max(n, 1))
    target = np.diag(np.diag(cov))
    cov = (1 - shrinkage) * cov + shrinkage * target
    cov += np.eye(d) * 1e-9 * max(1.0, float(np.trace(cov)))
    if method == "covariance":
        return cov
    if method == "mahalanobis":
        return np.linalg.inv(cov)
    raise ValueError(f"unknown method: {method}")


def pairwise_distances_missing(
    Z: np.ndarray, min_shared: int = 3
) -> Tuple[np.ndarray, np.ndarray]:
    """Distances between cases that do not all carry the same qualities.

    ``Z`` should be standardised (see ``scores.standardise``). The distance between two
    cases is the root mean square difference over the qualities both carry. Pairs that
    share fewer than ``min_shared`` qualities get NaN. Returns ``(D, shared_counts)``.
    """
    Z = np.asarray(Z, float)
    present = ~np.isnan(Z)
    Z0 = np.where(present, Z, 0.0)
    P = present.astype(float)
    shared = P @ P.T
    sq = (Z0**2) @ P.T + P @ (Z0**2).T - 2 * Z0 @ Z0.T
    with np.errstate(invalid="ignore", divide="ignore"):
        D = np.sqrt(np.maximum(sq, 0.0) / shared)
    D[shared < min_shared] = np.nan
    np.fill_diagonal(D, 0.0)
    return D, shared.astype(int)


def data_geodesics(D: np.ndarray, k: int = 5) -> np.ndarray:
    """Shortest paths that hop between near cases (each case linked to its k nearest).

    ``D`` is a full distance matrix (NaN = unknown, treated as no link). Returns a matrix
    of path lengths; ``inf`` where two cases cannot reach each other.
    """
    D = np.asarray(D, float)
    n = D.shape[0]
    W = np.full((n, n), np.inf)
    Dm = np.where(np.isnan(D), np.inf, D)
    for i in range(n):
        order = np.argsort(Dm[i])
        nbrs = [j for j in order if j != i and np.isfinite(Dm[i, j])][:k]
        for j in nbrs:
            W[i, j] = W[j, i] = Dm[i, j]
    np.fill_diagonal(W, 0.0)
    G = W.copy()
    for m in range(n):  # Floyd-Warshall
        G = np.minimum(G, G[:, m : m + 1] + G[m : m + 1, :])
    return G


def curvature_index(X: np.ndarray, k: int = 5, far_share: float = 0.25) -> float:
    """Mean of (path along the cases) / (straight line) over the farthest pairs.

    A fold shows most between cases far apart: on a circle, opposite points are pi/2
    times farther along the circle than straight across. Only the ``far_share`` of
    reachable pairs with the largest straight-line distance are used. Hopping between
    neighbours always adds a little, so the number only means something next to a
    shuffled baseline: see :func:`curvature_index_vs_shuffled`.
    """
    X = np.asarray(X, float)
    D = RiemannianManifold(X.shape[1]).pairwise(X)
    G = data_geodesics(D, k)
    mask = np.isfinite(G) & (D > 0)
    if not mask.any():
        return float("nan")
    far = mask & (D >= np.quantile(D[mask], 1 - far_share))
    return float(np.mean(G[far] / D[far]))


def curvature_index_vs_shuffled(
    X: np.ndarray, k: int = 5, n_perm: int = 200, seed: int = 0
) -> dict:
    """Compare the cases' curvature index with clouds whose qualities were shuffled.

    Shuffling each quality on its own keeps how spread out every quality is but breaks
    any shape the qualities make together. ``p`` is the share of shuffled clouds at
    least as folded as the real one; a small ``p`` says the real cloud has a fold the
    shuffles do not.
    """
    rng = np.random.default_rng(seed)
    X = np.asarray(X, float)
    observed = curvature_index(X, k)
    D = RiemannianManifold(X.shape[1]).pairwise(X)
    connected = float(np.mean(np.isfinite(data_geodesics(D, k))))
    null = []
    for _ in range(n_perm):
        Xs = np.column_stack([rng.permutation(col) for col in X.T])
        null.append(curvature_index(Xs, k))
    null = np.asarray(null)
    return {
        "observed": observed,
        "shuffled_mean": float(np.nanmean(null)),
        "shuffled_sd": float(np.nanstd(null)),
        "p_at_least_as_folded": float((np.sum(null >= observed) + 1) / (len(null) + 1)),
        "k": k,
        "share_of_pairs_connected": connected,
        "n_cases": int(X.shape[0]),
        "n_dims": int(X.shape[1]),
    }
