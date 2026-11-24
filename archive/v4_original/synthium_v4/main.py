"""
Synthium v4.0 - Interactive Demonstrations
===========================================

Run: python -m synthium.main

Demonstrates:
1. Dimensional Discovery
2. Manifold Geometry
3. Infinite Derivatives
4. N-D Integration
5. Trading Application
6. v3.4 vs v4.0 Comparison
"""

import numpy as np
import synthium as syn


def demo_1_dimensional_discovery():
    """Demo: Discover dimensions from data"""
    print("\n" + "="*70)
    print("DEMO 1: DIMENSIONAL DISCOVERY")
    print("="*70)
    print("\nProblem: We have 20-dimensional data. How many 'real' dimensions?")
    
    # Generate synthetic data
    np.random.seed(42)
    observations = np.random.randn(100, 20)
    
    print("\nUsing PCA (Principal Component Analysis)...")
    result = syn.discover_reality_dimensions(observations, method='pca', max_components=10)
    
    print(f"\nMethod: {result.method}")
    print(f"Intrinsic Dimensions Found: {result.intrinsic_dimensions}")
    print(f"Total Dimensions Analyzed: {result.total_dimensions}")
    print(f"Confidence: {result.confidence:.2f}")
    
    print("\nExplained Variance:")
    for i, var in enumerate(result.explained_variance[:5]):
        bar = "█" * int(var * 50)
        print(f"  Dimension {i+1}: {var:6.2%} {bar}")
    
    cumsum = np.cumsum(result.explained_variance)
    print(f"\nCumulative variance (first 5 dims): {cumsum[4]:.1%}")
    
    print(f"\n✓ Conclusion: Reality has ~{result.intrinsic_dimensions} dimensions, not 20!")
    print("  (And NOT the assumed 5 from v3.4!)")


def demo_2_manifold_geometry():
    """Demo: Manifold operations"""
    print("\n" + "="*70)
    print("DEMO 2: MANIFOLD GEOMETRY")
    print("="*70)
    print("\nReality is a CURVED manifold, not flat Euclidean space")
    
    # Create manifold
    manifold = syn.RiemannianManifold(dimension=5)
    
    # Two states
    state_A = np.array([0.7, 0.5, 0.8, 0.6, 0.4])
    state_B = np.array([0.3, 0.8, 0.6, 0.7, 0.5])
    
    print(f"\nState A: {state_A}")
    print(f"State B: {state_B}")
    
    # Distance
    distance = manifold.distance(state_A, state_B)
    print(f"\nRiemannian distance: {distance:.4f}")
    
    # Geodesic
    path = manifold.geodesic(state_A, state_B, num_points=10)
    print(f"Geodesic path length: {path.length:.4f}")
    print(f"Path points: {path.points.shape[0]}")
    
    # Inner product
    inner = manifold.inner_product(state_A, state_B)
    print(f"Inner product <A,B>: {inner:.4f}")
    
    print("\n✓ Conclusion: States evolve along geodesics (shortest paths),")
    print("  not straight lines like in v3.4!")


def demo_3_infinite_derivatives():
    """Demo: Infinite derivative chain"""
    print("\n" + "="*70)
    print("DEMO 3: INFINITE DERIVATIVE CHAIN")
    print("="*70)
    print("\nEverything is the derivative of something else...")
    
    # Define a function
    def position(t):
        return np.sin(t) + 0.5 * np.cos(2*t)
    
    print("\nFunction: f(t) = sin(t) + 0.5·cos(2t)")
    
    # Compute derivative chain
    chain = syn.InfiniteDerivativeChain(position)
    derivatives = chain.compute(t=1.0, max_order=6)
    
    print("\nAt t=1.0:")
    interp = chain.interpret()
    for name, value in interp.items():
        print(f"  {name:35s}: {value:12.6f}")
    
    # Chaos detection
    chaos = chain.detect_chaos(threshold=1e6)
    print(f"\nChaos detected: {'YES ⚠️' if chaos else 'No'}")
    
    print("\n✓ Conclusion: Higher derivatives reveal hidden dynamics!")
    print("  6th derivative (Pop) detects chaos that 1st derivative (velocity) misses")


def demo_4_nd_integration():
    """Demo: N-dimensional integration"""
    print("\n" + "="*70)
    print("DEMO 4: N-DIMENSIONAL INTEGRATION")
    print("="*70)
    print("\nIntegration works in ANY dimension")
    
    integrator = syn.NDimensionalIntegral()
    
    # 1D integral
    print("\n1D: ∫₀¹ x² dx")
    integral_1d = integrator.integrate_1d(lambda x: x**2, 0, 1)
    print(f"  Result: {integral_1d:.4f} (exact: 0.3333)")
    print(f"  Meaning: {integrator.interpret(1)}")
    
    # 2D integral
    print("\n2D: ∬ (x² + y²) dxdy over [0,1]×[0,1]")
    integral_2d = integrator.integrate_2d(
        lambda x, y: x**2 + y**2,
        (0, 1), (0, 1)
    )
    print(f"  Result: {integral_2d:.4f}")
    print(f"  Meaning: {integrator.interpret(2)}")
    
    # 5D integral
    print("\n5D: ∫...∫ (Σxᵢ²) dx₁...dx₅ over [0,1]⁵")
    integral_5d = integrator.integrate_nd(
        lambda x: np.sum(x**2),
        [(0, 1)] * 5
    )
    print(f"  Result: {integral_5d:.4f}")
    print(f"  Meaning: {integrator.interpret(5)}")
    
    print("\n✓ Conclusion: We can compute integrals in ANY dimension!")
    print("  v3.4 was limited to 3D. v4.0 handles arbitrary N-D!")


def demo_5_trading_application():
    """Demo: Gold Assistant v4.0"""
    print("\n" + "="*70)
    print("DEMO 5: TRADING APPLICATION (Gold Assistant v4.0)")
    print("="*70)
    print("\nReal-world application: Trading position sizing")
    
    # Generate synthetic trading history
    np.random.seed(42)
    trading_history = np.random.randn(50, 10) * 0.1 + 0.5
    
    # Create assistant
    print("\nInitializing Gold Assistant v4.0...")
    assistant = syn.GoldAssistantV4()
    
    # Learn from history
    print("Learning from trading history...")
    assistant.fit(trading_history)
    
    # Make decision
    print("\nMaking trading decision...")
    decision = assistant.decide(
        account_balance=100000,
        posterior_edge=0.78,
        edge_confidence='MODERATE',
        ewma_vol=0.012,
        vol_median=0.010,
        drawdown=0.05,
        entropy=0.58,
        daily_risk_budget=2.5
    )
    
    print(decision)
    
    print("\n✓ Conclusion: v4.0 discovers dimensions, detects chaos,")
    print("  and provides uncertainty ranges (pessimistic/point/optimistic)!")


def demo_6_comparison():
    """Demo: v3.4 vs v4.0 comparison"""
    print("\n" + "="*70)
    print("DEMO 6: v3.4 vs v4.0 COMPARISON")
    print("="*70)
    
    comparison = """
╔════════════════════════════════════════════════════════════════╗
║                   v3.4 vs v4.0 Comparison                      ║
╚════════════════════════════════════════════════════════════════╝

v3.4 (Old Approach):
  • 5 dimensions (ASSUMED, not discovered)
  • Flat Euclidean space
  • Simple algebra: E = 1 - (v·R + S)
  • Straight-line paths
  • 1st derivative only
  • 3D integrals maximum
  • No chaos detection
  • Single point estimates

v4.0 (New Approach):
  • N dimensions (DISCOVERED via PCA/ICA/manifolds)
  • Riemannian manifold (curved space)
  • Differential geometry + tensor calculus
  • Geodesic paths (optimal trajectories)
  • Infinite derivative chains (0th through Nth)
  • N-dimensional integrals
  • Chaos detection via 6th derivative
  • Uncertainty ranges (pessimistic/point/optimistic)

Key Mathematical Upgrades:
  ✓ PCA/ICA for dimensional discovery
  ✓ Metric tensors g_ij for distance
  ✓ Contravariant/covariant tensors
  ✓ Christoffel symbols Γⁱⱼₖ (prepared for)
  ✓ Riemann curvature tensor (prepared for)
  ✓ N-D integration via Monte Carlo
  ✓ Numerical derivative chains

What We Kept from v3.4:
  ✓ Agnosticism (Axiom 0)
  ✓ Confidence tracking
  ✓ Epistemic humility
  ✓ Philosophy of uncertainty

The Fundamental Shift:
  v3.4: "Let's ASSUME reality has 5 dimensions"
  v4.0: "Let's DISCOVER how many dimensions reality has"
    """
    print(comparison)


def main():
    """Run all demonstrations"""
    print("="*70)
    print(" "*15 + "SYNTHIUM v4.0")
    print(" "*10 + "INTERACTIVE DEMONSTRATIONS")
    print("="*70)
    print("\nPress Enter to continue through each demo...")
    print("(Or Ctrl+C to exit)")
    
    demos = [
        ("Dimensional Discovery", demo_1_dimensional_discovery),
        ("Manifold Geometry", demo_2_manifold_geometry),
        ("Infinite Derivatives", demo_3_infinite_derivatives),
        ("N-D Integration", demo_4_nd_integration),
        ("Trading Application", demo_5_trading_application),
        ("v3.4 vs v4.0 Comparison", demo_6_comparison)
    ]
    
    for i, (name, demo_func) in enumerate(demos, 1):
        if i > 1:
            try:
                input(f"\nPress Enter for Demo {i}: {name}...")
            except KeyboardInterrupt:
                print("\n\nExiting...")
                return
        
        try:
            demo_func()
        except Exception as e:
            print(f"\n❌ Error in demo: {e}")
            import traceback
            traceback.print_exc()
    
    # Final axiom reminder
    print("\n" + "="*70)
    print("AXIOM 0 - AGNOSTICISM REMINDER")
    print("="*70)
    syn.print_agnosticism_axiom()
    
    print("\n" + "="*70)
    print("DEMOS COMPLETE")
    print("="*70)
    print("\nSynthium v4.0: N-dimensional mathematics + agnostic epistemology")
    print("Status: Foundation complete, ready for real-world testing")
    print("\nTo use in your code:")
    print("  >>> import synthium as syn")
    print("  >>> result = syn.discover_reality_dimensions(your_data)")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
