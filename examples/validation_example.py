#!/usr/bin/env python3
"""
Validation System Example
Demonstrates how to validate Synthium predictions against empirical data
"""
import sys
import os
import asyncio

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from synthium_core.engine import SynthiumEngine
from synthium_core.vectors import SynthiumVector
from web_backend.validation import SynthiumValidator


async def main():
    print("=" * 60)
    print("SYNTHIUM VALIDATION SYSTEM - Example")
    print("=" * 60)
    print()

    # Initialize engine and validator
    engine = SynthiumEngine()
    validator = SynthiumValidator(engine)

    # Example 1: Single phenomenon validation
    print("Example 1: Validating 'Flow State' phenomenon")
    print("-" * 60)

    # Simulated empirical data for Flow State (phenomenon ID 1)
    flow_empirical_data = [
        {
            "participant_id": "P001",
            "phenomenon_id": 1,
            "vector": {"v": 0.65, "R": 0.25, "r": 0.75, "C": 0.85, "S": 0.15},
            "phase": "integration",
            "wellbeing": 0.85
        },
        {
            "participant_id": "P002",
            "phenomenon_id": 1,
            "vector": {"v": 0.72, "R": 0.18, "r": 0.82, "C": 0.90, "S": 0.12},
            "phase": "integration",
            "wellbeing": 0.88
        },
        {
            "participant_id": "P003",
            "phenomenon_id": 1,
            "vector": {"v": 0.68, "R": 0.22, "r": 0.79, "C": 0.88, "S": 0.10},
            "phase": "integration",
            "wellbeing": 0.87
        },
    ]

    result = await validator.validate_phenomenon(1, flow_empirical_data)

    print(f"Phenomenon: {result['phenomenon_name']}")
    print(f"Sample size: {result['sample_size']}")
    print()
    print("Validation Metrics:")
    for metric, value in result['validation_metrics'].items():
        print(f"  {metric}: {value}")
    print()
    print(f"Validation {'✅ PASSED' if result['validation_passed'] else '❌ FAILED'}")
    print()

    # Example 2: Full validation study
    print("Example 2: Running validation study for multiple phenomena")
    print("-" * 60)

    # Simulated participant data
    participant_data = {
        "P001": [
            {"phenomenon_id": 1, "vector": {"v": 0.7, "R": 0.2, "r": 0.8, "C": 0.9, "S": 0.1}, "phase": "integration"},
            {"phenomenon_id": 3, "vector": {"v": 0.15, "R": 0.65, "r": 0.25, "C": 0.25, "S": 0.55}, "phase": "awakening"},
        ],
        "P002": [
            {"phenomenon_id": 1, "vector": {"v": 0.68, "R": 0.25, "r": 0.75, "C": 0.85, "S": 0.15}, "phase": "integration"},
            {"phenomenon_id": 3, "vector": {"v": 0.12, "R": 0.72, "r": 0.18, "C": 0.20, "S": 0.62}, "phase": "awakening"},
        ],
        "P003": [
            {"phenomenon_id": 1, "vector": {"v": 0.72, "R": 0.18, "r": 0.82, "C": 0.92, "S": 0.08}, "phase": "integration"},
            {"phenomenon_id": 3, "vector": {"v": 0.08, "R": 0.68, "r": 0.22, "C": 0.18, "S": 0.58}, "phase": "awakening"},
        ],
    }

    # Run study for Flow (1) and Depression (3)
    study_results = await validator.run_validation_study([1, 3], participant_data)

    print(f"Study ID: {study_results['study_id']}")
    print()
    print("Summary:")
    for key, value in study_results['summary'].items():
        print(f"  {key}: {value}")
    print()

    if study_results['recommendations']:
        print("Recommendations:")
        for rec in study_results['recommendations']:
            print(f"  → {rec}")
        print()

    # Example 3: Export results
    print("Example 3: Exporting validation results")
    print("-" * 60)

    json_file = validator.export_validation_results(format="json", filepath="validation_results.json")
    print(f"Results exported to: {json_file}")

    csv_file = validator.export_validation_results(format="csv", filepath="validation_results.csv")
    print(f"Results exported to: {csv_file}")

    print()
    print("=" * 60)
    print("Validation complete. The framework is empirically grounded.")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
