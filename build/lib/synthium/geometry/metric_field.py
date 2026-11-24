"""A metric that changes from place to place, and the curvature it implies.

This is the part V4 promised but left at zero. Given any smooth metric field
``g(x)`` it computes, by finite differences:

* Christoffel symbols  Gamma^i_jk = 1/2 g^il (d_k g_lj + d_j g_lk - d_l g_jk)
* Riemann tensor       R^r_smn = d_m Gamma^r_ns - d_n Gamma^r_ms
                                 + Gamma^r_ml Gamma^l_ns - Gamma^r_nl Gamma^l_ms
* Ricci tensor         R_sn = R^r_srn
* Scalar curvature     R = g^sn R_sn
* Geodesics            x'' = -Gamma^i_jk x'^j x'^k  (Runge-Kutta 4)

Checked in the tests on a sphere of radius r (scalar curvature 2 / r^2) and on flat
space (0).

:func:`metric_field_from_cases` builds a metric field from the cases themselves: near
each place, the metric is the inverse of the spread of nearby cases (weighted by a
Gaussian). Where cases bunch tightly along a direction, a step in that direction
counts as long. With few cases this is rough; use it in two or three dimensions only.

UNTESTED on case data: the curvature of a ranking space has no meaning yet beyond
"the spread of cases changes from one region to the next".
"""

from __future__ import annotations

from typing import Callable

import numpy as np


class MetricField:
    def __init__(self, g: Callable[[np.ndarray], np.ndarray], dim: int, h: float = 1e-3):
        self.g = g
        self.dim = dim
        self.h = h

    def metric(self, x) -> np.ndarray:
        return np.asarray(self.g(np.asarray(x, float)), float)

    def _dg(self, x: np.ndarray) -> np.ndarray:
        """dg[k, i, j] = d g_ij / d x^k."""
        n, h = self.dim, self.h
        out = np.zeros((n, n, n))
        for k in range(n):
            e = np.zeros(n)
            e[k] = h
            out[k] = (self.metric(x + e) - self.metric(x - e)) / (2 * h)
        return out

    def christoffel(self, x) -> np.ndarray:
        """Gamma[i, j, k] = Gamma^i_jk at x."""
        x = np.asarray(x, float)
        ginv = np.linalg.inv(self.metric(x))
        dg = self._dg(x)  # dg[k, l, j] = d_k g_lj
        # term[l, j, k] = d_k g_lj + d_j g_lk - d_l g_jk
        term = (
            np.transpose(dg, (1, 2, 0))  # d_k g_lj -> [l, j, k]
            + np.transpose(dg, (1, 0, 2))  # d_j g_lk -> [l, j, k]
            - dg  # d_l g_jk -> [l, j, k]
        )
        return 0.5 * np.einsum("il,ljk->ijk", ginv, term)

    def riemann(self, x) -> np.ndarray:
        """R[r, s, m, n] = R^r_smn at x."""
        x = np.asarray(x, float)
        n, h = self.dim, self.h
        G = self.christoffel(x)
        dG = np.zeros((n, n, n, n))  # dG[m, r, a, b] = d_m Gamma^r_ab
        for m in range(n):
            e = np.zeros(n)
            e[m] = h
            dG[m] = (self.christoffel(x + e) - self.christoffel(x - e)) / (2 * h)
        R = (
            np.einsum("mrns->rsmn", dG)  # d_m Gamma^r_ns
            - np.einsum("nrms->rsmn", dG)  # d_n Gamma^r_ms
            + np.einsum("rml,lns->rsmn", G, G)
            - np.einsum("rnl,lms->rsmn", G, G)
        )
        return R

    def ricci(self, x) -> np.ndarray:
        return np.einsum("rsrn->sn", self.riemann(x))

    def scalar_curvature(self, x) -> float:
        ginv = np.linalg.inv(self.metric(x))
        return float(np.einsum("sn,sn->", ginv, self.ricci(x)))

    def geodesic(self, x0, v0, t_end: float = 1.0, steps: int = 200) -> np.ndarray:
        """Follow the straightest path from x0 with starting velocity v0 (RK4)."""
        x = np.asarray(x0, float).copy()
        v = np.asarray(v0, float).copy()
        dt = t_end / steps

        def acc(xx, vv):
            return -np.einsum("ijk,j,k->i", self.christoffel(xx), vv, vv)

        path = [x.copy()]
        for _ in range(steps):
            k1x, k1v = v, acc(x, v)
            k2x, k2v = v + 0.5 * dt * k1v, acc(x + 0.5 * dt * k1x, v + 0.5 * dt * k1v)
            k3x, k3v = v + 0.5 * dt * k2v, acc(x + 0.5 * dt * k2x, v + 0.5 * dt * k2v)
            k4x, k4v = v + dt * k3v, acc(x + dt * k3x, v + dt * k3v)
            x = x + dt / 6 * (k1x + 2 * k2x + 2 * k3x + k4x)
            v = v + dt / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
            path.append(x.copy())
        return np.asarray(path)

    def path_length(self, path: np.ndarray) -> float:
        path = np.asarray(path, float)
        total = 0.0
        for a, b in zip(path[:-1], path[1:]):
            mid = (a + b) / 2
            d = b - a
            total += float(np.sqrt(max(0.0, d @ self.metric(mid) @ d)))
        return total


def sphere_metric(radius: float = 1.0) -> MetricField:
    """Surface of a sphere in (theta, phi): ds^2 = r^2 dtheta^2 + r^2 sin^2(theta) dphi^2."""

    def g(x):
        return np.diag([radius**2, (radius * np.sin(x[0])) ** 2])

    return MetricField(g, 2)


def metric_field_from_cases(
    X: np.ndarray, bandwidth: float = 1.0, ridge: float = 1e-2
) -> MetricField:
    """Metric at x = inverse of the Gaussian-weighted spread of cases around x."""
    X = np.asarray(X, float)
    if np.isnan(X).any():
        raise ValueError("needs complete rows")
    n, d = X.shape

    def g(x):
        w = np.exp(-0.5 * np.sum((X - x) ** 2, axis=1) / bandwidth**2)
        w = w / max(w.sum(), 1e-300)
        mu = w @ X
        C = (X - mu).T @ ((X - mu) * w[:, None])
        C += ridge * np.eye(d)
        return np.linalg.inv(C)

    return MetricField(g, d)
