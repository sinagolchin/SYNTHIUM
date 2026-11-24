"""
Synthium v4.0 - Confidence Tracking
====================================

Track confidence at all levels (from v3.4, enhanced for v4.0)
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional


class ConfidenceLevel(Enum):
    """Confidence in a measurement or formula"""
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"
    SPECULATIVE = "SPECULATIVE"


@dataclass
class Confidence:
    """
    Confidence in a measurement, formula, or prediction
    
    Tracks why we believe something and known limitations
    
    Example:
        >>> conf = Confidence(
        ...     level=ConfidenceLevel.MODERATE,
        ...     source="PCA analysis on 100 samples",
        ...     limitations=["Assumes linear structure"]
        ... )
    """
    level: ConfidenceLevel
    source: str
    limitations: List[str]
    
    def __str__(self):
        return f"{self.level.value}: {self.source}"


# Axiom 0: Agnosticism reminder
AXIOM_0_AGNOSTICISM = """
╔════════════════════════════════════════════════════════════════╗
║                    AXIOM 0: AGNOSTICISM                        ║
║                                                                ║
║         ALL FORMULAS ARE HYPOTHESES, NOT TRUTHS               ║
╚════════════════════════════════════════════════════════════════╝

Nothing in Synthium is absolute truth. All formulas, measurements, and 
predictions are HYPOTHESES that appear to work but may be wrong.

This includes:
• Discovered dimensions (they're estimates from finite data, not facts)
• Metric tensors (learned from limited observations)
• Geodesics (computed approximations, not absolute paths)
• All formulas (E, M, P, etc. - all mathematical guesses)
• All predictions (uncertain by nature)
• Even this axiom itself (it too could be wrong)

We remain epistemically humble. We don't know what we don't know.
We work with the best models available while acknowledging uncertainty.

Every formula is a lens, not the territory. Every measurement is approximate.
Every prediction is conditional. Every insight is provisional.

────────────────────────────────────────────────────────────────
"The first principle is that you must not fool yourself — and you 
 are the easiest person to fool."  
                                              - Richard Feynman
────────────────────────────────────────────────────────────────
"""


def aggregate_confidence(confidences: List[Confidence]) -> Confidence:
    """
    Aggregate multiple confidence levels
    
    Overall confidence = minimum of all inputs (weakest link principle)
    
    Args:
        confidences: List of Confidence objects
    
    Returns:
        Aggregated Confidence
    
    Example:
        >>> conf1 = Confidence(ConfidenceLevel.HIGH, "Direct measurement", [])
        >>> conf2 = Confidence(ConfidenceLevel.LOW, "Estimation", ["Limited data"])
        >>> overall = aggregate_confidence([conf1, conf2])
        >>> overall.level  # Will be LOW (weakest link)
    """
    if not confidences:
        return Confidence(
            level=ConfidenceLevel.SPECULATIVE, 
            source="No data", 
            limitations=["No measurements available"]
        )
    
    # Map confidence levels to numeric values
    level_map = {
        ConfidenceLevel.HIGH: 3,
        ConfidenceLevel.MODERATE: 2,
        ConfidenceLevel.LOW: 1,
        ConfidenceLevel.SPECULATIVE: 0
    }
    
    # Get numeric levels
    numeric_levels = [level_map[c.level] for c in confidences]
    min_level = min(numeric_levels)
    
    # Reverse map
    reverse_map = {v: k for k, v in level_map.items()}
    overall_level = reverse_map[min_level]
    
    # Aggregate sources and limitations
    sources = [c.source for c in confidences]
    all_limitations = []
    for c in confidences:
        all_limitations.extend(c.limitations)
    
    return Confidence(
        level=overall_level,
        source=f"Aggregated from: {', '.join(sources)}",
        limitations=list(set(all_limitations))  # Remove duplicates
    )


class FormulaConfidenceRegistry:
    """
    Registry of formula confidence levels
    
    Track which formulas are well-tested vs. speculative
    
    Example:
        >>> registry = FormulaConfidenceRegistry()
        >>> registry.register("enjoyment_formula", 
        ...     Confidence(ConfidenceLevel.SPECULATIVE, "Hypothesis", ["Not tested"]))
        >>> conf = registry.get("enjoyment_formula")
    """
    
    def __init__(self):
        self.registry = {}
    
    def register(self, formula_name: str, confidence: Confidence):
        """Register confidence for a formula"""
        self.registry[formula_name] = confidence
    
    def get(self, formula_name: str) -> Optional[Confidence]:
        """Get confidence for a formula"""
        return self.registry.get(formula_name)
    
    def list_all(self) -> dict:
        """List all registered formulas"""
        return self.registry.copy()


# Global registry
FORMULA_CONFIDENCE = FormulaConfidenceRegistry()

# Register known formulas
FORMULA_CONFIDENCE.register(
    "enjoyment_formula",
    Confidence(
        level=ConfidenceLevel.SPECULATIVE,
        source="Hypothetical formula E = 1 - (v·R + S)",
        limitations=[
            "Formula is a GUESS, not proven",
            "May be wrong functional form",
            "Thresholds are arbitrary",
            "Not tested on large datasets",
            "No empirical validation"
        ]
    )
)

FORMULA_CONFIDENCE.register(
    "dimensional_discovery_pca",
    Confidence(
        level=ConfidenceLevel.MODERATE,
        source="PCA-based dimensional discovery",
        limitations=[
            "Assumes linear structure",
            "Variance threshold is arbitrary",
            "May miss nonlinear dimensions",
            "Sensitive to preprocessing"
        ]
    )
)

FORMULA_CONFIDENCE.register(
    "metric_learning",
    Confidence(
        level=ConfidenceLevel.LOW,
        source="Learned from finite data",
        limitations=[
            "Metric may change with more data",
            "Assumes stationarity",
            "Regularization is arbitrary",
            "May overfit to training data"
        ]
    )
)

FORMULA_CONFIDENCE.register(
    "geodesic_computation",
    Confidence(
        level=ConfidenceLevel.MODERATE,
        source="Numerical approximation",
        limitations=[
            "Assumes constant metric",
            "Ignores curvature effects",
            "Discretization error",
            "May not be global minimum"
        ]
    )
)

FORMULA_CONFIDENCE.register(
    "chaos_detection",
    Confidence(
        level=ConfidenceLevel.LOW,
        source="6th derivative threshold",
        limitations=[
            "Threshold is arbitrary",
            "Numerical errors compound",
            "May miss subtle chaos",
            "False positives possible"
        ]
    )
)
