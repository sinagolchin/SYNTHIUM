from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Dict
import numpy as np
from .confidence import Confidence, ConfidenceLevel
from .governance import GovernanceDecision, GovernanceEngine
from .infinite_calculus import RobustDerivativeChain
from .manifold_geometry import RiemannianManifold, learn_metric_from_data
from .reality_state import RealityState

@dataclass
class MonitoringDecision:
    decision: GovernanceDecision
    state_summary: Dict
    derivative_summary: Dict[int, float]
    uncertainty_summary: Dict[int, float]

class AnomalyGovernanceMonitor:
    def __init__(self, baseline_observations: np.ndarray, chaos_threshold: float = 1e4):
        metric = learn_metric_from_data(baseline_observations, method="mahalanobis")
        self.manifold = RiemannianManifold(baseline_observations.shape[1], metric=metric)
        self.governor = GovernanceEngine(chaos_threshold=chaos_threshold)
        self.confidence = Confidence(ConfidenceLevel.MODERATE, "Baseline-observation monitor", ["Thresholds heuristic"], numeric_score=0.65, source_type="empirical")

    def evaluate(self, semantic_coords: np.ndarray, behavioral_coords: np.ndarray, trajectory_fn: Callable[[float], float], t: float = 0.0) -> MonitoringDecision:
        state = RealityState(semantic_coords, self.manifold, behavioral_coords)
        chain = RobustDerivativeChain(trajectory_fn)
        estimates = chain.compute(t=t, max_order=6)
        derivs = {k: v.value for k, v in estimates.items()}
        uncert = {k: v.uncertainty for k, v in estimates.items()}
        decision = self.governor.evaluate_trajectory(derivs, state.fusion_score, derivative_uncertainty=uncert, confidence=self.confidence)
        return MonitoringDecision(decision, state.to_dict(), derivs, uncert)
