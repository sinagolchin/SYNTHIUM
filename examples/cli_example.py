#!/usr/bin/env python3
"""
Simple CLI example for Synthium Omega Prime
Demonstrates the core consciousness quantification capabilities
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from synthium_core.engine import SynthiumEngine
from synthium_core.vectors import SynthiumVector, PREDEFINED_VECTORS


def main():
    print("=" * 60)
    print("SYNTHIUM OMEGA PRIME - Command Line Interface")
    print("Created by Sina Golchin & Maysam BaygMuhammady")
    print("=" * 60)
    print()

    # Initialize engine
    engine = SynthiumEngine()

    # Example 1: Analyze a predefined state
    print("Example 1: Analyzing 'burnout' state")
    print("-" * 60)
    burnout_vector = PREDEFINED_VECTORS["burnout"]
    analysis = engine.analyze_state(burnout_vector)

    print(f"Vector: {burnout_vector}")
    print(f"Wellbeing Score: {analysis['wellbeing_score']}")
    print(f"Phase: {analysis['phase']}")
    print(f"Stability: {analysis['stability']}")
    print()
    print("Similar phenomena:")
    for p in analysis['similar_phenomena'][:3]:
        print(f"  - {p['phenomenon']} (similarity: {p['similarity']})")
    print()
    print("Insights:")
    for insight in analysis['insights']:
        print(f"  • {insight}")
    print()
    print("Recommendations:")
    for rec in analysis['recommendations']:
        print(f"  → {rec}")
    print()

    # Example 2: Create a transformation plan
    print("Example 2: Creating transformation from burnout to peace")
    print("-" * 60)
    current = PREDEFINED_VECTORS["burnout"]
    plan = engine.create_transformation_plan(current, "peace")

    print(f"Current: {current}")
    print(f"Target: peace")
    print(f"Distance: {plan['distance']}")
    print(f"Difficulty: {plan['estimated_difficulty']}")
    print()
    print("Transformation steps:")
    for i, step in enumerate(plan['steps'], 1):
        print(f"{i}. {step['dimension']}: {step['action']}")
        print(f"   (change needed: {step['change']:+.3f})")
    print()

    # Example 3: Explore phenomena
    print("Example 3: Exploring consciousness phenomena")
    print("-" * 60)
    mystical = engine.db.get_phenomena_by_tag("mystical")
    print(f"Found {len(mystical)} mystical phenomena:")
    for p in mystical:
        print(f"  - {p.term}: {p.description}")
    print()

    # Example 4: Custom vector
    print("Example 4: Analyzing a custom state")
    print("-" * 60)
    custom = SynthiumVector(
        v=0.8,  # High velocity (rushing)
        R=0.7,  # High resistance (blocked)
        r=0.3,  # Low resonance (disconnected)
        C=0.4,  # Moderate capacity
        S=0.8   # High entropy (chaotic)
    )
    analysis = engine.analyze_state(custom)
    print(f"Custom Vector: {custom}")
    print(f"Closest match: {analysis['similar_phenomena'][0]['phenomenon']}")
    print(f"  → {analysis['similar_phenomena'][0]['description']}")
    print()

    # Interactive mode
    print("=" * 60)
    print("Interactive Mode")
    print("=" * 60)
    print("Enter values for each dimension (0-1), or 'q' to quit")
    print()

    while True:
        try:
            print("Create a consciousness vector:")
            v = input("  Velocity (0=stuck, 1=rushing): ").strip()
            if v.lower() == 'q':
                break
            R = input("  Resistance (0=smooth, 1=blocked): ").strip()
            r = input("  Resonance (0=isolated, 1=connected): ").strip()
            C = input("  Capacity (0=depleted, 1=full): ").strip()
            S = input("  Entropy (0=ordered, 1=chaotic): ").strip()

            vector = SynthiumVector(
                v=float(v),
                R=float(R),
                r=float(r),
                C=float(C),
                S=float(S)
            )

            analysis = engine.analyze_state(vector)

            print()
            print(f"Analysis Results:")
            print(f"  Wellbeing: {analysis['wellbeing_score']:.3f}")
            print(f"  Phase: {analysis['phase']}")
            print(f"  Most similar: {analysis['similar_phenomena'][0]['phenomenon']}")
            print()
            print("  Recommendations:")
            for rec in analysis['recommendations'][:2]:
                print(f"    → {rec}")
            print()

        except (ValueError, EOFError, KeyboardInterrupt):
            break

    print()
    print("Tat tvam asi.")
    print()


if __name__ == "__main__":
    main()
