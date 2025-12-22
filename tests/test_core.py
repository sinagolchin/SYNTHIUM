"""
Basic tests for Synthium Core functionality
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from synthium_core.vectors import SynthiumVector, PREDEFINED_VECTORS
from synthium_core.engine import SynthiumEngine
from synthium_core.phenomena import CORE_PHENOMENA


def test_vector_creation():
    """Test basic vector creation and validation"""
    v = SynthiumVector(v=0.5, R=0.5, r=0.5, C=0.5, S=0.5)
    assert v.v == 0.5
    assert v.R == 0.5
    assert v.r == 0.5
    assert v.C == 0.5
    assert v.S == 0.5
    print("✓ Vector creation works")


def test_vector_clamping():
    """Test that vectors clamp to [0, 1]"""
    v = SynthiumVector(v=1.5, R=-0.5, r=0.5, C=0.5, S=0.5)
    assert v.v == 1.0  # Clamped to max
    assert v.R == 0.0  # Clamped to min
    print("✓ Vector clamping works")


def test_vector_distance():
    """Test distance calculation"""
    v1 = SynthiumVector(v=0, R=0, r=0, C=0, S=0)
    v2 = SynthiumVector(v=1, R=1, r=1, C=1, S=1)

    # Distance between opposite corners of unit hypercube
    import math
    expected = math.sqrt(5)
    assert abs(v1.distance_to(v2) - expected) < 0.001
    print("✓ Vector distance calculation works")


def test_vector_similarity():
    """Test similarity calculation"""
    v1 = SynthiumVector(v=0.5, R=0.5, r=0.5, C=0.5, S=0.5)
    v2 = SynthiumVector(v=0.5, R=0.5, r=0.5, C=0.5, S=0.5)

    # Identical vectors should have similarity 1.0
    assert abs(v1.similarity_to(v2) - 1.0) < 0.001
    print("✓ Vector similarity calculation works")


def test_predefined_vectors():
    """Test that predefined vectors exist"""
    assert "flow" in PREDEFINED_VECTORS
    assert "burnout" in PREDEFINED_VECTORS
    assert "peace" in PREDEFINED_VECTORS

    flow = PREDEFINED_VECTORS["flow"]
    assert isinstance(flow, SynthiumVector)
    print("✓ Predefined vectors exist")


def test_engine_initialization():
    """Test engine initialization"""
    engine = SynthiumEngine()
    assert engine.db is not None
    print("✓ Engine initialization works")


def test_analyze_state():
    """Test state analysis"""
    engine = SynthiumEngine()
    vector = PREDEFINED_VECTORS["flow"]

    analysis = engine.analyze_state(vector)

    assert "vector" in analysis
    assert "wellbeing_score" in analysis
    assert "phase" in analysis
    assert "similar_phenomena" in analysis
    assert "insights" in analysis
    assert "recommendations" in analysis

    # Flow should have high wellbeing
    assert analysis["wellbeing_score"] > 0.6

    print("✓ State analysis works")


def test_wellbeing_calculation():
    """Test wellbeing scoring"""
    engine = SynthiumEngine()

    # High wellbeing state
    good = SynthiumVector(v=0.5, R=0.1, r=0.9, C=0.9, S=0.1)
    score_good = engine.calculate_wellbeing(good)

    # Low wellbeing state
    bad = SynthiumVector(v=0.9, R=0.9, r=0.1, C=0.1, S=0.9)
    score_bad = engine.calculate_wellbeing(bad)

    assert score_good > score_bad
    assert 0 <= score_good <= 1
    assert 0 <= score_bad <= 1

    print("✓ Wellbeing calculation works")


def test_transformation_plan():
    """Test transformation plan creation"""
    engine = SynthiumEngine()

    current = PREDEFINED_VECTORS["burnout"]
    plan = engine.create_transformation_plan(current, "peace")

    assert "current_state" in plan
    assert "target_state" in plan
    assert "distance" in plan
    assert "steps" in plan
    assert len(plan["steps"]) > 0

    print("✓ Transformation planning works")


def test_phenomena_database():
    """Test phenomena database"""
    engine = SynthiumEngine()

    # Test getting by ID
    flow = engine.db.get_phenomenon(1)
    assert flow is not None
    assert flow.term == "Flow State"

    # Test getting by term
    peace = engine.db.get_phenomenon_by_term("Inner Peace")
    assert peace is not None

    # Test getting by phase
    transcendent = engine.db.get_phenomena_by_phase("transcendence")
    assert len(transcendent) > 0

    # Test getting by tag
    mystical = engine.db.get_phenomena_by_tag("mystical")
    assert len(mystical) > 0

    print("✓ Phenomena database works")


def test_find_similar():
    """Test finding similar phenomena"""
    engine = SynthiumEngine()

    # Create a vector similar to flow
    near_flow = SynthiumVector(v=0.65, R=0.25, r=0.75, C=0.85, S=0.15)

    similar = engine.db.find_similar_phenomena(near_flow, limit=3)

    assert len(similar) <= 3
    assert similar[0][0].term == "Flow State"  # Should match flow most closely

    print("✓ Similar phenomena finding works")


def test_core_phenomena_count():
    """Test that we have 20 core phenomena"""
    assert len(CORE_PHENOMENA) == 20
    print("✓ All 20 core phenomena present")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("SYNTHIUM CORE - Running Tests")
    print("=" * 60)
    print()

    tests = [
        test_vector_creation,
        test_vector_clamping,
        test_vector_distance,
        test_vector_similarity,
        test_predefined_vectors,
        test_engine_initialization,
        test_analyze_state,
        test_wellbeing_calculation,
        test_transformation_plan,
        test_phenomena_database,
        test_find_similar,
        test_core_phenomena_count,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1

    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
