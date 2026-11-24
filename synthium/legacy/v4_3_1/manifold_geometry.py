from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Optional
import numpy as np

@dataclass
class GeodesicPath:
    points: np.ndarray
    length: float
    parameterization: np.ndarray
    local_lengths: np.ndarray

class RiemannianManifold:
    def __init__(self, dimension: int, metric: Optional[np.ndarray] = None, metric_field: Optional[Callable[[np.ndarray], np.ndarray]] = None):
        self.dim = dimension
        self.metric = np.eye(dimension) if metric is None else np.asarray(metric, dtype=float)
        self.metric_field = metric_field
        self.metric_inv = np.linalg.inv(self.metric)

    def metric_at(self, point: Optional[np.ndarray] = None) -> np.ndarray:
        if self.metric_field is not None and point is not None:
            g = np.asarray(self.metric_field(np.asarray(point, dtype=float)), dtype=float)
            return 0.5 * (g + g.T) + np.eye(self.dim) * 1e-8
        return self.metric

    def distance(self, point1: np.ndarray, point2: np.ndarray, num_points: int = 64) -> float:
        if self.metric_field is None:
            diff = np.asarray(point2) - np.asarray(point1)
            return float(np.sqrt(max(0.0, diff @ self.metric @ diff)))
        path = self.approximate_geodesic(np.asarray(point1), np.asarray(point2), num_points=num_points)
        return path.length

    def inner_product(self, v1: np.ndarray, v2: np.ndarray, point: Optional[np.ndarray] = None) -> float:
        g = self.metric_at(point)
        return float(np.asarray(v1) @ g @ np.asarray(v2))

    def norm(self, vector: np.ndarray, point: Optional[np.ndarray] = None) -> float:
        return float(np.sqrt(max(0.0, self.inner_product(vector, vector, point))))

    def approximate_geodesic(self, start: np.ndarray, end: np.ndarray, num_points: int = 100) -> GeodesicPath:
        t = np.linspace(0.0, 1.0, num_points)
        points = np.outer(1.0 - t, start) + np.outer(t, end)
        local_lengths = []
        for i in range(len(points) - 1):
            mid = 0.5 * (points[i] + points[i + 1])
            diff = points[i + 1] - points[i]
            g = self.metric_at(mid)
            local_lengths.append(np.sqrt(max(0.0, diff @ g @ diff)))
        ll = np.asarray(local_lengths, dtype=float)
        return GeodesicPath(points=points, length=float(ll.sum()), parameterization=t, local_lengths=ll)

    def geodesic(self, start: np.ndarray, end: np.ndarray, num_points: int = 100) -> GeodesicPath:
        return self.approximate_geodesic(start, end, num_points=num_points)

    def local_curvature_proxy(self, point: np.ndarray, eps: float = 1e-3) -> float:
        if self.metric_field is None:
            return 0.0
        point = np.asarray(point, dtype=float)
        g0 = self.metric_at(point)
        diffs = []
        for k in range(self.dim):
            p_plus = point.copy(); p_plus[k] += eps
            p_minus = point.copy(); p_minus[k] -= eps
            gp = self.metric_at(p_plus)
            gm = self.metric_at(p_minus)
            diffs.append(np.linalg.norm((gp - gm) / (2.0 * eps)))
        return float(np.mean(diffs) / (np.linalg.norm(g0) + 1e-12))

def learn_metric_from_data(data: np.ndarray, method: str = "covariance") -> np.ndarray:
    X = np.asarray(data, dtype=float)
    n_samples, _ = X.shape
    Xc = X - X.mean(axis=0)
    cov = (Xc.T @ Xc) / max(1, n_samples)
    cov = 0.5 * (cov + cov.T) + np.eye(cov.shape[0]) * 1e-6
    if method == "covariance":
        return cov
    if method == "mahalanobis":
        return np.linalg.inv(cov)
    raise ValueError(f"Unknown method: {method}")
