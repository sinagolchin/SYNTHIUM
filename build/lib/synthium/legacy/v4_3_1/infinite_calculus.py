from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple
import numpy as np
from scipy.integrate import trapezoid

@dataclass
class DerivativeEstimate:
    value: float
    uncertainty: float
    stable: bool

class RobustDerivativeChain:
    def __init__(self, base_function: Callable[[float], float], dt_candidates: Tuple[float, ...] = (1e-2, 5e-3, 1e-3)):
        self.base_function = base_function
        self.dt_candidates = dt_candidates
        self.estimates: Dict[int, DerivativeEstimate] = {}

    def compute(self, t: float, max_order: int = 6) -> Dict[int, DerivativeEstimate]:
        funcs: List[Callable[[float], float]] = [self.base_function]
        self.estimates = {0: DerivativeEstimate(float(self.base_function(t)), 0.0, True)}
        for order in range(1, max_order + 1):
            prev_f = funcs[-1]
            est = self._robust_derivative(prev_f, t)
            self.estimates[order] = est
            funcs.append(lambda x, f=prev_f: self._robust_derivative(f, x).value)
        return self.estimates

    def _robust_derivative(self, f: Callable[[float], float], x: float) -> DerivativeEstimate:
        vals = []
        for dt in self.dt_candidates:
            try:
                val = (f(x + dt) - f(x - dt)) / (2.0 * dt)
                if np.isfinite(val):
                    vals.append(float(val))
            except Exception:
                continue
        if not vals:
            return DerivativeEstimate(0.0, float("inf"), False)
        arr = np.asarray(vals)
        med = float(np.median(arr))
        mad = float(np.median(np.abs(arr - med)))
        stable = mad <= max(1e-6, 0.15 * (abs(med) + 1e-9))
        return DerivativeEstimate(med, mad, stable)

    def flatten_values(self) -> Dict[int, float]:
        return {k: v.value for k, v in self.estimates.items()}

    def chaos_score(self, order: int = 6) -> float:
        est = self.estimates.get(order)
        if est is None:
            return 0.0
        penalty = 2.0 if not est.stable else 1.0
        return abs(est.value) * penalty

class NDimensionalIntegral:
    @staticmethod
    def integrate_1d(f: Callable[[float], float], a: float, b: float, n_points: int = 1000) -> float:
        x = np.linspace(a, b, n_points)
        y = np.array([f(xi) for xi in x], dtype=float)
        return float(trapezoid(y, x))

    @staticmethod
    def integrate_nd(f: Callable[[np.ndarray], float], ranges: List[Tuple[float, float]], n_samples: int = 100000) -> float:
        samples = np.random.uniform(
            low=[r[0] for r in ranges],
            high=[r[1] for r in ranges],
            size=(n_samples, len(ranges)),
        )
        values = np.array([f(sample) for sample in samples], dtype=float)
        box_volume = np.prod([r[1] - r[0] for r in ranges])
        return float(box_volume * np.mean(values))

def integrate_along_path(f: Callable[[np.ndarray], float], path: np.ndarray) -> float:
    values = np.array([f(point) for point in path], dtype=float)
    segments = np.linalg.norm(np.diff(path, axis=0), axis=1)
    return float(np.sum((values[:-1] + values[1:]) * 0.5 * segments))
