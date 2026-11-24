from __future__ import annotations
import numpy as np
from .applications import AnomalyGovernanceMonitor
from .dimensional_discovery import DimensionalDiscoveryEngine
from .manifold_geometry import RiemannianManifold
from .reality_state import RealityState


def main():
    np.random.seed(42)
    print("=" * 70)
    print(" SYNTHIUM v4.2 - IMPROVED COHERENCE AND GOVERNANCE ")
    print("=" * 70)

    baseline = np.random.randn(250, 5)
    engine = DimensionalDiscoveryEngine()
    analysis = engine.discover(baseline, method="pca", max_components=5)
    print(f"Discovered dimensions: {analysis.intrinsic_dimensions} via {analysis.method}")
    print(f"Stability score: {analysis.stability_score:.3f}")
    print(f"Interpretations: {analysis.interpretations[:2]}")

    monitor = AnomalyGovernanceMonitor(baseline, chaos_threshold=5e2)

    semantic = np.array([0.4, 0.2, 0.1, 0.3, 0.2])
    behavioral = np.array([0.9, 0.2, 0.1, 0.8, 0.2])

    def trajectory(t: float) -> float:
        return np.sin(t) * np.exp(t / 3.0)

    report = monitor.evaluate(semantic, behavioral, trajectory, t=10.0)
    print(f"Fusion score: {report.state_summary['fusion_score']:.3f}")
    print(f"Mismatch score: {report.state_summary['mismatch_score']:.3f}")
    print(f"Governance action: {report.decision.action.name}")
    print(f"Risk score: {report.decision.risk_score:.3f}")
    print(f"Justification: {report.decision.justification}")

    manifold = RiemannianManifold(5, metric=np.eye(5), metric_field=lambda x: np.eye(5) * (1.0 + 0.05 * np.linalg.norm(x)))
    state = RealityState(semantic, manifold, behavioral)
    print(f"Local curvature proxy at semantic point: {manifold.local_curvature_proxy(semantic):.6f}")
    print(f"Fusion breakdown keys: {list(state.to_dict().keys())}")

if __name__ == "__main__":
    main()
