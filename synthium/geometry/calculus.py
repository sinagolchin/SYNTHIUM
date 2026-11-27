"""Rates of change and integrals (restored from V4's infinite_calculus, made safe).

V4 differentiated a formula again and again with a step of 1e-6. Past the third order
that returns floating point noise, and its "chaos" test on the 6th derivative mostly
measured that noise. Here:

* :func:`derivative_chain` differentiates a function with a step chosen for the order,
  and :func:`InfiniteDerivativeChain` keeps V4's interface on top of it.
* :func:`rate_along` gives the rate of change of a quality along an ordering of cases
  (reading order, or filing date), next to a shuffled-order baseline. Cases are separate
  events, not one moving body, so a rate here describes the sample: which cases were
  picked, and whether the scoring drifted while they were read.
* :func:`integrate_along_path`, :func:`integrate_1d`, :func:`integrate_nd` are V4's
  integrals, written with numpy only.

UNTESTED on case data.
"""

from __future__ import annotations

from math import comb
from typing import Callable, Dict, List, Sequence, Tuple

import numpy as np


def derivative(f: Callable[[float], float], x: float, order: int = 1, h: float = None) -> float:
    """n-th derivative by one central difference stencil (not nested)."""
    if order == 0:
        return float(f(x))
    if h is None:
        h = 1e-2 * max(1.0, abs(x)) ** 0.5 * (1.0 if order > 2 else 1e-1)
    total = 0.0
    for i in range(order + 1):
        total += (-1) ** i * comb(order, i) * f(x + (order / 2 - i) * h)
    return float(total / h**order)


def derivative_chain(f: Callable[[float], float], x: float, max_order: int = 4) -> Dict[int, float]:
    return {n: derivative(f, x, n) for n in range(max_order + 1)}


class InfiniteDerivativeChain:
    """V4 interface: position, velocity, acceleration, jerk, snap, ..."""

    NAMES = {
        0: "Position (state)",
        1: "Velocity (rate of change)",
        2: "Acceleration (rate of rate of change)",
        3: "Jerk",
        4: "Snap",
        5: "Crackle",
        6: "Pop",
    }

    def __init__(self, base_function: Callable[[float], float]):
        self.base_function = base_function
        self.derivatives: Dict[int, float] = {}

    def compute(self, t: float, max_order: int = 4) -> Dict[int, float]:
        self.derivatives = derivative_chain(self.base_function, t, max_order)
        return self.derivatives

    def interpret(self) -> Dict[str, float]:
        return {self.NAMES.get(k, f"Derivative order {k}"): v for k, v in self.derivatives.items()}


def _smooth(y: np.ndarray, window: int) -> np.ndarray:
    if window <= 1:
        return y
    kernel = np.ones(window) / window
    pad = window // 2
    yp = np.pad(y, (pad, window - 1 - pad), mode="edge")
    return np.convolve(yp, kernel, mode="valid")


def rate_along(
    t: Sequence[float],
    y: Sequence[float],
    window: int = 5,
    n_perm: int = 500,
    seed: int = 0,
) -> dict:
    """Rate of change of y along t, from a straight-line fit plus smoothed derivatives.

    Returns the slope (change in y per unit of t), the smoothed velocity and
    acceleration series, and ``p``: the share of random orderings of the same values
    that give a slope at least as steep. Missing values are dropped.
    """
    t = np.asarray(t, float)
    y = np.asarray(y, float)
    ok = ~(np.isnan(t) | np.isnan(y))
    t, y = t[ok], y[ok]
    if len(t) < 4 or np.ptp(t) == 0:
        return {"n": int(len(t)), "slope": float("nan"), "p_slope": float("nan")}
    order = np.argsort(t, kind="stable")
    t, y = t[order], y[order]
    slope = float(np.polyfit(t, y, 1)[0])
    rng = np.random.default_rng(seed)
    null = np.array([np.polyfit(t, rng.permutation(y), 1)[0] for _ in range(n_perm)])
    p = float((np.sum(np.abs(null) >= abs(slope)) + 1) / (n_perm + 1))
    ys = _smooth(y, window)
    # Distinct t values only for np.gradient
    tu, inv = np.unique(t, return_inverse=True)
    yu = np.array([ys[inv == i].mean() for i in range(len(tu))])
    vel = np.gradient(yu, tu) if len(tu) > 2 else np.array([])
    acc = np.gradient(vel, tu) if len(tu) > 2 else np.array([])
    return {
        "n": int(len(t)),
        "slope": slope,
        "p_slope": p,
        "t": tu.tolist(),
        "smoothed": yu.tolist(),
        "velocity": vel.tolist(),
        "acceleration": acc.tolist(),
    }


def integrate_along_path(f: Callable[[np.ndarray], float], path: np.ndarray) -> float:
    """Line integral of f along a path of points (trapezoid rule)."""
    path = np.asarray(path, float)
    vals = np.array([f(p) for p in path])
    seg = np.linalg.norm(np.diff(path, axis=0), axis=1)
    return float(np.sum((vals[:-1] + vals[1:]) / 2 * seg))


def integrate_1d(f: Callable[[float], float], a: float, b: float, n_points: int = 1001) -> float:
    x = np.linspace(a, b, n_points)
    y = np.array([f(v) for v in x])
    return float(np.sum((y[:-1] + y[1:]) / 2 * np.diff(x)))


def integrate_nd(
    f: Callable[[np.ndarray], float],
    ranges: List[Tuple[float, float]],
    n_samples: int = 20000,
    seed: int = 0,
) -> float:
    """Monte Carlo integral over a box."""
    rng = np.random.default_rng(seed)
    lo = np.array([r[0] for r in ranges], float)
    hi = np.array([r[1] for r in ranges], float)
    pts = rng.uniform(lo, hi, size=(n_samples, len(ranges)))
    vals = np.array([f(p) for p in pts])
    return float(np.prod(hi - lo) * vals.mean())
